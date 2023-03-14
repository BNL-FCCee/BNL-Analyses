# BNL FCC-ee studies

The purpose of this repository is to keep track of analysis configurations to perform FCC-ee feasability studies performed at BNL. This analysis includes phase space selections and plotters for:

* Higgs to invisible
* Z(cc)H

## Initial Setup

Clone the repository, including the FCCAnalyses submodule(s).

Via ssh:
```shell
git clone --recurse-submodules git@github.com:BNL-FCCee/HInvisible.git HInvisible
cd HInvisible
```

or via https:
```shell
git clone --recurse-submodules https://github.com/BNL-FCCee/HInvisible.git HInvisible
cd HInvisible
```

## Initial Setup

Note that there are two submodules defined in the repository: `FCCAnalyses` and `FCCAnalyses_BNL_dev`. `FCCAnalyses` points to the [central FCCAnalyses framework](https://github.com/HEP-FCC/FCCAnalyses) used by the FCC community. However, if one wants to run an analysis configuration using a custom addition to the framework which has not yet been merged into the central repository, one can run with that configuration by pushing it to the [BNL development fork](https://github.com/BNL-FCCee/FCCAnalyses/tree/master) of FCCAnalyses, and sourcing that submodule instead of the central one while working. 

For the initial setup of the central `FCCAnalyses` repository, run the command:

```bash
source setup_FCC.sh
```

For initial setup and sourcing of the BNL development fork, run the following:

```bash
source setup_FCC_BNL_Dev.sh
```

## Regular Setup

After initial setup, first make sure you have the latest versions of the submodules:

```bash
git submodule update --recursive
```

Then, one can source either the central version or BNL development version of `FCCAnalyses` with the following:

```shell
cd FCCAnalyses; source setup.sh; cd ..
cd FCCAnalyses_BNL_Dev; source setup.sh; cd ..
```

## Run the selections

Depending on the physics process you want to study, you may need to apply different analysis selections and define certain variables in order to pin down the relevant phase space, in which the physics process you are targetting has a strong signal to background ratio. These selections and plotters are currently defined per analysis - in this case for Higgs Invisible, or Z(cc)H.

Before running, note that if one wants to use json information for a certain campaign, one should specify it with the `FCCDICTSDIR` environment variable:

```
export FCCDICTSDIR="/afs/cern.ch/work/f/fccsw/public/FCCDicts" 
```

### Higgs Invisible

The analysis proceeds in multiple steps. Execute these steps in squence.
H->inv, Z->mumu selection

```shell
fccanalysis run analysis_HInvMuMu_stage1.py
fccanalysis final analysis_HInvMuMu_final.py
```

H->inv, Z->jj selection ( **work in progress** )

```shell
fccanalysis run analysis_HInvjj_stage1.py
```

### Z(cc)H

The purpose of the Z(cc)H analysis is to indirectly constrain the Higgs self-coupling via precision measurements of the ZH cross section and Higgs branching ratios, which are altered for non-SM-value Higgs self-couplings [[Higgs performance meeting update]](https://indico.cern.ch/event/1257240/contributions/5284224/attachments/2605291/4499663/6_March_2023_ZccH_atFCCee%20(1).pdf). 

Before running, first check the `RunConfig.yaml` file for the configured parameters for your run. Currently the following options exist:

* `batch`: Boolean 0 or 1 - determines whether or not to submit jobs to HTCondor.
* `EOSoutput`: Boolean 0 or 1 - determines where or not to output files to EOS.
* `JobName`: String - used for name of output directory.
* `njets`: Integer - number of jets to demand when performing jet reclustering.

Example configuration to run without HTCondor, without EOS, and requiring 4 jets upon reclustering:

```yaml
batch: 0
EOSoutput: 0
JobName: "ZccH_4jetsRequired"
njets: 4
```

To run the current analysis selections locally on a single file, set the config to the above and run the following commands:

```bash
fccanalysis run ZccH_stage1.py --output wzp6_ee_ccH_Hcc_ecm240.root --files-list /eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_ccH_Hcc_ecm240/events_056080797.root --ncpus 64 --nev 1000
fccanalysis final ZccH_final.py
fccanalysis plots ZccH_plots.py
```

Note that if you run via `HTCondor`, you can find useful batchoutput logging information in the `BatchOutputs` directory in whichever FCCAnalyses version you are using. For example, when running with `FCCAnalyses_BNL_Dev`, after submitting batch jobs, you can find batch information in `FCCAnalyses_BNL_Dev/BatchOutputs`.

## Misc.

in `/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_ccH_Hbb_ecm240/events_180562176.root`,  Jet#2.collectionID is 15, indicating this is the ReconstructedParticles collection of jets. 

Know this from podio_metadata->Scan("m_names")

```
***********************************
*    Row   * Instance *   m_names *
***********************************
*        0 *        0 * MissingET *
*        0 *        1 * MCReco *
*        0 *        2 * ParticleI *
*        0 *        3 * magFieldB *
*        0 *        4 * TrackerHi *
*        0 *        5 * EFlowTrac *
*        0 *        6 * Calorimet *
*        0 *        7 *  Particle *
*        0 *        8 *    Photon *
*        0 *        9 * EFlowTrac *
*        0 *       10 *  Electron *
*        0 *       11 * EFlowPhot *
*        0 *       12 * EFlowNeut *
*        0 *       13 *       Jet *
*        0 *       14 * Reconstru *
*        0 *       15 *      Muon *
***********************************
```

Can also tell by printing the collectionID:

```
Jet#2: ReconstructedParticles
Jet#3: ParticleIDs
```

### Example with previous config 

```bash
fccanalysis run ZccH/ZccH_stage1.py --output ZccH_stage1.root --files-list /eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_ccH_Hbb_ecm240/events_180562176.root --nevents 100
fccanalysis run ZccH/ZccH_stage1_Reclustering.py --output ZccH_stage1.root --files-list /eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_ccH_Hbb_ecm240/events_180562176.root --nevents 100
fccanalysis run ZccH/ZccH_stage2.py --output wzp6_ee_ccH_Hbb_ecm240.root --files-list ZccH/stage1/ZccH_stage1.root --nevents 100
fccanalysis final ZccH/ZccH_final.py 
fccanalysis plots ZccH/ZccH_plots.py 
```

### Git 

Added BNL dev submodule with: 

```bash
git submodule add -b Add_Jet_Fcn git@github.com:BNL-FCCee/FCCAnalyses.git FCCAnalyses_BNL_Dev
```
