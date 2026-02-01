#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

OPUS=opus-1.5.2
OPUS_FILE=opusfile-0.12

curl -sL --retry 10 http://downloads.xiph.org/releases/opus/${OPUS}.tar.gz > ${OPUS}.tar.gz
curl -sL --retry 10 http://downloads.xiph.org/releases/opus/${OPUS_FILE}.tar.gz > ${OPUS_FILE}.tar.gz
sha512sum -c opus.sha512

tar xzf ${OPUS}.tar.gz
cd $OPUS

# Opus doesn't support rtcd on ARM Windows yet.
if [ "$WIN_ARCH" == "aarch64" ]; then
  PG_EXTRA_OPUS_ARGS="--disable-rtcd"
fi

./configure $PG_BASE_CONFIGURE_FLAGS $PG_EXTRA_OPUS_ARGS
make
make install

cd ..

tar xzf ${OPUS_FILE}.tar.gz
cd $OPUS_FILE

./configure $PG_BASE_CONFIGURE_FLAGS --disable-http
make
make install
