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
# autoreconf -fvi

# alsa is only needed for examples here
./configure $PG_BASE_CONFIGURE_FLAGS --disable-mpeg --disable-alsa
make
make install
