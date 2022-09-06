"""
sub_Heating_Sources.vi_vi_relative

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-ion relative velocities
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

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

`u_op_o2p`: \(O^+\)- \(O_2^+\) relative velocity vector in \(m/s\) [ENU]

`u_op_nop`: \(O^+\)- \(NO^+\) relative velocity vector in \(m/s\) [ENU]

`u_op_np`: \(O^+\)- \(N^+\) relative velocity vector in \(m/s\) [ENU]

`u_o2p_nop`: \(O_2^+\)- \(NO^+\) relative velocity vector in \(m/s\) [ENU]

`u_np_o2p`: \(N^+\)- \(O_2^+\) relative velocity vector in \(m/s\) [ENU]

`uop_o2p_mag`: \(O^+\)- \(O_2^+\) relative velocity magnitude in \(m/s\)

`uop_nop_mag`: \(O^+\)- \(NO^+\) relative velocity magnitude in \(m/s\)

`uop_np_mag`: \(O^+\)- \(N^+\) relative velocity magnitude in \(m/s\)

`uo2p_nop_mag`: \(O_2^+\)- \(NO^+\) relative velocity magnitude in \(m/s\)

`unp_o2p_mag`: \(N^+\)- \(O_2^+\) relative velocity magnitude in \(m/s\)

`unop_np_mag`: \(NO^+\)- \(N^+\) relative velocity magnitude in \(m/s\)
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""

import numpy as np

def vi_vi_relative(vi_op_starx,vi_op_stary,vi_op_starz,vi_o2p_starx,vi_o2p_stary,vi_o2p_starz,vi_nop_starx,vi_nop_stary,vi_nop_starz,vi_np_starx,vi_np_stary,vi_np_starz):
    
    u_op_o2p=[vi_op_starx-vi_o2p_starx,vi_op_stary-vi_o2p_stary,vi_op_starz-vi_o2p_starz]
    u_op_nop=[vi_op_starx-vi_nop_starx,vi_op_stary-vi_nop_stary,vi_op_starz-vi_nop_starz]
    u_op_np=[vi_op_starx-vi_np_starx,vi_op_stary-vi_np_stary,vi_op_starz-vi_np_starz]
    u_o2p_nop=[vi_o2p_starx-vi_nop_starx,vi_o2p_stary-vi_nop_stary,vi_o2p_starz-vi_nop_starz]
    u_np_o2p=[vi_np_starx-vi_o2p_starx,vi_np_stary-vi_o2p_stary,vi_np_starz-vi_o2p_starz]
    u_nop_np=[vi_nop_starx-vi_np_starx,vi_nop_stary-vi_np_stary,vi_nop_starz-vi_np_starz]
    uop_o2p_mag=np.sqrt(u_op_o2p[0]*u_op_o2p[0]+u_op_o2p[1]*u_op_o2p[1]+u_op_o2p[2]*u_op_o2p[2])
    uop_nop_mag=np.sqrt(u_op_nop[0]*u_op_nop[0]+u_op_nop[1]*u_op_nop[1]+u_op_nop[2]*u_op_nop[2])
    uop_np_mag=np.sqrt(u_op_np[0]*u_op_np[0]+u_op_np[1]*u_op_np[1]+u_op_np[2]*u_op_np[2])
    uo2p_nop_mag=np.sqrt(u_o2p_nop[0]*u_o2p_nop[0]+u_o2p_nop[1]*u_o2p_nop[1]+u_o2p_nop[2]*u_o2p_nop[2])
    unp_o2p_mag=np.sqrt(u_np_o2p[0]*u_np_o2p[0]+u_np_o2p[1]*u_np_o2p[1]+u_np_o2p[2]*u_np_o2p[2])
    unop_np_mag=np.sqrt(u_nop_np[0]*u_nop_np[0]+u_nop_np[1]*u_nop_np[1]+u_nop_np[2]*u_nop_np[2])
    
    return u_op_o2p,u_op_nop,u_op_np,u_o2p_nop,u_np_o2p,uop_o2p_mag,uop_nop_mag,uop_np_mag,uo2p_nop_mag,unp_o2p_mag,unop_np_mag