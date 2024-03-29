'''
This file contains erro function which used to calculate error propagation and contribution oof measurement 
error on the caculation of LTI products
'''
import time
import numpy as np
import factors


# ############################################ CALCULATE ERROR ############################################
# #########################################################################################################
def error(error_flag, B_error=0, E_error=0, NO_error=0, NO2_error=0, NN2_error=0, NOp_error=0, NO2p_error=0, NNOp_error=0,
          Ne_error=0, Te_error=0, Ti_error=0, Tn_error=0, Un_error=0, Vi_error=0, lat_value=-1, lon_value=-1,
          pressure_level=-1):

    '''
    This function used to calculate Error propagation and error contribution on LTI products. 
    This fuction should be used after the execution of model_inputs and products function, 
    in order to all the required quantites are fufllilled in the appropriate structures.

        Args:
        error_flag (bool): If error_flag==False then as error inputs used the error quantites provide by user.
                            If error_flag==True then error values are came from Daedalus Science Study
        B_error(float): As precentage in case of error flag is not set and errors came from user inputs 
        E_error(float): As precentage in case of error flag is not set and errors came from user inputs
        NO_error(float): As precentage in case of error flag is not set and errors came from user inputs
        NO2_error(float): As precentage in case of error flag is not set and errors came from user inputs
        NN2_error(float): As precentage in case of error flag is not set and errors came from user inputs
        NOp_error(float): As precentage in case of error flag is not set and errors came from user inputs
        NO2p_error(float): As precentage in case of error flag is not set and errors came from user inputs
        NNOp_error(float): As precentage in case of error flag is not set and errors came from user inputs
        Ne_error(float): As precentage in case of error flag is not set and errors came from user inputs
        Te_error(float): As precentage in case of error flag is not set and errors came from user inputs
        Ti_error(float): As precentage in case of error flag is not set and errors came from user inputs
        Tn_error(float): As precentage in case of error flag is not set and errors came from user inputs
        Un_error(float): As precentage in case of error flag is not set and errors came from user inputs
        Vi_error(float): As precentage in case of error flag is not set and errors came from user inputs

        lat_value (int): Latitude as index of TIEGCM file, used to obtain the kind of function execution
        lon_value (int): Longitude as index of TIEGCM file, used to obtain the kind of function execution
        pressure_value (int): Pressure level as index of TIEGCM file, used to obtain the kind of function execution
        Latitude - Altitude map profile
        lat_value == -1, pressure_level == -1
        Lattitude - Longitude map profile
        lat_value == -1 and lon_value == -1
        Vertical profile
        lat_value != -1 and lon_value != -1:

        Returns calculated errors and error contributions pruducts structures as factors.xxx. 
        See file factor.py lines 112 to 217

    '''
    start_time = time.time()
    print('Calculating Error.....')
    print(' ')

    # Distinguish Map from Vertical profile
    lev_range = 0
    lat_range = 0
    lon_range = 0

    lev_start = 0
    lat_start = 0
    lon_start = 0
    max_bar = 0

    # Lat - Alt map profile
    if lat_value == -1 and pressure_level == -1:
        lev_range = len(factors.glev_in) - 1
        lat_range = len(factors.glat_in)
        lon_start = lon_value
        lon_range = lon_start + 1
        max_bar = lev_range

    # Lat - Lon map profile
    if lat_value == -1 and lon_value == -1:
        lev_start = pressure_level
        lev_range = lev_start + 1
        lat_range = len(factors.glat_in)
        lon_range = len(factors.glon_in)
        max_bar = lat_range

    # Vertical profile
    if lat_value != -1 and lon_value != -1:
        lat_start = lat_value
        lon_start = lon_value
        lat_range = lat_start + 1
        lon_range = lon_start + 1
        lev_range = len(factors.glev_in) - 1
        max_bar = lev_range

    
    for lev in range(lev_start, lev_range):
        for lat in range(lat_start, lat_range):
            for lon in range(lon_start, lon_range):
                # progress bar index
                if max_bar == 56:
                    i = lev
                else:
                    i = lat

                # Magnetic field vector(in tesla)
                B = [factors.Bx[lat, lon, lev], factors.By[lat, lon, lev], factors.Bz[lat, lon, lev]]
                # Magnetic field norm and unit vector
                Bnorm = np.sqrt(B[0] ** 2 + B[1] ** 2 + B[2] ** 2)
                bunit = [B[0] / Bnorm, B[1] / Bnorm, B[2] / Bnorm]
                # Electric field vector(in volt/meter)
                E = [factors.Ex[lat, lon, lev], factors.Ey[lat, lon, lev], factors.Ez[lat, lon, lev]]
                # Neutral wind vector(in meter/sec)
                Un = [factors.Unx[lat, lon, lev], factors.Uny[lat, lon, lev], factors.Unz[lat, lon, lev]]
                # Ion velocity vector(in meter/sec)
                # Vi_vert ≡ Vi as mentioned in products function above
                Vi_vert = [factors.Vi_vertx[lat, lon, lev], factors.Vi_verty[lat, lon, lev], factors.Vi_vertz[lat, lon, lev]]

                # ############################### ASSIGNING ERRORS ###############################
                # distinguish percentage from real errors
                if not error_flag:
                    # percentage errors, squared
                    # ############# magnetic field ###########
                    dBx = ((B_error / 100) * B[0]) ** 2
                    dBy = ((B_error / 100) * B[1]) ** 2
                    dBz = ((B_error / 100) * B[2]) ** 2
                    # |theta_|B| / theta_Bx|^2
                    thB_Bx = (B[0] / Bnorm) ** 2
                    # |theta_|B| / theta_By|^2
                    thB_By = (B[1] / Bnorm) ** 2
                    # |theta_|B| / theta_Bz|^2
                    thB_Bz = (B[2] / Bnorm) ** 2
                    # d|B|^2
                    dB = thB_Bx * dBx + thB_By * dBy + thB_Bz * dBz
                    # ############## electric field ##################
                    dEx = ((E_error / 100) * E[0]) ** 2
                    dEy = ((E_error / 100) * E[1]) ** 2
                    dEz = ((E_error / 100) * E[2]) ** 2
                    # ################### densities in cm^(-3) ####################
                    dNO = ((NO_error / 100) * factors.NO[lat, lon, lev]) ** 2
                    dNO2 = ((NO2_error / 100) * factors.NO2[lat, lon, lev]) ** 2
                    dNN2 = ((NN2_error / 100) * factors.NN2[lat, lon, lev]) ** 2
                    dNOp = ((NOp_error / 100) * factors.NOp[lat, lon, lev]) ** 2
                    dNO2p = ((NO2p_error / 100) * factors.NO2p[lat, lon, lev]) ** 2
                    dNNOp = ((NNOp_error / 100) * factors.NNOp[lat, lon, lev]) ** 2
                    dNe = ((Ne_error / 100) * factors.Ne[lat, lon, lev]) ** 2
                    # ################## temperatures in kelvin ###################
                    dTe = ((Te_error / 100) * factors.Te[lat, lon, lev]) ** 2
                    dTi = ((Ti_error / 100) * factors.Ti[lat, lon, lev]) ** 2
                    dTn = ((Tn_error / 100) * factors.Tn[lat, lon, lev]) ** 2
                    # ############### neutral wind in m/s ################
                    dUnx = ((Un_error / 100) * Un[0]) ** 2
                    dUny = ((Un_error / 100) * Un[1]) ** 2
                    dUnz = ((Un_error / 100) * Un[2]) ** 2
                    # ############### ion velocity in m/s #############
                    dVix = ((Vi_error / 100) * Vi_vert[0]) ** 2
                    dViy = ((Vi_error / 100) * Vi_vert[1]) ** 2
                    dViz = ((Vi_error / 100) * Vi_vert[2]) ** 2
                elif error_flag:
                    # Daedalus team threshold errors, squared
                    # ########### magnetic field #########
                    dBx = (5 * 10 ** (-9)) ** 2
                    dBy = (5 * 10 ** (-9)) ** 2
                    dBz = (5 * 10 ** (-9)) ** 2
                    # |theta_|B| / theta_Bx|^2
                    thB_Bx = (B[0] / Bnorm) ** 2
                    # |theta_|B| / theta_By|^2
                    thB_By = (B[1] / Bnorm) ** 2
                    # |theta_|B| / theta_Bz|^2
                    thB_Bz = (B[2] / Bnorm) ** 2
                    # d|B|^2
                    dB = thB_Bx * dBx + thB_By * dBy + thB_Bz * dBz
                    # ################# electric field ############
                    dEx = (2 * 10 ** (-3)) ** 2
                    dEy = (2 * 10 ** (-3)) ** 2
                    dEz = (2 * 10 ** (-3)) ** 2
                    # ################### densities in cm^(-3) ####################
                    dNO = ((20 / 100) * factors.NO[lat, lon, lev]) ** 2
                    dNO2 = ((20 / 100) * factors.NO2[lat, lon, lev]) ** 2
                    dNN2 = ((20 / 100) * factors.NN2[lat, lon, lev]) ** 2
                    dNOp = ((10 / 100) * factors.NOp[lat, lon, lev]) ** 2
                    dNO2p = ((10 / 100) * factors.NO2p[lat, lon, lev]) ** 2
                    dNNOp = ((10 / 100) * factors.NNOp[lat, lon, lev]) ** 2
                    dNe = ((10 / 100) * factors.Ne[lat, lon, lev]) ** 2
                    # ############### temperatures in kelvin ########################
                    dTe = ((10 / 100) * factors.Te[lat, lon, lev]) ** 2
                    dTi = ((10 / 100) * factors.Ti[lat, lon, lev]) ** 2
                    dTn = ((20 / 100) * factors.Tn[lat, lon, lev]) ** 2
                    # ################# neutral wind in m/s #########################
                    H_wind = 20 # horizontal wind accuracy
                    V_wind = 10 # vertical wind accuracy
                    dUnx = V_wind ** 2
                    dUny = V_wind ** 2
                    dUnz = H_wind ** 2
                    # #################### ion velocity in m/s ###################3
                    dVix = 100 ** 2
                    dViy = 100 ** 2
                    dViz = 100 ** 2

                # ################# COLLISION FREQUENCIES ERROR #################
                # ######################### O+ #########################
                # |dnuOp|^2 = |dnuOp-O|^2 + |dnuOp-O2|^2 + |dnuOp-N2|^2
                Tr = (factors.Ti[lat, lon, lev] + factors.Tn[lat, lon, lev]) / 2
                # |theta_nuOp-O / theta_NO|^2
                thOp_O_NO = (factors.fb * 3.67 * 10 ** (-11) * Tr ** (1 / 2) * (1 - 0.064 * np.log10(Tr)) ** 2) ** 2
                # |theta_nuOp-O / theta_Ti|^2
                thOp_O_Ti = ((9.175 * 10 ** (-12) * factors.fb * factors.NO[lat, lon, lev] * (1 - 0.064 * (np.log(Tr) / np.log(10))) ** 2) / Tr ** (1 / 2) -
                             (2.3488 * 10 ** (-12) * factors.fb * factors.NO[lat, lon, lev] * (1 - 0.064 * (np.log(Tr) / np.log(10)))) /
                             (np.log(10) * Tr ** (1 / 2))) ** 2
                # |theta_nuOp-O / theta_Tn|^2
                thOp_O_Tn = thOp_O_Ti
                # |dnuOp_O|^2
                dnuOp_O = thOp_O_NO * dNO + thOp_O_Ti * dTi + thOp_O_Tn * dTn

                # |theta_nuOp-O2 / theta_NO2|^2
                thOp_O2_NO2 = (6.64 * 10 ** (-10)) ** 2
                # |dnuOp_O2|^2
                dnuOp_O2 = thOp_O2_NO2 * dNO2

                # |theta_nuOp-N2 / theta_NN2|^2
                thOp_N2_NN2 = (6.82 * 10 ** (-10)) ** 2
                # |dnuOp_N2|^2
                dnuOp_N2 = thOp_N2_NN2 * dNN2

                # |dnuOp|
                factors.nuOp_error[lat, lon, lev] = np.sqrt(dnuOp_O + dnuOp_O2 + dnuOp_N2)
                # ############################# O2+ #############################
                # |dnuO2p|^2 = |dnuO2p-O2|^2 + |dnuOp-O|^2 + |dnuOp-N2|^2
                # |theta_nuO2p-O2 / theta_NO2|^2
                thO2p_O2_NO2 = (2.59 * 10 ** (-11) * Tr ** (1 / 2) * (1 - 0.073 * np.log10(Tr)) ** 2) ** 2
                # |theta_nuO2p-O2 / theta_Ti|^2
                thO2p_O2_Ti = ((6.475 * 10 ** (-12) * factors.NO2[lat, lon, lev] * (1 - 0.073 * (np.log(Tr) / np.log(10))) ** 2) / Tr ** (1 / 2) -
                               (1.8907 * 10 ** (-12) * factors.NO2[lat, lon, lev] * (1 - 0.073 * (np.log(Tr) / np.log(10)))) /
                               (np.log(10) * Tr ** (1 / 2))) ** 2
                # |theta_nuO2p-O2 / theta_Tn|^2
                thO2p_O2_Tn = thO2p_O2_Ti

                # |dnuO2p_O2|^2
                dnuO2p_O2 = thO2p_O2_NO2 * dNO2 + thO2p_O2_Ti * dTi + thO2p_O2_Tn * dTn

                # |theta_nuO2p-O / theta_NO|^2
                thO2p_O_NO = (2.31 * 10 ** (-10)) ** 2
                # |dnuO2p_O|^2
                dnuO2p_O = thO2p_O_NO * dNO
                # |theta_nuO2p-N2 / theta_NN2|^2
                thO2p_N2_NN2 = (4.13 * 10 ** (-10)) ** 2
                # |dnuO2p_N2|^2
                dnuO2p_N2 = thO2p_N2_NN2 * dNN2

                # |dnuO2p|
                factors.nuO2p_error[lat, lon, lev] = np.sqrt(dnuO2p_O2 + dnuO2p_O + dnuO2p_N2)
                # ########################## NO+ ###########################
                # |dnuNOp|^2 = |dnuNOp-O|^2 + |dnuNOp-O2|^2 + |dnuNOp-N2|^2
                # |theta_nuNOp-O / theta_NO|^2
                thNOp_O_NO = (2.44 * 10 ** (-10)) ** 2
                # |dnuNOp_O|^2
                dnuNOp_O = thNOp_O_NO * dNO
                # |theta_nuNOp_O2 / theta_NO2|^2
                thNOp_O2_NO2 = (4.27 * 10 ** (-10)) ** 2
                # |dnuNOp_O2|^2
                dnuNOp_O2 = thNOp_O2_NO2 * dNO2
                # |theta_nuNOp-N2 / theta_NN2|^2
                thNOp_N2_NN2 = (4.34 * 10 ** (-10)) ** 2
                # |dnuNOp_N2|^2
                dnuNOp_N2 = thNOp_N2_NN2 * dNN2

                # |dnuNOp|
                factors.nuNOp_error[lat, lon, lev] = np.sqrt(dnuNOp_O + dnuNOp_N2 + dnuNOp_O2)
                # ############################ Ion collision frequency contributions error ############################
                # squared
                factors.dnuion_Ti[lat, lon, lev] = thOp_O_Ti * dTi + thO2p_O2_Ti * dTi
                factors.dnuion_Tn[lat, lon, lev] = thOp_O_Tn * dTn + thO2p_O2_Tn * dTn
                factors.dnuion_Nneutral[lat, lon, lev] = ((thOp_O_NO + thO2p_O_NO + thNOp_O_NO) / 9) * dNO + (
                                                  (thOp_O2_NO2 + thO2p_O2_NO2 + thNOp_O2_NO2) / 9) * dNO2 + (
                                                  (thOp_N2_NN2 + thO2p_N2_NN2 + thNOp_N2_NN2) / 9) * dNN2
                # ######################################################################################################
                # ######################## electron #######################
                # |dnue|^2 = |dnue-O|^2 + |dnue-O2|^2 + |dnue-N2|^2
                # |theta_nue-O / theta_Te|^2
                the_O_Te = (4.45 * 10 ** (-11) * factors.NO[lat, lon, lev] * factors.Te[lat, lon, lev] ** (-1 / 2) +
                            7.6095 * 10 ** (-14) * factors.NO[lat, lon, lev] * factors.Te[lat, lon, lev] ** (1 / 2)) ** 2
                # |theta_nue-O / theta_NO|^2
                the_O_NO = (8.9 * 10 ** (-11) * factors.Te[lat, lon, lev] ** (1 / 2) * (1 + 5.7 * 10 ** (-4) * factors.Te[lat, lon, lev])) ** 2
                # |dne_O|^2
                dnue_O = the_O_Te * dTe + the_O_NO * dNO
                # |theta_nue-O2 / theta_Te|^2
                the_O2_Te = (9.1 * 10 ** (-11) * factors.NO2[lat, lon, lev] * factors.Te[lat, lon, lev] ** (-1 / 2) +
                             6.552 * 10 ** (-12) * factors.NO2[lat, lon, lev]) ** 2
                # |theta_nue-O2 / theta_NO2|^2
                the_O2_NO2 = (1.82 * 10 ** (-10) * factors.Te[lat, lon, lev] ** (1 / 2) * (1 + 3.6 * 10 ** (-2) * factors.Te[lat, lon, lev] ** (1 / 2))) ** 2
                # |dnue_O2|^2
                dnue_O2 = the_O2_Te * dTe + the_O2_NO2 * dNO2
                # |theta_nue-N2 / theta_Te|^2
                the_N2_Te = (2.33 * 10 ** (-11) * factors.NN2[lat, lon, lev] - 5.6386 * 10 ** (-15) * factors.NN2[lat, lon, lev] * factors.Te[lat, lon, lev]) ** 2
                # |theta_nue-N2 / theta_NN2|^2
                the_N2_NN2 = (2.33 * 10 ** (-11) * factors.Te[lat, lon, lev] * (1 - 1.21 * 10 ** (-4) * factors.Te[lat, lon, lev])) ** 2
                # |dnue_N2|^2
                dnue_N2 = the_N2_Te * dTe + the_N2_NN2 * dNN2

                # |dnue|
                factors.nue_error[lat, lon, lev] = np.sqrt(dnue_O + dnue_O2 + dnue_N2)
                # ############################### e collision frequency contributions error ##############################
                # squared
                factors.dnue_Te[lat, lon, lev] = the_O_Te * dTe + the_O2_Te * dTe + the_N2_Te * dTe
                factors.dnue_Nneutral[lat, lon, lev] = the_O_NO * dNO + the_O2_NO2 * dNO2 + the_N2_NN2 * dNN2
                # ########################################################################################################
                # ###################### OMEGAS ERROR ######################

                # qe(in coulomb), mk(masses in kg), omegas(in Hz)
                omega_Op = (factors.qe * Bnorm) / factors.mkO
                omega_O2p = (factors.qe * Bnorm) / factors.mkO2
                omega_NOp = (factors.qe * Bnorm) / factors.mkNO
                omega_e = (factors.qe * Bnorm) / factors.me

                # ############## O+ ##############
                # |theta_omegaOp / theta_B|^2
                th_omOp_B = (factors.qe / factors.mkO) ** 2
                # |domegaOp|^2
                domegaOp = th_omOp_B * dB
                # ############# O2+ ##############
                # |theta_omegaO2p / theta_B|^2
                th_omO2p_B = (factors.qe / factors.mkO2) ** 2
                # |domegaO2p|^2
                domegaO2p = th_omO2p_B * dB
                # ############# NO+ ##############
                # |theta_omegaNOp / theta_B|^2
                th_omNOp_B = (factors.qe / factors.mkNO) ** 2
                # |domegaOp|^2
                domegaNOp = th_omNOp_B * dB
                # ############## e ###############
                # |theta_omega_e / theta_B|^2
                th_ome_B = (factors.qe / factors.me) ** 2
                # |domega_e|^2
                domegae = th_ome_B * dB
                # ####################### RATIOS ERROR #######################
                r_Op = factors.nu_Op_sum[lat, lon, lev] / omega_Op
                r_O2p = factors.nu_O2p_sum[lat, lon, lev] / omega_O2p
                r_NOp = factors.nu_NOp_sum[lat, lon, lev] / omega_NOp
                r_e = factors.nu_e_sum[lat, lon, lev] / omega_e
                # ############ O+ ###########
                # |theta_rOp / theta_nuOp|^2
                th_rOp_nuOp = (1 / omega_Op) ** 2
                # |theta_rOp / theta_omegaOp|^2
                th_rOp_omOp = (factors.nu_Op_sum[lat, lon, lev] / omega_Op ** 2) ** 2
                # |drOp|^2
                drOp = th_rOp_nuOp * factors.nuOp_error[lat, lon, lev] ** 2 + th_rOp_omOp * domegaOp
                # ########### O2+ ###########
                # |theta_rO2p / theta_nuO2p|^2
                th_rO2p_nuO2p = (1 / omega_O2p) ** 2
                # |theta_rO2p / theta_omegaO2p|^2
                th_rO2p_omO2p = (factors.nu_O2p_sum[lat, lon, lev] / omega_O2p ** 2) ** 2
                # |drO2p|^2
                drO2p = th_rO2p_nuO2p * factors.nuO2p_error[lat, lon, lev] ** 2 + th_rO2p_omO2p * domegaO2p
                # ########### NO+ ###########
                # |theta_rNOp / theta_nuNOp|^2
                th_rNOp_nuNOp = (1 / omega_NOp) ** 2
                # |theta_rNOp / theta_omegaNOp|^2
                th_rNOp_omNOp = (factors.nu_NOp_sum[lat, lon, lev] / omega_NOp ** 2) ** 2
                # |drNOp|^2
                drNOp = th_rNOp_nuNOp * factors.nuNOp_error[lat, lon, lev] ** 2 + th_rNOp_omNOp * domegaNOp
                # ########## e ##########
                # |theta_re / theta_nue|^2
                th_re_nue = (1 / omega_e) ** 2
                # |theta_re / theta_omegae|^2
                th_re_ome = (factors.nu_e_sum[lat, lon, lev] / omega_e ** 2) ** 2
                # |dre|^2
                dre = th_re_nue * factors.nue_error[lat, lon, lev] ** 2 + th_re_ome * domegae
                # ################################ CONDUCTIVITIES ERROR ################################
                # ############################# PEDERSEN CONDUCTIVITY ERROR ############################
                # densities error in m^(-3)
                # |theta_sigmaP/ theta_B|^2
                term_e = (factors.Ne[lat, lon, lev] * factors.ccm * r_e) / (1 + r_e ** 2)
                term_Op = (factors.NOp[lat, lon, lev] * factors.ccm * r_Op) / (1 + r_Op ** 2)
                term_O2p = (factors.NO2p[lat, lon, lev] * factors.ccm * r_O2p) / (1 + r_O2p ** 2)
                term_NOp = (factors.NNOp[lat, lon, lev] * factors.ccm * r_NOp) / (1 + r_NOp ** 2)
                thP_B = (factors.qe * (term_e + term_Op + term_O2p + term_NOp) / Bnorm ** 2) ** 2
                # |theta_sigmaP / theta_Ne|^2
                thP_Ne = (factors.qe * r_e / (Bnorm * (1 + r_e ** 2))) ** 2
                # |theta_sigmaP / theta_re|^2
                thP_re = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (1 - r_e ** 2) / (Bnorm * (1 + r_e ** 2) ** 2)) ** 2
                # |theta_sigmaP / theta_NOp|^2
                thP_NOp = (factors.qe * r_Op / (Bnorm * (1 + r_Op ** 2))) ** 2
                # |theta_sigmaP / theta_rOp|^2
                thP_rOp = (factors.qe * factors.NOp[lat, lon, lev] * factors.ccm * (1 - r_Op ** 2) / (Bnorm * (1 + r_Op ** 2) ** 2)) ** 2
                # |theta_sigmaP / theta_NO2p|^2
                thP_NO2p = (factors.qe * r_O2p / (Bnorm * (1 + r_O2p ** 2))) ** 2
                # |theta_sigmaP / theta_rO2p|^2
                thP_rO2p = (factors.qe * factors.NO2p[lat, lon, lev] * factors.ccm * (1 - r_O2p ** 2) / (Bnorm * (1 + r_O2p ** 2) ** 2)) ** 2
                # |theta_sigmaP / theta_NNOp|^2
                thP_NNOp = (factors.qe * r_NOp / (Bnorm * (1 + r_NOp ** 2))) ** 2
                # |theta_sigmaP / theta_rOp|^2
                thP_rNOp = (factors.qe * factors.NNOp[lat, lon, lev] * factors.ccm * (1 - r_NOp ** 2) / (Bnorm * (1 + r_NOp ** 2) ** 2)) ** 2
                # |dsigmaP|
                factors.pedersen_con_error[lat, lon, lev] = np.sqrt(thP_B * dB + thP_Ne * dNe * factors.ccm ** 2 + thP_re * dre +
                                                            thP_NOp * dNOp * factors.ccm ** 2 + thP_rOp * drOp +
                                                            thP_NO2p * dNO2p * factors.ccm ** 2 + thP_rO2p * drO2p +
                                                            thP_NNOp * dNNOp * factors.ccm ** 2 + thP_rNOp * drNOp)
                # ############################ Pedersen conductivity contributions error ############################
                # squared
                factors.dsp_B[lat, lon, lev] = thP_B * dB + thP_re * th_re_ome * th_ome_B * dB + thP_rOp * th_rOp_omOp * th_omOp_B * dB + \
                                       thP_rO2p * th_rO2p_omO2p * th_omO2p_B * dB + thP_rNOp * th_rNOp_omNOp * th_omNOp_B * dB
                factors.dsp_Ti[lat, lon, lev] = thP_rOp * th_rOp_nuOp * thOp_O_Ti * dTi + thP_rO2p * th_rO2p_nuO2p * thO2p_O2_Ti * dTi
                factors.dsp_Te[lat, lon, lev] = thP_re * th_re_nue * the_O_Te * dTe + thP_re * th_re_nue * the_O2_Te * dTe + \
                                        thP_re * th_re_nue * the_N2_Te * dTe
                factors.dsp_Tn[lat, lon, lev] = thP_rOp * th_rOp_nuOp * thOp_O_Tn * dTn + thP_rO2p * th_rO2p_nuO2p * thO2p_O2_Tn * dTn
                factors.dsp_Nion[lat, lon, lev] = thP_NOp * dNOp * factors.ccm ** 2 + thP_NO2p * dNO2p * factors.ccm ** 2 + thP_NNOp * dNNOp * factors.ccm ** 2
                factors.dsp_Ne[lat, lon, lev] = thP_Ne * dNe * factors.ccm ** 2
                factors.dsp_Nneutral[lat, lon, lev] = thP_rOp * th_rOp_nuOp * thOp_O_NO * dNO + thP_rOp * th_rOp_nuOp * thOp_O2_NO2 * dNO2 + \
                                              thP_rOp * th_rOp_nuOp * thOp_N2_NN2 * dNN2 + thP_rO2p * th_rO2p_nuO2p * thO2p_O2_NO2 * dNO2 + \
                                              thP_rO2p * th_rO2p_nuO2p * thO2p_O_NO * dNO + thP_rO2p * th_rO2p_nuO2p * thO2p_N2_NN2 * dNN2 + \
                                              thP_rNOp * th_rNOp_nuNOp * thNOp_O_NO * dNO + thP_rNOp * th_rNOp_nuNOp * thNOp_O2_NO2 * dNO2 + \
                                              thP_rNOp * th_rNOp_nuNOp * thNOp_N2_NN2 * dNN2 + thP_re * th_re_nue * the_O_NO * dNO + \
                                              thP_re * th_re_nue * the_O2_NO2 * dNO2 + thP_re * th_re_nue * the_N2_NN2 * dNN2
                # ####################################################################################################
                # ####################### HALL CONDUCTIVITY ERROR #######################
                # densities error in m^(-3)
                # |theta_sigmaH / theta_B|^2
                thH_B = (factors.qe * (term_e / r_e - term_Op / r_Op - term_O2p / r_O2p - term_NOp / r_NOp) / Bnorm ** 2) ** 2
                # |theta_sigmaH / theta_Ne|^2
                thH_Ne = (factors.qe / (Bnorm * (1 + r_e ** 2))) ** 2
                # |theta_sigmaH / theta_re|^2
                thH_re = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * 2 * r_e / (Bnorm * (1 + r_e ** 2) ** 2)) ** 2
                # |theta_sigmaH / theta_NOp|^2
                thH_NOp = (factors.qe / (Bnorm * (1 + r_Op ** 2))) ** 2
                # |theta_sigmaH / theta_rOp|^2
                thH_rOp = (factors.qe * factors.NOp[lat, lon, lev] * factors.ccm * 2 * r_Op / (Bnorm * (1 + r_Op ** 2) ** 2)) ** 2
                # |theta_sigmaH / theta_NO2p|^2
                thH_NO2p = (factors.qe / (Bnorm * (1 + r_O2p ** 2))) ** 2
                # |theta_sigmaH / theta_rO2p|^2
                thH_rO2p = (factors.qe * factors.NO2p[lat, lon, lev] * factors.ccm * 2 * r_O2p / (Bnorm * (1 + r_O2p ** 2) ** 2)) ** 2
                # |theta_sigmaH / theta_NNOp|^2
                thH_NNOp = (factors.qe / (Bnorm * (1 + r_NOp ** 2))) ** 2
                # |theta_sigmaH / theta_rNOp|^2
                thH_rNOp = (factors.qe * factors.NNOp[lat, lon, lev] * factors.ccm * 2 * r_NOp / (Bnorm * (1 + r_NOp ** 2) ** 2)) ** 2
                # |dsigmaH|
                factors.hall_con_error[lat, lon, lev] = np.sqrt(thH_B * dB + thH_Ne * dNe * factors.ccm ** 2 + thH_re * dre +
                                                        thH_NOp * dNOp * factors.ccm ** 2 + thH_rOp * drOp +
                                                        thH_NO2p * dNO2p * factors.ccm ** 2 + thH_rO2p * drO2p +
                                                        thH_NNOp * dNNOp * factors.ccm ** 2 + thH_rNOp * drNOp)
                # ###################################### Hall conductivity contributions error ######################################
                factors.dsh_B[lat, lon, lev] = thH_B * dB + thH_re * th_re_ome * th_ome_B * dB + thH_rOp * th_rOp_omOp * th_omOp_B * dB + \
                                       thH_rO2p * th_rO2p_omO2p * th_omO2p_B * dB + thH_rNOp * th_rNOp_omNOp * th_omNOp_B * dB
                factors.dsh_Ti[lat, lon, lev] = thH_rOp * th_rOp_nuOp * thOp_O_Ti * dTi + thH_rO2p * th_rO2p_nuO2p * thO2p_O2_Ti * dTi
                factors.dsh_Te[lat, lon, lev] = thH_re * th_re_nue * the_O_Te * dTe + thH_re * th_re_nue * the_O2_Te * dTe + \
                                        thH_re * th_re_nue * the_N2_Te * dTe
                factors.dsh_Tn[lat, lon, lev] = thH_rOp * th_rOp_nuOp * thOp_O_Tn * dTn + thH_rO2p * th_rO2p_nuO2p * thO2p_O2_Tn * dTn
                factors.dsh_Nion[lat, lon, lev] = thH_NOp * dNOp * factors.ccm ** 2 + thH_NO2p * dNO2p * factors.ccm ** 2 + thH_NNOp * dNNOp * factors.ccm ** 2
                factors.dsh_Ne[lat, lon, lev] = thH_Ne * dNe * factors.ccm ** 2
                factors.dsh_Nneutral[lat, lon, lev] = thH_rOp * th_rOp_nuOp * thOp_O_NO * dNO + thH_rOp * th_rOp_nuOp * thOp_O2_NO2 * dNO2 + \
                                              thH_rOp * th_rOp_nuOp * thOp_N2_NN2 * dNN2 + thH_rO2p * th_rO2p_nuO2p * thO2p_O2_NO2 * dNO2 + \
                                              thH_rO2p * th_rO2p_nuO2p * thO2p_O_NO * dNO + thH_rO2p * th_rO2p_nuO2p * thO2p_N2_NN2 * dNN2 + \
                                              thH_rNOp * th_rNOp_nuNOp * thNOp_O_NO * dNO + thH_rNOp * th_rNOp_nuNOp * thNOp_O2_NO2 * dNO2 + \
                                              thH_rNOp * th_rNOp_nuNOp * thNOp_N2_NN2 * dNN2 + thH_re * th_re_nue * the_O_NO * dNO + \
                                              thH_re * th_re_nue * the_O2_NO2 * dNO2 + thH_re * th_re_nue * the_N2_NN2 * dNN2
                # #####################################################################################################################
                # ############################# PARALLEL CONDUCTIVITY ERROR #############################
                # densities error in m^(-3)
                # |theta_sigma_paral / theta_Ne|^2
                thparal_Ne = (factors.qe ** 2 / (factors.me * factors.nu_e_sum[lat, lon, lev])) ** 2
                # |theta_sigma_paral / theta_nue|^2
                thparal_nue = (factors.Ne[lat, lon, lev] * factors.ccm * factors.qe ** 2 / (factors.me * factors.nu_e_sum[lat, lon, lev] ** 2)) ** 2
                # |dsigma_paral|
                factors.parallel_con_error[lat, lon, lev] = np.sqrt(thparal_Ne * dNe * factors.ccm ** 2 + thparal_nue * factors.nue_error[lat, lon, lev] ** 2)
                # ########################### HEATING RATES ERROR ###########################
                # ################## bunit error ##################
                # ######### bx #########
                # |theta_bx / theta_Bx|^2
                thbx_Bx = (1 / Bnorm) ** 2
                # |theta_bx / theta_B|^2
                thbx_B = (B[0] / Bnorm ** 2) ** 2
                # |dbx|^2
                dbx = thbx_Bx * dBx + thbx_B * dB
                # ######### by #########
                # |theta_by / theta_By|^2
                thby_By = (1 / Bnorm) ** 2
                # |theta_by / theta_B|^2
                thby_B = (B[1] / Bnorm ** 2) ** 2
                # |dby|^2
                dby = thby_By * dBy + thby_B * dB
                # ######### bz #########
                # |theta_bz / theta_Bz|^2
                thbz_Bz = (1 / Bnorm) ** 2
                # |theta_bz / theta_B|^2
                thbz_B = (B[2] / Bnorm ** 2) ** 2
                # |dbz|^2
                dbz = thbz_Bz * dBz + thbz_B * dB
                # ############### Un vertical error ###############
                # ########## Un_vertx ##########
                # |theta_Unvertx / theta_Uny|^2
                thUn_vertx_Uny = (bunit[2]) ** 2
                # |theta_Unvertx / theta_Unz|^2
                thUn_vertx_Unz = (bunit[1]) ** 2
                # |theta_Unvertx / theta_bz|^2
                thUn_vertx_bz = (Un[1]) ** 2
                # |theta_Unvertx / theta_by|^2
                thUn_vertx_by = (Un[2]) ** 2
                # |dUn_vertx|^2
                dUn_vertx = thUn_vertx_Uny * dUny + thUn_vertx_Unz * dUnz + thUn_vertx_bz * dbz + thUn_vertx_by * dby
                # ########## Un_verty ##########
                # |theta_Unverty / theta_Unz|^2
                thUn_verty_Unz = (bunit[0]) ** 2
                # |theta_Unverty / theta_Unx|^2
                thUn_verty_Unx = (bunit[2]) ** 2
                # |theta_Unverty / theta_bx|^2
                thUn_verty_bx = (Un[2]) ** 2
                # |theta_Unverty / theta_bz|^2
                thUn_verty_bz = (Un[0]) ** 2
                # |dUn_verty|^2
                dUn_verty = thUn_verty_Unz * dUnz + thUn_verty_Unx * dUnx + thUn_verty_bx * dbx + thUn_verty_bz * dbz
                # ########## Un_vertz ##########
                # |theta_Unvertz / theta_Unx|^2
                thUn_vertz_Unx = (bunit[1]) ** 2
                # |theta_Unvertz / theta_Uny|^2
                thUn_vertz_Uny = (bunit[0]) ** 2
                # |theta_Unvertz / theta_by|^2
                thUn_vertz_by = (Un[0]) ** 2
                # |theta_Unvertz / theta_bx|^2
                thUn_vertz_bx = (Un[1]) ** 2
                # |dUn_vertz|^2
                dUn_vertz = thUn_vertz_Unx * dUnx + thUn_vertz_Uny * dUny + thUn_vertz_by * dby + thUn_vertz_bx * dbx
                # ###################### E vertical error ######################
                # ######### E_vertx #########
                # |theta_Evertx / theta_Ey|^2
                thEvertx_Ey = (bunit[2]) ** 2
                # |theta_Evertx / theta_Ez|^2
                thEvertx_Ez = (bunit[1]) ** 2
                # |theta_Evertx / theta_bz|^2
                thEvertx_bz = (E[1]) ** 2
                # |theta_Evertx / theta_by|^2
                thEvertx_by = (E[2]) ** 2
                # |dEvertx|^2
                dEvertx = thEvertx_Ey * dEy + thEvertx_Ez * dEz + thEvertx_bz * dbz + thEvertx_by * dby
                # ######### E_verty #########
                # |theta_Everty / theta_Ez|^2
                thEverty_Ez = (bunit[0]) ** 2
                # |theta_Everty / theta_Ex|^2
                thEverty_Ex = (bunit[2]) ** 2
                # |theta_Everty / theta_bx|^2
                thEverty_bx = (E[2]) ** 2
                # |theta_Everty / theta_bz|^2
                thEverty_bz = (E[0]) ** 2
                # |dEverty|^2
                dEverty = thEverty_Ez * dEz + thEverty_Ex * dEx + thEverty_bx * dbx + thEverty_bz * dbz
                # ######### E_vertz #########
                # |theta_Evertz / theta_Ex|^2
                thEvertz_Ex = (bunit[1]) ** 2
                # |theta_Evertz / theta_Ey|^2
                thEvertz_Ey = (bunit[0]) ** 2
                # |theta_Evertz / theta_by|^2
                thEvertz_by = (E[0]) ** 2
                # |theta_Evertz / theta_bx|^2
                thEvertz_bx = (E[1]) ** 2
                # |dEvertz|^2
                dEvertz = thEvertz_Ex * dEx + thEvertz_Ey * dEy + thEvertz_by * dby + thEvertz_bx * dbx
                # ############################ JOULE HEATING ERROR ############################
                # #############################################################################
                # densities error in m^(-3)
                # Electric field perpendicular to magnetic field
                # Evert = E cross bunit
                Evertx = E[1] * bunit[2] - E[2] * bunit[1]
                Everty = E[2] * bunit[0] - E[0] * bunit[2]
                Evertz = E[0] * bunit[1] - E[1] * bunit[0]

                # E vertical vector
                Evert = [Evertx, Everty, Evertz]

                # Neutral wind perpendicular to magnetic field
                # Unvert = Un cross bunit
                Un_vertx = Un[1] * bunit[2] - Un[2] * bunit[1]
                Un_verty = Un[2] * bunit[0] - Un[0] * bunit[2]
                Un_vertz = Un[0] * bunit[1] - Un[1] * bunit[0]

                # Un perpendicular to magnetic field vector
                Un_vert = [Un_vertx, Un_verty, Un_vertz]

                # Unvert cross B vector
                UnvertXBx = Un_vert[1] * B[2] - Un_vert[2] * B[1]
                UnvertXBy = Un_vert[2] * B[0] - Un_vert[0] * B[2]
                UnvertXBz = Un_vert[0] * B[1] - Un_vert[1] * B[0]
                UnvXB = [UnvertXBx, UnvertXBy, UnvertXBz]

                # Estar: perpendicular electric field in the neutral frame, Estar = Evert + Unvert cross B
                # vector addition
                Estar_x = Evert[0] + UnvXB[0]
                Estar_y = Evert[1] + UnvXB[1]
                Estar_z = Evert[2] + UnvXB[2]

                Estar = [Estar_x, Estar_y, Estar_z]

                # |theta_JH / theta_Ne|^2
                thJH_Ne = (factors.Joule_Heating[lat, lon, lev] / (factors.Ne[lat, lon, lev] * factors.ccm)) ** 2
                # |theta_JH / theta_Vi_vertx|^2
                thJH_Vi_vertx = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * Estar[0]) ** 2
                # |theta_JH / theta_Vi_verty|^2
                thJH_Vi_verty = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * Estar[1]) ** 2
                # |theta_JH / theta_Vi_vertz|^2
                thJH_Vi_vertz = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * Estar[2]) ** 2
                # |theta_JH / theta_Un_vertx|^2
                thJH_Un_vertx = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (Vi_vert[2] * B[1] - Vi_vert[1] * B[2] - Evert[0])) ** 2
                # |theta_JH / theta_Un_verty|^2
                thJH_Un_verty = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (Vi_vert[0] * B[2] - Vi_vert[2] * B[0] - Evert[1])) ** 2
                # |theta_JH / theta_Un_vertz|^2
                thJH_Un_vertz = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (Vi_vert[1] * B[0] - Vi_vert[0] * B[1] - Evert[2])) ** 2
                # |theta_JH / theta_Evertx|^2
                thJH_Evertx = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (Vi_vert[0] - Un_vert[0])) ** 2
                # |theta_JH / theta_Everty|^2
                thJH_Everty = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (Vi_vert[1] - Un_vert[1])) ** 2
                # |theta_JH / theta_Evertz|^2
                thJH_Evertz = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (Vi_vert[2] - Un_vert[2])) ** 2
                # |theta_JH / theta_Bx|^2
                thJH_Bx = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (Vi_vert[1] * Un_vert[2] - Vi_vert[2] * Un_vert[1])) ** 2
                # |theta_JH / theta_By|^2
                thJH_By = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (Vi_vert[2] * Un_vert[0] - Vi_vert[0] * Un_vert[2])) ** 2
                # |theta_JH / theta_Bz|^2
                thJH_Bz = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (Vi_vert[0] * Un_vert[1] - Vi_vert[1] * Un_vert[0])) ** 2

                # |dJH|
                factors.Joule_Heating_error[lat, lon, lev] = np.sqrt(thJH_Ne * dNe * factors.ccm ** 2 + thJH_Vi_vertx * dVix + thJH_Vi_verty * dViy +
                                                             thJH_Vi_vertz * dViz + thJH_Un_vertx * dUn_vertx + thJH_Un_verty * dUn_verty +
                                                             thJH_Un_vertz * dUn_vertz + thJH_Evertx * dEvertx + thJH_Everty * dEverty +
                                                             thJH_Evertz * dEvertz + thJH_Bx * dBx + thJH_By * dBy + thJH_Bz * dBz)
                # ######################################### Joule Heating contributions error #########################################
                # squared
                factors.dJH_B[lat, lon, lev] = thJH_Bx * dBx + thJH_Un_verty * thUn_verty_bx * dbx + thJH_Un_vertz * thUn_vertz_bx * dbx + \
                                       thJH_Everty * thEverty_bx * dbx + thJH_Evertz * thEvertz_bx * dbx + thJH_By * dBy + \
                                       thJH_Un_vertx * thUn_vertx_by * dby + thJH_Un_vertz * thUn_vertz_by * dby + \
                                       thJH_Evertx * thEvertx_by * dby + thJH_Evertz * thEvertz_by * dby + thJH_Bz * dBz + \
                                       thJH_Un_vertx * thUn_vertx_bz * dbz + thJH_Un_verty * thUn_verty_bz * dbz + \
                                       thJH_Evertx * thEvertx_bz * dbz + thJH_Everty * thEverty_bz * dbz
                factors.dJH_E[lat, lon, lev] = thJH_Evertx * thEvertx_Ey * dEy + thJH_Evertx * thEvertx_Ez * dEz + \
                                       thJH_Everty * thEverty_Ex * dEx + thJH_Everty * thEverty_Ez * dEz + thJH_Evertz * thEvertz_Ex * dEx + \
                                       thJH_Evertz * thEvertz_Ey * dEy
                factors.dJH_Vi[lat, lon, lev] = thJH_Vi_vertx * dVix + thJH_Vi_verty * dViy + thJH_Vi_vertz * dViz
                factors.dJH_Un[lat, lon, lev] = thJH_Un_vertx * thUn_vertx_Uny * dUny + thJH_Un_vertx * thUn_vertx_Unz * dUnz + \
                                        thJH_Un_verty * thUn_verty_Unx * dUnx + thJH_Un_verty * thUn_verty_Unz * dUnz + \
                                        thJH_Un_vertz * thUn_vertz_Unx * dUnx + thJH_Un_vertz * thUn_vertz_Unx * dUnx
                factors.dJH_Ne[lat, lon, lev] = thJH_Ne * dNe * factors.ccm ** 2
                # ######################################################################################################################
                # ############################ OHMIC HEATING ERROR ############################
                # #############################################################################
                # |theta_OH / theta_sigmaP|^2
                thOH_sigmaP = (Estar[0] ** 2 + Estar[1] ** 2 + Estar[2] ** 2) ** 2
                # |theta_OH /theta_Evertx|^2
                thOH_Evertx = (2 * factors.pedersen_con[lat, lon, lev] * Estar[0]) ** 2
                # |theta_OH /theta_Everty|^2
                thOH_Everty = (2 * factors.pedersen_con[lat, lon, lev] * Estar[1]) ** 2
                # |theta_OH /theta_Evertz|^2
                thOH_Evertz = (2 * factors.pedersen_con[lat, lon, lev] * Estar[2]) ** 2
                # |theta_OH / thetaUn_vertx|^2
                thOH_Un_vertx = (2 * factors.pedersen_con[lat, lon, lev] * (B[1] * Estar[2] - B[2] * Estar[1])) ** 2
                # |theta_OH / thetaUn_verty|^2
                thOH_Un_verty = (2 * factors.pedersen_con[lat, lon, lev] * (B[2] * Estar[0] - B[0] * Estar[2])) ** 2
                # |theta_OH / thetaUn_vertz|^2
                thOH_Un_vertz = (2 * factors.pedersen_con[lat, lon, lev] * (B[0] * Estar[1] - B[1] * Estar[0])) ** 2
                # |theta_OH / theta_Bx|^2
                thOH_Bx = (2 * factors.pedersen_con[lat, lon, lev] * (Un[2] * Estar[1] - Un[1] * Estar[2])) ** 2
                # |theta_OH / theta_By|^2
                thOH_By = (2 * factors.pedersen_con[lat, lon, lev] * (Un[0] * Estar[2] - Un[2] * Estar[0])) ** 2
                # |theta_OH / theta_Bz|^2
                thOH_Bz = (2 * factors.pedersen_con[lat, lon, lev] * (Un[1] * Estar[0] - Un[0] * Estar[1])) ** 2

                # |dOH|
                factors.Ohmic_Heating_error[lat, lon, lev] = np.sqrt(thOH_sigmaP * factors.pedersen_con_error[lat, lon, lev] ** 2 + thOH_Evertx * dEvertx +
                                                             thOH_Everty * dEverty + thOH_Evertz * dEvertz + thOH_Un_vertx * dUn_vertx +
                                                             thOH_Un_verty * dUn_verty + thOH_Un_vertz * dUn_vertz + thOH_Bx * dBx +
                                                             thOH_By * dBy + thOH_Bz * dBz)
                # ######################################### Ohmic Heating contributions error #########################################
                # squared
                factors.dOH_B[lat, lon, lev] = thOH_Bx * dBx + thOH_By * dBy + thOH_Bz * dBz + thOH_sigmaP * factors.dsp_B[lat, lon, lev] + \
                                       thOH_Evertx * thEvertx_by * dby + thOH_Evertx * thEvertx_bz * dbz + thOH_Everty * thEverty_bx * dbx + \
                                       thOH_Everty * thEverty_bz * dbz + thOH_Evertz * thEvertz_bx * dbx + thOH_Evertz * thEvertz_by * dby + \
                                       thOH_Un_vertx * thUn_vertx_by * dby + thOH_Un_vertx * thUn_vertx_bz * dbz + \
                                       thOH_Un_verty * thUn_verty_bx * dbx + thOH_Un_verty * thUn_verty_bz * dbz + \
                                       thOH_Un_vertz * thUn_vertz_bx * dbx + thOH_Un_vertz * thUn_vertz_by * dby
                factors.dOH_E[lat, lon, lev] = thOH_Evertx * thEvertx_Ey * dEy + thOH_Evertx * thEvertx_Ez * dEz + thOH_Everty * thEverty_Ex * dEx + \
                                       thOH_Everty * thEverty_Ez * dEz + thOH_Evertz * thEvertz_Ex * dEx + thOH_Evertz * thEvertz_Ey * dEy
                factors.dOH_Un[lat, lon, lev] = thOH_Un_vertx * thUn_vertx_Uny * dUny + thOH_Un_vertx * thUn_vertx_Unz * dUnz + \
                                        thOH_Un_verty * thUn_verty_Unx * dUnx + thOH_Un_verty * thUn_verty_Unz * dUnz + \
                                        thOH_Un_vertz * thUn_vertz_Unx * dUnx + thOH_Un_vertz * thUn_vertz_Uny * dUny
                factors.dOH_Nion[lat, lon, lev] = thOH_sigmaP * factors.dsp_Nion[lat, lon, lev]
                factors.dOH_Nneutral[lat, lon, lev] = thOH_sigmaP * factors.dsp_Nneutral[lat, lon, lev]
                factors.dOH_Ne[lat, lon, lev] = thOH_sigmaP * factors.dsp_Ne[lat, lon, lev]
                factors.dOH_Te[lat, lon, lev] = thOH_sigmaP * factors.dsp_Te[lat, lon, lev]
                factors.dOH_Ti[lat, lon, lev] = thOH_sigmaP * factors.dsp_Ti[lat, lon, lev]
                factors.dOH_Tn[lat, lon, lev] = thOH_sigmaP * factors.dsp_Tn[lat, lon, lev]
                factors.dOH_sp[lat, lon, lev] = thOH_sigmaP * factors.pedersen_con_error[lat, lon, lev] ** 2
                # #####################################################################################################################
                # ############################ FRICTIONAL HEATING ERROR ############################
                # ##################################################################################
                # densities error in m^(-3)
                termFH_Op = factors.mkO * factors.nu_Op_sum[lat, lon, lev] * factors.NOp[lat, lon, lev] * factors.ccm
                termFH_O2p = factors.mkO2 * factors.nu_O2p_sum[lat, lon, lev] * factors.NO2p[lat, lon, lev] * factors.ccm
                termFH_NOp = factors.mkNO * factors.nu_NOp_sum[lat, lon, lev] * factors.NNOp[lat, lon, lev] * factors.ccm

                # ion velocity - neutral wind difference vector
                DV = [Vi_vert[0] - Un_vert[0], Vi_vert[1] - Un_vert[1], Vi_vert[2] - Un_vert[2]]

                # |theta_FH / theta_Vi_vertx|^2
                thFH_Vi_vertx = (2 * (DV[0]) * (termFH_Op + termFH_O2p + termFH_NOp)) ** 2
                # |theta_FH / theta_Vi_verty|^2
                thFH_Vi_verty = (2 * (DV[1]) * (termFH_Op + termFH_O2p + termFH_NOp)) ** 2
                # |theta_FH / theta_Vi_vertz|^2
                thFH_Vi_vertz = (2 * (DV[2]) * (termFH_Op + termFH_O2p + termFH_NOp)) ** 2
                # |theta_FH / theta_Un_vertx|^2
                thFH_Un_vertx = thFH_Vi_vertx
                # |theta_FH / theta_Un_verty|^2
                thFH_Un_verty = thFH_Vi_verty
                # |theta_FH / theta_Un_vertz|^2
                thFH_Un_vertz = thFH_Vi_vertz
                # |theta_FH / theta_NOp|^2
                thFH_NOp = (factors.mkO * factors.nu_Op_sum[lat, lon, lev] * (DV[0] ** 2 + DV[1] ** 2 + DV[2] ** 2)) ** 2
                # |theta_FH / theta_NO2p|^2
                thFH_NO2p = (factors.mkO2 * factors.nu_O2p_sum[lat, lon, lev] * (DV[0] ** 2 + DV[1] ** 2 + DV[2] ** 2)) ** 2
                # |theta_FH / theta_NNOp|^2
                thFH_NNOp = (factors.mkNO * factors.nu_NOp_sum[lat, lon, lev] * (DV[0] ** 2 + DV[1] ** 2 + DV[2] ** 2)) ** 2
                # |theta_FH / theta_nuOp|^2
                thFH_nuOp = (factors.mkO * factors.NOp[lat, lon, lev] * factors.ccm * (DV[0] ** 2 + DV[1] ** 2 + DV[2] ** 2)) ** 2
                # |theta_FH / theta_nuO2p|^2
                thFH_nuO2p = (factors.mkO2 * factors.NO2p[lat, lon, lev] * factors.ccm * (DV[0] ** 2 + DV[1] ** 2 + DV[2] ** 2)) ** 2
                # |theta_FH / theta_nuNOp|^2
                thFH_nuNOp = (factors.mkNO * factors.NNOp[lat, lon, lev] * factors.ccm * (DV[0] ** 2 + DV[1] ** 2 + DV[2] ** 2)) ** 2

                # |dFH|
                factors.Frictional_Heating_error[lat, lon, lev] = np.sqrt(thFH_Vi_vertx * dVix + thFH_Vi_verty * dViy + thFH_Vi_vertz * dViz +
                                                                  thFH_Un_vertx * dUn_vertx + thFH_Un_verty * dUn_verty +
                                                                  thFH_Un_vertz * dUn_vertz + thFH_NOp * dNOp * factors.ccm ** 2 +
                                                                  thFH_NO2p * dNO2p * factors.ccm ** 2 + thFH_NNOp * dNNOp * factors.ccm ** 2 +
                                                                  thFH_nuOp * factors.nuOp_error[lat, lon, lev] ** 2 +
                                                                  thFH_nuO2p * factors.nuO2p_error[lat, lon, lev] ** 2 +
                                                                  thFH_nuNOp * factors.nuNOp_error[lat, lon, lev] ** 2)
                # ############################# Frictional Heating contributions error #############################
                # squared
                factors.dFH_B[lat, lon, lev] = thFH_Un_vertx * thUn_vertx_by * dby + thFH_Un_vertx * thUn_vertx_bz * dbz + \
                                       thFH_Un_verty * thUn_verty_bx * dbx + thFH_Un_verty * thUn_verty_bz * dbz + \
                                       thFH_Un_vertz * thUn_vertz_bx * dbx + thFH_Un_vertz * thUn_vertz_by * dby
                factors.dFH_Un[lat, lon, lev] = thFH_Un_vertx * thUn_vertx_Uny * dUny + thFH_Un_vertx * thUn_vertx_Unz * dUnz + \
                                        thFH_Un_verty * thUn_verty_Unx * dUnx + thFH_Un_verty * thUn_verty_Unz * dUnz + \
                                        thFH_Un_vertz * thUn_vertz_Unx * dUnx + thFH_Un_vertz * thUn_vertz_Uny * dUny
                factors.dFH_Vi[lat, lon, lev] = thFH_Vi_vertx * dVix + thFH_Vi_verty * dViy + thFH_Vi_vertz * dViz
                factors.dFH_Nion[lat, lon, lev] = thFH_NOp * dNOp * factors.ccm ** 2 + thFH_NO2p * dNO2p * factors.ccm ** 2 + thFH_NNOp * dNNOp * factors.ccm ** 2
                factors.dFH_Nneutral[lat, lon, lev] = thFH_nuOp * (thOp_O_NO * dNO + thOp_O2_NO2 * dNO2 + thOp_N2_NN2 * dNN2) + \
                                              thFH_nuO2p * (thO2p_O_NO * dNO + thO2p_O2_NO2 * dNO2 + thO2p_N2_NN2 * dNN2) + \
                                              thFH_nuNOp * (thNOp_O_NO * dNO + thNOp_O2_NO2 * dNO2 + thNOp_N2_NN2 * dNN2)
                factors.dFH_Ti[lat, lon, lev] = thFH_nuOp * thOp_O_Ti * dTi + thFH_nuO2p * thO2p_O2_Ti * dTi
                factors.dFH_Tn[lat, lon, lev] = thFH_nuOp * thOp_O_Tn * dTn + thFH_nuO2p * thO2p_O2_Tn * dTn
                factors.dFH_nu[lat, lon, lev] = thFH_nuOp * factors.nuOp_error[lat, lon, lev] ** 2 + thFH_nuO2p * factors.nuO2p_error[lat, lon, lev] ** 2 + \
                                        thFH_nuNOp * factors.nuNOp_error[lat, lon, lev] ** 2
                # ####################################################################################################
                # ########################## CROSS SECTIONS ERROR ##########################
                # nu(in Hz), N(in m^(-3)), T(in kelvin), mass(in kg)
                N_neutral = factors.NO[lat, lon, lev] + factors.NO2[lat, lon, lev] + factors.NN2[lat, lon, lev]
                N_neutral = N_neutral * factors.ccm
                nu_ion = factors.nu_Op_sum[lat, lon, lev] + factors.nu_O2p_sum[lat, lon, lev] + factors.nu_NOp_sum[lat, lon, lev]
                nu_ion = nu_ion / 3
                m_ion = factors.mkO + factors.mkO2 + factors.mkNO
                m_ion = m_ion / 3
                # |dnu_ion|^2
                dnu_ion = (factors.nuOp_error[lat, lon, lev] ** 2 + factors.nuO2p_error[lat, lon, lev] ** 2 + factors.nuNOp_error[lat, lon, lev] ** 2) / 3
                # |dN_neutral|^2
                dN_neutral = dNO * factors.ccm ** 2 + dNO2 * factors.ccm ** 2 + dNN2 * factors.ccm ** 2
                # ############ O+ ###########
                # |theta_COp / theta_nuOp|^2
                thCOp_nuOp = (np.sqrt(factors.mkO / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) / N_neutral) ** 2
                # |theta_COp / theta_N_neutral|^2
                thCOp_N_neutral = (factors.nu_Op_sum[lat, lon, lev] * np.sqrt(factors.mkO / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) / N_neutral ** 2) ** 2
                # |theta_COp / theta_Ti|^2
                thCOp_Ti = (factors.nu_Op_sum[lat, lon, lev] * np.sqrt(factors.mkO / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) /
                            (2 * N_neutral * factors.Ti[lat, lon, lev])) ** 2
                # |dCOp|
                factors.C_Op_error[lat, lon, lev] = np.sqrt(thCOp_nuOp * factors.nuOp_error[lat, lon, lev] ** 2 + thCOp_N_neutral * dN_neutral +
                                                    thCOp_Ti * dTi)
                # ############ O2+ ############
                # |theta_CO2p / theta_nuO2p|^2
                thCO2p_nuO2p = (np.sqrt(factors.mkO2 / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) / N_neutral) ** 2
                # |theta_CO2p / theta_N_neutral|^2
                thCO2p_N_neutral = (factors.nu_O2p_sum[lat, lon, lev] * np.sqrt(factors.mkO2 / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) / N_neutral ** 2) ** 2
                # |theta_CO2p / theta_Ti|^2
                thCO2p_Ti = (factors.nu_O2p_sum[lat, lon, lev] * np.sqrt(factors.mkO2 / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) /
                             (2 * N_neutral * factors.Ti[lat, lon, lev])) ** 2
                # |dCOp|
                factors.C_O2p_error[lat, lon, lev] = np.sqrt(thCO2p_nuO2p * factors.nuO2p_error[lat, lon, lev] ** 2 + thCO2p_N_neutral * dN_neutral +
                                                     thCO2p_Ti * dTi)
                # ############ NO+ ############
                # |theta_CNOp / theta_nuNOp|^2
                thCNOp_nuNOp = (np.sqrt(factors.mkNO / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) / N_neutral) ** 2
                # |theta_CNOp / theta_N_neutral|^2
                thCNOp_N_neutral = (factors.nu_NOp_sum[lat, lon, lev] * np.sqrt(factors.mkNO / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) / N_neutral ** 2) ** 2
                # |theta_CNOp / theta_Ti|^2
                thCNOp_Ti = (factors.nu_NOp_sum[lat, lon, lev] * np.sqrt(factors.mkNO / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) /
                             (2 * N_neutral * factors.Ti[lat, lon, lev])) ** 2
                # |dCNOp|
                factors.C_NOp_error[lat, lon, lev] = np.sqrt(thCNOp_nuNOp * factors.nuNOp_error[lat, lon, lev] ** 2 + thCNOp_N_neutral * dN_neutral +
                                                     thCNOp_Ti * dTi)
                # ############ ion #############
                # |theta_Cion / theta_nu_ion|^2
                thCion_nuion = (np.sqrt(m_ion / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) / N_neutral) ** 2
                # |theta_Cion / theta_N_neutral|^2
                thCion_N_neutral = (nu_ion * np.sqrt(m_ion / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) / N_neutral ** 2) ** 2
                # |theta_Cion / theta_Ti|^2
                thCion_Ti = (nu_ion * np.sqrt(m_ion / (2 * factors.boltzmann * factors.Ti[lat, lon, lev])) / (2 * N_neutral * factors.Ti[lat, lon, lev])) ** 2
                # |dCion|
                factors.C_ion_error[lat, lon, lev] = np.sqrt(thCion_nuion * dnu_ion + thCion_N_neutral * dN_neutral + thCion_Ti * dTi)
                # ###################################### Cross section contributions error ######################################
                # squared
                factors.dCion_Ti[lat, lon, lev] = thCion_Ti * dTi + thCion_nuion * (thOp_O_Ti * dTi + thO2p_O2_Ti * dTi) / 3
                factors.dCion_Tn[lat, lon, lev] = thCion_nuion * (thOp_O_Tn * dTn + thO2p_O2_Tn * dTn) / 3
                factors.dCion_nu[lat, lon, lev] = thCion_nuion * dnu_ion
                factors.dCion_Nneutral[lat, lon, lev] = thCion_N_neutral * dN_neutral + thCion_nuion * (
                                                thOp_O_NO * dNO + thOp_O2_NO2 * dNO2 + thOp_N2_NN2 * dNN2 + thO2p_O_NO * dNO +
                                                thO2p_O2_NO2 * dNO2 + thO2p_N2_NN2 * dNN2 + thNOp_O_NO * dNO + thNOp_O2_NO2 * dNO2 +
                                                thNOp_N2_NN2 * dNN2) / 3
                # ###############################################################################################################
                # ########################## CURRENTS ERROR PROPAGATION ##########################
                # #################### 1st Methodology - Ohms law ####################
                # ########### Pedersen current error ###########
                mag = np.sqrt(Estar[0] ** 2 + Estar[1] ** 2 + Estar[2] ** 2)

                # |theta_JP / theta_sigmaP|^2
                thJp_sigmaP = mag ** 2
                # |theta_JP / theta_Evertx|^2
                thJp_Evertx = (factors.pedersen_con[lat, lon, lev] * Estar[0] / mag) ** 2
                # |theta_JP / theta_Everty|^2
                thJp_Everty = (factors.pedersen_con[lat, lon, lev] * Estar[1] / mag) ** 2
                # |theta_JP / theta_Evertz|^2
                thJp_Evertz = (factors.pedersen_con[lat, lon, lev] * Estar[2] / mag) ** 2
                # |theta_JP / theta_Un_vertx|^2
                thJp_Un_vertx = (factors.pedersen_con[lat, lon, lev] * (B[1] * Estar[2] - B[2] * Estar[1]) / mag) ** 2
                # |theta_JP / theta_Un_verty|^2
                thJp_Un_verty = (factors.pedersen_con[lat, lon, lev] * (B[2] * Estar[0] - B[0] * Estar[2]) / mag) ** 2
                # |theta_JP / theta_Un_vertz|^2
                thJp_Un_vertz = (factors.pedersen_con[lat, lon, lev] * (B[0] * Estar[1] - B[1] * Estar[0]) / mag) ** 2
                # |theta_JP / theta_Bx|^2
                thJp_Bx = (factors.pedersen_con[lat, lon, lev] * (Un_vert[2] * Estar[1] - Un_vert[1] * Estar[2]) / mag) ** 2
                # |theta_JP / theta_By|^2
                thJp_By = (factors.pedersen_con[lat, lon, lev] * (Un_vert[0] * Estar[2] - Un_vert[2] * Estar[0]) / mag) ** 2
                # |theta_JP / theta_Bz|^2
                thJp_Bz = (factors.pedersen_con[lat, lon, lev] * (Un_vert[1] * Estar[0] - Un_vert[0] * Estar[1]) / mag) ** 2

                # |dJP|
                factors.J_pedersen_error[lat, lon, lev] = np.sqrt(thJp_sigmaP * factors.pedersen_con_error[lat, lon, lev] ** 2 + thJp_Evertx * dEvertx +
                                                          thJp_Everty * dEverty + thJp_Evertz * dEvertz + thJp_Un_vertx * dUn_vertx +
                                                          thJp_Un_verty * dUn_verty + thJp_Un_vertz * dUn_vertz + thJp_Bx * dBx +
                                                          thJp_By * dBy + thJp_Bz * dBz)
                # ############# Hall current error #############
                x = bunit[1] * Estar[2] - bunit[2] * Estar[1]
                y = bunit[2] * Estar[0] - bunit[0] * Estar[2]
                z = bunit[0] * Estar[1] - bunit[1] * Estar[0]
                mag1 = np.sqrt(x ** 2 + y ** 2 + z ** 2)

                # |theta_JH / theta_sigmaH|^2
                thJh_sigmaH = mag1 ** 2
                # |theta_JH / theta_Evertx|^2
                thJh_Evertx = (factors.hall_con[lat, lon, lev] * (bunit[2] * y - bunit[1] * z) / mag1) ** 2
                # |theta_JH / theta_Everty|^2
                thJh_Everty = (factors.hall_con[lat, lon, lev] * (bunit[0] * z - bunit[2] * x) / mag1) ** 2
                # |theta_JH / theta_Evertz|^2
                thJh_Evertz = (factors.hall_con[lat, lon, lev] * (bunit[1] * x - bunit[0] * y) / mag1) ** 2
                # |theta_JH / theta_bx|^2
                thJh_bx = (factors.hall_con[lat, lon, lev] * (Estar[1] * z - Estar[2] * y) / mag1) ** 2
                # |theta_JH / theta_by|^2
                thJh_by = (factors.hall_con[lat, lon, lev] * (Estar[2] * x - Estar[0] * z) / mag1) ** 2
                # |theta_JH / theta_bz|^2
                thJh_bz = (factors.hall_con[lat, lon, lev] * (Estar[0] * y - Estar[1] * x) / mag1) ** 2
                # |theta_JH / theta_Bx|^2
                thJh_Bx = (factors.hall_con[lat, lon, lev] * (- x * (bunit[1] * Un_vert[1] + bunit[2] * Un_vert[2]) +
                                                      bunit[0] * (Un_vert[1] * y + Un_vert[2] * z)) / mag1) ** 2
                # |theta_JH / theta_By|^2
                thJh_By = (factors.hall_con[lat, lon, lev] * (- y * (bunit[0] * Un_vert[0] + bunit[2] * Un_vert[2]) +
                                                      bunit[1] * (Un_vert[0] * x + Un_vert[2] * z)) / mag1) ** 2
                # |theta_JH / theta_Bz|^2
                thJh_Bz = (factors.hall_con[lat, lon, lev] * (- z * (bunit[0] * Un_vert[0] + bunit[1] * Un_vert[1]) +
                                                      bunit[2] * (Un_vert[0] * x + Un_vert[1] * y)) / mag1) ** 2
                # |theta_JH / theta_Un_vertx|^2
                thJh_Un_vertx = (factors.hall_con[lat, lon, lev] * (x * (bunit[1] * B[1] + bunit[2] * B[2]) - bunit[0] *
                                                            (B[1] * y + B[2] * z)) / mag1) ** 2
                # |theta_JH / theta_Un_verty|^2
                thJh_Un_verty = (factors.hall_con[lat, lon, lev] * (y * (bunit[0] * B[0] + bunit[2] * B[2]) - bunit[1] *
                                                            (B[0] * x + B[2] * z)) / mag1) ** 2
                # |theta_JH / theta_Un_vertz|^2
                thJh_Un_vertz = (factors.hall_con[lat, lon, lev] * (z * (bunit[0] * B[0] + bunit[1] * B[1]) - bunit[2] *
                                                            (B[0] * x + B[1] * y)) / mag1) ** 2

                # |dJh|
                factors.J_hall_error[lat, lon, lev] = np.sqrt(thJh_sigmaH * factors.hall_con_error[lat, lon, lev] ** 2 + thJh_Evertx * dEvertx +
                                                      thJh_Everty * dEverty + thJh_Evertz * dEvertz + thJh_bx * dbx + thJh_by * dby +
                                                      thJh_bz * dbz + thJh_Bx * dBx + thJh_By * dBy + thJh_Bz * dBz +
                                                      thJh_Un_vertx * dUn_vertx + thJh_Un_verty * dUn_verty + thJh_Un_vertz * dUn_vertz)
                # ############################## TOTAL CURRENT ERROR J_OHMIC ##############################
                x1 = factors.pedersen_con[lat, lon, lev] * Estar[0] + factors.hall_con[lat, lon, lev] * x
                y1 = factors.pedersen_con[lat, lon, lev] * Estar[1] + factors.hall_con[lat, lon, lev] * y
                z1 = factors.pedersen_con[lat, lon, lev] * Estar[2] + factors.hall_con[lat, lon, lev] * z
                mag2 = np.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2)

                # |theta_Johm / theta_sigmaP|^2
                thJohm_sigmaP = ((x1 * Estar[0] + y1 * Estar[1] + z1 * Estar[2]) / mag2) ** 2
                # |theta_Johm / theta_sigmaH|^2
                thJohm_sigmaH = ((x1 * x + y1 * y + z1 * z) / mag2) ** 2
                # |theta_Johm / theta_Evertx|^2
                thJohm_Evertx = ((x1 * factors.pedersen_con[lat, lon, lev] + factors.hall_con[lat, lon, lev] *
                                  (y1 * bunit[2] - z1 * bunit[1])) / mag2) ** 2
                # |theta_Johm / theta_Everty|^2
                thJohm_Everty = ((y1 * factors.pedersen_con[lat, lon, lev] + factors.hall_con[lat, lon, lev] *
                                  (z1 * bunit[0] - x1 * bunit[2])) / mag2) ** 2
                # |theta_Johm / theta_Evertz|^2
                thJohm_Evertz = ((z1 * factors.pedersen_con[lat, lon, lev] + factors.hall_con[lat, lon, lev] *
                                  (x1 * bunit[1] - y1 * bunit[0])) / mag2) ** 2
                # |theta_Johm / theta_Un_vertx|^2
                thJohm_Un_vertx = ((x1 * factors.hall_con[lat, lon, lev] * (B[1] * bunit[1] + B[2] * bunit[2]) -
                                    y1 * (factors.pedersen_con[lat, lon, lev] * B[2] + factors.hall_con[lat, lon, lev] * B[1] * bunit[0]) +
                                    z1 * (factors.pedersen_con[lat, lon, lev] * B[1] - factors.hall_con[lat, lon, lev] * B[2] * bunit[0])) / mag2) ** 2
                # |theta_Johm / theta_Un_verty|^2
                thJohm_Un_verty = ((y1 * factors.hall_con[lat, lon, lev] * (B[2] * bunit[2] + B[0] * bunit[0]) -
                                    z1 * (factors.pedersen_con[lat, lon, lev] * B[0] + factors.hall_con[lat, lon, lev] * B[2] * bunit[1]) +
                                    x1 * (factors.pedersen_con[lat, lon, lev] * B[2] - factors.hall_con[lat, lon, lev] * B[0] * bunit[1])) / mag2) ** 2
                # |theta_Johm / theta_Un_vertz|^2
                thJohm_Un_vertz = ((z1 * factors.hall_con[lat, lon, lev] * (B[0] * bunit[0] + B[1] * bunit[1]) -
                                    x1 * (factors.pedersen_con[lat, lon, lev] * B[1] + factors.hall_con[lat, lon, lev] * B[1] * bunit[2]) +
                                    y1 * (factors.pedersen_con[lat, lon, lev] * B[0] - factors.hall_con[lat, lon, lev] * B[1] * bunit[2])) / mag2) ** 2
                # |theta_Johm / theta_bx|^2
                thJohm_bx = ((factors.hall_con[lat, lon, lev] * (z1 * Estar[1] - y1 * Estar[2])) / mag2) ** 2
                # |theta_Johm / theta_by|^2
                thJohm_by = ((factors.hall_con[lat, lon, lev] * (x1 * Estar[2] - z1 * Estar[0])) / mag2) ** 2
                # |theta_Johm / theta_bz|^2
                thJohm_bz = ((factors.hall_con[lat, lon, lev] * (y1 * Estar[0] - x1 * Estar[1])) / mag2) ** 2
                # |theta_Johm / theta_Bx|^2
                thJohm_Bx = ((- x1 * factors.hall_con[lat, lon, lev] * (Un_vert[1] * bunit[1] + Un_vert[2] * bunit[2]) +
                              y1 * (factors.pedersen_con[lat, lon, lev] * Un_vert[2] + factors.hall_con[lat, lon, lev] * Un_vert[1] * bunit[0]) +
                              z1 * (factors.hall_con[lat, lon, lev] * Un_vert[2] * bunit[0] - factors.pedersen_con[lat, lon, lev] * Un_vert[1])) / mag2) ** 2
                # |theta_Johm / theta_By|^2
                thJohm_By = ((- y1 * factors.hall_con[lat, lon, lev] * (Un_vert[2] * bunit[2] + Un_vert[0] * bunit[0]) +
                              z1 * (factors.pedersen_con[lat, lon, lev] * Un_vert[0] + factors.hall_con[lat, lon, lev] * Un_vert[2] * bunit[1]) +
                              x1 * (factors.hall_con[lat, lon, lev] * Un_vert[0] * bunit[1] - factors.pedersen_con[lat, lon, lev] * Un_vert[2])) / mag2) ** 2
                # |theta_Johm / theta_Bz|^2
                thJohm_Bz = ((- z1 * factors.hall_con[lat, lon, lev] * (Un_vert[0] * bunit[0] + Un_vert[1] * bunit[1]) +
                              x1 * (factors.pedersen_con[lat, lon, lev] * Un_vert[1] + factors.hall_con[lat, lon, lev] * Un_vert[0] * bunit[2]) +
                              y1 * (factors.hall_con[lat, lon, lev] * Un_vert[1] * bunit[2] - factors.pedersen_con[lat, lon, lev] * Un_vert[0])) / mag2) ** 2

                # |dJohmic|
                factors.J_ohmic_error[lat, lon, lev] = np.sqrt(thJohm_sigmaP * factors.pedersen_con_error[lat, lon, lev] ** 2 +
                                                       thJohm_sigmaH * factors.hall_con_error[lat, lon, lev] ** 2 + thJohm_Evertx * dEvertx +
                                                       thJohm_Everty * dEverty + thJohm_Evertz * dEvertz + thJohm_Un_vertx * dUn_vertx +
                                                       thJohm_Un_verty * dUn_verty + thJohm_Un_vertz * dUn_vertz + thJohm_bx * dbx +
                                                       thJohm_by * dby + thJohm_bz * dbz + thJohm_Bx * dBx + thJohm_By * dBy + thJohm_Bz * dBz)
                # ######################################### Johmic contributions error #########################################
                # squared
                factors.dJohm_B[lat, lon, lev] = thJohm_bx * dbx + thJohm_by * dby + thJohm_bz * dbz + thJohm_Bx * dBx + thJohm_By * dBy + thJohm_Bz * dBz + \
                                         thJohm_sigmaP * factors.dsp_B[lat, lon, lev] + thJohm_sigmaH * factors.dsh_B[lat, lon, lev] + \
                                         thJohm_Evertx * thEvertx_by * dby + thJohm_Evertx * thEvertx_bz * dbz + thJohm_Everty * thEverty_bx * dbx + \
                                         thJohm_Everty * thEverty_bz * dbz + thJohm_Evertz * thEvertz_bx * dbx + thJohm_Evertz * thEvertz_by * dby + \
                                         thJohm_Un_vertx * thUn_vertx_by * dby + thJohm_Un_vertx * thUn_vertx_bz * dbz + \
                                         thJohm_Un_verty * thUn_verty_bx * dbx + thJohm_Un_verty * thUn_verty_bz * dbz + \
                                         thJohm_Un_vertz * thUn_vertz_bx * dbx + thJohm_Un_vertz * thUn_vertz_by * dby
                factors.dJohm_E[lat, lon, lev] = thJohm_Evertx * thEvertx_Ey * dEy + thJohm_Evertx * thEvertx_Ez * dEz + thJohm_Everty * thEverty_Ex * dEx + \
                                         thJohm_Everty * thEverty_Ez * dEz + thJohm_Evertz * thEvertz_Ex * dEx + thJohm_Evertz * thEvertz_Ey * dEy
                factors.dJohm_Un[lat, lon, lev] = thJohm_Un_vertx * thUn_vertx_Uny * dUny + thJohm_Un_vertx * thUn_vertx_Unz * dUnz + \
                                          thJohm_Un_verty * thUn_verty_Unx * dUnx + thJohm_Un_verty * thUn_verty_Unz * dUnz + \
                                          thJohm_Un_vertz * thUn_vertz_Unx * dUnx + thJohm_Un_vertz * thUn_vertz_Uny * dUny
                factors.dJohm_sp[lat, lon, lev] = thJohm_sigmaP * factors.pedersen_con_error[lat, lon, lev] ** 2
                factors.dJohm_sh[lat, lon, lev] = thJohm_sigmaH * factors.hall_con_error[lat, lon, lev] ** 2
                factors.dJohm_Ti[lat, lon, lev] = thJohm_sigmaP * factors.dsp_Ti[lat, lon, lev] + thJohm_sigmaH * factors.dsh_Ti[lat, lon, lev]
                factors.dJohm_Tn[lat, lon, lev] = thJohm_sigmaP * factors.dsp_Tn[lat, lon, lev] + thJohm_sigmaH * factors.dsh_Tn[lat, lon, lev]
                factors.dJohm_Te[lat, lon, lev] = thJohm_sigmaP * factors.dsp_Te[lat, lon, lev] + thJohm_sigmaH * factors.dsh_Te[lat, lon, lev]
                factors.dJohm_Ne[lat, lon, lev] = thJohm_sigmaP * factors.dsp_Ne[lat, lon, lev] + thJohm_sigmaH * factors.dsh_Ne[lat, lon, lev]
                factors.dJohm_Nneutral[lat, lon, lev] = thJohm_sigmaP * factors.dsp_Nneutral[lat, lon, lev] + thJohm_sigmaH * factors.dsh_Nneutral[lat, lon, lev]
                factors.dJohm_Nion[lat, lon, lev] = thJohm_sigmaP * factors.dsp_Nion[lat, lon, lev] + thJohm_sigmaH * factors.dsh_Nion[lat, lon, lev]
                # ##############################################################################################################
                # #################### 2nd Methodology - Densities current (current definition) ####################
                x2 = Vi_vert[0] - Un_vert[0] + (Estar[2] * B[1] - Estar[1] * B[2]) / Bnorm ** 2
                y2 = Vi_vert[1] - Un_vert[1] + (Estar[0] * B[2] - Estar[2] * B[0]) / Bnorm ** 2
                z2 = Vi_vert[2] - Un_vert[2] + (Estar[1] * B[0] - Estar[0] * B[1]) / Bnorm ** 2
                mag3 = np.sqrt(x2 ** 2 + y2 ** 2 + z2 ** 2)

                # |theta_Jd / theta_Vi_vertx|^2
                thJd_Vi_vertx = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * x2 / mag3) ** 2
                # |theta_Jd / theta_Vi_verty|^2
                thJd_Vi_verty = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * y2 / mag3) ** 2
                # |theta_Jd / theta_Vi_vertz|^2
                thJd_Vi_vertz = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * z2 / mag3) ** 2
                # |theta_Jd / theta_Un_vertx|^2
                thJd_Un_vertx = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (x2 * ((B[2] ** 2 + B[1] ** 2) / Bnorm ** 2 - 1) - y2 * B[0] * B[1] /
                                                                 Bnorm ** 2 - z2 * B[0] * B[2] / Bnorm ** 2) / mag3) ** 2
                # |theta_Jd / theta_Un_verty|^2
                thJd_Un_verty = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (y2 * ((B[0] ** 2 + B[2] ** 2) / Bnorm ** 2 - 1) - x2 * B[0] * B[1] /
                                                                 Bnorm ** 2 - z2 * B[1] * B[2] / Bnorm ** 2) / mag3) ** 2
                # |theta_Jd / theta_Un_vertz|^2
                thJd_Un_vertz = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (z2 * ((B[0] ** 2 + B[1] ** 2) / Bnorm ** 2 - 1) - x2 * B[0] * B[2] /
                                                                 Bnorm ** 2 - y2 * B[1] * B[2] / Bnorm ** 2) / mag3) ** 2
                # |theta_Jd / theta_Evertx|^2
                thJd_Evertx = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (y2 * B[2] / Bnorm ** 2 - z2 * B[1] / Bnorm ** 2) / mag3) ** 2
                # |theta_Jd / theta_Everty|^2
                thJd_Everty = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (z2 * B[0] / Bnorm ** 2 - x2 * B[2] / Bnorm ** 2) / mag3) ** 2
                # |theta_Jd / theta_Evertz|^2
                thJd_Evertz = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (x2 * B[1] / Bnorm ** 2 - y2 * B[0] / Bnorm ** 2) / mag3) ** 2
                # |theta_Jd / theta_Bx|^2
                thJd_Bx = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (- x2 * (Un_vert[2] * B[2] + Un_vert[1] * B[1]) / Bnorm ** 2 +
                                                             y2 * (Un_vert[1] * B[0] - Estar[2]) / Bnorm ** 2 +
                                                             z2 * (Un_vert[2] * B[0] + Estar[1])) / mag3) ** 2
                # |theta_Jd / theta_By|^2
                thJd_By = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (- y2 * (Un_vert[0] * B[0] + Un_vert[2] * B[2]) / Bnorm ** 2 +
                                                             z2 * (Un_vert[2] * B[1] - Estar[0]) / Bnorm ** 2 +
                                                             x2 * (Un_vert[0] * B[1] + Estar[2])) / mag3) ** 2
                # |theta_Jd / theta_Bz|^2
                thJd_Bz = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (- z2 * (Un_vert[1] * B[1] + Un_vert[0] * B[0]) / Bnorm ** 2 +
                                                             x2 * (Un_vert[0] * B[1] - Estar[1]) / Bnorm ** 2 +
                                                             y2 * (Un_vert[1] * B[2] + Estar[0])) / mag3) ** 2
                # |theta_Jd / theta_B|^2
                thJd_B = (factors.qe * factors.Ne[lat, lon, lev] * factors.ccm * (2 * x2 * (Estar[1] * B[2] - Estar[2] * B[1]) / Bnorm ** 3 +
                                                          2 * y2 * (Estar[2] * B[0] - Estar[0] * B[2]) / Bnorm ** 3 +
                                                          2 * z2 * (Estar[0] * B[1] - Estar[1] * B[0]) / Bnorm ** 3) / mag3) ** 2
                # |theta_Jd / theta_Ne|^2
                thJd_Ne = (factors.qe * mag3) ** 2

                # |dJd|
                factors.J_dens_error[lat, lon, lev] = np.sqrt(thJd_Vi_vertx * dVix + thJd_Vi_verty * dViy + thJd_Vi_vertz * dViz +
                                                      thJd_Un_vertx * dUn_vertx + thJd_Un_verty * dUn_verty + thJd_Un_vertz * dUn_vertz +
                                                      thJd_Evertx * dEvertx + thJd_Everty * dEverty + thJd_Evertz * dEvertz + thJd_Bx * dBx +
                                                      thJd_By * dBy + thJd_Bz * dBz + thJd_B * dB + thJd_Ne * dNe * factors.ccm ** 2)
                # ###################################### J(densities) contributions error ######################################
                # squared
                factors.dJd_B[lat, lon, lev] = thJd_Bx * dBx + thJd_By * dBy + thJd_Bz * dBz + thJd_B * dB + thJd_Un_vertx * thUn_vertx_by * dby + \
                                       thJd_Un_vertx * thUn_vertx_bz * dbz + thJd_Un_verty * thUn_verty_bx * dbx + \
                                       thJd_Un_verty * thUn_verty_bz * dbz + thJd_Un_vertz * thUn_vertz_bx * dbx + \
                                       thJd_Un_vertz * thUn_vertz_by * dby + thJd_Evertx * thEvertx_by * dby + thJd_Evertx * thEvertx_bz * dbz + \
                                       thJd_Everty * thEverty_bx * dbx + thJd_Everty * thEverty_bz * dbz + thJd_Evertz * thEvertz_bx * dbx + \
                                       thJd_Evertz * thEvertz_by * dby
                factors.dJd_E[lat, lon, lev] = thJd_Evertx * thEvertx_Ey * dEy + thJd_Evertx * thEvertx_Ez * dEz + thJd_Everty * thEverty_Ex * dEx + \
                                       thJd_Everty * thEverty_Ez * dEz + thJd_Evertz * thEvertz_Ex * dEx + thJd_Evertz * thEvertz_Ey * dEy
                factors.dJd_Vi[lat, lon, lev] = thJd_Vi_vertx * dVix + thJd_Vi_verty * dViy + thJd_Vi_vertz * dViz
                factors.dJd_Un[lat, lon, lev] = thJd_Un_vertx * thUn_vertx_Uny * dUny + thJd_Un_vertx * thUn_vertx_Unz * dUnz + \
                                        thJd_Un_verty * thUn_verty_Unx * dUnx + thJd_Un_verty * thUn_verty_Unz * dUnz + \
                                        thJd_Un_vertz * thUn_vertz_Unx * dUnx + thJd_Un_vertz * thUn_vertz_Uny * dUny
                factors.dJd_Ne[lat, lon, lev] = thJd_Ne * dNe * factors.ccm ** 2
                # ##############################################################################################################
    
    # Inform user that error is ready
    print('Calculated Errors in: ', time.time() - start_time, ' sec !')
    print(' ')