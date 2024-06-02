#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# use pinned commit (latest at the time of this comment) as 1.0.3 has compilation issues
PIPEWIRE_VER="0cfe57f33d4a6e511577614e97c7491e6450f0eb"  # 1.0.3
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
