"""
**sub_heating_sources.i_n_collision_freqs_sangalli**

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-neutral collision frequencies

$$\\nu_{in}=\\frac{\Omega_i}{B}\\frac{|\\vec{E}+\\vec{v_i}\\times\\vec{B}|}{|\\vec{v}_{i,\\perp}-\\vec{u}_{n,\\perp}|}=\\frac{e}{m_i}\\frac{|\\vec{E}+\\vec{v_i}\\times\\vec{B}|}{|\\vec{v}_{i,\\perp}-\\vec{u}_{n,\\perp}|}$$
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`B_enu`: magnetic field in T in ENU

`E_enu`: electric field in V/m in ENU

`Ui_enu`: ion velocity in m/s in ENU

`Un_enu`: neutral velocity in m/s in ENU

`mi`: ion mas in kg

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________


`vin`: ion-neutral collision frequency

_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Sangalli, L., Knudsen, D., Larsen, M., Zhan, T., Pfaff, R., and Rowland, D. (2009). Rocket-based
measurements of ion velocity, neutral wind, and electric field in the collisional transition region of the832
auroral ionosphere. Journal of Geophysical Research: Space Physics 114
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def i_n_collision_freqs_sangalli(B_enu,E_enu,Ui_enu,Un_enu,mi):
    bnorm=np.sqrt(B_enu[0]*B_enu[0]+B_enu[1]*B_enu[1]+B_enu[2]*B_enu[2])
    b_unit=[B_enu[0]/bnorm,B_enu[1]/bnorm,B_enu[2]/bnorm]
    uixB=np.cross(Ui_enu,B_enu)
    E_uixB=E_enu+uixB
    E_uixB_norm=np.sqrt(E_uixB[0]*E_uixB[0]+E_uixB[1]*E_uixB[1]+E_uixB[2]*E_uixB[2])

    Unvert=np.cross(Un_enu,b_unit)
    Ui_Un=Ui_enu-Unvert
    Ui_Un_norm=np.sqrt(Ui_Un[0]*Ui_Un[0]+Ui_Un[1]*Ui_Un[1]+Ui_Un[2]*Ui_Un[2])

    vin=(const.electron/mi)*(E_uixB_norm/Ui_Un_norm)
    return vin