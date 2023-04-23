"""
25 January 2023
Abraham Tishelman-Charny

The purpose of this python module is to run the plotting step of the FCC analysis for Z(cc)H. 

"""

import yaml 
import ROOT

configFile = "/afs/cern.ch/work/a/atishelm/private/FCC/BNL-Analyses/RunConfig.yaml" # for the moment, need to specify full path so that HTCondor node can find this file (since afs is mounted). Need to check how to pass this as an input file to HTCondor job.
with open(configFile, 'r') as cfg:
    values = yaml.safe_load(cfg)
    
    batch = values["batch"]
    EOSoutput = values["EOSoutput"]
    JobName = values["JobName"]

print("batch:",batch)
print("EOSoutput:",EOSoutput)
print("JobName:",JobName)

import ROOT

# global parameters
intLumi        = 5e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow Z(cc)H'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
addMoreVars = 0
#allSamples = 1

if(EOSoutput):
    inputDir = f"/eos/user/a/atishelm/ntuples/FCC/{JobName}/final/"
else:
    inputDir       = f'{JobName}/final/'

formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = f'/eos/user/a/atishelm/www/FCC/{JobName}/plots/'

# add vars
variables = [
    #"all_invariant_masses",
    #"event_njet",
    #"recojetpair_isC",
    #"recojetpair_isB",
    #"recoil_masses"
    "recoil_masses_HiggsPeak"
    #"jet_nconst"
]


if(addMoreVars):

    # add more vars
    flavors = ["G", "Q", "S", "C", "B"]

    for flavor in flavors:
        varName = f"recojet_is{flavor}"
        variables.append(varName)

    constituent_types = ["mu", "el", "chad", "nhad", "gamma"]
    const_nbins, const_xmin, const_xmax = 20, 0, 20
    for const_type in constituent_types:
        varName = f"jet_n{const_type}"
        variables.append(varName)

    kins = ["p", "e", "phi", "theta"]
    for kin in kins:
        varName = f"jet_{kin}"
        variables.append(varName)

# Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ZccH'] = [
    #"selNone",
    #"4Jets",
    #"4JetsBpair", 
    #"4JetsCpair"
    #"4JetsOneBpairHiggsMassWindow",
    #"4JetsOneCpairHiggsMassWindow",
    "4JetsOneCpairHiggsMassWindowOnlyThatPair"
]

selections['ZccH_combined'] = [
    #"selNone",
    #"4Jets",
    #"4JetsBpair", 
    #"4JetsCpair"
    #"4JetsOneBpairHiggsMassWindow",
    #"4JetsOneCpairHiggsMassWindow",
    "4JetsOneCpairHiggsMassWindowOnlyThatPair"
]

extralabel = {}
extralabel['selNone'] = "No selections"
extralabel['4Jets'] = "Exactly 4 jets"
extralabel['4JetsBpair'] = "4jets + recojetpair_isB>1.8"
extralabel['4JetsCpair'] = "4jets + recojetpair_isC>1.8"
# extralabel['4JetsOneBpairHiggsMassWindow'] = "#splitline{Ex one jet pair}{B tagged, near Higgs window}"
# extralabel['4JetsOneCpairHiggsMassWindow'] = "#splitline{Ex one jet pair}{C tagged, near Higgs window}"

extralabel['4JetsOneBpairHiggsMassWindow'] = "B tagged jet pairs == 1"
extralabel['4JetsOneCpairHiggsMassWindow'] = "Exactly one c-tagged jet pair"

extralabel['4JetsOneCpairHiggsMassWindowOnlyThatPair'] = "Exactly one c-tagged jet pair"

# custom colors
class Color(int):
    """Create a new ROOT.TColor object with an associated index"""
    #__slots__ = ["object", "name"]

    def __new__(cls, r, g, b, name=""):
        self = int.__new__(cls, ROOT.TColor.GetFreeColorIndex())
        self.object = ROOT.TColor(self, r, g, b, name, 1.0)
        self.name = name
        return self

custom_colors = [
        Color(86/255., 88/255., 126/255., "fccdeepblue"),
        Color(170/255., 122/255., 347/255., "energy"),
        Color( 183/255., 169/255., 155/255.,"earth"), 

        Color(1,0,0, "Red"),
        Color(1,69/255.,0, "Orange_Red"),
        Color(1,140/255.,0, "Orange"),
        Color(1,215/255.,0, "Yellow_Orange"),
        Color(1,1,0, "Yellow"),
        Color(154/255.,205/255.,0, "Yellow_Green"),
        Color(0,128/255.,0, "Green"),
        Color(0,191/255.,1, "Blue_Green"),
        Color(0,0,1, "Blue"),
        Color(238/255.,130/255.,238/255., "Violet"),
        ]

for color in custom_colors:
    setattr(ROOT, color.name, color)

colors = {}

# exclusive 

# ZccH
# colors['ZccHbb'] = ROOT.kRed
# colors['ZccHmumu'] = ROOT.kRed+2
# colors['ZccHWW'] = ROOT.kGreen
# colors['ZccHgg'] = ROOT.kGreen+4
# colors['ZccHZa'] = ROOT.kBlue
# colors['ZccHss'] = ROOT.kBlue+2
# colors['ZccHcc'] = ROOT.kMagenta-9
# colors['ZccHmumu'] = ROOT.kMagenta+2
# colors['ZccHZZ'] = ROOT.kBlack
# colors['ZccHaa'] = ROOT.kGray
# colors['ZccHtautau'] = ROOT.kViolet

