#!/bin/sh
echo $(dirname "$0")
pushd $(dirname "$0")
./venv/bin/python3 album-art.py
popd