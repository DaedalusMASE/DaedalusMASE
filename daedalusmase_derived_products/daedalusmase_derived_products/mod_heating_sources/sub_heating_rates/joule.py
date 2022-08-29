"""
sub_Heating_Sources.joule

**Description**:
_____________________________________________________________________________________________________________________

Calculate Joule heating rate
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

NOp:

NO2p:

NNOp:

vi_op_starx:

vi_op_stary:

vi_op_starz:

vi_o2p_starx:

vi_o2p_stary:

vi_o2p_starz:

vi_nop_starx:

vi_nop_stary:

vi_nop_starz:

E_T_vert:

Unvert:

B:
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

Joule1: joule heating rate in W/m^3

Joule_op: O+ joule heating rate in W/m^3

Joule_o2p: O2+ joule heating rate in W/m^3

Joule_nop: NO+ joule heating rate in W/m^3
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def joule(NOp,NO2p,NNOp,vi_op_starx,vi_op_stary,vi_op_starz,vi_o2p_starx,vi_o2p_stary,vi_o2p_starz,vi_nop_starx,vi_nop_stary,vi_nop_starz,E_T_vert,Un,B_enu):
    
    bnorm=np.sqrt(B_enu[0]*B_enu[0]+B_enu[1]*B_enu[1]+B_enu[2]*B_enu[2])
    bunit=[B_enu[0]/bnorm,B_enu[1]/bnorm,B_enu[2]/bnorm]
    Unvert=np.cross(Un,bunit)

    A=E_T_vert+np.cross(Unvert,B_enu)
    vi_op_star=[vi_op_starx,vi_op_stary,vi_op_starz]
    vi_o2p_star=[vi_o2p_starx,vi_o2p_stary,vi_o2p_starz]
    vi_nop_star=[vi_nop_starx,vi_nop_stary,vi_nop_starz]
    
    Joule_op=const.electron*NOp*(10**6)*np.dot(vi_op_star,A)
    Joule_o2p=const.electron*NO2p*(10**6)*np.dot(vi_o2p_star,A)
    Joule_nop=const.electron*NNOp*(10**6)*np.dot(vi_nop_star,A)
    Joule1=Joule_op+Joule_o2p+Joule_nop
    
    return Joule1,Joule_op,Joule_o2p,Joule_nop