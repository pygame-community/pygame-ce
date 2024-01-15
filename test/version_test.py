import os
import unittest

from importlib.metadata import version

import pygame

pg_header = os.path.join("src_c", "include", "_pygame.h")


class VersionTest(unittest.TestCase):
    @unittest.skipIf(
        not os.path.isfile(pg_header), "Skipping because we cannot find _pygame.h"
    )
    def test_pg_version_consistency(self):
        pgh_major = -1
        pgh_minor = -1
        pgh_patch = -1
        import re

        major_exp_search = re.compile(r"define\s+PG_MAJOR_VERSION\s+([0-9]+)").search
        minor_exp_search = re.compile(r"define\s+PG_MINOR_VERSION\s+([0-9]+)").search
        patch_exp_search = re.compile(r"define\s+PG_PATCH_VERSION\s+([0-9]+)").search
        with open(pg_header) as f:
            for line in f:
                if pgh_major == -1:
                    m = major_exp_search(line)
                    if m:
                        pgh_major = int(m.group(1))
                if pgh_minor == -1:
                    m = minor_exp_search(line)
                    if m:
                        pgh_minor = int(m.group(1))
                if pgh_patch == -1:
                    m = patch_exp_search(line)
                    if m:
                        pgh_patch = int(m.group(1))
        self.assertEqual(pgh_major, pygame.version.vernum[0])
        self.assertEqual(pgh_minor, pygame.version.vernum[1])
        self.assertEqual(pgh_patch, pygame.version.vernum[2])

    def test_sdl_version(self):
        self.assertEqual(len(pygame.version.SDL), 3)

    def test_installed_version_and_dunder(self):
        self.assertEqual(pygame.__version__, pygame.version.ver)
        self.assertEqual(pygame.__version__, version("pygame-ce"))


if __name__ == "__main__":
    unittest.main()
