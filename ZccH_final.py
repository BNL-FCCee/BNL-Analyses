"""
25 January 2023
Abraham Tishelman-Charny

The purpose of this python module is to run the 'final' step of the FCC analysis for Z(cc)H. Started with examples in repo. 

Does batch mode not work for this step?
"""

import yaml 

configFile = "/afs/cern.ch/work/a/atishelm/private/HInvisible/RunConfig.yaml" # for the moment, need to specify full path so that HTCondor node can find this file (since afs is mounted). Need to check how to pass this as an input file to HTCondor job.
with open(configFile, 'r') as cfg:
    values = yaml.safe_load(cfg)
    
    batch = values["batch"]
    EOSoutput = values["EOSoutput"]
    JobName = values["JobName"]

print("batch:",batch)
print("EOSoutput:",EOSoutput)
print("JobName:",JobName)

processList = {
    # Z(cc)H by higgs final state 
    # 'wzp6_ee_ccH_HWW_ecm240':{'chunks':20},
    # 'wzp6_ee_ccH_Hgg_ecm240' : {'chunks':20},
    # 'wzp6_ee_ccH_HZa_ecm240' : {'chunks':20},
    # 'wzp6_ee_ccH_Hss_ecm240' : {'chunks':20},
    #'wzp6_ee_ccH_Hcc_ecm240' : {'chunks':20},
    # 'wzp6_ee_ccH_Hmumu_ecm240':{'chunks':20},
    # 'wzp6_ee_ccH_HZZ_ecm240' : {'chunks':20},	
    # 'wzp6_ee_ccH_Htautau_ecm240' : {'chunks':20},
    # 'wzp6_ee_ccH_Haa_ecm240' : {'chunks':20},
    'wzp6_ee_ccH_Hbb_ecm240':{'chunks':20},

    # backgrounds
    #'p8_ee_WW_ecm240' : {'chunks':20},
    #'p8_ee_ZZ_ecm240' : {'chunks':20},
    #'p8_ee_Zqq_ecm240' : {'chunks':20}
}

#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_winter2023_IDEA.json" 

if(EOSoutput):
    inputDir    = f"/eos/user/a/atishelm/ntuples/FCC/{JobName}/stage1/"
    outputDir = f"/eos/user/a/atishelm/ntuples/FCC/{JobName}/final/"
    eosType = "eosuser"
else:
    inputDir    = f"{JobName}/stage1/"
    outputDir   = f"{JobName}/final/"

nCPUS       = 4
runBatch    = batch
batchQueue = "longlunch" # 2 hours
#compGroup = "group_u_FCC.local_gen"

#Add MySample_p8_ee_ZH_ecm240 as it is not an offical process
#procDictAdd={"MySample_p8_ee_ZH_ecm240":{"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 0.201868, "kfactor": 1.0, "matchingEfficiency": 1.0}}

#Number of CPUs to use
nCPUS = 64

#produces ROOT TTrees, default is False
doTree = True

# Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    "NoSelection" : "1",
}

#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {

    "all_invariant_masses" : {"name":"all_invariant_masses", 
                              "title" : "all_invariant_masses" ,
                              "bin" : 50,
                              "xmin" : 0,
                              "xmax" : 250},

    "event_njet" :            {"name":"event_njet", 
                              "title" : "event_njet" ,
                              "bin" : 10,
                              "xmin" : 0,
                              "xmax" : 10},

    "recojetpair_isC" :       {"name":"recojetpair_isC", 
                              "title" : "recojetpair_isC" ,
                              "bin" : 40,
                              "xmin" : 0,
                              "xmax" : 2},                                           
    "recojetpair_isB" :       {"name":"recojetpair_isB", 
                              "title" : "recojetpair_isB" ,
                              "bin" : 40,
                              "xmin" : 0,
                              "xmax" : 2}, 
    
    "jet_p":                  {"name" : "jet_p",
                               "title" : "jet_p",
                               "bin" : 40,
                               "xmin" : 0,
                               "xmax" : 200},

    "jet_e":                  {"name" : "jet_e",
                               "title" : "jet_e",
                               "bin" : 40,
                               "xmin" : 0,
                               "xmax" : 200},

    "jet_phi":                 {"name" : "jet_phi",
                               "title" : "jet_phi",
                               "bin" : 20,
                               "xmin" : -10,
                               "xmax" : 10},

    "jet_theta":               {"name" : "jet_theta",
                               "title" : "jet_theta",
                               "bin" : 20,
                               "xmin" : -10,
                               "xmax" : 10},      

    "jet_nconst":              {"name" : "jet_nconst",
                               "title" : "jet_nconst",
                               "bin" : 100,
                               "xmin" : 0,
                               "xmax" : 100},                                                                                                                                                               

}

# add variables in a smart way with python

flavors = ["G", "Q", "S", "C", "B"]
flavor_nbins, flavor_xmin, flavor_xmax = 40, 0, 1

for flavor in flavors:
    varName = f"recojet_is{flavor}"
    histoList[varName] = {
        "name" : varName,
        "title" : varName,
        "bin": flavor_nbins,
        "xmin" : flavor_xmin,
        "xmax" : flavor_xmax
    }


constituent_types = ["mu", "el", "chad", "nhad", "gamma"]
const_nbins, const_xmin, const_xmax = 20, 0, 20
for const_type in constituent_types:
    varName = f"jet_n{const_type}"
    histoList[varName] = {
        "name" : varName,
        "title" : varName,
        "bin" : const_nbins,
        "xmin" : const_xmin,
        "xmax" : const_xmax
    }