"""
environment_mod.allocations

**Description**:
_____________________________________________________________________________________________________________________

File with all the needed allocations for the simulations
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

"""
import numpy as np

#1D allocations
zg_1D=[]
lat_1D=[]
lon_1D=[]
Ti_1D=[]
Te_1D=[]
Tn_1D=[]
Ne_1D=[]
NOp_1D=[]
NO2p_1D=[]
Np_1D=[]
NNOp_1D=[]
NO_1D=[]
NO2_1D=[]
NN2_1D=[]
NHe_1D=[]
Be_1D=[]
Bn_1D=[]
Bu_1D=[]
Bmag_1D=[]
Une_1D=[]
Unn_1D=[]
Unu_1D=[]
Uie_1D=[]
Uin_1D=[]
Uiu_1D=[]
Ee_1D=[]
En_1D=[]
Eu_1D=[]
omega_e_1D=[] 
omega_op_1D=[]
omega_o2p_1D=[]
omega_nop_1D=[]
omega_np_1D=[]
ve_i_1D=[] 
ve_op_1D=[]
ve_o2p_1D=[]
ve_nop_1D=[]
ve_np_1D=[]
ven_1D=[]
ve_n2_1D=[]
ve_o_1D=[]
ve_o2_1D=[]
ve_he_1D=[]
vi_i_1D=[]
vi_op_1D=[]
vi_o2p_1D=[]
vi_nop_1D=[]
vi_np_1D=[]
vin_1D=[]
vop_o_1D=[]
vop_o2_1D=[]
vop_n2_1D=[]
vop_he_1D=[]
vo2p_o_1D=[]
vo2p_o2_1D=[]
vo2p_n2_1D=[]
vo2p_he_1D=[]
vnp_o_1D=[]
vnp_o2_1D=[]
vnp_n2_1D=[]
vnp_he_1D=[]
vnop_o_1D=[]
vnop_o2_1D=[]
vnop_n2_1D=[]
vnop_he_1D=[]
pedersen_1D=[]
hall_1D=[]
parallel_1D=[]                
                    
qDTi_n_1D=[]
qDTop_n_1D=[]
qDTo2p_n_1D=[]
qDTnop_n_1D=[]
qDTnp_n_1D=[]
qFop_o_1D=[]
qFop_o2_1D=[]
qFop_n2_1D=[]
qFop_he_1D=[]
qFo2p_o_1D=[]
qFo2p_o2_1D=[]
qFo2p_n2_1D=[]
qFo2p_he_1D=[]
qFnop_o_1D=[]
qFnop_o2_1D=[]
qFnop_n2_1D=[]
qFnop_he_1D=[]
qFnp_o_1D=[]
qFnp_o2_1D=[]
qFnp_n2_1D=[]
qFnp_he_1D=[]
qFop_n_1D=[]
qFo2p_n_1D=[]
qFnop_n_1D=[]
qFnp_n_1D=[]
qFi_n_1D=[]
qFop_e_1D=[]
qFo2p_e_1D=[]
qFnop_e_1D=[]
qFnp_e_1D=[]
qFe_i_1D=[]   
qFop_o2p_1D=[]
qFop_nop_1D=[]
qFop_np_1D=[]
qFo2p_nop_1D=[]
qFo2p_np_1D=[]
qFnop_np_1D=[]
qFi_i_1D=[]
L_eN2_elast_rees_1D=[]
L_eO2_elast_rees_1D=[]
L_eO_elast_rees_1D=[]
L_eHe_elast_rees_1D=[]
L_eN2_elast_schunk_1D=[]
L_eO2_elast_schunk_1D=[]
L_eO_elast_schunk_1D=[]
L_eHe_elast_schunk_1D=[]
L_en_schunk_1D=[]
L_en_rees_1D=[]
qDTe_op_1D=[]
qDTe_o2p_1D=[]
qDTe_nop_1D=[]
qDTe_np_1D=[]
qDTe_i_1D=[] 
Le_N2_rot_schunk_1D=[]
Le_N2_rot_rees_1D=[]
Le_N2_rot_tiegcm_1D=[]
Le_O2_rot_schunk_1D=[]
Le_O2_rot_rees_1D=[]
Le_O2_rot_tiegcm_1D=[]
Le_N2_vib_schunk_1D=[]
Le_N2_vib_rees_1D=[]
Le_N2_vib_tiegcm_1D=[]
Le_O2_vib_schunk_1D=[]
Le_O2_vib_rees_1D=[]
Le_O2_vib_tiegcm_1D=[]
Le_O_fine_schunk_1D=[]
Le_O_fine_rees_1D=[]
Le_O_fine_tiegcm_1D=[]
wind_heating_1D=[]                    
convection_heating_1D=[]
ohmic_1D=[]
ohmic_mass_1D=[]
joule_1D=[]
joule_op_1D=[]
joule_o2p_1D=[]
joule_nop_1D=[]
frictional_1D=[]
frictional_op_1D=[]
frictional_o2p_1D=[]
frictional_nop_1D=[]
jpede_1D=[]
jpedn_1D=[]
jpedu_1D=[]
jhalle_1D=[]
jhalln_1D=[]
jhallu_1D=[]
jperpe_1D=[]
jperpn_1D=[]
jperpu_1D=[]
mech_power_1D=[]
ion_vele_1D=[]
ion_veln_1D=[]
ion_velu_1D=[]
cross_in_1D=[]
cross_op_1D=[]
cross_o2p_1D=[]
cross_nop_1D=[]             
maplat=np.zeros((72),order='F')
maplon=np.zeros((144),order='F')
maptime=np.zeros((24),order='F')

