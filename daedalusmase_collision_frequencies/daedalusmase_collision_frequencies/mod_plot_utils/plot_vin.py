"""
sub_heating_sources.plot_vin

**Description**:
_____________________________________________________________________________________________________________________

Plot ion-neutral collision frequencies based on different parameterisations
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

"""



import numpy as np
from daedalusmase_collision_frequencies.mod_utils import allocations as alloc
import matplotlib.pyplot as plt


def plot_vin(time_sim,lat_sim,lon_sim,altmin_sim,altmax_sim,dalt_sim,savefig=True):
    
    alt_range=np.arange(altmin_sim,altmax_sim,dalt_sim)
    fig1c, ax1c = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    plt.suptitle(r'Ion-Neutral Collision Frequencies',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))
#     ax1b.set_xscale('log')
    ax1c.plot(alloc.vin_SN[0:-1],alt_range[0:-1],color='tab:blue', linewidth=2, label='vin [Shcunk_Nagy (2009)]')
    ax1c.plot(alloc.vin_R[0:-1],alt_range[0:-1],color='tab:green', linewidth=2, label='vin [Richmond (2016)]')
    ax1c.plot(alloc.vin_SW[0:-1],alt_range[0:-1],color='tab:red', linewidth=2, label='vin [Shcunk_Walker (1973)]')
    ax1c.plot(alloc.vin_B[0:-1],alt_range[0:-1],color='tab:orange', linewidth=2, label='vin [Banks (1996)]')
    ax1c.plot(alloc.vin_I[0:-1],alt_range[0:-1],color='tab:purple', linewidth=2, label='vin [Ieda (2020)]')

    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
    ax1c.tick_params(axis='both', which='major', labelsize=14)
    ax1c.set_xscale('log')
    ax1c.set_xlabel(r"$\nu_{in} (s^{-1}$)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/vin.jpg',dpi=300)
    plt.show()