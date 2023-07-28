import unittest
import pygame
import os

from pygame._sdl2.video import Window
from pygame.version import SDL

pygame.init()


class WindowTypeTest(unittest.TestCase):
    DEFAULT_TITLE = "pygame window"

    def setUp(self):
        self.win = Window()

    @unittest.skipIf(
        os.environ.get("SDL_VIDEODRIVER") == "dummy",
        "requires the SDL_VIDEODRIVER to be a non dummy value",
    )
    def test_grab(self):
        self.win.grab = True
        self.assertTrue(self.win.grab)
        self.win.grab = False
        self.assertFalse(self.win.grab)

    def test_title(self):
        self.assertEqual(self.win.title, self.DEFAULT_TITLE)

        title = "Hello_World你好世界こにじわ"
        self.win.title = title
        self.assertEqual(self.win.title, title)

    @unittest.skipIf(
        os.environ.get("SDL_VIDEODRIVER") == "dummy",
        "requires the SDL_VIDEODRIVER to be a non dummy value",
    )
    def test_resizable(self):
        self.win.resizable = True
        self.assertTrue(self.win.resizable)
        self.win.resizable = False
        self.assertFalse(self.win.resizable)

    @unittest.skipIf(
        os.environ.get("SDL_VIDEODRIVER") == "dummy",
        "requires the SDL_VIDEODRIVER to be a non dummy value",
    )
    def test_borderless(self):
        self.win.borderless = True
        self.assertTrue(self.win.borderless)
        self.win.borderless = False
        self.assertFalse(self.win.borderless)

    @unittest.skipIf(
        os.environ.get("SDL_VIDEODRIVER") == "dummy",
        "requires the SDL_VIDEODRIVER to be a non dummy value",
    )
    @unittest.skipIf(
        SDL < (2, 0, 16),
        "requires SDL 2.0.16+",
    )
    def test_always_on_top(self):
        self.win.always_on_top = True
        self.assertTrue(self.win.always_on_top)
        self.win.always_on_top = False
        self.assertFalse(self.win.always_on_top)

    def test_size(self):
        self.win.size = (1280, 720)
        self.assertTupleEqual(self.win.size, (1280, 720))

        self.assertRaises(ValueError, lambda: setattr(self.win, "size", (-1, 10)))
        self.assertRaises(ValueError, lambda: setattr(self.win, "size", (1, -10)))
        self.assertRaises(ValueError, lambda: setattr(self.win, "size", (-1, -10)))
        self.assertRaises(ValueError, lambda: setattr(self.win, "size", (0, 0)))

        # test set size when init
        win = Window(size=(12, 34))
        self.assertTupleEqual((12, 34), win.size)
        win.destroy()

        self.assertRaises(ValueError, lambda: Window(size=(-1, 0)))

        self.win.size = (640, 480)

    def test_position(self):
        self.win.position = (12, 34)
        self.assertTupleEqual(self.win.position, (12, 34))

        self.win.position = pygame.WINDOWPOS_CENTERED

        # raise TypeError if input is some random number instead of flag
        self.assertRaises(TypeError, lambda: setattr(self.win, "position", 123))

        # test set position when init
        win = Window(position=(20, 48))
        self.assertTupleEqual((20, 48), win.position)
        win.destroy()

        self.assertRaises(TypeError, lambda: Window(position=123))

    @unittest.skipIf(
        os.environ.get("SDL_VIDEODRIVER") == "dummy",
        "requires the SDL_VIDEODRIVER to be a non dummy value",
    )
    def test_opacity(self):
        self.win.opacity = 0.5
        self.assertEqual(self.win.opacity, 0.5)
        self.win.opacity = 0
        self.assertEqual(self.win.opacity, 0)
        self.win.opacity = 1
        self.assertEqual(self.win.opacity, 1)

    @unittest.skipIf(
        os.environ.get("SDL_VIDEODRIVER") == "dummy",
        "requires the SDL_VIDEODRIVER to be a non dummy value",
    )
    def test_init_flags(self):
        # test borderless
        win = Window(borderless=True)
        self.assertTrue(win.borderless)
        win.destroy()

        # test resizable
        win = Window(resizable=True)
        self.assertTrue(win.resizable)
        win.destroy()

        self.assertRaises(TypeError, lambda: Window(aaa=True))
        self.assertRaises(TypeError, lambda: Window(aaa=False))

    def tearDown(self):
        self.win.destroy()


if __name__ == "__main__":
    unittest.main()
