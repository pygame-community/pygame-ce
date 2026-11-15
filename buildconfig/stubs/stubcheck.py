"""
A helper script to run mypy stubtest on the stubs directory
"""

import subprocess
import sys

from pathlib import Path

STUBS_BASE_DIR = Path(__file__).parent
ROOT_DIR = STUBS_BASE_DIR.parents[1]
ALLOW_LIST = STUBS_BASE_DIR / "mypy_allow_list.txt"


def typing_check():
    """
    Ensure type aliases in typing.py work as expected with type checkers
    """
    mypy_version_args = [sys.executable, "-m", "mypy"]
    try:
        version = subprocess.run(
                [*mypy_version_args, "--version"], capture_output=True, check=True, text=True
            ).stdout.strip()
    except subprocess.CalledProcessError:
        print("ERROR: could not validate typing.py, make sure you have mypy installed")
        return

    mypy_args = [*mypy_version_args, "."]
    cmd = " ".join(mypy_args)
    print(f"Using mypy invocation: `{cmd}` (version: {version})")
    returncode = subprocess.run([*mypy_args], cwd=ROOT_DIR).returncode
    if returncode != 0:
        raise RuntimeError(f"mypy process finished with unsuccessful return code {returncode}")

def stubs_check():
    """
    Validate the stubs files
    """
    for stubtest in ([sys.executable, "-m", "mypy.stubtest"], ["stubtest"]):
        try:
            version = subprocess.run(
                [*stubtest, "--version"], capture_output=True, check=True, text=True
            ).stdout.strip()
        except subprocess.CalledProcessError:
            continue

        cmd = " ".join(stubtest)
        print(f"Using stubtest invocation: `{cmd}` (version: {version})")
        sys.exit(
            subprocess.run(
                [
                    *stubtest,
                    "pygame",
                    "--ignore-disjoint-bases",
                    "--mypy-config-file",
                    "pyproject.toml",
                    "--allowlist",
                    str(ALLOW_LIST),
                ],
                cwd=ROOT_DIR,
            ).returncode
        )

    print("ERROR: Could not find a valid stubtest program.")
    print("Make sure you have mypy installed.")
    sys.exit(1)


def main():
    """
    Main entrypoint
    """
    typing_check()
    stubs_check()


if __name__ == "__main__":
    main()
