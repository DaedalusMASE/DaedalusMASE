"""
This module holds all data structures necessary for the calculation of the Altitude Profiles.
It can also save and load calculation results in netcdf files.
"""
import copy
import numpy as np
import pandas as pd
import netCDF4
from netCDF4 import Dataset 
import datetime
import glob
import os
import random


MLT_duration_of_a_bin = 1
LAT_degrees_of_a_bin = 2.5
ALT_distance_of_a_bin   = 5
MLT_min = 0
MLT_max = 24
LAT_min = -90
LAT_max = +90
ALT_min = 100
ALT_max = 500
num_of_KP_bins = 2
KPsequence     = [ 0, 3 ] 
ALTsequence    = list( range( ALT_min,    ALT_max,    ALT_distance_of_a_bin  ) )
LATsequence    = list( np.arange( LAT_min,   LAT_max,    LAT_degrees_of_a_bin) )
MLTsequence    = list( range( MLT_min,    MLT_max,    MLT_duration_of_a_bin ) )

ResultFilename = ""
TypeOfCalculation = ""
Progress = 0  # integer 0 to 100
DistributionNumOfSlots = 0

def setDataParams( _MLT_min, _MLT_max, _MLT_duration_of_a_bin, _LAT_min, _LAT_max, _LAT_degrees_of_a_bin, _ALT_min, _ALT_max, _ALT_distance_of_a_bin, _num_of_KP_bins, _TypeOfCalculation, _DistributionNumOfSlots ):
    """
    Sets the data parameteres before a calculation. If not called then default values will be applied.
    These parameters define the ranges and size of each bin regarding Magnetic Local Time, Latitude, Altitude and Geomagnetic Kp index.
    
    Args:
        _MLT_min: Magnetic Local Time range
        _MLT_max: Magnetic Local Time range
        _MLT_duration_of_a_bin: the size of each bin regarding Magnetic Local Time 
        _LAT_min: Latitude range
        _LAT_max: Latitude range
        _LAT_degrees_of_a_bin: how many degrees correspond to each bin 
        _ALT_min: Alttiude range
        _ALT_max: Alttiude range
        _ALT_distance_of_a_bin: kilometers of altitude assigned to each bin
        _num_of_KP_bins: how many Kp bins will be.  
                         One leads to range 0-9, two leads to ranges 0-3 and 3-9, three leads to ranges 0-2, 2-4, 4-9.
        _TypeOfCalculation: defines the variable used for the calculations. Possible values:  
            "JH" for Joule Heating (Ohmic)  
            "JHminusWindHeat" for Joule Heating minus Wind heating  
            "PedCond" for Pedersen Conductivity  
            "HallCond" for Pedersen Conductivity  
            "EEX" for Electric Field East in V/cm 
            "EEY" for Electric Field North in V/cm
            "EEX_si" for Electric Field East in V/m
            "EEY_si" for Electric Field North in V/m
            "ConvHeat" for Convection heating  
            "WindHeat" for Wind heating  
        _DistributionNumOfSlots: the resolution for calculating distribution.
    """
    
    global MLT_min, MLT_max, MLT_duration_of_a_bin, ALT_min, ALT_max, ALT_distance_of_a_bin, LAT_min, LAT_max, LAT_degrees_of_a_bin, num_of_KP_bins,  TypeOfCalculation, DistributionNumOfSlots, KPsequence, ALTsequence, LATsequence, MLTsequence, ResultFilename
    ####
    print( "DATA params:", _MLT_min, _MLT_max, _MLT_duration_of_a_bin, _LAT_min, _LAT_max, _LAT_degrees_of_a_bin, _ALT_min, _ALT_max, _ALT_distance_of_a_bin, _num_of_KP_bins, _TypeOfCalculation, _DistributionNumOfSlots )
    MLT_duration_of_a_bin   = _MLT_duration_of_a_bin
    LAT_degrees_of_a_bin    = _LAT_degrees_of_a_bin
    ALT_distance_of_a_bin   = _ALT_distance_of_a_bin
    MLT_min = _MLT_min
    MLT_max = _MLT_max
    LAT_min = _LAT_min
    LAT_max = _LAT_max
    ALT_min = _ALT_min
    ALT_max = _ALT_max
    num_of_KP_bins = _num_of_KP_bins
    MLTsequence    = copy.deepcopy( list( np.arange( MLT_min,    MLT_max,    MLT_duration_of_a_bin ) ) )
    LATsequence    = copy.deepcopy( list( np.arange( LAT_min, LAT_max, LAT_degrees_of_a_bin) ) )
    ALTsequence    = copy.deepcopy( list( np.arange( ALT_min,    ALT_max,    ALT_distance_of_a_bin  ) ) )
    if num_of_KP_bins == 1:
        KPsequence     = copy.deepcopy( [ 0 ] )
    elif num_of_KP_bins == 2:
        KPsequence     = copy.deepcopy( [ 0, 3 ] )
    elif num_of_KP_bins == 3:    
        KPsequence     = copy.deepcopy( [ 0, 2, 4 ] )
    #
    TypeOfCalculation = _TypeOfCalculation
    DistributionNumOfSlots = _DistributionNumOfSlots
    # construct the results filename and check if exists so that you do not overwrite it
    ResultFilename = "results/" + TypeOfCalculation + "__"
    ResultFilename += "MLT" + "_" + str(MLT_min) + "_" + str(MLT_max) + "_" + str(MLT_duration_of_a_bin) + "_"
    ResultFilename += "LAT" + "_" + str(LAT_min) + "_" + str(LAT_max) + "_" + str(LAT_degrees_of_a_bin) + "_"
    ResultFilename += "ALT" + "_" + str(ALT_min) + "_" + str(ALT_max) + "_" + str(ALT_distance_of_a_bin) + "_"
    ResultFilename += "Kp" + str(num_of_KP_bins) + "Bins"
    ResultFilename += ".nc"
    ResultFilename = ResultFilename.replace(".0", "")
    
    
                    
