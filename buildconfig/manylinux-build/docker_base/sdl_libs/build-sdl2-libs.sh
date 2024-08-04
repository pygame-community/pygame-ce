#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

SDL2_VER="2.30.6"
SDL2="SDL2-$SDL2_VER"
IMG2_VER="2.8.2"
IMG2="SDL2_image-$IMG2_VER"
TTF2_VER="2.22.0"
TTF2="SDL2_ttf-$TTF2_VER"
MIX2_VER="2.8.0"
MIX2="SDL2_mixer-$MIX2_VER"


# Download
curl -sL --retry 10 https://github.com/libsdl-org/SDL/releases/download/release-$SDL2_VER/$SDL2.tar.gz > ${SDL2}.tar.gz
curl -sL --retry 10 https://github.com/libsdl-org/SDL_image/releases/download/release-$IMG2_VER/$IMG2.tar.gz > ${IMG2}.tar.gz
curl -sL --retry 10 https://github.com/libsdl-org/SDL_mixer/releases/download/release-$MIX2_VER/$MIX2.tar.gz > ${MIX2}.tar.gz
curl -sL --retry 10 https://github.com/libsdl-org/SDL_ttf/releases/download/release-$TTF2_VER/$TTF2.tar.gz > ${TTF2}.tar.gz
sha512sum -c sdl2.sha512



# Build SDL
tar xzf ${SDL2}.tar.gz

# this is for renaming the tip.tar.gz
# mv SDL-* ${SDL2}

if [[ "$MAC_ARCH" == "arm64" ]]; then
    # Build SDL with ARM optimisations on M1 macs
    export M1_MAC_EXTRA_FLAGS="--enable-arm-simd --enable-arm-neon"
fi

cd $SDL2
./configure --disable-video-vulkan $PG_BASE_CONFIGURE_FLAGS $M1_MAC_EXTRA_FLAGS
make
make install

cd ..


# Build SDL_image
tar xzf ${IMG2}.tar.gz
cd $IMG2
# The --disable-x-shared flags make it use standard dynamic linking rather than
# dlopen-ing the library itself. This is important for when auditwheel moves
# libraries into the wheel.
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
      # linux
      export SDL_IMAGE_CONFIGURE=
elif [[ "$OSTYPE" == "darwin"* ]]; then
      # Mac OSX
      # --disable-imageio is so it doesn't use the built in mac image loading.
      #     Since it is not as compatible with some jpg/png files.
      export SDL_IMAGE_CONFIGURE=--disable-imageio
fi

# We prefer libpng and libjpeg-turbo over stb-image at the moment
# We also don't compile avif and jxl support at the moment
./configure $ARCHS_CONFIG_FLAG \
      --disable-stb-image \
      --disable-avif --disable-avif-shared \
      --disable-jxl --disable-jxl-shared \
      --enable-png --disable-png-shared \
      --enable-jpg --disable-jpg-shared \
      --enable-tif --disable-tif-shared \
      --enable-webp --disable-webp-shared \
      $SDL_IMAGE_CONFIGURE $PG_BASE_CONFIGURE_FLAGS
make
make install

cd ..

# Build SDL_ttf
tar xzf ${TTF2}.tar.gz
cd $TTF2

# We already build freetype+harfbuzz for pygame.freetype
# So we make SDL_ttf use that instead of SDL_ttf vendored copies
./configure $PG_BASE_CONFIGURE_FLAGS --disable-freetype-builtin --disable-harfbuzz-builtin
make
make install

cd ..


# Build SDL_mixer
tar xzf ${MIX2}.tar.gz
cd $MIX2

# The --disable-x-shared flags make it use standard dynamic linking rather than
# dlopen-ing the library itself. This is important for when auditwheel moves
# libraries into the wheel.
# We prefer libflac, mpg123 and ogg-vorbis over SDL vendored implementations
# at the moment. This can be changed later if need arises.
# We don't build with libgme for now
./configure $PG_BASE_CONFIGURE_FLAGS \
      --disable-dependency-tracking \
      --disable-music-ogg-stb --enable-music-ogg-vorbis \
      --disable-music-flac-drflac --enable-music-flac-libflac \
      --disable-music-mp3-drmp3 --disable-music-mp3-minimp3 --enable-music-mp3-mpg123 \
      --disable-music-mod-modplug \
      --enable-music-mod-xmp --disable-music-mod-xmp-shared \
      --enable-music-midi-fluidsynth --disable-music-midi-fluidsynth-shared \
      --enable-music-opus --disable-music-opus-shared \
      --enable-music-wavpack --disable-music-wavpack-shared \
      --disable-music-ogg-vorbis-shared \
      --disable-music-ogg-tremor \
      --disable-music-flac-libflac-shared \
      --disable-music-mp3-mpg123-shared \
      --disable-music-gme

make
make install

