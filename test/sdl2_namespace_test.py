import unittest

import pygame


class SDL2NamespaceTest(unittest.TestCase):
    def test_namespace_matches_sdl_api(self):
        if pygame.get_sdl_version()[0] >= 3:
            with self.assertRaisesRegex(
                ImportError, "pygame\\._sdl2 is only available when pygame is built with SDL2"
            ):
                __import__("pygame._sdl2")
        else:
            __import__("pygame._sdl2")


if __name__ == "__main__":
    unittest.main()