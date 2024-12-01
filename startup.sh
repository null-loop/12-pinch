#!/bin/sh
pushd $(dirname "$0")
./venv/bin/python3 album-art.py
popd