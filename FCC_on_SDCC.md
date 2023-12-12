# FCC on SDCC

Cloning and building the [`FCCAnalyses`](https://github.com/HEP-FCC/FCCAnalyses) repository on the [BNL SDCC](https://www.sdcc.bnl.gov/) ATLAS cluster should largely follow the same steps as cloning and building the repository on [`lxplus`](https://abpcomputing.web.cern.ch/computing_resources/lxplus/).

Currently, one known difference is that when building on SDCC, one must add the following line to their `CMakeLists.txt` file:

```
link_directories(/cvmfs/sw.hsf.org/spackages7/intel-tbb/2020.3/x86_64-centos7-gcc11.2.0-opt/ey3ft/lib /cvmfs/sw.hsf.org/spackages7/zlib/1.2.13/x86_64-centos7-gcc11.2.0-opt/2wmsk/lib)
```

## 12 December 2023 setup

When cloning the master branch of `FCCAnalyses`, I found I had to source this stack of key4hep on the cluster:

```
source /cvmfs/sw.hsf.org/key4hep/releases/2023-06-05-fcchh/x86_64-centos7-gcc12.2.0-opt/key4hep-stack/*/setup.sh
```

Run the ZH hadronic ntupler:

```
fccanalysis run ZH_Hadronic_stage1.py --output wzp6_ee_ccH_Hcc_ecm240.root --files-list /eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_ccH_Hcc_ecm240/events_056080797.root --ncpus 64 --nev 10
```
