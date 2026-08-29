"""
A helper script to run mypy stubtest on the stubs directory
"""

import os
import shutil
import subprocess
import sys
import tempfile

from pathlib import Path

STUBS_BASE_DIR = Path(__file__).parent


def selected_stub_check():
    """
    Verify that the root pygame stub matches the SDL major of the build.
    """
    import pygame

    sdl_major = pygame.get_sdl_version()[0]
    installed_stub = Path(pygame.__file__).with_name("__init__.pyi")
    if installed_stub.exists():
        root_stub = installed_stub
    else:
        stub_name = "__init__sdl3.pyi" if sdl_major == 3 else "__init__.pyi"
        root_stub = STUBS_BASE_DIR / "pygame" / stub_name

    if not root_stub.exists():
        raise RuntimeError(f"Could not find the selected root stub: {root_stub}")

    has_legacy_mixer = "from .mixer import" in root_stub.read_text(encoding="utf-8")
    if has_legacy_mixer != (sdl_major < 3):
        raise RuntimeError(
            f"Root stub {root_stub} does not match SDL{sdl_major} mixer exports"
        )


def typing_check():
    """
    Ensure type aliases in typing.py work as expected with type checkers
    """
    mypy_version_args = [sys.executable, "-m", "mypy"]
    try:
        version = subprocess.run(
                [*mypy_version_args, "--version"], capture_output=True, check=True, text=True
            ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: could not validate typing.py, make sure you have mypy installed")
        return

    mypy_args = [*mypy_version_args, "typing_sample_app.py"]
    cmd = " ".join(mypy_args)
    print(f"Using mypy invocation: `{cmd}` (version: {version})")
    prev_dir = os.getcwd()
    try:
        os.chdir(STUBS_BASE_DIR)
        returncode = subprocess.run([*mypy_args]).returncode
        if returncode != 0:
            raise RuntimeError(f"mypy process finished with unsuccessful return code {returncode}")
    finally:
        os.chdir(prev_dir)

def stubs_check():
    """
    Validate the stubs files
    """
    for stubtest in ([sys.executable, "-m", "mypy.stubtest"], ["stubtest"]):
        try:
            version = subprocess.run(
                [*stubtest, "--version"], capture_output=True, check=True, text=True
            ).stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

        cmd = " ".join(stubtest)
        print(f"Using stubtest invocation: `{cmd}` (version: {version})")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            temp_package = temp_path / "pygame"
            shutil.copytree(STUBS_BASE_DIR / "pygame", temp_package)
            sdl_major = __import__("pygame").get_sdl_version()[0]
            if sdl_major == 3:
                shutil.copyfile(
                    temp_package / "__init__sdl3.pyi",
                    temp_package / "__init__.pyi",
                )
                (temp_package / "__init__sdl3.pyi").unlink()
                shutil.rmtree(temp_package / "_sdl2")
                for module in ("mixer.pyi", "mixer_music.pyi", "sndarray.pyi"):
                    (temp_package / module).unlink()
            else:
                (temp_package / "__init__sdl3.pyi").unlink()
                for module in ("_audio.pyi", "_sdl3_mixer.pyi"):
                    (temp_package / module).unlink()
            allowlist = temp_path / "mypy_allow_list.txt"
            allowlist_lines = (STUBS_BASE_DIR / "mypy_allow_list.txt").read_text(
                encoding="utf-8"
            ).splitlines(keepends=True)
            if sdl_major == 3:
                allowlist_lines = [
                    line
                    for line in allowlist_lines
                    if not line.startswith("pygame\\._sdl2")
                ]
            allowlist.write_text("".join(allowlist_lines), encoding="utf-8")
            stubtest_modules = ["pygame"]
            if sdl_major == 3:
                stubtest_modules = []
                for stub in temp_package.rglob("*.pyi"):
                    module_parts = list(stub.relative_to(temp_path).with_suffix("").parts)
                    if module_parts[-1] == "__init__":
                        module_parts.pop()
                    if module_parts != ["pygame"]:
                        stubtest_modules.append(".".join(module_parts))
            stubtest_args = [
                *stubtest,
                *stubtest_modules,
                "--ignore-disjoint-bases",
                "--allowlist",
                str(allowlist),
            ]
            if sdl_major == 3:
                stubtest_args.extend(
                    ("--ignore-missing-stub", "--ignore-unused-allowlist")
                )
            sys.exit(
                subprocess.run(stubtest_args, cwd=temp_path).returncode
            )

    print("ERROR: Could not find a valid stubtest program.")
    print("Make sure you have mypy installed.")
    sys.exit(1)


def main():
    """
    Main entrypoint
    """
    selected_stub_check()
    typing_check()
    stubs_check()


if __name__ == "__main__":
    main()
