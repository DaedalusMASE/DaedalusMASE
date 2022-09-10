import numpy as np
def enu_ecef(lat_phi, lon_lmd, Fe, Fn, Fup):
    fac = np.pi / 180
    lat_phi = lat_phi * fac
    lon_lmd = lon_lmd * fac

    north_temp_unit = [-np.cos(lon_lmd) * np.sin(lat_phi), - np.sin(lon_lmd) * np.sin(lat_phi), np.cos(lat_phi)]
    east_temp_unit = [-np.sin(lon_lmd), np.cos(lon_lmd), 0]
    up_temp_unit = [np.cos(lon_lmd) * np.cos(lat_phi), np.sin(lon_lmd) * np.cos(lat_phi), np.sin(lat_phi)]

    Fnorth_vector = [Fn * north_temp_unit[0], Fn * north_temp_unit[1], Fn * north_temp_unit[2]]
    Feast_vector = [Fe * east_temp_unit[0], Fe * east_temp_unit[1], Fe * east_temp_unit[2]]
    Fup_vector = [Fup * up_temp_unit[0], Fup * up_temp_unit[1], Fup * up_temp_unit[2]]

    Fx = Fnorth_vector[0] + Feast_vector[0] + Fup_vector[0]
    Fy = Fnorth_vector[1] + Feast_vector[1] + Fup_vector[1]
    Fz = Fnorth_vector[2] + Feast_vector[2] + Fup_vector[2]

    return Fx, Fy, Fz

###

"""
sub_Heating_Sources.igrf_B
**Description**:
_____________________________________________________________________________________________________________________
Calculate IGRF-12 magnetic field in ENU and ECEF
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________
**Inputs**:
_____________________________________________________________________________________________________________________
`time_p`: time (datetime object) 
`lat_p`: latitude in \(deg\) 
`lon_p`: longitude in \(deg\)
`alt_p`: altitude in \(km\)
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________
**Outputs**:
_____________________________________________________________________________________________________________________
`B_enu`: Magnetic field vector in \(T\) [ENU]
`b_unit_enu`: Magnetic field unit vector [ENU]
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________
**Reference**:
_____________________________________________________________________________________________________________________
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________
"""

import igrf12

def igrf_B(time_p, lat_p, lon_p, alt_p):    
    mag=igrf12.igrf(time_p,lat_p,lon_p,alt_p)
    Be = mag.east.values[0]/10**9
    Bn = mag.north.values[0]/10**9
    Bu = -mag.down.values[0]/10**9
    B_enu = [Be, Bn, Bu]  # vector of magnetic field ENU in Telsa
    

    bnorm = np.sqrt(Be * Be + Bn * Bn + Bu * Bu)
    b_unit_enu = [Be / bnorm, Bn / bnorm, Bu / bnorm]

    return B_enu,b_unit_enu
