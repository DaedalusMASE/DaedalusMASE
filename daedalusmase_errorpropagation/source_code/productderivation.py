'''
This file containts the functions with are used to calculate all Low Atmosphere and Ionoshpere
quantities.
models_input function used to read inputs from TIE-GCM files and store the inputs into appropriate sturctures.
Moreover this function used to run IGRM model to calculate Earth's Magnetic field components along TIE-GCM grid.
products function used to calculate all the LTI (Low atmosphre and Ionoshpere) products such as Heating rates,
Conductivities, Currents etc.

'''



import datetime
import sys
import warnings
import time
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from matplotlib import ticker
from matplotlib.colors import LogNorm
from cmcrameri import cm
import factors
import supportfunctions
my_dpi=300

# ##################################### GET INPUT FROM TIE-GCM AND I-GRF #####################################
# ############################################################################################################
def models_input(file_name, timer, lat_value=-1, lon_value=-1, pressure_level=-1):
    '''
    This function used to read TIE-GCM input file and execute the IGRF model on the points of input grid.

        Args:
        file_name (String): Input file of netcdf format, as comes from TIE-GCM output
        timer (int): timer as index of TIEGCM file, is used to obtain the utc time used in IGRF execution
        lat_value (int): Latitude as index of TIEGCM file, used to obtain the kind of function execution
        lon_value (int): Longitude as index of TIEGCM file, used to obtain the kind of function execution
        pressure_value (int): Pressure level as index of TIEGCM file, used to obtain the kind of function execution
        Latitude - Altitude map profile
        lat_value == -1, pressure_level == -1
        Lattitude - Longitude map profile
        lat_value == -1 and lon_value == -1
        Vertical profile
        lat_value != -1 and lon_value != -1:

        Returns the sturcture of input variables needed to calculate LTI products

    '''

    print(sys.version)
    warnings.filterwarnings("ignore")
    start_time = time.time()
    print('Getting data from models........')

    # Get TIE-GCM file from gui
    tiegcm_file = file_name

    # Open TIE-GCM file
    tiegcm = Dataset(tiegcm_file)

    # Input parameters from TIE-GCM
    zgmid_in = tiegcm.variables['ZGMID'][:]  # geometric height at midpoints
    factors.glat_in = tiegcm.variables['lat'][:]     # geographic latitude in deg(earth as perfect sphere)
    factors.glon_in = tiegcm.variables['lon'][:]     # geographic longitude in deg(earth as perfect sphere)
    
    factors.glev_in = tiegcm.variables['lev'][:]     # midpoint levels
    time_in = tiegcm.variables['time'][:]    # minutes since 2015-1-1 0:0:0
    O_in = tiegcm.variables['O_CM3'][:]      # atomic oxygen density (neutral) in cm^(-3)
    O2_in = tiegcm.variables['O2_CM3'][:]    # molecular oxygen density (neutral) in cm^(-3)
    N2_in = tiegcm.variables['N2_CM3'][:]    # molecular nitrogen density (neutral) in cm^(-3)

    Op_in = tiegcm.variables['OP'][:]        # atomic oxygen density (ion) in cm^(-3)
    O2p_in = tiegcm.variables['O2P'][:]      # molecular oxygen density (ion) in cm^(-3)
    NOp_in = tiegcm.variables['NOP_LAM'][:]  # nitric oxide density (ion) in cm^(-3)
    Te_in = tiegcm.variables['TE'][:]        # electron temperature in kelvin
    Tn_in = tiegcm.variables['TN'][:]        # neutral temperature in kelvin
    Ti_in = tiegcm.variables['TI'][:]        # ion temperature in kelvin
    
      
    Un_north_in = tiegcm.variables['VN'][:]/100  # neutral meridional wind (+north) in m/sec
    Un_east_in = tiegcm.variables['UN'][:]/100   # neutral zonal wind (+east) in m/sec
    Un_up_in = tiegcm.variables['WN'][:]/100     # neutral vertical wind (+up) in m/sec


    Ee_in = tiegcm.variables['EEX'][:]*100  # electric field (+east) in V/m
    En_in = tiegcm.variables['EEY'][:]*100  # electric field (+north) in V/m
    Eu_in = tiegcm.variables['EEZ'][:]*100  # electric field (+up) in V/m
    #end panagiotis edit 20220629


    # Close TIE-GCM file
    tiegcm.close()

    timeg = time_in[timer]  # time input from a TIE-GCM file for index value defined by GUI
    time_IGRF = datetime.datetime(2015, 1, 1, 0, 0, 0)         # first time step of the TIE-GCM run
    real_time = time_IGRF + datetime.timedelta(minutes=timeg)  # real time after adding file's time to initial run time

    # Distinguish Map from Vertical profile
    lev_range = 0
    lat_range = 0
    lon_range = 0

    lev_start = 0
    lat_start = 0
    lon_start = 0

    # Lat - Alt map profile
    if lat_value == -1 and pressure_level == -1:
        lev_range = len(factors.glev_in) - 1
        lat_range = len(factors.glat_in)
        lon_start = lon_value
        lon_range = lon_start + 1
        factors.title = ' Lon: ' + str(factors.glon_in[lon_value]) + ', Date/Time: ' + str(real_time) + ' (UTC)'
        factors.pngNameMap=' Lon' + str(factors.glon_in[lon_value]) + '_DateTime_' + str(real_time) + '_UTC.png'
        factors.map_time = real_time

    # Lat - Lon map profile
    if lat_value == -1 and lon_value == -1:
        lev_start = pressure_level
        lev_range = lev_start + 1
        lat_range = len(factors.glat_in)
        lon_range = len(factors.glon_in)
        factors.map_time = real_time

    # Vertical profile
    if lat_value != -1 and lon_value != -1:
        lat_start = lat_value
        lon_start = lon_value
        lat_range = lat_start + 1
        lon_range = lon_start + 1
        lev_range = len(factors.glev_in) - 1
        factors.map_time = real_time
        factors.title = ' Lat: ' + str(factors.glat_in[lat_value]) + ', ' + 'Lon: ' + str(factors.glon_in[lon_value]) + ', Date/Time: ' + str(real_time) + ' (UTC)'

    temp_lat_lon = 0    # variable used to get mean altitude for the lat-lon map plot
    for lev in range(lev_start, lev_range):
        temp_height = 0 # variable used to get mean altitude for the lat-alt map plot
        for lat in range(lat_start, lat_range):
            for lon in range(lon_start, lon_range):

                factors.heights[lat, lon, lev] = zgmid_in[timer, lev, lat, lon] / 1e5  # altitude in km

                # Average heights for Lat - Alt map
                temp_height = temp_height + factors.heights[lat, lon, lev]
                factors.heights_la[lev] = round(temp_height / lat_range)

                # Average altitude for Lat-Lon map
                temp_lat_lon = temp_lat_lon +factors.heights[lat, lon, lev]

                # Run IGRF12 model using igrf12 to get magnetic field
                               
                ##################################
                Benu,b_unit_enu=supportfunctions.igrf_B(real_time, factors.glat_in[lat], factors.glon_in[lon], factors.heights[lat, lon, lev])
                

                # Magnetic field in ENU
                Be = Be[0]  # in tesla
                Bn = Bn[1]  # in tesla
                Bu = Bu[2]  # in tesla

                # Magnetic field from ENU to ECEF (in tesla)
                factors.Bx[lat, lon, lev], factors.By[lat, lon, lev], factors.Bz[lat, lon, lev] = supportfunctions.enu_ecef(factors.glat_in[lat], factors.glon_in[lon], Be, Bn, Bu)

                # Electric field from ENU to ECEF (in V/m)
                Ee_temp = Ee_in[timer, lev, lat, lon]
                En_temp = En_in[timer, lev, lat, lon]
                Eu_temp = Eu_in[timer, lev, lat, lon]
                factors.Ex[lat, lon, lev], factors.Ey[lat, lon, lev], factors.Ez[lat, lon, lev] = supportfunctions.enu_ecef(factors.glat_in[lat], factors.glon_in[lon], Ee_temp, En_temp, Eu_temp)

                # Neutral wind from ENU to ECEF (in m/sec)
                Un_e_temp = Un_east_in[timer, lev, lat, lon]
                Un_n_temp = Un_north_in[timer, lev, lat, lon]
                Un_u_temp = Un_up_in[timer, lev, lat, lon]
                factors.Unx[lat, lon, lev], factors.Uny[lat, lon, lev], factors.Unz[lat, lon, lev] = supportfunctions.enu_ecef(factors.glat_in[lat], factors.glon_in[lon], Un_e_temp, Un_n_temp, Un_u_temp)

                # Assign densities (in cm^(-3))
                factors.NO[lat, lon, lev] = O_in[timer, lev, lat, lon]
                factors.NO2[lat, lon, lev] = O2_in[timer, lev, lat, lon]
                factors.NN2[lat, lon, lev] = N2_in[timer, lev, lat, lon]
                factors.NOp[lat, lon, lev] = Op_in[timer, lev, lat, lon]
                factors.NO2p[lat, lon, lev] = O2p_in[timer, lev, lat, lon]
                factors.NNOp[lat, lon, lev] = NOp_in[timer, lev, lat, lon]

                # Force charge neutrality ignoring other minor ion densities
                factors.Ne[lat, lon, lev] = factors.NOp[lat, lon, lev] + factors.NO2p[lat, lon, lev] + factors.NNOp[lat, lon, lev]

                # Assign temperatures (in kelvin)
                factors.Te[lat, lon, lev] = Te_in[timer, lev, lat, lon]
                factors.Ti[lat, lon, lev] = Ti_in[timer, lev, lat, lon]
                factors.Tn[lat, lon, lev] = Tn_in[timer, lev, lat, lon]

    # Get the mean value for the altitude in Lat-Lon map
    if lat_value==-1 and lon_value==-1:
        # Average altitude for the Lat-Lon map
        altitude_lat_lon = temp_lat_lon / (144 * 72) # divide by latitude x longitude size
        altitude_lat_lon = round(altitude_lat_lon)   # round the mean altitude result
        factors.title = ' Pressure level: ' + str(factors.glev_in[pressure_level]) + ' (~' + str(altitude_lat_lon) + ' km) ' + \
                'Date/Time: ' + str(real_time) + ' (UTC)'
        factors.pngNameMap='P_lev_' + str(factors.glev_in[pressure_level]) + 'Alt_' + str(altitude_lat_lon) + 'km_' + \
                'DateTime_' + str(real_time) + '_UTC.png'

    # Inform user that data from models are ready
    print('Data imported in: ', str(time.time() - start_time), ' sec!')
    print(' ')

