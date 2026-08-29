import unittest

import pygame

try:
    import pygame._sdl3_mixer as mixer
except ImportError:
    mixer = None


@unittest.skipIf(mixer is None, "SDL3 mixer is not available")
class SDL3MixerModuleTest(unittest.TestCase):
    def tearDown(self):
        mixer.quit()

    def test_init_get_decoders_and_quit(self):
        mixer.quit()
        with self.assertRaises(pygame.error):
            mixer.get_decoders()

        mixer.init()
        self.assertIsInstance(mixer.get_decoders(), list)
        self.assertEqual(len(mixer.get_sdl_mixer_version()), 3)

        mixer.quit()
        with self.assertRaises(pygame.error):
            mixer.get_decoders()


if __name__ == "__main__":
    unittest.main()
