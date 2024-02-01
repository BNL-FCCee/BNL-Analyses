# FCC on SDCC

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
