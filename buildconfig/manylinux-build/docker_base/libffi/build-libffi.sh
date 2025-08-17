#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

LIBFFI_VER="3.5.1"
LIBFFI="libffi-$LIBFFI_VER"

curl -sL --retry 10 https://github.com/libffi/libffi/releases/download/v${LIBFFI_VER}/${LIBFFI}.tar.gz > ${LIBFFI}.tar.gz

sha512sum -c libffi.sha512

tar xzf ${LIBFFI}.tar.gz
cd $LIBFFI

# --disable-multi-os-directory is passed so that /usr/local/lib is used
./configure $PG_BASE_CONFIGURE_FLAGS --disable-docs --disable-multi-os-directory
make
make install
