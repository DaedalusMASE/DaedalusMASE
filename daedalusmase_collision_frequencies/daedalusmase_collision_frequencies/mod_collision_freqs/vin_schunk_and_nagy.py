"""
**sub_heating_sources.i_n_collision_freqs**

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-neutral collision frequencies
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`B_enu`: mangetic field vector in T in ENU

`Ti`: Ion temperature in K

`Tn`: Neutral temperature in K

`NO2`: \(O_2\) density in \(cm^{-3}\)

`NO` : \(O\) density in \(cm^{-3}\)

`NN2` : \(N_2\) density in \(cm^{-3}\)

`helium_f` : \(He\) density in \(cm^{-3}\)

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________


`vin`: ion-neutral collision frequency

`vop_o`: \(O^+-O\) collision frequency

`vop_o2`: \(O^+-O_2\) collision frequency

`vop_n2`: \(O^+-N_2\) collision frequency

`vop_he`: \(O^+-He\) collision frequency

`vo2p_o`: \(O_2^+-O\) collision frequency

`vo2p_o2`: \(O_2^+-O_2\) collision frequency

`vo2p_n2`: \(O_2^+-N_2\) collision frequency

`vo2p_he`: \(O_2^+-He\) collision frequency

`vnop_o`: \(NO^+-O\) collision frequency

`vnop_o2`: \(NO^+-O_2\) collision frequency

`vnop_n2`: \(NO^+-N_2\) collision frequency

`vnop_he`: \(NO^+-He\) collision frequency

`vnp_o`: \(N^+-O\) collision frequency

`vnp_o2`: \(N^+-O_2\) collision frequency

`vnp_n2`: \(N^+-N_2\) collision frequency

`vnp_he`: \(N^+-He\) collision frequency

`vOp`: \(O^+-neutral\) collision frequency

`vO2p`: \(O_2^+-neutral\) collision frequency

`vNOp`: \(NO^+-neutral\) collision frequency

`vNp`: \(N^+-neutral\) collision frequency

_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Schunk, R. and Nagy, A. (2009). Ionospheres: physics, plasma physics, and chemistry (Cambridge
university press)
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
from daedalusmase_collision_frequencies.mod_utils import const

def vin_schunk_and_nagy(B_enu,Ti,Tn,NO2,NO,NN2,helium_f):
    bnorm=np.sqrt(B_enu[0]*B_enu[0]+B_enu[1]*B_enu[1]+B_enu[2]*B_enu[2])
    bgauss=bnorm*10000
    qeomeo10=1.7588028*10**7
    qeoNa010=9.6489*10**3
    rmassinv_op=1/const.mO
    rmassinv_nop=1/const.mNO
    rmassinv_o2p=1/const.mO2
    rmassinv_np=1/const.mN
    
    #gyrofrequencies
    omega_op=qeoNa010*bgauss*rmassinv_op
    omega_o2p=qeoNa010*bgauss*rmassinv_o2p
    omega_nop=qeoNa010*bgauss*rmassinv_nop
    omega_np=qeoNa010*bgauss*rmassinv_np
    omega_op_inv=1/omega_op
    omega_o2p_inv=1/omega_o2p
    omega_nop_inv=1/omega_nop
    omega_np_inv=1/omega_np
    omega_e=qeomeo10*bgauss
    omega_e_inv=1/omega_e
    
    #collision frequencies in Hz
    
    temps=(Ti+Tn)/2
    rnu_o2p_o2=2.59 * (10**(-11))* np.sqrt(temps)*((1-0.073*np.log10(temps))**2)
    rnu_op_o2=6.64 * (10**(-10))
    rnu_nop_o2=4.27 * (10**(-10))
    rnu_np_o2=7.25*(10**(-10))

    rnu_o2p_o=2.31*(10**(-10))
    rnu_op_o=3.67 * (10**(-11)) * np.sqrt(temps)*((1-0.064*np.log10(temps))**2)*const.fcor
    rnu_nop_o=2.44 * (10**(-10))
    rnu_np_o=4.42*(10**(-10))

    rnu_o2p_n2=4.13*(10**(-10))
    rnu_op_n2=6.82 * (10**(-10))
    rnu_nop_n2=4.34*(10**(-10))
    rnu_np_n2=7.47*(10**(-10))

    rnu_o2p_he=0.7*(10**(-10))
    rnu_op_he=1.32*(10**(-10))
    rnu_nop_he=0.74*(10**(-10))
    rnu_np_he=1.49*(10**(-10))

    rnu_o2p_he=0.7*(10**(-10))
    rnu_op_he=1.32*(10**(-10))
    rnu_nop_he=0.74*(10**(-10))
    rnu_np_he=1.49*(10**(-10))                


    rnu_o2p_co2=5.63*(10**(-10))
    rnu_op_co2=8.95*(10**(-10))
    rnu_nop_co2=5.89*(10**(-10))
    rnu_np_co2=9.73*(10**(-10))                


    rnu_o2p=(rnu_o2p_o2*NO2+rnu_o2p_o*NO+rnu_o2p_n2*NN2+rnu_o2p_he*helium_f)*omega_o2p_inv
    rnu_op=(rnu_op_o2*NO2+rnu_op_o*NO+rnu_op_n2*NN2+rnu_op_he*helium_f)*omega_op_inv
    rnu_nop=(rnu_nop_o2*NO2+rnu_nop_o*NO+rnu_nop_n2*NN2+rnu_nop_he*helium_f)*omega_nop_inv
    rnu_np=(rnu_np_o2*NO2+rnu_np_o*NO+rnu_np_n2*NN2+rnu_np_he*helium_f)*omega_np_inv

    vOp=rnu_op_o2*NO2+rnu_op_o*NO+rnu_op_n2*NN2+rnu_op_he*helium_f
    vO2p=rnu_o2p_o2*NO2+rnu_o2p_o*NO+rnu_o2p_n2*NN2+rnu_o2p_he*helium_f
    vNOp=rnu_nop_o2*NO2+rnu_nop_o*NO+rnu_nop_n2*NN2+rnu_nop_he*helium_f
    vNp=rnu_np_o2*NO2+rnu_np_o*NO+rnu_np_n2*NN2+rnu_np_he*helium_f
    vin=(vOp+vO2p+vNOp)/4

    vop_o=rnu_op_o*NO
    vop_o2=rnu_op_o2*NO2
    vop_n2=rnu_op_n2*NN2
    vop_he=rnu_op_he*helium_f
    vo2p_o=rnu_o2p_o*NO
    vo2p_o2=rnu_o2p_o2*NO2
    vo2p_n2=rnu_o2p_n2*NN2
    vo2p_he=rnu_o2p_he*helium_f
    vnop_o=rnu_nop_o*NO
    vnop_o2=rnu_nop_o2*NO2
    vnop_n2=rnu_nop_n2*NN2
    vnop_he=rnu_nop_he*helium_f
    vnp_o=rnu_np_o*NO
    vnp_o2=rnu_np_o2*NO2
    vnp_n2=rnu_np_n2*NN2
    vnp_he=rnu_np_he*helium_f

    return vin,vop_o,vop_o2,vop_n2,vop_he,vo2p_o,vo2p_o2,vo2p_n2,vo2p_he,vnop_o,vnop_o2,vnop_n2,vnop_he,vnp_o,vnp_o2,vnp_n2,vnp_he,vOp,vO2p,vNOp,vNp
