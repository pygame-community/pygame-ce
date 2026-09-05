#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# We need mesa for opengl, gbm (SDL kmsdrm driver needs it), egl (SDL
# wayland driver needs this) and glx (SDL needs it)
# we don't support vulkan yet

MESA_VER="mesa-25.1.3"
MESA="mesa-$MESA_VER" # yes mesa comes twice in the name

curl -sL --retry 10 https://gitlab.freedesktop.org/mesa/mesa/-/archive/$MESA_VER/$MESA.tar.gz > $MESA.tar.gz
sha512sum -c mesa.sha512sum

tar xzf $MESA.tar.gz
cd $MESA

# build with meson+ninja, a very minimal install will do because this is not actually
# being installed in the wheel
meson build/ $PG_BASE_MESON_FLAGS -Dgallium-drivers=softpipe -Dvulkan-drivers=[]
ninja -C build/ install
