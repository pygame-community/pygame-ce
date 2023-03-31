import unittest
import pygame

pygame.init()


class WindowModuleTest(unittest.TestCase):
    def test_get_windows(self):
        pygame.display.set_mode((640, 480))

        window_list = [pygame.window.Window() for i in range(10)]

        window_from_display = pygame.window.Window.from_display_module()
        pygame.window.Window.from_display_module()
        pygame.window.Window.from_display_module()
        pygame.window.Window.from_display_module()

        got_windows = pygame.window.get_windows()
        for win in window_list:
            self.assertIn(win, got_windows)
        self.assertIn(window_from_display, got_windows)
        self.assertEqual(11, len(got_windows))

        for win in got_windows:
            win.destroy()
        got_windows = pygame.window.get_windows()
        self.assertEqual(0, len(got_windows))


class WindowFromDisplayTest(unittest.TestCase):
    def test_from_display_module(self):
        pygame.display.quit()
        pygame.display.set_mode((640, 480))

        win = pygame.window.Window.from_display_module()
        win2 = pygame.window.Window.from_display_module()
        self.assertIs(win, win2)

        # display should be quit after the window is destroyed
        win.destroy()
        self.assertFalse(pygame.display.get_init())


class WindowTypeTest(unittest.TestCase):
    def setUp(self):
        self.win = pygame.window.Window()

    def test_grab(self):
        self.win.set_grab(1)
        self.assertTrue(self.win.get_grab())
        self.win.set_grab(0)
        self.assertFalse(self.win.get_grab())

    def test_title(self):
        title = "Hello_World你好世界こにじわ"
        self.win.set_title(title)
        self.assertEqual(self.win.get_title(), title)

    def test_resizable(self):
        self.win.set_resizable(1)
        self.assertTrue(self.win.get_resizable())
        self.win.set_resizable(0)
        self.assertFalse(self.win.get_resizable())

    def test_borderless(self):
        self.win.set_borderless(1)
        self.assertTrue(self.win.get_borderless())
        self.win.set_borderless(0)
        self.assertFalse(self.win.get_borderless())

    def test_size(self):
        self.win.set_size((1280, 720))
        self.assertTupleEqual(self.win.get_size(), (1280, 720))

        self.assertRaises(ValueError, lambda: self.win.set_size((-1, 10)))
        self.assertRaises(ValueError, lambda: self.win.set_size((1, -10)))
        self.assertRaises(ValueError, lambda: self.win.set_size((-1, -10)))
        self.assertRaises(ValueError, lambda: self.win.set_size((0, 0)))

        self.win.set_size((640, 480))

    def test_position(self):
        self.win.set_position((12, 34))
        self.assertTupleEqual(self.win.get_position(), (12, 34))

        self.win.set_position(pygame.window.WINDOWPOS_CENTERED)

        # raise TypeError if input is some random number instead of flag
        self.assertRaises(TypeError, lambda: self.win.set_position(123))

    def test_opacity(self):
        self.win.set_opacity(0.5)
        self.assertEqual(self.win.get_opacity(), 0.5)
        self.win.set_opacity(0)
        self.assertEqual(self.win.get_opacity(), 0)
        self.win.set_opacity(1)
        self.assertEqual(self.win.get_opacity(), 1)

    @unittest.skipIf(
        pygame.version.get_sdl_version() < pygame.version.SDLVersion(2, 0, 16),
        "always_on_top requires SDL 2.0.16+",
    )
    def test_always_on_top(self):
        self.win.set_always_on_top(1)
        self.assertTrue(self.win.get_always_on_top())
        self.win.set_always_on_top(0)
        self.assertFalse(self.win.get_always_on_top())

    def tearDown(self):
        self.win.destroy()


class WindowSurfaceTest(unittest.TestCase):
    def setUp(self):
        self.win = pygame.window.Window()
        self.sf = self.win.get_surface()

    def test_surface_auto_resize(self):
        size = (360, 360)
        self.win.set_size(size)
        self.assertTupleEqual(self.sf.get_size(), size)
        size = (1280, 720)
        self.win.set_size(size)
        self.assertTupleEqual(self.sf.get_size(), size)
        size = (640, 640)
        self.win.set_size(size)
        self.assertTupleEqual(self.sf.get_size(), size)


if __name__ == "__main__":
    unittest.main()
