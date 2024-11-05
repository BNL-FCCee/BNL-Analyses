# run as: fccanalysis run analysis_HInvMuMu_stage1.py

#Mandatory: List of processes
processList = {
    #'p8_ee_ZZ_ecm240':{},#Run the full statistics in one output file named <outputDir>/p8_ee_ZZ_ecm240.root
    #'p8_ee_WW_ecm240':{'fraction':0.5, 'chunks':2}, #Run 50% of the statistics in two files named <outputDir>/p8_ee_WW_ecm240/chunk<N>.root
    'wzp6_ee_mumuH_ecm240':{'fraction':1., 'output':'wzp6_ee_mumuH_ecm240'} #Run 100% of the statistics in one file named <outputDir>/p8_ee_ZH_ecm240_out.root (example on how to change the output name)
    #'wzp6_ee_mumuH_ecm240':{'chunks':5, 'output':'wzp6_ee_mumuH_ecm240'} #Run 100% of the statistics in one file named <outputDir>/p8_ee_ZH_ecm240_out.root (example on how to change the output name)

    
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs_HInvMuMu/stage1"

#Optional: analysisName, default is ""
#analysisName = "My Analysis"

#Optional: ncpus, default is 4
nCPUS       = 1

#Optional running on HTCondor, default is False
#runBatch    = True

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
#compGroup = "group_u_FCC.local_gen"

#Optional test file
#testFile ="root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm240/events_017670037.root"


#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (

            # it looks like the 'ReconstructedParticles' are implemented as 'ROOT::VecOps::RVec':
            # https://root.cern.ch/doc/master/classROOT_1_1VecOps_1_1RVec.html

            df
            # define an alias for muon index collection
            .Alias("Muon0", "Muon#0.index")
            # define the muon collection
            .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            # define number of muons
            .Define("n_muons",  "ReconstructedParticle::get_n( muons ) ")
            # Filter at on the number of muons
            .Filter("n_muons==2")

            # define an alias for electron index collection
            .Alias("Electron0", "Electron#0.index")
            # define the electron collection
            .Define("electrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
            # define number of electrons
            .Define("n_electrons",  "ReconstructedParticle::get_n( electrons ) ")
            # Filter at on the number of electrons
            .Filter("n_electrons==0")

            .Define("muons_pt", "ReconstructedParticle::get_pt(muons)")
            # create branch with muon rapidity
            .Define("muons_y",  "ReconstructedParticle::get_y(muons)")
            # create branch with muon total momentum
            .Define("muons_p",   "ReconstructedParticle::get_p(muons)")
            # create branch with muon energy
            .Define("muons_e",   "ReconstructedParticle::get_e(muons)")

            .Define("MET", "ReconstructedParticle::get_pt(MissingET)") #absolute value of MET
            #.Define("METSorted", "Sort(MET)") #absolute value of MET

            # build a candidate Z boson
            .Define("ZCandidate",    "ReconstructedParticle::resonanceBuilder(91)(muons)")
            # Z boson pt
            .Define("ZBosonPt",   "ReconstructedParticle::get_pt(ZCandidate)")
            # Z boson mass
            .Define("ZBosonMass",   "ReconstructedParticle::get_mass(ZCandidate)")

            .Define("recoilParticle",  "ReconstructedParticle::recoilBuilder(240)(ZCandidate)")
            # create branch with recoil mass
            .Define("recoil_M","ReconstructedParticle::get_mass(recoilParticle)")
            #.Filter("MET[0]>10.")
            #.Filter("zed_leptonic_recoil_m.size()>0")


        )
        return df2 

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            "muons_pt",
            "muons_y",
            "muons_p",
            "muons_e",
            "ZBosonPt",
            "ZBosonMass",
            "MET",
            "recoil_M",

        ]
        return branchList
