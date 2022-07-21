"""
This module includes functions which initiate the calculation of Altitude Profiles.
The function the user should call to initate a calculation is called "StartCalculating(...)". 
This function spawns one process for each source netcdf file. These processes save their results into temporary binary files.
After they all finish, "StartCalculating(...)" merges all results into a netcdf result-file.
"""

# local imports
import Data

# system imports
import netCDF4
from netCDF4 import Dataset 
import os
import datetime
import time
import glob
import shutil
import math
import numpy as np
import multiprocessing
import sys
from pathlib import Path
import random
from array import array

DEBUG_ENABLED = False # if true then the subprocesses print debug info in debug files. Useful because process cannot print on stdout

def CalcSurfaceAreaBetweenLatitudes( Lat1, Lat2 ):
    """
    Calculates and returns the area on the surface of the Earth between Lat1 and Lat2.
    It assumes the Earth is a sphere with a radius of 6371km.
    
    Args:
        Lat1 (real): a latitude
        Lat2 (real): a latitude
        
    Returns:
        The area between the two latitudes on the Earth's surface
    """
    result = math.sin(math.radians(Lat1)) - math.sin(math.radians(Lat2))
    result = 2 * math.pi * 6371 * result
    result = abs( result )
    return result
                                                     
                                                     

def StartCalculating( NetCDF_files_path, ResultFilename, TypeOfCalculation, TmpFilesPath, DeleteTmpFiles, Num_of_CalculationProcesses,   _MLT_min, _MLT_max, _MLT_duration_of_a_bin, _LAT_min, _LAT_max, _LAT_degrees_of_a_bin, _ALT_min, _ALT_max, _ALT_distance_of_a_bin, _num_of_KP_bins, _DistributionNumOfSlots, LatStep_for_WeightedAverage):
    """
    Initiate the calculation of Altitude Profiles. 
    The calculation is executed upon data from the TIEGCM model and the results are stored into a netcdf file.
    For each TIEGCM file one process is spawned, which saves its results into temporary binary files.
    After all processes finish, the temporary files are merged to create the results netcdf file.
    
    Args:
        NetCDF_files_path (string): the folder where TIEGCM model files are stored. 
        ResultFilename (string): the netcdf file where the calculation results will be stored
        TypeOfCalculation (string): the variable which will be used for the calculations. Possible values:  
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
        TmpFilesPath (string): a folder where temporary files regarding the calculation will be stored.
        DeleteTmpFiles (boolean): whether the temporary files will be deleted after calculation finishes. 
        They can be ussed to continue a calculation after an intermediate halt. 
        Num_of_CalculationProcesses (int): how many processes will be spawned at the same time max, so that the calculation is parallel.
        There will be one process per sourcefile.
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
        _DistributionNumOfSlots: the resolution for calculating the Distribution of the values in the Bin.
        LatStep_for_WeightedAverage: Higher latitudes correspond to less surface area. 
            Thus, it is logical that values from different latitudes to have different impact on the calulation of average. 
            This value should match the grid size of the tiegcm source data.
            Possible values:  
            negative: normal average will be used for the calculations
            zero: default test values are used for latitudes 68.75, 71.25, 73.75, 76.25
            positive: the Bin is sliced by latitude of this magnitude and values falling in each slice have their own weight
    """
    startSecs = time.time()
    print( "START", datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") )
    
    Data.setDataParams(_MLT_min, _MLT_max, _MLT_duration_of_a_bin, _LAT_min, _LAT_max, _LAT_degrees_of_a_bin, _ALT_min, _ALT_max, _ALT_distance_of_a_bin, _num_of_KP_bins, TypeOfCalculation, _DistributionNumOfSlots)
    
    if not os.path.exists(TmpFilesPath):
        os.makedirs(TmpFilesPath)
    
    Allprocesses = list()
    AllCDFfiles = sorted( glob.glob( NetCDF_files_path, recursive=True ) )
    print( datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") )
    print( "I will calculate '" + TypeOfCalculation + "' on", len(AllCDFfiles), "files in", NetCDF_files_path, "\n" )
    print( "Results will be stored in '" + ResultFilename + "'\n" )
    
    # del older partial txt files - there is one file for each bin containing all values in it
    if DeleteTmpFiles:
        try:
            shutil.rmtree( TmpFilesPath )
        except:
            pass
        
    num_of_processes = 0
    for CDF_file in AllCDFfiles:
        
        #print("-----------------------------------------------") # for debugging, so that prints errors on stdout
        #PROC_StatsCalculator(222, CDF_file, TypeOfCalculation, TmpFilesPath,    _MLT_min, _MLT_max, _MLT_duration_of_a_bin, _LAT_min, _LAT_max, _LAT_degrees_of_a_bin, _ALT_min, _ALT_max, _ALT_distance_of_a_bin, _num_of_KP_bins, _DistributionNumOfSlots, LatStep_for_WeightedAverage)
        #print("-----------------------------------------------")
        
        num_of_processes += 1
        Data.Progress = int( 100 * num_of_processes/len(AllCDFfiles))
        
        # spawn new process
        print( "Spawning process", num_of_processes, ", reading",  CDF_file)    
        print( Data.ALT_min, Data.ALT_max, Data.ALT_distance_of_a_bin, Data.LAT_min, Data.LAT_max)
        print(Data.ALTsequence)
        P = multiprocessing.Process(target=PROC_StatsCalculator, args=(num_of_processes,CDF_file,TypeOfCalculation,TmpFilesPath,     _MLT_min, _MLT_max, _MLT_duration_of_a_bin, _LAT_min, _LAT_max, _LAT_degrees_of_a_bin, _ALT_min, _ALT_max, _ALT_distance_of_a_bin, _num_of_KP_bins, _DistributionNumOfSlots, LatStep_for_WeightedAverage))
        Allprocesses.append(P)
        P.start()
        
        pause_spawning = True
        while pause_spawning:
            Num_of_alive_processes = 0        
            for P in Allprocesses:
                if P.is_alive():
                    Num_of_alive_processes += 1            
            if Num_of_alive_processes >= Num_of_CalculationProcesses:
                pause_spawning = True
                time.sleep(12)
            else:
                pause_spawning = False
        
           
    # wait for all processes to terminate
    for T in Allprocesses: T.join()
        
    # every process creates a partial file, merge all of them into one
    print( "Merging partial data files and calculating result values...",  datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    ResultBins = Data.init_ResultDataStructure()
    NumOfBins = len(Data.KPsequence) * len(Data.ALTsequence) * len(Data.LATsequence) * len(Data.MLTsequence)
    CurrBinNum = 0
    
    for aKP in Data.KPsequence:
        for anALT in Data.ALTsequence:
            for aLat in Data.LATsequence:
                for aMLT in Data.MLTsequence:
                    CurrBinNum += 1
                    Data.Progress = int( 100 * CurrBinNum/NumOfBins )
                    AllBinValues = list()
                    for i in range(1,num_of_processes+1): # read all partial files for this bin 
                        partialDataFolder = TmpFilesPath+"proc"+ f"{i:03}" +"/"
                        if os.path.isdir(partialDataFolder)==False:
                            #print( "There are no partial data files for process", i )
                            continue
                        partialTextFilename = partialDataFolder + str(aKP)+"_"+str(anALT)+"_"+str(aLat)+"_"+str(aMLT)+".txt"
                        if os.path.exists(partialTextFilename) == False: # no hits for this bin from this process
                            #print(partialTextFilename, "does not exist")
                            continue
                            
                        f = open(partialTextFilename, "rb")
                        float_array = array('d')
                        float_array.frombytes(f.read())
                        AllBinValues += float_array.tolist()
                        f.close()
                        
                    print("BIN", "Kp"+str(aKP), "Alt"+str(anALT), "Lat"+str(aLat), "MLT"+str(aMLT), "", len(AllBinValues), "items" )
                        
                    if len(AllBinValues) > 0:
                        ResultBins[aKP, anALT, aLat, aMLT, "Sum"] = np.sum(AllBinValues)
                        ResultBins[aKP, anALT, aLat, aMLT, "Len"] = len(AllBinValues)
                        ResultBins[aKP, anALT, aLat, aMLT, "Percentile10"] = np.percentile(AllBinValues, 10)
                        ResultBins[aKP, anALT, aLat, aMLT, "Percentile25"] = np.percentile(AllBinValues, 25)
                        ResultBins[aKP, anALT, aLat, aMLT, "Percentile50"] = np.percentile(AllBinValues, 50)
                        ResultBins[aKP, anALT, aLat, aMLT, "Percentile75"] = np.percentile(AllBinValues, 75)
                        ResultBins[aKP, anALT, aLat, aMLT, "Percentile90"] = np.percentile(AllBinValues, 90)
                        ResultBins[aKP, anALT, aLat, aMLT, "Variance"] = np.var(AllBinValues)
                        ResultBins[aKP, anALT, aLat, aMLT, "Minimum"] = np.nanmin(AllBinValues)
                        ResultBins[aKP, anALT, aLat, aMLT, "Maximum"] = np.nanmax(AllBinValues)
                        
                        # calculate distribution
                        if Data.DistributionNumOfSlots > 0:
                            histo_values, histo_ranges = np.histogram(AllBinValues, Data.DistributionNumOfSlots, (0, 0.0000001))
                            for i in range(0, Data.DistributionNumOfSlots):
                                ResultBins[aKP, anALT, aLat, aMLT, "Distribution"][i] = histo_values[i]
        
    if TypeOfCalculation == "JH":
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Joule Heating", "W/m3")
    if TypeOfCalculation == "JHminusWindHeat" :
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Joule Heating minus Wind Heating", "W/m3")
    elif TypeOfCalculation == "PedCond":
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Pedersen Conductivity", "S/m")
    elif TypeOfCalculation == "HallCond":
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Hall Conductivity", "S/m")    
    elif TypeOfCalculation=="EEX_si":
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Electric Field East", "V/m")
    elif TypeOfCalculation=="EEY_si":
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Electric Field North", "V/m")
    elif TypeOfCalculation=="EEX":
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Electric Field East", "V/cm")
    elif TypeOfCalculation=="EEY":
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Electric Field North", "V/cm")    
    elif TypeOfCalculation=="ConvHeat":
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Convection heating", "W/m^3")
    elif TypeOfCalculation=="WindHeat":
        Data.WriteResultsToCDF(ResultBins, ResultFilename, "Wind heating", "W/m^3")
    
    # delete temporary files, which contain all values for each bin
    if DeleteTmpFiles:
        try:
            shutil.rmtree( TmpFilesPath )
        except:
            pass
    
    # 
    finishSecs = time.time()
    print( "FINISH",  datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), " (", finishSecs-startSecs, "sec )")


    
    

    
                  
                  
    

def PROC_StatsCalculator(ProcessNum, CDF_filename, TypeOfCalculation, TmpFilesPath,    _MLT_min, _MLT_max, _MLT_duration_of_a_bin, _LAT_min, _LAT_max, _LAT_degrees_of_a_bin, _ALT_min, _ALT_max, _ALT_distance_of_a_bin, _num_of_KP_bins, _DistributionNumOfSlots, LatStep_for_WeightedAverage):
    """
    Reads a NetCDF file and saves all the values of the variable in files.
    The variable is chosen by the <TypeOfCalculation> argument.
    The process saves several files in its own folder with name: TmpFilesPath+"proc"+<ProcessNum>+"/"
    The folder contains one binary file for each bin. The file contains all values of the variable which fall in the bin
    Args:
        ProcessNum: the unique index number of this process
        CDF_filename: the source file this process is going to read.
        TypeOfCalculation (string): the variable which will be used for the calculations. Possible values:  
            "JH" for Joule Heating (Ohmic)  
            "JHminusWindHeat" for Joule Heating minus Wind heating  
            "PedCond" for Pedersen Conductivity  
            "HallCond" for Pedersen Conductivity  
            "EEX_si" for Electric Field East in V/cm  
            "EEY_si" for Electric Field North in V/cm  
            "EEX_si" for Electric Field East in V/m  
            "EEY_si" for Electric Field North in V/m  
            "ConvHeat" for Convection heating  
            "WindHeat" for Wind heating  
        TmpFilesPath: the path where ths process is going to save its temporary files
    """
    
    if DEBUG_ENABLED: debug_file = open( "debug"+str(ProcessNum)+".txt", "w" )
    if DEBUG_ENABLED: debug_file.write( "START\n" )
    
    # set again the data parameters, because the process has a different scope
    Data.setDataParams(_MLT_min, _MLT_max, _MLT_duration_of_a_bin, _LAT_min, _LAT_max, _LAT_degrees_of_a_bin, _ALT_min, _ALT_max, _ALT_distance_of_a_bin, _num_of_KP_bins, TypeOfCalculation, _DistributionNumOfSlots)
    
    print( "Process", ProcessNum, "reading",  CDF_filename)    

    # check if the data of this process have already been calculated
    procfolder = TmpFilesPath+"proc"+ f"{ProcessNum:03}" +"/"
    if os.path.isdir(procfolder):
        print( "Data for file", ProcessNum, "already calculated.", "Process", ProcessNum, "finished." )
        return # <<<<
    else:
        if os.path.isdir(TmpFilesPath)==False: os.mkdir( TmpFilesPath )
        os.mkdir( procfolder )    
        
    # open netCDF file 
    ######## while( os.path.exists("ReadingFile.flag") ): # wait until no other process is reading from disk/NFS
    ########    time.sleep(random.randint(8,20))
    #Path("ReadingFile.flag").touch() # raise a flag that this process is now reading a file, so that other processes wait
    try:
        CDFroot = Dataset( CDF_filename, 'r' )
    except:
        print ( " !!!!!!!! WRONG FORMAT:", CDF_filename )
        #os.remove("ReadingFile.flag") # lower the reading-file flag
        return
        
    # read the data from the netCDF file
    #TIMEs  = CDFroot.variables['time'][:] 
    if "JH" in TypeOfCalculation:        Ohmics = CDFroot.variables['Ohmic'][:, :, :, :]  # m/s
    if "PedCond" in TypeOfCalculation:   PEDs   = CDFroot.variables['SIGMA_PED'][:, :, :, :]
    if "HallCond" in TypeOfCalculation:  HALs   = CDFroot.variables['SIGMA_HAL'][:, :, :, :]
    if "EEX_si" in TypeOfCalculation:    EEXs   = CDFroot.variables['EEX_si'][:, :, :, :]
    if "EEY_si" in TypeOfCalculation:    EEYs   = CDFroot.variables['EEY_si'][:, :, :, :]
    if TypeOfCalculation == "EEX":       EEXs   = CDFroot.variables['EEX'][:, :, :, :]
    if TypeOfCalculation == "EEY":       EEYs   = CDFroot.variables['EEY'][:, :, :, :]
    if "ConvHeat" in TypeOfCalculation:  ConvH  = CDFroot.variables['Convection_heating'][:, :, :, :]
    if "WindHeat" in TypeOfCalculation:  WindH  = CDFroot.variables['Wind_heating'][:, :, :, :]
    if "JHminusWindHeat" in TypeOfCalculation:  WindH  = CDFroot.variables['Wind_heating'][:, :, :, :]        
        
    if "JHnoWindsEISCAT" in TypeOfCalculation: 
        UI = CDFroot.variables['UI_ExB'][:, :, :, :]
        VI = CDFroot.variables['VI_ExB'][:, :, :, :]
        WI = CDFroot.variables['WI_ExB'][:, :, :, :]
        TIMEs = CDFroot.variables['time'][:] 
        PEDs  = CDFroot.variables['SIGMA_PED'][:, :, :, :]
        LONs  = CDFroot.variables['lon'][:] 
        ZGs   = CDFroot.variables['ZG'][:, :, :, :] / 100000 # Geometric height stored in cm, converted to km
    #
    LATs   = CDFroot.variables['lat'][:] 
    #MLATs   = CDFroot.variables['mlat_qdf'][:, :, :, :] 
    MLTs    = CDFroot.variables['mlt_qdf'][:, :, :, :]         
    ALTs    = CDFroot.variables['ZGMID'][:, :, :, :] / 100000 # Geometric height stored in cm, converted to km
    KPs     = CDFroot.variables['Kp'][:]
    
    #try:
    #    os.remove("ReadingFile.flag") # lower the reading-file flag
    #except:
    #    pass
    
    hits = 0   # num of instances that fit in any of the defined bins

    ResultBins = Data.init_ResultDataStructure().copy()
    num_of_unbinned_items = 0
    step = 1
    for idx_time in range(0, len(ALTs), step):
        # $$$$$$$$ for each moment in time put the values in their bins and calculate the mean of each bin. 
        SingleMomentBins = Data.init_ResultDataStructure().copy()
        for idx_lev in range(0, len(ALTs[0]), step):
            for idx_lat in range(0, len(ALTs[0,0]), step):
                for idx_lon in range(0, len(ALTs[0,0,0]), step):
                    
                    curr_alt_km = ALTs[idx_time, idx_lev, idx_lat, idx_lon] 
                    
                    # ignore values for out-of-range positions 
                    if curr_alt_km<Data.ALT_min or curr_alt_km>Data.ALT_max:
                        continue
                        
                    curr_kp     = KPs[idx_time]
                    curr_mlt    = MLTs[idx_time, idx_lev, idx_lat, idx_lon]
                    curr_lat    = LATs[idx_lat]
                    
                    kp_to_fall,alt_to_fall,lat_to_fall,mlt_to_fall = Data.LocatePositionInBins(curr_kp,curr_alt_km,curr_lat,curr_mlt)
                    
                    if kp_to_fall is None or alt_to_fall is None or lat_to_fall is None or mlt_to_fall is None:
                        num_of_unbinned_items += 1
                        break # no other longitude can have a hit either
                    else:
                        if TypeOfCalculation=="JHminusWindHeat" or TypeOfCalculation=="JHminusWindHeatEISCAT":
                            aValue = Ohmics[idx_time, idx_lev, idx_lat, idx_lon] - WindH[idx_time, idx_lev, idx_lat, idx_lon]
                            if aValue > 100: continue # ignore faulty large values
                        elif TypeOfCalculation=="JH":
                            aValue = Ohmics[idx_time, idx_lev, idx_lat, idx_lon]
                            if aValue > 100: continue # ignore faulty large values
                        elif "PedCond" in TypeOfCalculation:
                            aValue = PEDs[idx_time, idx_lev, idx_lat, idx_lon]
                        elif "HallCond" in TypeOfCalculation:
                            aValue = HALs[idx_time, idx_lev, idx_lat, idx_lon]
                        elif "EEX_si" in TypeOfCalculation:
                            aValue = EEXs[idx_time, idx_lev, idx_lat, idx_lon]
                        elif "EEY_si" in TypeOfCalculation:
                            aValue = EEYs[idx_time, idx_lev, idx_lat, idx_lon]
                        elif "EEX" in TypeOfCalculation:
                            aValue = EEXs[idx_time, idx_lev, idx_lat, idx_lon]
                        elif "EEY" in TypeOfCalculation:
                            aValue = EEYs[idx_time, idx_lev, idx_lat, idx_lon]    
                        elif "ConvHeat" in TypeOfCalculation:
                            aValue = ConvH[idx_time, idx_lev, idx_lat, idx_lon]
                            if aValue > 100: continue # ignore faulty large values
                        elif "WindHeat" in TypeOfCalculation:
                            aValue = WindH[idx_time, idx_lev, idx_lat, idx_lon]
                        elif TypeOfCalculation=="JHnoWindsEISCAT": 
                            I = list()
                            B = list()
                            time_p = datetime.datetime(2015, 3, 15, 0, 0, 0) + datetime.timedelta(minutes=TIMEs[idx_time])
                            lat_p = LATs[idx_lat]
                            lon_p = LONs[idx_lon]
                            alt_p = ZGs[idx_time, idx_lev, idx_lat, idx_lon]
                            pt = pyglow.Point(time_p, lat_p, lon_p, alt_p) # pyglow igrf
                            pt.run_igrf()
                            B.append( pt.Bx )  # Be, Tesla  (si)
                            B.append( pt.By )  # Bn, Tesla  (si)
                            B.append( pt.Bz )  # Bu, Tesla  (si)
                            I.append( UI[idx_time,idx_lev,idx_lat,idx_lon] )
                            I.append( VI[idx_time,idx_lev,idx_lat,idx_lon] )
                            I.append( WI[idx_time,idx_lev,idx_lat,idx_lon] )
                            E = -1 * np.cross(I, B)
                            aValue = PEDs[idx_time,idx_lev,idx_lat,idx_lon] * np.dot(E, E)
                        else:
                            print("ERROR: UNRECOGNISED TypeOfCalculation '" + TypeOfCalculation + "'")
                            CDFroot.close()
                            return
                        
                        # bin this value
                        SingleMomentBins[ kp_to_fall, alt_to_fall, lat_to_fall, mlt_to_fall, "Vals" ].append( aValue )
                        
                        # if weights are enabled then store the value's weight as well
                        if LatStep_for_WeightedAverage >= 0:
                            weight = 1
                            if LatStep_for_WeightedAverage == 0:
                                if curr_lat == 68.75:
                                    weight = 0.0410
                                elif curr_lat == 71.25:
                                    weight = 0.381
                                elif curr_lat == 73.75:
                                    weight = 0.328
                                elif curr_lat == 76.25:
                                    weight = 0.249
                            else:
                                BinSurfaceArea = CalcSurfaceAreaBetweenLatitudes(lat_to_fall, lat_to_fall+Data.LAT_degrees_of_a_bin)
                                for i in range(math.floor(lat_to_fall), math.ceil(lat_to_fall+Data.LAT_degrees_of_a_bin)):
                                    if curr_lat>i and curr_lat<i+LatStep_for_WeightedAverage:
                                        RingArea = CalcSurfaceAreaBetweenLatitudes(i, i+LatStep_for_WeightedAverage )
                                        break
                                weight = RingArea / BinSurfaceArea 
                            #### warn
                            if DEBUG_ENABLED and weight==1: debug_file.write("Lat " + str(curr_lat) + " could not be assigned a weight\n")
                            #### bin the weight    
                            SingleMomentBins[ kp_to_fall, alt_to_fall, lat_to_fall, mlt_to_fall, "Weights" ].append( weight )
                            
                            if DEBUG_ENABLED: debug_file.write( str(weight) + " " +  str(aValue) + "\n" )
                        else:
                            SingleMomentBins[ kp_to_fall, alt_to_fall, lat_to_fall, mlt_to_fall, "Weights" ].append( 1 )
                        
                        # keep tracks of the number of the total binned values 
                        hits +=1
                        
        # $$$$$$$$ the averages of each time moment are stored in their bin. The percentiles will be calculated on them at the end 
        if LatStep_for_WeightedAverage >= 0: # weighted average
            for aKP in Data.KPsequence:
                for anALT in Data.ALTsequence:
                    for aLat in Data.LATsequence:
                        for aMLT in Data.MLTsequence: 
                            L = len(SingleMomentBins[aKP,anALT,aLat,aMLT,"Vals"])
                            if L > 0:
                                S = 0
                                sum_of_weights = 0
                                BinVals    = SingleMomentBins[aKP,anALT,aLat,aMLT,"Vals"]
                                BinWeights = SingleMomentBins[aKP,anALT,aLat,aMLT,"Weights"]
                                for i in range(0, len(SingleMomentBins[aKP,anALT,aLat,aMLT,"Vals"])):
                                    S +=  BinWeights[i] * BinVals[i]
                                    sum_of_weights += BinWeights[i]
                                ResultBins[aKP,anALT,aLat,aMLT,"Vals"].append( S / sum_of_weights )
                                
        else: # normal average
            for aKP in Data.KPsequence:
                for anALT in Data.ALTsequence:
                    for aLat in Data.LATsequence:
                        for aMLT in Data.MLTsequence: 
                            L = len(SingleMomentBins[aKP,anALT,aLat,aMLT,"Vals"])
                            if L > 0:
                                S = sum(SingleMomentBins[aKP,anALT,aLat,aMLT,"Vals"])
                                ResultBins[aKP,anALT,aLat,aMLT,"Vals"].append( S / L )

    # close cdf
    CDFroot.close()
    
    # ---- save values of each bin in a binary file
    for aKP in Data.KPsequence:
        for anALT in Data.ALTsequence:
            for aLat in Data.LATsequence:
                for aMLT in Data.MLTsequence:    
                    if len( ResultBins[ aKP, anALT, aLat, aMLT, "Vals" ] ) > 0:
                        fname = str(aKP) + "_" + str(anALT) + "_" + str(aLat) + "_" + str(aMLT) + ".txt"
                        f = open( procfolder + fname, "wb" )
                        float_array = array('d', ResultBins[aKP, anALT, aLat, aMLT, "Vals"])
                        float_array.tofile(f)
                        f.close()

    # -------- print result
    '''
    msg = "Process " + str(ProcessNum) + " " + CDF_filename +  " Hits=" + str(hits)
    for aKP in Data.KPsequence:
        msg += "\n"
        for aMLT in Data.MLTsequence: 
            n = 0
            for aLat in Data.LATsequence:
                for anALT in Data.ALTsequence:
                    n += len(ResultBins[aKP,anALT,aLat,aMLT,"Vals"])
            msg += "  " + str(n)
    '''
    if DEBUG_ENABLED: debug_file.write( "FINISH\n" )
    if DEBUG_ENABLED: debug_file.close() 
    
    
    
    
    
