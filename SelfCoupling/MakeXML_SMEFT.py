"""
12 February 2024
Abraham Tishelman-Charny

The purpose of this script is to create an XML file for modifying a RooWorkspace to add SMEFT parameterization.

Example usage:

python3 MakeXML_SMEFT.py --inFile workspaces/runBase21Aug_WS_combined_wsfolder_model.root --outFile workspaces_modified/runBase21Aug_WS_SMEFT_modified.root --outXMLFile modify_ws_SMEFT_base.xml

python3 MakeXML_SMEFT.py --inFile workspaces/runWSHR21Aug_WS_combined_wsfolder_model.root --outFile workspaces_modified/runWSHR21Aug_WS_SMEFT_modified.root --outXMLFile modify_ws_SMEFT_worsenedRes.xml

"""

import argparse
import ROOT

# Create parser and get command line arguments 
parser = argparse.ArgumentParser()
parser.add_argument("--inFile", type=str, default=None, required=True, help="Input file")
parser.add_argument("--outFile", type=str, default="WS_combined_ws_model_SMEFT.root", required=True, help="Output file - name of output workspace")
parser.add_argument("--outXMLFile", type=str, default="modify_ws_SMEFT.xml", required=True, help="Output file - name of output workspace")

options = parser.parse_args()

inFile = options.inFile
outFile = options.outFile
outXMLFile = options.outXMLFile

file = ROOT.TFile(inFile, "READ")
ws = file.Get("combined")
snapshot_name = "NominalParamValues"
snapshot = ws.getSnapshot(snapshot_name)
iterator = snapshot.createIterator()
var = iterator.Next()

vals_dict = {}

while var:
    var_name = var.GetName()
    var_value = var.getVal()
    vals_dict[var_name] = var_value
    var = iterator.Next()
    
xml_template = f"""
<Organization InFile="{inFile}"
              OutFile="{outFile}"
              WorkspaceName="combined"
              DataName="asimovData"
              >

<!--Base parameters-->
<Item Name="mu[1]"/>
<Item Name="Cphi[-2.12766]"/>
<Item Name="deltaZ_precise[-0.001536]"/>
<Item Name="CSTrue_240GeV[1.0]"/>
<Item Name="CSLO_240GeV[1.0]"/>
<Item Name="C1_240GeV[0.017]"/>
<Item Name="dZh_240GeV[-0.00154]"/>
<Item Name="varKappaHZZ_240GeV[0.0]"/>
<Item Name="varKappa_240GeV[0.0]"/>

<Item Name="expr::mu_Cphi_Hbb    ('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>
<Item Name="expr::mu_Cphi_Hyy    ('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>
<Item Name="expr::mu_Cphi_HZZ    ('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>
<Item Name="expr::mu_Cphi_HWW    ('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>
<Item Name="expr::mu_Cphi_Htautau('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>
<Item Name="expr::mu_Cphi_HZa    ('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>
<Item Name="expr::mu_Cphi_Hgg    ('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>
<Item Name="expr::mu_Cphi_Hmumu  ('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>
<Item Name="expr::mu_Cphi_Hss    ('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>
<Item Name="expr::mu_Cphi_Hcc    ('((1./(1.-(@2)*((1 - 0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((1 - 0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi)"/>

<!--Might use this. Example.-->
<Item Name="Hbb_mod[0]"/>
<Item Name="expr::mu_Cphi_Hbb('@4*((1./(1.-(@2)*((-0.47 * @3)-1.)^2))*(@0)*(1. + (@1)*((-0.47 * @3)-1.)))', CSLO_240GeV, C1_240GeV, dZh_240GeV, Cphi, Hbb_mod)"/>
"""

# Ask Iza why these are missing (maybe too low yield in the ws creation step?)
params_to_skip = []

HiggsTruthFinalStates = ["WW", "ZZ", "Za", "bb", "cc", "gg", "ss", "tautau"]
ZFinalStateCats = ["bb", "cc", "qq", "ss"]
purities = ["Hi", "Mi", "L"]
HiggsFinalStateCats = ["bb", "cc", "ss", "gg"]

for HiggsTruthFinalState in HiggsTruthFinalStates:
    for purity in purities:
        for ZFinalStateCat in ZFinalStateCats:
            for HiggsFinalStateCat in HiggsFinalStateCats:
                param = f"N_H{HiggsTruthFinalState}_{purity}{ZFinalStateCat}H{HiggsFinalStateCat}"
                if(param in params_to_skip): 
                    print("Skipping",param)
                    continue
                try: 
                    param_val = vals_dict[param]
                except Exception as e:
                    print(f"Issue looking for {param}: {e} - continuing to next param...")
    
                line = f"<Item Name=\"expr::N_H{HiggsTruthFinalState}_{purity}{ZFinalStateCat}H{HiggsFinalStateCat}(\'{param_val} * @0\',mu_Cphi_H{HiggsTruthFinalState})\"/>"
                xml_template += line + "\n"

xml_template += "</Organization>\n"

with open(outXMLFile, "w") as f:
    f.write(xml_template) 
