"""
The purpose of this plotter is to plot likelihood scans using json files containing values.
"""

import os
import json
import pandas as pd
import numpy as np
import argparse

# https://gitlab.cern.ch/atlas-physics/HDBS/DiHiggs/yybb/hh_legacy_analysis/HH_Legacy_analysis_code/-/blob/29107c0adf2a9e79a380882c0416dc5423956801/bbyy_analysis_framework/plots/limit_scan_plot.py#L28-41
def get_intersections(x_data, y_data, x_theory, y_theory):
    # get the intersection between expected and theory prediction
    # interpolate expected limit with same number of datapoints as used in theory prediction
    interpolated_limit = np.interp(x_theory, x_data, y_data) 
    #limitm1 = n*np.array(limit_bands[0]) - 1
    limitm1 = interpolated_limit - y_theory 
    idx = np.argwhere(np.diff(np.sign(limitm1))).flatten() # determines what index intersection points are at 

    #linear interpolation to get exact intercepts: x = x1 + (x2-x1)/(y2-y1) * (y-y1)
    #y = 0 -> x = x1 - (x2-x1)/(y2-y1) * y1
    intersections = [x_theory[x] - (x_theory[x+1] - x_theory[x])/(limitm1[x+1] - limitm1[x]) * limitm1[x] for x in idx]
    
    return intersections

parser = argparse.ArgumentParser()
parser.add_argument('--inputs', required=True, help="comma separated list of input json files from poi scan using asimov dataset")
parser.add_argument('--labels', required=True, help="comma separated list of labels")
parser.add_argument('--unblind_input', required=False, default=None, help="input json file from poi scan using data")
parser.add_argument('--poi', required=True, help="scanned poi (reported on x-axis of the plot)")
parser.add_argument('--xmin', default=None, help="x min poi scan range", type=float)
parser.add_argument('--xmax', default=None, help="x max poi scan range", type=float)
parser.add_argument('--ymin', default=None, help="y min", type=float)
parser.add_argument('--ymax', default=None, help="y max", type=float)
parser.add_argument('--output', default='likelihood_scan_{poi}.pdf', help="output file name. Use {poi} to replace it with poi (defaults to likelihood_scan_{poi}.pdf)")
parser.add_argument('--outputDir', dest='outputDir', default='plots', help="folder to store plots (will create if not existing)") 
parser.add_argument('--NoInteractiveMode', dest='NoInteractiveMode', default=False, help="Turn off matplotlib interactive mode", action='store_true')
args = parser.parse_args()

NoInteractiveMode = args.NoInteractiveMode 

import matplotlib 
if(NoInteractiveMode): matplotlib.use('Agg') # turn off interactive mode
import matplotlib.pyplot as plt

import mplhep as hep 
plt.style.use(hep.style.ATLAS) # customization: https://mplhep.readthedocs.io/en/latest/api.html

if(args.unblind_input):
    data_obs = json.load(open(args.unblind_input))
    df_obs = pd.DataFrame(data_obs)
    df_obs = df_obs.drop(0)

poi_names = {
    'klambda' : '$\kappa_{\lambda}$',
    'Cphi' : '$C_{\phi}$',
    'mu_Hbb' : '$\mu_{H_{bb}}$',
    'mu_Hcc' : '$\mu_{H_{cc}}$',
    'mu_Hss' : '$\mu_{H_{ss}}$',
    'mu_Hgg' : '$\mu_{H_{gg}}$',
    'kl' : '$\kappa_{\lambda}}$',
    'd_kl' : '$\delta\kappa_{\lambda}}$',
    'chhh'  : '$c_{hhh}$',
    'ctth'  : '$c_{tth}$',
    'cgghh' : '$c_{gghh}$',
    'cggh'  : '$c_{ggh}$',
    'ctthh' : '$c_{tthh}$',
    ######
    'cdp'   : r'$c_{H,box}$',
    'cp'    : r'$C_{H}$',
    'ctp'   : r'$c_{tH}$',
    'ctG'   : r'$c_{tG}$',
    'cpg'   : r'$c_{HG}$',
}

# plotting params
linewidth=2

fig, ax = plt.subplots()
fig.set_size_inches(9, 5)

yval = 'qmu'

plot_negdeltlogL = 0 # remove the factor of 2

# 1D scan, -2deltaln(L)
one_sig_level = 1.
two_sig_level = 4.

if(plot_negdeltlogL):
    # 1D scan, -deltaln(L)
    one_sig_level = 0.5
    two_sig_level = 2.

