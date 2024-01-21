#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

SDL2="SDL2-2.28.5"
IMG2="SDL2_image-2.8.2"
TTF2="SDL2_ttf-2.20.2"
MIX2="SDL2_mixer-2.6.3"


# Download
curl -sL --retry 10 https://www.libsdl.org/release/${SDL2}.tar.gz > ${SDL2}.tar.gz
# curl -sL --retry 10 https://www.libsdl.org/tmp/release/SDL2-2.0.14.tar.gz > SDL2-2.0.14.tar.gz
# curl -sL --retry 10 https://hg.libsdl.org/SDL/archive/tip.tar.gz > ${SDL2}.tar.gz

curl -sL --retry 10 https://www.libsdl.org/projects/SDL_image/release/${IMG2}.tar.gz > ${IMG2}.tar.gz
curl -sL --retry 10 https://www.libsdl.org/projects/SDL_ttf/release/${TTF2}.tar.gz > ${TTF2}.tar.gz
curl -sL --retry 10 https://www.libsdl.org/projects/SDL_mixer/release/${MIX2}.tar.gz > ${MIX2}.tar.gz
sha512sum -c sdl2.sha512



# Build SDL
tar xzf ${SDL2}.tar.gz

# this is for renaming the tip.tar.gz
# mv SDL-* ${SDL2}

if [ "$(uname -m)" == "arm64" ] || [ "$(uname -m)" == "aarch64" ]; then
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
mkdir builddir && cd builddir
# The SDL2IMAGE_DEPS_SHARED flag makes it use standard dynamic linking rather than
# dlopen-ing the library itself. This is important for when auditwheel moves
# libraries into the wheel.
if [[ "$OSTYPE" == "darwin"* ]]; then
      # Mac OSX
      # disable imageio is so it doesn't use the built in mac image loading.
      # Since it is not as compatible with some jpg/png files.
      export SDL_IMAGE_CONFIGURE="-DSDL2IMAGE_BACKEND_IMAGEIO=0"
else
      export SDL_IMAGE_CONFIGURE=
fi

# We prefer libpng and libjpeg-turbo over stb-image at the moment
# We also don't compile avif and jxl support at the moment
cmake -S .. -B . $PG_BASE_CMAKE_FLAGS $SDL_IMAGE_CONFIGURE \
      -DSDL2IMAGE_DEPS_SHARED=0 -DSDL2IMAGE_VENDORED=0 \
      -DSDL2IMAGE_TIF=1 -DSDL2IMAGE_WEBP=1 \
      -DSDL2IMAGE_BACKEND_STB=0

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

# The SDL2MIXER_DEPS_SHARED flag make it use standard dynamic linking rather than
# dlopen-ing the library itself. This is important for when auditwheel moves
# libraries into the wheel.
# We prefer mpg123 and ogg-vorbis over SDL vendored implementations
# at the moment. This can be changed later if need arises.
# libflac had link time issues on macs and windows(mingw) so we use drflac.
# For now, libmodplug is preferred over libxmp (but this may need changing
# in the future)
cmake -S .. -B . $PG_BASE_CMAKE_FLAGS \
      -DSDL2MIXER_DEPS_SHARED=0 -DSDL2MIXER_VENDORED=0 \
      -DSDL2MIXER_FLAC_LIBFLAC=0 -DSDL2MIXER_FLAC_DRFLAC=1 \
      -DSDL2MIXER_MOD_MODPLUG=1 -DSDL2MIXER_MOD_XMP=0 \
      -DSDL2MIXER_MP3_MPG123=1 -DSDL2MIXER_MP3_DRMP3=0 \
      -DSDL2MIXER_VORBIS=VORBISFILE -DSDL2MIXER_VORBIS_VORBISFILE_SHARED=0 \
      -DSDL2MIXER_OPUS_SHARED=0

make
make install

