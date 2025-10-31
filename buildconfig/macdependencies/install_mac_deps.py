"""
A python helper script to install built (cached) mac deps into /usr/local
"""

import shutil
import subprocess
import sys
from pathlib import Path


def rmpath(path: Path, verbose: bool = False):
    """
    Tries to remove a path of any kind
    """
    if path.is_symlink():
        if verbose:
            print(f"- Removing existing symlink at '{path}'")

        path.unlink()

    elif path.is_file():
        if verbose:
            print(f"- Removing existing file at '{path}'")

        path.unlink()

    elif path.is_dir():
        if verbose:
            print(f"- Removing existing directory at '{path}'")

        shutil.rmtree(path)


def merge_dylibs(out_dir: Path, x86_dir: Path, arm_dir: Path, verbose: bool = False):
    """
    Merge .dylib files from x86_64 into a copy of arm64 folder.
    - Moves arm_dir to out_dir.
    - For each .dylib in x86_dir, merges it with the arm64 one if present,
      otherwise just copies it over.
    - Deletes x86_dir after merging.
    """
    shutil.move(arm_dir, out_dir)
    if verbose:
        print(f"- Moved {arm_dir} -> {out_dir}")

    for x86_file in x86_dir.rglob("*.dylib"):
        rel_path = x86_file.relative_to(x86_dir)
        out_file = out_dir / rel_path
        if out_file.is_symlink():
            try:
                target = out_file.resolve(strict=True)
            except (FileNotFoundError, OSError):
                raise RuntimeError(f"Broken or bad symlink: {rel_path}")

            if not target.is_relative_to(out_dir):
                raise RuntimeError(
                    f"Unsafe symlink: {rel_path} points to {target} (outside {out_dir})"
                )

            if verbose:
                print(f"- Skipped symlink: {rel_path}")
            continue

        if out_file.exists():
            subprocess.run(
                ["lipo", "-create", "-output", out_file, out_file, x86_file], check=True
            )
            if verbose:
                print(f"- Merged: {rel_path}")
        else:
            out_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(x86_file, out_file)
            if verbose:
                print(f"- Copied x86-only: {rel_path}")

    shutil.rmtree(x86_dir)
    if verbose:
        print(f"- Deleted {x86_dir}")


def symtree(srcdir: Path, destdir: Path, verbose: bool = False):
    """
    This function creates symlinks pointing to srcdir, from destdir, such that
    existing folders and files in the tree of destdir are retained
    """
    if not destdir.is_dir():
        # dest dir does not exist at all, create dir symlink
        rmpath(destdir, verbose)
        if verbose:
            print(
                f"- Creating directory symlink from '{destdir}' pointing to '{srcdir}'"
            )

        destdir.symlink_to(srcdir)
        return

    for path in srcdir.glob("*"):
        destpath = destdir / path.name
        if path.is_dir():
            symtree(path, destpath, verbose)
        else:
            rmpath(destpath, verbose)
            if verbose:
                print(f"- Creating file symlink from '{destpath}' pointing to '{path}'")

            destpath.symlink_to(path)


if __name__ == "__main__":
    out_dir, x86_dir, arm_dir = map(Path, sys.argv[1:])
    try:
        merge_dylibs(out_dir, x86_dir, arm_dir, verbose=True)
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    symtree(out_dir, Path("/usr/local"), verbose=True)
