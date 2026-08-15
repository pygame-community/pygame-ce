# This uses manylinux build scripts to build dependencies on windows.

set -e -x

# fix symlink extraction errors
export MSYS="winsymlinks:lnk"

# The below three lines convert something like D:\path\goes\here to /d/path/goes/here
export BASE_DIR=$(echo "$GITHUB_WORKSPACE" | tr '[:upper:]' '[:lower:]')
export BASE_DIR="${BASE_DIR//\\//}"  # //\\// replaces all \ with / in the variable
export BASE_DIR="/${BASE_DIR//:/}"  # remove colon from drive part, add leading /

export PG_DEP_PREFIX="$BASE_DIR/pygame_win_deps_$WIN_ARCH"
mkdir $PG_DEP_PREFIX

export PKG_CONFIG_PATH="$PG_DEP_PREFIX/lib/pkgconfig"
export PATH="$PATH:$PG_DEP_PREFIX/bin"

# for great speed.
export MAKEFLAGS="-j 4"

# for scripts using ./configure
export CC="gcc"
export CXX="g++"
export AR="ar"

# With this we
# 1) Force install prefix to $PG_DEP_PREFIX
# 2) use lib directory within $PG_DEP_PREFIX (and not lib64)
# 3) make release binaries
# 4) build shared libraries
# 5) tell cmake to search in $PG_DEP_PREFIX for sub dependencies
# 6) make cmake use gcc/g++/make (needed on windows only)
export PG_BASE_CMAKE_FLAGS="-DCMAKE_INSTALL_PREFIX=$PG_DEP_PREFIX \
    -DCMAKE_INSTALL_LIBDIR:PATH=lib \
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DBUILD_SHARED_LIBS=true \
    -DCMAKE_PREFIX_PATH=$PG_DEP_PREFIX \
    -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DCMAKE_MAKE_PROGRAM=make"

export CMAKE_GENERATOR="MSYS Makefiles"

mkdir -p $HOME/build-cache
export AUTOCONF_CACHE=$HOME/build-cache/config.cache
touch $AUTOCONF_CACHE

export PG_BASE_CONFIGURE_FLAGS="--prefix=$PG_DEP_PREFIX \
    --enable-shared --disable-static \
    --cache-file=$AUTOCONF_CACHE"
export CPPFLAGS="-I$PG_DEP_PREFIX/include"
export LDFLAGS="-L$PG_DEP_PREFIX/lib"

export PG_BASE_MESON_FLAGS="--prefix=$PG_DEP_PREFIX \
    -Dlibdir=lib \
    -Doptimization=s -Ddebug=false \
    -Ddefault_library=shared"

# clean msys versions of dependencies we are about to build
bash ./clean_sys_deps.sh

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
# bash bzip2/build-bzip2.sh
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
bash sndfile/build-sndfile.sh
bash fluidsynth/build-fluidsynth.sh

bash sdl_libs/build-sdl2-libs.sh

# for pygame.midi
bash portmidi/build-portmidi.sh

## Below are windows specific fixes

# copy in required mingw DLLs
for pattern in "libgcc_s_dw2-1.dll" "libgcc_s_seh-1.dll" "libwinpthread-1.dll"; do
    dll="$MINGW_PREFIX/bin/$pattern"
    if [[ -f "$dll" ]]; then
        cp "$dll" "$PG_DEP_PREFIX/bin"
    fi
done

# strip dll/a files to reduce size
bash strip-lib-so-files.sh

# Download and setup strings.h
STRINGS_H_COMMIT="20e7935c46af10deaa74b914c1fe2ebb038c69a2"
STRINGS_H_SHA256="e082f06213cc2faf5cf36ec2db5f41627bd652784eaab818c3e7b95e61808346"
curl -sL --retry 10 https://raw.githubusercontent.com/win32ports/strings_h/$STRINGS_H_COMMIT/strings.h > $PG_DEP_PREFIX/include/strings.h
echo "$STRINGS_H_SHA256  $PG_DEP_PREFIX/include/strings.h" | sha256sum -c -

# Make MSVC compatible .lib files from MinGW .dll files
cd $PG_DEP_PREFIX/lib
for lib in SDL2 SDL2_image SDL2_ttf SDL2_mixer freetype portmidi; do
    cp lib${lib}.dll.a ${lib}.lib
done

# Finally, clean the deps folder to only include required stuff
cd $BASE_DIR
python3 buildconfig/windependencies/clean_windows_deps.py $PG_DEP_PREFIX
