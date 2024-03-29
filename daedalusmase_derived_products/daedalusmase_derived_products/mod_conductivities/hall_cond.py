"""
**sub_heating_sources.hall_cond**

**Description**:
_____________________________________________________________________________________________________________________

Calculate Hall conductivity in S/m

$$\\sigma_H=\\frac{e}{B}\\Bigg( N_e\\frac{\\Omega_e^2 }{\\Omega_e^2+\\nu_{en}^2} -\\sum_i N_i\\frac{\\Omega_i^2 }{\\Omega_i^2+\\nu_{in}^2} \\Bigg)$$
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`B`: Magnetic field vector in T

`Ti`: Ion temperature in K

`Tn`: Neutral temperature in K

`NO2`: \(O_2\) density in \(cm^{-3}\)

`NN2`: \(N_2\) density in \(cm^{-3}\)

`NO`: \(O\) density in \(cm^{-3}\)

`NOp`: \(O^+\) density in \(cm^{-3}\)

`NO2p`: \(O_2^+\) density in \(cm^{-3}\)

`NNOp`: \(NO^+\) density in \(cm^{-3}\)
____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`sigmaHall`: Hall conductivity in S/m
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Schunk, R. and Nagy, A. (2009). Ionospheres: physics, plasma physics, and chemistry (Cambridge
university press)
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""


import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def hall_cond(B,Ti,Te,Tn,NO2,NN2,NO,NOp,NO2p,NNOp):

    bnorm = np.sqrt(B[0] * B[0] + B[1] * B[1] + B[2] * B[2])

    bgauss=bnorm*10000
    qeomeo10=1.7588028*10**7
    qeoNa010=9.6489*10**3
    rmassinv_op=1/const.mO
    rmassinv_nop=1/const.mNO
    rmassinv_o2p=1/const.mO2
    
    omega_op=qeoNa010*bgauss*rmassinv_op
    omega_o2p=qeoNa010*bgauss*rmassinv_o2p
    omega_nop=qeoNa010*bgauss*rmassinv_nop
    omega_op_inv=1/omega_op
    omega_o2p_inv=1/omega_o2p
    omega_nop_inv=1/omega_nop
    omega_e=qeomeo10*bgauss
    omega_e_inv=1/omega_e
    
  

    #collision frequencies (Hz)
    temps=(Ti+Tn)/2
    
    rnu_o2p_o2=2.59 * (10**(-11))* np.sqrt(temps)*((1-0.073*np.log10(temps))**2)
    rnu_op_o2=6.64 * (10**(-10))
    rnu_nop_o2=4.27 * (10**(-10))
    rnu_np_o2=7.25 * (10**(-10))
    
    rnu_o2p_o=2.31*(10**(-10))
    rnu_op_o=3.67 * (10**(-11)) * np.sqrt(temps)*((1-0.064*np.log10(temps))**2)*const.fcor
    rnu_nop_o=2.44 * (10**(-10))
    rnu_np_o=4.42 * (10**(-10))
    
    rnu_o2p_n2=4.13*(10**(-10))
    rnu_op_n2=6.82 * (10**(-10))
    rnu_nop_n2=4.34*(10**(-10))
    rnu_np_n2=7.47*(10**(-10))
    
    rnu_o2p_he=0.7* (10**(-10))
    rnu_op_he=1.32* (10**(-10))
    rnu_nop_he=0.74* (10**(-10))
    rnu_np_he=1.49*(10**(-10))
    
    rnu_o2p=(rnu_o2p_o2*NO2+rnu_o2p_o*NO+rnu_o2p_n2*NN2)*omega_o2p_inv
    rnu_op=(rnu_op_o2*NO2+rnu_op_o*NO+rnu_op_n2*NN2)*omega_op_inv
    rnu_nop=(rnu_nop_o2*NO2+rnu_nop_o*NO+rnu_nop_n2*NN2)*omega_nop_inv
    
    
    vOp=rnu_op_o2*NO2+rnu_op_o*NO+rnu_op_n2*NN2
    vO2p=rnu_o2p_o2*NO2+rnu_o2p_o*NO+rnu_o2p_n2*NN2
    vNOp=rnu_nop_o2*NO2+rnu_nop_o*NO+rnu_nop_n2*NN2
    vin=vOp+vO2p+vNOp
    
    
    vop_o=rnu_op_o*NO
    vop_o2=rnu_op_o2*NO2
    vop_n2=rnu_op_n2*NN2
    vo2p_o=rnu_o2p_o*NO
    vo2p_o2=rnu_o2p_o2*NO2
    vo2p_n2=rnu_o2p_n2*NN2
    vnop_o=rnu_nop_o*NO
    vnop_o2=rnu_nop_o2*NO2
    vnop_n2=rnu_nop_n2*NN2
    # vop_he=rnu_op_he*helium_f
    # vo2p_he=rnu_o2p_he*helium_f
    # vnop_he=rnu_nop_he*helium_f
    vnp_o=rnu_np_o*NO
    vnp_o2=rnu_np_o2*NO2
    vnp_n2=rnu_np_n2*NN2
    # vnp_he=rnu_np_he*helium_f
    
    
    ven=(2.33 * (10**(-11))*NN2*Te*(1-(1.21*(10**(-4)*Te))) \
        + 1.82 * (10**(-10))*NO2*np.sqrt(Te)*(1+(3.6*(10**(-2)*np.sqrt(Te)))) \
        +8.9 * (10**(-11))*NO*np.sqrt(Te)*(1+(5.7*(10**(-4)*Te))))
    
    ve_n2=2.33 * (10**(-11))*NN2*Te*(1-(1.21*(10**(-4)*Te)))
    ve_o=8.9 * (10**(-11))*NO*np.sqrt(Te)*(1+(5.7*(10**(-4)*Te)))
    ve_o2=1.82 * (10**(-10))*NO2*np.sqrt(Te)*(1+(3.6*(10**(-2)*np.sqrt(Te))))
    # ve_he=4.6* (10**(-10))*helium_f*np.sqrt(Te)
    
    rnu_ne=(2.33 * (10**(-11))*NN2*Te*(1-(1.21*(10**(-4)*Te))) \
        + 1.82 * (10**(-10))*NO2*np.sqrt(Te)*(1+(3.6*(10**(-2)*np.sqrt(Te)))) \
        +8.9 * (10**(-11))*NO*np.sqrt(Te)*(1+(5.7*(10**(-4)*Te))))*omega_e_inv
    rnu_ne=4*rnu_ne

      
    ########################################################################
#                   Conductivities
    ########################################################################                
    
    qe_fac=(const.electron*10**10)/bgauss
    Necm2=NOp+NO2p+NNOp
    
    sigmaHall=qe_fac*(Necm2/(1+rnu_ne**2)-NOp/(1+rnu_op**2)-NO2p/(1+rnu_o2p**2)-NNOp/(1+rnu_nop**2))

    return sigmaHall