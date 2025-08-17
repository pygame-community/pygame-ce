#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# TODO: when freetype is updated, we can look into resolving the circular
# dependency between freetype and harfbuzz by using the upcoming freetype
# dynamic harfbuzz loading feature.
FREETYPE="freetype-2.13.3"
HARFBUZZ_VER=11.3.3
HARFBUZZ_NAME="harfbuzz-$HARFBUZZ_VER"

curl -sL --retry 10 https://savannah.nongnu.org/download/freetype/${FREETYPE}.tar.gz > ${FREETYPE}.tar.gz
curl -sL --retry 10 https://github.com/harfbuzz/harfbuzz/releases/download/${HARFBUZZ_VER}/${HARFBUZZ_NAME}.tar.xz > ${HARFBUZZ_NAME}.tar.xz
sha512sum -c freetype.sha512

# extract installed sources
tar xzf ${FREETYPE}.tar.gz
unxz ${HARFBUZZ_NAME}.tar.xz
tar xf ${HARFBUZZ_NAME}.tar

# freetype and harfbuzz have an infamous circular dependency, which is why
# this file is not like the rest of docker_base files

# 1. First compile freetype without harfbuzz support
cd $FREETYPE

./configure $PG_BASE_CONFIGURE_FLAGS --with-harfbuzz=no
make
make install  # this freetype is not installed to mac cache dir

cd ..

# 2. Compile harfbuzz with freetype support
cd ${HARFBUZZ_NAME}

# harfbuzz has a load of optional dependencies but only freetype is important
# to us.
# Cairo and chafa are only needed for harfbuzz commandline utilities so we
# don't use it. glib available is a bit old so we don't prefer it as of now.
# we also don't compile-in icu so that harfbuzz uses built-in unicode handling
meson setup _build $PG_BASE_MESON_FLAGS -Dfreetype=enabled \
    -Dglib=disabled -Dgobject=disabled -Dcairo=disabled -Dchafa=disabled -Dicu=disabled \
    -Dtests=disabled -Dintrospection=disabled -Ddocs=disabled

meson compile -C _build
meson install -C _build

if [[ "$OSTYPE" == "darwin"* ]]; then
    # We do a little hack...
    # When freetype finds harfbuzz with pkg-config, we tell freetype a little
    # lie that harfbuzz doesn't depend on freetype (even though it does).
    # This ensures no direct circular dylib link happen.
    # This is a bit of a brittle hack: This command removes the entire line that
    # contains "freetype". This is fine for now when the harfbuzz we are
    # building has no other dependencies
    sed -i '' '/freetype/d' $PG_DEP_PREFIX/lib/pkgconfig/harfbuzz.pc
fi

cd ..

# 3. Recompile freetype, and this time with harfbuzz support
cd $FREETYPE

# fully clean previous install
make clean
if [[ "$OSTYPE" == "darwin"* ]]; then
    make uninstall
fi

./configure $PG_BASE_CONFIGURE_FLAGS --with-harfbuzz=yes
make
make install
