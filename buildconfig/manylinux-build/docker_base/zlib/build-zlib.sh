#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

ZLIB_VER=1.3.1
ZLIB_NAME="zlib-$ZLIB_VER"
curl -sL --retry 10 https://www.zlib.net/${ZLIB_NAME}.tar.gz > ${ZLIB_NAME}.tar.gz

sha512sum -c zlib.sha512
tar -xf ${ZLIB_NAME}.tar.gz
cd ${ZLIB_NAME}

./configure $PG_BASE_CONFIGURE_FLAGS
make
make install
