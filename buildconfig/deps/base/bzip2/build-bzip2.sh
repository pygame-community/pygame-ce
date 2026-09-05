#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

BZIP2_VER=1.0.8
BZIP2=bzip2-$BZIP2_VER

curl -sL --retry 10 https://sourceware.org/pub/bzip2/${BZIP2}.tar.gz > ${BZIP2}.tar.gz
sha512sum -c bzip2.sha512

tar xzf ${BZIP2}.tar.gz
cd $BZIP2

if [[ -z "${CC}" ]]; then
    make install PREFIX=$PG_DEP_PREFIX
else
    # pass CC explicitly because it's needed here
    make install CC="${CC}" PREFIX=$PG_DEP_PREFIX
fi
