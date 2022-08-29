"""
sub_Heating_Sources.Op_velocities

**Description**:
_____________________________________________________________________________________________________________________

Calculate O+ by solving the coresponding momentum equation
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

vin: O+-neutral collision frequency

omega_op: O+ cyclotron frequency

Estar: Perpendicular electric field in neutral atmosphere reference frame in V/m      

B_enu: magnetic field vector in ENU

Un: Neutral velocity in m/s [ENU]

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

vi_starx

vi_stary

vi_starz

vi_starmag
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

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