#2D allocations

zg_2D=np.zeros((72, 144),order='F')
lat_2D=np.zeros((72, 144),order='F')
lon_2D=np.zeros((72, 144),order='F')
Ti_2D=np.zeros((72, 144),order='F')
Te_2D=np.zeros((72, 144),order='F')
Tn_2D=np.zeros((72, 144),order='F')
Ne_2D=np.zeros((72, 144),order='F')
NOp_2D=np.zeros((72, 144),order='F')
NO2p_2D=np.zeros((72, 144),order='F')
Np_2D=np.zeros((72, 144),order='F')
NNOp_2D=np.zeros((72, 144),order='F')
NO_2D=np.zeros((72, 144),order='F')
NO2_2D=np.zeros((72, 144),order='F')
NN2_2D=np.zeros((72, 144),order='F')
NHe_2D=np.zeros((72, 144),order='F')
Be_2D=np.zeros((72, 144),order='F')
Bn_2D=np.zeros((72, 144),order='F')
Bu_2D=np.zeros((72, 144),order='F')
Bmag_2D=np.zeros((72, 144),order='F')
Une_2D=np.zeros((72, 144),order='F')
Unn_2D=np.zeros((72, 144),order='F')
Unu_2D=np.zeros((72, 144),order='F')
Uie_2D=np.zeros((72, 144),order='F')
Uin_2D=np.zeros((72, 144),order='F')
Uiu_2D=np.zeros((72, 144),order='F')
Ee_2D=np.zeros((72, 144),order='F')
En_2D=np.zeros((72, 144),order='F')
Eu_2D=np.zeros((72, 144),order='F')
omega_e_2D=np.zeros((72, 144),order='F') 
omega_op_2D=np.zeros((72, 144),order='F')
omega_o2p_2D=np.zeros((72, 144),order='F')
omega_nop_2D=np.zeros((72, 144),order='F')
omega_np_2D=np.zeros((72, 144),order='F')
ve_i_2D=np.zeros((72, 144),order='F') 
ve_op_2D=np.zeros((72, 144),order='F')
ve_o2p_2D=np.zeros((72, 144),order='F')
ve_nop_2D=np.zeros((72, 144),order='F')
ve_np_2D=np.zeros((72, 144),order='F')
ven_2D=np.zeros((72, 144),order='F')
ve_n2_2D=np.zeros((72, 144),order='F')
ve_o_2D=np.zeros((72, 144),order='F')
ve_o2_2D=np.zeros((72, 144),order='F')
ve_he_2D=np.zeros((72, 144),order='F')
vi_i_2D=np.zeros((72, 144),order='F')
vi_op_2D=np.zeros((72, 144),order='F')
vi_o2p_2D=np.zeros((72, 144),order='F')
vi_nop_2D=np.zeros((72, 144),order='F')
vi_np_2D=np.zeros((72, 144),order='F')
vin_2D=np.zeros((72, 144),order='F')
vop_o_2D=np.zeros((72, 144),order='F')
vop_o2_2D=np.zeros((72, 144),order='F')
vop_n2_2D=np.zeros((72, 144),order='F')
vop_he_2D=np.zeros((72, 144),order='F')
vo2p_o_2D=np.zeros((72, 144),order='F')
vo2p_o2_2D=np.zeros((72, 144),order='F')
vo2p_n2_2D=np.zeros((72, 144),order='F')
vo2p_he_2D=np.zeros((72, 144),order='F')
vnp_o_2D=np.zeros((72, 144),order='F')
vnp_o2_2D=np.zeros((72, 144),order='F')
vnp_n2_2D=np.zeros((72, 144),order='F')
vnp_he_2D=np.zeros((72, 144),order='F')
vnop_o_2D=np.zeros((72, 144),order='F')
vnop_o2_2D=np.zeros((72, 144),order='F')
vnop_n2_2D=np.zeros((72, 144),order='F')
vnop_he_2D=np.zeros((72, 144),order='F')
pedersen_2D=np.zeros((72, 144),order='F')
hall_2D=np.zeros((72, 144),order='F')
parallel_2D=np.zeros((72, 144),order='F')                
                    
