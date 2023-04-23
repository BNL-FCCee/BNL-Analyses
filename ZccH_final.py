"""
25 January 2023
Abraham Tishelman-Charny

The purpose of this python module is to run the 'final' step of the FCC analysis for Z(cc)H. Started with examples in repo. 

Does batch mode not work for this step?
"""

import yaml 

configFile = "/afs/cern.ch/work/a/atishelm/private/FCC/BNL-Analyses/RunConfig.yaml" # for the moment, need to specify full path so that HTCondor node can find this file (since afs is mounted). Need to check how to pass this as an input file to HTCondor job.
with open(configFile, 'r') as cfg:
    values = yaml.safe_load(cfg)
    
    batch = values["batch"]
    EOSoutput = values["EOSoutput"]
    JobName = values["JobName"]

print("batch:",batch)
print("EOSoutput:",EOSoutput)
print("JobName:",JobName)

oneFile = 0

if(oneFile):
    processList = {
        # backgrounds. Option: 'fraction' : frac_value
        'p8_ee_ZZ_ecm240_oneFile':{'chunks':1},
        'p8_ee_WW_ecm240_oneFile':{'chunks':1},
        'p8_ee_Zqq_ecm240_oneFile':{'chunks':1},
    }

    procDictAdd={"p8_ee_WW_ecm240_oneFile":
                    {"numberOfEvents": 700000, "sumOfWeights": 700000, "crossSection": 16.4385, "kfactor": 1.0, "matchingEfficiency": 1.0},
                "p8_ee_Zqq_ecm240_oneFile": 
                    {"numberOfEvents": 200000, "sumOfWeights": 200000, "crossSection": 52.6539, "kfactor": 1.0, "matchingEfficiency": 1.0},
                "p8_ee_ZZ_ecm240_oneFile": 
                    {"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 1.35899, "kfactor": 1.0, "matchingEfficiency": 1.0},                
                    }

else:
    processList = {
        # Z(cc)H by higgs final state 
        #'wzp6_ee_ccH_HWW_ecm240':{'chunks':20},
        #'wzp6_ee_ccH_Hgg_ecm240' : {'chunks':20},
        #'wzp6_ee_ccH_HZa_ecm240' : {'chunks':20},
        #'wzp6_ee_ccH_Hss_ecm240' : {'chunks':20},
        #'wzp6_ee_ccH_Hmumu_ecm240':{'chunks':20},
        #'wzp6_ee_ccH_HZZ_ecm240' : {'chunks':20},	
        #'wzp6_ee_ccH_Htautau_ecm240' : {'chunks':20},
        #'wzp6_ee_ccH_Haa_ecm240' : {'chunks':20},
        #'wzp6_ee_ccH_Hcc_ecm240' : {'chunks':20},
        'wzp6_ee_ccH_Hbb_ecm240':{'chunks':20},

        # backgrounds. Option: 'fraction' : frac_value
        #'p8_ee_WW_ecm240' : {'chunks':3740},
        #'p8_ee_ZZ_ecm240' : {'chunks':562},
        #'p8_ee_Zqq_ecm240' : {'chunks':1007}
        
    }

#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_winter2023_IDEA.json" 

if(EOSoutput):
    inputDir    = f"/eos/user/a/atishelm/ntuples/FCC/{JobName}/stage1/"
    outputDir = f"/eos/user/a/atishelm/ntuples/FCC/{JobName}/final/"
    #eosType = "eosuser"
else:
    inputDir    = f"{JobName}/stage1/"
    outputDir   = f"{JobName}/final/"

runBatch    = batch
batchQueue = "longlunch" # 2 hours
saveTabular = True
doScale = 1
intLumi        = 5e+06 #in pb-1

#compGroup = "group_u_FCC.local_gen"

#produces ROOT TTrees, default is False
#doTree = True

# Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file

# Build cut strings w/ python
flavors = ["B", "C"]

score_cut = 1.8
Njet_pairs = 6

for flavor in flavors:
    exec("ExOne%spair_str = ''"%(flavor))
    for i in range(Njet_pairs): # 6 jet pairs total if Njets = 4
        s = "(recojetpair_is%s[%s] > %s)"%(flavor, i, score_cut)
        if(i != (Njet_pairs - 1)): # not last one 
            s += " + "
        exec("ExOne%spair_str += s"%(flavor))

ExOneJetmassNearHiggs = "( "
for i in range(Njet_pairs):
    s = " ((recoil_masses[%s] > 115) && (recoil_masses[%s] < 140)) "%(i, i)
    if(i != (Njet_pairs -1 )):
        s += " + "
    ExOneJetmassNearHiggs += s

ExOneJetmassNearHiggs += " ) == 1"

# combined to get one jet pair which is flavor tagged AND that same pair has a recoil mass near the higgs peak
for flavor in flavors:
    exec("ExOneJetPairNearHiggs%sTagged_str = '('"%(flavor))

    for i in range(Njet_pairs):
        s = f" ((recoil_masses[{i}] > 115) && (recoil_masses[{i}] < 140) && recojetpair_is{flavor}[{i}] > {score_cut} ) "
        if(i != (Njet_pairs -1 )):
            s += " + "
        exec("ExOneJetPairNearHiggs%sTagged_str += s"%(flavor))

    exec("ExOneJetPairNearHiggs%sTagged_str += ' ) == 1' "%(flavor))

#print("ExOneJetmassNearHiggs:",ExOneJetmassNearHiggs)
#print("ExOneBpair_str: ",ExOneBpair_str)
#print("ExOneCpair_str: ",ExOneCpair_str)
#print("ExOneJetPairNearHiggsBTagged_str:",ExOneJetPairNearHiggsBTagged_str)
#print("ExOneJetPairNearHiggsCTagged_str:",ExOneJetPairNearHiggsCTagged_str)

cutList = {
    #"selNone" : "1",
    #"4Jets" : "event_njet==4",

    #"4JetsOneBpair" : f"event_njet==4 && ( {ExOneBpair_str} ) == 1",
    #"4JetsOneCpair" : f"event_njet==4 && ( {ExOneCpair_str} ) == 1",

    #"4JetsOneBpairHiggsMassWindow" : f"event_njet==4 && ({ExOneJetPairNearHiggsBTagged_str})",
    "4JetsOneCpairHiggsMassWindow" : f"event_njet==4 && ({ExOneJetPairNearHiggsCTagged_str})",
    
    #"4JetsOneCpairHiggsMassWindowOnlyThatPair" : f"event_njet==4 && ({ExOneJetPairNearHiggsCTagged_str}) ",
}

cutLabels = {
    #"selNone" : "No Selection",
    #"4Jets" : "Exactly 4 jets",
    #"4JetsOneBpair" : "Njets == 4, one B pair score $>$ 1.8",
    #"4JetsOneCpair" : "Njets == 4, one C pair score $>$ 1.8",
    "4JetsOneBpairHiggsMassWindow" : "Ex one jet pair B tagged, near Higgs window",
    "4JetsOneCpairHiggsMassWindow" : "Ex one jet pair C tagged, near Higgs window",
    
    "4JetsOneCpairHiggsMassWindowOnlyThatPair" : "Ex one jet pair C tagged, near Higgs window"
}

#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {

    # "all_invariant_masses" : {"name":"all_invariant_masses", 
    #                           "title" : "all_invariant_masses" ,
    #                           "bin" : 50,
    #                           "xmin" : 0,
    #                           "xmax" : 250},

    "recoil_masses" :         {"name" : "recoil_masses", 
                               "title" : "Recoil mass" , 
                               "bin" : 50, 
                               "xmin" : 0, 
                               "xmax" : 250},

    "recoil_masses_HiggsPeak" :{"name" : "recoil_masses", 
                              "title" : "Recoil mass" , 
                              "bin" : 20, 
                              "xmin" : 115, 
                              "xmax" : 140},                              

    # "event_njet" :            {"name":"event_njet", 
    #                           "title" : "event_njet" ,
    #                           "bin" : 10,
    #                           "xmin" : 0,
    #                           "xmax" : 10},

     "recojetpair_isC" :       {"name":"recojetpair_isC", 
                               "title" : "Jet pair c-score" ,
                               "bin" : 40,
                               "xmin" : 0,
                               "xmax" : 2},   

     "Leading_recojetpair_isC" :{"name":"recojetpair_isC[0]", 
                               "title" : "Leading jet pair c-score" ,
                               "bin" : 40,
                               "xmin" : 0,
                               "xmax" : 2},                                  
                                                                       
    # "recojetpair_isB" :       {"name":"recojetpair_isB", 
    #                           "title" : "recojetpair_isB" ,
    #                           "bin" : 40,
    #                           "xmin" : 0,
    #                           "xmax" : 2}, 
    
    # "jet_p":                  {"name" : "jet_p",
    #                            "title" : "jet_p",
    #                            "bin" : 40,
    #                            "xmin" : 0,
    #                            "xmax" : 200},

    # "jet_e":                  {"name" : "jet_e",
    #                            "title" : "jet_e",
    #                            "bin" : 40,
    #                            "xmin" : 0,
    #                            "xmax" : 200},

    # "jet_phi":                 {"name" : "jet_phi",
    #                            "title" : "jet_phi",
    #                            "bin" : 30,
    #                            "xmin" : 0,
    #                            "xmax" : 6.4},

    # "jet_theta":               {"name" : "jet_theta",
    #                            "title" : "jet_theta",
    #                            "bin" : 30,
    #                            "xmin" : 0,
    #                            "xmax" : 3.3},      

    # "jet_nconst":              {"name" : "jet_nconst",
    #                            "title" : "jet_nconst",
    #                            "bin" : 200,
    #                            "xmin" : 0,
    #                            "xmax" : 200},                                                                                                                                                               

}

# add variables in a smart way with python

# flavors = ["G", "Q", "S", "C", "B"]
# flavor_nbins, flavor_xmin, flavor_xmax = 40, 0, 1

# for flavor in flavors:
#     varName = f"recojet_is{flavor}"
#     histoList[varName] = {
#         "name" : varName,
#         "title" : varName,
#         "bin": flavor_nbins,
#         "xmin" : flavor_xmin,
#         "xmax" : flavor_xmax
#     }


# constituent_types = ["mu", "el", "chad", "nhad", "gamma"]
# const_nbins, const_xmin, const_xmax = 20, 0, 20
# for const_type in constituent_types:
#     varName = f"jet_n{const_type}"
#     histoList[varName] = {
#         "name" : varName,
#         "title" : varName,
#         "bin" : const_nbins,
#         "xmin" : const_xmin,
#         "xmax" : const_xmax
#     }
