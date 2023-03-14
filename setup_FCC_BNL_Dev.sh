#!/bin/bash
cd FCCAnalyses_BNL_Dev
source ./setup.sh
mkdir -p build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
time make install
cd ../..
