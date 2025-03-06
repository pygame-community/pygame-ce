#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

MACROS_VER="1.20.1"
MACROS="util-macros-$MACROS_VER"

curl -sL --retry 10 https://www.x.org/releases/individual/util/$MACROS.tar.gz > $MACROS.tar.gz
sha512sum -c macros.sha512sum

tar xzf $MACROS.tar.gz
cd $MACROS

./configure $PG_BASE_CONFIGURE_FLAGS
make
make install
