#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

JPEG_VERSION=3.1.1
JPEG="libjpeg-turbo-${JPEG_VERSION}"

curl -sL --retry 10 https://github.com/libjpeg-turbo/libjpeg-turbo/releases/download/${JPEG_VERSION}/${JPEG}.tar.gz > ${JPEG}.tar.gz

sha512sum -c libjpegturbo.sha512
tar xzf ${JPEG}.tar.gz
cd ${JPEG}

cmake . $PG_BASE_CMAKE_FLAGS -DWITH_TURBOJPEG=0

make
make install
