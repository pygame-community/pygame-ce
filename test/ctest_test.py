import unittest

base_ctest = None
try:
    import pygame.base_ctest as base_ctest
except ModuleNotFoundError:
    pass


class Ctest(unittest.TestCase):
    @unittest.skipIf(base_ctest is None, "base_ctest not built")
    def test_run_base_ctests(self):
        self.assertEqual(base_ctest.run_tests(), 0)


if __name__ == "__main__":
    unittest.main()
