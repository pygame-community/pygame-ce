#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# Gettext 0.22 didn't work for some reason
GETTEXT=gettext-0.21

curl -sL --retry 10 https://ftp.gnu.org/gnu/gettext/${GETTEXT}.tar.gz > ${GETTEXT}.tar.gz
sha512sum -c gettext.sha512

if [[ "$OSTYPE" == "darwin"* ]]; then
      # Mac OSX, ship libintl.h on mac.
      export GETTEXT_CONFIGURE=--with-included-gettext
else
      export GETTEXT_CONFIGURE=
fi

tar xzf ${GETTEXT}.tar.gz
cd $GETTEXT

./configure $PG_BASE_CONFIGURE_FLAGS $GETTEXT_CONFIGURE  \
--disable-dependency-tracking \
--disable-silent-rules \
--disable-debug \
--with-included-glib \
--with-included-libcroco \
--with-included-libunistring \
--with-included-libxml \
--without-emacs \
--disable-java \
--disable-csharp \
--without-git \
--without-cvs \
--without-xz

make
make install

# For some reason, this is needed for glib to find gettext
# TODO: remove this, hopefully after glib is updated this won't be needed
if [[ "$OSTYPE" == "darwin"* ]]; then
    make install prefix=/usr/local
fi
