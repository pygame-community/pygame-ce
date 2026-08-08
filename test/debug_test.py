import io
import os
import unittest
import unittest.mock

import pygame


class DebugTest(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout(self, expected_output, mock_stdout):
        pygame.print_debug_info()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_empty_stdout(self, filename_arg, fileobject_arg, mock_stdout):
        pygame.print_debug_info(filename_arg, fileobject_arg)
        self.assertEqual(mock_stdout.getvalue(), "")

    def test_print_debug(self):
        filename = "test_print_debug_temp_file.txt"

        try:
            pygame.print_debug_info(filename)
            with open(filename, "r") as temp_file:
                text = temp_file.read()

            self.assertNotEqual(text, "")
            self.assert_stdout(text)

        finally:
            if os.path.isfile(filename):
                os.remove(filename)

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

    def test_no_stdout(self):
        filename = "test_no_stdout_temp_file.txt"

        try:
            stringio = io.StringIO()

            self.assert_empty_stdout(filename, None)
            self.assert_empty_stdout(None, stringio)
            self.assert_empty_stdout(filename, stringio)

        finally:
            if os.path.isfile(filename):
                os.remove(filename)
