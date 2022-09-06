"""
sub_heating_sources.plot_densities

**Description**:
_____________________________________________________________________________________________________________________

Plot vertical profiles of neutral and ion densities
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

"""


import numpy as np
from daedalusmase_collision_frequencies.mod_utils import allocations as alloc
import matplotlib.pyplot as plt


def plot_densities(time_sim,lat_sim,lon_sim,altmin_sim,altmax_sim,dalt_sim,savefig=True):
    
    alt_range=np.arange(altmin_sim,altmax_sim,dalt_sim)
    
    fig1c, ax1c = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    plt.suptitle(r'Densities',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))

    ax1c.plot(alloc.ne_den[0:-1],alt_range[0:-1],color='tab:blue', linewidth=2, label='ne_den')
    ax1c.plot(alloc.Op_den[0:-1],alt_range[0:-1],color='tab:orange', linewidth=2, label='Op_den')
    ax1c.plot(alloc.O2p_den[0:-1],alt_range[0:-1],color='tab:red', linewidth=2, label='O2p_den')
    ax1c.plot(alloc.NOp_den[0:-1],alt_range[0:-1],color='tab:green', linewidth=2, label='NOp_den')
    ax1c.plot(alloc.Npp_den[0:-1],alt_range[0:-1],color='tab:purple', linewidth=2, label='Npp_den')
    ax1c.plot(alloc.O_den[0:-1],alt_range[0:-1],color='tab:pink', linewidth=2, label='O_den')
    ax1c.plot(alloc.O2_den[0:-1],alt_range[0:-1],color='tab:olive', linewidth=2, label='O2_den')
    ax1c.plot(alloc.N2_den[0:-1],alt_range[0:-1],color='tab:gray', linewidth=2, label='N2_den')
    
    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.ylim(100,299)
    plt.legend(loc='best',fontsize=14)
    ax1c.set_xscale('log')
    ax1c.set_xlabel(r"Density $(m^{-3}$)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/Densities.jpg',dpi=300)
    plt.show()