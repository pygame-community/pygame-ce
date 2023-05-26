import zipfile
import logging
import os
import shutil
from os.path import join
from .config import DOWNLOAD, BUILD, SDL2_VERSION, PREBUILT_PATH_64, PREBUILT_PATH_86

logger = logging.getLogger("Extract")

extract_path = [
    ("SDL2_image", ""),
    ("libpng", "SDL2_image/external"),
    ("jpeg", "SDL2_image/external"),
    ("zlib", "SDL2_image/external"),
    ("libtiff", "SDL2_image/external"),
    ("libwebp", "SDL2_image/external"),
]

path_alias = {
    "SDL2_image": "SDL_image-d40d6cc94e4601b4d23e9e886bbe168fda567b20",
    "libpng": "libpng-999173059e2651fab2a0102eeba18748c4bd9827",
    "jpeg": "jpeg-bc27d050625f126dcba73ae5b731272de1a89dc1",
    "zlib": "zlib-f040d0cf7a553078a195d6c3af0ec78b14d4242e",
    "libtiff": "libtiff-dad25b3f71cfd7f4fcb089a5881a31e65ae92c0a",
    "libwebp": "libwebp-8333c34e62ff907112bb556aab2725164abdccfe",
}


def main(arch):
    if not os.path.exists(BUILD):
        os.mkdir(BUILD)

    for name, _path in extract_path:
        path = join(BUILD, _path, name)
        if os.path.exists(path):
            if os.path.exists(join(path, "CMakeLists.txt")) or name == "SDL2":
                logger.info(f"Skipping '{name}'")
                continue
            else:
                logger.info(f"Removeing '{path}'")
                shutil.rmtree(path)

        logger.info(f"Extracting '{name}.zip'")
        z = zipfile.ZipFile(join(DOWNLOAD, name + ".zip"), "r")
        z.extractall(join(BUILD, _path))
        logger.info(f"Renaming path...")
        os.rename(join(BUILD, _path, path_alias[name]), path)
    
    PREBUILT_PATH = {"x64":PREBUILT_PATH_64,"x86":PREBUILT_PATH_86}[arch]
    logger.info(f"Extracting 'SDL2-{SDL2_VERSION}.zip'")
    z = zipfile.ZipFile(join(DOWNLOAD, f'SDL2-{SDL2_VERSION}.zip'), "r")
    z.extractall(PREBUILT_PATH)

