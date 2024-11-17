# Self coupling interpretation

The purpose of this readme is to run a Higgs self-coupling interpretation via SMEFT using existing RooWorkspaces from the fully hadronic ZH analysis.

If it doesn't work, send complaints to Abe: `abraham.tishelman.charny@cern.ch`.

## Setup repository

If not already done, set up the repository:

Via ssh:
```shell
git clone --recurse-submodules git@github.com:BNL-FCCee/BNL-Analyses.git BNL-Analyses
cd BNL-Analyses
```

or via https:
```shell
git clone --recurse-submodules https://github.com/BNL-FCCee/BNL-Analyses.git BNL-Analyses
cd BNL-Analyses
```

## Setup submodules

Two submodules have to be set up in order to perform the self-coupling interpretation: `FCCeePostCutCode` in order to ensure version compatibility with the RooWorkspaces produced for this analysis, and `quickstats` in order to alter workspaces and perform statistical interpretation. 

If not yet done, first setup the submodule(s):

```shell
cd ../BNL-Analyses/FCCeePostCutCode/
source setup_firsttime.sh
```

After running initial setup (Note this can potentially take time due to the `quickstats compile` step):

```shell
cd BNL-Analyses/SelfCoupling
source SetupAll.sh
```

## Run self-coupling

At this point you should have the environment properly set up. The next steps are:

- Add the `RooWorkspaces` you want to alter in the `workspaces` directory
- Run the `MakeXML_SMEFT.py` script. Example command is `python3 MakeXML_SMEFT.py --inFile workspaces/{variation}.root --outFile workspaces_modified/{variation}_modified.root --outXMLFile XML/{variation}.xml` where `variation` is a label used for your workspace name and associated files. This should create an xml file used to add the CPhi SMEFT parameter to your workspace and parameterize the yields of each category.
- Run the `modify_ws` step of `quickstats` in order to update the original workspace using the XML file you just created. Example command is `quickstats modify_ws -i XML/{variation}.xml --input_workspace workspaces/{variation}.root`.
- Run a likelihood scan using the updated workspace. Example command is `quickstats likelihood_scan -i workspaces_modified/{variation}_modified.root -p "Cphi=-3_3_0.1" -d asimovData --outdir {variation}`
- Plot the scan. `cd Plots` then example command is `python3 plot.py --inputs {baseDir}FSR_studies_IDEA_BASE/Cphi.json,{baseDir}FSR_studies_IDEA_nodndx_7labels/Cphi.json,{baseDir}FSR_studies_IDEA_noTOF_7labels/Cphi.json --poi Cphi --NoInteractiveMode --labels FSR_studies_IDEA_BASE{ext},FSR_studies_IDEA_nodndx_7labels{ext},FSR_studies_IDEA_noTOF_7labels{ext} --xmin -1 --xmax 1`
