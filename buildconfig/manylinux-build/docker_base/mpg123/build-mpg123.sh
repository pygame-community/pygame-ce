#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

MPG123="mpg123-1.33.2"

curl -sL --retry 10 https://downloads.sourceforge.net/sourceforge/mpg123/${MPG123}.tar.bz2 > ${MPG123}.tar.bz2
sha512sum -c mpg123.sha512

bzip2 -d ${MPG123}.tar.bz2
tar xf ${MPG123}.tar
cd $MPG123

./configure $PG_BASE_CONFIGURE_FLAGS --enable-int-quality --disable-debug \
    --disable-components --enable-libmpg123 --enable-libsyn123

make
make install
