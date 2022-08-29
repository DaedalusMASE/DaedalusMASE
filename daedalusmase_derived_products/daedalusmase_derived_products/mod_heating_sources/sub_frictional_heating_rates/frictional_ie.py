"""
sub_Heating_Sources.frictional_ie

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-electron frictional heating rate in W/m^3
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

NOp: O+ density in cm^-3

NO2p: O2+ density in cm^-3

NNOp: NO+ density in cm^-3

Nplus: N+ density in cm^-3

ve_op: e-O+ collision frequency

ve_o2p: e-O2+ collision frequency

ve_nop: e-NO+ collision frequency

ve_np: e-N+ collision frequency

ue_uop_mag: electron-O+ relative velocity

ue_uo2p_mag: electron-O2+ relative velocity

ue_unop_mag: electron-NO+ relative velocity

ue_unp_mag: electron-N+ relative velocity 
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

qFe_i: electron-ion frictional heating rate in W/m^3

qFop_e: O+-e frictional heating rate in W/m^3

qFo2p_e: O2+-e frictional heating rate in W/m^3

qFnop_e: NO+-e frictional heating rate in W/m^3

qFnp_e: N+-e frictional heating rate in W/m^3
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""
import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def frictional_ie(NOp,NO2p,NNOp,Nplus,ve_op,ve_o2p,ve_nop,ve_np,ue_uop_mag,ue_uo2p_mag,ue_unop_mag,ue_unp_mag):

    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)

    qFop_e=NOp*MO*(const.me/(MO+const.me))*ve_op*ue_uop_mag*ue_uop_mag
    qFo2p_e=NO2p*MO2*(const.me/(MO2+const.me))*ve_o2p*ue_uo2p_mag*ue_uo2p_mag
    qFnop_e=NNOp*MNO*(const.me/(MNO+const.me))*ve_nop*ue_unop_mag*ue_unop_mag
    qFnp_e=Nplus*MN*(const.me/(MN+const.me))*ve_np*ue_unp_mag*ue_unp_mag

    qFe_i=qFop_e+qFo2p_e+qFnop_e+qFnp_e
    
    return qFe_i,qFop_e,qFo2p_e,qFnop_e,qFnp_e