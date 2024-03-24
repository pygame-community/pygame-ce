#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# This is a libsamplerate dependency
FFTW_VER="3.3.10"
FFTW="fftw-3.3.10"

LIBSAMPLERATE_VER="0.2.2"
LIBSAMPLERATE="libsamplerate-$LIBSAMPLERATE_VER"

curl -sL --retry 10 https://www.fftw.org/${FFTW}.tar.gz > ${FFTW}.tar.gz
curl -sL --retry 10 https://github.com/libsndfile/libsamplerate/releases/download/${LIBSAMPLERATE_VER}/${LIBSAMPLERATE}.tar.xz > ${LIBSAMPLERATE}.tar.xz
sha512sum -c libsamplerate.sha512

tar xzf ${FFTW}.tar.gz
cd ${FFTW}

mkdir build
cd build

cmake .. $PG_BASE_CMAKE_FLAGS
make
make install

cd ../..

tar xf ${LIBSAMPLERATE}.tar.xz
cd $LIBSAMPLERATE

mkdir build
cd build

cmake .. $PG_BASE_CMAKE_FLAGS
make
make install