#ROOT.gStyle.SetPalette(55)

colors['ZccHbb'] = ROOT.Red
colors['ZccHWW'] = ROOT.Orange_Red
colors['ZccHtautau'] = ROOT.Orange
colors['ZccHgg'] = ROOT.Yellow_Orange
colors['ZccHZa'] = ROOT.Yellow
colors['ZccHss'] = ROOT.Yellow_Green
colors['ZccHcc'] = ROOT.Green
colors['ZccHZZ'] = ROOT.Blue_Green
colors['ZccHaa'] = ROOT.Blue
colors['ZccHmumu'] = ROOT.Violet

# colors['ZccHbb'] = ROOT.Red
# colors['ZccHWW'] = ROOT.Orange_Red
# colors['ZccHmumu'] = ROOT.Orange
# colors['ZccHgg'] = ROOT.Yellow_Orange
# colors['ZccHZa'] = ROOT.Yellow
# colors['ZccHss'] = ROOT.Yellow_Green
# colors['ZccHcc'] = ROOT.Green
# colors['ZccHZZ'] = ROOT.Blue_Green
# colors['ZccHaa'] = ROOT.Blue
# colors['ZccHtautau'] = ROOT.Violet

colors['WW'] = ROOT.energy #"ROOT.fccdeepblue"
colors['ZZ'] = ROOT.earth

# nonres
colors['qq'] = ROOT.fccdeepblue

# inclusive 
colors['ZccH'] = ROOT.Red # signal 
colors['VV'] = ROOT.earth # background

plots = {}
plots['ZccH'] = {

    
    'signal' : {
        'ZccHbb' : ['wzp6_ee_ccH_Hbb_ecm240'],
        #'ZccHmumu': ['wzp6_ee_ccH_Hmumu_ecm240'],
        #'ZccHWW' : ['wzp6_ee_ccH_HWW_ecm240'],
        #'ZccHgg' :       ['wzp6_ee_ccH_Hgg_ecm240'],
        #'ZccHZa' :       ['wzp6_ee_ccH_HZa_ecm240'],
        #'ZccHss':        ['wzp6_ee_ccH_Hss_ecm240'],
        #'ZccHcc' :       ['wzp6_ee_ccH_Hcc_ecm240'],
        #'ZccHmumu' :       ['wzp6_ee_ccH_Hmumu_ecm240'],
        #'ZccHZZ':        ['wzp6_ee_ccH_HZZ_ecm240'],	
        #'ZccHtautau':        ['wzp6_ee_ccH_Htautau_ecm240'],
        #'ZccHaa':        ['wzp6_ee_ccH_Haa_ecm240'],
    },

    'backgrounds' : {
            #'WW':['p8_ee_WW_ecm240'],
            #'ZZ':['p8_ee_ZZ_ecm240'],
            #'qq' : ['p8_ee_Zqq_ecm240']
        }
}

plots['ZccH_combined'] = {

    'signal' : {

        'ZccH' : [
                    'wzp6_ee_ccH_Hbb_ecm240', 
                    #'wzp6_ee_ccH_Hmumu_ecm240',
                    #'wzp6_ee_ccH_HWW_ecm240',
                    #'wzp6_ee_ccH_Hgg_ecm240',
                    #'wzp6_ee_ccH_HZa_ecm240',
                    #'wzp6_ee_ccH_Hss_ecm240',
                    #'wzp6_ee_ccH_Hcc_ecm240',
                    #'wzp6_ee_ccH_HZZ_ecm240',
                    #'wzp6_ee_ccH_Htautau_ecm240',
                    #'wzp6_ee_ccH_Haa_ecm240'
                  ],
    },

    'backgrounds' : { 
                      #'VV' : ['p8_ee_WW_ecm240', 'p8_ee_ZZ_ecm240'],
                      #'qq' : ['p8_ee_Zqq_ecm240']
                    }

}

legend = {}
legend['ZccHbb'] = 'Z(cc)H(bb)'
legend['ZccHmumu'] = 'Z(cc)H(\mu\mu)'
legend['ZccHWW'] = 'Z(cc)H(WW)'
legend['ZccHgg'] = 'Z(cc)H(gg)'
legend['ZccHZa'] = 'Z(cc)H(Z\gamma)'
legend['ZccHss'] = 'Z(cc)H(ss)'
legend['ZccHcc'] = 'Z(cc)H(cc)'
legend['ZccHZZ'] = 'Z(cc)H(ZZ)'
legend['ZccHaa'] = 'Z(cc)H(\gamma\gamma)'
legend['ZccHtautau'] = 'Z(cc)H(\\tau\\tau)'

# VV 
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'
legend['qq'] = 'qq'

# inclusive 
legend['ZccH'] = 'ZccH'
legend['VV'] = 'VV'

# one column
#nCols = 1
#LegendTextSize = 0.035 # 1 columns

# three column
nCols = 3
LegendTextSize = 0.020
legendCoord    = [0.475,0.65,0.9,0.85] 