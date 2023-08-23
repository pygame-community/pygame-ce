import unittest
import pygame
import os

from pygame._sdl2.video import Window
from pygame.version import SDL

# os.environ["SDL_VIDEODRIVER"] = "dummy"

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
        # On Windows, if SDL <= 2.0.22, this test fails
        # This bug have been fixed in SDL 2.24.0
        if SDL > (2, 0, 22):
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

    def test_maximum_size(self):
        # Use a new window to prevent being influenced by other tests
        self.win = Window()

        self.win.maximum_size = (50, 50)
        self.assertTupleEqual(self.win.maximum_size, (50, 50))

        # size should be limited to the maximum_size
        self.assertTupleEqual(self.win.size, (50, 50))

        self.win.size = (640, 480)
        # size should not larger than maximum_size
        self.assertTupleEqual(self.win.size, (50, 50))

        if SDL.major >= 3:
            # This part should pass in SDL3
            self.win.maximum_size = (0, 0)  # remove the size limit
            self.win.size = (640, 480)
            self.assertTupleEqual(self.win.size, (640, 480))

        self.assertRaises(
            ValueError, lambda: setattr(self.win, "maximum_size", (-1, -1))
        )
        self.assertRaises(
            TypeError, lambda: setattr(self.win, "maximum_size", "dummy_str")
        )

    def test_minimum_size(self):
        # Use a new window to prevent being influenced by other tests
        self.win = Window()

        self.win.minimum_size = (700, 700)
        self.assertTupleEqual(self.win.minimum_size, (700, 700))

        # size should be limited to the minimum_size
        self.assertTupleEqual(self.win.size, (700, 700))

        self.win.size = (640, 480)
        # size should not small than minimum_size
        self.assertTupleEqual(self.win.size, (700, 700))

        if SDL.major >= 3:
            # This part should pass in SDL3
            self.win.minimum_size = (0, 0)  # remove the size limit
            self.win.size = (640, 480)
            self.assertTupleEqual(self.win.size, (640, 480))

        self.assertRaises(
            ValueError, lambda: setattr(self.win, "minimum_size", (-1, -1))
        )
        self.assertRaises(
            TypeError, lambda: setattr(self.win, "minimum_size", "dummy_str")
        )

    def test_min_size_interact_with_max_size(self):
        # Use a new window to prevent being influenced by other tests
        self.win = Window()

        self.win.maximum_size = (100, 100)
        # min size should not larger than max size
        self.assertRaises(
            ValueError, lambda: setattr(self.win, "minimum_size", (200, 200))
        )

        self.win.minimum_size = (90, 90)
        # max size should not smaller than min size
        self.assertRaises(
            ValueError, lambda: setattr(self.win, "maximum_size", (50, 50))
        )

        # minimum size should be able to equal to maxium size
        # This test fails in SDL <= 2.0.12
        # have been fixed after SDL 2.0.18
        if SDL >= (2, 0, 18):
            self.win.minimum_size = (60, 60)
            self.win.maximum_size = (60, 60)
            self.assertTupleEqual(self.win.maximum_size, (60, 60))
            self.assertTupleEqual(self.win.minimum_size, (60, 60))

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
        self.win.opacity = -0.1
        self.assertEqual(self.win.opacity, 0)
        self.win.opacity = 1.1
        self.assertEqual(self.win.opacity, 1)

        self.assertRaises(TypeError, lambda: setattr(self.win, "opacity", "dummy str"))

    def test_init_flags(self):
        # test borderless
        win = Window(borderless=True)
        self.assertTrue(win.borderless)
        win.destroy()

        # test always_on_top
        if SDL >= (2, 0, 16):
            win = Window(always_on_top=True)
            self.assertTrue(win.always_on_top)
            win.destroy()

        # test resizable
        win = Window(resizable=True)
        self.assertTrue(win.resizable)
        win.destroy()

        # should raise a TypeError if keyword is random
        self.assertRaises(TypeError, lambda: Window(aaa=True))
        self.assertRaises(TypeError, lambda: Window(aaa=False))

    def test_set_icon(self):
        self.assertRaises(TypeError, lambda: self.win.set_icon(1234))

        test_icon = pygame.Surface((32, 32))
        test_icon.fill((255, 0, 0))

        return_value = self.win.set_icon(test_icon)
        self.assertIsNone(return_value)

    def test_window_object_repr(self):
        win = Window("awa")
        self.assertEqual(repr(win), f"<Window(title='{win.title}', id={win.id})>")

        win.destroy()
        self.assertEqual(repr(win), "<Window(Destroyed)>")

        pygame.display.set_mode((640, 480))
        win = Window.from_display_module()
        self.assertEqual(repr(win), "<Window(From Display)>")

        pygame.display.quit()
        pygame.init()

    def test_from_display_module(self):
        pygame.display.set_mode((640, 480))

        win1 = Window.from_display_module()
        win2 = Window.from_display_module()

        self.assertIs(win1, win2)

        pygame.display.quit()
        pygame.init()

    def tearDown(self):
        self.win.destroy()


if __name__ == "__main__":
    unittest.main()
