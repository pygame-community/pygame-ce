# This uses manylinux build scripts to build dependencies on windows.

set -e -x

# This is needed for tar to work in some places
export MSYS=winsymlinks:lnk

# The below three lines convert something like D:\path\goes\here to /d/path/goes/here
export BASE_DIR=$(echo "$GITHUB_WORKSPACE" | tr '[:upper:]' '[:lower:]')
export BASE_DIR="${BASE_DIR//\\//}"  # //\\// replaces all \ with / in the variable
export BASE_DIR="/${BASE_DIR//:/}"  # remove colon from drive part, add leading /

export PG_DEP_PREFIX="$BASE_DIR/pygame_win_deps_$WIN_ARCH"

export PKG_CONFIG_PATH="$PG_DEP_PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH"

mkdir $PG_DEP_PREFIX

# for great speed.
export MAKEFLAGS="-j 4"

# for scripts using ./configure
export CC="gcc"
export CXX="g++"

# With this we
# 1) Force install prefix to $PG_DEP_PREFIX
# 2) use lib directory within $PG_DEP_PREFIX (and not lib64)
# 3) make release binaries
# 4) build shared libraries
# 5) make cmake use gcc/g++/make
export PG_BASE_CMAKE_FLAGS="-DCMAKE_INSTALL_PREFIX=$PG_DEP_PREFIX \
    -DCMAKE_INSTALL_LIBDIR:PATH=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=true \
    -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DCMAKE_MAKE_PROGRAM=make"

export CMAKE_GENERATOR="MSYS Makefiles"

export PG_BASE_CONFIGURE_FLAGS="--prefix=$PG_DEP_PREFIX"

export PG_BASE_MESON_FLAGS="--prefix=$PG_DEP_PREFIX \
    -Dlibdir=lib \
    -Dbuildtype=release \
    -Ddefault_library=shared"

cd ../manylinux-build/docker_base

# Now start installing dependencies
# ---------------------------------

# install some buildtools
# bash buildtools/install.sh

# sdl_image deps
bash zlib-ng/build-zlib-ng.sh
bash libpng/build-png.sh # depends on zlib
bash libjpegturbo/build-jpeg-turbo.sh
bash libtiff/build-tiff.sh
bash libwebp/build-webp.sh

# freetype (also sdl_ttf dep)
bash brotli/build-brotli.sh
bash bzip2/build-bzip2.sh
bash freetype/build-freetype.sh

# sdl_mixer deps
bash libxmp/build-libxmp.sh
bash ogg/build-ogg.sh
bash flac/build-flac.sh
bash mpg123/build-mpg123.sh
bash opus/build-opus.sh # needs libogg (which is a container format)
bash wavpack/build-wavpack.sh

# fluidsynth (for sdl_mixer)
# bash gettext/build-gettext.sh
bash glib/build-glib.sh
bash sndfile/build-sndfile.sh
bash fluidsynth/build-fluidsynth.sh

bash sdl_libs/build-sdl2-libs.sh

# for pygame.midi
bash portmidi/build-portmidi.sh
