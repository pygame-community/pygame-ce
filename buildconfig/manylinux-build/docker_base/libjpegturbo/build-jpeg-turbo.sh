#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

JPEG_VERSION=3.1.2
JPEG="libjpeg-turbo-${JPEG_VERSION}"

curl -sL --retry 10 https://github.com/libjpeg-turbo/libjpeg-turbo/releases/download/${JPEG_VERSION}/${JPEG}.tar.gz > ${JPEG}.tar.gz

sha512sum -c libjpegturbo.sha512
tar xzf ${JPEG}.tar.gz
cd ${JPEG}

cmake . $PG_BASE_CMAKE_FLAGS $PG_STATIC_CMAKE -DWITH_TURBOJPEG=0 -DWITH_JAVA=0 \
    -DWITH_TOOLS=0 -DWITH_TESTS=0 -DENABLE_STATIC=1 -DENABLE_SHARED=0

make
make install
