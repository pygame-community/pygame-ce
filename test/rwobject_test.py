import io
import pathlib
import platform
import sys
import unittest

import pygame
from pygame import encode_file_path, encode_string
from pygame.tests.test_utils import example_path

IS_PYPY = "PyPy" == platform.python_implementation()


class RWopsEncodeStringTest(unittest.TestCase):
    def test_obj_None(self):
        encoded_string = encode_string(None)

        self.assertIsNone(encoded_string)

    def test_returns_bytes(self):
        u = "Hello"
        encoded_string = encode_string(u)

        self.assertIsInstance(encoded_string, bytes)

    def test_obj_bytes(self):
        b = b"encyclop\xe6dia"
        encoded_string = encode_string(b, "ascii", "strict")

        self.assertIs(encoded_string, b)

    def test_encode_unicode(self):
        u = "\u00dee Olde Komp\u00fcter Shoppe"
        b = u.encode("utf-8")
        self.assertEqual(encode_string(u, "utf-8"), b)

    def test_error_fowarding(self):
        self.assertRaises(SyntaxError, encode_string)

    def test_errors(self):
        u = "abc\u0109defg\u011dh\u0125ij\u0135klmnoprs\u015dtu\u016dvz"
        b = u.encode("ascii", "ignore")
        self.assertEqual(encode_string(u, "ascii", "ignore"), b)

    def test_encoding_error(self):
        u = "a\x80b"
        encoded_string = encode_string(u, "ascii", "strict")

        self.assertIsNone(encoded_string)

    def test_check_defaults(self):
        u = "a\u01f7b"
        b = u.encode("unicode_escape", "backslashreplace")
        encoded_string = encode_string(u)

        self.assertEqual(encoded_string, b)

    def test_etype(self):
        u = "a\x80b"
        self.assertRaises(SyntaxError, encode_string, u, "ascii", "strict", SyntaxError)

    def test_etype__invalid(self):
        """Ensures invalid etypes are properly handled."""

        for etype in ("SyntaxError", self):
            self.assertRaises(TypeError, encode_string, "test", etype=etype)

    def test_string_with_null_bytes(self):
        b = b"a\x00b\x00c"
        encoded_string = encode_string(b, etype=SyntaxError)
        encoded_decode_string = encode_string(b.decode(), "ascii", "strict")

        self.assertIs(encoded_string, b)
        self.assertEqual(encoded_decode_string, b)

    @unittest.skipIf(IS_PYPY, "getrefcount not available on pypy")
    def test_refcount(self):
        bpath = b" This is a string that is not cached."[1:]
        upath = bpath.decode("ascii")
        before = sys.getrefcount(bpath)
        bpath = encode_string(bpath)
        self.assertEqual(sys.getrefcount(bpath), before)
        bpath = encode_string(upath)
        self.assertIn(sys.getrefcount(bpath), (before, before - 1))

    def test_smp(self):
        utf_8 = b"a\xf0\x93\x82\xa7b"
        u = "a\U000130a7b"
        b = encode_string(u, "utf-8", "strict", AssertionError)
        self.assertEqual(b, utf_8)

    def test_pathlib_obj(self):
        """Test loading string representation of pathlib object"""
        """
        We do this because pygame functions internally use pg_EncodeString
        to decode the filenames passed to them. So if we test that here, we
        can safely assume that all those functions do not have any issues
        with pathlib objects
        """
        encoded = encode_string(pathlib.PurePath("foo"), "utf-8")
        self.assertEqual(encoded, b"foo")

        encoded = encode_string(pathlib.Path("baz"))
        self.assertEqual(encoded, b"baz")


class RWopsEncodeFilePathTest(unittest.TestCase):
    # Most tests can be skipped since RWopsEncodeFilePath wraps
    # RWopsEncodeString
    def test_encoding(self):
        u = "Hello"
        encoded_file_path = encode_file_path(u)

        self.assertIsInstance(encoded_file_path, bytes)

    def test_error_fowarding(self):
        self.assertRaises(SyntaxError, encode_file_path)

    def test_path_with_null_bytes(self):
        b = b"a\x00b\x00c"
        encoded_file_path = encode_file_path(b)

        self.assertIsNone(encoded_file_path)

    def test_etype(self):
        b = b"a\x00b\x00c"
        self.assertRaises(TypeError, encode_file_path, b, TypeError)

    def test_etype__invalid(self):
        """Ensures invalid etypes are properly handled."""

        for etype in ("SyntaxError", self):
            self.assertRaises(TypeError, encode_file_path, "test", etype)


class FailingFileObject:
    """File-like object that raises a Python exception on a selected operation."""

    def __init__(self, operation, exception):
        with open(example_path("data/alien1.png"), "rb") as f:
            self._file = io.BytesIO(f.read())

        self._operation = operation
        self._exception = exception

    def read(self, *args, **kwargs):
        if self._operation == "read":
            raise self._exception
        return self._file.read(*args, **kwargs)

    def write(self, *args, **kwargs):
        if self._operation == "write":
            raise self._exception
        return self._file.write(*args, **kwargs)

    def seek(self, *args, **kwargs):
        if self._operation == "seek":
            raise self._exception
        return self._file.seek(*args, **kwargs)

    def tell(self):
        return self._file.tell()

    def flush(self):
        return self._file.flush()

    def close(self):
        return self._file.close()


class RWopsUnderlyingFileErrorTest(unittest.TestCase):
    """
    Test Python exceptions from file-like object operations.
    """

    def test_read_error(self):
        error = RuntimeError("read operation failed")

        with self.assertRaises(pygame.error):
            pygame.image.load(FailingFileObject("read", error))

    def test_write_error(self):
        error = RuntimeError("write operation failed")
        surface = pygame.Surface((10, 10))
        with self.assertRaises(pygame.error) as context:
            pygame.image.save(
                surface,
                FailingFileObject("write", error),
            )

        # SDL_image forwards the underlying error message in the save path
        # for now, but if this changes in the future the below assertion is
        # safe to remove
        self.assertIn(str(error), str(context.exception))

    def test_seek_error(self):
        error = RuntimeError("seek operation failed")

        with self.assertRaises(pygame.error):
            pygame.image.load(FailingFileObject("seek", error))


if __name__ == "__main__":
    unittest.main()
