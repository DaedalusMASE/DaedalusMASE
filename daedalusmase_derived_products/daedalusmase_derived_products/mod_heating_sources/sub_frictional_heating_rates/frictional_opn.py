"""
sub_Heating_Sources.frictional_opn

**Description**:
_____________________________________________________________________________________________________________________

Calculate \(O^+\)-neutral frictional heating rate
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`NOp`: \(O^+\) density in \(cm^{-3}\)

`vop_o`: \(O^+\)-\(O\) collision frequency

`vop_o2`: \(O^+\)-\(O_2\) collision frequency

`vop_n2`: \(O^+\)-\(N_2\) collision frequency

`vop_he`: \(O^+\)-\(He\) collision frequency

`vi_op_starmag`: \(O^+\) velocity magnitude in \(m/s\)
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`qFop_o`: \(O^+\)-\(O\) frictional heating rate in \(W/m^{3}\)

`qFop_o2`: \(O^+\)-\(O_2\) frictional heating rate in \(W/m^{3}\)

`qFop_n2`: \(O^+\)-\(N_2\) frictional heating rate in \(W/m^{3}\)

`qFop_he`: \(O^+\)-\(He\) frictional heating rate in \(W/m^{3}\)

`qFop_n`: \(O^+\)-neutral frictional heating rate in \(W/m^{3}\)
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Schunk, R. and Nagy, A. (2009). Ionospheres: physics, plasma physics, and chemistry (Cambridge
university press)
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def frictional_opn(NOp,vop_o,vop_o2,vop_n2,vop_he,vi_op_starmag):

    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)

    qFop_o=NOp*MO*(MO/(MO+MO))*vop_o*vi_op_starmag*vi_op_starmag
    qFop_o2=NOp*MO*(MO2/(MO+MO2))*vop_o2*vi_op_starmag*vi_op_starmag
    qFop_n2=NOp*MO*(MN2/(MO+MN2))*vop_n2*vi_op_starmag*vi_op_starmag
    qFop_he=NOp*MO*(MHE/(MO+MHE))*vop_he*vi_op_starmag*vi_op_starmag
    

    qFop_n=qFop_o+qFop_o2+qFop_n2+qFop_he

    return qFop_o,qFop_o2,qFop_n2,qFop_he,qFop_n