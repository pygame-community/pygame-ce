#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

XSHMFENCE_VER="1.3.2"
XSHMFENCE="libxshmfence-$XSHMFENCE_VER"

curl -sL --retry 10 https://www.x.org/releases/individual/lib/${XSHMFENCE}.tar.gz > $XSHMFENCE.tar.gz
sha512sum -c libxshmfence.sha512sum

tar xzf $XSHMFENCE.tar.gz
cd $XSHMFENCE

./configure $PG_BASE_CONFIGURE_FLAGS
make
make install
