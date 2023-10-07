#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

LIBFFI_VER="3.4.4"
LIBFFI="libffi-$LIBFFI_VER"

curl -sL --retry 10 https://github.com/libffi/libffi/releases/download/v${LIBFFI_VER}/${LIBFFI}.tar.gz > ${LIBFFI}.tar.gz

sha512sum -c libffi.sha512

tar xzf ${LIBFFI}.tar.gz
cd $LIBFFI

./configure $ARCHS_CONFIG_FLAG
make
make install

if [[ "$OSTYPE" == "darwin"* ]]; then
    # Install to mac deps cache dir as well
    make install DESTDIR=${MACDEP_CACHE_PREFIX_PATH}
fi
