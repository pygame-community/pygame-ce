#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

LIBDECOR_VER=0.2.3
LIBDECOR="libdecor-$LIBDECOR_VER"

curl -sL --retry 10 https://gitlab.freedesktop.org/libdecor/libdecor/-/releases/${LIBDECOR_VER}/downloads/${LIBDECOR}.tar.xz > ${LIBDECOR}.tar.xz
sha512sum -c libdecor.sha512sum

tar xf $LIBDECOR.tar.xz
cd $LIBDECOR

# This is a hack because I'm lazy :)
# libdecor depends on cairo which is a kinda heavy dependency and need more
# scripting work. But libdecor shared lib is not actually present in the
# manylinux wheel and is dynamically loaded by SDL at runtime (if available on
# users system)
# So we override the plugin builds to skip cairo (and only build dummy plugin)
echo "plugin_include_path = include_directories('.')" > src/plugins/meson.build
echo "subdir('dummy')" > src/plugins/meson.build

meson build/ $PG_BASE_MESON_FLAGS -Ddemo=false
ninja -C build/ install
