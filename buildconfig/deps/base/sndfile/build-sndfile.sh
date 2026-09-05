#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

SNDFILEVER=1.2.2
SNDNAME="libsndfile-$SNDFILEVER"
SNDFILE="$SNDNAME.tar.xz"
curl -sL --retry 10 https://github.com/libsndfile/libsndfile/releases/download/${SNDFILEVER}/${SNDFILE} > ${SNDFILE}

sha512sum -c sndfile.sha512
tar xf ${SNDFILE}
cd $SNDNAME

cmake . $PG_BASE_CMAKE_FLAGS -DBUILD_PROGRAMS=OFF -DBUILD_EXAMPLES=OFF -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make
make install
