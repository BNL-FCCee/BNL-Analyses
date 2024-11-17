mkdir -p build
mkdir -p run
cd build
source ../source/setup.sh
cmake ../source
make -j
cd ../run
source ../build/setup.sh
