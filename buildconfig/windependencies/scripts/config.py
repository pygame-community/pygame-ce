from os.path import join

DOWNLOAD = "./prebuilt_downloads/SDL_image_download"
BUILD = "./build"
IMAGE_SRC = join(BUILD, "SDL2_image")
OUTPUT_PATH = "./prebuilt_downloads"
OUTPUT_FILENAME = join(OUTPUT_PATH, "SDL2_image-2.7.0-pygame.zip")

PREBUILT_PATH_64 = "./prebuilt-x64"
PREBUILT_PATH_86 = "./prebuilt-x86"
OUTPUT_UNZIP_64 = join(PREBUILT_PATH_64, "SDL2_image-2.7.0-pygame")
OUTPUT_UNZIP_86 = join(PREBUILT_PATH_86, "SDL2_image-2.7.0-pygame")

SDL2_VERSION ='2.26.4'
SDL2_PATH_64 = join(PREBUILT_PATH_64, f"SDL2-{SDL2_VERSION}")
SDL2_PATH_86 = join(PREBUILT_PATH_86, f"SDL2-{SDL2_VERSION}")

