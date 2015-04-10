#!/usr/bin/env bash

cd ./3DAlignment/
make
make release
cd ..

cd ./LightField/
make
make release
cd ..
