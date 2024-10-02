#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

PCIACCESS_VER="0.18.1"
PCIACCESS="libpciaccess-$PCIACCESS_VER"

curl -sL --retry 10 https://www.x.org/releases/individual/lib/$PCIACCESS.tar.xz > $PCIACCESS.tar.xz
sha512sum -c libpciaccess.sha512sum

tar xf $PCIACCESS.tar.xz
cd $PCIACCESS

meson build/ $PG_BASE_MESON_FLAGS
ninja -C build/ install