label_dict = {
    "nobkg" : "nobkg",
    "WW" : "WW",
    "ZZ" : "WW+ZZ",
    "Zqq" : "WW+ZZ+Zqq",
    "base" : "base",
    "65pcworse" : r"$65\%$ worse res.",
    "C1_0":"C1 = 0",
    "C1_0p017":"C1 = 0.017",
    "FSR_studies_IDEA_BASE" : "Baseline",
    "FSR_studies_IDEA_nodndx_7labels" : "nodndx",
    "FSR_studies_IDEA_noTOF_7labels" : "noTOF"
}

inputs = args.inputs.split(',')
labels = args.labels.split(',')

colors = [
    (87/255., 151/255., 240/255.),
    (137/255., 195/255., 128/255.),
    (239/255., 145/255., 119/255.)
]

styles = [
    "solid",
    "dashed",
    "dashed",
]

# for each input
for input_i,input in enumerate(inputs):
    label = labels[input_i]
    color = colors[input_i]
    style = styles[input_i]

    if(label in label_dict):
        label = label_dict[label]

    data = json.load(open(input))
    df = pd.DataFrame(data)

    ### drop first point - it's the min not ordered
    df = df.drop(0)

    if(plot_negdeltlogL):
        ax.plot(df[args.poi], df[yval]/2., '-', ms=2, lw=linewidth, label=label)
    else:
        ax.plot(df[args.poi], df[yval], ms=2, lw=linewidth, label=label, color=color, linestyle = style)
        
    if(args.unblind_input): 
        ax.plot(df_obs[args.poi], df_obs[yval], '-', color='black', ms=2, lw=linewidth, label = "Observed")

    thry_pnts = 10000
    x_thry = np.linspace(args.xmin,args.xmax,thry_pnts) 
    y_thry = [one_sig_level] * thry_pnts
    
    if(plot_negdeltlogL): intersections_exp_1sig = get_intersections(df[args.poi], df[yval]/2., x_thry, y_thry) # x_data, y_data, x_theory, y_theory
        
    else: 
        intersections_exp_1sig = get_intersections(df[args.poi], df[yval], x_thry, y_thry) # x_data, y_data, x_theory, y_theory
        intersections_exp_2sig = get_intersections(df[args.poi], df[yval], x_thry, y_thry) # x_data, y_data, x_theory, y_theory
    
    # observed
    if(args.unblind_input): 
        intersections_obs_1sig = get_intersections(df_obs[args.poi], df_obs[yval], df_obs[args.poi], [one_sig_level] * len(df_obs[yval]))

    label_fontsize = 15

    ax.annotate(r'%s: 1$\sigma$: %s $\in [%.3f, %.3f]$' %(label, poi_names[args.poi], intersections_exp_1sig[0], intersections_exp_1sig[1]), 
                           (0.2, 0.90 - input_i*0.1), xycoords = 'axes fraction', fontsize = label_fontsize)

ax.set_xlabel(poi_names[args.poi], loc='right', size=15)

if(plot_negdeltlogL):
    ax.set_ylabel(r'-$\Delta\ln(L)$', loc='top', size=15)
else:
    ax.set_ylabel(r'-2$\Delta\ln(L)$', loc='top', size=15)

ax.set_ylim(0, 8)
xlim = ax.get_xlim()
if args.xmin:
    xlim = (args.xmin, xlim[1])
if args.xmax:
    xlim = (xlim[0], args.xmax)
ax.set_xlim(xlim)

ax.plot(xlim, [one_sig_level, one_sig_level], '--', color='black', lw=0.75)
ax.plot(xlim, [two_sig_level, two_sig_level], '--', color='black', lw=0.75)

# y range if entered
ylim = ax.get_ylim()
if args.ymin:
    ylim = (args.ymin, ylim[1])
if args.ymax:
    ylim = (ylim[0], args.ymax)

if(args.ymin or args.ymax):
    ax.set_ylim(ylim)

#plt.legend(loc = "upper right", bbox_to_anchor=(1, 0.5))
#plt.legend(loc=(1.04, 0))
plt.legend(bbox_to_anchor=(1.025, 1.0), loc='upper left')
plt.tight_layout()

print(f'[INFO] : Saving plots into {args.outputDir}')
if not os.path.exists(args.outputDir):
    print(f'[INFO] : creating folder {args.outputDir}')
    os.makedirs(args.outputDir)

oname = "%s/%s"%(args.outputDir, args.output.format(poi=args.poi))

print('... saving plot as', oname)
fig.savefig(oname, dpi = 150)

oname = oname.replace(".pdf", ".png")

print('... saving plot as', oname)
fig.savefig(oname, dpi = 150)
