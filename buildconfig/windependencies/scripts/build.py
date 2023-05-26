import logging
import subprocess
from subprocess import PIPE, STDOUT
import time
from os.path import join
from .config import IMAGE_SRC, SDL2_PATH_64, SDL2_PATH_86

logger = logging.getLogger("Build")


def get_cmd_config(arch):
    SDL2_PATH = {"x64":SDL2_PATH_64,"x86":SDL2_PATH_86}[arch[0]]
    return [
        "cmake",
        "--no-warn-unused-cli",
        f"-S{IMAGE_SRC}",
        f"-B{join(IMAGE_SRC,'build')}",
        "-G Visual Studio 16 2019",
        f"-T host={arch[0]}",
        f"-A {arch[1]}",
        "-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE",
        "-DSDL2IMAGE_BACKEND_STB=OFF",
        "-DSDL2IMAGE_TIF=ON",
        "-DSDL2IMAGE_WEBP=ON",
        "-DSDL2IMAGE_JPG_SHARED=OFF",
        "-DSDL2IMAGE_WEBP_SHARED=OFF",
        f"-DSDL2_DIR={SDL2_PATH}",
        f"-DSDL2_INCLUDE_DIR={join(SDL2_PATH,'include')}",
        f"-DSDL2_LIBRARY={join(SDL2_PATH,f'lib/{arch[0]}/SDL2.lib')}",
        f"-DSDL2_MAIN_LIBRARY={join(SDL2_PATH,f'lib/{arch[0]}/SDL2main.lib')}",
        "-DAWK=AWK-NOTFOUND",
    ]


cmd_build = f"cmake --build {join(IMAGE_SRC,'build')} --config Release --target SDL2_image -j 18 --"


def run_cmd(cmd):
    logger.info(f"Executing command {cmd}")
    with subprocess.Popen(cmd, text=True, stdout=PIPE, stderr=STDOUT, encoding="utf8") as proc:
        while proc.poll() is None:
            line = proc.stdout.readline()
            logger.info(line.rstrip())
        line = proc.stdout.readline()
        logger.info(line.rstrip())
        if proc.poll() == 0:
            logger.info(f"Command returns with an exit code: 0")
        else:
            logger.error(f"Command returns with an exit code: {proc.poll()}")
            raise OSError(f"Failed to execute command {cmd}")


def main(arch):
    if arch == "x64":
        _arch = ("x64", "x64")
    elif arch == "x86":
        _arch = ("x86", "win32")
    else:
        raise ValueError("Unknown arch")
    run_cmd(get_cmd_config(_arch))
    run_cmd(cmd_build)
