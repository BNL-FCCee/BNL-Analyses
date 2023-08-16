# run as: fccanalysis run analysis_HInvee_stage1.py

#Mandatory: List of processes
processList = {
    #'p8_ee_ZZ_ecm240':{},#Run the full statistics in one output file named <outputDir>/p8_ee_ZZ_ecm240.root
    #'p8_ee_WW_ecm240':{'fraction':0.5, 'chunks':2}, #Run 50% of the statistics in two files named <outputDir>/p8_ee_WW_ecm240/chunk<N>.root
    'wzp6_ee_eeH_ecm240':{'fraction':1, 'output':'wzp6_ee_eeH_ecm240'} #Run 100% of the statistics in one file named <outputDir>/p8_ee_ZH_ecm240_out.root (example on how to change the output name)
    #'wzp6_ee_mumuH_ecm240':{'chunks':5, 'output':'wzp6_ee_mumuH_ecm240'} #Run 100% of the statistics in one file named <outputDir>/p8_ee_ZH_ecm240_out.root (example on how to change the output name)

    
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs_HInvee_IDEA/stage1"

#Optional: analysisName, default is ""
#analysisName = "My Analysis"

#Optional: ncpus, default is 4
nCPUS       = 4

#Optional running on HTCondor, default is False
runBatch    = False

#Optional batch queue name when running on HTCondor, default is workday
#batchQueue = "longlunch"
batchQueue = "tomorrow"

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
            .Filter("n_muons==0")

            # define an alias for electron index collection
            .Alias("Electron0", "Electron#0.index")
            # define the electron collection
            .Define("electrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
            # define number of electrons
            .Define("n_electrons",  "ReconstructedParticle::get_n( electrons ) ")
            # Filter at on the number of electrons
            .Filter("n_electrons==2")

            .Define("electrons_pt", "ReconstructedParticle::get_pt(electrons)")
            # create branch with muon rapidity
            .Define("electrons_y",  "ReconstructedParticle::get_y(electrons)")
            # create branch with muon total momentum
            .Define("electrons_p",   "ReconstructedParticle::get_p(electrons)")
            # create branch with muon energy
            .Define("electrons_e",   "ReconstructedParticle::get_e(electrons)")

            .Define("MET", "ReconstructedParticle::get_pt(MissingET)") #absolute value of MET
            #.Define("METSorted", "Sort(MET)") #absolute value of MET

            .Define("jets", "ReconstructedParticle::sel_pt(15)(Jet)") # Loosest selection at this stage
            # define number of jets
            .Define("n_jets",  "ReconstructedParticle::get_n( jets ) ")

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

            ### Filter for Higgs to invisible, e.g. neutrinos ###
            
            # truth selection / filtering
            .Alias("Particle1", "Particle#1.index")
            .Define("Higgs", "FCCAnalyses::MCParticle::sel_pdgID(25, true)(Particle)")

           # https://github.com/HEP-FCC/FCCAnalyses/blob/dce3af87057a930fa0e0cd55dc26f8e4ba7b5143/examples/FCCee/tutorials/vertexing/analysis_Bs2JpsiPhi_MCseeded.py

           # MC indices of the decay Higgs (PDG = 25) -> nu_e+ (PDG = -12) nu_e- (PDG = 12) nu_mu+ (PDG = -14) nu_mu- (PDG = 14), etc.
           # Retrieves a vector of int's which correspond to indices in the Particle block
           # vector[0] = the mother, and then the daughters in the order specified, i.e. here
           #       [1] = the nu_e+, [2] = the nu_e-, [3] = the nu_mu+, [4] = the nu_mu-
           # Boolean arguments :
           #    1st: stableDaughters. when set to true, the daughters specified in the list are looked
           #             for among the final, stable particles that come out from the mother, i.e. the decay tree is
           #             explored recursively if needed.
           #        2nd: chargeConjugateMother
           #        3rd: chargeConjugateDaughters
           #        4th: inclusiveDecay: when set to false, if a mother is found, that decays
           #             into the particles specified in the list plus other particle(s), this decay is not selected.
           # If the event contains more than one such decays,only the first one is kept.
            .Define("HiggsToInvIndices_4NUe",       "MCParticle::get_indices( 25, {-12,12,-12,12}, true, true, true, false) ( Particle, Particle1)" )
            .Define("HiggsToInvIndices_2NUe_2NUmu", "MCParticle::get_indices( 25, {-14,14,-12,12}, true, true, true, false) ( Particle, Particle1)" )
            .Define("HiggsToInvIndices_4NUe_2NUtau","MCParticle::get_indices( 25, {-16,16,-12,12}, true, true, true, false) ( Particle, Particle1)" )

            .Define("HiggsToInvIndices_4NUmu",       "MCParticle::get_indices( 25, {-14,14,-14,14}, true, true, true, false) ( Particle, Particle1)" )
            .Define("HiggsToInvIndices_4NUmu_2NUtau","MCParticle::get_indices( 25, {-16,16,-14,14}, true, true, true, false) ( Particle, Particle1)" )

            .Define("HiggsToInvIndices_4NUtau","MCParticle::get_indices( 25, {-16,16,-16,16}, true, true, true, false) ( Particle, Particle1)" )

           # select events for which the requested decay chain has been found:
           #.Filter("HiggsToInvIndices.size() > 0")

            .Filter("HiggsToInvIndices_4NUe.size()  > 0 || HiggsToInvIndices_2NUe_2NUmu.size()  > 0 || HiggsToInvIndices_4NUe_2NUtau.size()  > 0 || HiggsToInvIndices_4NUmu.size()  > 0 || HiggsToInvIndices_4NUmu_2NUtau.size()  > 0 || HiggsToInvIndices_4NUtau.size()  > 0  ")


        )
        return df2 

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            "electrons_pt",
            "electrons_y",
            "electrons_p",
            "electrons_e",
            "ZBosonPt",
            "ZBosonMass",
            "MET",
            "recoil_M",
            "n_jets"

        ]
        return branchList
