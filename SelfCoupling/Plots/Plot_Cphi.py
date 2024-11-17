"""
https://cds.cern.ch/record/2835483/files/CERN-THESIS-2022-143.pdf?version=1
Equations 3.6-3.7 were used to rescale the XS , where it appears the "C" coefficient values are taken from Eq. 16. 
https://link.springer.com/article/10.1007/JHEP02(2018)178
"""

import matplotlib
from matplotlib import pyplot as plt
import mplhep as hep 
plt.style.use(hep.style.ATLAS)

matplotlib.use('Agg')

def Compute_XS(Cphi, computeDelta=False):

    updated_XS = (1 + 0.017 * ((1 - 0.47*Cphi) - 1)) / (1 + 0.00154 * ((1 - 0.47*Cphi) - 1)**2)
    if(computeDelta): 
        updated_XS = abs(1 - updated_XS)*100.
    return updated_XS

xmin, xmax = -1, 1

Cphi_vals = [i/10. for i in range(-10,10)]

for computeDelta in [0,1]:
    
    if(computeDelta): deltaExt = "_delta"
    else: deltaExt = ""
    
    XS_scaled_vals = [Compute_XS(Cphi_val, computeDelta) for Cphi_val in Cphi_vals]
    fig, ax = plt.subplots(figsize=(6, 4), dpi = 200)
    plt.plot(Cphi_vals, XS_scaled_vals, label = r"$\frac{\sigma_{Updated}}{\sigma_{Initial}}$")
    ax.set_xlim(xmin, xmax)
    ax.set_xlabel(r"$C_{\phi}$")

    ylabel = r"$\frac{\sigma_{Updated}}{\sigma_{Initial}}$"
    if(computeDelta):
        ylabel = r"Change in $\sigma$ [%]"

    ax.set_ylabel(ylabel)

    plt.legend()
    
    ax.grid(which='major', linestyle=':', linewidth='0.5', color='gray')
    
    fig.tight_layout()
    plt.savefig(f"plots/Cphi_vals{deltaExt}.png")
    plt.savefig(f"plots/Cphi_vals{deltaExt}.pdf")
    plt.close()