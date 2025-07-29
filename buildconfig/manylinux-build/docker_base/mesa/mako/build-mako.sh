#!/bin/bash
set -e -x

cd $(dirname `readlink -f "$0"`)

# pin for build stability, remember to keep updated
python3 -m pip install mako==1.3.10 PyYAML==6.0.2
