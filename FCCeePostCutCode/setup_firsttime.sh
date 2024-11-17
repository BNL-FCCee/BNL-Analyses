mkdir -p build
cd build
source ../source/setup.sh
cmake ../source
make -j
cd ../run
source ../build/setup.sh
