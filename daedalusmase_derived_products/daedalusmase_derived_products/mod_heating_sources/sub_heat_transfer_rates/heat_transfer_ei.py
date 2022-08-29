"""
sub_Heating_Sources.heat_transfer_ei

**Description**:
_____________________________________________________________________________________________________________________

Calculate heating rate due to electron-ion coulomb collisions in W/m^3
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

Necm: electron density in cm^-3

ve_op: electron-O+ collision frequency

ve_o2p: electron-O2+ collision frequency

ve_nop: electron-NO+ collision frequency

ve_np: electron-N+ collision frequency

Te: electron temperature in K

Ti: ion temperature in K

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

qDTe_if: heating rate due to electron-ion coulomb collisions in W/m^3

qDTe_opf: heating rate due to electron-O+ coulomb collisions in W/m^3
 
qDTe_o2pf: heating rate due to electron-O2+ coulomb collisions in W/m^3

qDTe_nopf: heating rate due to electron-NO+ coulomb collisions in W/m^3

qDTe_npf: heating rate due to electron-N+ coulomb collisions in W/m^3


_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**: 
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""
import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def heat_transfer_ei(Necm,ve_op,ve_o2p,ve_nop,ve_np,Te,Ti):

    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)

    qDTe_opf=3*Necm*(10 ** 6)*const.boltzmann_si*ve_op*(const.me/(const.me+MO))*(Te-Ti)
    qDTe_o2pf=3*Necm*(10 ** 6)*const.boltzmann_si*ve_o2p*(const.me/(const.me+MO2))*(Te-Ti)
    qDTe_nopf=3*Necm*(10 ** 6)*const.boltzmann_si*ve_nop*(const.me/(const.me+MNO))*(Te-Ti)
    qDTe_npf=3*Necm*(10 ** 6)*const.boltzmann_si*ve_np*(const.me/(const.me+MN))*(Te-Ti)
    qDTe_if=qDTe_opf+qDTe_o2pf+qDTe_nopf+qDTe_npf
    
    return qDTe_opf,qDTe_o2pf,qDTe_nopf,qDTe_npf,qDTe_if