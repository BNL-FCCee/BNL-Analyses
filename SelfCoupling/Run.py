import os 

plotting = 0
workspaces = 1

variations = [
#     "FSR_studies_IDEA_BASE",
#     "FSR_studies_IDEA_nodndx_7labels",
    "FSR_studies_IDEA_noTOF_7labels"
]

if(workspaces):
    for variation in variations:
        c1 = f"python3 MakeXML_SMEFT.py --inFile workspaces/{variation}.root --outFile workspaces_modified/{variation}_modified.root --outXMLFile XML/{variation}.xml"
        print("$",c1)
        os.system(c1)

        c2 = f"quickstats modify_ws -i XML/{variation}.xml --input_workspace workspaces/{variation}.root "
        print("$",c2)
        os.system(c2)

        c3 = f'quickstats likelihood_scan -i workspaces_modified/{variation}_modified.root -p "Cphi=-3_3_0.1" -d asimovData --outdir {variation}'
        print("$",c3)
        os.system(c3)
    
if(plotting):
    ext = ""
    baseDir = "/direct/usatlas+u/atishelma/FCC/quickstats/SMEFT/"

    cmd = f"python3 plot.py --inputs {baseDir}FSR_studies_IDEA_BASE/Cphi.json,{baseDir}FSR_studies_IDEA_nodndx_7labels/Cphi.json,{baseDir}FSR_studies_IDEA_noTOF_7labels/Cphi.json --poi Cphi --NoInteractiveMode --labels FSR_studies_IDEA_BASE{ext},FSR_studies_IDEA_nodndx_7labels{ext},FSR_studies_IDEA_noTOF_7labels{ext} --xmin -1 --xmax 1"

    print("$",cmd)
    os.system(cmd)
