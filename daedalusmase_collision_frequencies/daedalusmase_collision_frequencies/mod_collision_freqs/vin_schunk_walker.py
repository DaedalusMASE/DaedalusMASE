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

Schunk, R. and Walker, J. (1973). Theoretical ion densities in the lower ionosphere. Planetary and Space
Science 21, 1875–1896
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
from daedalusmase_collision_frequencies.mod_utils import const

def vin_schunk_walker(Ti,Tn,NO2,NO,NN2):
    Tr=(Ti+Tn)/2

    vinNOp_N2=(4.34*NN2)*10**(-10)
    vinNOp_O2=(4.28*NO2)*10**(-10)
    vinNOP_O=(2.44*NO)*10**(-10)

    vinO2p_N2=4.13*NN2*10**(-10)
    if Tr>800:
        vinO2p_O2=2.4*10**(-13)*NO2*(Tr**(0.5))*(10.4-0.76*np.log10(Tr))*(10.4-0.76*np.log10(Tr))
    elif Tr<800:
        vinO2p_O2=4.08*10**(-10)*NO2
    
    vinO2p_O=2.31*NO*10**(-10)

    vinOp_N2=6.82*NN2*10**(-10)
    vinOp_O2=6.66*NO2*10**(-10)
    vinOp_O=3.42*10**(-11)*NO*(Tr**(0.5))*(1.08-0.139*np.log10(Tr)+4.51*10**(-3)*np.log10(Tr)*np.log10(Tr))

    vinNOp=vinNOp_N2+vinNOp_O2+vinNOP_O
    vinOp=vinOp_N2+vinOp_O2+vinOp_O
    vinO2p=vinO2p_N2+vinO2p_O2+vinO2p_O

    vin=(vinNOp+vinOp+vinO2p)/3

    return vin,vinNOp,vinO2p,vinOp,vinNOp_N2,vinNOp_O2,vinNOP_O,vinO2p_N2,vinO2p_O2,vinO2p_O,vinOp_N2,vinOp_O2,vinOp_O



