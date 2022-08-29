"""
sub_Heating_Sources.frictional

**Description**:
_____________________________________________________________________________________________________________________

Calculate frictional heating rate in W/m^3
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

vOp: O+- neutral collision frequency

vO2p: O2+- neutral collision frequency

vNOp: NO+- neutral collision frequency

NOp: O+ density in cm^-3

NO2p: O2+ density in cm^-3

NNOp: NO+ density in cm^-3

vi_op_starmag: O+ velcoity magnitude

vi_o2p_starmag: O2+ velcoity magnitude

vi_nop_starmag: NO+ velcoity magnitude
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

Frictional1: frictional heating in W/m^3

Frictional_op: O+ frictional heating in W/m^3

Frictional_o2p: O2+ frictional heating in W/m^3

Frictional_nop: NO+ frictional heating in W/m^3
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def frictional(vOp,vO2p,vNOp,NOp,NO2p,NNOp,vi_op_starmag,vi_o2p_starmag,vi_nop_starmag):
    
    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)

    Frictional_op=MO*NOp*(10**6)*vOp*vi_op_starmag*vi_op_starmag
    Frictional_o2p=MO2*NO2p*(10**6)*vO2p*vi_o2p_starmag*vi_o2p_starmag
    Frictional_nop=MNO*NNOp*(10**6)*vNOp*vi_nop_starmag*vi_nop_starmag
    Frictional1=Frictional_op+Frictional_o2p+Frictional_nop
    
    return Frictional1,Frictional_op,Frictional_o2p,Frictional_nop