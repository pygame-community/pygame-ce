import platform
import unittest
import sys
import pygame

from pygame._sdl2 import video


IS_PYPY = "PyPy" == platform.python_implementation()


class VideoModuleTest(unittest.TestCase):
    default_caption = "pygame window"

    @unittest.skipIf(
        not (sys.maxsize > 2**32),
        "32 bit SDL 2.0.16 has an issue.",
    )
    def test_renderer_set_viewport(self):
        """works."""
        window = video.Window(title=self.default_caption, size=(800, 600))
        renderer = video.Renderer(window=window)
        renderer.logical_size = (1920, 1080)
        rect = pygame.Rect(0, 0, 1920, 1080)
        renderer.set_viewport(rect)
        self.assertEqual(renderer.get_viewport(), (0, 0, 1920, 1080))

    @unittest.skipIf(IS_PYPY, "PyPy doesn't have sys.getrefcount")
    def test_renderer_to_surface_refcount(self):
        """Make sure to_surface doesn't leak memory due to reference counting."""
        window = video.Window(title=self.default_caption, size=(800, 600))
        renderer = video.Renderer(window=window)
        surface = pygame.Surface(window.size)

        # directly getting a refcount returns the actual refcount
        # as opposed to using an itermediate variable where it's 1 more than expected
        self.assertEqual(sys.getrefcount(renderer.to_surface()), 1)
        self.assertEqual(sys.getrefcount(renderer.to_surface(surface=surface)), 2)


if __name__ == "__main__":
    unittest.main()
