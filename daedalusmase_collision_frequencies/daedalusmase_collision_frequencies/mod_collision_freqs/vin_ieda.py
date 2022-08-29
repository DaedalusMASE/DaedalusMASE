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

def vin_ieda(Ti,Tn,NO2,NO,NN2):


    a0_N2=1.76
    a0_O2=1.59
    a0_O=0.77

    mN2=28
    mO2=32
    mO=16
    mNO=30

    Tr=(Ti+Tn)/2

    def vin(a0,Nn,mn,mi):
        vtmp=25.879*10**(-16)*np.sqrt(a0/((mi*mn)/(mi+mn)))*Nn*(mn/(mi+mn))

        return vtmp


    vinNOp_N2=vin(a0_N2,NN2,mN2,mNO)
    vinNOp_O2=vin(a0_O2,NO2,mO2,mNO)
    vinNOP_O=vin(a0_O,NO,mO,mNO)

    vinO2p_N2=vin(a0_N2,NN2,mN2,mO2)
    vinO2p_O=vin(a0_O,NO,mO,mO2)


    vinOp_N2=vin(a0_N2,NN2,mN2,mO)
    vinOp_O2=vin(a0_O2,NO2,mO2,mO)

    vinOp_O=3.6834 * (10**(-11)) * np.sqrt(Tr)*((1-0.06482*np.log10(Tr))**2)

    vinO2p_O2=2.6173 * (10**(-11)) * np.sqrt(Tr)*((1-0.073511*np.log10(Tr))**2)

    vinNOp=vinNOp_N2+vinNOp_O2+vinNOP_O
    vinOp=vinOp_N2+vinOp_O2+vinOp_O
    vinO2p=vinO2p_N2+vinO2p_O2+vinO2p_O

    vin=(vinNOp+vinOp+vinO2p)/3

    return vin,vinNOp,vinO2p,vinOp,vinNOp_N2,vinNOp_O2,vinNOP_O,vinO2p_N2,vinO2p_O2,vinO2p_O,vinOp_N2,vinOp_O2,vinOp_O



