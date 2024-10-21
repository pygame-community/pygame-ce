"""
Cleans self-built windows deps, to only retain what's needed for the build
"""

import sys
import pathlib
import shutil

base_dir = pathlib.Path(sys.argv[1])

# delete 'share' and 'man'
shutil.rmtree(base_dir / "share")
shutil.rmtree(base_dir / "man")


# delete all headers and import lib in 'include' and 'lib' except the ones we
# need
def clean_dir(dir: pathlib.Path, allowlist: set[str]):
    for path in dir.iterdir():
        if path.name in allowlist:
            continue

        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


clean_dir(
    base_dir / "include",
    {
        "SDL2",
        "freetype2",
        "portmidi.h",
        "porttime.h",
        "pmutil.h",
    },
)

clean_dir(
    base_dir / "lib",
    {
        "libSDL2.dll.a",
        "libSDL2_ttf.dll.a",
        "libSDL2_image.dll.a",
        "libSDL2_mixer.dll.a",
        "libportmidi.dll.a",
        "libfreetype.dll.a",
    },
)


# copy all dlls from 'bin' into 'lib', and then delete 'bin'
bindir = base_dir / "bin"
for dll in bindir.glob("*.dll"):
    shutil.copy(dll, base_dir / "lib")

shutil.rmtree(bindir)
