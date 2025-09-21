"""
Cleans self-built windows deps, to only retain what's needed for the build
"""

import sys
import pathlib
import shutil

base_dir = pathlib.Path(sys.argv[1])

# delete 'share' and 'cmake'
shutil.rmtree(base_dir / "share")
shutil.rmtree(base_dir / "cmake")


# delete all headers and import lib in 'include' and 'lib' except the ones we
# need
def clean_dir(dir: pathlib.Path, allowlist: set[str]):
    for path in dir.iterdir():
        if path.name in allowlist:
            continue

        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        except PermissionError:
            print(f"WARNING: Failed to remove '{path}'")
            pass


clean_dir(
    base_dir / "include",
    {
        "SDL2",
        "freetype2",
        "portmidi.h",
        "porttime.h",
        "pmutil.h",
        "strings.h",
    },
)

clean_dir(
    base_dir / "lib",
    {
        "libSDL2.dll.a",
        "SDL2.lib",
        "libSDL2_ttf.dll.a",
        "SDL2_ttf.lib",
        "libSDL2_image.dll.a",
        "SDL2_image.lib",
        "libSDL2_mixer.dll.a",
        "SDL2_mixer.lib",
        "libportmidi.dll.a",
        "portmidi.lib",
        "libfreetype.dll.a",
        "freetype.lib",
    },
)


# copy all dlls from 'bin' into 'lib', and then delete 'bin'
bindir = base_dir / "bin"
for dll in bindir.glob("*.dll"):
    shutil.copy(dll, base_dir / "lib")

try:
    shutil.rmtree(bindir)
except PermissionError:
    print(f"WARNING: Failed to remove '{bindir}'")
    pass
