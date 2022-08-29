"""
sub_Heating_Sources.i_i_frictional

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-ion frictional heating rate in W/m^3
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________



NOp: O+ density in cm^-3

NO2p: O2+ density in cm^-3

NNOp: NO+ density in cm^-3

NNp: N+ density in cm^-3

vop_o2p: O+-O2+ collision frequency

vop_nop: O+-NO+ collision frequency

vop_np: O+-N+ collision frequency

vo2p_nop: O2+-NO+ collision frequency

vo2p_np: O2+-N+ collision frequency

vnop_np: NO+-N+ collision frequency

uop_o2p_mag: O+-O2+ relative velocity

uop_nop_mag: O+-NO+ relative velocity

uop_np_mag: O+-N+ relative velocity

uo2p_nop_mag: O2+-NO+ relative velocity

unp_o2p_mag: N+-O2+ relative velocity

unop_np_mag: NO+-N+ relative velocity

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

qFi_i: ion-ion frictional heating rate in W/m^3

qFop_o2p: O+-O2+ frictional heating rate in W/m^3

qFop_nop: O+-NO+ frictional heating rate in W/m^3

qFop_np: O+-N+ frictional heating rate in W/m^3

qFo2p_nop: O2+-O+ frictional heating rate in W/m^3

qFo2p_np: O2+-N+ frictional heating rate in W/m^3

qFnop_np: NO+-N+ frictional heating rate in W/m^3

_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""
import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def i_i_frictional(NOp,NO2p,NNOp,NNp,vop_o2p,vop_nop,vop_np,vo2p_nop,vo2p_np,vnop_np,uop_o2p_mag,uop_nop_mag,
                  uop_np_mag,uo2p_nop_mag,unp_o2p_mag,unop_np_mag):

    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)

    qFop_o2p=NOp*MO*(MO2/(MO+MO2))*vop_o2p*uop_o2p_mag*uop_o2p_mag
    qFop_nop=NOp*MO*(MNO/(MO+MNO))*vop_nop*uop_nop_mag*uop_nop_mag
    qFop_np=NNp*MO*(MN/(MO+MN))*vop_np*uop_np_mag*uop_np_mag
    qFo2p_nop=NO2p*MO2*(MNO/(MO2+MNO))*vo2p_nop*uo2p_nop_mag*uo2p_nop_mag
    qFo2p_np=NO2p*MO2*(MN/(MO2+MN))*vo2p_np*unp_o2p_mag*unp_o2p_mag
    qFnop_np=NNOp*MNO*(MN/(MNO+MN))*vnop_np*unop_np_mag*unop_np_mag

    qFi_i=qFop_o2p+qFop_nop+qFop_np+qFo2p_nop+qFo2p_np+qFnop_np
    
    return qFi_i,qFop_o2p,qFop_nop,qFop_np,qFo2p_nop,qFo2p_np,qFnop_np
