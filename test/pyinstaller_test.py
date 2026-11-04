import os
import subprocess
import sys
import tempfile
import unittest

import pygame
import pygame.examples


class PyinstallerTest(unittest.TestCase):
    """Tests that pygame-ce can be frozen into a standalone executable
    using PyInstaller.

    Note: PyInstaller cannot see into pygame-ce's editable-install import
    hook, so this test only reflects a normal (non-editable) install of
    pygame-ce, matching how CI and end users actually install the package.
    """

    def test_pyinstaller_build_and_run(self):
        """A minimal pygame-ce script can be frozen with PyInstaller and
        the resulting executable runs successfully (exit code 0)."""
        if any(name.endswith("_editable_loader") for name in sys.modules):
            self.skipTest(
                "pygame-ce is installed in editable mode; PyInstaller cannot "
                "see through the editable-install import hook to bundle it"
            )

        example_script = os.path.join(
            os.path.dirname(os.path.abspath(pygame.examples.__file__)),
            "headless_no_windows_needed.py",
        )
        self.assertTrue(
            os.path.isfile(example_script),
            f"expected example script not found: {example_script}",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            dist_path = os.path.join(tmp_dir, "dist")
            build_path = os.path.join(tmp_dir, "build")
            spec_path = tmp_dir

            build_cmd = [
                sys.executable,
                "-m",
                "PyInstaller",
                "--onefile",
                "--distpath",
                dist_path,
                "--workpath",
                build_path,
                "--specpath",
                spec_path,
                example_script,
            ]

            build_result = subprocess.run(
                build_cmd,
                timeout=120,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(
                build_result.returncode,
                0,
                f"PyInstaller build failed:\n{build_result.stderr.decode(errors='replace')}",
            )

            exe_name = "headless_no_windows_needed"
            if sys.platform == "win32":
                exe_name += ".exe"
            exe_path = os.path.join(dist_path, exe_name)

            self.assertTrue(
                os.path.isfile(exe_path),
                f"expected frozen executable not found: {exe_path}",
            )

            run_result = subprocess.run(
                [exe_path],
                timeout=30,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(
                run_result.returncode,
                0,
                f"frozen executable exited nonzero:\n{run_result.stderr.decode(errors='replace')}",
            )


if __name__ == "__main__":
    unittest.main()
