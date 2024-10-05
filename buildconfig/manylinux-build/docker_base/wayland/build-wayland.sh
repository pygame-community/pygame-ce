#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

WAYLAND_VER=1.23.1
WAYLAND_PROT_VER=1.37

WAYLAND="wayland-$WAYLAND_VER"
WAYLAND_PROT="wayland-protocols-$WAYLAND_PROT_VER"

curl -sL --retry 10 https://gitlab.freedesktop.org/wayland/wayland/-/archive/$WAYLAND_VER/$WAYLAND.tar.gz > $WAYLAND.tar.gz
curl -sL --retry 10 https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/$WAYLAND_PROT_VER/$WAYLAND_PROT.tar.gz > $WAYLAND_PROT.tar.gz

sha512sum -c wayland.sha512sum

tar xzf $WAYLAND.tar.gz
cd $WAYLAND

meson build/ $PG_BASE_MESON_FLAGS -Ddocumentation=false -Dtests=false
ninja -C build/ install

cd ..
tar xzf $WAYLAND_PROT.tar.gz
cd $WAYLAND_PROT

meson build/ $PG_BASE_MESON_FLAGS -Dtests=false
ninja -C build/ install
