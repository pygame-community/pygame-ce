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


class MessageBoxInteractiveTest(unittest.TestCase):
    __tags__ = ["interactive"]

    def test_message_box_type(self):
        result = pygame.display.message_box(
            "Test",
            "Is this an error message box?",
            type="error",
            buttons=("Yes", "No"),
        )
        self.assertEqual(result, 0)

        result = pygame.display.message_box(
            "Test",
            "Is this an info message box?",
            type="info",
            buttons=("Yes", "No"),
        )
        self.assertEqual(result, 0)

        result = pygame.display.message_box(
            "Test",
            "Is this a warn message box?",
            type="warn",
            buttons=("Yes", "No"),
        )
        self.assertEqual(result, 0)

    def test_message_box_buttons(self):
        result = pygame.display.message_box("Hit the 'OK' button")
        self.assertEqual(result, 0)

        result = pygame.display.message_box(
            "Hit the 'Hello' button",
            buttons=("Nope", "Nope", "Nope", "Hello", "Nope", "Nope"),
        )
        self.assertEqual(result, 3)

        result = pygame.display.message_box(
            "Press Enter on your keyboard",
            buttons=("O", "O", "O", "O", "O", "O"),
            return_button=4,
        )
        self.assertEqual(result, 4)

        result = pygame.display.message_box(
            "Press Esc on your keyboard",
            buttons=("O", "O", "O", "O", "O", "O"),
            escape_button=2,
        )
        self.assertEqual(result, 2)

        result = pygame.display.message_box(
            "Test",
            "You saw 'Yes' on the left and 'No' on the right. Is this correct?",
            buttons=("Yes", "No"),
        )
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
