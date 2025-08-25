#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

GLSLANG_VER=15.3.0
GLSLANG="glslang-$GLSLANG_VER"
curl -sL --retry 10 https://github.com/KhronosGroup/glslang/archive/refs/tags/${GLSLANG_VER}.tar.gz > ${GLSLANG}.tar.gz

sha512sum -c glslang.sha512sum
tar xzf ${GLSLANG}.tar.gz
cd $GLSLANG

mkdir build
cd build

cmake .. $PG_BASE_CMAKE_FLAGS -DENABLE_OPT=0 -DGLSLANG_TESTS=0
make
make install
