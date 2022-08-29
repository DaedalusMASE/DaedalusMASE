"""
**sub_heating_sources.i_i_collision_freqs**

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-ion collision frequencies
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`NOp`: \(O^+\) density in \(cm^{-3}\)

`NO2p`: \(O_2^+\) density in \(cm^{-3}\)

`NNOp`: \(NO^+\) density in \(cm^{-3}\)

`Nplus`: \(N^+\) density in \(cm^{-3}\)

`Ti`: Ion temperature in K

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`vop_op`: \(O^+-O^+\) collision frequency

`vop_o2p`: \(O^+-O_2^+\) collision frequency

`vop_nop`: \(O^+-NO^+\) collision frequency

`vop_np`: \(O^+-N^+\) collision frequency

`vo2p_op`: \(O_2^+-O^+\) collision frequency

`vo2p_o2p`: \(O_2^+-O_2^+\) collision frequency

`vo2p_nop`: \(O_2^+-NO^+\) collision frequency

`vo2p_np`: \(O_2^+-N^+\) collision frequency

`vnop_op`: \(NO^+-O^+\) collision frequency

`vnop_o2p`: \(NO^+-O_2^+\) collision frequency

`vnop_nop`: \(NO^+-NO^+\) collision frequency

`vnop_np`: \(NO^+-N^+\) collision frequency

`vnp_op`: \(N^+-O^+\) collision frequency

`vnp_o2p`: \(N^+-O_2^+\) collision frequency

`vnp_nop`: \(N^+-NO^+\) collision frequency

`vnp_np`: \(N^+-N^+\) collision frequency


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

def i_i_collision_freqs(NOp,NO2p,NNOp,Nplus,Ti):
    vop_op=0.22*(NOp/(Ti**1.5))
    vop_o2p=0.26*(NO2p/(Ti**1.5))
    vop_nop=0.26*(NNOp/(Ti**1.5))
    vop_np=0.22*(Nplus/(Ti**1.5))
    vo2p_op=0.13*(NOp/(Ti**1.5))
    vo2p_o2p=0.16*(NO2p/(Ti**1.5))
    vo2p_nop=0.16*(NNOp/(Ti**1.5))
    vo2p_np=0.12*(Nplus/(Ti**1.5))     
    vnop_op=0.14*(NOp/(Ti**1.5))
    vnop_o2p=0.17*(NO2p/(Ti**1.5))
    vnop_nop=0.16*(NNOp/(Ti**1.5))
    vnop_np=0.13*(Nplus/(Ti**1.5))
    vnp_op=0.25*(NOp/(Ti**1.5))
    vnp_o2p=0.28*(NO2p/(Ti**1.5))
    vnp_nop=0.28*(NNOp/(Ti**1.5))
    vnp_np=0.24*(Nplus/(Ti**1.5))

    
    vi_op=(vop_op+vop_o2p+vop_nop+vop_np)/4
    vi_o2p=(vo2p_op+vo2p_o2p+vo2p_nop+vo2p_np)/4
    vi_nop=(vnop_op+vnop_o2p+vnop_nop+vnop_np)/4
    vi_np=(vnp_op+vnp_o2p+vnp_nop+vnp_np)/4
    vi_i=(vi_op+vi_o2p+vi_np+vi_nop)/4

    return vop_op,vop_o2p,vop_nop,vop_np,vo2p_op,vo2p_o2p,vo2p_nop,vo2p_np,vnop_op,vnop_o2p,vnop_nop,vnop_np,vnp_op,vnp_o2p,vnp_nop,vnp_np

