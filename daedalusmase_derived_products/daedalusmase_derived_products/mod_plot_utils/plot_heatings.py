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

def plot_heatings(timer,lat,lon,savefig=True):
    
    time_begin=datetime.datetime(2015,3,15,0,0,0)
    time_plot=time_begin+datetime.timedelta(minutes=alloc.maptime[timer])
    
     
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    plt.suptitle("Heating Rates",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
#     ax1b.set_xscale('log')
    ax.plot(alloc.joule_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='Joule Heating')
    ax.plot(alloc.wind_heating_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='Wind Heating')
    ax.plot(alloc.convection_heating_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='Convection Heating')
    ax.plot(alloc.qDTi_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='Ion-Neutral Heating Rate')
    ax.plot(alloc.L_en_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:green', linewidth=2, label='Electron-Neutral Heating Rate (Schunk)')
    ax.plot(alloc.L_en_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:olive', linewidth=2, label='Electron-Neutral Heating Rate (Rees)')
    ax.plot(alloc.qFi_i_1D[0:-1],alloc.zg_1D[0:-1],color='crimson', linewidth=2, label='Ion-Ion Frictional Heating')
    ax.plot(alloc.qFe_i_1D[0:-1],alloc.zg_1D[0:-1],color='firebrick', linewidth=2, label='Electron-Ion Frictional Heating')
    ax.plot(alloc.qFi_n_1D[0:-1],alloc.zg_1D[0:-1],color='blueviolet', linewidth=2, label='Ion-Neutral Frictional Heating')
    ax.plot(alloc.ohmic_1D[0:-1],alloc.zg_1D[0:-1],color='fuchsia', linewidth=2, label='Ohmic Heating')
    ax.plot(alloc.frictional_1D[0:-1],alloc.zg_1D[0:-1],color='peru', linewidth=2, label='Frictional Heating')
    ax.plot(alloc.mech_power_1D[0:-1],alloc.zg_1D[0:-1],color='peru', linewidth=2, label='Mechanical Power')
    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$mW/m^{3}$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/heating_rates_alt.jpg',dpi=300)
    plt.show()    
################################################################################
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

    plt.suptitle("$q\Delta_{in}$",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
#     ax1b.set_xscale('log')
    ax.plot(alloc.qDTi_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='Ion-Neutral Heating Rate')
    ax.plot(alloc.qDTop_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='$O^+$-Neutral Heating Rate')
    ax.plot(alloc.qDTo2p_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='$O_2^+$-Neutral Heating Rate')
    ax.plot(alloc.qDTnop_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='$NO^+$-Neutral Heating Rate')
    ax.plot(alloc.qDTnp_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:green', linewidth=2, label='$N^+$-Neutral Heating Rate')
    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$mW/m^{3}$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/qDtin.jpg',dpi=300)
    plt.show()   
################################################################################
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

    plt.suptitle("$q\Delta_{en}$",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
#     ax1b.set_xscale('log')
    ax.plot(alloc.L_en_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='Electron-Neutral Heating Rate [Schunk and Nugy]')
    ax.plot(alloc.L_eO2_elast_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='Electron-$O_2$ Heating Rate [Schunk and Nugy]')
    ax.plot(alloc.L_eO_elast_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='Electron-$O$ Heating Rate [Schunk and Nugy]')
    ax.plot(alloc.L_eN2_elast_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='Electron-$N_2$ Heating Rate [Schunk and Nugy]')
    ax.plot(alloc.L_eHe_elast_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:green', linewidth=2, label='Electron-$He$ Heating Rate [Schunk and Nugy]')
    ax.plot(alloc.L_en_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='Electron-Neutral Heating Rate [Rees]',linestyle='--')
    ax.plot(alloc.L_eO2_elast_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='Electron-$O_2$ Heating Rate [Rees]',linestyle='--')
    ax.plot(alloc.L_eO_elast_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='Electron-$O$ Heating Rate [Rees]',linestyle='--')
    ax.plot(alloc.L_eN2_elast_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='Electron-$N_2$ Heating Rate [Rees]',linestyle='--')
    ax.plot(alloc.L_eHe_elast_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:green', linewidth=2, label='Electron-$He$ Heating Rate [Rees]',linestyle='--')

    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$mW/m^{3}$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/qDten.jpg',dpi=300)
    plt.show() 
################################################################################
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

    plt.suptitle("$q\Delta_{ei}$",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
#     ax1b.set_xscale('log')
    ax.plot(alloc.qDTe_i_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='Electron-Ion Heating Rate')
    ax.plot(alloc.qDTe_op_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='Electron-$O^+$ Heating Rate')
    ax.plot(alloc.qDTe_o2p_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='Electron-$O_2^+$ Heating Rate')
    ax.plot(alloc.qDTe_nop_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='Electron-$NO^+$ Heating Rate')
    ax.plot(alloc.qDTe_np_1D[0:-1],alloc.zg_1D[0:-1],color='tab:green', linewidth=2, label='Electron-$N^+$ Heating Rate')
    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$mW/m^{3}$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/qDtei.jpg',dpi=300)
    plt.show() 
###############################################################################################
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    plt.suptitle("Ion-Neutral Frictional Heating Rates",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
#     ax1b.set_xscale('log')
    ax.plot(alloc.qFi_n_1D[0:-1],alloc.zg_1D[0:-1],color='peru', linewidth=2, label='Ion-Neutral Frictional Heating')
    ax.plot(alloc.qFop_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='$O^+$-Neutral Frictional Heating')
    ax.plot(alloc.qFo2p_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='$O_2^+$-Neutral Frictional Heating')
    ax.plot(alloc.qFnop_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='$NO^+$-Neutral Frictional Heating')
    ax.plot(alloc.qFnp_n_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='$N^+$-Neutral Frictional Heating')

    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$mW/m^{3}$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/qFin.jpg',dpi=300)
    plt.show()  
###############################################################################################
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    plt.suptitle("Ion-Electron Frictional Heating Rates",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
#     ax1b.set_xscale('log')
    ax.plot(alloc.qFe_i_1D[0:-1],alloc.zg_1D[0:-1],color='peru', linewidth=2, label='Ion-Electron Frictional Heating')
    ax.plot(alloc.qFop_e_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='$O^+$-Electron Frictional Heating')
    ax.plot(alloc.qFo2p_e_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='$O_2^+$-Electron Frictional Heating')
    ax.plot(alloc.qFnop_e_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='$NO^+$-Electron Frictional Heating')
    ax.plot(alloc.qFnp_e_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='$N^+$-Electron Frictional Heating')

    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$mW/m^{3}$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/qFie.jpg',dpi=300)
    plt.show()  
###############################################################################################
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    plt.suptitle("Ion-Ion Frictional Heating Rates",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
#     ax1b.set_xscale('log')
    ax.plot(alloc.qFi_i_1D[0:-1],alloc.zg_1D[0:-1],color='peru', linewidth=2, label='Ion-Ion Frictional Heating')
    ax.plot(alloc.qFop_o2p_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='$O^+$-$O_2^+$ Frictional Heating')
    ax.plot(alloc.qFop_nop_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='$O^+$-$NO^+$ Frictional Heating')
    ax.plot(alloc.qFop_np_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='$O^+$-$N^+$ Frictional Heating')
    ax.plot(alloc.qFo2p_nop_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='$O_2^+$-$NO^+$ Frictional Heating')
    ax.plot(alloc.qFo2p_np_1D[0:-1],alloc.zg_1D[0:-1],color='firebrick', linewidth=2, label='$O_2^+$-$N^+$ Frictional Heating')
    ax.plot(alloc.qFnop_np_1D[0:-1],alloc.zg_1D[0:-1],color='blueviolet', linewidth=2, label='$NO^+$-$N^+$ Frictional Heating')
    
    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$mW/m^{3}$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/qFii.jpg',dpi=300)
    plt.show() 
###############################################################################################
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    plt.suptitle("Electron Cooling Rates",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
#     ax1b.set_xscale('log')
    ax.plot(alloc.Le_N2_rot_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='$N_2$ rotational excitation [Schunk and Nugy]')
    ax.plot(alloc.Le_O2_rot_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='$O_2$ rotational excitation [Schunk and Nugy]')
    ax.plot(alloc.Le_N2_vib_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='$N_2$ vibrational excitation [Schunk and Nugy]')
    ax.plot(alloc.Le_O2_vib_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='$O_2$ vibrational excitation [Schunk and Nugy]')
    ax.plot(alloc.Le_O_fine_schunk_1D[0:-1],alloc.zg_1D[0:-1],color='tab:green', linewidth=2, label='$O$ fine structure [Schunk and Nugy]')
    ax.plot(alloc.Le_N2_rot_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:red', linewidth=2, label='$N_2$ rotational excitation [Rees]',linestyle='--')
    ax.plot(alloc.Le_O2_rot_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='$O_2$ rotational excitation [Rees]',linestyle='--')
    ax.plot(alloc.Le_N2_vib_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='$N_2$ vibrational excitation [Rees]',linestyle='--')
    ax.plot(alloc.Le_O2_vib_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='$O_2$ vibrational excitation [Rees]',linestyle='--')
    ax.plot(alloc.Le_O_fine_rees_1D[0:-1],alloc.zg_1D[0:-1],color='tab:green', linewidth=2, label='$O$ fine structure [Rees]',linestyle='--')

    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$mW/m^{3}$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/e_cooling.jpg',dpi=300)
    plt.show()    
###############################################################################################
    fig, ax = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    plt.suptitle("Joule Heating Rates",fontsize=15)
    ax.set_title('%s Lattitude=%s Longitude=%s' % (time_plot.strftime("%d %b %Y %H:%M:%S"),alloc.lat_1D[0],alloc.lon_1D[0]))
#     ax1b.set_xscale('log')
    ax.plot(alloc.joule_1D[0:-1],alloc.zg_1D[0:-1],color='peru', linewidth=2, label='Joule Heating')
    ax.plot(alloc.joule_op_1D[0:-1],alloc.zg_1D[0:-1],color='tab:blue', linewidth=2, label='$O^+$ Joule Heating')
    ax.plot(alloc.joule_o2p_1D[0:-1],alloc.zg_1D[0:-1],color='tab:orange', linewidth=2, label='$O_2^+$ Joule Heating')
    ax.plot(alloc.joule_nop_1D[0:-1],alloc.zg_1D[0:-1],color='tab:pink', linewidth=2, label='$NO^+$ Joule Heating')

    ax.grid(True, color="#93a1a1", alpha=0.3)
    ax.minorticks_on()
    plt.legend(loc='best')
#     plt.ylim(100,400)
    ax.set_xlabel("$mW/m^{3}$", labelpad=15, fontsize=15, color="#333533")
    ax.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/joule.jpg',dpi=300)
    plt.show()  
###############################################################################################