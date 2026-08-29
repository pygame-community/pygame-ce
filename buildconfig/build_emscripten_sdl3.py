"""Build the pinned SDL3 dependency prefix used by WebAssembly builds."""

import argparse
import os
import shutil
import subprocess
from pathlib import Path


RELEASES = {
    "SDL": "3.4.0",
    "SDL_image": "3.4.0",
    "SDL_ttf": "3.2.2",
    "SDL_mixer": "3.2.2",
}


def run(command, cwd=None):
    print("+", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def checkout(source_root, project, version):
    source_dir = source_root / project
    if source_dir.exists():
        return source_dir
    run(
        [
            "git",
            "clone",
            "--branch",
            f"release-{version}",
            "--depth",
            "1",
            f"https://github.com/libsdl-org/{project}",
            str(source_dir),
        ]
    )
    return source_dir


def prepare_source(source_dir, paths=()):
    if (source_dir / ".gitmodules").is_file():
        run(
            [
                "git",
                "submodule",
                "update",
                "--init",
                "--depth",
                "1",
                "--",
                *paths,
            ],
            cwd=source_dir,
        )


def configure_and_install(
    source_dir, build_root, prefix, toolchain, options, cmake_prefix_path
):
    build_dir = build_root / source_dir.name
    if build_dir.exists():
        shutil.rmtree(build_dir)
    generator = "Ninja" if shutil.which("ninja") else "Unix Makefiles"
    command = [
        "cmake",
        "-S",
        str(source_dir),
        "-B",
        str(build_dir),
        "-G",
        generator,
        f"-DCMAKE_TOOLCHAIN_FILE={toolchain}",
        "-DCMAKE_BUILD_TYPE=Release",
        f"-DCMAKE_INSTALL_PREFIX={prefix}",
        "-DCMAKE_INSTALL_LIBDIR=lib",
        "-DBUILD_SHARED_LIBS=OFF",
        "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
        f"-DCMAKE_PREFIX_PATH={cmake_prefix_path}",
        f"-DSDL3_DIR={prefix / 'lib' / 'cmake' / 'SDL3'}",
        *options,
    ]
    run(command)
    run(["cmake", "--build", str(build_dir), "--parallel"])
    run(["cmake", "--install", str(build_dir)])
    library_dir = prefix / "lib"
    library_dir.mkdir(parents=True, exist_ok=True)
    for archive in build_dir.rglob("*.a"):
        shutil.copy2(archive, library_dir / archive.name)


def find_toolchain(emsdk_root):
    candidates = []
    if emsdk_root:
        candidates.append(Path(emsdk_root))
    if os.environ.get("EMSDK"):
        candidates.append(Path(os.environ["EMSDK"]))
    for root in candidates:
        toolchain = (
            root
            / "upstream"
            / "emscripten"
            / "cmake"
            / "Modules"
            / "Platform"
            / "Emscripten.cmake"
        )
        if toolchain.is_file():
            return toolchain.resolve()
    raise SystemExit(
        "Could not find Emscripten.cmake; pass --emsdk-root or set EMSDK."
    )


def verify_prefix(prefix):
    required = [
        prefix / "include" / "SDL3" / "SDL.h",
        prefix / "include" / "SDL3_image" / "SDL_image.h",
        prefix / "include" / "SDL3_ttf" / "SDL_ttf.h",
        prefix / "include" / "SDL3_mixer" / "SDL_mixer.h",
        prefix / "lib" / "libSDL3.a",
        prefix / "lib" / "libSDL3_image.a",
        prefix / "lib" / "libSDL3_ttf.a",
        prefix / "lib" / "libSDL3_mixer.a",
        prefix / "lib" / "libwebp.a",
        prefix / "lib" / "libsharpyuv.a",
        prefix / "lib" / "libwebpdemux.a",
        prefix / "lib" / "libwebpmux.a",
        prefix / "lib" / "libpng16.a",
        prefix / "lib" / "libzlibstatic.a",
        prefix / "lib" / "libfreetype.a",
        prefix / "lib" / "libharfbuzz.a",
        prefix / "lib" / "libplutosvg.a",
        prefix / "lib" / "libplutovg.a",
    ]
    missing = [path for path in required if not path.is_file()]
    if missing:
        raise SystemExit(
            "SDL3 Emscripten prefix is incomplete:\n"
            + "\n".join(f"- {path}" for path in missing)
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, default=Path(".cache/sdl3"))
    parser.add_argument("--build-root", type=Path, default=Path(".cache/sdl3-build"))
    parser.add_argument("--emsdk-root", type=Path)
    args = parser.parse_args()

    args.prefix = args.prefix.resolve()
    args.source_root = args.source_root.resolve()
    args.build_root = args.build_root.resolve()

    toolchain = find_toolchain(args.emsdk_root)
    args.prefix.mkdir(parents=True, exist_ok=True)
    args.source_root.mkdir(parents=True, exist_ok=True)
    args.build_root.mkdir(parents=True, exist_ok=True)

    sdl = checkout(args.source_root, "SDL", RELEASES["SDL"])
    prepare_source(sdl)
    configure_and_install(
        sdl,
        args.build_root,
        args.prefix,
        toolchain,
        [
            "-DSDL_TESTS=OFF",
            "-DSDL_EXAMPLES=OFF",
            "-DSDL_INSTALL_TESTS=OFF",
            "-DSDL_TEST_LIBRARY=OFF",
        ],
        args.prefix,
    )

    projects = [
        (
            "SDL_image",
            [
                "-DSDLIMAGE_VENDORED=ON",
                "-DSDLIMAGE_SAMPLES=OFF",
                "-DSDLIMAGE_TESTS=OFF",
                "-DSDLIMAGE_INSTALL=ON",
                "-DSDLIMAGE_INSTALL_CPACK=OFF",
                "-DSDLIMAGE_DEPS_SHARED=OFF",
                "-DSDLIMAGE_AVIF=OFF",
                "-DSDLIMAGE_JXL=OFF",
                "-DSDLIMAGE_TIF=OFF",
                "-DSDLIMAGE_PNG=ON",
                "-DSDLIMAGE_PNG_LIBPNG=ON",
                "-DSDLIMAGE_JPG=ON",
                "-DSDLIMAGE_BACKEND_STB=ON",
                "-DSDLIMAGE_WEBP=ON",
            ],
            ("external/libpng", "external/libwebp", "external/zlib"),
        ),
        (
            "SDL_ttf",
            [
                "-DSDLTTF_VENDORED=ON",
                "-DSDLTTF_SAMPLES=OFF",
                "-DSDLTTF_INSTALL=ON",
                "-DSDLTTF_INSTALL_CPACK=OFF",
                "-DSDLTTF_HARFBUZZ=ON",
                "-DSDLTTF_PLUTOSVG=ON",
                "-DCMAKE_CXX_FLAGS=-DHB_NO_PRAGMA_GCC_DIAGNOSTIC_ERROR -Wno-error=unused-template",
            ],
            ("external/freetype", "external/harfbuzz", "external/plutosvg", "external/plutovg"),
        ),
        (
            "SDL_mixer",
            [
                "-DSDLMIXER_VENDORED=ON",
                "-DSDLMIXER_EXAMPLES=OFF",
                "-DSDLMIXER_TESTS=OFF",
                "-DSDLMIXER_INSTALL=ON",
                "-DSDLMIXER_INSTALL_CPACK=OFF",
                "-DSDLMIXER_DEPS_SHARED=OFF",
                "-DSDLMIXER_OPUS=OFF",
                "-DSDLMIXER_VORBIS_VORBISFILE=OFF",
                "-DSDLMIXER_FLAC_LIBFLAC=OFF",
                "-DSDLMIXER_GME=OFF",
                "-DSDLMIXER_MOD_XMP=OFF",
                "-DSDLMIXER_MP3_MPG123=OFF",
                "-DSDLMIXER_MIDI_FLUIDSYNTH=OFF",
                "-DSDLMIXER_WAVPACK=OFF",
            ],
            (),
        ),
    ]
    for project, options, paths in projects:
        source_dir = checkout(args.source_root, project, RELEASES[project])
        prepare_source(source_dir, paths)
        configure_and_install(
            source_dir,
            args.build_root,
            args.prefix,
            toolchain,
            options,
            args.prefix,
        )

    verify_prefix(args.prefix)
    print(f"SDL3 Emscripten prefix ready: {args.prefix}")


if __name__ == "__main__":
    main()