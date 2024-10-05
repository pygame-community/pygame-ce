#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# This is an old version... but compiling 0.8.9.0 has problems
MODPLUG_VER=0.8.8.5
MODPLUG_NAME="libmodplug-$MODPLUG_VER"
curl -sL --retry 10 https://sourceforge.net/projects/modplug-xmms/files/libmodplug/${MODPLUG_VER}/${MODPLUG_NAME}.tar.gz/download > ${MODPLUG_NAME}.tar.gz

sha512sum -c libmodplug.sha512
tar -xf ${MODPLUG_NAME}.tar.gz
cd ${MODPLUG_NAME}

./configure $PG_BASE_CONFIGURE_FLAGS
make
make install
