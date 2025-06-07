"""
This script is aimed at making development more convenient by having all useful
development commands under one place.

For help on how to use this, do `python dev.py -h` to get a general overview
and `python dev.py [subcommand] -h` to get subcommand specific help.
"""

import argparse
import os
import re
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Union

MOD_NAME = "pygame-ce"
DIST_DIR = "dist"

VENV_NAME = "dev_venv"

source_tree = Path(__file__).parent
venv_path = source_tree / VENV_NAME
pyproject_path = source_tree / "pyproject.toml"

SDL3_ARGS = [
    "-Csetup-args=-Dsdl_api=3",
    "-Csetup-args=-Dmixer=disabled",
]
COVERAGE_ARGS = ["-Csetup-args=-Dcoverage=true"]

# We assume this script works with any pip version above this.
PIP_MIN_VERSION = "23.1"


class Colors(Enum):
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


# logic based on https://docs.python.org/3.13/using/cmdline.html#controlling-color
def has_color():
    # highest precedence
    python_colors = os.environ.get("PYTHON_COLORS", "").strip()
    if python_colors == "1":
        return True

    if python_colors == "0":
        return False

    # second highest precedence
    if "NO_COLOR" in os.environ:
        return False

    # third highest precedence
    if "FORCE_COLOR" in os.environ:
        return True

    # lowest precedence
    return os.environ.get("TERM", "").strip().lower() != "dumb"


def pprint(arg: str, col: Colors = Colors.YELLOW):
    do_col = has_color()
    start = Colors.BLUE.value if do_col else ""
    mid = col.value if do_col else ""
    end = Colors.RESET.value if do_col else ""
    print(f"{start}[dev.py] {mid}{arg}{end}", flush=True)


def cmd_run(
    cmd: list[Union[str, Path]],
    capture_output: bool = False,
    error_on_output: bool = False,
) -> str:
    if error_on_output:
        capture_output = True

    norm_cmd = [str(i) for i in cmd]
    pprint(f"> {' '.join(norm_cmd)}", Colors.CYAN)
    try:
        ret = subprocess.run(
            norm_cmd,
            stdout=subprocess.PIPE if capture_output else sys.stdout,
            stderr=subprocess.STDOUT,
            text=capture_output,
            cwd=source_tree,
        )
    except FileNotFoundError:
        pprint(f"{norm_cmd[0]}: command not found", Colors.RED)
        sys.exit(1)

    if ret.stdout:
        print(ret.stdout, end="", flush=True)

    if (error_on_output and ret.stdout) and not ret.returncode:
        # Convert success code to failure code if we have stdout and need to
        # error
        ret.returncode = 1

    ret.check_returncode()
    return ret.stdout


def pip_install(py: Path, args: list[str]):
    return cmd_run([py, "-m", "pip", "install", "-v", *args])


def get_pyproject_list_param(section: str, key: str) -> list[str]:
    with open(pyproject_path, "r", encoding="utf-8") as f:
        content = f.read()
        if sys.version_info >= (3, 11):
            import tomllib

            cur = tomllib.loads(content)
            for i in section.split("."):
                cur = cur[i]

            return cur[key]

        # hacky solution, because we don't have tomllib in stdlib on older
        # python versions
        import ast
        import re

        # this regex only works to extract a list, nothing else
        pattern = rf"\[{section}\].*\n\s*{key}\s*=\s*(\[.*?\])"
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return []

        return ast.literal_eval(match.group(1).strip())


def get_build_deps():
    return set(get_pyproject_list_param("build-system", "requires"))


def get_cibw_setup_args():
    return [
        f"-Csetup-args={i}"
        for i in get_pyproject_list_param(
            "tool.cibuildwheel.config-settings", "setup-args"
        )
    ]


def show_diff_and_suggest_fix(parent: str):
    try:
        cmd_run(["git", "status", "--porcelain"], error_on_output=True)
    except subprocess.CalledProcessError:
        try:
            cmd_run(["git", "diff"])
        finally:
            pprint(f"Running '{parent}' caused changes")
            pprint(f"You need to run `python3 dev.py {parent}` and commit the changes")
            pprint(
                "Alternatively, you may run `python3 dev.py all` to catch more issues"
            )
        raise


def check_version_atleast(version: str, min_version: str):
    try:
        version_tup = tuple(int(i.strip()) for i in version.split("."))
        min_version_tup = tuple(int(i.strip()) for i in min_version.split("."))
    except (AttributeError, TypeError, ValueError):
        return False

    return version_tup >= min_version_tup


