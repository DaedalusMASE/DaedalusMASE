"""
sub_Heating_Sources.heat_transfer_en_elastic_rees

**Description**:
_____________________________________________________________________________________________________________________

Calculate heating rate due to electron neutral collisions in \(W/m^{3}\) according to Rees (1989)

$$L_{eN_2}=(1.77 \\times 10^{-19} N_e N_{N_2} T_e (1-1.21\\times 10^{-4} T_e) (T_e-T_n)) 1.60217662 \\times 10^{-13}$$

$$L_{eO_2}=(1.21 \\times 10^{-18} N_e N_{O_2} \\sqrt{T_e} (1-3\\times 10^{-2} \\sqrt{T_e}) (T_e-T_n)) 1.60217662 \\times 10^{-13}$$

$$L_{eO}=(3.74 \\times 10^{-18} N_e N_{O} \\sqrt{T_e} (T_e-T_n)) 1.60217662 \\times 10^{-13}$$

$$L_{eHe}=(2.46 \\times 10^{-17} N_e N_{He} \\sqrt{T_e} (T_e-T_n)) 1.60217662 \\times 10^{-13}$$

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

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`qDTe_n`: heating rate due to electron neutral collisions in \(W/m^{3}\)

`qDTe_of`: heating rate due to electron-O collisions in \(W/m^{3}\)

`qDTe_o2f`: heating rate due to electron-O2 collisions in \(W/m^{3}\)

`qDTe_n2f`: heating rate due to electron-N2 collisions in \(W/m^{3}\)

`qDTe_hef`: heating rate due to electron-He collisions in \(W/m^{3}\)


_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**: 
_____________________________________________________________________________________________________________________

Rees, M. H. (1989). Physics and chemistry of the upper atmosphere. Cambridge University Press.
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""
from daedalusmase_derived_products.mod_tiegcm_utils import const
import numpy as np

def heat_transfer_en_elastic_rees(Necm,NN2,NO2,NO,helium_f,Te,Tn):

    #Rees and Roble
    L_eN2_elast=(1.77*10**(-19)*Necm*NN2*Te*(1-1.21*10**(-4)*Te)*(Te-Tn))*1.60217662*10**(-13) #W/m^3
    L_eO2_elast=(1.21*10**(-18)*Necm*NO2*np.sqrt(Te)*(1+3.6*10**(-2)*np.sqrt(Te))*(Te-Tn))*1.60217662*10**(-13) #W/m^3
    L_eO_elast=(3.74*10**(-18)*Necm*NO*np.sqrt(Te)*(Te-Tn))*1.60217662*10**(-13) #W/m^3
    L_eHe_elast=(2.46*10**(-17)*Necm*helium_f*np.sqrt(Te)*(Te-Tn))*1.60217662*10**(-13) #W/m^3

    Len_rees=L_eN2_elast+L_eO2_elast+L_eO_elast+L_eHe_elast

    return Len_rees, L_eN2_elast, L_eO2_elast, L_eO_elast, L_eHe_elast   
    