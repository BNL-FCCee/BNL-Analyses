# Self coupling interpretation

The purpose of this readme is to run a Higgs self-coupling interpretation via SMEFT using existing RooWorkspaces from the fully hadronic ZH analysis.

If it doesn't work, send complaints to Abe: `abraham.tishelman.charny@cern.ch`.

## Setup submodules

Two submodules have to be set up in order to perform the self-coupling interpretation: `FCCeePostCutCode` in order to ensure version compatibility with the RooWorkspaces produced for this analysis, and `quickstats` in order to alter workspaces and perform statistical interpretation. 

If not yet done, first setup the submodule(s):

```
cd ../BNL-Analyses/FCCeePostCutCode/
source setup_firsttime.sh
```

After running initial setup (Note this can potentially take time due to the `quickstats compile` step):

```
cd BNL-Analyses/SelfCoupling
source SetupAll.sh
```

## Run self-coupling

At this point you should have the environment properly set up.