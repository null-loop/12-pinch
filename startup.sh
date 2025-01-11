#!/bin/bash

pushd $(dirname "$0")
./venv/bin/python3 pisnake.py
popd