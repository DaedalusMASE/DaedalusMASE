'''
This file containes all the required factors, constants and global variables
which are required to execute product derivation and error propagation to estimate the
overall error and error contribution on the calculation of Heating rates, Conductivites and other parameters
'''

import numpy as np

# ######################## CONSTANTS ########################
qe = 1.602176565 * 10 ** (-19)  # electron charge in coulomb
me = 9.10938356 * 10 ** (-31)   # electron mass in kg
mO = 15.9994   # Oxygen atomic mass in g/mol
mO2 = 2 * mO   # Oxygen molecular mass in g/mol
mN = 14.0067   # Nitrogen atomic mass in g/mol
mN2 = 2 * mN   # Nitrogen molecular mass in g/mol
mNO = mN + mO  # Nitric oxide mass in g/mol

boltzmann = 1.380645852 * 10 ** (-16)  # Boltzmann's constant in cm^2 * g * s^(-2) * K^(-1)
nAvogadro = 6.02214086 * 10 ** 23      # Avogadro's constant in mol^(-1)
fb = 1.5  # Burnside Factor, the factor that connects theoretical and practical estimations of O+

# Masses in kg
mkO = mO / (nAvogadro * 1000)
mkO2 = mO2 / (nAvogadro * 1000)
mkN = mN / (nAvogadro * 1000)
mkN2 = mN2 / (nAvogadro * 1000)
mkNO = mNO / (nAvogadro * 1000)

ccm = 10 ** 6  # constant to convert cm^(-3) to m^(-3)


glat_in=0  # lat values variable to store TIE-GCMs latitude
glon_in=0  # lon values variable to store TIE-GCMs longitude
glev_in=0 # pressure level variable (lev not ilev) to store TIE-GCMs lev
title=""    # variable to store titles for plots
map_time="" # variable to store time used for night shadow in lat-lon map plots
pngNameMap=""

# Altitudes
heights = np.zeros((72, 144, 57), order='F')

# Altitude used in Lat - Alt plot
heights_la = np.zeros(57, order='F')

# Magnetic field
Bx = np.zeros((72, 144, 57), order='F')
By = np.zeros((72, 144, 57), order='F')
Bz = np.zeros((72, 144, 57), order='F')

# Electric field
Ex = np.zeros((72, 144, 57), order='F')
Ey = np.zeros((72, 144, 57), order='F')
Ez = np.zeros((72, 144, 57), order='F')

# Neutral wind
Unx = np.zeros((72, 144, 57), order='F')
Uny = np.zeros((72, 144, 57), order='F')
Unz = np.zeros((72, 144, 57), order='F')

# Densities
NO = np.zeros((72, 144, 57), order='F')
NO2 = np.zeros((72, 144, 57), order='F')
NN2 = np.zeros((72, 144, 57), order='F')
NOp = np.zeros((72, 144, 57), order='F')
NO2p = np.zeros((72, 144, 57), order='F')
NNOp = np.zeros((72, 144, 57), order='F')
Ne = np.zeros((72, 144, 57), order='F')

# Temperatures
Te = np.zeros((72, 144, 57), order='F')
Ti = np.zeros((72, 144, 57), order='F')
Tn = np.zeros((72, 144, 57), order='F')

# Collision frequencies
nu_Op_sum = np.zeros((72, 144, 57), order='F')
nu_O2p_sum = np.zeros((72, 144, 57), order='F')
nu_NOp_sum = np.zeros((72, 144, 57), order='F')
nu_e_sum = np.zeros((72, 144, 57), order='F')

# Conductivities
pedersen_con = np.zeros((72, 144, 57), order='F')
hall_con = np.zeros((72, 144, 57), order='F')
parallel_con = np.zeros((72, 144, 57), order='F')

# Ion velocities perpendicular to magnetic field
Vi_vertx = np.zeros((72, 144, 57), order='F')
Vi_verty = np.zeros((72, 144, 57), order='F')
Vi_vertz = np.zeros((72, 144, 57), order='F')

# Heating rates
Joule_Heating = np.zeros((72, 144, 57), order='F')
Frictional_Heating = np.zeros((72, 144, 57), order='F')
Ohmic_Heating = np.zeros((72, 144, 57), order='F')

# Cross sections
C_Op = np.zeros((72, 144, 57), order='F')
C_O2p = np.zeros((72, 144, 57), order='F')
C_NOp = np.zeros((72, 144, 57), order='F')
C_ion = np.zeros((72, 144, 57), order='F')

# Perpendicular currents
J_pedersen = np.zeros((72, 144, 57), order='F')
J_hall = np.zeros((72, 144, 57), order='F')
J_ohmic = np.zeros((72, 144, 57), order='F')
J_dens = np.zeros((72, 144, 57), order='F')

# Gyro-frequencies
Omega_ion = np.zeros((72, 144, 57), order='F')
Omega_e = np.zeros((72, 144, 57), order='F')


# Collision frequencies error
nuOp_error = np.zeros((72, 144, 57), order='F')
nuO2p_error = np.zeros((72, 144, 57), order='F')
nuNOp_error = np.zeros((72, 144, 57), order='F')
nue_error = np.zeros((72, 144, 57), order='F')

# Conductivities error (absolute)
pedersen_con_error = np.zeros((72, 144, 57), order='F')
hall_con_error = np.zeros((72, 144, 57), order='F')
parallel_con_error = np.zeros((72, 144, 57), order='F')

