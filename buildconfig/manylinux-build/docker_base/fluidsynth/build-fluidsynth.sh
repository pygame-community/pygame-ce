#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

FSYNTH_VER="2.5.0"
FSYNTH="fluidsynth-$FSYNTH_VER"

curl -sL --retry 10 https://github.com/FluidSynth/fluidsynth/archive/v${FSYNTH_VER}.tar.gz > ${FSYNTH}.tar.gz
sha512sum -c fluidsynth.sha512
tar xzf ${FSYNTH}.tar.gz

cd $FSYNTH
# Vendor in the fix from https://github.com/FluidSynth/fluidsynth/pull/1687
# this can be removed when we bump fluidsynth next
patch -p1 < ../pr-1687.patch
mkdir build
cd build

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    export FLUIDSYNTH_EXTRA_PLAT_FLAGS="-Denable-alsa=NO -Denable-systemd=NO"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # We don't need fluidsynth framework on mac builds
    export FLUIDSYNTH_EXTRA_PLAT_FLAGS="-Denable-framework=NO"
fi

cmake .. $PG_BASE_CMAKE_FLAGS -Denable-readline=OFF $FLUIDSYNTH_EXTRA_PLAT_FLAGS \
    -Denable-openmp=OFF -Dosal=cpp11 -Denable-libinstpatch=0 \
    -Denable-pulseaudio=NO \
    -Denable-pipewire=NO

make
make install
