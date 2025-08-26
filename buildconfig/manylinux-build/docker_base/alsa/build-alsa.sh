#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

ALSA=alsa-lib-1.2.14
curl -sL https://www.alsa-project.org/files/pub/lib/${ALSA}.tar.bz2 > ${ALSA}.tar.bz2
sha512sum -c alsa.sha512

tar xjf ${ALSA}.tar.bz2
cd ${ALSA}

# alsa prefers /usr prefix as a default, so we explicitly override it
./configure $PG_BASE_CONFIGURE_FLAGS --with-configdir=$PG_DEP_PREFIX/share/alsa
make
make install
