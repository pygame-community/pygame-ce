#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

FLEX_VER="2.6.4"
FLEX="flex-$FLEX_VER"

curl -sL --retry 10 https://github.com/westes/flex/releases/download/v$FLEX_VER/$FLEX.tar.gz > $FLEX.tar.gz
sha512sum -c flex.sha512sum

tar xzf $FLEX.tar.gz
cd $FLEX

./configure $PG_BASE_CONFIGURE_FLAGS
make
make install
