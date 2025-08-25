#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

SDL2_VER="2.32.8"
SDL2="SDL2-$SDL2_VER"
IMG2_VER="2.8.8"
IMG2="SDL2_image-$IMG2_VER"
TTF2_VER="2.24.0"
TTF2="SDL2_ttf-$TTF2_VER"
MIX2_VER="2.8.1"
MIX2="SDL2_mixer-$MIX2_VER"


# Download
curl -sL --retry 10 https://github.com/libsdl-org/SDL/releases/download/release-$SDL2_VER/$SDL2.tar.gz > ${SDL2}.tar.gz
curl -sL --retry 10 https://github.com/libsdl-org/SDL_image/releases/download/release-$IMG2_VER/$IMG2.tar.gz > ${IMG2}.tar.gz
curl -sL --retry 10 https://github.com/libsdl-org/SDL_mixer/releases/download/release-$MIX2_VER/$MIX2.tar.gz > ${MIX2}.tar.gz
curl -sL --retry 10 https://github.com/libsdl-org/SDL_ttf/releases/download/release-$TTF2_VER/$TTF2.tar.gz > ${TTF2}.tar.gz
sha512sum -c sdl2.sha512

# On mac/manylinux we have to make use of standard dynamic linking rather than
# dlopen-ing the library itself. This is important for when auditwheel/delocate
# moves libraries into the wheel.
PG_DEPS_SHARED=0

# Build SDL
tar xzf ${SDL2}.tar.gz

# this is for renaming the tip.tar.gz
# mv SDL-* ${SDL2}

if [[ "$MAC_ARCH" == "arm64" ]]; then
    # Build SDL with ARM optimisations on M1 macs
    export ARM_EXTRA_FLAGS="-DSDL_ARMSIMD=1 -DSDL_ARMNEON=1"
fi

cd $SDL2
mkdir builddir && cd builddir

cmake -S .. -B . $PG_BASE_CMAKE_FLAGS -DSDL_VULKAN=0 $ARM_EXTRA_FLAGS
make
make install

cd ../..


# Build SDL_image
tar xzf ${IMG2}.tar.gz
cd $IMG2
if [[ "$OSTYPE" == "darwin"* ]]; then
      # Mac OSX
      # disable imageio is so it doesn't use the built in mac image loading.
      # Since it is not as compatible with some jpg/png files.
      export SDL_IMAGE_CONFIGURE="-DSDL2IMAGE_BACKEND_IMAGEIO=0"
else
      export SDL_IMAGE_CONFIGURE=
fi

mkdir builddir && cd builddir

# We prefer libpng and libjpeg-turbo over stb-image at the moment
# We also don't compile avif and jxl support at the moment
cmake -S .. -B . $PG_BASE_CMAKE_FLAGS $SDL_IMAGE_CONFIGURE \
      -DSDL2IMAGE_DEPS_SHARED=$PG_DEPS_SHARED -DSDL2IMAGE_VENDORED=0 \
      -DSDL2IMAGE_BACKEND_STB=0 -DSDL2IMAGE_AVIF=0 -DSDL2IMAGE_JXL=0 \
      -DSDL2IMAGE_TIF=1 -DSDL2IMAGE_WEBP=1

make
make install

cd ../..

# Build SDL_ttf
tar xzf ${TTF2}.tar.gz
cd $TTF2
mkdir builddir && cd builddir

# We already build freetype+harfbuzz for pygame.freetype
# So we make SDL_ttf use that instead of SDL_ttf vendored copies
cmake -S .. -B . $PG_BASE_CMAKE_FLAGS -DSDL2TTF_VENDORED=0 -DSDL2TTF_HARFBUZZ=1
make
make install

cd ../..


# Build SDL_mixer
tar xzf ${MIX2}.tar.gz
cd $MIX2
mkdir builddir && cd builddir

# We prefer libflac, mpg123 and ogg-vorbis over SDL vendored implementations
# at the moment. This can be changed later if need arises.
# We don't build with libgme for now
# With CMake, libxmp is handled differently compared to the other dependencies.
# The library gets statically linked instead of using standard dynamic linking.
# A fix has been proposed: https://github.com/libsdl-org/SDL_mixer/pull/642
cmake -S .. -B . $PG_BASE_CMAKE_FLAGS \
      -DSDL2MIXER_DEPS_SHARED=$PG_DEPS_SHARED -DSDL2MIXER_VENDORED=0 \
      -DSDL2MIXER_FLAC_LIBFLAC=1 -DSDL2MIXER_FLAC_DRFLAC=0 \
      -DSDL2MIXER_MP3_MPG123=1 -DSDL2MIXER_MP3_MINIMP3=0 \
      -DSDL2MIXER_VORBIS=VORBISFILE

make
make install
