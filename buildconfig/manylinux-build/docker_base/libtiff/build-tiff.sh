#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

TIFF=tiff-4.7.1

curl -sL --retry 10 https://download.osgeo.org/libtiff/${TIFF}.tar.gz > ${TIFF}.tar.gz
sha512sum -c tiff.sha512

tar xzf ${TIFF}.tar.gz
cd $TIFF

# turn off lzma, webp and zstd so that cmake does not try to pick them up from
# the system.
cmake . $PG_BASE_CMAKE_FLAGS -Dlzma=OFF -Dwebp=OFF -Dzstd=OFF \
    -Dtiff-tools=OFF -Dtiff-tests=OFF -Dtiff-contrib=OFF -Dtiff-docs=OFF

make
make install
