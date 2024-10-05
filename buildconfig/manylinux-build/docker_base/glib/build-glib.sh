#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

GLIB_VER="2.78"
GLIB_PATCH="1"
GLIB="glib-${GLIB_VER}.${GLIB_PATCH}"

curl -sL --retry 10 https://download.gnome.org/sources/glib/${GLIB_VER}/${GLIB}.tar.xz > ${GLIB}.tar.xz
sha512sum -c glib.sha512

unxz ${GLIB}.tar.xz
tar xf ${GLIB}.tar
cd $GLIB

# a minimal glib install will do for us
meson setup _build $PG_BASE_MESON_FLAGS --force-fallback-for libpcre2-8 -Dtests=false \
    -Dselinux=disabled -Dlibmount=disabled -Ddtrace=false -Dsystemtap=false -Dnls=disabled

meson compile -C _build
meson install -C _build
