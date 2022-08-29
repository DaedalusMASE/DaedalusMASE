"""
sub_heating_sources.parallel_cond

**Description**:
_____________________________________________________________________________________________________________________

Calculate parallel conductivity in S/m
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

Ne: electron density in cm^-3

B: Magnetic field vector in T

Te: Electron temperature in K

NO2: O2 density in cm^-3

NN2: N2 density in cm^-3

NO: O density in cm^-3


_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

sigma0: parallel conductivity in S/m
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""


import numpy as np
from daedalusmase_collision_frequencies.mod_utils import allocations as alloc
import matplotlib.pyplot as plt


def plot_pedersen_vin(time_sim,lat_sim,lon_sim,altmin_sim,altmax_sim,dalt_sim,savefig=True):
    
    alt_range=np.arange(altmin_sim,altmax_sim,dalt_sim)
    
    fig1c, ax1c = plt.subplots(figsize=(10, 7))
    plt.suptitle(r'Pedersen for different $\nu_{in}$ models',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))
#     ax1b.set_xscale('log')
    ax1c.plot(alloc.sigmaped_SN[0:-1],alt_range[0:-1],color='tab:blue', linewidth=2, label='vin [Shcunk_Nagy (2009)]')
    ax1c.plot(alloc.sigmaped_R[0:-1],alt_range[0:-1],color='tab:orange', linewidth=2, label='vin [Richmond (2016)]')
    ax1c.plot(alloc.sigmaped_SW[0:-1],alt_range[0:-1],color='tab:red', linewidth=2, label='vin [Shcunk_Walker (1973)]')
    ax1c.plot(alloc.sigmaped_B[0:-1],alt_range[0:-1],color='tab:green', linewidth=2, label='vin [Banks (1966)]')
    ax1c.plot(alloc.sigmaped_I[0:-1],alt_range[0:-1],color='gold', linewidth=2, label='vin [Ieda (2020)]')

    
    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
    ax1c.tick_params(axis='both', which='major', labelsize=14)
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax1c.set_xlabel(r"$\sigma$ (S/m)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/Pedersen_vin.jpg',dpi=300)
    plt.show()