# ################################### CALCULATE PRODUCTS USING MODEL INPUTS ###################################
# #############################################################################################################
def products(lat_value=-1, lon_value=-1, pressure_level=-1):
    '''
    This function used to calculate LTI products. THis fuction should be used after the execution of model_inputs function, 
    in order to all the required quantites are fufllilled in the appropriate structures.

        Args:
        lat_value (int): Latitude as index of TIEGCM file, used to obtain the kind of function execution
        lon_value (int): Longitude as index of TIEGCM file, used to obtain the kind of function execution
        pressure_value (int): Pressure level as index of TIEGCM file, used to obtain the kind of function execution
        Latitude - Altitude map profile
        lat_value == -1, pressure_level == -1
        Lattitude - Longitude map profile
        lat_value == -1 and lon_value == -1
        Vertical profile
        lat_value != -1 and lon_value != -1:

        Returns all the LTI pruducts structures as factors.xxx. See file factor.py lines 74 to 116

    '''
    
    start_time = time.time()
    print('Calculating Products.....')
    print(' ')
    print(factors.title)

    # distinguish Map from Vertical profile
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
                if max_bar == lev_range:
                    i = lev
                else:
                    i = lat
                # ########################## COLLISION FREQUENCIES ##########################
                # nu-Op = nu(Op-N2) + nu(Op-O2) + nu(Op-O) (in Hz)
                # densities in cm^(-3)
                nu_Op_N2 = 6.82 * factors.NN2[lat, lon, lev] * 10 ** (-10)
                nu_Op_O2 = 6.64 * factors.NO2[lat, lon, lev] * 10 ** (-10)

                Tr = (factors.Ti[lat, lon, lev] + factors.Tn[lat, lon, lev]) / 2  # in kelvin
                nu_Op_O = factors.fb * (3.67 * factors.NO[lat, lon, lev] * 10 ** (-11) * Tr ** (1 / 2) * (1 - 0.064 * np.log10(Tr)) ** 2)

                factors.nu_Op_sum[lat, lon, lev] = nu_Op_N2 + nu_Op_O2 + nu_Op_O

                # nu-O2p = nu(O2p-N2) + nu(O2p-O) + nu(O2p-O2) (in Hz)
                # densities in cm^(-3)
                nu_O2p_N2 = 4.13 * factors.NN2[lat, lon, lev] * 10 ** (-10)
                nu_O2p_O = 2.31 * factors.NO[lat, lon, lev] * 10 ** (-10)
                nu_O2p_O2 = 2.59 * factors.NO2[lat, lon, lev] * 10 ** (-11) * Tr ** (1 / 2) * (1 - 0.073 * np.log10(Tr)) ** 2

                factors.nu_O2p_sum[lat, lon, lev] = nu_O2p_N2 + nu_O2p_O + nu_O2p_O2

                # nu-NOp = nu(NOp-N2) + nu(NOp-O) + nu(NOp-O2) (in Hz)
                # densities in cm^(-3)
                nu_NOp_N2 = 4.34 * factors.NN2[lat, lon, lev] * 10 ** (-10)
                nu_NOp_O = 2.44 * factors.NO[lat, lon, lev] * 10 ** (-10)
                nu_NOp_O2 = 4.27 * factors.NO2[lat, lon, lev] * 10 ** (-10)

                factors.nu_NOp_sum[lat, lon, lev] = nu_NOp_N2 + nu_NOp_O + nu_NOp_O2

                # nu-e = nu(e-N2) + nu(e-O) + nu(e-O2) (in Hz)
                # densities in cm^(-3)
                nu_e_N2 = 2.33 * 10 ** (-11) * factors.NN2[lat, lon, lev] * factors.Te[lat, lon, lev] * (1 - 1.21 * 10 ** (-4) * factors.Te[lat, lon, lev])
                nu_e_O2 = 1.82 * 10 ** (-10) * factors.NO2[lat, lon, lev] * factors.Te[lat, lon, lev] ** (1 / 2) * \
                          (1 + 3.6 * 10 ** (-2) * factors.Te[lat, lon, lev] ** (1 / 2))
                nu_e_O = 8.9 * 10 ** (-11) * factors.NO[lat, lon, lev] * factors.Te[lat, lon, lev] ** (1 / 2) * (1 + 5.7 * 10 ** (-4) * factors.Te[lat, lon, lev])

                factors.nu_e_sum[lat, lon, lev] = nu_e_N2 + nu_e_O2 + nu_e_O
                # ################ GYRO-FREQUENCIES(OMEGAS) ################
                # Magnetic field vector (in tesla)
                B = [factors.Bx[lat, lon, lev], factors.By[lat, lon, lev], factors.Bz[lat, lon, lev]]
                # Magnetic field magnitude (in tesla)
                Bnorm = np.sqrt(B[0] ** 2 + B[1] ** 2 + B[2] ** 2)
                # Magnetic field unit vector
                bunit = [B[0] / Bnorm, B[1] / Bnorm, B[2] / Bnorm]

                # qe(in coulomb), mk(masses in kg), omegas(in Hz)
                omega_Op = (factors.qe * Bnorm) / factors.mkO
                omega_O2p = (factors.qe * Bnorm) / factors.mkO2
                omega_NOp = (factors.qe * Bnorm) / factors.mkNO
                omega_e = (factors.qe * Bnorm) / factors.me

                factors.Omega_ion[lat, lon, lev] = (omega_Op + omega_O2p + omega_NOp) / 3
                factors.Omega_e[lat, lon, lev] = omega_e
                # ################## RATIOS ##################
                # dimensionless
                r_Op = factors.nu_Op_sum[lat, lon, lev] / omega_Op
                r_O2p = factors.nu_O2p_sum[lat, lon, lev] / omega_O2p
                r_NOp = factors.nu_NOp_sum[lat, lon, lev] / omega_NOp
                r_e = factors.nu_e_sum[lat, lon, lev] / omega_e
                # ############################# CONDUCTIVITIES #############################
                # Pedersen conductivity (in siemens/meter)
                # qe(in coulomb), B_norm(in tesla), N(densities in m^(-3)), ratios(dimensionless)
                term_a_ped = (factors.Ne[lat, lon, lev] * factors.ccm) * (r_e / (1 + r_e ** 2))
                term_b_ped = (factors.NOp[lat, lon, lev] * factors.ccm) * (r_Op / (1 + r_Op ** 2))
                term_c_ped = (factors.NO2p[lat, lon, lev] * factors.ccm) * (r_O2p / (1 + r_O2p ** 2))
                term_d_ped = (factors.NNOp[lat, lon, lev] * factors.ccm) * (r_NOp / (1 + r_NOp ** 2))

                factors.pedersen_con[lat, lon, lev] = (factors.qe / Bnorm) * (term_a_ped + term_b_ped + term_c_ped + term_d_ped)

                # Hall conductivity (in siemens/meter)
                # qe(in coulomb), B_norm(in tesla), N(densities in m^(-3)), ratios(dimensionless)
                term_a_hall = (factors.Ne[lat, lon, lev] * factors.ccm) / (1 + r_e ** 2)
                term_b_hall = (factors.NOp[lat, lon, lev] * factors.ccm) / (1 + r_Op ** 2)
                term_c_hall = (factors.NO2p[lat, lon, lev] * factors.ccm) / (1 + r_O2p ** 2)
                term_d_hall = (factors.NNOp[lat, lon, lev] * factors.ccm) / (1 + r_NOp ** 2)

                factors.hall_con[lat, lon, lev] = (factors.qe / Bnorm) * (term_a_hall - term_b_hall - term_c_hall - term_d_hall)
                # Parallel conductivity (in siemens/meter)
                # qe(in coulomb), me(mass in tesla), N(density) (in m^(-3)), collision frequency(in Hz)
                factors.parallel_con[lat, lon, lev] = (factors.Ne[lat, lon, lev] * factors.ccm * factors.qe ** 2) / (factors.me * factors.nu_e_sum[lat, lon, lev])

                # ################################ HEATING RATES ################################
                # Electric field vector(in volt/meter)
                E = [factors.Ex[lat, lon, lev], factors.Ey[lat, lon, lev], factors.Ez[lat, lon, lev]]

                # Electric field perpendicular to magnetic field
                # Evert = E cross bunit
                Evertx = E[1] * bunit[2] - E[2] * bunit[1]
                Everty = E[2] * bunit[0] - E[0] * bunit[2]
                Evertz = E[0] * bunit[1] - E[1] * bunit[0]

                # E vertical vector
                Evert = [Evertx, Everty, Evertz]

                # Neutral wind vector(in meter/sec)
                Un = [factors.Unx[lat, lon, lev], factors.Uny[lat, lon, lev], factors.Unz[lat, lon, lev]]

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

                # Estar: perpendicular electric field in the neutral frame Estar = Evert + Unvert cross B
                # vector addition
                Estar_x = Evert[0] + UnvXB[0]
                Estar_y = Evert[1] + UnvXB[1]
                Estar_z = Evert[2] + UnvXB[2]

                Estar = [Estar_x, Estar_y, Estar_z]

                # Estar cross bunit
                x = Estar[1] * bunit[2] - Estar[2] * bunit[1]
                y = Estar[2] * bunit[0] - Estar[0] * bunit[2]
                z = Estar[0] * bunit[1] - Estar[1] * bunit[0]

                EstarXbunit = [x, y, z]

                # Ion velocities vectors(in meter/sec) (in neutral frame, star) perpendicular to magnetic field
                # extracted from ion momentum equations
                # ############# O+ #############
                Vi_Op_star_x = (factors.nu_Op_sum[lat, lon, lev] * omega_Op * Estar[0] + omega_Op ** 2 * EstarXbunit[0]) / \
                               (Bnorm * (factors.nu_Op_sum[lat, lon, lev] ** 2 + omega_Op ** 2))
                Vi_Op_star_y = (factors.nu_Op_sum[lat, lon, lev] * omega_Op * Estar[1] + omega_Op ** 2 * EstarXbunit[1]) / \
                               (Bnorm * (factors.nu_Op_sum[lat, lon, lev] ** 2 + omega_Op ** 2))
                Vi_Op_star_z = (factors.nu_Op_sum[lat, lon, lev] * omega_Op * Estar[2] + omega_Op ** 2 * EstarXbunit[2]) / \
                               (Bnorm * (factors.nu_Op_sum[lat, lon, lev] ** 2 + omega_Op ** 2))
                # ############# O2+ #############
                Vi_O2p_star_x = (factors.nu_O2p_sum[lat, lon, lev] * omega_O2p * Estar[0] + omega_O2p ** 2 * EstarXbunit[0]) / \
                                (Bnorm * (factors.nu_O2p_sum[lat, lon, lev] ** 2 + omega_O2p ** 2))
                Vi_O2p_star_y = (factors.nu_O2p_sum[lat, lon, lev] * omega_O2p * Estar[1] + omega_O2p ** 2 * EstarXbunit[1]) / \
                                (Bnorm * (factors.nu_O2p_sum[lat, lon, lev] ** 2 + omega_O2p ** 2))
                Vi_O2p_star_z = (factors.nu_O2p_sum[lat, lon, lev] * omega_O2p * Estar[2] + omega_O2p ** 2 * EstarXbunit[2]) / \
                                (Bnorm * (factors.nu_O2p_sum[lat, lon, lev] ** 2 + omega_O2p ** 2))
                # ############ NO+ ############
                Vi_NOp_star_x = (factors.nu_NOp_sum[lat, lon, lev] * omega_NOp * Estar[0] + omega_NOp ** 2 * EstarXbunit[0]) / \
                                (Bnorm * (factors.nu_NOp_sum[lat, lon, lev] ** 2 + omega_NOp ** 2))
                Vi_NOp_star_y = (factors.nu_NOp_sum[lat, lon, lev] * omega_NOp * Estar[1] + omega_NOp ** 2 * EstarXbunit[1]) / \
                                (Bnorm * (factors.nu_NOp_sum[lat, lon, lev] ** 2 + omega_NOp ** 2))
                Vi_NOp_star_z = (factors.nu_NOp_sum[lat, lon, lev] * omega_NOp * Estar[2] + omega_NOp ** 2 * EstarXbunit[2]) / \
                                (Bnorm * (factors.nu_NOp_sum[lat, lon, lev] ** 2 + omega_NOp ** 2))

                # Changing frame from neutral to ECEF frame (not star)
                Vi_Op_x = Vi_Op_star_x + Un_vert[0]
                Vi_O2p_x = Vi_O2p_star_x + Un_vert[0]
                Vi_NOp_x = Vi_NOp_star_x + Un_vert[0]

                Vi_Op_y = Vi_Op_star_y + Un_vert[1]
                Vi_O2p_y = Vi_O2p_star_y + Un_vert[1]
                Vi_NOp_y = Vi_NOp_star_y + Un_vert[1]

                Vi_Op_z = Vi_Op_star_z + Un_vert[2]
                Vi_O2p_z = Vi_O2p_star_z + Un_vert[2]
                Vi_NOp_z = Vi_NOp_star_z + Un_vert[2]

                # Measurements for each ion cannot be made separately so we take the average
                # no coordinate system assigned to satellite, assumed as point measurement
                # perpendicular ion velocity corresponds to measured ion velocity
                # in contrast to neutral wind, which we get as model input

                # Ion velocity perpendicular to magnetic field
                factors.Vi_vertx[lat, lon, lev] = (Vi_Op_x + Vi_O2p_x + Vi_NOp_x) / 3
                factors.Vi_verty[lat, lon, lev] = (Vi_Op_y + Vi_O2p_y + Vi_NOp_y) / 3
                factors.Vi_vertz[lat, lon, lev] = (Vi_Op_z + Vi_O2p_z + Vi_NOp_z) / 3

                # Vi perpendicular to magnetic field vector
                Vi_vert = [factors.Vi_vertx[lat, lon, lev], factors.Vi_verty[lat, lon, lev], factors.Vi_vertz[lat, lon, lev]]

                # ################################## JOULE HEATING ##################################
                # ###################################################################################
                # Joule Heating = qeNe(Vi_vert - Un_vert)dot(E_vert + Un_vert cross B)(in watt/m^3)
                # qe(in coulomb), B(in tesla), E(in volt/meter), Vi,Un(in meter/sec)
                factors.Joule_Heating[lat, lon, lev] = factors.qe * (factors.Ne[lat, lon, lev] * factors.ccm) * \
                                               (Vi_vert[0] * Estar[0] - Un_vert[0] * Evert[0] +
                                                Vi_vert[1] * Estar[1] - Un_vert[1] * Evert[1] +
                                                Vi_vert[2] * Estar[2] - Un_vert[2] * Evert[2])
                # ################################# OHMIC HEATING ###################################
                # ###################################################################################
                # Ohmic Heating = sigmaPedersen * |Evert + Unvert cross B|^2 (in watt/m^3)
                # sigmaPedersen(in siemens/meter), E(in volt/meter), Un(in meter/sec), B(in tesla)
                term_ohm_x = (Evert[0] + UnvXB[0]) ** 2
                term_ohm_y = (Evert[1] + UnvXB[1]) ** 2
                term_ohm_z = (Evert[2] + UnvXB[2]) ** 2
                factors.Ohmic_Heating[lat, lon, lev] = factors.pedersen_con[lat, lon, lev] * (term_ohm_x + term_ohm_y + term_ohm_z)
                # ############################### FRICTIONAL HEATING ################################
                # ###################################################################################
                # Frictional Heating = m_ion * nu_ion * N_ion * |Vi_vert - Un_vert|^2 (in watt/m^3)
                # m_ion(in kg), nu_ion(in Hz), N_ion(in m^(-3)), Vi,Un(in meter/sec)
                term_fric_x = (Vi_vert[0] - Un_vert[0]) ** 2
                term_fric_y = (Vi_vert[1] - Un_vert[1]) ** 2
                term_fric_z = (Vi_vert[2] - Un_vert[2]) ** 2
                term_Op = factors.mkO * factors.nu_Op_sum[lat, lon, lev] * (factors.NOp[lat, lon, lev] * factors.ccm)
                term_O2p = factors.mkO2 * factors.nu_O2p_sum[lat, lon, lev] * (factors.NO2p[lat, lon, lev] * factors.ccm)
                term_NOp = factors.mkNO * factors.nu_NOp_sum[lat, lon, lev] * (factors.NNOp[lat, lon, lev] * factors.ccm)
                factors.Frictional_Heating[lat, lon, lev] = (term_Op + term_O2p + term_NOp) * (term_fric_x + term_fric_y + term_fric_z)
                # ############################ CROSS SECTIONS ############################
                # C = (nu_ion / N_neutral) / (sqrt(2 * boltzmann * T_i / m_ion)) (in m^2)
                # nu(in Hz), N(in m^(-3)), T(in kelvin), mass(in kg)
                N_neutral = factors.NO[lat, lon, lev] + factors.NO2[lat, lon, lev] + factors.NN2[lat, lon, lev]
                N_neutral = N_neutral * factors.ccm
                # ####### O+ #######
                factors.C_Op[lat, lon, lev] = (factors.nu_Op_sum[lat, lon, lev] / N_neutral) / (np.sqrt(2 * factors.boltzmann * factors.Ti[lat, lon, lev] / factors.mkO))
                # ####### O2+ #######
                factors.C_O2p[lat, lon, lev] = (factors.nu_O2p_sum[lat, lon, lev] / N_neutral) / (np.sqrt(2 * factors.boltzmann * factors.Ti[lat, lon, lev] / factors.mkO2))
                # ####### NO+ #######
                factors.C_NOp[lat, lon, lev] = (factors.nu_NOp_sum[lat, lon, lev] / N_neutral) / (np.sqrt(2 * factors.boltzmann * factors.Ti[lat, lon, lev] / factors.mkNO))
                # ####### ION #######
                nu_ion = factors.nu_Op_sum[lat, lon, lev] + factors.nu_O2p_sum[lat, lon, lev] + factors.nu_NOp_sum[lat, lon, lev]
                # Average collision frequency
                nu_ion = nu_ion / 3  # in Hz
                m_ion = factors.mkO + factors.mkO2 + factors.mkNO
                # Average mass
                m_ion = m_ion / 3  # in kg
                # Because measurements for each species cannot be made we assume an average ion cross section
                factors.C_ion[lat, lon, lev] = (nu_ion / N_neutral) / (np.sqrt(2 * factors.boltzmann * factors.Ti[lat, lon, lev] / m_ion))
                # ################################# PERPENDICULAR CURRENTS ##############################
                # ###############################  1st Methodology - Ohms law ###########################
                # Pedersen current = sigmaPedersen * E_star = (Evert + Unvert cross B) (in ampere/meter^2)
                # sigmaPedersen(in siemens/meter), E(in volt/meter)
                J_px = factors.pedersen_con[lat, lon, lev] * Estar[0]
                J_py = factors.pedersen_con[lat, lon, lev] * Estar[1]
                J_pz = factors.pedersen_con[lat, lon, lev] * Estar[2]

                factors.J_pedersen[lat, lon, lev] = np.sqrt(J_px ** 2 + J_py ** 2 + J_pz ** 2)

                # b_unit cross E_star
                x1 = bunit[1] * Estar[2] - bunit[2] * Estar[1]
                y1 = bunit[2] * Estar[0] - bunit[0] * Estar[2]
                z1 = bunit[0] * Estar[1] - bunit[1] * Estar[0]

                # Hall current = sigmaHall * (b_unit cross E_star) (in ampere/meter^2)
                # sigmaHall(in siemens/meter), E(in volt/meter)
                J_hx = factors.hall_con[lat, lon, lev] * x1
                J_hy = factors.hall_con[lat, lon, lev] * y1
                J_hz = factors.hall_con[lat, lon, lev] * z1

                factors.J_hall[lat, lon, lev] = np.sqrt(J_hx ** 2 + J_hy ** 2 + J_hz ** 2)

                # Ohmic current = |JPedersen + JHall|
                factors.J_ohmic[lat, lon, lev] = np.sqrt((J_px + J_hx) ** 2 + (J_py + J_hy) ** 2 + (J_pz + J_hz) ** 2)

                # ####################### 2nd Methodology - Current definition #######################
                # J_density = qe * Ne * (Vi_vert_star - Ve_vert_star) (in neutral frame) or
                # J_density = qe * Ne * (Vi_vert - Ve_vert) (in ECEF frame) in ampere/meter^2

                # Ve_vert (electron velocity perpendicular to magnetic field) in meter/sec
                # Ve_vert_star = (E_star cross B) / |B|^2
                # Ve_vert = (E_star cross B) / |B|^2 + Un_vert
                # ####################################################################################
                # Estar cross B
                x2 = Estar[1] * B[2] - Estar[2] * B[1]
                y2 = Estar[2] * B[0] - Estar[0] * B[2]
                z2 = Estar[0] * B[1] - Estar[1] * B[0]

                x2 = x2 / Bnorm ** 2
                y2 = y2 / Bnorm ** 2
                z2 = z2 / Bnorm ** 2

                Ve_vertx = x2 + Un_vert[0]
                Ve_verty = y2 + Un_vert[1]
                Ve_vertz = z2 + Un_vert[2]

                Ve_vert = [Ve_vertx, Ve_verty, Ve_vertz]

                # qe(in coulomb), Ne(in m^(-3)), Vi,Ve(in meter/sec)
                J_denx = factors.qe * (factors.Ne[lat, lon, lev] * factors.ccm) * (Vi_vert[0] - Ve_vert[0])
                J_deny = factors.qe * (factors.Ne[lat, lon, lev] * factors.ccm) * (Vi_vert[1] - Ve_vert[1])
                J_denz = factors.qe * (factors.Ne[lat, lon, lev] * factors.ccm) * (Vi_vert[2] - Ve_vert[2])
                factors.J_dens[lat, lon, lev] = np.sqrt(J_denx ** 2 + J_deny ** 2 + J_denz ** 2)

    
    # Inform user that derived products are ready
    print('Products calculated in: ', time.time() - start_time, ' sec!')
    print(' ')
