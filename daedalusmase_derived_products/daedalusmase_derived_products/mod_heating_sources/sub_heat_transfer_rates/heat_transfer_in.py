"""
sub_Heating_Sources.heat_transfer_in

**Description**:
_____________________________________________________________________________________________________________________

Calculate heat transfer rate between ions and neutrals in \(W/m^{3}\)

$$q_{\\Delta T_{in}}=N_e \\nu_{in} \\frac{m_i}{m_i+m_n} 3 k_B \\Big(T_i - T_n \\Big)$$
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________


`NOp`: \(O^+\) density in \(cm^{-3}\) 

`NO2p`: \(O_2^+\) density in \(cm^{-3}\) 

`NNOp`: \(NO^+\) density in \(cm^{-3}\) 

`Nplus`: \(N^+\) density in \(cm^{-3}\) 

`vop_o`: \(O^+\)-\(O\) collision frequency

`vop_o2`: \(O^+\)-\(O_2\) collision frequency

`vop_n2`: \(O^+\)-\(N_2\) collision frequency

`vop_he`: \(O^+\)-\(He\) collision frequency

`vo2p_o`: \(O_2^+\)-\(O\) collision frequency

`vo2p_o2`: \(O_2^+\)-\(O_2\) collision frequency

`vo2p_n2`: \(O_2^+\)-\(N_2\) collision frequency

`vo2p_he`: \(O_2^+\)-\(He\) collision frequency

`vnop_o`: \(NO^+\)-\(O\) collision frequency

`vnop_o2`: \(NO^+\)-\(O_2\) collision frequency

`vnop_n2`: \(NO^+\)-\(N_2\) collision frequency

`vnop_he`: \(NO^+\)-\(He\) collision frequency

`vnp_o`: \(N^+\)-\(O\) collision frequency

`vnp_o2`: \(N^+\)-\(O_2\) collision frequency

`vnp_n2`: \(N^+\)-\(N_2\) collision frequency

`vnp_he`: \(N^+\)-\(He\) collision frequency

`Ti`: ion temperature in \(K\)

`Tn`: neutral temperature in \(K\)



_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`qDTi_n`: heat transfer rate between ions and neutrals in \(W/m^{3}\)

`qDTop_n`: heat transfer rate between neutrals and O+ in \(W/m^{3}\)

`qDTo2p_n`: heat transfer rate between neutrals and O2+ in \(W/m^{3}\)

`qDTnop_n`: heat transfer rate between neutrals and O+ in \(W/m^{3}\)

`qDTnp_n`: heat transfer rate between neutrals and N+ in \(W/m^{3}\)

_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**: 
_____________________________________________________________________________________________________________________

Killeen, T., Hays, P., Carignan, G., Heelis, R., Hanson, W., Spencer, N., et al. (1984). Ion-neutral coupling
in the high-latitude f region: Evaluation of ion heating terms from dynamics explorer 2. Journal of
Geophysical Research: Space Physics 89, 7495–7508
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import const

def heat_transfer_in(NOp,NO2p,NNOp,Nplus,vop_o,vop_o2,vop_n2,vop_he,vo2p_o,vo2p_o2,vo2p_n2,vo2p_he,
                      vnop_o,vnop_o2,vnop_n2,vnop_he,vnp_o,vnp_o2,vnp_n2,vnp_he,Ti,Tn):
#     Te_op=(me*Ti+MO*Te)/(MO+me)
#     mu_eop=(me*MO)/(me+MO)
#     ue_op=np.sqrt((vi_op_starx-ve_starx)**2+(vi_op_stary-ve_stary)**2+(vi_op_starz-ve_starz)**2)
#     eps_eop=ue_op/np.sqrt(2*boltzmann_si*Te_op/mu_eop)
#     Psi_eop=np.exp(-eps_eop**2)
#     Phi_eop= ((3*np.sqrt(np.pi))/4)*((erf(eps_eop))/(eps_eop**3))-1.5*(eps_eop**(-2))*np.exp(-eps_eop**2)

# #                     qDTe_opf=3*Necm*(10 ** 6)*boltzmann_si*ve_op*(me/(me+MO))*(Te-Ti)*Psi_eop+\
# #                             (Necm*(10 ** 6)*ve_op*(me*MO/(me+MO)))*Phi_eop

    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)

    qDTop_o=3*NOp*(10 ** 6)*const.boltzmann_si*vop_o*(MO/(MO+MO))*(Ti-Tn)
    qDTop_o2=3*NOp*(10 ** 6)*const.boltzmann_si*vop_o2*(MO/(MO2+MO))*(Ti-Tn)
    qDTop_n2=3*NOp*(10 ** 6)*const.boltzmann_si*vop_n2*(MO/(MN2+MO))*(Ti-Tn)
    qDTop_he=3*NOp*(10 ** 6)*const.boltzmann_si*vop_he*(MO/(MHE+MO))*(Ti-Tn)
    qDTo2p_o=3*NO2p*(10 ** 6)*const.boltzmann_si*vo2p_o*(MO2/(MO+MO2))*(Ti-Tn)
    qDTo2p_o2=3*NO2p*(10 ** 6)*const.boltzmann_si*vo2p_o2*(MO2/(MO2+MO2))*(Ti-Tn)
    qDTo2p_n2=3*NO2p*(10 ** 6)*const.boltzmann_si*vo2p_n2*(MO2/(MN2+MO2))*(Ti-Tn)
    qDTo2p_he=3*NO2p*(10 ** 6)*const.boltzmann_si*vo2p_he*(MO2/(MHE+MO2))*(Ti-Tn)
    qDTnop_o=3*NNOp*(10 ** 6)*const.boltzmann_si*vnop_o*(MNO/(MO+MNO))*(Ti-Tn)
    qDTnop_o2=3*NNOp*(10 ** 6)*const.boltzmann_si*vnop_o2*(MNO/(MO2+MNO))*(Ti-Tn)
    qDTnop_n2=3*NNOp*(10 ** 6)*const.boltzmann_si*vnop_n2*(MNO/(MN2+MNO))*(Ti-Tn)
    qDTnop_he=3*NNOp*(10 ** 6)*const.boltzmann_si*vnop_he*(MNO/(MHE+MNO))*(Ti-Tn)
    qDTnp_o=3*Nplus*(10 ** 6)*const.boltzmann_si*vnp_o*(MN/(MO+MN))*(Ti-Tn)
    qDTnp_o2=3*Nplus*(10 ** 6)*const.boltzmann_si*vnp_o2*(MN/(MO2+MN))*(Ti-Tn)
    qDTnp_n2=3*Nplus*(10 ** 6)*const.boltzmann_si*vnp_n2*(MN/(MN2+MN))*(Ti-Tn)
    qDTnp_he=3*Nplus*(10 ** 6)*const.boltzmann_si*vnp_he*(MN/(MHE+MN))*(Ti-Tn)

    qDTop_n=qDTop_o+qDTop_o2+qDTop_n2+qDTop_he
    qDTo2p_n=qDTo2p_o+qDTo2p_o2+qDTo2p_n2+qDTo2p_he
    qDTnop_n=qDTnop_o+qDTnop_o2+qDTnop_n2+qDTnop_he
    qDTnp_n=qDTnp_o+qDTnp_o2+qDTnp_n2+qDTnp_he

    qDTi_n=qDTop_n+qDTo2p_n+qDTnop_n+qDTnp_n
    
    return qDTi_n,qDTop_n,qDTo2p_n,qDTnop_n,qDTnp_n