qDTi_n_2D=np.zeros((72, 144),order='F')
qDTop_n_2D=np.zeros((72, 144),order='F')
qDTo2p_n_2D=np.zeros((72, 144),order='F')
qDTnop_n_2D=np.zeros((72, 144),order='F')
qDTnp_n_2D=np.zeros((72, 144),order='F')
qFop_o_2D=np.zeros((72, 144),order='F')
qFop_o2_2D=np.zeros((72, 144),order='F')
qFop_n2_2D=np.zeros((72, 144),order='F')
qFop_he_2D=np.zeros((72, 144),order='F')
qFo2p_o_2D=np.zeros((72, 144),order='F')
qFo2p_o2_2D=np.zeros((72, 144),order='F')
qFo2p_n2_2D=np.zeros((72, 144),order='F')
qFo2p_he_2D=np.zeros((72, 144),order='F')
qFnop_o_2D=np.zeros((72, 144),order='F')
qFnop_o2_2D=np.zeros((72, 144),order='F')
qFnop_n2_2D=np.zeros((72, 144),order='F')
qFnop_he_2D=np.zeros((72, 144),order='F')
qFnp_o_2D=np.zeros((72, 144),order='F')
qFnp_o2_2D=np.zeros((72, 144),order='F')
qFnp_n2_2D=np.zeros((72, 144),order='F')
qFnp_he_2D=np.zeros((72, 144),order='F')
qFop_n_2D=np.zeros((72, 144),order='F')
qFo2p_n_2D=np.zeros((72, 144),order='F')
qFnop_n_2D=np.zeros((72, 144),order='F')
qFnp_n_2D=np.zeros((72, 144),order='F')
qFi_n_2D=np.zeros((72, 144),order='F')
qFop_e_2D=np.zeros((72, 144),order='F')
qFo2p_e_2D=np.zeros((72, 144),order='F')
qFnop_e_2D=np.zeros((72, 144),order='F')
qFnp_e_2D=np.zeros((72, 144),order='F')
qFe_i_2D=np.zeros((72, 144),order='F')   
qFop_o2p_2D=np.zeros((72, 144),order='F')
qFop_nop_2D=np.zeros((72, 144),order='F')
qFop_np_2D=np.zeros((72, 144),order='F')
qFo2p_nop_2D=np.zeros((72, 144),order='F')
qFo2p_np_2D=np.zeros((72, 144),order='F')
qFnop_np_2D=np.zeros((72, 144),order='F')
qFi_i_2D=np.zeros((72, 144),order='F')
L_eN2_elast_rees_2D=np.zeros((72, 144),order='F')
L_eO2_elast_rees_2D=np.zeros((72, 144),order='F')
L_eO_elast_rees_2D=np.zeros((72, 144),order='F')
L_eHe_elast_rees_2D=np.zeros((72, 144),order='F')
L_eN2_elast_schunk_2D=np.zeros((72, 144),order='F')
L_eO2_elast_schunk_2D=np.zeros((72, 144),order='F')
L_eO_elast_schunk_2D=np.zeros((72, 144),order='F')
L_eHe_elast_schunk_2D=np.zeros((72, 144),order='F')
L_en_schunk_2D=np.zeros((72, 144),order='F')
L_en_rees_2D=np.zeros((72, 144),order='F')
qDTe_op_2D=np.zeros((72, 144),order='F')
qDTe_o2p_2D=np.zeros((72, 144),order='F')
qDTe_nop_2D=np.zeros((72, 144),order='F')
qDTe_np_2D=np.zeros((72, 144),order='F')
qDTe_i_2D=np.zeros((72, 144),order='F') 
Le_N2_rot_schunk_2D=np.zeros((72, 144),order='F')
Le_N2_rot_rees_2D=np.zeros((72, 144),order='F')
Le_N2_rot_tiegcm_2D=np.zeros((72, 144),order='F')
Le_O2_rot_schunk_2D=np.zeros((72, 144),order='F')
Le_O2_rot_rees_2D=np.zeros((72, 144),order='F')
Le_O2_rot_tiegcm_2D=np.zeros((72, 144),order='F')
Le_N2_vib_schunk_2D=np.zeros((72, 144),order='F')
Le_N2_vib_rees_2D=np.zeros((72, 144),order='F')
Le_N2_vib_tiegcm_2D=np.zeros((72, 144),order='F')
Le_O2_vib_schunk_2D=np.zeros((72, 144),order='F')
Le_O2_vib_rees_2D=np.zeros((72, 144),order='F')
Le_O2_vib_tiegcm_2D=np.zeros((72, 144),order='F')
Le_O_fine_schunk_2D=np.zeros((72, 144),order='F')
Le_O_fine_rees_2D=np.zeros((72, 144),order='F')
Le_O_fine_tiegcm_2D=np.zeros((72, 144),order='F')
wind_heating_2D=np.zeros((72, 144),order='F')                    
convection_heating_2D=np.zeros((72, 144),order='F')
ohmic_2D=np.zeros((72, 144),order='F')
ohmic_mass_2D=np.zeros((72, 144),order='F')
joule_2D=np.zeros((72, 144),order='F')
joule_op_2D=np.zeros((72, 144),order='F')
joule_o2p_2D=np.zeros((72, 144),order='F')
joule_nop_2D=np.zeros((72, 144),order='F')
frictional_2D=np.zeros((72, 144),order='F')
frictional_op_2D=np.zeros((72, 144),order='F')
frictional_o2p_2D=np.zeros((72, 144),order='F')
frictional_nop_2D=np.zeros((72, 144),order='F')
jpede_2D=np.zeros((72, 144),order='F')
jpedn_2D=np.zeros((72, 144),order='F')
jpedu_2D=np.zeros((72, 144),order='F')
jhalle_2D=np.zeros((72, 144),order='F')
jhalln_2D=np.zeros((72, 144),order='F')
jhallu_2D=np.zeros((72, 144),order='F')
jperpe_2D=np.zeros((72, 144),order='F')
jperpn_2D=np.zeros((72, 144),order='F')
jperpu_2D=np.zeros((72, 144),order='F')
cross_in_2D=np.zeros((72, 144),order='F')
cross_op_2D=np.zeros((72, 144),order='F')
cross_o2p_2D=np.zeros((72, 144),order='F')
cross_nop_2D=np.zeros((72, 144),order='F')
Pot_2D=np.zeros((72, 144),order='F')
mech_power_2D=np.zeros((72, 144),order='F')
J_mag_2D=np.zeros((72, 144),order='F')
vi_mag_2D=np.zeros((72, 144),order='F')
veli_e_2D=np.zeros((72, 144),order='F')
veli_n_2D=np.zeros((72, 144),order='F')
jxbe_2D=np.zeros((72, 144),order='F')
jxbn_2D=np.zeros((72, 144),order='F')
jxbu_2D=np.zeros((72, 144),order='F')

