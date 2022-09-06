"""
sub_Heating_Sources.frictional_nopn

**Description**:
_____________________________________________________________________________________________________________________

Calculate \(NO^+\)-neutral frictional heating rate
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`NNOp`: \(NO^+\) density in \(cm^{-3}\)

`vnop_o`: \(NO^+\)-\(O\) collision frequency

`vnop_o2`: \(NO^+\)-\(O_2\) collision frequency

`vnop_n2`: \(NO^+\)-\(N_2\) collision frequency

`vnop_he`: \(NO^+\)-\(He\) collision frequency

`vi_nop_starmag`: \(NO^+\) velocity magnitude in \(m/s\)
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`qFnop_o`: \(NO^+\)-\(O\) frictional heating rate in \(W/m^{3}\)

`qFnop_o2`: \(NO^+\)-\(O_2\) frictional heating rate in \(W/m^{3}\)

`qFnop_n2`: \(NO^+\)-\(N_2\) frictional heating rate in \(W/m^{3}\)

`qFnop_he`: \(NO^+\)-\(He\) frictional heating rate in \(W/m^{3}\)

`qFnop_n`: \(NO^+\)-neutral frictional heating rate in \(W/m^{3}\)
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

def frictional_nopn(NNOp,vnop_o,vnop_o2,vnop_n2,vnop_he,vi_nop_starmag):


    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)    

    qFnop_o=NNOp*MNO*(MO/(MNO+MO))*vnop_o*vi_nop_starmag*vi_nop_starmag
    qFnop_o2=NNOp*MNO*(MO2/(MNO+MO2))*vnop_o2*vi_nop_starmag*vi_nop_starmag
    qFnop_n2=NNOp*MNO*(MN2/(MNO+MN2))*vnop_n2*vi_nop_starmag*vi_nop_starmag
    qFnop_he=NNOp*MNO*(MHE/(MNO+MHE))*vnop_he*vi_nop_starmag*vi_nop_starmag
    

    qFnop_n=qFnop_o+qFnop_o2+qFnop_n2+qFnop_he

    return qFnop_o,qFnop_o2,qFnop_n2,qFnop_he,qFnop_n