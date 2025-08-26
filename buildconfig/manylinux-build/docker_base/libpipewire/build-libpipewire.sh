#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# pipewire 1.4.5 has some compilation issues, stay at an older version for now
PIPEWIRE_VER="1.2.7"
PIPEWIRE="pipewire-$PIPEWIRE_VER"

curl -sL --retry 10 https://gitlab.freedesktop.org/pipewire/pipewire/-/archive/${PIPEWIRE_VER}/${PIPEWIRE}.tar.gz > ${PIPEWIRE}.tar.gz
sha512sum -c libpipewire.sha512

tar xzf ${PIPEWIRE}.tar.gz
cd $PIPEWIRE

# a minimal pipewire install will do for us (as SDL loads it dynamically)
meson setup _build $PG_BASE_MESON_FLAGS -Dsession-managers=[] \
    -Dexamples=disabled -Dtests=disabled -Dsystemd=disabled -Dselinux=disabled \
    -Dpipewire-alsa=disabled -Dpipewire-jack=disabled -Dpipewire-v4l2=disabled \
    -Dspa-plugins=disabled -Ddbus=disabled -Dudev=disabled -Dsndfile=disabled \
    -Dx11=disabled -Dlibpulse=disabled -Davb=disabled

meson compile -C _build
meson install -C _build