forcing_e_2D=np.zeros((72, 144),order='F')
forcing_n_2D=np.zeros((72, 144),order='F')
forcing_u_2D=np.zeros((72, 144),order='F')

jxb_mag_2D=np.zeros((72, 144),order='F')
#lat_lon allocations
zgl=np.zeros((57, 72),order='F')
latl=np.zeros((57, 72),order='F')
lonl=np.zeros((57, 72),order='F')
Til=np.zeros((57, 72),order='F')
Tel=np.zeros((57, 72),order='F')
Tnl=np.zeros((57, 72),order='F')
Nel=np.zeros((57, 72),order='F')
NOpl=np.zeros((57, 72),order='F')
NO2pl=np.zeros((57, 72),order='F')
Npl=np.zeros((57, 72),order='F')
NNOpl=np.zeros((57, 72),order='F')
NOl=np.zeros((57, 72),order='F')
NO2l=np.zeros((57, 72),order='F')
NN2l=np.zeros((57, 72),order='F')
NHel=np.zeros((57, 72),order='F')
Bel=np.zeros((57, 72),order='F')
Bnl=np.zeros((57, 72),order='F')
Bul=np.zeros((57, 72),order='F')
Bmagl=np.zeros((57, 72),order='F')
Unel=np.zeros((57, 72),order='F')
Unnl=np.zeros((57, 72),order='F')
Unul=np.zeros((57, 72),order='F')
Uiel=np.zeros((57, 72),order='F')
Uinl=np.zeros((57, 72),order='F')
Uiul=np.zeros((57, 72),order='F')
Eel=np.zeros((57, 72),order='F')
Enl=np.zeros((57, 72),order='F')
Eul=np.zeros((57, 72),order='F')
omega_el=np.zeros((57, 72),order='F') 
omega_opl=np.zeros((57, 72),order='F')
omega_o2pl=np.zeros((57, 72),order='F')
omega_nopl=np.zeros((57, 72),order='F')
omega_npl=np.zeros((57, 72),order='F')
ve_il=np.zeros((57, 72),order='F') 
ve_opl=np.zeros((57, 72),order='F')
ve_o2pl=np.zeros((57, 72),order='F')
ve_nopl=np.zeros((57, 72),order='F')
ve_npl=np.zeros((57, 72),order='F')
venl=np.zeros((57, 72),order='F')
ve_n2l=np.zeros((57, 72),order='F')
ve_ol=np.zeros((57, 72),order='F')
ve_o2l=np.zeros((57, 72),order='F')
ve_hel=np.zeros((57, 72),order='F')
vi_il=np.zeros((57, 72),order='F')
vi_opl=np.zeros((57, 72),order='F')
vi_o2pl=np.zeros((57, 72),order='F')
vi_nopl=np.zeros((57, 72),order='F')
vi_npl=np.zeros((57, 72),order='F')
vinl=np.zeros((57, 72),order='F')
vop_ol=np.zeros((57, 72),order='F')
vop_o2l=np.zeros((57, 72),order='F')
vop_n2l=np.zeros((57, 72),order='F')
vop_hel=np.zeros((57, 72),order='F')
vo2p_ol=np.zeros((57, 72),order='F')
vo2p_o2l=np.zeros((57, 72),order='F')
vo2p_n2l=np.zeros((57, 72),order='F')
vo2p_hel=np.zeros((57, 72),order='F')
vnp_ol=np.zeros((57, 72),order='F')
vnp_o2l=np.zeros((57, 72),order='F')
vnp_n2l=np.zeros((57, 72),order='F')
vnp_hel=np.zeros((57, 72),order='F')
vnop_ol=np.zeros((57, 72),order='F')
vnop_o2l=np.zeros((57, 72),order='F')
vnop_n2l=np.zeros((57, 72),order='F')
vnop_hel=np.zeros((57, 72),order='F')
pedersenl=np.zeros((57, 72),order='F')
halll=np.zeros((57, 72),order='F')
parallell=np.zeros((57, 72),order='F')                
                    
