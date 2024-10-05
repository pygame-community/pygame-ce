#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

TIFF=tiff-4.7.0

curl -sL --retry 10 https://download.osgeo.org/libtiff/${TIFF}.tar.gz > ${TIFF}.tar.gz
sha512sum -c tiff.sha512

tar xzf ${TIFF}.tar.gz
cd $TIFF

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ./configure $PG_BASE_CONFIGURE_FLAGS --disable-lzma --disable-webp --disable-zstd
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Use CMake on macOS because arm64 builds fail with weird errors in ./configure
    cmake . $PG_BASE_CMAKE_FLAGS -Dlzma=OFF -Dwebp=OFF -Dzstd=OFF
fi

make
make install
