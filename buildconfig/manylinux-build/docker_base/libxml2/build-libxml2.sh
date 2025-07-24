#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

LIBXML2_VER=2.14
LIBXML2_PATCH=4
LIBXML2="libxml2-$LIBXML2_VER.$LIBXML2_PATCH"

curl -sL --retry 10 https://download.gnome.org/sources/libxml2/${LIBXML2_VER}/${LIBXML2}.tar.xz > ${LIBXML2}.tar.xz
sha512sum -c libxml2.sha512

tar xf ${LIBXML2}.tar.xz
cd $LIBXML2

./configure $PG_BASE_CONFIGURE_FLAGS --disable-static --with-python=no
make
make install