qDTi_nl=np.zeros((57, 72),order='F')
qDTop_nl=np.zeros((57, 72),order='F')
qDTo2p_nl=np.zeros((57, 72),order='F')
qDTnop_nl=np.zeros((57, 72),order='F')
qDTnp_nl=np.zeros((57, 72),order='F')
qFop_ol=np.zeros((57, 72),order='F')
qFop_o2l=np.zeros((57, 72),order='F')
qFop_n2l=np.zeros((57, 72),order='F')
qFop_hel=np.zeros((57, 72),order='F')
qFo2p_ol=np.zeros((57, 72),order='F')
qFo2p_o2l=np.zeros((57, 72),order='F')
qFo2p_n2l=np.zeros((57, 72),order='F')
qFo2p_hel=np.zeros((57, 72),order='F')
qFnop_ol=np.zeros((57, 72),order='F')
qFnop_o2l=np.zeros((57, 72),order='F')
qFnop_n2l=np.zeros((57, 72),order='F')
qFnop_hel=np.zeros((57, 72),order='F')
qFnp_ol=np.zeros((57, 72),order='F')
qFnp_o2l=np.zeros((57, 72),order='F')
qFnp_n2l=np.zeros((57, 72),order='F')
qFnp_hel=np.zeros((57, 72),order='F')
qFop_nl=np.zeros((57, 72),order='F')
qFo2p_nl=np.zeros((57, 72),order='F')
qFnop_nl=np.zeros((57, 72),order='F')
qFnp_nl=np.zeros((57, 72),order='F')
qFi_nl=np.zeros((57, 72),order='F')
qFop_el=np.zeros((57, 72),order='F')
qFo2p_el=np.zeros((57, 72),order='F')
qFnop_el=np.zeros((57, 72),order='F')
qFnp_el=np.zeros((57, 72),order='F')
qFe_il=np.zeros((57, 72),order='F')   
qFop_o2pl=np.zeros((57, 72),order='F')
qFop_nopl=np.zeros((57, 72),order='F')
qFop_npl=np.zeros((57, 72),order='F')
qFo2p_nopl=np.zeros((57, 72),order='F')
qFo2p_npl=np.zeros((57, 72),order='F')
qFnop_npl=np.zeros((57, 72),order='F')
qFi_il=np.zeros((57, 72),order='F')
L_eN2_elast_reesl=np.zeros((57, 72),order='F')
L_eO2_elast_reesl=np.zeros((57, 72),order='F')
L_eO_elast_reesl=np.zeros((57, 72),order='F')
L_eHe_elast_reesl=np.zeros((57, 72),order='F')
L_eN2_elast_schunkl=np.zeros((57, 72),order='F')
L_eO2_elast_schunkl=np.zeros((57, 72),order='F')
L_eO_elast_schunkl=np.zeros((57, 72),order='F')
L_eHe_elast_schunkl=np.zeros((57, 72),order='F')
L_en_schunkl=np.zeros((57, 72),order='F')
L_en_reesl=np.zeros((57, 72),order='F')
qDTe_opl=np.zeros((57, 72),order='F')
qDTe_o2pl=np.zeros((57, 72),order='F')
qDTe_nopl=np.zeros((57, 72),order='F')
qDTe_npl=np.zeros((57, 72),order='F')
qDTe_il=np.zeros((57, 72),order='F') 
Le_N2_rot_schunkl=np.zeros((57, 72),order='F')
Le_N2_rot_reesl=np.zeros((57, 72),order='F')
Le_N2_rot_tiegcml=np.zeros((57, 72),order='F')
Le_O2_rot_schunkl=np.zeros((57, 72),order='F')
Le_O2_rot_reesl=np.zeros((57, 72),order='F')
Le_O2_rot_tiegcml=np.zeros((57, 72),order='F')
Le_N2_vib_schunkl=np.zeros((57, 72),order='F')
Le_N2_vib_reesl=np.zeros((57, 72),order='F')
Le_N2_vib_tiegcml=np.zeros((57, 72),order='F')
Le_O2_vib_schunkl=np.zeros((57, 72),order='F')
Le_O2_vib_reesl=np.zeros((57, 72),order='F')
Le_O2_vib_tiegcml=np.zeros((57, 72),order='F')
Le_O_fine_schunkl=np.zeros((57, 72),order='F')
Le_O_fine_reesl=np.zeros((57, 72),order='F')
Le_O_fine_tiegcml=np.zeros((57, 72),order='F')
wind_heatingl=np.zeros((57, 72),order='F')                    
convection_heatingl=np.zeros((57, 72),order='F')
ohmicl=np.zeros((57, 72),order='F')
ohmic_massl=np.zeros((57, 72),order='F')
joulel=np.zeros((57, 72),order='F')
joule_opl=np.zeros((57, 72),order='F')
joule_o2pl=np.zeros((57, 72),order='F')
joule_nopl=np.zeros((57, 72),order='F')
frictionall=np.zeros((57, 72),order='F')
frictional_opl=np.zeros((57, 72),order='F')
frictional_o2pl=np.zeros((57, 72),order='F')
frictional_nopl=np.zeros((57, 72),order='F')
jpedel=np.zeros((57, 72),order='F')
jpednl=np.zeros((57, 72),order='F')
jpedul=np.zeros((57, 72),order='F')
jhallel=np.zeros((57, 72),order='F')
jhallnl=np.zeros((57, 72),order='F')
jhallul=np.zeros((57, 72),order='F')
jperpel=np.zeros((57, 72),order='F')
jperpnl=np.zeros((57, 72),order='F')
jperpul=np.zeros((57, 72),order='F')
mech_powerl=np.zeros((57, 72),order='F')
Potl=np.zeros((72),order='F')
maplatl=np.zeros((72),order='F')
mapaltl=np.zeros((57),order='F')
maptimel=np.zeros((24),order='F')