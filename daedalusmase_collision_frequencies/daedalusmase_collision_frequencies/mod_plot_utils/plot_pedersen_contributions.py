"""
sub_heating_sources.plot_pedersen_contributions

**Description**:
_____________________________________________________________________________________________________________________

Plot ion contributions to pedersen conductivity
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

"""


import numpy as np
from daedalusmase_collision_frequencies.mod_utils import allocations as alloc
import matplotlib.pyplot as plt


def plot_pedersen_contributions(time_sim,lat_sim,lon_sim,altmin_sim,altmax_sim,dalt_sim,savefig=True):
    
    alt_range=np.arange(altmin_sim,altmax_sim,dalt_sim)
    
    fig1c, ax1c = plt.subplots(figsize=(10, 7))
    plt.suptitle(r'Pedersen Conductivity [Banks (1966)]',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))
#     ax1b.set_xscale('log')
    ax1c.plot(alloc.sigmaped_B[0:-1],alt_range[0:-1],color='tab:blue', linewidth=2, label='$\sigma_P$')
    ax1c.plot(alloc.sigmaped_e_B[0:-1],alt_range[0:-1],color='tab:orange', linewidth=2, label='$e$ contribution')
    ax1c.plot(alloc.sigmaped_op_B[0:-1],alt_range[0:-1],color='tab:red', linewidth=2, label='$O^+$ contribution')
    ax1c.plot(alloc.sigmaped_o2p_B[0:-1],alt_range[0:-1],color='tab:green', linewidth=2, label='$O_2^+$ contribution')
    ax1c.plot(alloc.sigmaped_nop_B[0:-1],alt_range[0:-1],color='gold', linewidth=2, label='$NO^+$ contribution')       
    
    
    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
    ax1c.tick_params(axis='both', which='major', labelsize=14)
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax1c.set_xlabel(r"$\sigma$ (S/m)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/Pedersen_Banks.jpg',dpi=300)
    plt.show()

    fig1c, ax1c = plt.subplots(figsize=(10, 7))
    plt.suptitle(r'Pedersen Conductivity [Shcunk and Walker (1973)]',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))
#     ax1b.set_xscale('log')
    ax1c.plot(alloc.sigmaped_SW[0:-1],alt_range[0:-1],color='tab:blue', linewidth=2, label='$\sigma_P$')
    ax1c.plot(alloc.sigmaped_e_SW[0:-1],alt_range[0:-1],color='tab:orange', linewidth=2, label='$e$ contribution')
    ax1c.plot(alloc.sigmaped_op_SW[0:-1],alt_range[0:-1],color='tab:red', linewidth=2, label='$O^+$ contribution')
    ax1c.plot(alloc.sigmaped_o2p_SW[0:-1],alt_range[0:-1],color='tab:green', linewidth=2, label='$O_2^+$ contribution')
    ax1c.plot(alloc.sigmaped_nop_SW[0:-1],alt_range[0:-1],color='gold', linewidth=2, label='$NO^+$ contribution')       
    
    
    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
    ax1c.tick_params(axis='both', which='major', labelsize=14)
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax1c.set_xlabel(r"$\sigma$ (S/m)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/Pedersen_Schunk_Walker.jpg',dpi=300)
    plt.show()

    fig1c, ax1c = plt.subplots(figsize=(10, 7))
    plt.suptitle(r'Pedersen Conductivity [Shcunk and Nagy (2009)]',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))
#     ax1b.set_xscale('log')
    ax1c.plot(alloc.sigmaped_SN[0:-1],alt_range[0:-1],color='tab:blue', linewidth=2, label='$\sigma_P$')
    ax1c.plot(alloc.sigmaped_e_SN[0:-1],alt_range[0:-1],color='tab:orange', linewidth=2, label='$e$ contribution')
    ax1c.plot(alloc.sigmaped_op_SN[0:-1],alt_range[0:-1],color='tab:red', linewidth=2, label='$O^+$ contribution')
    ax1c.plot(alloc.sigmaped_o2p_SN[0:-1],alt_range[0:-1],color='tab:green', linewidth=2, label='$O_2^+$ contribution')
    ax1c.plot(alloc.sigmaped_nop_SN[0:-1],alt_range[0:-1],color='gold', linewidth=2, label='$NO^+$ contribution')       
    
    
    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
    ax1c.tick_params(axis='both', which='major', labelsize=14)
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax1c.set_xlabel(r"$\sigma$ (S/m)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/Pedersen_Schunk_Nagy.jpg',dpi=300)
    plt.show()


    fig1c, ax1c = plt.subplots(figsize=(10, 7))
    plt.suptitle(r'Pedersen Conductivity [Richmond (2016)]',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))
#     ax1b.set_xscale('log')
    ax1c.plot(alloc.sigmaped_R[0:-1],alt_range[0:-1],color='tab:blue', linewidth=2, label='$\sigma_P$')
    ax1c.plot(alloc.sigmaped_e_R[0:-1],alt_range[0:-1],color='tab:orange', linewidth=2, label='$e$ contribution')
    ax1c.plot(alloc.sigmaped_op_R[0:-1],alt_range[0:-1],color='tab:red', linewidth=2, label='$O^+$ contribution')
    ax1c.plot(alloc.sigmaped_o2p_R[0:-1],alt_range[0:-1],color='tab:green', linewidth=2, label='$O_2^+$ contribution')
    ax1c.plot(alloc.sigmaped_nop_R[0:-1],alt_range[0:-1],color='gold', linewidth=2, label='$NO^+$ contribution')       
    
    
    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
    ax1c.tick_params(axis='both', which='major', labelsize=14)
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax1c.set_xlabel(r"$\sigma$ (S/m)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")

    if savefig:
        plt.savefig('Figures/Pedersen_Richmond.jpg',dpi=300)
    plt.show()


    fig1c, ax1c = plt.subplots(figsize=(10, 7))
    plt.suptitle(r'Pedersen Conductivity [Ieda (2020)]',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))
#     ax1b.set_xscale('log')
    ax1c.plot(alloc.sigmaped_I[0:-1],alt_range[0:-1],color='tab:blue', linewidth=2, label='$\sigma_P$')
    ax1c.plot(alloc.sigmaped_e_I[0:-1],alt_range[0:-1],color='tab:orange', linewidth=2, label='$e$ contribution')
    ax1c.plot(alloc.sigmaped_op_I[0:-1],alt_range[0:-1],color='tab:red', linewidth=2, label='$O^+$ contribution')
    ax1c.plot(alloc.sigmaped_o2p_I[0:-1],alt_range[0:-1],color='tab:green', linewidth=2, label='$O_2^+$ contribution')
    ax1c.plot(alloc.sigmaped_nop_I[0:-1],alt_range[0:-1],color='gold', linewidth=2, label='$NO^+$ contribution')       
    
    
    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
    ax1c.tick_params(axis='both', which='major', labelsize=14)
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax1c.set_xlabel(r"$\sigma$ (S/m)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel("Altitude (km)", labelpad=15, fontsize=15, color="#333533")
    if savefig:
        plt.savefig('Figures/Pedersen_Ieda.jpg',dpi=300)
    plt.show()

           