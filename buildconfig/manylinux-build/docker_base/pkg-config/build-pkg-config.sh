#!/bin/bash

# This file exists because pkg-config is too old on manylinux docker centos 
# images (the older version segfaults if it gets a cyclic dependency, like
# freetype2+harfbuzz)

set -e -x

cd $(dirname `readlink -f "$0"`)

# We save the compiled-in PKG_CONFIG_PATH of the pre-existing pkg-config, and
# re-use it with the new pkg-config
COMPILED_PKGCONFIG_DIRS=$(pkg-config --variable pc_path pkg-config)

# append path(s) where other installs put .pc files
COMPILED_PKGCONFIG_DIRS="$PG_DEP_PREFIX/lib/pkgconfig:$PG_DEP_PREFIX/share/pkgconfig:${COMPILED_PKGCONFIG_DIRS}"

PKGCONFIG=pkg-config-0.29.2

curl -sL --retry 10 https://pkg-config.freedesktop.org/releases/${PKGCONFIG}.tar.gz > ${PKGCONFIG}.tar.gz
sha512sum -c pkg-config.sha512

tar xzf ${PKGCONFIG}.tar.gz
cd $PKGCONFIG

# Passing --with-internal-glib will make this pickup internally vendored glib
# Use this flag if there are build issues with this step later on
./configure $PG_BASE_CONFIGURE_FLAGS --with-pc-path=$COMPILED_PKGCONFIG_DIRS
make
make install
