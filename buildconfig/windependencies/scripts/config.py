from os.path import join

SDL2_IMAGE = "SDL2_image-2.7.0-pygame-ce"
SDL2_VERSION ='2.26.4'

DOWNLOAD = join("./prebuilt_downloads",f"{SDL2_IMAGE}_downloads")
BUILD = "./build"
IMAGE_SRC = join(BUILD, "SDL2_image")
OUTPUT_ZIP_PATH = join("./prebuilt_downloads", SDL2_IMAGE+".zip")

PREBUILT_64 = "./prebuilt-x64"
PREBUILT_86 = "./prebuilt-x86"

SDL2_PATH_64 = join(PREBUILT_64, f"SDL2-{SDL2_VERSION}")
SDL2_PATH_86 = join(PREBUILT_86, f"SDL2-{SDL2_VERSION}")
