"""
sub_Heating_Sources.op_o_temps

**Description**:
_____________________________________________________________________________________________________________________

Calculate dependence of different \(O^+-O\) collision frequency formulas on temperatures
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`Tmin`: minimum temperature

`Tmax`: maximum temperature

`dT`: temperature resolution
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

Plot of \(O^+-O\) collision frequencies vs temperature
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Dalgarno, A., Henry, R., and Stewart, A. (1964). The photoionization of atomic oxygen. Planetary and
Space Science 12, 235–246

Banks, P. (1966). Collision frequencies and energy transfer electrons. Planetary and Space Science 14,
1085–1103

Stubbe, P. (1968). Frictional forces and collision frequencies between moving ion and neutral gases.
Journal of Atmospheric and Terrestrial Physics 30, 1965–1985

Schunk, R. and Walker, J. (1973). Theoretical ion densities in the lower ionosphere. Planetary and Space
Science 21, 1875–1896

Salah, J. E. (1993). Interim standard for the ion-neutral atomic oxygen collision frequency. Geophysical
research letters 20, 1543–1546

Pesnell, W. D., Omidvar, K., and Hoegy, W. R. (1993). Momentum transfer collision frequency of o+-o.
Geophysical Research Letters 20, 1343–1346

Hickman, A., Medikeri-Naphade, M., Chapin, C., and Huestis, D. (1997). Fine structure effects in the o+-o
collision frequency. Geophysical research letters 24, 119–122

Schunk, R. and Nagy, A. (2009). Ionospheres: physics, plasma physics, and chemistry (Cambridge
university press)

Richmond, A. D. (2017). Ionospheric electrodynamics. In Handbook of atmospheric electrodynamics,
volume II (CRC Press). 249–290

Ieda, A. (2020). Ion-neutral collision frequencies for calculating ionospheric conductivity. Journal of
Geophysical Research: Space Physics 125, e2019JA027128
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
from daedalusmase_collision_frequencies.mod_utils import allocations as alloc
import matplotlib.pyplot as plt

def op_o_temps(Tmin,Tmax,dT):
    Tr=np.arange(Tmin,Tmax,dT)
    for i in range(0,len(Tr)):
        q_dalgarno=4.3*10**(-11)*Tr[i]**(0.41)
        q_banks=3.5*10**(-11)*np.sqrt(Tr[i])*((1-np.log10(Tr[i]))**2)
        q_stubbe=7.2*10**(-11)*(Tr[i]**0.37)
        
        q_sw=3.69*10**(-11)*np.sqrt(Tr[i])*((1-np.log10(Tr[i]))**2)
        q_salah=4*10**(-11)*np.sqrt(Tr[i])
        q_pesnell=5.9*10**(-11)*np.sqrt(Tr[i])*((1-0.096*np.log10(Tr[i]))**2)
        q_hickmann=5.92*10**(-11)*(Tr[i]**(0.393))*(1+(96.6/Tr[i])**2)
        q_shunk_nagy=3.67 * (10**(-11)) * np.sqrt(Tr[i])*((1-0.064*np.log10(Tr[i]))**2)
        q_richmond=6.7 * (10**(-11)) * np.sqrt(Tr[i])*((0.96-0.135*np.log10(Tr[i]))**2)
        q_ieda=3.6834 * (10**(-11)) * np.sqrt(Tr[i])*((1-0.06482*np.log10(Tr[i]))**2)
        q_baily_belan=4.45*10**(-11)*np.sqrt(Tr[i])*((1.04-0.067*np.log10(Tr[i]))**2)

        alloc.Tr_temps.append(Tr[i])
        alloc.q_dalgarno_temps.append(q_dalgarno)
        alloc.q_banks_temps.append(q_banks)
        alloc.q_stubbe_temps.append(q_stubbe)
        alloc.q_sw_temps.append(q_sw)
        alloc.q_salah_temps.append(q_salah)
        alloc.q_pesnell_temps.append(q_pesnell)
        alloc.q_hickmann_temps.append(q_hickmann)
        alloc.q_shunk_nagy_temps.append(q_shunk_nagy)
        alloc.q_richmond_temps.append(q_richmond)
        alloc.q_ieda_temps.append(q_ieda)
        alloc.q_baily_belan_temps.append(q_baily_belan)

    fig1c, ax1c = plt.subplots(figsize=(10, 7))
#     plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    ax1c.set_title(r'$O_+-O$ Collision Frequencies',fontsize=15)
#     ax1b.set_xscale('log')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_dalgarno_temps[0:-1],color='tab:blue', linewidth=2, label='Dalgarno_1964')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_banks_temps[0:-1],color='tab:orange', linewidth=2, label='Banks_1966')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_stubbe_temps[0:-1],color='tab:red', linewidth=2, label='Stubbe_1968')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_sw_temps[0:-1],color='tab:green', linewidth=2, label='Shcunk & Walker_1973')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_salah_temps[0:-1],color='tab:purple', linewidth=2, label='Salah_1993')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_pesnell_temps[0:-1],color='tab:pink', linewidth=2, label='Pesnell_1993')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_hickmann_temps[0:-1],color='tab:olive', linewidth=2, label='Hickman_1997')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_shunk_nagy_temps[0:-1],color='tab:gray', linewidth=2, label='Schunk $ Nagy_2009')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_richmond_temps[0:-1],color='tab:cyan', linewidth=2, label='Richmond_2006')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_ieda_temps[0:-1],color='gold', linewidth=2, label='Ieda_2020')
    ax1c.plot(alloc.Tr_temps[0:-1],alloc.q_baily_belan_temps[0:-1],color='pink', linewidth=2, label='Baily & Balan_1996')

    ax1c.grid(True, color="#93a1a1", alpha=0.3)
    ax1c.minorticks_on()
    plt.legend(loc='best',fontsize=14)
#     plt.ylim(100,400)
    ax1c.set_xlabel("Tr (K)", labelpad=15, fontsize=15, color="#333533")
    ax1c.set_ylabel(r"$\nu_{O+-O}/N_O  (cm^{-3} s^{-1}$)", labelpad=15, fontsize=15, color="#333533")

    ax1c.tick_params(axis='both', which='major', labelsize=14)
    plt.show()