#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

XMP_VERSION=4.6.3
XMP="libxmp-${XMP_VERSION}"


curl -sL --retry 10 https://github.com/libxmp/libxmp/releases/download/${XMP}/${XMP}.tar.gz > ${XMP}.tar.gz

sha512sum -c libxmp.sha512
tar xzf ${XMP}.tar.gz
cd ${XMP}

cmake . $PG_BASE_CMAKE_FLAGS -DLIBXMP_PIC=1

make
make install
