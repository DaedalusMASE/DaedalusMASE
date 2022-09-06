"""
sub_Heating_Sources.vi_ve_relative

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-electron relative velocities
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

ve_starx: electron velocity in \(m/s\) [east]

ve_stary: electron velocity in \(m/s\) [north]

ve_starz: electron velocity in \(m/s\) [up]

`vi_op_starx`: \(O^+\) velocity in \(m/s\) [east]

`vi_op_stary`: \(O^+\) velocity in \(m/s\) [north]

`vi_op_starz`: \(O^+\) velocity in \(m/s\) [up]

`vi_o2p_starx`: \(O_2^+\) velocity in \(m/s\) [east]

`vi_o2p_stary`: \(O_2^+\) velocity in \(m/s\) [north]

`vi_o2p_starz`: \(O_2^+\) velocity in \(m/s\) [up]

`vi_nop_starx`: \(NO^+\) velocity in \(m/s\) [east]

`vi_nop_stary`: \(NO^+\) velocity in \(m/s\) [north]

`vi_nop_starz`: \(NO^+\) velocity in \(m/s\) [up]

`vi_np_starx`: \(N^+\) velocity in \(m/s\) [east]

`vi_np_stary`: \(N^+\) velocity in \(m/s\) [north]

`vi_np_starz`: \(N^+\) velocity in \(m/s\) [up]
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`ue_uop`: electron- \(O^+\) relative velocity vector in \(m/s\) [ENU]

`ue_uo2p`: electron- \(O_2^+\) relative velocity vector in \(m/s\) [ENU]

`ue_unop`: electron- \(NO^+\) relative velocity vector in \(m/s\) [ENU]

`ue_unp`: electron- \(N^+\) relative velocity vector in \(m/s\) [ENU]

`ue_uop_mag`: electron- \(O^+\) relative velocity magnitude in \(m/s\)

`ue_uo2p_mag`: electron- \(O_2^+\) relative velocity magnitude in \(m/s\)

`ue_unop_mag`: electron- \(NO^+\) relative velocity magnitude in \(m/s\)

`ue_unp_mag`: electron- \(N^+\) relative velocity magnitude in \(m/s\)
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np

def vi_ve_relative(ve_starx,ve_stary,ve_starz,vi_op_starx,vi_op_stary,vi_op_starz,vi_o2p_starx,vi_o2p_stary,vi_o2p_starz,vi_nop_starx,vi_nop_stary,vi_nop_starz,vi_np_starx,vi_np_stary,vi_np_starz):
    ue_uop=[ve_starx-vi_op_starx,ve_stary-vi_op_stary,ve_starz-vi_op_starz]
    ue_uo2p=[ve_starx-vi_o2p_starx,ve_stary-vi_o2p_stary,ve_starz-vi_o2p_starz]
    ue_unop=[ve_starx-vi_nop_starx,ve_stary-vi_nop_stary,ve_starz-vi_nop_starz]
    ue_unp=[ve_starx-vi_np_starx,ve_stary-vi_np_stary,ve_starz-vi_np_starz]
    ue_uop_mag=np.sqrt(ue_uop[0]*ue_uop[0]+ue_uop[1]*ue_uop[1]+ue_uop[2]*ue_uop[2])
    ue_uo2p_mag=np.sqrt(ue_uo2p[0]*ue_uo2p[0]+ue_uo2p[1]*ue_uo2p[1]+ue_uo2p[2]*ue_uo2p[2])
    ue_unop_mag=np.sqrt(ue_unop[0]*ue_unop[0]+ue_unop[1]*ue_unop[1]+ue_unop[2]*ue_unop[2])
    ue_unp_mag=np.sqrt(ue_unp[0]*ue_unp[0]+ue_unp[1]*ue_unp[1]+ue_unp[2]*ue_unp[2])
    
    return ue_uop,ue_uo2p,ue_unop,ue_unp,ue_uop_mag,ue_uo2p_mag,ue_unop_mag,ue_unp_mag

