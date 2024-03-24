#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

WAVPACK_VERSION=5.6.0
WAVPACK="wavpack-${WAVPACK_VERSION}"

curl -sL --retry 10 https://github.com/dbry/WavPack/releases/download/${WAVPACK_VERSION}/${WAVPACK}.tar.xz > ${WAVPACK}.tar.xz

sha512sum -c wavpack.sha512
tar xf ${WAVPACK}.tar.xz
cd ${WAVPACK}

if [[ "$MAC_ARCH" == "arm64" ]]; then
    # As of now, wavpack builds fail on arm64 cross compilation when ASM
    # optimisations are enabled, so disable it
    export WAVPACK_EXTRA_M1_FLAGS="-DWAVPACK_ENABLE_ASM=OFF"
fi

cmake . $PG_BASE_CMAKE_FLAGS $WAVPACK_EXTRA_M1_FLAGS

make
make install
