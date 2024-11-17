# Self coupling interpretation

The purpose of this readme is to run a Higgs self-coupling interpretation via SMEFT using existing RooWorkspaces from the fully hadronic ZH analysis.

## Setup submodules

Two submodules have to be set up in order to perform the self-coupling interpretation: `FCCeePostCutCode` in order to ensure version compatibility with the RooWorkspaces produced for this analysis, and `quickstats` in order to alter workspaces and perform statistical interpretation. 

If not yet done, first setup the submodules:

```
cd BNL-Analyses/FCCeePostCutCode/
cd ../build
source ../source/setup.sh
cmake ../source
make -j
cd ../run
source ../build/setup.sh
```

```
cd BNL-Analyses/SelfCoupling
```

If you have not yet set up the submodules:

```
cd ../build
source ../source/setup.sh
cmake ../source 
make -j
cd ../run
source ../build/setup.sh
```