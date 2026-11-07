#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# The drm already available on manylinux docker images is too old for mesa, so
# we need to compile the latest from source

DRM_VER="libdrm-2.4.124"
DRM="libdrm-$DRM_VER"

curl -sL --retry 10 https://gitlab.freedesktop.org/mesa/libdrm/-/archive/$DRM_VER/$DRM.tar.gz > $DRM.tar.gz
sha512sum -c libdrm.sha512sum

tar xzf $DRM.tar.gz
cd $DRM

# build with meson+ninja
meson build/ $PG_BASE_MESON_FLAGS -Dman-pages=disabled -Dvalgrind=disabled -Dtests=false
ninja -C build/ install
