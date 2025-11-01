# This uses manylinux build scripts to build dependencies
#  on mac.
#
# Warning: this should not be run on your own mac as it cleans dependencies on the system

set -e -x

export PG_DEP_PREFIX=${GITHUB_WORKSPACE}/pygame_mac_deps_${MAC_ARCH}

bash ./clean_usr_local.sh
mkdir $PG_DEP_PREFIX

export PKG_CONFIG_PATH="$PG_DEP_PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH"

# to use the gnu readlink, needs `brew install coreutils`
export PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH"

# for great speed.
export MAKEFLAGS="-j 4"

# With this we
# 1) Force install prefix to $PG_DEP_PREFIX
# 2) use lib directory within $PG_DEP_PREFIX (and not lib64)
# 3) make release binaries
# 4) build shared libraries
# 5) not have @rpath in the linked dylibs (needed on macs only)
# 6) tell cmake to search in $PG_DEP_PREFIX for sub dependencies
export PG_BASE_CMAKE_FLAGS="-DCMAKE_INSTALL_PREFIX=$PG_DEP_PREFIX \
    -DCMAKE_INSTALL_LIBDIR:PATH=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=true \
    -DCMAKE_INSTALL_NAME_DIR=$PG_DEP_PREFIX/lib \
    -DCMAKE_PREFIX_PATH=$PG_DEP_PREFIX"

export PG_BASE_CONFIGURE_FLAGS="--prefix=$PG_DEP_PREFIX"

export PG_BASE_MESON_FLAGS="--prefix=$PG_DEP_PREFIX \
    -Dlibdir=lib \
    -Dbuildtype=release \
    -Ddefault_library=shared"

if [[ "$MAC_ARCH" == "arm64" ]]; then
    # needs native-file that has correct macosx deployment target
    export PG_BASE_MESON_FLAGS="$PG_BASE_MESON_FLAGS --native-file $(pwd)/macos_arm64.ini"

    # we don't need mac 10.9 support while compiling for apple M1 macs
    export MACOSX_DEPLOYMENT_TARGET=11.0
else
    # install NASM to generate optimised x86_64 libjpegturbo builds
    brew install nasm

    # for scripts using ./configure to make x86_64 binaries
    export CC="clang -target x86_64-apple-macos10.11"
    export CXX="clang++ -target x86_64-apple-macos10.11"

    export PG_BASE_CONFIGURE_FLAGS="$PG_BASE_CONFIGURE_FLAGS --host=x86_64-apple-darwin"

    # configure cmake to cross-compile
    export PG_BASE_CMAKE_FLAGS="$PG_BASE_CMAKE_FLAGS -DCMAKE_OSX_ARCHITECTURES=x86_64"

    # SDL 2.26.5 new minimum macos is 10.11, so we build our x86 mac deps
    # for 10.11 as well.
    export MACOSX_DEPLOYMENT_TARGET=10.11

    # configure meson to cross-compile with correct target
    export PG_BASE_MESON_FLAGS="$PG_BASE_MESON_FLAGS --cross-file $(pwd)/macos_x86_64.ini"
fi

export PG_STATIC_AUTOTOOLS="--enable-static --disable-shared"
export PG_STATIC_CMAKE="-DBUILD_SHARED_LIBS=false"
export PG_STATIC_MESON="-Ddefault_library=static"

cd ../manylinux-build/docker_base

# Now start installing dependencies
# ---------------------------------

# install some buildtools
bash buildtools/install.sh

# sdl dep
bash libsamplerate/build-libsamplerate.sh

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
# bash glib/build-glib.sh
# bash sndfile/build-sndfile.sh
bash fluidsynth/build-fluidsynth.sh

bash sdl_libs/build-sdl2-libs.sh

# for pygame.midi
bash portmidi/build-portmidi.sh
