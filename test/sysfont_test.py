import unittest
import platform


class SysfontModuleTest(unittest.TestCase):
    def test_create_aliases(self):
        import pygame.sysfont

        pygame.sysfont.initsysfonts()
        pygame.sysfont.create_aliases()
        self.assertTrue(len(pygame.sysfont.Sysalias) > 0)

    def test_initsysfonts(self):
        import pygame.sysfont

        pygame.sysfont.initsysfonts()
        self.assertTrue(len(pygame.sysfont.get_fonts()) > 0)

    @unittest.skipIf("Darwin" not in platform.platform(), "Not mac we skip.")
    def test_initsysfonts_darwin(self):
        import pygame.sysfont

        self.assertTrue(len(pygame.sysfont.get_fonts()) > 10)

    def test_sysfont(self):
        import pygame.font

        pygame.font.init()
        arial = pygame.font.SysFont("Arial", 40)
        self.assertTrue(isinstance(arial, pygame.font.Font))

        pygame.font.SysFont(None, 40)

    @unittest.skipIf(
        ("Darwin" in platform.platform() or "Windows" in platform.platform()),
        "Not unix we skip.",
    )
    def test_initsysfonts_unix(self):
        import pygame.sysfont

        self.assertTrue(len(pygame.sysfont.get_fonts()) > 0)

    @unittest.skipIf("Windows" not in platform.platform(), "Not windows we skip.")
    def test_initsysfonts_win32(self):
        import pygame.sysfont

        self.assertTrue(len(pygame.sysfont.get_fonts()) > 10)

    def test_sysfont_warnings(self):
        import pygame.font

        pygame.font.init()

        with self.assertWarns(UserWarning):
            pygame.font.SysFont("non-existent font", 40)

        with self.assertWarns(UserWarning):
            pygame.font.SysFont(bytes("non-existent font", "utf-8"), 40)

        with self.assertWarns(UserWarning):
            pygame.font.SysFont(("non-existent font", "non-existent font2"), 40)

        with self.assertWarns(UserWarning):
            pygame.font.SysFont(
                (bytes("non-existent font", "utf-8"), "non-existent font2"), 40
            )


###############################################################################

if __name__ == "__main__":
    unittest.main()