def check_module_in_constraint(mod: str, constraint: str):
    constraint_mod = re.match(r"[a-z0-9._-]*", constraint.lower().strip())
    if not constraint_mod:
        return False

    return mod.lower().strip() == constraint_mod[0]


class Dev:
    def __init__(self) -> None:
        self.py: Path = Path(sys.executable)
        self.args: dict[str, Any] = {}

        self.deps: dict[str, set[str]] = {
            "build": get_build_deps(),
            "docs": get_build_deps(),
            "test": {"numpy"},
            "lint": {"pylint==3.3.1", "numpy"},
            "stubs": {"mypy==1.13.0", "numpy"},
            "format": {"pre-commit==4.0.1"},
        }
        self.deps["all"] = set()
        for k in self.deps.values():
            self.deps["all"] |= k

    def cmd_build(self):
        wheel_dir = self.args.get("wheel", DIST_DIR)
        debug = self.args.get("debug", False)
        lax = self.args.get("lax", False)
        sdl3 = self.args.get("sdl3", False)
        coverage = self.args.get("coverage", False)
        if wheel_dir and coverage:
            pprint("Cannot pass --wheel and --coverage together", Colors.RED)
            sys.exit(1)

        build_suffix = ""
        if debug:
            build_suffix += "-dbg"
        if lax:
            build_suffix += "-lax"
        if sdl3:
            build_suffix += "-sdl3"
        if coverage:
            build_suffix += "-cov"
        install_args = [
            "--no-build-isolation",
            f"-Cbuild-dir=.mesonpy-build{build_suffix}",
        ]

        if not wheel_dir:
            # editable install
            install_args.append("--editable")

        install_args.append(".")

        if debug:
            install_args.append("-Csetup-args=-Dbuildtype=debug")

        if not lax:
            # use the same flags as CI
            install_args.extend(get_cibw_setup_args())

        if sdl3:
            install_args.extend(SDL3_ARGS)

        if coverage:
            install_args.extend(COVERAGE_ARGS)

        info_str = f"with {debug=}, {lax=}, {sdl3=}, and {coverage=}"
        if wheel_dir:
            pprint(f"Building wheel at '{wheel_dir}' ({info_str})")
            cmd_run(
                [self.py, "-m", "pip", "wheel", "-v", "-w", wheel_dir, *install_args]
            )
            pprint("Installing wheel")
            pip_install(
                self.py, ["--no-index", "--force", "--find-links", wheel_dir, MOD_NAME]
            )
        else:
            pprint(f"Installing in editable mode ({info_str})")
            pip_install(self.py, install_args)

    def cmd_docs(self):
        full = self.args.get("full", False)

        pprint(f"Generating docs (with {full=})")
        extra_args = ["full_generation"] if full else []
        cmd_run([self.py, "buildconfig/make_docs.py", *extra_args])

        if "CI" in os.environ:
            show_diff_and_suggest_fix("docs")

    def cmd_lint(self):
        pprint("Linting code (with pylint)")
        cmd_run([self.py, "-m", "pylint", "src_py", "docs"])

    def cmd_stubs(self):
        pprint("Generating and testing type stubs (with mypy)")
        cmd_run([self.py, "buildconfig/stubs/gen_stubs.py"])
        if "CI" in os.environ:
            show_diff_and_suggest_fix("stubs")

        cmd_run([self.py, "buildconfig/stubs/stubcheck.py"])

    def cmd_format(self):
        pre_commit = self.py.parent / "pre-commit"

        pprint("Formatting code (with pre-commit)")
        try:
            cmd_run(
                [
                    pre_commit if pre_commit.exists() else "pre-commit",
                    "run",
                    "--all-files",
                ]
            )
        except subprocess.CalledProcessError:
            # pre_commit may set error code when it modifies a file, ignore it
            pass

        if "CI" in os.environ:
            show_diff_and_suggest_fix("format")

    def cmd_test(self):
        mod = self.args.get("mod", [])

        if mod:
            pprint(f"Running tests (with module(s): {' '.join(mod)})")
            for i in mod:
                cmd_run([self.py, "-m", f"pygame.tests.{i}_test"])
        else:
            pprint("Running tests (with all modules)")
            cmd_run([self.py, "-m", "pygame.tests"])

    def cmd_all(self):
        self.cmd_format()
        self.cmd_docs()
        self.cmd_build()
        self.cmd_stubs()
        self.cmd_lint()
        self.cmd_test()

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description=(
                "Build commands for the project. "
                "For more info on any subcommand you can run -h/--help on it like: "
                "dev.py build -h"
            )
        )
        subparsers = parser.add_subparsers(dest="command", required=True)

        parser.add_argument(
            "--venv",
            action="store_true",
            help="Make and use a venv (recommended, but not default)",
        )
        parser.add_argument(
            "--ignore-dep", action="append", help="Dependency to ignore in pip install"
        )

        # Build command
        build_parser = subparsers.add_parser("build", help="Build the project")
        build_parser.add_argument(
            "--wheel",
            nargs="?",
            const=DIST_DIR,  # Used if argument is provided without a value
            default="",  # Used if argument is not provided at all
            help=(
                "Generate a wheel and do a regular install from it. By default, this "
                "value is empty in which case the script does an 'editable' install. "
                "A value can passed optionally, to indicate the directory to place the "
                f"wheel (if not passed, '{DIST_DIR}' is used)"
            ),
        )
        build_parser.add_argument(
            "--debug",
            action="store_true",
            help="Install in debug mode (optimizations disabled and debug symbols enabled)",
        )
        build_parser.add_argument(
            "--lax",
            action="store_true",
            help="Be lax about build warnings, allow the build to succeed with them",
        )
        build_parser.add_argument(
            "--sdl3",
            action="store_true",
            help="Build against SDL3 instead of the default SDL2",
        )
        build_parser.add_argument(
            "--coverage",
            action="store_true",
            help=(
                "Do a coverage build. To generate a test coverage report, you need "
                "to compile pygame with this flag and run tests. This flag is only "
                "supported if the underlying compiler supports the --coverage argument"
            ),
        )

        # Docs command
        docs_parser = subparsers.add_parser("docs", help="Generate docs")
        docs_parser.add_argument(
            "--full",
            action="store_true",
            help="Force a full regeneration of docs, ignoring previous build cache",
        )

        # Test command
        test_parser = subparsers.add_parser("test", help="Run tests")
        test_parser.add_argument(
            "mod",
            nargs="*",
            help=(
                "Name(s) of sub-module(s) to test. If no args are given all are tested"
            ),
        )

        # Lint command
        subparsers.add_parser("lint", help="Lint code")

        # Stubs command
        subparsers.add_parser("stubs", help="Generate and test type stubs")

        # Format command
        subparsers.add_parser("format", help="Format code")

        # All command
        subparsers.add_parser(
            "all",
            help=(
                "Run all the subcommands. This is handy for checking that your work is "
                "ready to be submitted"
            ),
        )

        args = parser.parse_args()
        self.args = vars(args)

    def prep_env(self):
        if self.args["venv"]:
            if venv_path.is_dir():
                pprint(f"Using existing virtual environment '{venv_path}'")
            else:
                cmd_run([sys.executable, "-m", "venv", VENV_NAME])
                pprint(f"Virtual environment '{venv_path}' created")

            bin = venv_path / "Scripts" if os.name == "nt" else venv_path / "bin"
            self.py = bin / "python"
        else:
            pprint(f"Using python '{self.py}'")

        # set PATH to give high priority to executables in the python bin folder
        # this is where the binaries for meson/ninja/cython/sphinx/etc are installed
        os.environ["PATH"] = f"{self.py.parent}{os.pathsep}{os.environ.get('PATH', '')}"

        pprint("Checking pip version")
        pip_v = cmd_run([self.py, "-m", "pip", "-V"], capture_output=True)
        try:
            pip_version = pip_v.split()[1]
        except (AttributeError, IndexError):
            pip_version = "UNKNOWN"

        pprint(f"Determined pip version: {pip_version}")
        if not check_version_atleast(pip_version, PIP_MIN_VERSION):
            pprint("pip version is too old or unknown, attempting pip upgrade")
            pip_install(self.py, ["-U", "pip"])

        deps = self.deps.get(self.args["command"], set())
        ignored_deps = self.args["ignore_dep"]
        deps_filtered = deps.copy()
        if ignored_deps:
            for constr in deps:
                for dep in ignored_deps:
                    if check_module_in_constraint(dep, constr):
                        deps_filtered.remove(constr)
                        break

        if deps_filtered:
            pprint("Installing dependencies")
            pip_install(self.py, list(deps_filtered))

    def run(self):
        self.parse_args()
        self.prep_env()
        try:
            func = getattr(self, f"cmd_{self.args['command']}")
            func()
        except subprocess.CalledProcessError as e:
            pprint(f"Process exited with error code {e.returncode}", Colors.RED)
            sys.exit(e.returncode)
        except KeyboardInterrupt:
            pprint("Got KeyboardInterrupt, exiting", Colors.RED)
            sys.exit(1)

        pprint("Process exited successfully", Colors.GREEN)


if __name__ == "__main__":
    Dev().run()
