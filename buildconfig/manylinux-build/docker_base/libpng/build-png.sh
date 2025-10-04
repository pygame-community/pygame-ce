#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

PNG=libpng-1.6.50

curl -sL --retry 10 http://download.sourceforge.net/libpng/${PNG}.tar.gz > ${PNG}.tar.gz
sha512sum -c png.sha512

tar xzf ${PNG}.tar.gz
cd $PNG

cmake . $PG_BASE_CMAKE_FLAGS -DPNG_TESTS=0 -DPNG_TOOLS=0 -DPNG_STATIC=0 -DPNG_FRAMEWORK=0
make
make install
