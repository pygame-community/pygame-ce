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

    def test_print_debug(self):
        text = pygame.get_debug_info()

        self.assertNotEqual(text, "")
        self.assert_stdout(text)
