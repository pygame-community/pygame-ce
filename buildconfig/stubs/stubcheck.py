"""
A helper script to run mypy stubtest on the stubs directory
"""

import os
import subprocess
import sys

from pathlib import Path

STUBS_BASE_DIR = Path(__file__).parent


def main():
    """
    Main entrypoint
    """
    for stubtest in ([sys.executable, "-m", "mypy.stubtest"], ["stubtest"]):
        try:
            version = subprocess.run(
                [*stubtest, "--version"], capture_output=True, check=True, text=True
            ).stdout.strip()
        except subprocess.CalledProcessError:
            continue

        cmd = " ".join(stubtest)
        print(f"Using stubtest invokation: `{cmd}` (version: {version})")
        prev_dir = os.getcwd()
        try:
            os.chdir(STUBS_BASE_DIR)
            sys.exit(
                subprocess.run(
                    [*stubtest, "pygame", "--allowlist", "mypy_allow_list.txt"]
                ).returncode
            )
        finally:
            os.chdir(prev_dir)

    print("ERROR: Could not find a valid stubtest program.")
    print("Make sure you have mypy installed.")
    sys.exit(1)


if __name__ == "__main__":
    main()
