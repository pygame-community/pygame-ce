#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

OGG=libogg-1.3.5
VORBIS=libvorbis-1.3.7

curl -sL --retry 10 http://downloads.xiph.org/releases/ogg/${OGG}.tar.gz > ${OGG}.tar.gz
curl -sL --retry 10 http://downloads.xiph.org/releases/vorbis/${VORBIS}.tar.gz > ${VORBIS}.tar.gz
sha512sum -c ogg.sha512

tar xzf ${OGG}.tar.gz
cd $OGG

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ./configure $PG_BASE_CONFIGURE_FLAGS
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Use CMake on macOS because ./configure doesn't generate dylib
    cmake . $PG_BASE_CMAKE_FLAGS
fi

make
make install

cd ..

tar xzf ${VORBIS}.tar.gz
cd $VORBIS

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ./configure $PG_BASE_CONFIGURE_FLAGS
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Use CMake on macOS because ./configure doesn't generate dylib
    cmake . $PG_BASE_CMAKE_FLAGS
fi
make
make install
