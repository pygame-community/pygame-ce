#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# 2.0.4 has compilation issues on windows, so pin to latest commit on github
PORTMIDI_VER="7a5de5b7597c46f963d72a83defe7592f901e5f1"
PORTMIDI="portmidi-${PORTMIDI_VER}"

curl -sL --retry 10 https://github.com/PortMidi/portmidi/archive/$PORTMIDI_VER.tar.gz > ${PORTMIDI}.tar.gz
sha512sum -c portmidi.sha512

tar xzf ${PORTMIDI}.tar.gz
cd $PORTMIDI

cmake . $PG_BASE_CMAKE_FLAGS
make
make install
