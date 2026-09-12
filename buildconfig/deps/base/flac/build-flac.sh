#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

FLAC=flac-1.5.0

curl -sL --retry 10 http://downloads.xiph.org/releases/flac/${FLAC}.tar.xz > ${FLAC}.tar.xz
sha512sum -c flac.sha512

# The tar we have is too old to handle .tar.xz directly
unxz ${FLAC}.tar.xz
tar xf ${FLAC}.tar
cd $FLAC

mkdir build
cd build

if [ -n "$WIN_ARCH" ]; then
  # When SDL_image is linking against FLAC on windows, it doesn't find
  # Threads::Threads
  export PG_FLAC_EXTRA_ARGS="-DENABLE_MULTITHREADING=0"
fi

# use cmake to try to catch the ogg dependency
cmake .. $PG_BASE_CMAKE_FLAGS $PG_FLAC_EXTRA_ARGS \
    -DBUILD_CXXLIBS=0 \
    -DBUILD_PROGRAMS=0 \
    -DBUILD_EXAMPLES=0 \
    -DBUILD_TESTING=0 \
    -DBUILD_DOCS=0 \
    -DINSTALL_MANPAGES=0

make
make install
