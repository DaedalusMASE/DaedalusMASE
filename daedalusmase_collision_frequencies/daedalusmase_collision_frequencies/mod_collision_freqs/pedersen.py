"""
**sub_heating_sources.pedersen**

**Description**:
_____________________________________________________________________________________________________________________

Calculate pedersen conductivity
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


def pedersen(bnorm,ne,nop,no2p,nnop,ven,vop,vo2p,vnop):

    MO=const.mO/(const.NA*1000)  # Atomic oxygen mass in kg
    MO2=(2*const.mO)/(const.NA*1000) # Molecular oxygen mass in kg
    MNO=(const.mNO)/(const.NA*1000) #Nitric oxide mass in kg                    
    
    fac=const.electron/bnorm

    omegae=(const.electron*bnorm)/const.me
    omegaop=(const.electron*bnorm)/MO
    omegao2p=(const.electron*bnorm)/MO2
    omeganop=(const.electron*bnorm)/MNO

    ke=omegae/ven
    kop=omegaop/vop
    ko2p=omegao2p/vo2p
    knop=omeganop/vnop

    # sigmaped_e=fac*ne*omegae*ven/(omegae*omegae+ven*ven)
    # sigmaped_op=fac*nop*omegaop*vop/(omegaop*omegaop+vop*vop)
    # sigmaped_o2p=fac*no2p*omegao2p*vo2p/(omegao2p*omegao2p+vo2p*vo2p)
    # sigmaped_nop=fac*nnop*omeganop*vnop/(omeganop*omeganop+vnop*vnop)

    sigmaped_e=fac*ne*ke/(1+ke*ke)
    sigmaped_op=fac*nop*kop/(1+kop*kop)
    sigmaped_o2p=fac*no2p*ko2p/(1+ko2p*ko2p)
    sigmaped_nop=fac*nnop*knop/(1+knop*knop)

    sigmaped=sigmaped_e+sigmaped_op+sigmaped_o2p+sigmaped_nop

    return sigmaped,sigmaped_e,sigmaped_op,sigmaped_o2p,sigmaped_nop



