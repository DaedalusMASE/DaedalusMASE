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
from daedalusmase_collision_frequencies.mod_utils import allocations as alloc
import matplotlib.pyplot as plt

def op_o_cols(Ti,Tn):
        #O+_O freqs
        Tr=(Ti+Tn)/2

        q_dalgarno=4.3*10**(-11)*Tr**(0.41)
        q_banks=3.5*10**(-11)*np.sqrt(Tr)*((1-np.log10(Tr))**2)
        q_stubbe=7.2*10**(-11)*(Tr**0.37)

        q_sw=3.69*10**(-11)*np.sqrt(Tr)*((1-np.log10(Tr))**2)
        q_salah=4*10**(-11)*np.sqrt(Tr)
        q_pesnell=5.9*10**(-11)*np.sqrt(Tr)*((1-0.096*np.log10(Tr))**2)
        q_hickmann=5.92*10**(-11)*(Tr**(0.393))*(1+(96.6/Tr)**2)
        q_shunk_nagy=3.67 * (10**(-11)) * np.sqrt(Tr)*((1-0.064*np.log10(Tr))**2)
        q_richmond=6.7 * (10**(-11)) * np.sqrt(Tr)*((0.96-0.135*np.log10(Tr))**2)
        q_ieda=3.6834 * (10**(-11)) * np.sqrt(Tr)*((1-0.06482*np.log10(Tr))**2)
        q_baily_belan=4.45*10**(-11)*np.sqrt(Tr)*((1.04-0.067*np.log10(Tr))**2)
        return Tr,q_dalgarno,q_banks,q_stubbe,q_sw,q_salah,q_pesnell,q_hickmann,q_shunk_nagy,q_richmond,q_ieda,q_baily_belan