"""
sub_Heating_Sources.ion_velocities

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion velocity by solving the coresponding momentum equation

$$\\vec{v_{i\\bot}^{*}}= \\frac{\\nu_{in} \\Omega_{i} \\vec{E_{\\bot}^{*}} - \\Omega_{i}^2 \\hat{b} \\times \\vec{E_{\\bot}^{*}} }{B(\\nu_{in}^2+\\Omega_{i}^2)}$$
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`vin`: ion-neutral collision frequency

`omega_op`: ion cyclotron frequency

`Estar`: Perpendicular electric field in neutral atmosphere reference frame in \(V/m\)      

`B_enu`: magnetic field vector in \(T\) [ENU]

`Un`: Neutral velocity in \(m/s\) [ENU]

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`vi_starx`: ion velocity in \(m/s\) in neutral reference frame [east]

`vi_stary`: ion velocity in \(m/s\) in neutral reference frame [north]

`vi_starz`: ion velocity in \(m/s\) in neutral reference frame [up]

`vi_starmag`: ion velocity magnitude in \(m/s\) in neutral reference frame 
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

def ion_velocities(vin,omega_i,Estar,B_enu,Un):

    bnorm=np.sqrt(B_enu[0]*B_enu[0]+B_enu[1]*B_enu[1]+B_enu[2]*B_enu[2])
    b_unit=[B_enu[0]/bnorm,B_enu[1]/bnorm,B_enu[2]/bnorm]
    #O+
    vi_star=(vin*omega_i*Estar+omega_i**2*(np.cross(Estar,b_unit)))/(bnorm*(vin**2+omega_i**2))
    vi_starx=vi_star[0] #m/s
    vi_stary=vi_star[1] #m/s
    vi_starz=vi_star[2] #m/s
    vi_starmag=np.sqrt(vi_star[0] * vi_star[0] + vi_star[1] * vi_star[1] + vi_star[2] * vi_star[2])

    Unvert=np.cross(Un,b_unit)

    vie_op=vi_starx+Unvert[0] #from neutral frame to ENU
    vin_op=vi_stary+Unvert[1] #from neutral frame to ENU
    viu_op=vi_starz+Unvert[2] #from neutral frame to ENU

    vi_east_op=vie_op
    vi_north_op=vin_op

    vinorm_op=np.sqrt(vie_op*vie_op+vin_op*vin_op+viu_op*viu_op)
    e_unit_op=[vie_op / vinorm_op, vin_op / vinorm_op, viu_op / vinorm_op]
    
    return vi_starx,vi_stary,vi_starz,vi_starmag


