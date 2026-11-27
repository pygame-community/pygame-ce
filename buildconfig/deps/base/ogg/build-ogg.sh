#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

OGG=libogg-1.3.6
VORBIS=libvorbis-1.3.7

curl -sL --retry 10 http://downloads.xiph.org/releases/ogg/${OGG}.tar.gz > ${OGG}.tar.gz
curl -sL --retry 10 http://downloads.xiph.org/releases/vorbis/${VORBIS}.tar.gz > ${VORBIS}.tar.gz
sha512sum -c ogg.sha512

tar xzf ${OGG}.tar.gz
cd $OGG

cmake . $PG_BASE_CMAKE_FLAGS
make
make install

# Workaround https://github.com/xiph/ogg/issues/14
# When the issue is fixed this block can be removed.
if [ -n "$WIN_ARCH" ]; then
  cp $PG_DEP_PREFIX/bin/libogg.dll $PG_DEP_PREFIX/bin/ogg.dll
fi

cd ..

tar xzf ${VORBIS}.tar.gz
cd $VORBIS

# some hackery needed to make libvorbis build under mingw
if [ -n "$WIN_ARCH" ]; then
  sed -i '/LIBRARY/d' win32/*.def
fi

# Vendor in the fix from first commit of https://github.com/xiph/vorbis/pull/89
# With this fix, the size of the vorbis DLL goes down on Windows significantly.
patch -p1 < ../pr-89-part.patch

# CMake 3.5 or higher policy is required for buiding under CMake 4
cmake . $PG_BASE_CMAKE_FLAGS -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make
make install
