#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

WAVPACK_VERSION=5.8.1
WAVPACK="wavpack-${WAVPACK_VERSION}"

curl -sL --retry 10 https://github.com/dbry/WavPack/releases/download/${WAVPACK_VERSION}/${WAVPACK}.tar.xz > ${WAVPACK}.tar.xz

sha512sum -c wavpack.sha512
tar xf ${WAVPACK}.tar.xz
cd ${WAVPACK}

cmake . $PG_BASE_CMAKE_FLAGS $PG_STATIC_CMAKE

make
make install
