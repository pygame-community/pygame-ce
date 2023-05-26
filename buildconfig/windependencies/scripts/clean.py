import logging
import os
import shutil
from .config import IMAGE_SRC
from os.path import join

logger = logging.getLogger("Clean")


def clean(path, is_file):
    if os.path.exists(path):
        logger.info(f"Cleaning '{path}'")
        if is_file:
            os.remove(path)
        else:
            shutil.rmtree(path)


def main():
    cmake_cache_path = join(IMAGE_SRC, "build", "CMakeCache.txt")
    release_path = join(IMAGE_SRC, "build", "Release")
    external_path = join(IMAGE_SRC, "build", "external")

    clean(cmake_cache_path, is_file=True)
    clean(release_path, is_file=False)
    clean(external_path, is_file=False)
