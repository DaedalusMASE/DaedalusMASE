"""
**sub_heating_sources.i_n_collision_freqs**

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-neutral collision frequencies
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`B_enu`: mangetic field vector in T in ENU

`Ti`: Ion temperature in K

`Tn`: Neutral temperature in K

`NO2`: \(O_2\) density in \(cm^{-3}\)

`NO` : \(O\) density in \(cm^{-3}\)

`NN2` : \(N_2\) density in \(cm^{-3}\)

`helium_f` : \(He\) density in \(cm^{-3}\)

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________


`vin`: ion-neutral collision frequency

`vop_o`: \(O^+-O\) collision frequency

`vop_o2`: \(O^+-O_2\) collision frequency

`vop_n2`: \(O^+-N_2\) collision frequency

`vop_he`: \(O^+-He\) collision frequency

`vo2p_o`: \(O_2^+-O\) collision frequency

`vo2p_o2`: \(O_2^+-O_2\) collision frequency

`vo2p_n2`: \(O_2^+-N_2\) collision frequency

`vo2p_he`: \(O_2^+-He\) collision frequency

`vnop_o`: \(NO^+-O\) collision frequency

`vnop_o2`: \(NO^+-O_2\) collision frequency

`vnop_n2`: \(NO^+-N_2\) collision frequency

`vnop_he`: \(NO^+-He\) collision frequency

`vnp_o`: \(N^+-O\) collision frequency

`vnp_o2`: \(N^+-O_2\) collision frequency

`vnp_n2`: \(N^+-N_2\) collision frequency

`vnp_he`: \(N^+-He\) collision frequency

`vOp`: \(O^+-neutral\) collision frequency

`vO2p`: \(O_2^+-neutral\) collision frequency

`vNOp`: \(NO^+-neutral\) collision frequency

`vNp`: \(N^+-neutral\) collision frequency

_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Schunk, R. and Nagy, A. (2009). Ionospheres: physics, plasma physics, and chemistry (Cambridge
university press)
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
from daedalusmase_collision_frequencies.mod_utils import const

def vin_richmond(Ti,Tn,NO2,NO,NN2):
    Ri=(Ti+Tn)/1000

    vinNOp=(4.35*(NN2+NO2)*(Ri**(-0.11))+1.9*NO*(Ri**(-0.19)))*10**(-16)
    vinO2p=(4.3*NN2+5.2*NO2+1.8*NO*(Ri**(-0.19)))*10**(-16)
    vinOp=(5.4*NN2*(Ri**(-0.2))+7*NO2*(Ri**(0.05))+6.7*NO*(Ri**(0.5))*(0.96-0.135**np.log10(Ri))*(0.96-0.135**np.log10(Ri)))*10**(-16)

    vinNOp_N2=(4.35*NN2)*(Ri**(-0.11))*10**(-16)
    vinNOp_O2=(4.35*NO2)*(Ri**(-0.11))*10**(-16)
    vinNOP_O=1.9*NO*(Ri**(-0.19))*10**(-16)

    vinO2p_N2=4.3*NN2*10**(-16)
    vinO2p_O2=5.2*NO2*10**(-16)
    vinO2p_O=1.8*NO*(Ri**(-0.19))*10**(-16)

    vinOp_N2=5.4*NN2*(Ri**(-0.2))*10**(-16)
    vinOp_O2=7*NO2*(Ri**(0.05))*10**(-16)
    vinOp_O=6.7*NO*(Ri**(0.5))*(0.96-0.135**np.log10(Ri))*(0.96-0.135**np.log10(Ri))*10**(-16)

    vin=(vinNOp+vinOp+vinO2p)/3

    return vin,vinNOp,vinO2p,vinOp,vinNOp_N2,vinNOp_O2,vinNOP_O,vinO2p_N2,vinO2p_O2,vinO2p_O,vinOp_N2,vinOp_O2,vinOp_O

    

