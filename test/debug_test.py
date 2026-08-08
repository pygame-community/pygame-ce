import io
import unittest
import unittest.mock

import pygame


class DebugTest(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout(self, expected_output, mock_stdout):
        pygame.print_debug_info()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_print_debug(self):
        import os

        pygame.print_debug_info("temp_file.txt")
        with open("temp_file.txt", "r") as temp_file:
            text = temp_file.read()

        self.assertNotEqual(text, "")
        self.assert_stdout(text)

        os.remove("temp_file.txt")

    def test_iobase_debug(self):
        stringio = io.StringIO()
        bytestream = io.BytesIO()
        textiowrapper = io.TextIOWrapper(bytestream, "utf-8")

        pygame.print_debug_info(None, stringio)
        pygame.print_debug_info(None, textiowrapper)

        stringio.seek(0)
        textiowrapper.seek(0)

        stringio_text = stringio.read()
        textio_text = textiowrapper.read()

        self.assertEqual(stringio_text, textio_text)
        self.assertNotEqual("", stringio_text)

        self.assert_stdout(stringio_text)
