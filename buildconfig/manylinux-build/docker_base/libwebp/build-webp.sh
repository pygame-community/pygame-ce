#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

WEBP=libwebp-1.6.0

curl -sL --retry 10 http://storage.googleapis.com/downloads.webmproject.org/releases/webp/${WEBP}.tar.gz > ${WEBP}.tar.gz
sha512sum -c webp.sha512

tar xzf ${WEBP}.tar.gz
cd $WEBP

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # libwebp 1.6.0 introduced SIMD support for speedups. While it works on mac,
    # it doesn't compile on manylinux because gcc is too old for a particular SIMD
    # function (_mm256_cvtsi256_si32) webp happens to use.
    # TODO: enable SIMD when the issue is resolved.
    export PG_WEBP_EXTRA_ARGS="-DWEBP_ENABLE_SIMD=NO"
fi

# we don't need to build webp commandline tools.
cmake . $PG_BASE_CMAKE_FLAGS $PG_WEBP_EXTRA_ARGS $PG_STATIC_CMAKE \
    -DWEBP_BUILD_DWEBP=NO -DWEBP_BUILD_CWEBP=NO -DWEBP_BUILD_VWEBP=NO \
    -DWEBP_BUILD_ANIM_UTILS=NO -DWEBP_BUILD_GIF2WEBP=NO -DWEBP_BUILD_IMG2WEBP=NO \
    -DWEBP_BUILD_WEBPINFO=NO -DWEBP_BUILD_WEBPMUX=NO -DWEBP_BUILD_EXTRAS=NO
make
make install
