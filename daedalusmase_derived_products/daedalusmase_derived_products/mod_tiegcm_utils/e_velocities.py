"""
sub_Heating_Sources.e_velocities

**Description**:
_____________________________________________________________________________________________________________________

Calculate e velocity by solving the coresponding momentum equation

$$\\vec{v_{e\\bot}^{*}}= \\frac{-\\nu_{en} \\Omega_{e} \\vec{E_{\\bot}^{*}} - \\Omega_{e}^2 \\hat{b} \\times \\vec{E_{\\bot}^{*}} }{B(\\nu_{en}^2+\\Omega_{e}^2)}$$
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`ven`: electron-neutral collision frequency

`omega_e`: electron cyclotron frequency 

`Estar`: Perpendicular electric field in neutral atmosphere reference frame in \(V/m\)    

`B_enu`: magnetic field vector in \(T\) [ENU]

`Un`: Neutral velocity in \(m/s\) [ENU]

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`ve_starx`: electron velocity in \(m/s\) in neutral reference frame [east]

`ve_stary`: electron velocity in \(m/s\) in neutral reference frame [north]

`ve_starz`: electron velocity in \(m/s\) in neutral reference frame [up]

`ve_starmag`: electron velocity magnitude in \(m/s\) in neutral reference frame 
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Richmond, A. and Thayer, J. (2000). Ionospheric electrodynamics: A tutorial. Magnetospheric current
systems 118, 131–146
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np

def e_velocities(ven,omega_e,Estar,B_enu,Un):
    
    bnorm=np.sqrt(B_enu[0]*B_enu[0]+B_enu[1]*B_enu[1]+B_enu[2]*B_enu[2])
    b_unit=[B_enu[0]/bnorm,B_enu[1]/bnorm,B_enu[2]/bnorm]
    ve_star=(-ven*omega_e*Estar+omega_e**2*(np.cross(Estar,b_unit)))/(bnorm*(ven**2+omega_e**2))
    ve_starx=ve_star[0] #m/s
    ve_stary=ve_star[1] #m/s
    ve_starz=ve_star[2] #m/s
    ve_starmag=np.sqrt(ve_star[0] * ve_star[0] + ve_star[1] * ve_star[1] + ve_star[2] * ve_star[2])

    Unvert=np.cross(Un,b_unit)

    ve_xtemp=ve_starx+Unvert[0] #from neutral frame to ENU
    ve_ytemp=ve_stary+Unvert[1] #from neutral frame to ENU
    ve_ztemp=ve_starz+Unvert[2] #from neutral frame to ENU

    return ve_starx,ve_stary,ve_starz,ve_starmag

