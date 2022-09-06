"""
sub_Heating_Sources.frictional_o2pn

**Description**:
_____________________________________________________________________________________________________________________

Calculate \(O_2^+\)-neutral frictional heating rate
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`NO2p`: \(O_2^+\) density in \(cm^{-3}\)

`vo2p_o`: \(O_2^+\)-\(O\) collision frequency

`vo2p_o2`: \(O_2^+\)-\(O_2\) collision frequency

`vo2p_n2`: \(O_2^+\)-\(N_2\) collision frequency

`vo2p_he`: \(O_2^+\)-\(He\) collision frequency

`vi_o2p_starmag`: \(O_2^+\) velocity magnitude in \(m/s\)
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`qFo2p_o`: \(O_2^+\)-\(O\) frictional heating rate in \(W/m^{3}\)

`qFo2p_o2`: \(O_2^+\)-\(O_2\) frictional heating rate in \(W/m^{3}\)

`qFo2p_n2`: \(O_2^+\)-\(N_2\) frictional heating rate in \(W/m^{3}\)

`qFo2p_he`: \(O_2^+\)-\(He\) frictional heating rate in \(W/m^{3}\)

`qFo2p_n`: \(O_2^+\)-neutral frictional heating rate in \(W/m^{3}\)
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

def frictional_o2pn(NO2p,vo2p_o,vo2p_o2,vo2p_n2,vo2p_he,vi_o2p_starmag):

    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)

    qFo2p_o=NO2p*MO2*(MO/(MO2+MO))*vo2p_o*vi_o2p_starmag*vi_o2p_starmag
    qFo2p_o2=NO2p*MO2*(MO2/(MO2+MO2))*vo2p_o2*vi_o2p_starmag*vi_o2p_starmag
    qFo2p_n2=NO2p*MO2*(MN2/(MO2+MN2))*vo2p_n2*vi_o2p_starmag*vi_o2p_starmag
    qFo2p_he=NO2p*MO2*(MHE/(MO2+MHE))*vo2p_he*vi_o2p_starmag*vi_o2p_starmag
    

    qFo2p_n=qFo2p_o+qFo2p_o2+qFo2p_n2+qFo2p_he

    return qFo2p_o,qFo2p_o2,qFo2p_n2,qFo2p_he,qFo2p_n