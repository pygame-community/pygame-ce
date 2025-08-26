#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

OGG=libogg-1.3.6
VORBIS=libvorbis-1.3.7

curl -sL --retry 10 http://downloads.xiph.org/releases/ogg/${OGG}.tar.gz > ${OGG}.tar.gz
curl -sL --retry 10 http://downloads.xiph.org/releases/vorbis/${VORBIS}.tar.gz > ${VORBIS}.tar.gz
sha512sum -c ogg.sha512

tar xzf ${OGG}.tar.gz
cd $OGG

cmake . $PG_BASE_CMAKE_FLAGS
make
make install

cd ..

tar xzf ${VORBIS}.tar.gz
cd $VORBIS

# CMake 3.5 or higher policy is required for buiding under CMake 4
cmake . $PG_BASE_CMAKE_FLAGS -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make
make install
