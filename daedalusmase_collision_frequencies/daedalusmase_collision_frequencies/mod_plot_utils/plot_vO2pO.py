"""
sub_heating_sources.plot_vO2pO

**Description**:
_____________________________________________________________________________________________________________________

Plot \(O_2^+-O) collision frequencies
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

"""



import numpy as np
from daedalusmase_collision_frequencies.mod_utils import allocations as alloc
import matplotlib.pyplot as plt


def plot_vO2pO(time_sim,lat_sim,lon_sim,altmin_sim,altmax_sim,dalt_sim,savefig=True):
    
    alt_range=np.arange(altmin_sim,altmax_sim,dalt_sim)
    fig1c, ax1c = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    plt.suptitle(r'$O_2^+-O$ Collision Frequencies',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))
    ax1c.plot(alloc.vO2p_SN[0:-1],alt_range[0:-1],color='tab:blue', linewidth=2, label='[Shcunk_Nagy (2009)]')
    ax1c.plot(alloc.vO2p_R[0:-1],alt_range[0:-1],color='tab:green', linewidth=2, label='[Richmond (2016)]')
    ax1c.plot(alloc.vO2p_SW[0:-1],alt_range[0:-1],color='tab:red', linewidth=2, label='[Shcunk_Walker (1973)]')
    ax1c.plot(alloc.vO2p_B[0:-1],alt_range[0:-1],color='tab:orange', linewidth=2, label='[Banks (1966)]')
    ax1c.plot(alloc.vO2p_I[0:-1],alt_range[0:-1],color='tab:purple', linewidth=2, label='[Ieda (2020)]')


    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
    ax1c.tick_params(axis='both', which='major', labelsize=14)
    ax1c.set_xscale('log')
    ax1c.set_xlabel(r"$\nu_{O_2+-O} ( s^{-1}$)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/O2p_O_alt.jpg',dpi=300)
    plt.show()

    plt.show()