# Heating rates error (absolute)
Joule_Heating_error = np.zeros((72, 144, 57), order='F')
Frictional_Heating_error = np.zeros((72, 144, 57), order='F')
Ohmic_Heating_error = np.zeros((72, 144, 57), order='F')

# Cross sections error (absolute)
C_Op_error = np.zeros((72, 144, 57), order='F')
C_O2p_error = np.zeros((72, 144, 57), order='F')
C_NOp_error = np.zeros((72, 144, 57), order='F')
C_ion_error = np.zeros((72, 144, 57), order='F')

# Perpendicular currents error (absolute)
J_pedersen_error = np.zeros((72, 144, 57), order='F')
J_hall_error = np.zeros((72, 144, 57), order='F')
J_ohmic_error = np.zeros((72, 144, 57), order='F')
J_dens_error = np.zeros((72, 144, 57), order='F')

# Collision frequencies contributions error
dnuion_Ti = np.zeros((72, 144, 57), order='F')
dnuion_Tn = np.zeros((72, 144, 57), order='F')
dnuion_Nneutral = np.zeros((72, 144, 57), order='F')
dnue_Te = np.zeros((72, 144, 57), order='F')
dnue_Nneutral = np.zeros((72, 144, 57), order='F')

# Pedersen conductivity contributions error
dsp_B = np.zeros((72, 144, 57), order='F')
dsp_Te = np.zeros((72, 144, 57), order='F')
dsp_Ti = np.zeros((72, 144, 57), order='F')
dsp_Tn = np.zeros((72, 144, 57), order='F')
dsp_Nion = np.zeros((72, 144, 57), order='F')
dsp_Ne = np.zeros((72, 144, 57), order='F')
dsp_Nneutral = np.zeros((72, 144, 57), order='F')

# Hall conductivity contributions error
dsh_B = np.zeros((72, 144, 57), order='F')
dsh_Te = np.zeros((72, 144, 57), order='F')
dsh_Ti = np.zeros((72, 144, 57), order='F')
dsh_Tn = np.zeros((72, 144, 57), order='F')
dsh_Nion = np.zeros((72, 144, 57), order='F')
dsh_Ne = np.zeros((72, 144, 57), order='F')
dsh_Nneutral = np.zeros((72, 144, 57), order='F')

# Joule Heating contributions error
dJH_B = np.zeros((72, 144, 57), order='F')
dJH_E = np.zeros((72, 144, 57), order='F')
dJH_Vi = np.zeros((72, 144, 57), order='F')
dJH_Un = np.zeros((72, 144, 57), order='F')
dJH_Ne = np.zeros((72, 144, 57), order='F')

# Ohmic Heating contributions error
dOH_B = np.zeros((72, 144, 57), order='F')
dOH_E = np.zeros((72, 144, 57), order='F')
dOH_Nneutral = np.zeros((72, 144, 57), order='F')
dOH_Nion = np.zeros((72, 144, 57), order='F')
dOH_Un = np.zeros((72, 144, 57), order='F')
dOH_Ne = np.zeros((72, 144, 57), order='F')
dOH_Te = np.zeros((72, 144, 57), order='F')
dOH_Tn = np.zeros((72, 144, 57), order='F')
dOH_Ti = np.zeros((72, 144, 57), order='F')
dOH_sp = np.zeros((72, 144, 57), order='F')

# Frictional Heating contributions error
dFH_B = np.zeros((72, 144, 57), order='F')
dFH_Nneutral = np.zeros((72, 144, 57), order='F')
dFH_Nion = np.zeros((72, 144, 57), order='F')
dFH_Un = np.zeros((72, 144, 57), order='F')
dFH_Tn = np.zeros((72, 144, 57), order='F')
dFH_Ti = np.zeros((72, 144, 57), order='F')
dFH_Vi = np.zeros((72, 144, 57), order='F')
dFH_nu = np.zeros((72, 144, 57), order='F')

# Ion cross section contribution error
dCion_Ti = np.zeros((72, 144, 57), order='F')
dCion_Tn = np.zeros((72, 144, 57), order='F')
dCion_nu = np.zeros((72, 144, 57), order='F')
dCion_Nneutral = np.zeros((72, 144, 57), order='F')

# Perpendicular currents contributions error
dJohm_B = np.zeros((72, 144, 57), order='F')
dJohm_E = np.zeros((72, 144, 57), order='F')
dJohm_Un = np.zeros((72, 144, 57), order='F')
dJohm_sp = np.zeros((72, 144, 57), order='F')
dJohm_sh = np.zeros((72, 144, 57), order='F')
dJohm_Ti = np.zeros((72, 144, 57), order='F')
dJohm_Tn = np.zeros((72, 144, 57), order='F')
dJohm_Te = np.zeros((72, 144, 57), order='F')
dJohm_Ne = np.zeros((72, 144, 57), order='F')
dJohm_Nneutral = np.zeros((72, 144, 57), order='F')
dJohm_Nion = np.zeros((72, 144, 57), order='F')

dJd_B = np.zeros((72, 144, 57), order='F')
dJd_E = np.zeros((72, 144, 57), order='F')
dJd_Vi = np.zeros((72, 144, 57), order='F')
dJd_Un = np.zeros((72, 144, 57), order='F')
dJd_Ne = np.zeros((72, 144, 57), order='F')