def init_ResultDataStructure():
    """
    Initializes the dictionaries where the calculation data will be stored
    
    Returns: a reference to the data structure created.
    """
    Bins = dict()
    for aKP in KPsequence:
        for anALT in ALTsequence:
            for aLat in LATsequence:
                for aMLT in MLTsequence:
                    Bins[(aKP, anALT, aLat, aMLT, "Sum")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Len")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Vals")] = list()
                    Bins[(aKP, anALT, aLat, aMLT, "Weights")] = list() # each weight is associated with each value
                    Bins[(aKP, anALT, aLat, aMLT, "Percentile10")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Percentile25")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Percentile50")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Percentile75")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Percentile90")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Variance")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Minimum")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Maximum")] = 0
                    Bins[(aKP, anALT, aLat, aMLT, "Distribution")] = [0] * DistributionNumOfSlots
                    
    return Bins



def LocatePositionInBins( aKp, anALT, aLat, aMLT ):
    """
    Given the position as described in the arguments, it returns the bin information in which the position should be assigned. 
    """
    kp_to_fall = alt_to_fall = lat_to_fall = mlt_to_fall = None
    # find correct Alt
    for tmp in ALTsequence:
        if anALT>=tmp and anALT<tmp+ALT_distance_of_a_bin:
            alt_to_fall=tmp
            break
    if alt_to_fall is None and anALT==ALTsequence[-1]+ALT_distance_of_a_bin: alt_to_fall=ALTsequence[-1]
    # find correct kp
    if num_of_KP_bins == 1:
        kp_to_fall = 0
    elif num_of_KP_bins == 2:
        if aKp < 3: 
            kp_to_fall = 0
        else:
            kp_to_fall = 3
    elif num_of_KP_bins == 3:
        if aKp < 2: 
            kp_to_fall = 0
        elif aKp < 4: 
            kp_to_fall = 2
        else:
            kp_to_fall = 4
    # find correct MLT
    if MLTsequence[-1] < 24:
        for tmp in MLTsequence:
            if aMLT>=tmp and aMLT<tmp+MLT_duration_of_a_bin: 
                mlt_to_fall=tmp
                break
        if mlt_to_fall is None and aMLT==MLTsequence[-1]+MLT_duration_of_a_bin: mlt_to_fall=MLTsequence[-1] # for last position
    else:
        MLT_to_check = aMLT
        if MLT_to_check < MLTsequence[0]: MLT_to_check+=24
        for tmp in MLTsequence:
            if MLT_to_check>=tmp and MLT_to_check<tmp+MLT_duration_of_a_bin: 
                mlt_to_fall=tmp
                break
        if mlt_to_fall is None and MLT_to_check==MLTsequence[-1]+MLT_duration_of_a_bin: mlt_to_fall=MLTsequence[-1] # for last position
    # find correct Lat
    for tmp in LATsequence:
        if aLat>=tmp and aLat<tmp+LAT_degrees_of_a_bin:
            lat_to_fall=tmp
            break
    if lat_to_fall is None and aLat==LATsequence[-1]+LAT_degrees_of_a_bin: lat_to_fall=LATsequence[-1]
    #
    return  kp_to_fall, alt_to_fall, lat_to_fall, mlt_to_fall



