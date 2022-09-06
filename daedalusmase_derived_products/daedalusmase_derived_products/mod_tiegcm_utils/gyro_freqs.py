"""
sub_heating_sources.gyro_freqs

**Description**:
_____________________________________________________________________________________________________________________

Calculate cyclotron frequencys

$$\\Omega_i=\\frac{q_i B}{m_i}$$
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`B`: Magnetic field in T

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`omega_e`: \(e\) gyrofrequency in \(rad/s\)

`omega_op`: \(O^+\) gyrofrequency in \(rad/s\)

`omega_o2p`: \(O_2^+\) gyrofrequency in \(rad/s\)

`omega_nop`: \(NO^+\) gyrofrequency in \(rad/s\)

`omega_np`: \(N^+\) gyrofrequency in \(rad/s\)

_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""


import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def gyro_freqs(B):

    bnorm = np.sqrt(B[0] * B[0] + B[1] * B[1] + B[2] * B[2])
    bgauss=bnorm*10000
    qeomeo10=1.7588028*10**7
    qeoNa010=9.6489*10**3
    rmassinv_op=1/const.mO
    rmassinv_nop=1/const.mNO
    rmassinv_o2p=1/const.mO2 
    rmassinv_np=1/const.mN

    omega_op=qeoNa010*bgauss*rmassinv_op
    omega_o2p=qeoNa010*bgauss*rmassinv_o2p
    omega_nop=qeoNa010*bgauss*rmassinv_nop
    omega_e=qeomeo10*bgauss
    omega_np=qeoNa010*bgauss*rmassinv_np

    return omega_e, omega_op, omega_o2p, omega_nop, omega_np