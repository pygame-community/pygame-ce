import unittest

import pygame


class MessageBoxTest(unittest.TestCase):
    def test_messagebox_args(self):
        mb = pygame.display.message_box
        self.assertRaises(IndexError, lambda: mb("", escape_button=1))
        self.assertRaises(IndexError, lambda: mb("", escape_button=-1))
        self.assertRaises(IndexError, lambda: mb("", return_button=1))
        self.assertRaises(IndexError, lambda: mb("", return_button=-1))
        self.assertRaises(
            IndexError,
            lambda: mb("", buttons=("A", "B", "C"), return_button=10),
        )
        self.assertRaises(
            IndexError,
            lambda: mb("", buttons=("A", "B", "C"), return_button=-1),
        )
        self.assertRaises(
            IndexError,
            lambda: mb("", buttons=("A", "B", "C"), escape_button=10),
        )
        self.assertRaises(
            IndexError,
            lambda: mb("", buttons=("A", "B", "C"), escape_button=-1),
        )
        self.assertRaises(ValueError, lambda: mb("", type="random_str"))
        self.assertRaises(TypeError, lambda: mb("", buttons=()))
        self.assertRaises(TypeError, lambda: mb("", parent_window=123456))


if __name__ == "__main__":
    unittest.main()
