"""
sub_Heating_Sources.vi_vi_relative

**Description**:
_____________________________________________________________________________________________________________________

Calculate ion-ion relative velocities
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

vi_op_starx:

vi_op_stary:

vi_op_starz:

vi_o2p_starx:

vi_o2p_stary:

vi_o2p_starz:

vi_nop_starx:

vi_nop_stary:

vi_nop_starz:

vi_np_starx:

vi_np_stary:

vi_np_starz
_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

u_op_o2p:

u_op_nop:

u_op_np:

u_o2p_nop:

u_np_o2p:

uop_o2p_mag:

uop_nop_mag:

uop_np_mag:

uo2p_nop_mag:

unp_o2p_mag:

unop_np_mag
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