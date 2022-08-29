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


def plot_oplus_freq_temperature(time_sim,lat_sim,lon_sim,savefig=True):
    
    fig1c, ax1c = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    plt.suptitle(r'$O_+-O$ Collision Frequencies',fontsize=15)
    ax1c.set_title('%s Lattitude=%s Longitude=%s' % (time_sim.strftime("%d %b %Y %H:%M:%S"),lat_sim,lon_sim))
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_dalgarno_iri[0:-1],color='tab:blue', linewidth=2, label='Dalgarno_1964')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_banks_iri[0:-1],color='tab:orange', linewidth=2, label='Banks_1966')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_stubbe_iri[0:-1],color='tab:red', linewidth=2, label='Stubbe_1968')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_sw_iri[0:-1],color='tab:green', linewidth=2, label='Shcunk & Walker_1973')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_salah_iri[0:-1],color='tab:purple', linewidth=2, label='Salah_1993')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_pesnell_iri[0:-1],color='tab:pink', linewidth=2, label='Pesnell_1993')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_hickmann_iri[0:-1],color='tab:olive', linewidth=2, label='Hickman_1997')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_shunk_nagy_iri[0:-1],color='tab:gray', linewidth=2, label='Schunk $ Nagy_2009')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_richmond_iri[0:-1],color='tab:cyan', linewidth=2, label='Richmond_2006')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_ieda_iri[0:-1],color='gold', linewidth=2, label='Ieda_2020')
    ax1c.plot(alloc.Tr_iri[0:-1],alloc.q_baily_belan_iri[0:-1],color='pink', linewidth=2, label='Baily & Balan_1996')
    
    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
    ax1c.tick_params(axis='both', which='major', labelsize=14)
    ax1c.set_xlabel("Tr (K)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel(r"$\nu_{O+-O}/N_O  (cm^{-3} s^{-1}$)", labelpad=15, fontsize=15, color="#333533")

    if savefig:
        plt.savefig('Figures/Op_O_per_temperature.jpg',dpi=300)

    plt.show()
  