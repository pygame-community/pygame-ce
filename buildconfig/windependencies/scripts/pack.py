import logging
import zipfile
import os
from os.path import join
from .config import OUTPUT_ZIP_PATH, IMAGE_SRC, PREBUILT_64, PREBUILT_86, SDL2_IMAGE

logger = logging.getLogger("Pack")

lib_path_map = [
    ("build/Release/SDL2_image.dll", "SDL2_image.dll"),
    ("build/Release/SDL2_image.lib", "SDL2_image.lib"),
    ("build/external/libpng/Release/libpng16.dll", "libpng16.dll"),
    ("build/external/libtiff/libtiff/Release/tiff.dll", "tiff.dll"),
    ("build/external/zlib/Release/zlib1.dll", "zlib1.dll"),
]

include_path_map = [
    ("SDL_image.h", "SDL_image.h"),
]

license_path_map = [
    ("LICENSE.txt", "LICENSE-SDL2_image"),
    ("external/libpng/LICENSE", "LICENSE-libpng"),
    ("external/libwebp/COPYING", "LICENSE-libwebp"),
    ("external/jpeg/README", "LICENSE-jpeg"),
    ("external/libtiff/README.md", "LICENSE-libtiff"),
    ("external/zlib/README", "LICENSE-zlib"),
]


def write_zip(path_map, path_in_zip):
    with zipfile.ZipFile(OUTPUT_ZIP_PATH, "a") as pack:
        for path, arc in path_map:
            logger.info(f"Adding '{join(IMAGE_SRC,path)}' to pack.")
            pack.write(join(IMAGE_SRC, path), join(path_in_zip, arc))

def unzip(arch):
    PREBUILT_PATH = {"x64":PREBUILT_64,"x86":PREBUILT_86}[arch]
    logger.info(f"Extracting pack to '{join(PREBUILT_PATH,SDL2_IMAGE)}'")
    with zipfile.ZipFile(OUTPUT_ZIP_PATH, "r") as pack:
        pack.extractall(join(PREBUILT_PATH,SDL2_IMAGE))

def main(target, arch=None):
    if not os.path.exists("./dist"):
        os.makedirs("./dist")

    if target == "clear":
        with zipfile.ZipFile(OUTPUT_ZIP_PATH, "w"):
            pass
    
    elif target == "unzip":
        if arch is None:
            raise ValueError("arch must be specified")
        unzip(arch)

    elif target == "libx64":
        write_zip(lib_path_map, "lib/x64/")
    elif target == "libx86":
        write_zip(lib_path_map, "lib/x86/")
    elif target == "include":
        write_zip(include_path_map, "include/")
    elif target == "license":
        write_zip(license_path_map, "license/")
    else:
        raise ValueError("Unknown target")
