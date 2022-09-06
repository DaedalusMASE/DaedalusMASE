"""
sub_Heating_Sources.frictional_npn

**Description**:
_____________________________________________________________________________________________________________________

Calculate \(N^+\)-neutral frictional heating rate
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`NNp`: \(N^+\) density in \(cm^{-3}\)

`vnp_o`: \(N^+\)-\(O\) collision frequency

`vnp_o2`: \(N^+\)-\(O_2\) collision frequency

`vnp_n2`: \(N^+\)-\(N_2\) collision frequency

`vnp_he`: \(N^+\)-\(He\) collision frequency

`vi_np_starmag`: \(N^+\) velocity magnitude in \(m/s\)
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`qFnp_o`: \(N^+\)-\(O\) frictional heating rate in \(W/m^{3}\)

`qFnp_o2`: \(N^+\)-\(O_2\) frictional heating rate in \(W/m^{3}\)

`qFnp_n2`: \(N^+\)-\(N_2\) frictional heating rate in \(W/m^{3}\)

`qFnp_he`: \(N^+\)-\(He\) frictional heating rate in \(W/m^{3}\)

`qFnp_n`: \(N^+\)-neutral frictional heating rate in \(W/m^{3}\)
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

def frictional_npn(Nplus,vnp_o,vnp_o2,vnp_n2,vnp_he,vi_np_starmag):


    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)    

    qFnp_o=Nplus*MN*(MO/(MN+MO))*vnp_o*vi_np_starmag*vi_np_starmag
    qFnp_o2=Nplus*MN*(MO2/(MN+MO2))*vnp_o2*vi_np_starmag*vi_np_starmag
    qFnp_n2=Nplus*MN*(MN2/(MN+MN2))*vnp_n2*vi_np_starmag*vi_np_starmag
    qFnp_he=Nplus*MN*(MHE/(MN+MHE))*vnp_he*vi_np_starmag*vi_np_starmag
    

    qFnp_n=qFnp_o+qFnp_o2+qFnp_n2+qFnp_he

    return qFnp_o,qFnp_o2,qFnp_n2,qFnp_he,qFnp_n