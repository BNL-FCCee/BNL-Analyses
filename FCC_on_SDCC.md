# FCC on SDCC

Quickstart:

Example ssh into BNL cluster:

```
sudo ssh -i .ssh/id_rsa atishelma@ssh.sdcc.bnl.gov # asks you for your PC password
rterm -i spar0103 # or ssh atishelma@spar0103.usatlas.bnl.gov - asks you for your bnl account password
```

Clone `FCCAnalyses`:

```
mkdir FCC_at_BNL
cd FCC_at_BNL
```

via https:

```
git clone https://github.com/BNL-FCCee/FCCAnalyses.git -b ZH_Hadronic_SelfCoupling
```

via ssh:

```
git clone git@github.com:BNL-FCCee/FCCAnalyses.git -b ZH_Hadronic_SelfCoupling
```

set up:

```
cd FCCAnalyses
source /cvmfs/sw.hsf.org/key4hep/releases/2023-06-05-fcchh/x86_64-centos7-gcc12.2.0-opt/key4hep-stack/*/setup.sh
source setup.sh
fccanalysis build
```

change `outputDir` variable in `ZH_Hadronic_stage1.py` to desired output location, then process a few files:

```
fccanalysis run ZH_Hadronic_stage1.py --output wzp6_ee_ccH_Hcc_ecm240.root --files-list /eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_ccH_Hcc_ecm240/events_056080797.root --nev 10
```

check that your output file is there:

```
root -l <outputDir>/wzp6_ee_ccH_Hcc_ecm240.root
```

to submit on `HTCondor`, edit the `ZH_Hadronic_stage1.py` configuration file parameters to the desired values, for example:

```
batch = 1 # use HTCondor
EOSoutput = 0 # output to EOS
JobName = "ZHadronic_4JetReco" # job name used for output directory
njets = 4 # number of jets in exclusive reclustering
outputDir   = f"/usatlas/atlas01/atlasdisk/users/<BNLclusterUsername>/{JobName}/stage1/"
```

and in the same file, choose the samples to run over, for example just one ZH process:

```
processList = {
    "wzp6_ee_bbH_Hbb_ecm240" : {'chunks' : 2},
}
```

then run without the extra flags from before:

```
fccanalysis run ZH_Hadronic_stage1.py
```

see if your jobs were submitted:

```
condor_q
condor_q -batch
```

______________________________
______________________________
______________________________

## Extra information

Cloning and building the [`FCCAnalyses`](https://github.com/HEP-FCC/FCCAnalyses) repository on the [BNL SDCC](https://www.sdcc.bnl.gov/) ATLAS cluster should largely follow the same steps as cloning and building the repository on [`lxplus`](https://abpcomputing.web.cern.ch/computing_resources/lxplus/).

Currently, one known difference is that when building on SDCC, one must add the following line to their `CMakeLists.txt` file:

```
link_directories(/cvmfs/sw.hsf.org/spackages7/intel-tbb/2020.3/x86_64-centos7-gcc11.2.0-opt/ey3ft/lib /cvmfs/sw.hsf.org/spackages7/zlib/1.2.13/x86_64-centos7-gcc11.2.0-opt/2wmsk/lib)
```

Example ssh into BNL cluster:

```
sudo ssh -i .ssh/id_rsa atishelma@ssh.sdcc.bnl.gov
rterm -i spar0103 # or ssh atishelma@spar0103.usatlas.bnl.gov
bash
```

When cloning the master branch of `FCCAnalyses`, I found I had to source a particular key4hep stack and build like so:

```
source /cvmfs/sw.hsf.org/key4hep/releases/2023-06-05-fcchh/x86_64-centos7-gcc12.2.0-opt/key4hep-stack/*/setup.sh
source setup.sh
fccanalysis build
```

Run the ZH hadronic ntupler:

```
fccanalysis run ZH_Hadronic_stage1.py --output wzp6_ee_ccH_Hcc_ecm240.root --files-list /eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_ccH_Hcc_ecm240/events_056080797.root --nev 10
```

Lines I found useful to add in my ~/.vimrc:

```
hi Search cterm=NONE ctermfg=grey ctermbg=blue
:set number
```

Lines I found useful to add in my ~/.bashrc:

```
export KRB5CCNAME=$HOME/krb5cc_`id -u`
kinit atishelm@CERN.CH
alias 'l=ls -lrt --color=auto'
alias 'gst=git status'
stty erase '^?' # fix vim backspace issue
alias grep='grep --color=auto'
```

Stat analysis related commands after producing ntuples:

In CharmCutCode repo, to process one file:

```
runAnalysis --nEvents 1000 --inputFileList /eos/user/a/atishelm/ntuples/FCC/ZH_Hadronic_4JetReco/wzp6_ee_ccH_Hbb_ecm240/chunk0.root --analType SelfCoupling --sampleName wzp6_ee_ccH_Hbb_ecm240 --processName Hbb
```

Run over everything with condor:

```

```