def WriteResultsToCDF(ResultBins, ResultFilename, VariableName, Units):
    """
    Writes the calculated data into a netcdf file.
    
    Args:
        ResultBins: the data structure holding the data for saving. It is created by init_ResultDataStructure().
        ResultFilename: the netcdf filename where the calculation results will be saved. 
        VariableName: the name of the variable used for the calculations.
        Units: units of the variable.
    """
    resultsCDF = Dataset( ResultFilename, 'w' )
    # add attributes defining the results file - TODO: add more attributes
    resultsCDF.DateOfCreation = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    resultsCDF.VariableName = VariableName
    resultsCDF.Units = Units
    resultsCDF.TypeOfCalculation = TypeOfCalculation
    # Create dimensions
    resultsCDF.createDimension( "dim_MLT", len(MLTsequence) )
    resultsCDF.createDimension( "dim_LAT", len(LATsequence) )
    resultsCDF.createDimension( "dim_KP", len(KPsequence) )
    resultsCDF.createDimension( "dim_ALT", len(ALTsequence) )
    resultsCDF.createDimension( "dim_distribution", DistributionNumOfSlots )
    # Create variables
    VAR_MLT = resultsCDF.createVariable( "MLT", "f4", "dim_MLT" )
    VAR_MLT[:] = MLTsequence
    VAR_LAT = resultsCDF.createVariable( "LAT", "f4", "dim_LAT" )
    VAR_LAT[:] = LATsequence
    VAR_KP = resultsCDF.createVariable( "KP", "f4", "dim_KP" )
    VAR_KP[:] = KPsequence
    VAR_ALT = resultsCDF.createVariable( "ALT", "f4", "dim_ALT" )
    VAR_ALT[:] = ALTsequence
    #
    VAR_BinSums = resultsCDF.createVariable( "BinSums", "f4", ('dim_KP', 'dim_ALT', 'dim_LAT', 'dim_MLT') )
    VAR_BinLens = resultsCDF.createVariable( "BinLens", "f4", ('dim_KP', 'dim_ALT', 'dim_LAT', 'dim_MLT') )
    VAR_Percentile10=resultsCDF.createVariable( "Percentile10", "f4", ('dim_KP','dim_ALT','dim_LAT','dim_MLT'))
    VAR_Percentile25=resultsCDF.createVariable( "Percentile25", "f4", ('dim_KP','dim_ALT','dim_LAT','dim_MLT'))
    VAR_Percentile50=resultsCDF.createVariable( "Percentile50", "f4", ('dim_KP','dim_ALT','dim_LAT','dim_MLT'))
    VAR_Percentile75=resultsCDF.createVariable( "Percentile75", "f4", ('dim_KP','dim_ALT','dim_LAT','dim_MLT'))
    VAR_Percentile90=resultsCDF.createVariable( "Percentile90", "f4", ('dim_KP','dim_ALT','dim_LAT','dim_MLT'))
    VAR_Variance=resultsCDF.createVariable( "Variance", "f4", ('dim_KP','dim_ALT','dim_LAT','dim_MLT'))
    VAR_Minimum=resultsCDF.createVariable( "Minimum", "f4", ('dim_KP','dim_ALT','dim_LAT','dim_MLT'))
    VAR_Maximum=resultsCDF.createVariable( "Maximum", "f4", ('dim_KP','dim_ALT','dim_LAT','dim_MLT'))
    if DistributionNumOfSlots > 0:
        VAR_Distribution=resultsCDF.createVariable( "Distribution", "i4",('dim_KP','dim_ALT','dim_LAT','dim_MLT','dim_distribution'))
    for aKP in KPsequence:
        for anALT in ALTsequence:
            for aLat in LATsequence:
                for aMLT in MLTsequence:
                    vector = (KPsequence.index(aKP), ALTsequence.index(anALT), LATsequence.index(aLat), MLTsequence.index(aMLT))
                    VAR_BinSums[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Sum")]
                    VAR_BinLens[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Len")]
                    VAR_Percentile10[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Percentile10")]
                    VAR_Percentile25[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Percentile25")]
                    VAR_Percentile50[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Percentile50")]
                    VAR_Percentile75[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Percentile75")]
                    VAR_Percentile90[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Percentile90")]
                    VAR_Variance[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Variance")]
                    VAR_Minimum[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Minimum")]
                    VAR_Maximum[vector] = ResultBins[(aKP, anALT, aLat, aMLT, "Maximum")]
                    if DistributionNumOfSlots > 0:
                        for i in range(0, DistributionNumOfSlots):
                            VAR_Distribution[vector+(i,)] = ResultBins[(aKP, anALT, aLat, aMLT, "Distribution")][i]
                    
    resultsCDF.close()
    

    
def LoadResultsCDF( _ResultFilename ):
    """
    Reads a calculations result netcdf file, fills the data structure and returns a reference to it. 
    
    Returns:
        ResultBins: the data structure holding the loaded data.
        BinSums: used for distribution calculation
        BinLens: used for distribution calculation
        VariableName: the variable used for the result-calculations in the file. 
        Units: the units of the variable.
    """
    global MLT_min, MLT_max, MLT_duration_of_a_bin
    global ALT_min, ALT_max, ALT_distance_of_a_bin 
    global LAT_min, LAT_max, LAT_degrees_of_a_bin
    global num_of_KP_bins, ResultFilename, TypeOfCalculation
    global KPsequence, ALTsequence, LATsequence, MLTsequence
    
    ResultFilename = _ResultFilename
    
    # open result file
    try:
        CDFroot = Dataset( ResultFilename, 'r' )
    except:
        print ( "Loading Error:", ResultFilename, ". File does not exits or has wrong format." )
        return

    # read atributes
    DateOfCreation = CDFroot.DateOfCreation
    VariableName = CDFroot.VariableName
    Units = CDFroot.Units
    TypeOfCalculation = CDFroot.TypeOfCalculation
    
    # read results
    MLTs    = CDFroot.variables['MLT'][:]         
    LATs    = CDFroot.variables['LAT'][:] 
    ALTs    = CDFroot.variables['ALT'][:]
    KPs     = CDFroot.variables['KP'][:]        
    BinSums = CDFroot.variables['BinSums'][:, :, :, :] 
    BinLens = CDFroot.variables['BinLens'][:, :, :, :]
    P10 = CDFroot.variables['Percentile10'][:, :, :, :]
    P25 = CDFroot.variables['Percentile25'][:, :, :, :]
    P50 = CDFroot.variables['Percentile50'][:, :, :, :]
    P75 = CDFroot.variables['Percentile75'][:, :, :, :]
    P90 = CDFroot.variables['Percentile90'][:, :, :, :]
    try:
        Variances = CDFroot.variables['Variance'][:, :, :, :]
        Minimums = CDFroot.variables['Minimum'][:, :, :, :]
        Maximums = CDFroot.variables['Maximum'][:, :, :, :]
        Distribution = CDFroot.variables['Distribution'][:, :, :, :, :]    
    except:
        pass
    
    # apply loaded info to data structures
    MLT_duration_of_a_bin = MLTs[1] - MLTs[0]
    MLT_min = MLTs[0]
    MLT_max = MLTs[-1] + MLT_duration_of_a_bin
    #
    if len(LATs)==1:
        LAT_degrees_of_a_bin = 180
    else:
        LAT_degrees_of_a_bin = LATs[1] - LATs[0]
    LAT_min = LATs[0]
    LAT_max = LATs[-1] + LAT_degrees_of_a_bin
    #
    if len(ALTs)==1:
        ALT_distance_of_a_bin = 5
    else:
        ALT_distance_of_a_bin = ALTs[1] - ALTs[0]
    ALT_min = ALTs[0]
    ALT_max = ALTs[-1] + ALT_distance_of_a_bin
    #
    num_of_KP_bins = len(KPs)

    # reconstruct sequences
    MLTsequence  = list( np.arange( MLT_min,  MLT_max,  MLT_duration_of_a_bin ) )
    LATsequence = list( np.arange( LAT_min, LAT_max, LAT_degrees_of_a_bin) )
    ALTsequence  = list( np.arange( ALT_min,  ALT_max,  ALT_distance_of_a_bin  ) )
    
    if num_of_KP_bins == 1:
        KPsequence     = [ 0 ] 
    elif num_of_KP_bins == 2:
        KPsequence     = [ 0, 3 ] 
    elif num_of_KP_bins == 3:    
        KPsequence     = [ 0, 2, 4 ] 
        
    # assign data to the bins
    ResultBins = init_ResultDataStructure()
    for idx_kp in range(0, len(BinSums)):
        for idx_alt in range(0, len(BinSums[0])):
            for idx_mlat in range(0, len(BinSums[0,0])):
                for idx_mlt in range(0, len(BinSums[0,0,0])):
                    aKP     = KPs[idx_kp]
                    anALT   = ALTs[idx_alt]
                    aLat = LATs[idx_mlat]
                    aMLT    = MLTs[idx_mlt]
                    ResultBins[(aKP, anALT, aLat, aMLT, "Sum")] = BinSums[idx_kp, idx_alt, idx_mlat, idx_mlt]
                    ResultBins[(aKP, anALT, aLat, aMLT, "Len")] = BinLens[idx_kp, idx_alt, idx_mlat, idx_mlt]
                    ResultBins[(aKP, anALT, aLat, aMLT, "Percentile10")] = P10[idx_kp, idx_alt, idx_mlat, idx_mlt]
                    ResultBins[(aKP, anALT, aLat, aMLT, "Percentile25")] = P25[idx_kp, idx_alt, idx_mlat, idx_mlt]
                    ResultBins[(aKP, anALT, aLat, aMLT, "Percentile50")] = P50[idx_kp, idx_alt, idx_mlat, idx_mlt]
                    ResultBins[(aKP, anALT, aLat, aMLT, "Percentile75")] = P75[idx_kp, idx_alt, idx_mlat, idx_mlt]
                    ResultBins[(aKP, anALT, aLat, aMLT, "Percentile90")] = P90[idx_kp, idx_alt, idx_mlat, idx_mlt]
                    try:
                        ResultBins[(aKP, anALT, aLat, aMLT, "Variance")] = Variances[idx_kp, idx_alt, idx_mlat, idx_mlt]
                        ResultBins[(aKP, anALT, aLat, aMLT, "Minimum")] = Minimums[idx_kp, idx_alt, idx_mlat, idx_mlt]
                        ResultBins[(aKP, anALT, aLat, aMLT, "Maximum")] = Maximums[idx_kp, idx_alt, idx_mlat, idx_mlt]
                        
                        # for distribution
                        ResultBins[(aKP, anALT, aLat, aMLT, "Distribution")] = [0] * len(Distribution[0,0,0,0,:])
                        for i in range(0, len(Distribution[0,0,0,0,:])):
                            ResultBins[(aKP, anALT, aLat, aMLT, "Distribution")][i] = Distribution[idx_kp, idx_alt, idx_mlat, idx_mlt, i]
                    except:
                        pass
                    
    # verbose
    print( "Opened ", ResultFilename, ":"  )
    print("   DateOfCreation:", DateOfCreation, " TypeOfCalculation:", TypeOfCalculation )
    print("   Variable:", VariableName, " Units:", Units, " filled bins:", np.count_nonzero(BinSums), "/", len(BinSums)*len(BinSums[0])*len(BinSums[0][0])*len(BinSums[0][0][0]), " Num of Kp bins:", num_of_KP_bins)
    print("   MLT:", MLT_min, "-", MLT_max, "step", MLT_duration_of_a_bin, "  Alt.:", ALT_min, "-", ALT_max, "step", ALT_distance_of_a_bin, "  Mag.Lat.:", LAT_min, "-", LAT_max, "step", LAT_degrees_of_a_bin)
    print("\n")
    
    # clean up
    CDFroot.close()
    return ResultBins, BinSums, BinLens, VariableName, Units
    

def mergeResultCDFs( CDF_filenames, mergedFilename ):
    """
    Merges several cdf result files into a single one.
    
    Args:
        CDF_filenames: string with wildcards, describing the files to be merged
        mergedFilename: string with the filename of the final merged file
    """

    AllCDFfilenames = sorted( glob.glob( CDF_filenames ) )
    MergedBins = init_ResultDataStructure()
    for CDF_filename in AllCDFfilenames:
        # read a file
        ResultBins, BinSums, BinLens, VariableName, Units = LoadResultsCDF( CDF_filename )
        # merge it 
        for aKP in KPsequence:
            for anALT in ALTsequence:
                for aLat in LATsequence:
                    for aMLT in MLTsequence:
                        MergedBins[(aKP, anALT, aLat, aMLT, "Sum")] += ResultBins[(aKP, anALT, aLat, aMLT, "Sum")]
                        MergedBins[(aKP, anALT, aLat, aMLT, "Len")] += ResultBins[(aKP, anALT, aLat, aMLT, "Len")]
        # delete file
        os.remove( CDF_filename )
    # save merged data
    WriteResultsToCDF(MergedBins, mergedFilename, VariableName, Units)
        
