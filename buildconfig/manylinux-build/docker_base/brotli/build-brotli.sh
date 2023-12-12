#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

BROTLI_VER=1.1.0
BROTLI=brotli-$BROTLI_VER

curl -sL --retry 10 https://github.com/google/brotli/archive/refs/tags/v${BROTLI_VER}.tar.gz > ${BROTLI}.tar.gz
sha512sum -c brotli.sha512

tar xzf ${BROTLI}.tar.gz
cd $BROTLI

cmake . $PG_BASE_CMAKE_FLAGS
make
make install
