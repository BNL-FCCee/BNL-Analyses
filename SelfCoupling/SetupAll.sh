cd ../FCCeePostCutCode/run
cd ../build
source ../source/setup.sh
cmake ../source 
make -j
cd ../run
source ../build/setup.sh
cd ../../quickstats
pip3 install --user quickstats
source setup.sh
quickstats compile
cd ../SelfCoupling
