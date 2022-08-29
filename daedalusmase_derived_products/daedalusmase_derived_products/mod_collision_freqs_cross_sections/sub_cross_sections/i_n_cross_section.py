"""
**sub_heating_sources.i_n_cross_section**

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-neutral collision frequencies


$$\\sigma_{in} = \\frac{\\nu_{in}}{N_n \\sqrt{\\frac{2 k_B T_i}{m_i}}}$$
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`vin`: ion-neutral collision frequency

`vOp`: \(O^+\) collision frequency

`vO2p`: \(O_2^+\) collision frequency

`vNOp`: \(NO^+\) collision frequency

`NO2`: \(O_2\) density in \(cm^{-3}\)

`NN2`: \(N_2\) density in \(cm^{-3}\)

`NO`: \(O\) density in \(cm^{-3}\)

`Ti`: Ion temperature in K

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________


`cross`: ion-neutral collision cross section

`cross_op`:  \(O^+\)collision cross section

`cross_o2p`: \(O_2^+\) collision cross section

`cross_nop`: \(NO^+\) collision cross section
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Banks, P. M. and Kockarts, G. (1973). Aeronomy (Academic Press, ISBN: 9781483260068
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

from cmath import sqrt
import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def i_n_cross_section(vin,vOp,vO2p,vNOp,NO2,NN2,NO,Ti):

    N_neutral=(NO2+NN2+NO)*10**6
    MNO=(const.mNO)/(const.NA*1000)
    MO=(const.mO)/(const.NA*1000)
    MO2=(const.mO2)/(const.NA*1000)

    M_ion=MO+MO2+MNO
    
    cross=(vin/N_neutral)/(np.sqrt((2*const.boltzmann*Ti)/M_ion))
    
    cross_op=(vOp/N_neutral)/(np.sqrt((2*const.boltzmann*Ti)/MO))
    
    cross_o2p=(vO2p/N_neutral)/(np.sqrt((2*const.boltzmann*Ti)/MO2))
    
    cross_nop=(vNOp/N_neutral)/(np.sqrt((2*const.boltzmann*Ti)/MNO))

    return cross,cross_op,cross_o2p,cross_nop