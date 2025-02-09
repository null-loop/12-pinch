#!/bin/bash

pushd $(dirname "$0")
./venv/bin/python3 game-of-life.py
popd