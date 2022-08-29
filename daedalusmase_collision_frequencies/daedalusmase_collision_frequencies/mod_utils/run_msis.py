"""
sub_Heating_Sources.igrf_B

**Description**:
_____________________________________________________________________________________________________________________

Calculate IGRF magnetic field in ENU and ECEF
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

time_p: time (datetime object) 

lat_p: latitude in deg 

lon_p: longitude in deg 

alt_p: altitude in km
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

B_enu: Magnetic field vector in ENU

b_unit_enu: Magnetic field unit vector in ENU
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
import msise00

def run_msis(time_p, lat_p, lon_p, alt_p):    
    atmos = msise00.run(time_p, alt_p, lat_p, lon_p)
    He = atmos.He.values[0][0][0][0]
    O  = atmos.O.values[0][0][0][0]
    N2 = atmos.N2.values[0][0][0][0]
    O2 = atmos.O2.values[0][0][0][0]
    Ar  = atmos.Ar.values[0][0][0][0]
    H = atmos.H.values[0][0][0][0]
    N  = atmos.N.values[0][0][0][0]
    Tn = atmos.Tn.values[0][0][0][0]
    AnomalousO = atmos.AnomalousO.values[0][0][0][0]

    Ntotal= atmos.Total.values[0][0][0][0]
    f107=atmos.f107s
    Ap=atmos.Ap
    return O,O2,N,N2,He,H,Ar,Ntotal,Tn
