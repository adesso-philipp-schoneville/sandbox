#!/bin/bash

echo "version = $1"

# Get version number from version tag
PY_VERSION=`echo $1 | cut -d'v' -f2`
echo "py = $PY_VERSION"

# Set new version via setuptools
python setup.py setopt --command metadata --option version --set-value $PY_VERSION
