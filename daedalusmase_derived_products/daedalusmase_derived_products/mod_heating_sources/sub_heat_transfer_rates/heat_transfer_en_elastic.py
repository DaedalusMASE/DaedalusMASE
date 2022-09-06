"""
sub_Heating_Sources.heat_transfer_en_elastic

**Description**:
_____________________________________________________________________________________________________________________

Calculate heating rate due to electron neutral collisions in \(W/m^{3}\)

$$q_{\\Delta T_{en}}=N_e \\nu_{en} \\frac{m_e}{m_e+m_n} 3 k_B \\Big(T_e - T_n \\Big)$$
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________


`Necm`: electron density in \(cm^{-3}\)

`NN2`: \(N_2\) density in \(cm^{-3}\)

`NO2`: \(O_2\) density in \(cm^{-3}\)

`NO`: \(O\) density in \(cm^{-3}\)

`helium_f`: \(He\) density in \(cm^{-3}\)

`Te`: electron temperature in K

`Tn`: neutral temperature in K

`ve_o`: \(e\)-\(O\) collision frequency

`ve_o2`: \(e\)-\(O_2\) collision frequency

`ve_n2`: \(e\)-\(N_2\) collision frequency

`ve_he`: \(e\)-\(He\) collision frequency

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`qDTe_n`: heating rate due to electron-neutral collisions in \(W/m^{3}\)

`qDTe_of`: heating rate due to \(e\)-\(O\) collisions in \(W/m^{3}\)

`qDTe_o2f`: heating rate due to \(e\)-\(O_2\) collisions in \(W/m^{3}\)

`qDTe_n2f`: heating rate due to \(e\)-\(N_2\) collisions in \(W/m^{3}\)

`qDTe_hef`: heating rate due to \(e\)-\(He\) collisions in \(W/m^{3}\)


_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**: 
_____________________________________________________________________________________________________________________

Schunk, R. and Nagy, A. (2009). Ionospheres: physics, plasma physics, and chemistry (Cambridge
university press)
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""
from daedalusmase_derived_products.mod_tiegcm_utils import const

def heat_transfer_en_elastic(Necm,NN2,NO2,NO,helium_f,Te,Tn,ve_o,ve_o2,ve_n2,ve_he):
    #Rees and Roble

    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    MN2=28/(const.NA*1000)   #Nitrogen mass in kg
    MHe=4/(const.NA*1000)
    MN=14/(const.NA*1000)
    MHE=4/(const.NA*1000)
    
    #Schunk and Nagy
    qDTe_of=3*Necm*(10 ** 6)*const.boltzmann_si*ve_o*(const.me/(const.me+MO))*(Te-Tn) #W/m^3
    qDTe_o2f=3*Necm*(10 ** 6)*const.boltzmann_si*ve_o2*(const.me/(const.me+MO2))*(Te-Tn) #W/m^3
    qDTe_n2f=3*Necm*(10 ** 6)*const.boltzmann_si*ve_n2*(const.me/(const.me+MN2))*(Te-Tn) #W/m^3
    qDTe_hef=3*Necm*(10 ** 6)*const.boltzmann_si*ve_he*(const.me/(const.me+MHE))*(Te-Tn) #W/m^3

    qDTe_n=qDTe_of+qDTe_o2f+qDTe_n2f+qDTe_hef

    return qDTe_n,qDTe_of,qDTe_o2f,qDTe_n2f,qDTe_hef   
    