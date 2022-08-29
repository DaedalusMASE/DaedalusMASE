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
from daedalusmase_derived_products.mod_tiegcm_utils import allocations as alloc
import matplotlib.pyplot as plt
import datetime

def plot_frequencies(timer,lat,lon,savefig=True):
    
    time_begin=datetime.datetime(2015,3,15,0,0,0)
    time_plot=time_begin+datetime.timedelta(minutes=alloc.maptime[timer])
    
     
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    plt.suptitle("Frequencies",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
    ax.set_xscale('log')
    ax.plot(alloc.omega_e_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='$e$ gyrofrequency')
    ax.plot(alloc.omega_op_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='$O^+$ gyrofrequency')
    ax.plot(alloc.omega_o2p_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='$O_2^+$ gyrofrequency')
    ax.plot(alloc.omega_nop_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='$NO^+$ gyrofrequency')
    ax.plot(alloc.omega_np_1D[0:-1],alloc.zg_1D[0:-1],color='tab:green', linewidth=2, label='$N^+$ gyrofrequency')
    ax.plot(alloc.ve_i_1D[0:-1],alloc.zg_1D[0:-1],color='crimson', linewidth=2, label='Electron-Ion Collision Frequency')
    ax.plot(alloc.vi_i_1D[0:-1],alloc.zg_1D[0:-1],color='firebrick', linewidth=2, label='Ion-Ion Collision Frequency')
    ax.plot(alloc.ven_1D[0:-1],alloc.zg_1D[0:-1],color='blueviolet', linewidth=2, label='Electron-Neutral Collision Frequency')
    ax.plot(alloc.vin_1D[0:-1],alloc.zg_1D[0:-1],color='fuchsia', linewidth=2, label='Ion-Neutral Collision Frequency')

    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$Hz$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/frequencies_alt.jpg',dpi=300)
    plt.show()  
    #####################################################################