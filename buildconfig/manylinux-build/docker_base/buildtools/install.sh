#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# This file installs tools (cmake and meson+ninja) needed to build dependencies
# Also installs setuptools to make sure distutils is available (on newer python
# versions) because some builds may need it.
# cmake is also installed via pip because it is easier than maintaining a
# separate build script for it

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    export PG_PIP_EXTRA_FLAGS="--user"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    export PG_PIP_EXTRA_FLAGS="--break-system-packages"
fi

# pin versions for stability (remember to keep updated)
python3 -m pip install $PG_PIP_EXTRA_FLAGS \
    setuptools==80.9.0 meson==1.9.1 ninja==1.13.0

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    cp /root/.local/bin/* /usr/bin
fi
