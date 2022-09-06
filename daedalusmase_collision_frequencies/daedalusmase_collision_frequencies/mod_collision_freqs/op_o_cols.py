"""
sub_Heating_Sources.op_o_cols

**Description**:
_____________________________________________________________________________________________________________________

Calculate dependence of different \(O^+-O\) collision frequency formulas on temperatures
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`Ti`: Ion temperature in K

`Tn`: Neutral temperature in K
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`Tr`: transition temperature in K

`q_dalgarno`: normalised \(O^+-O\) frequency according to Dalgarno et al (1964)

`q_banks`: normalised \(O^+-O\) frequency according to Banks (1966)

`q_stubbe`: normalised \(O^+-O\) frequency according to Stubbe (1968)

`q_sw`: normalised \(O^+-O\) frequency according to Schunk and Walker (1973)

`q_salah`: normalised \(O^+-O\) frequency according to  Salah (1993)

`q_pesnell`: normalised \(O^+-O\) frequency according to Pesnell et al (1993)

`q_hickmann`: normalised \(O^+-O\) frequency according to Hickman et al (1997)

`q_shunk_nagy`: normalised \(O^+-O\) frequency according to SAchunk and Nagy (2009)

`q_richmond`: normalised \(O^+-O\) frequency according to  Richmond (2017)

`q_ieda`: normalised \(O^+-O\) frequency according to Ieda (2020)

`q_baily_belan`: normalised \(O^+-O\) frequency according to Bailey and Belan
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Dalgarno, A., Henry, R., and Stewart, A. (1964). The photoionization of atomic oxygen. Planetary and
Space Science 12, 235–246

Banks, P. (1966). Collision frequencies and energy transfer electrons. Planetary and Space Science 14,
1085–1103

Stubbe, P. (1968). Frictional forces and collision frequencies between moving ion and neutral gases.
Journal of Atmospheric and Terrestrial Physics 30, 1965–1985

Schunk, R. and Walker, J. (1973). Theoretical ion densities in the lower ionosphere. Planetary and Space
Science 21, 1875–1896

Salah, J. E. (1993). Interim standard for the ion-neutral atomic oxygen collision frequency. Geophysical
research letters 20, 1543–1546

Pesnell, W. D., Omidvar, K., and Hoegy, W. R. (1993). Momentum transfer collision frequency of o+-o.
Geophysical Research Letters 20, 1343–1346

Hickman, A., Medikeri-Naphade, M., Chapin, C., and Huestis, D. (1997). Fine structure effects in the o+-o
collision frequency. Geophysical research letters 24, 119–122

Schunk, R. and Nagy, A. (2009). Ionospheres: physics, plasma physics, and chemistry (Cambridge
university press)

Richmond, A. D. (2017). Ionospheric electrodynamics. In Handbook of atmospheric electrodynamics,
volume II (CRC Press). 249–290

Ieda, A. (2020). Ion-neutral collision frequencies for calculating ionospheric conductivity. Journal of
Geophysical Research: Space Physics 125, e2019JA027128


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