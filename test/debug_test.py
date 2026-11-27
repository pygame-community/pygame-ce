import io
import unittest
import unittest.mock

import pygame


class DebugTest(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout_equal(self, expected_output, mock_stdout):
        pygame.print_debug_info()
        # print_debug_info adds a newline when sending to stdout, so capture that
        self.assertEqual(mock_stdout.getvalue(), expected_output + "\n")

    def test_print_debug_info(self):
        self.maxDiff = None
        text = pygame.get_debug_info()

        self.assertNotEqual(text, "")
        self.assert_stdout_equal(text)
