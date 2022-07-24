"""
This module contains all data structures, tools for saving and loading data from NetCDF files amd function which calculate statistics.
The main data container is called Bin. A Bin is defined by ranges of Magnetic Latitude, Magnetic Local Time, Altitude and Kp-index.
There are several predefined Bins, but they can be deleted and new ones added. 
The first letters of the Bin's ID is consiered the region name, which is a central notion for grouping the data and ploting them.
During calculations values of many variables are read from the TIEGCM or/and ORBIT NeyCDF files and are stored into the corresponding Bins along with their positions. These data can then be stored to a NetCDF result-file and are used to produce various plots. 
The variables which are expected to be at the source and are stored to the result files are:
    Variable description            Unit             Name in NetCDF files           Comment
    ------------------------------------------------------------------------------------------------------------
    UTC timestamp                   seconds          time
    Altitude                        cm               ZGMID
    Latitude                        degrees          lat
    Magnetic Latitude               degrees          mlat_qdf
    Magnetic Local Time             hours            mlt_qdf
    Kp index                        0-9              Kp
    midpoint levels                 -                lev          
    Ohmic (Joule) Heating           W/m3             Ohmic                          can be plotted 
    Convection Heating              W/m3             Convection_heating             can be plotted
    Wind Heating                    W/m3             Wind_heating                   can be plotted
    Electric field strength East    V/m              EEX                            can be plotted
    Electric field strength North   V/m              EEY                            can be plotted
    Total Density                   g/cm3            DEN                            can be plotted
    Pedersen Conductivity           S/m              SIGMA_PED                      can be plotted 
    Hall Conductivity               S/m              SIGMA_HAL                      can be plotted
Because many large files may contain the source data, folders are used to keep each file category:
    ORBITdata: all netcdf files containing the data along the orbit of a satellite
    RESULTS: netcdf files which this software creates as results and can be loaded in order to produce plots
    TIEGCMdata/*/: all netcdf files containing the data from the TIEGCM model. There must be one subfolder for each year.
"""

from datetime import datetime
import netCDF4
from netCDF4 import Dataset 
from os import path
import numpy as np 

import time
import numpy as np 
import threading
import glob
import copy
import calendar

from utils import *

# Properties of the current calculation
CALCULATIONS_Title = ""
CALCULATIONS_Description =""
CALCULATIONS_RegionName = ""
CALCULATIONS_OrbitFilesPath = ""
CALCULATIONS_ResultsFilename = ""
CALCULATIONS_TIEGCMfolder = ""
CALCULATIONS_ExecutionDuration = 0

# The following lists store data about each hit
all_JH_values       = list()
all_MagLat_values   = list()
all_MLT_values      = list()
all_Altitude_values = list()
all_Lat_values      = list()
all_Kp_values       = list() 
all_Time_values     = list()
all_HittedBin_IDs   = list()
all_EEX_values      = list()
all_EEY_values      = list()
all_Pedersen_values = list()
all_Density_values  = list()
all_Lev_values      = list()
all_Hall_values     = list()
all_ConvectionHeating_values = list()
all_WindHeating_values = list()


def doit():
    global all_JH_values
    all_JH_values.append(4.44);
    all_JH_values.clear()
    all_JH_values.append(4.44);

# Define a class which can describe a bin
class Bin:
    ID             = ""
    Description    = ""
    MLT_min        = 0 # Magnetic Local Time (hour & min of the 24-hour day) (string)
    MLT_max        = 0 # Magnetic Local Time (hour & min of the 24-hour day) (string)
    MagLat_min     = 0 # Magnetic Latitude (degrees)
    MagLat_max     = 0 # Magnetic Latitude (degrees)
    Altitude_min   = 0 # Satellite's Altitude measured from Earth's surface (km)
    Altitude_max   = 0 # Satellite's Altitude measured from Earth's surface (km)
    Kp_min         = 0 #
    Kp_max         = 0 #
    Lat_min        = 0
    Lat_max        = 0
    NumOfBins      = 0 # How many parts will the Altitude range be splitted in
    CumulativeTime = 0 # (sec)
    DesirableCumulativeTime = 0 # (sec)
    JH_min      = 99999 # the minimum JH value inside the bin
    JH_max      = 0     # the maximum JH value inside the bin
    JH_mean     = 0     # the mean JH value inside the bin
    JH_median   = 0     # the median JH value inside the bin (=50th percentile)
    JH_variance = 0     # the variance of JH value inside the bin (variance = (1/(N-1)) * Sum{1->N}(X-MeanVariance)^2  )
    JH_medianVariance = 0
    JH_medianAbsDev = 0
    # Data:
    JH_values         = list() # here will be stored all Joule Heating values in order to calculate the variance at the end
    JH_distribution   = list() # the item 0 holds the number of points which have 0<JH<JH_max/100 etc
    MagLat_values     = list() #  these values correspond to the JH_values
    MLT_values        = list() #  these values correspond to the JH_values
    Altitude_values   = list() #  these values correspond to the JH_values
    Kp_values         = list() #  these values correspond to the JH_values
    Time_values       = list() #  these values correspond to the JH_values
    EEX_values        = list()
    EEY_values        = list()
    Pedersen_values   = list()
    Density_values    = list()
    Lev_values        = list()
    Hall_values       = list()
    ConvectionHeating_values = list()
    WindHeating_values = list()
    
    def __init__(self, ID, Description, MLT_min, MLT_max, MagLat_min, MagLat_max, Altitude_min, Altitude_max, Lat_min, Lat_max, Kp_min, Kp_max, DesirableCumulativeTime):
        self.ID             = ID
        self.Description    = Description
        self.MLT_min        = MLT_min 
        self.MLT_max        = MLT_max
        self.MagLat_min     = MagLat_min
        self.MagLat_max     = MagLat_max
        self.Altitude_min   = Altitude_min
        self.Altitude_max   = Altitude_max
        self.Lat_min        = Lat_min
        self.Lat_max        = Lat_max                
        self.Kp_min         = Kp_min
        self.Kp_max         = Kp_max
        self.DesirableCumulativeTime = DesirableCumulativeTime
        self.JH_values       = list()
        self.JH_distribution = [0] * 100
        self.MagLat_values   = list()
        self.MLT_values      = list()
        self.Altitude_values = list()
        self.Lat_values       = list()
        self.Kp_values       = list()
        self.Time_values     = list()
        self.EEX_values        = list()
        self.EEY_values        = list()
        self.Pedersen_values   = list()
        self.Density_values    = list()
        self.Lev_values        = list()
        self.Hall_values       = list()
        self.ConvectionHeating_values = list()
        self.WindHeating_values = list()

    def reset(self):
        self.JH_min      = 99999
        self.JH_mean     = 0
        self.JH_median   = 0
        self.JH_variance = 0
        self.JH_medianVariance = 0
        self.JH_medianAbsDev = 0
        self.JH_values.clear()
        self.MagLat_values.clear()
        self.MLT_values.clear()
        self.Altitude_values.clear()
        self.Lat_values.clear()
        self.Kp_values.clear()
        self.Time_values.clear()
        self.EEX_values.clear()
        self.EEY_values.clear()
        self.Pedersen_values.clear()
        self.Density_values.clear()
        self.Lev_values.clear()
        self.Hall_values.clear()        
        self.ConvectionHeating_values.clear()
        self.WindHeating_values.clear()
        
    def getInfo(self):
        s  = self.ID.ljust(8, ' ') + ": "
        s += "{:02.0f}".format(self.MLT_min)      + "<MLT<="    + "{:02.0f}".format(self.MLT_max)      + " "
        s += "{:03.0f}".format(self.MagLat_min)   + "<MagLat<=" + "{:03.0f}".format(self.MagLat_max)   + " "
        s += "{:03.0f}".format(self.Altitude_min) + "<Alt<="    + "{:03.0f}".format(self.Altitude_max) + " "
        s += str(self.Kp_min)             + "<Kp<="     + str(self.Kp_max)       + " "
        if self.JH_min == 99999:
            s += " JHmin=" + "         "
        else:
            s += " JHmin=" + "{:.3e}".format(self.JH_min) #ConvertLeadingZerosToSpaces( "{:09.3f}".format(self.JH_min) )
        s += " JHmean=" + "{:.3e}".format(self.JH_mean) #ConvertLeadingZerosToSpaces( "{:09.3f}".format(self.JH_mean) )
        s += " JHvariance=" + "{:.3e}".format(self.JH_variance) #ConvertLeadingZerosToSpaces( "{:09.3f}".format(self.JH_variance) )
        ##
        str_JH = ""
        for i in range(0, len(self.JH_values) ):            
            str_JH += str( self.JH_values[i] )
            if i < len(self.JH_values)-1: str_JH += ','
        s += " JH_values=" + str_JH # ''.join(str(e) for e in self.JH_values)
        ##
        return s
    
    def printMe(self):
        print( self.getInfo()[:220] )


Bins = list() # this list holds the definitions of all bins
#                ID        Description                          MLT      MagLat    Altitude                Lat      Kp       DesiredTime(sec)
Bins.append( Bin("AEM_00", "Auroral E region, midnight sector", 21, 3,   60, 75,   100, 105,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_01", "Auroral E region, midnight sector", 21, 3,   60, 75,   105, 110,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_02", "Auroral E region, midnight sector", 21, 3,   60, 75,   110, 115,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_03", "Auroral E region, midnight sector", 21, 3,   60, 75,   115, 120,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_04", "Auroral E region, midnight sector", 21, 3,   60, 75,   120, 125,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_05", "Auroral E region, midnight sector", 21, 3,   60, 75,   125, 130,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_06", "Auroral E region, midnight sector", 21, 3,   60, 75,   130, 135,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_07", "Auroral E region, midnight sector", 21, 3,   60, 75,   135, 140,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_08", "Auroral E region, midnight sector", 21, 3,   60, 75,   140, 145,               -90,90,  0, 3,   50*60 ) )    
Bins.append( Bin("AEM_09", "Auroral E region, midnight sector", 21, 3,   60, 75,   145, 150,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_10", "Auroral E region, midnight sector", 21, 3,   60, 75,   150, 155,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_11", "Auroral E region, midnight sector", 21, 3,   60, 75,   155, 160,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEM_20", "Auroral E region, midnight sector", 21, 3,   60, 75,   100, 105,               -90,90,  3, 9,   30*60 ) )
Bins.append( Bin("AEM_21", "Auroral E region, midnight sector", 21, 3,   60, 75,   105, 110,               -90,90,  3, 9,   30*60 ) )
Bins.append( Bin("AEM_22", "Auroral E region, midnight sector", 21, 3,   60, 75,   110, 115,               -90,90,  3, 9,   30*60 ) )
Bins.append( Bin("AEM_23", "Auroral E region, midnight sector", 21, 3,   60, 75,   115, 120,               -90,90,  3, 9,   30*60 ) )
Bins.append( Bin("AEM_24", "Auroral E region, midnight sector", 21, 3,   60, 75,   120, 125,               -90,90,  3, 9,   30*60 ) )
Bins.append( Bin("AEM_25", "Auroral E region, midnight sector", 21, 3,   60, 75,   125, 130,               -90,90,  3, 9,   30*60 ) )    
Bins.append( Bin("AEM_26", "Auroral E region, midnight sector", 21, 3,   60, 75,   130, 135,               -90,90,  3, 9,   30*60 ) )    
Bins.append( Bin("AEM_27", "Auroral E region, midnight sector", 21, 3,   60, 75,   135, 140,               -90,90,  3, 9,   20*60 ) )
Bins.append( Bin("AEM_28", "Auroral E region, midnight sector", 21, 3,   60, 75,   140, 145,               -90,90,  3, 9,   20*60 ) )
Bins.append( Bin("AEM_29", "Auroral E region, midnight sector", 21, 3,   60, 75,   145, 150,               -90,90,  3, 9,   20*60 ) )
Bins.append( Bin("AEM_30", "Auroral E region, midnight sector", 21, 3,   60, 75,   150, 155,               -90,90,  3, 9,   20*60 ) )
Bins.append( Bin("AEM_31", "Auroral E region, midnight sector", 21, 3,   60, 75,   155, 160,               -90,90,  3, 9,   20*60 ) )

Bins.append( Bin("AAA_L1", "Auroral E region, midnight sector", 12, 12,   50, 90,   100, 105,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_L2", "Auroral E region, midnight sector", 12, 12,   50, 90,   105, 110,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_L3", "Auroral E region, midnight sector", 12, 12,   50, 90,   110, 115,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_L4", "Auroral E region, midnight sector", 12, 12,   50, 90,   115, 120,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_L5", "Auroral E region, midnight sector", 12, 12,   50, 90,   120, 125,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_L6", "Auroral E region, midnight sector", 12, 12,   50, 90,   125, 130,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_L7", "Auroral E region, midnight sector", 12, 12,   50, 90,   130, 135,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_L8", "Auroral E region, midnight sector", 12, 12,   50, 90,   135, 140,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_L9", "Auroral E region, midnight sector", 12, 12,   50, 90,   140, 145,               -90,90,  0, 3,   50*60 ) )    

Bins.append( Bin("AAA_La", "Auroral E region, midnight sector", 12, 12,   50, 90,   145, 150,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_Lb", "Auroral E region, midnight sector", 12, 12,   50, 90,   150, 155,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_Lc", "Auroral E region, midnight sector", 12, 12,   50, 90,   155, 160,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AAA_M1", "Auroral E region, midnight sector", 12, 12,   50, 90,   100, 105,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_M2", "Auroral E region, midnight sector", 12, 12,   50, 90,   105, 110,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_M3", "Auroral E region, midnight sector", 12, 12,   50, 90,   110, 115,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_M4", "Auroral E region, midnight sector", 12, 12,   50, 90,   115, 120,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_M5", "Auroral E region, midnight sector", 12, 12,   50, 90,   120, 125,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_M6", "Auroral E region, midnight sector", 12, 12,   50, 90,   125, 130,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_M7", "Auroral E region, midnight sector", 12, 12,   50, 90,   130, 135,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_M8", "Auroral E region, midnight sector", 12, 12,   50, 90,   135, 140,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_M9", "Auroral E region, midnight sector", 12, 12,   50, 90,   140, 145,               -90,90,  3, 9,   50*60 ) )    
Bins.append( Bin("AAA_Ma", "Auroral E region, midnight sector", 12, 12,   50, 90,   145, 150,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_Mb", "Auroral E region, midnight sector", 12, 12,   50, 90,   150, 155,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AAA_Mc", "Auroral E region, midnight sector", 12, 12,   50, 90,   155, 160,               -90,90,  3, 9,   50*60 ) )    
    
Bins.append( Bin("AFM_L1", "Auroral F region, midnight sector", 21, 3,   60, 75,   150, 185,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_L2", "Auroral F region, midnight sector", 21, 3,   60, 75,   185, 220,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_L3", "Auroral F region, midnight sector", 21, 3,   60, 75,   220, 255,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_L4", "Auroral F region, midnight sector", 21, 3,   60, 75,   255, 290,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_L5", "Auroral F region, midnight sector", 21, 3,   60, 75,   290, 325,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_L6", "Auroral F region, midnight sector", 21, 3,   60, 75,   325, 360,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_L7", "Auroral F region, midnight sector", 21, 3,   60, 75,   360, 395,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_L8", "Auroral F region, midnight sector", 21, 3,   60, 75,   395, 430,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_L9", "Auroral F region, midnight sector", 21, 3,   60, 75,   430, 465,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_L10","Auroral F region, midnight sector", 21, 3,   60, 75,   465, 500,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("AFM_M1", "Auroral F region, midnight sector", 21, 3,   60, 75,   150.0, 237.5,           -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("AFM_M2", "Auroral F region, midnight sector", 21, 3,   60, 75,   237.5, 325.0,           -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("AFM_M3", "Auroral F region, midnight sector", 21, 3,   60, 75,   325.0, 412.5,           -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("AFM_M4", "Auroral F region, midnight sector", 21, 3,   60, 75,   412.5, 500.0,           -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("AFM_H1", "Auroral F region, midnight sector", 21, 3,   60, 75,   150, 265,               -90,90,  4, 9,   20*60 ) )
Bins.append( Bin("AFM_H2", "Auroral F region, midnight sector", 21, 3,   60, 75,   265, 380,               -90,90,  4, 9,   20*60 ) )
Bins.append( Bin("AFM_H3", "Auroral F region, midnight sector", 21, 3,   60, 75,   380, 500,               -90,90,  4, 9,   20*60 ) )
    
Bins.append( Bin("AEE_00", "Auroral E region, evening sector",  15, 21,  60, 75,   100, 105,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_01", "Auroral E region, evening sector",  15, 21,  60, 75,   105, 110,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_02", "Auroral E region, evening sector",  15, 21,  60, 75,   110, 115,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_03", "Auroral E region, evening sector",  15, 21,  60, 75,   115, 120,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_04", "Auroral E region, evening sector",  15, 21,  60, 75,   120, 125,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_05", "Auroral E region, evening sector",  15, 21,  60, 75,   125, 130,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_06", "Auroral E region, evening sector",  15, 21,  60, 75,   130, 135,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_07", "Auroral E region, evening sector",  15, 21,  60, 75,   135, 140,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_08", "Auroral E region, evening sector",  15, 21,  60, 75,   140, 145,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_09", "Auroral E region, evening sector",  15, 21,  60, 75,   145, 150,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_10", "Auroral E region, evening sector",  15, 21,  60, 75,   150, 155,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_11", "Auroral E region, evening sector",  15, 21,  60, 75,   155, 160,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AEE_20", "Auroral E region, evening sector",  15, 21,  60, 75,   100, 105,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_21", "Auroral E region, evening sector",  15, 21,  60, 75,   105, 110,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_22", "Auroral E region, evening sector",  15, 21,  60, 75,   110, 115,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_23", "Auroral E region, evening sector",  15, 21,  60, 75,   115, 120,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_24", "Auroral E region, evening sector",  15, 21,  60, 75,   120, 125,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_25", "Auroral E region, evening sector",  15, 21,  60, 75,   125, 130,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_26", "Auroral E region, evening sector",  15, 21,  60, 75,   130, 135,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_27", "Auroral E region, evening sector",  15, 21,  60, 75,   135, 140,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_28", "Auroral E region, evening sector",  15, 21,  60, 75,   140, 145,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_29", "Auroral E region, evening sector",  15, 21,  60, 75,   145, 150,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_30", "Auroral E region, evening sector",  15, 21,  60, 75,   150, 155,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AEE_31", "Auroral E region, evening sector",  15, 21,  60, 75,   155, 160,               -90,90,  3, 9,   50*60 ) )

Bins.append( Bin("AED_00", "Auroral E region, dawn sector",   3,  9,  60, 75,   100, 105,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_01", "Auroral E region, dawn sector",   3,  9,  60, 75,   105, 110,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_02", "Auroral E region, dawn sector",   3,  9,  60, 75,   110, 115,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_03", "Auroral E region, dawn sector",   3,  9,  60, 75,   115, 120,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_04", "Auroral E region, dawn sector",   3,  9,  60, 75,   120, 125,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_05", "Auroral E region, dawn sector",   3,  9,  60, 75,   125, 130,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_06", "Auroral E region, dawn sector",   3,  9,  60, 75,   130, 135,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_07", "Auroral E region, dawn sector",   3,  9,  60, 75,   135, 140,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_08", "Auroral E region, dawn sector",   3,  9,  60, 75,   140, 145,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_09", "Auroral E region, dawn sector",   3,  9,  60, 75,   145, 150,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_10", "Auroral E region, dawn sector",   3,  9,  60, 75,   150, 155,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_11", "Auroral E region, dawn sector",   3,  9,  60, 75,   155, 160,               -90,90,  0, 3,   50*60 ) )
Bins.append( Bin("AED_20", "Auroral E region, dawn sector",   3,  9,  60, 75,   100, 105,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_21", "Auroral E region, dawn sector",   3,  9,  60, 75,   105, 110,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_22", "Auroral E region, dawn sector",   3,  9,  60, 75,   110, 115,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_23", "Auroral E region, dawn sector",   3,  9,  60, 75,   115, 120,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_24", "Auroral E region, dawn sector",   3,  9,  60, 75,   120, 125,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_25", "Auroral E region, dawn sector",   3,  9,  60, 75,   125, 130,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_26", "Auroral E region, dawn sector",   3,  9,  60, 75,   130, 135,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_27", "Auroral E region, dawn sector",   3,  9,  60, 75,   135, 140,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_28", "Auroral E region, dawn sector",   3,  9,  60, 75,   140, 145,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_29", "Auroral E region, dawn sector",   3,  9,  60, 75,   145, 150,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_30", "Auroral E region, dawn sector",   3,  9,  60, 75,   150, 155,               -90,90,  3, 9,   50*60 ) )
Bins.append( Bin("AED_31", "Auroral E region, dawn sector",   3,  9,  60, 75,   155, 160,               -90,90,  3, 9,   50*60 ) )
    
Bins.append( Bin("EEJ_A1", "Equatorial E-region",             10, 13,  -7,  7,   115,   127,                -90,90,  0, 9,   10*60 ) )
Bins.append( Bin("EEJ_A2", "Equatorial E-region",             10, 13,  -7,  7,   127,   139,                -90,90,  0, 9,   10*60 ) )
Bins.append( Bin("EEJ_A3", "Equatorial E-region",             10, 13,  -7,  7,   139,   150,                -90,90,  0, 9,   10*60 ) )

Bins.append( Bin("EPB_A1", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   150, 185,                  -90,90,  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A2", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   185, 220,                  -90,90,  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A3", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   220, 255,                  -90,90,  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A4", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   255, 290,                  -90,90,  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A5", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   290, 325,                  -90,90,  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A6", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   325, 360,                  -90,90,  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A7", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   360, 395,                  -90,90,  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A8", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   395, 430,                  -90,90,  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A9", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   430, 465,                  -90,90,  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A10","Equatorial Plasma Bubbles",       18,  4, -30, 30,   465, 500,                  -90,90,  0, 9,   150*60 ) )

Bins.append( Bin("SQ_A1",  "Sq & midlat F region currents",    6, 19, -60, 60,   150, 185,                  -90,90,  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A2",  "Sq & midlat F region currents",    6, 19, -60, 60,   185, 220,                  -90,90,  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A3",  "Sq & midlat F region currents",    6, 19, -60, 60,   220, 255,                  -90,90,  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A4",  "Sq & midlat F region currents",    6, 19, -60, 60,   255, 290,                  -90,90,  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A5",  "Sq & midlat F region currents",    6, 19, -60, 60,   290, 325,                  -90,90,  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A6",  "Sq & midlat F region currents",    6, 19, -60, 60,   325, 360,                  -90,90,  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A7",  "Sq & midlat F region currents",    6, 19, -60, 60,   360, 395,                  -90,90,  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A8",  "Sq & midlat F region currents",    6, 19, -60, 60,   395, 430,                  -90,90,  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A9",  "Sq & midlat F region currents",    6, 19, -60, 60,   430, 465,                  -90,90,  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A10", "Sq & midlat F region currents",    6, 19, -60, 60,   465, 500,                  -90,90,  0, 3,   150*60 ) )
    
Bins.append( Bin("CF_L1", "Dayside Cusp F-region",            10, 14,   70,  80,   140, 185,                -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("CF_L2", "Dayside Cusp F-region",            10, 14,   70,  80,   185, 230,                -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("CF_L3", "Dayside Cusp F-region",            10, 14,   70,  80,   230, 275,                -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("CF_L4", "Dayside Cusp F-region",            10, 14,   70,  80,   275, 320,                -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("CF_L5", "Dayside Cusp F-region",            10, 14,   70,  80,   320, 365,                -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("CF_L6", "Dayside Cusp F-region",            10, 14,   70,  80,   365, 410,                -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("CF_L7", "Dayside Cusp F-region",            10, 14,   70,  80,   410, 455,                -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("CF_L8", "Dayside Cusp F-region",            10, 14,   70,  80,   455, 500,                -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("CF_M1", "Dayside Cusp F-region",            10, 14,   70,  80,   140, 230,               -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("CF_M2", "Dayside Cusp F-region",            10, 14,   70,  80,   230, 320,               -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("CF_M3", "Dayside Cusp F-region",            10, 14,   70,  80,   320, 410,               -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("CF_M4", "Dayside Cusp F-region",            10, 14,   70,  80,   410, 500,               -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("CF_H1", "Dayside Cusp F-region",            10, 14,   70,  80,   140, 260,               -90,90,  4, 9,   20*60 ) )
Bins.append( Bin("CF_H2", "Dayside Cusp F-region",            10, 14,   70,  80,   260, 380,               -90,90,  4, 9,   20*60 ) )
Bins.append( Bin("CF_H3", "Dayside Cusp F-region",            10, 14,   70,  80,   380, 500,               -90,90,  4, 9,   20*60 ) )
    
Bins.append( Bin("PCF_L1", "Polar cap F-region",              14, 10,   70,  90,   140, 185,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("PCF_L2", "Polar cap F-region",              14, 10,   70,  90,   185, 230,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("PCF_L3", "Polar cap F-region",              14, 10,   70,  90,   230, 275,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("PCF_L4", "Polar cap F-region",              14, 10,   70,  90,   275, 320,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("PCF_L5", "Polar cap F-region",              14, 10,   70,  90,   320, 365,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("PCF_L6", "Polar cap F-region",              14, 10,   70,  90,   365, 410,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("PCF_L7", "Polar cap F-region",              14, 10,   70,  90,   410, 455,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("PCF_L8", "Polar cap F-region",              14, 10,   70,  90,   455, 500,               -90,90,  0, 2,   50*60 ) )
Bins.append( Bin("PCF_M1", "Polar cap F-region",              14, 10,   70,  90,   140, 230,               -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("PCF_M2", "Polar cap F-region",              14, 10,   70,  90,   230, 320,               -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("PCF_M3", "Polar cap F-region",              14, 10,   70,  90,   320, 410,               -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("PCF_M4", "Polar cap F-region",              14, 10,   70,  90,   410, 500,               -90,90,  2, 4,   30*60 ) )
Bins.append( Bin("PCF_H1", "Polar cap F-region",              14, 10,   70,  90,   140, 260,               -90,90,  4, 9,   20*60 ) )
Bins.append( Bin("PCF_H2", "Polar cap F-region",              14, 10,   70,  90,   260, 380,               -90,90,  4, 9,   20*60 ) )
Bins.append( Bin("PCF_H3", "Polar cap F-region",              14, 10,   70,  90,   380, 500,               -90,90,  4, 9,   20*60 ) )
    
Bins.append( Bin("TRO_01", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,   80,  85,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_02", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,   85,  90,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_03", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,   90,  95,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_04", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,   95, 100,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_05", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  100, 105,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_06", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  105, 110,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_07", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  110, 115,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_08", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  115, 120,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_09", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  120, 125,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_10", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  125, 130,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_11", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  130, 135,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_12", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  135, 140,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_13", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  140, 145,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_14", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  145, 150,                 60,90,  0, 2,   20*60 ) )
Bins.append( Bin("TRO_15", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,   80,  87,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_16", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,   87,  94,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_17", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,   94, 101,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_18", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  101, 108,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_19", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  108, 115,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_20", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  115, 122,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_21", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  122, 129,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_22", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  129, 136,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_23", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  136, 143,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_24", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,  143, 150,                 60,90,  2, 4,   20*60 ) )
Bins.append( Bin("TRO_25", "EISCAT Tromso radar scan region",  0, 24,  -90,  90,   80, 150,                 60,90,  4, 9,   20*60 ) )
    
#Bins.append( Bin("TST_00", "Test region",                      0, 24,  -90,  90,   80, 150,                 60,90,  0, 9,   20*60 ) )
    

    
    
def ClearBins():
    """
        Removes all Bins.
    """
    Bins.clear()     

def CreateNewBin( ID, Description, MagneticLocalTime_from, MagneticLocalTime_to, MagneticLatitude_from, MagneticLatitude_to, Altitude_from, Altitude_to, Kp_from, Kp_to, DesirableTime ):
    """
        Defines a new Bin according to the specified ranges.
        All satellite positions which fall in these ranges will be assigned to this Bin. 
        The plots will be created according to all the defined Bins.
        The library initializes certain predefined Bins. Call ClearBins() in order to remove them.
        Args:
            ID (string): a code name for this Bin. It will be displayed on the plots.
            Description (string): a description for this Bin. It will be displayed on the plots.
            MagneticLocalTime_from: range for Magnetic-Local-Time of the Bin.
            MagneticLocalTime_to: range for Magnetic-Local-Time of the Bin.
            MagneticLatitude_from: range for Magnetic-Latitude of the Bin.
            MagneticLatitude_to: range for Magnetic-Latitude of the Bin.
            Altitude_from: range for Altitude of the Bin.
            Altitude_to: range for Altitude of the Bin.
            Kp_from: range for Kp-index of the Bin.
            Kp_to: range for Kp-index of the Bin.
            DesirableTime: (seconds) The minimun time for the satellite to stay inside the Bin in order to accomplish its mission.
    """
    Bins.append( Bin(ID, Description, MagneticLocalTime_from, MagneticLocalTime_to, MagneticLatitude_from, MagneticLatitude_to, Altitude_from, Altitude_to, Kp_from, Kp_to, DesirableTime) )
    
    
    
    
def getBinDescription( str ):
    """
    Tries to identify the bin according to the given argument and returns its description. If it fails it returns the argument.
    examples: "PCF_H2"->"Polar cap F-region"   "PCF"->"Polar cap F-region"
    """
    result = ""
    for B in Bins:
        if B.ID == str: result = B.Description
    if len(result)==0:
        for B in Bins:
            if B.ID.startswith( str ): result = B.Description
    if len(result)==0: result = str
    #
    return result

def is_MLT_inside_range( MLT, MLT_min, MLT_max ):
    """
        Checks if certain Magnetic-Local-Time lies in a certain range. It can handle ranges like 22-2
        Returns:
            true if MLT falls inside [MLT_min, MLT_max]
    """
    if MLT_min < MLT_max: # example: from 13 to 18 hour
        return (MLT > MLT_min  and  MLT <= MLT_max)
    elif MLT_min == MLT_max: # example: from 12 until 12 the other day
        return True
    else: # example: from 22 to 3 hour
        return (MLT > MLT_min  or   MLT <= MLT_max)

    
    
def GetMatchedBin( MLT, MagLat, Altitude, Kp, Latitude ):
    """
        Finds and returns the Bin object which matches the position of the satellite described by the arguments.
        
        Args:
                MLT: the Magnetic Local Time
                MagLat: The Magnetic Latitude
                Altitude: The Altitude
                Kp: the Kp-index
                Latitude: the Latitude
        Returns:
                Bin: the Bin in which the position represented by the arguments is matched.
    """    
    MatchedBin = None
    for B in Bins:
        if Latitude >= B.Lat_min  and  Latitude <= B.Lat_max:
            if is_MLT_inside_range(MLT, B.MLT_min, B.MLT_max):
                if MagLat   > B.MagLat_min    and  MagLat   <= B.MagLat_max:
                    if Altitude > B.Altitude_min  and  Altitude <= B.Altitude_max:
                        Kp_min_to_check = B.Kp_min
                        if Kp_min_to_check == 0: Kp_min_to_check = -1
                        if Kp       > Kp_min_to_check and  Kp       <= B.Kp_max:
                            MatchedBin = B
                            break
    return MatchedBin



def getBinByItsProperties( MLT_min, MLT_max, MagLat_min, MagLat_max, Altitude_min, Altitude_max, Kp_min, Kp_max ):
    """
        Returns: the bin object which has been defined by the same ranges as the arguments
    """
    CorrectBin = None
    for B in Bins:
        if             MLT_min      == B.MLT_min       and  MLT_max      == B.MLT_max:
            if         MagLat_min   == B.MagLat_min    and  MagLat_max   == B.MagLat_max:
                if     Altitude_min == B.Altitude_min  and  Altitude_max == B.Altitude_max:
                    if Kp_min       == B.Kp_min        and  Kp_max       == B.Kp_max:
                        CorrectBin = B
                        break
    return CorrectBin

def getBinByItsID( aBinID ):
    """
        ReturnsL the Bin object wich has the same ID as the argument
    """
    CorrectBin = None
    for B in Bins:
        if  B.ID == aBinID:
            CorrectBin = B
            break
    return CorrectBin




def CreateResults_CDF( ResultsFilename,  CALCULATIONS_Title="", CALCULATIONS_Description="", CALCULATIONS_RegionName="", CALCULATIONS_OrbitFilesPath="", CALCULATIONS_TIEGCMfolder=""):
    """
        Creates a results NetCDF file and its structure. The file will contain no date.
        The optional parameters are extra information to be added to the result-file.
        Args: 
            ResultsFilename: the full or relative path and filename to be created.
    """
    global all_JH_values, all_MagLat_values, all_MLT_values, all_Altitude_values, all_Kp_values, all_Time_values, all_EEX_values, all_EEY_values, all_Pedersen_values, all_Density_values, all_Lev_values, all_Hall_values
    # save general info
    resultsCDF = Dataset( ResultsFilename, 'w' )
    resultsCDF.Content         = "JOULE HEATING per BIN RESULTS. This file contains information about the bins in which the thermosphere is divided according to Magnetic Latitude, Magnetic Local Time, Altitude and Kp-index. We say there is a hit inside a bin when a satellite position or TIEGCM-grid position lies inside the above boundaries. The file contains data for each hit inside a bin. That is the position's MagLat, MLT, Alt, Kp and Joule-Heating value"
    resultsCDF.DateOfCreation  = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    resultsCDF.DateOfUpdate    = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    resultsCDF.Title           = CALCULATIONS_Title
    resultsCDF.Region          = CALCULATIONS_RegionName
    resultsCDF.OrbitFile       = CALCULATIONS_OrbitFilesPath
    resultsCDF.Description     = CALCULATIONS_Description
    resultsCDF.DataPath        = CALCULATIONS_TIEGCMfolder
    resultsCDF.LastExecDurationSec = 0
    resultsCDF.Progress        = ""
    # save data for each bin spearately 
    resultsCDF.createDimension( "SingleSpaceFooDimension", 1 )
    resultsCDF.createDimension('char8', 8)
    for B in Bins:
        # save general info about the bin
        VAR_BinInfo = resultsCDF.createVariable( B.ID, "S1", ("SingleSpaceFooDimension",) )
        VAR_BinInfo.long_name    = "Information about the bin " + B.ID + " (" + B.Description + ")"
        VAR_BinInfo.MagLat_min   = "{:02.0f}".format(B.MagLat_min)
        VAR_BinInfo.MagLat_max   = "{:02.0f}".format(B.MagLat_max)
        VAR_BinInfo.MLT_min      = "{:02.0f}".format(B.MLT_min)
        VAR_BinInfo.MLT_max      = "{:02.0f}".format(B.MLT_max)
        VAR_BinInfo.Altitude_min = "{:02.0f}".format(B.Altitude_min)
        VAR_BinInfo.Altitude_max = "{:02.0f}".format(B.Altitude_max)
        VAR_BinInfo.Lat_min       = "{:02.0f}".format(B.Lat_min)
        VAR_BinInfo.Lat_max       = "{:02.0f}".format(B.Lat_max)
        VAR_BinInfo.Kp_min       = "{:02.0f}".format(B.Kp_min)
        VAR_BinInfo.Kp_max       = "{:02.0f}".format(B.Kp_max)
        VAR_BinInfo.JH_mean      = "{:.3e}".format(B.JH_mean)
        VAR_BinInfo.JH_variance  = "{:.3e}".format(B.JH_variance)
        VAR_BinInfo.DesirableCumulativeTime = str(B.DesirableCumulativeTime) + "sec"
        if B.JH_min == 99999: 
            VAR_BinInfo.JH_min = ""
        else:
            VAR_BinInfo.JH_min = "{:.3e}".format(B.JH_min)
        # create structure for each bin
        resultsCDF.createDimension( B.ID+"_time_dim", None )
        VAR_BinTimeValues             = resultsCDF.createVariable( B.ID+"_TimeValues", "f4", (B.ID+"_time_dim",) )
        VAR_BinTimeValues.description = "UTC timestamp"
        VAR_BinTimeValues.units       = "seconds"
        resultsCDF.createDimension( B.ID+"_jh_dim", None )
        VAR_BinJHvalues = resultsCDF.createVariable( B.ID+"_JHValues", "f4", (B.ID+"_jh_dim",) )
        VAR_BinJHvalues.description = "Ohmic"
        VAR_BinJHvalues.units       = "W/m3"
        resultsCDF.createDimension( B.ID+"_maglat_dim", None )
        VAR_BinMagLatValues = resultsCDF.createVariable( B.ID+"_MagLatValues", "f4", (B.ID+"_maglat_dim",) )
        VAR_BinMagLatValues.description = "Magnetic Latitude"
        VAR_BinMagLatValues.units       = "degrees"
        resultsCDF.createDimension( B.ID+"_mlt_dim", None )
        VAR_BinMLTValues = resultsCDF.createVariable( B.ID+"_MLTValues", "f4", (B.ID+"_mlt_dim",) )
        VAR_BinMLTValues.description = "Magnetic Local Time"
        VAR_BinMLTValues.units       = "hours"
        resultsCDF.createDimension( B.ID+"_alt_dim", None )
        VAR_BinAltitudeValues = resultsCDF.createVariable( B.ID+"_AltitudeValues", "f4", (B.ID+"_alt_dim",) )
        VAR_BinAltitudeValues.description = "Altitude from the surface of the Earth"
        VAR_BinAltitudeValues.units       = "km"
        resultsCDF.createDimension( B.ID+"_lat_dim", None )
        VAR_BinLatValues = resultsCDF.createVariable( B.ID+"_LatValues", "f4", (B.ID+"_lat_dim",) )
        VAR_BinLatValues.description = "Latitude"
        VAR_BinLatValues.units       = "degrees"
        resultsCDF.createDimension( B.ID+"_kp_dim", None )
        VAR_BinKpValues = resultsCDF.createVariable( B.ID+"_KpValues", "f4", (B.ID+"_kp_dim",) )
        VAR_BinKpValues.description = "Kp index of Sun activity"
        VAR_BinKpValues.units       = "-"
        resultsCDF.createDimension( B.ID+"_eex_dim", None )
        VAR_BinEEXValues = resultsCDF.createVariable( B.ID+"_EEXValues", "f4", (B.ID+"_eex_dim",) )
        VAR_BinEEXValues.description = "Electric field strength East. (SI)"
        VAR_BinEEXValues.units       = "V/m"
        resultsCDF.createDimension( B.ID+"_eey_dim", None )
        VAR_BinEEYValues = resultsCDF.createVariable( B.ID+"_EEYValues", "f4", (B.ID+"_eey_dim",) )
        VAR_BinEEYValues.description = "Electric field strength North. (SI)"
        VAR_BinEEYValues.units       = "V/m"
        resultsCDF.createDimension( B.ID+"_ped_dim", None )
        VAR_BinPedersenValues = resultsCDF.createVariable( B.ID+"_PedersenValues", "f4", (B.ID+"_ped_dim",) )
        VAR_BinPedersenValues.description = "SIGMA_PED"
        VAR_BinPedersenValues.units       = "S/m"
        resultsCDF.createDimension( B.ID+"_den_dim", None )
        VAR_BinDensityValues = resultsCDF.createVariable( B.ID+"_DensityValues", "f4", (B.ID+"_den_dim",) )
        VAR_BinDensityValues.description = "Total Density"
        VAR_BinDensityValues.units       = "g/cm3"
        resultsCDF.createDimension( B.ID+"_lev_dim", None )
        VAR_BinLevValues = resultsCDF.createVariable( B.ID+"_LevValues", "f4", (B.ID+"_lev_dim",) )
        VAR_BinLevValues.description = "midpoint levels"
        VAR_BinLevValues.units       = ""
        resultsCDF.createDimension( B.ID+"_hal_dim", None )
        VAR_BinHallValues = resultsCDF.createVariable( B.ID+"_HallValues", "f4", (B.ID+"_hal_dim",) )
        VAR_BinHallValues.description = "SIGMA_HAL"
        VAR_BinHallValues.units       = "S/m"
        resultsCDF.createDimension( B.ID+"_convh_dim", None )
        VAR_BinConvhValues = resultsCDF.createVariable( B.ID+"_ConvectionHeatingValues", "f4", (B.ID+"_convh_dim",) )
        VAR_BinConvhValues.description = "Convection Heating"
        VAR_BinConvhValues.units       = "W/m3"
        resultsCDF.createDimension( B.ID+"_windh_dim", None )
        VAR_BinWindhValues = resultsCDF.createVariable( B.ID+"_WindHeatingValues", "f4", (B.ID+"_windh_dim",) )
        VAR_BinWindhValues.description = "Wind Correction"
        VAR_BinWindhValues.units       = "W/m3"
    ## save data for all hits
    resultsCDF.createDimension( "time_dim", None )
    VAR_TimeValues         = resultsCDF.createVariable("allTimeValues", "f4", ("time_dim",) )
    VAR_TimeValues.description = "UTC timestamp"
    VAR_TimeValues.units       = "seconds"
    resultsCDF.createDimension( "jh_dim", None )
    VAR_JHvalues = resultsCDF.createVariable("allJHValues", "f4", ("jh_dim",) )
    VAR_JHvalues.description = "Ohmic"
    VAR_JHvalues.units       = "W/m3"
    resultsCDF.createDimension( "maglat_dim", None )
    VAR_MagLatValues = resultsCDF.createVariable("allMagLatValues", "f4", ("maglat_dim",) )
    VAR_MagLatValues.description = "Magnetic Latitude"
    VAR_MagLatValues.units       = "degrees"
    resultsCDF.createDimension( "mlt_dim", None )
    VAR_MLTValues = resultsCDF.createVariable("allMLTValues", "f4", ("mlt_dim",) )
    VAR_MLTValues.description = "Magnetic Local Time"
    VAR_MLTValues.units       = "hours"
    resultsCDF.createDimension( "alt_dim", None )
    VAR_AltitudeValues = resultsCDF.createVariable("allAltitudeValues", "f4", ("alt_dim",) )
    VAR_AltitudeValues.description = "Altitude from the surface of the Earth"
    VAR_AltitudeValues.units       = "km"
    resultsCDF.createDimension( "lat_dim", None )
    VAR_LatValues = resultsCDF.createVariable("allLatValues", "f4", ("lat_dim",) )
    VAR_LatValues.description = "Latitude"
    VAR_LatValues.units       = "degrees"
    resultsCDF.createDimension( "kp_dim", None )
    VAR_KpValues = resultsCDF.createVariable("allKpValues", "f4", ("kp_dim",) )
    VAR_KpValues.description = "Kp index of Sun activity"
    VAR_KpValues.units       = "-"
    resultsCDF.createDimension( "bins_dim", None )
    VAR_HittedBinIDs = resultsCDF.createVariable("allHittedBinIDs", "S1", ("bins_dim","char8",) )
    VAR_HittedBinIDs.description = "The ID of the bin, where the hit occured"
    resultsCDF.createDimension( "eex_dim", None )
    VAR_EEXvalues = resultsCDF.createVariable("allEEXValues", "f4", ("eex_dim",) )
    VAR_EEXvalues.description = "Electric field strength East. (SI)"
    VAR_EEXvalues.units       = "V/m"
    resultsCDF.createDimension( "eey_dim", None )
    VAR_EEYvalues = resultsCDF.createVariable("allEEYValues", "f4", ("eey_dim",) )
    VAR_EEYvalues.description = "Electric field strength North. (SI)"
    VAR_EEYvalues.units       = "V/m"
    resultsCDF.createDimension( "ped_dim", None )
    VAR_Pedersenvalues = resultsCDF.createVariable("allPedersenValues", "f4", ("ped_dim",) )
    VAR_Pedersenvalues.description = "Pedersen Conductivity"
    VAR_Pedersenvalues.units       = "S/m"
    resultsCDF.createDimension( "den_dim", None )
    VAR_Densityvalues = resultsCDF.createVariable("allDensityValues", "f4", ("den_dim",) )
    VAR_Densityvalues.description = "Total Density"
    VAR_Densityvalues.units       = "g/cm3"
    resultsCDF.createDimension( "lev_dim", None )
    VAR_LevValues = resultsCDF.createVariable("allLevValues", "f4", ("lev_dim",) )
    VAR_LevValues.description = "midpoint levels"
    VAR_LevValues.units       = ""
    resultsCDF.createDimension( "hal_dim", None )
    VAR_Hallvalues = resultsCDF.createVariable("allHallValues", "f4", ("hal_dim",) )
    VAR_Hallvalues.description = "Hall Conductivity"
    VAR_Hallvalues.units       = "S/m"
    resultsCDF.createDimension( "convh_dim", None )
    VAR_ConvhValues = resultsCDF.createVariable("allConvectionHeatingValues", "f4", ("convh_dim",) )
    VAR_ConvhValues.description = "Convection Heating"
    VAR_ConvhValues.units       = "W/m3"
    resultsCDF.createDimension( "windh_dim", None )
    VAR_WindhValues = resultsCDF.createVariable("allWindHeatingValues", "f4", ("windh_dim",) )
    VAR_WindhValues.description = "Wind Correction"
    VAR_WindhValues.units       = "W/m3"
    resultsCDF.close()
    
    
def SaveResults_CDF( ResultsFilename, DataFilename ):
    """
        Append the results in a NetCDF file which can contain results of several calculations.
        The data will be saved in ResultsFilename and they come from calculations on the netcdf DataFilename.
        DataFilename is needed to check if the file contains already the results of calculations on that file.
        Args: 
            ResultsFilename: the netcdf file where the results will be stored.
            DataFilename: the netcdf file (with orbit or tiegcm data ) on which the calculation have taken place. 
    """
    if path.exists( ResultsFilename ) == False:
        CreateResults_CDF( ResultsFilename )
    # save general info
    ErrorMsg = ""
    resultsCDF = Dataset( ResultsFilename, 'a' )
    resultsCDF.DateOfUpdate = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    if resultsCDF.Region    != CALCULATIONS_RegionName: ErrorMsg = "Save aborted: NetCDF file has already data about region " + resultsCDF.Region + " and you tried to save data about region " + CALCULATIONS_RegionName        
    if resultsCDF.OrbitFile != CALCULATIONS_OrbitFilesPath: ErrorMsg = "Save aborted: NetCDF file has already data about orbit " + resultsCDF.OrbitFile + " and you tried to save data about orbit " + DataFilename
    if resultsCDF.DataPath  != CALCULATIONS_TIEGCMfolder: ErrorMsg = "Save aborted: NetCDF file has already data about TIEGCM file " + resultsCDF.DataPath  + "and you tried to save data about TIEGCM file " + CALCULATIONS_TIEGCMfolder        
    if len(DataFilename)>0 and resultsCDF.Progress > DataFilename: ErrorMsg = "Save aborted: NetCDF file contains data about file: " + resultsCDF.Progress + " which is later than " + DataFilename
    if len(ErrorMsg) > 0:
        print( ErrorMsg )
        resultsCDF.close()
        return
    resultsCDF.LastExecDurationSec = ConvertLeadingZerosToSpaces("{0:.0f}".format(CALCULATIONS_ExecutionDuration)).strip()
    # save data for each bin spearately 
    for B in Bins:
        # save data about the hits inside the bin
        if len(B.Time_values) > 0:
            resultsCDF.variables[B.ID+"_TimeValues"][:]      = resultsCDF.variables[B.ID+"_TimeValues"][:].tolist() + B.Time_values
            resultsCDF.variables[B.ID+"_JHValues"][:]        = resultsCDF.variables[B.ID+"_JHValues"][:].tolist() + B.JH_values        
            resultsCDF.variables[B.ID+"_MagLatValues"][:]    = resultsCDF.variables[B.ID+"_MagLatValues"][:].tolist() + B.MagLat_values
            resultsCDF.variables[B.ID+"_MLTValues"][:]       = resultsCDF.variables[B.ID+"_MLTValues"][:].tolist() + B.MLT_values
            resultsCDF.variables[B.ID+"_AltitudeValues"][:]  = resultsCDF.variables[B.ID+"_AltitudeValues"][:].tolist() + B.Altitude_values
            resultsCDF.variables[B.ID+"_LatValues"][:]       = resultsCDF.variables[B.ID+"_LatValues"][:].tolist() + B.Lat_values
            resultsCDF.variables[B.ID+"_KpValues"][:]        = resultsCDF.variables[B.ID+"_KpValues"][:].tolist() + B.Kp_values
            resultsCDF.variables[B.ID+"_EEXValues"][:]       = resultsCDF.variables[B.ID+"_EEXValues"][:].tolist() + B.EEX_values        
            resultsCDF.variables[B.ID+"_EEYValues"][:]       = resultsCDF.variables[B.ID+"_EEYValues"][:].tolist() + B.EEY_values
            resultsCDF.variables[B.ID+"_PedersenValues"][:]  = resultsCDF.variables[B.ID+"_PedersenValues"][:].tolist() + B.Pedersen_values
            resultsCDF.variables[B.ID+"_DensityValues"][:]   = resultsCDF.variables[B.ID+"_DensityValues"][:].tolist() + B.Density_values
            resultsCDF.variables[B.ID+"_LevValues"][:]       = resultsCDF.variables[B.ID+"_LevValues"][:].tolist() + B.Lev_values
            resultsCDF.variables[B.ID+"_HallValues"][:]      = resultsCDF.variables[B.ID+"_HallValues"][:].tolist() + B.Hall_values
            resultsCDF.variables[B.ID+"_ConvectionHeatingValues"][:] = resultsCDF.variables[B.ID+"_ConvectionHeatingValues"][:].tolist() + B.ConvectionHeating_values
            resultsCDF.variables[B.ID+"_WindHeatingValues"][:] = resultsCDF.variables[B.ID+"_WindHeatingValues"][:].tolist() + B.WindHeating_values
    ## save data for all hits
    if len(all_Time_values) > 0:
        resultsCDF.variables["allTimeValues"][:]     = resultsCDF.variables["allTimeValues"][:].tolist() + all_Time_values
        resultsCDF.variables["allJHValues"][:]       = resultsCDF.variables["allJHValues"][:].tolist() + all_JH_values    
        resultsCDF.variables["allMagLatValues"][:]   = resultsCDF.variables["allMagLatValues"][:].tolist() + all_MagLat_values
        resultsCDF.variables["allMLTValues"][:]      = resultsCDF.variables["allMLTValues"][:].tolist() + all_MLT_values
        resultsCDF.variables["allAltitudeValues"][:] = resultsCDF.variables["allAltitudeValues"][:].tolist() + all_Altitude_values
        resultsCDF.variables["allLatValues"][:]      = resultsCDF.variables["allLatValues"][:].tolist() + all_Lat_values
        resultsCDF.variables["allKpValues"][:]       = resultsCDF.variables["allKpValues"][:].tolist() + all_Kp_values
        #resultsCDF.variables["allHittedBinIDs"][:]   = resultsCDF.variables["allHittedBinIDs"][:].tolist() + netCDF4.stringtochar(np.array(all_HittedBin_IDs[:], 'S8'))
        resultsCDF.variables["allEEXValues"][:]      = resultsCDF.variables["allEEXValues"][:].tolist() + all_EEX_values
        resultsCDF.variables["allEEYValues"][:]      = resultsCDF.variables["allEEYValues"][:].tolist() + all_EEY_values
        resultsCDF.variables["allPedersenValues"][:] = resultsCDF.variables["allPedersenValues"][:].tolist() + all_Pedersen_values
        resultsCDF.variables["allDensityValues"][:]  = resultsCDF.variables["allDensityValues"][:].tolist() + all_Density_values
        resultsCDF.variables["allLevValues"][:]      = resultsCDF.variables["allLevValues"][:].tolist() + all_Lev_values
        resultsCDF.variables["allHallValues"][:]     = resultsCDF.variables["allHallValues"][:].tolist() + all_Hall_values
        resultsCDF.variables["allConvectionHeatingValues"][:] = resultsCDF.variables["allConvectionHeatingValues"][:].tolist() + all_ConvectionHeating_values
        resultsCDF.variables["allWindHeatingValues"][:] = resultsCDF.variables["allWindHeatingValues"][:].tolist() + all_WindHeating_values
    #
    resultsCDF.close()    
    



    


def LoadResults_CDF( filepath, VariableToLoad, loadBinValues=True, loadGlobalValues=True, loadTimeValues=True, loadMagLatValues=True, loadMLTvalues=True, loadAltValues=True, loadLatValues=True, loadKpValues=True ):
    """
        Reads the calculation results from a netcdf result-file and fills with data the corresponding Bins.
        User must choose a Variable to work with (see start of this module for available variables).
        User can choose which other parallel data to load in order to produce the plots he is interested in, in order to speed up loading
        Args: 
             filepath: the netcdf resul-filename to be loaded or a folder (the last character has to be a slash '/') which contains many netcdf result-files.
             VariableToLoad: the variable which the user is interested in. Only data about this variable will be loaded
    """
    global CALCULATIONS_Title, CALCULATIONS_Description, CALCULATIONS_RegionName, CALCULATIONS_OrbitFilesPath, CALCULATIONS_TIEGCMfolder, CALCULATIONS_ExecutionDuration
    global all_JH_values, all_MagLat_values, all_MLT_values, all_Altitude_values, all_Kp_values, all_Time_values, all_EEX_values, all_EEY_values, all_Pedersen_values, all_Density_values, all_Lev_values, all_Hall_values

    # reset values
    for B in Bins:
        B.reset()
    all_JH_values.clear()
    all_MagLat_values.clear()
    all_MLT_values.clear()
    all_Altitude_values.clear()
    all_Lat_values.clear()
    all_Kp_values.clear() 
    all_Time_values.clear()
    all_HittedBin_IDs.clear()
    all_EEX_values.clear()
    all_EEY_values.clear()
    all_Pedersen_values.clear()
    all_Density_values.clear()
    all_Lev_values.clear()
    all_Hall_values.clear()
    all_ConvectionHeating_values.clear()
    all_WindHeating_values.clear()
    
    print( "Started Loading", filepath, datetime.now() )

    # make a list of all the files we are going to load
    All_ResultFilenames = list()
    if filepath[-1] == '/':
        All_ResultFilenames = sorted( glob.glob(filepath+"*.nc") )
    else:
        All_ResultFilenames.append( filepath )
    
    # load each file into memory
    for file_idx in range(0, len(All_ResultFilenames)):
        if file_idx % 10 == 0: print( "Now Loading", All_ResultFilenames[file_idx] )
        #if file_idx == 30: break
        resultsCDF = Dataset( All_ResultFilenames[file_idx], 'r' )
        #### load general information
        if file_idx == 0:
            try:
                print( "DateOfCreation:", resultsCDF.DateOfCreation, " LastExecDurationSec :", resultsCDF.LastExecDurationSec , "sec" )
                #print( "Title:", resultsCDF.Title, " Description:", resultsCDF.Description )
                print( "Region:", resultsCDF.Region )
                print( "OrbitFile:", resultsCDF.OrbitFile )
                print( "TIEGCM data path:", resultsCDF.DataPath, "\n" )
                #print( "Progress:", resultsCDF.Progress, "\n" )
            except:
                pass
            CALCULATIONS_Title = resultsCDF.Title
            CALCULATIONS_Description = resultsCDF.Description
            #CALCULATIONS_ExecutionDuration = resultsCDF.LastExecDurationSec
            CALCULATIONS_RegionName = resultsCDF.Region
            CALCULATIONS_OrbitFilesPath = resultsCDF.OrbitFile.split()
            CALCULATIONS_TIEGCMfolder = resultsCDF.DataPath
        #### load data for each bin
        if loadBinValues:
            for B in Bins:
                try:
                    if loadTimeValues and len(CALCULATIONS_OrbitFilesPath) > 0: concatLists( B.Time_values, list(resultsCDF.variables[ B.ID+"_TimeValues" ][:]) )
                    if loadMagLatValues: concatLists( B.MagLat_values, list(resultsCDF.variables[ B.ID+"_MagLatValues" ][:]) )
                    if loadMLTvalues: concatLists( B.MLT_values, list(resultsCDF.variables[ B.ID+"_MLTValues" ][:]) )
                    if loadAltValues: concatLists( B.Altitude_values, list(resultsCDF.variables[ B.ID+"_AltitudeValues" ][:]) )
                    try:
                        if loadLatValues: concatLists(B.Lat_values, list(resultsCDF.variables[ B.ID+"_LatValues" ][:]) )
                    except:
                        pass
                    if loadKpValues: concatLists(B.Kp_values, list(resultsCDF.variables[ B.ID+"_KpValues" ][:]) )
                    if VariableToLoad == "Ohmic":    
                        try:
                            Ohmics = resultsCDF.variables[ B.ID+"_ConvectionHeatingValues" ][:] + resultsCDF.variables[ B.ID+"_WindHeatingValues" ][:]
                            concatLists( B.JH_values, list(Ohmics) ) #    if VariableToLoad == "Ohmic":     concatLists( B.JH_values, list(resultsCDF.variables[ B.ID+"_ConvenctionHeatingValues" ][:]+resultsCDF.variables[ B.ID+"_WindHeatingValues" ][:]) )
                        except:
                            Ohmics = resultsCDF.variables[ B.ID+"_JHValues" ][:]
                            concatLists( B.JH_values, list(Ohmics) )
                    if VariableToLoad == "EEX":    concatLists( B.JH_values, list(resultsCDF.variables[ B.ID+"_EEXValues" ][:])*1000 ) #if VariableToLoad == "EEX_si":    B.EEX_values = list(resultsCDF.variables[ B.ID+"_EEXValues" ][:])
                    if VariableToLoad == "EEY":    concatLists( B.JH_values, list(resultsCDF.variables[ B.ID+"_EEYValues" ][:])*1000 ) #if VariableToLoad == "EEY_si":    B.EEY_values = list(resultsCDF.variables[ B.ID+"_EEYValues" ][:])
                    if VariableToLoad == "SIGMA_PED": concatLists( B.JH_values, list(resultsCDF.variables[ B.ID+"_PedersenValues" ][:]) ) #if VariableToLoad == "SIGMA_PED": B.Pedersen_values = list(resultsCDF.variables[ B.ID+"_PedersenValues" ][:])
                    if VariableToLoad == "SIGMA_HAL": concatLists( B.JH_values, list(resultsCDF.variables[ B.ID+"_HallValues" ][:]) ) #if VariableToLoad == "SIGMA_HAL": B.Hall_values = list(resultsCDF.variables[ B.ID+"_HallValues" ][:])
                    try:
                        if VariableToLoad == "Convection_heating": concatLists( B.JH_values, list(resultsCDF.variables[ B.ID+"_ConvectionHeatingValues" ][:]) )
                    except:
                        if VariableToLoad == "Convection_heating": concatLists( B.JH_values, list(resultsCDF.variables[ B.ID+"_ConvenctionHeatingValues" ][:]) )
                    if VariableToLoad == "Wind_heating": concatLists( B.JH_values, list(resultsCDF.variables[ B.ID+"_WindHeatingValues" ][:]) )
                except: # data about this region do not exist inside this netcdf file
                    continue
        #### load collective data about all bins
        if loadGlobalValues:
            if loadTimeValues and len(CALCULATIONS_OrbitFilesPath) > 0: concatLists( all_Time_values, list(resultsCDF.variables[ "allTimeValues" ][:]) )
            if loadMagLatValues:  concatLists( all_MagLat_values, list(resultsCDF.variables[ "allMagLatValues" ][:]) )
            if loadMLTvalues: concatLists( all_MLT_values, list(resultsCDF.variables[ "allMLTValues" ][:]) )
            if loadAltValues: concatLists( all_Altitude_values, list(resultsCDF.variables[ "allAltitudeValues" ][:]) )
            try:
                if loadLatValues: concatLists( all_Lat_values, list(resultsCDF.variables[ "allLatValues" ][:]) )
            except:
                pass
            if loadKpValues: concatLists( all_Kp_values, list(resultsCDF.variables[ "allKpValues" ][:]) )
            if VariableToLoad == "Ohmic": 
                try:
                    Ohmics = resultsCDF.variables[ "allConvectionHeatingValues" ][:] + resultsCDF.variables[ "allWindHeatingValues" ][:]
                    concatLists( all_JH_values, list(Ohmics) ) #if VariableToLoad == "Ohmic":     concatLists( all_JH_values, list(resultsCDF.variables[ "allConvenctionHeatingValues" ][:] + resultsCDF.variables[ "allWindHeatingValues" ][:]) )
                except:
                    Ohmics = resultsCDF.variables[ "allJHValues" ][:]
                    concatLists( all_JH_values, list(Ohmics) ) 
            if VariableToLoad == "EEX":    concatLists( all_JH_values, list(resultsCDF.variables[ "allEEXValues" ][:]*1000) )#if VariableToLoad == "EEX_si":    all_EEX_values = list(resultsCDF.variables[ "allEEXValues" ][:])
            if VariableToLoad == "EEY":    concatLists( all_JH_values, list(resultsCDF.variables[ "allEEYValues" ][:]*1000) )#if VariableToLoad == "EEY_si":    all_EEY_values = list(resultsCDF.variables[ "allEEYValues" ][:])
            if VariableToLoad == "SIGMA_PED": concatLists( all_JH_values, list(resultsCDF.variables[ "allPedersenValues" ][:]) )#if VariableToLoad == "SIGMA_PED": all_Pedersen_values = list(resultsCDF.variables[ "allPedersenValues" ][:])
            if VariableToLoad == "SIGMA_HAL": concatLists( all_JH_values, list(resultsCDF.variables[ "allHallValues" ][:]) )#if VariableToLoad == "SIGMA_HAL": all_Hall_values = list(resultsCDF.variables[ "allHallValues" ][:])
            if VariableToLoad == "JH/mass":   concatLists( all_JH_values, list(resultsCDF.variables[ "allJHValues" ][:]/(1000*resultsCDF.variables[ "allDensityValues" ][:]) ) )
            if VariableToLoad == "JH/pressure": 
                #newVals = np.zeros( len(resultsCDF.variables[ "allJHValues" ]) )
                #for i in range( 0, len(resultsCDF.variables[ "allJHValues" ]) ):
                #    newVals[i] = resultsCDF.variables[ "allJHValues" ][i]/(0.00005*math.exp(-resultsCDF.variables[ "allLevValues" ][i]) )  
                #concatLists( all_JH_values, list(newVals) )
                #print( "QQQQ ", resultsCDF.variables[ "allJHValues" ][1], resultsCDF.variables[ "allJHValues" ][1000] )
                #print( "QQQQ ", resultsCDF.variables[ "allAltitudeValues" ][1],  resultsCDF.variables[ "allAltitudeValues" ][1000] )
                concatLists( all_JH_values, list(resultsCDF.variables[ "allJHValues" ][:]/(0.00005*np.exp(-resultsCDF.variables[ "allLevValues" ][:]) ) ) )
            try:
                if VariableToLoad == "Convection_heating": concatLists( all_JH_values, list(resultsCDF.variables[ "allConvectionHeatingValues" ][:]) )
            except:
                if VariableToLoad == "Convection_heating": concatLists( all_JH_values, list(resultsCDF.variables[ "allConvenctionHeatingValues" ][:]) )
            if VariableToLoad == "Wind_heating": concatLists( all_JH_values, list(resultsCDF.variables[ "allWindHeatingValues" ][:]) )
        #### close and go on
        resultsCDF.close()
    ########
    
    # !!!! remove incorrect huge or negative Ohmic values
    if (VariableToLoad == "Ohmic")  and  ("Hz" in filepath or "Tri" in filepath):
        # for each bin
        for B in Bins:
            if len(B.JH_values): print(B.ID, "LENGTH BEFORE:", len(B.JH_values))
            huge_values = 0
            negative_values = 0
            nan_values = 0
            found_at_current_round = True
            while found_at_current_round:
                found_at_current_round = False
                for t in range(0, len(B.JH_values)):
                    if B.JH_values[t] > 100 or B.JH_values[t] == float("inf"):  huge_values += 1
                    if B.JH_values[t] < 0   or B.JH_values[t] == float("-inf"): negative_values += 1
                    if np.isnan(B.JH_values[t]): nan_values += 1
                    if B.JH_values[t]>100 or B.JH_values[t]<0 or np.isnan(B.JH_values[t]) or B.JH_values[t]==float("inf") or B.JH_values[t]==float("-inf"):
                        found_at_current_round = True
                        del B.JH_values[t]
                        if len(B.Time_values) > 0: del B.Time_values[t]
                        if len(B.MagLat_values) > 0: del B.MagLat_values[t]
                        if len(B.MLT_values) > 0: del B.MLT_values[t]
                        if len(B.Altitude_values) > 0: del B.Altitude_values[t]
                        if len(B.Lat_values) > 0: del B.Lat_values[t]
                        if len(B.Kp_values) > 0: del B.Kp_values[t]
                        break
            if len(B.JH_values): print( B.ID, ":",  "huge values =", huge_values, "negative values =", negative_values, "nan values =", nan_values )
            if len(B.JH_values): print(B.ID, "LENGTH AFTER:", len(B.JH_values))
        # for arrays with all the data
        print("ALL", "LENGTH BEFORE:", len(all_JH_values))
        huge_values = 0
        negative_values = 0
        nan_values = 0
        found_at_current_round = True
        while found_at_current_round:
            found_at_current_round = False
            for t in range(0, len(all_JH_values)):
                if all_JH_values[t] > 100 or all_JH_values[t] == float("inf"):  huge_values += 1
                if all_JH_values[t] < 0   or all_JH_values[t] == float("-inf"): negative_values += 1
                if np.isnan(all_JH_values[t]): nan_values += 1
                if all_JH_values[t]>100 or all_JH_values[t]<0 or np.isnan(all_JH_values[t]) or all_JH_values[t]==float("inf") or all_JH_values[t]==float("-inf"):
                    found_at_current_round = True
                    del all_JH_values[t]
                    if len(all_Time_values) > 0: del all_Time_values[t]
                    if len(all_MagLat_values) > 0: del all_MagLat_values[t]
                    if len(all_MLT_values) > 0: del all_MLT_values[t]
                    if len(all_Altitude_values) > 0: del all_Altitude_values[t]
                    if len(all_Lat_values) > 0: del all_Lat_values[t]
                    if len(all_Kp_values) > 0: del all_Kp_values[t]
                    break
        #print( "Globaly", ":",  "huge values =", huge_values, "negative values =", negative_values, "nan values =", nan_values )
        #print("ALL", "LENGTH AFTER:", len(all_JH_values))
    else:
        pass
        #print( "NO correct value check:", VariableToLoad , filepath )
    ########
    CalculateStatsOnData()
    print( "Results loaded for", VariableToLoad, "    ", datetime.now(), "\n" )

    
    
    
    

    
    
    
    
    
    
###########################################################################################################################
############################# CALCULATIONS ################################################################################
###########################################################################################################################
















def AssignJouleHeatingValuesToBins_AlongOrbit( TIEGCM_filesPath, Orbit_filesPath, ResultsFilename ): 
    """
        Reads the orbit positions and fills the correct Bin with values for each position.
        
        Args:
            TIEGCM_filesPath: the folder which has all TIEGCM netcdf files. Needed to read the Kp index for each satellite position.
            Orbit_filesPath: the folder which has the netCDF files which contain all the positions of the satellite.
            ResultsFilename: the netcdf file where the results of this calculation will be stored.
    """    
    
    if path.exists( ResultsFilename ): 
        print("Skipping because exists:", ResultsFilename)
        return
    
    # initialize
    MagLat_min =  1000
    MagLat_max = -1000
    MLT_min    =  1000
    MLT_max    = -1000
    Altitude_min    =  1000
    Altitude_max    = -1000
    Lat_min     =  1000
    Lat_max     = -1000
    Kp_min     =  1000
    Kp_max     = -1000
    for B in Bins:
        B.reset()
        if B.MagLat_min < MagLat_min: MagLat_min = B.MagLat_min 
        if B.MagLat_max > MagLat_max: MagLat_max = B.MagLat_max
        if B.MLT_min < MLT_min: MLT_min = B.MLT_min 
        if B.MLT_max > MLT_max: MLT_max = B.MLT_max
        if B.Altitude_min < Altitude_min: Altitude_min = B.Altitude_min 
        if B.Altitude_max > Altitude_max: Altitude_max = B.Altitude_max
        if B.Lat_min < Lat_min: Lat_min = B.Lat_min 
        if B.Lat_max > Lat_max: Lat_max = B.Lat_max                                
        if B.Kp_min < Kp_min: Kp_min = B.Kp_min 
        if B.Kp_max > Kp_max: Kp_max = B.Kp_max                    
            
    # miscellaneous
    currentfilenumber = -1        
    Matches = 0
    Errors  = 0
    # information about the TIEGCM files
    TIEGCMfilenamePrefix  = "tiegcm" 
    TIEGCMfilenamePostfix = ""

    # read orbit file
    current_timestamp_offset = 0 # increases after each satellite position is parsed
    AllOrbitFiles = sorted( glob.glob( Orbit_filesPath + "*.nc" ) )
    for currentOrbitFile in AllOrbitFiles:
        current_timestamp_offset = 0 # reseted ONLY when the orbits of 2 satellites are inside the folder (one file each)
        print( "\nReading Orbit file:", currentOrbitFile )
        try:
            Orbit_CDF = Dataset( currentOrbitFile, 'r' )
        except:
            print ( "WRONG FORMAT:", currentDataFile )
            continue
        # Load data from the netCDF file
        ORBIT_Times      = Orbit_CDF.variables['time'][:]
        try:
            ORBIT_MagLats    = Orbit_CDF.variables['DaedalusMagneticLatitude'][:]
        except:
            ORBIT_MagLats    = Orbit_CDF.variables['MagneticLatitude'][:]
        try:
            ORBIT_MLTs       = Orbit_CDF.variables['DaedalusMLT'][:]
        except:
            ORBIT_MLTs       = Orbit_CDF.variables['MLT'][:]
        ORBIT_Altitudes  = Orbit_CDF.variables['ZGMID'][:] / 100000
        ORBIT_Lats       = Orbit_CDF.variables['lat'][:]
        ORBIT_Ohmic      = Orbit_CDF.variables['Ohmic'][:]
        ORBIT_Density    = Orbit_CDF.variables['DEN'][:]
        try:
            ORBIT_Lev    = Orbit_CDF.variables['lev'][:]
        except:
            ORBIT_Lev    = list()
        try:
            ORBIT_ConvH  = Orbit_CDF.variables['Convection_heating'][:]
        except:
            ORBIT_ConvH  = Orbit_CDF.variables['Convenction_heating'][:]
        ORBIT_WindH  = Orbit_CDF.variables['Wind_heating'][:]
        try: 
            ORBIT_EEX    = Orbit_CDF.variables['EEX'][:] 
        except: 
            try:
                ORBIT_EEX    = Orbit_CDF.variables['EEX_si'][:] 
            except:
                ORBIT_EEX    = list()
        try: 
            ORBIT_EEY    = Orbit_CDF.variables['EEY'][:] 
        except: 
            try:
                ORBIT_EEY    = Orbit_CDF.variables['EEY_si'][:] 
            except:
                ORBIT_EEY    = list()  
        try: 
            ORBIT_Pedersen = Orbit_CDF.variables['SIGMA_PED'][:] 
        except: 
            ORBIT_Pedersen = list()            
        try: 
            ORBIT_Hall    = Orbit_CDF.variables['SIGMA_HAL'][:] 
        except: 
            ORBIT_Hall    = list()
            
        try:
            orbit_start_datetime = datetime.strptime(Orbit_CDF.variables['time'].UNITS[14:], '%d %b %Y %H:%M:%S.%f')
        except:
            orbit_start_datetime = datetime.strptime("Seconds Since 1 Jan 2015 00:00:00.000"[14:], '%d %b %Y %H:%M:%S.%f')
            print("!!! ERROR while reading units of time inside NetCDF file. Assumed default value: 'Seconds Since 1 Jan 2015 00:00:00.000'")
        orbit_start_timestamp = calendar.timegm(orbit_start_datetime.utctimetuple())
        orbit_timestamp_step = ORBIT_Times[1] - ORBIT_Times[0]
        print( "orbit_timestamp_step =", orbit_timestamp_step )
        num_of_positions =  len(ORBIT_Times)
        # read the satellite positions and try to fill the bins
        for idx in range(0, num_of_positions): # for each satellite position
            if idx % 200000 == 0: print ("Checking sat position No", idx, "of", num_of_positions)
            in_Altitude_range = in_MagLat_range = in_MLT_range = in_Lat_range = in_Kp_range = False
                      
            # check if this position lies inside some bin
            current_Altitude = ORBIT_Altitudes[ idx ]
            if current_Altitude >= Altitude_min and current_Altitude <= Altitude_max: in_Altitude_range = True
            #
            if in_Altitude_range:
                current_MagLat = ORBIT_MagLats[ idx ]
                if current_MagLat >= MagLat_min and current_MagLat <= MagLat_max: in_MagLat_range = True
            #
            if in_MagLat_range:
                current_MLT = ORBIT_MLTs[ idx ]
                in_MLT_range = is_MLT_inside_range( current_MLT, MLT_min, MLT_max )
                
            # 
            if in_MLT_range: 
                current_Lat = ORBIT_Lats[ idx ]
                if current_Lat >= Lat_min and current_Lat <= Lat_max: in_Lat_range = True
                    
            if in_Lat_range==False:
                current_MagLat = ORBIT_MagLats[ idx ]
                current_MLT = ORBIT_MLTs[ idx ]
                current_Lat = ORBIT_Lats[ idx ]
                #if idx % 200000 == 0: print( "ALT:",current_Altitude, "MAGLAT:", current_MagLat, "MLT:", current_MLT, "LAT:",current_Lat )

            # The position is probably inside a bin (only kp remains to be checked). 
            # Open the corresponding TIEGCM file to read the kp and if position is in bin then calculate JH
            if in_Lat_range:
                current_timestamp = orbit_start_timestamp + current_timestamp_offset
                current_datetime  = datetime.utcfromtimestamp( current_timestamp )
                
                # Locate the corresponding TIEGCM file and timestep inside the file
                # one TIEGCM file contains 60 timesteps, 1 per 120min. The file's duration is 5 days. Each year consists of 74 files (the last file is smaller)
                start_of_current_year_datetime  = datetime.strptime("01 Jan " + str(current_datetime.year) + " 00:00:00", '%d %b %Y %H:%M:%S')
                start_of_current_year_timestamp = calendar.timegm(start_of_current_year_datetime.utctimetuple())
                newfilenumber = int(  ( (current_timestamp - start_of_current_year_timestamp)/(60*120) ) / 60  ) 
                tmp = (current_timestamp - start_of_current_year_timestamp)/(60*120) - newfilenumber*60 
                timestep_number = int( tmp )
                if tmp - float(timestep_number) > 0.5: timestep_number += 1 # select the nearest neighbor
                if  ( current_timestamp==start_of_current_year_timestamp  or  (current_timestamp - start_of_current_year_timestamp)/(60*120) ) % 60  !=  0: newfilenumber += 1 # file numbers start from 1
                if current_datetime.year == 2016: newfilenumber += 74
                if current_datetime.year == 2017: newfilenumber += 148
                
                # open the TIEGCM file if necessary
                if currentfilenumber < 0   or   currentfilenumber != newfilenumber:
                    if currentfilenumber >= 0: 
                        try:
                            tiegcm_CDF.close()
                        except:
                            print("Error closing tiegcm file no", currentfilenumber )
                    TIEGCMfilename = TIEGCM_filesPath + str(current_datetime.year) + "/" + TIEGCMfilenamePrefix + "{:03.0f}".format(newfilenumber) + TIEGCMfilenamePostfix + ".nc"
                    currentfilenumber = newfilenumber
                    print(  "Opening TIEGCMfile:", TIEGCMfilename)
                    try:
                        tiegcm_CDF = Dataset( TIEGCMfilename, 'r' )
                    except Exception as ex:
                        print ( "FILE NOT FOUND OR WRONG FORMAT:", TIEGCMfilename )
                        continue
                        
                # read Kp from the tiegcm file
                try:
                    current_Kp = tiegcm_CDF.variables['Kp'][timestep_number]
                except:
                    #print("%%%%%%%%%%%%%%%%%%%%%")
                    #print(len(tiegcm_CDF.variables['Kp']), timestep_number)
                    #print( current_datetime, current_timestamp, start_of_current_year_timestamp )
                    #print(TIEGCMfilename)
                    #print("%%%%%%%%%%%%%%%%%%%%%")
                    try:
                        current_Kp = tiegcm_CDF.variables['Kp'][timestep_number-1]
                    except:
                        #print( "!! Timestep Error",  timestep_number) # "of", len(tiegcm_CDF.variables['Kp']) )
                        continue
                    
                if current_Kp >= Kp_min and current_Kp <= Kp_max:
                    in_Kp_range = True 
                # if the satellite position matches a bin then mark it as a hit and remember the JH values 
                if in_MagLat_range and in_MLT_range and in_Altitude_range and in_Kp_range:
                    matchedBin = GetMatchedBin( current_MLT, current_MagLat, current_Altitude, current_Kp, current_Lat )
                    if matchedBin is not None:
                        # for this position locate the neighbor latitudes at the TIEGCM file. 
                        #lat1_idx, lat2_idx, lat1_val, lat2_val = findNeighborValues( TIEGCM_Lats, current_GeogLat )
                        # for this position locate the neighbor longitudes at the TIEGCM file.
                        #lon1_idx, lon2_idx, lon1_val, lon2_val = findNeighborValues( TIEGCM_Lons, current_Lon )
                        # for this position locate the neighbor Altitudes at the TIEGCM file. 
                        #lev1_idx, lev2_idx, lev1_val, lev2_val = findNeighborValues( CDFroot.variables['ZGMID'][time_idx, :, lat_idx, lon_idx], current_Altitude )
                        current_JH = ORBIT_Ohmic[ idx ]
                        # save 
                        matchedBin.JH_values.append( current_JH )
                        matchedBin.MagLat_values.append( current_MagLat )
                        matchedBin.MLT_values.append( current_MLT )
                        matchedBin.Altitude_values.append( current_Altitude )
                        matchedBin.Lat_values.append( current_Lat )
                        matchedBin.Kp_values.append( current_Kp )
                        matchedBin.Time_values.append( current_timestamp )
                        matchedBin.EEX_values.append( ORBIT_EEX[ idx ] ) 
                        matchedBin.EEY_values.append( ORBIT_EEY[ idx ] ) 
                        matchedBin.Pedersen_values.append( ORBIT_Pedersen[ idx ] ) 
                        matchedBin.Density_values.append( ORBIT_Density[ idx ] ) 
                        if len(ORBIT_Lev) > 0: matchedBin.Lev_values.append( ORBIT_Lev[ idx ] )
                        matchedBin.ConvectionHeating_values.append( ORBIT_ConvH[ idx ] )
                        matchedBin.WindHeating_values.append( ORBIT_WindH[ idx ] )
                        if len(ORBIT_Hall) > 0: 
                            matchedBin.Hall_values.append( ORBIT_Hall[ idx ] ) 
                        all_JH_values.append( current_JH )
                        all_MagLat_values.append( current_MagLat )
                        all_MLT_values.append( current_MLT )
                        all_Altitude_values.append( current_Altitude )
                        all_Lat_values.append( current_Lat )
                        all_Kp_values.append( current_Kp )
                        all_Time_values.append( current_timestamp )
                        all_HittedBin_IDs.append( matchedBin.ID )
                        all_EEX_values.append( ORBIT_EEX[ idx ] )
                        all_EEY_values.append( ORBIT_EEY[ idx ] )
                        all_Pedersen_values.append( ORBIT_Pedersen[ idx ] )
                        all_Density_values.append( ORBIT_Density[ idx ] )
                        if len(ORBIT_Lev) > 0: all_Lev_values.append( ORBIT_Lev[ idx ] )
                        all_ConvectionHeating_values.append( ORBIT_ConvH[ idx ] )
                        all_WindHeating_values.append( ORBIT_WindH[ idx ] )
                        if len(ORBIT_Hall) > 0: all_Hall_values.append( ORBIT_Hall[ idx ] )
                        Matches += 1
                    else:
                        pass
                        #print( "PARADOX at:", current_MLT, current_MagLat, current_Altitude, current_Kp, " :: ", time_idx, lev_idx, lat_idx, lon_idx )
            current_timestamp_offset += orbit_timestamp_step
    # save and clean up
    CalculateStatsOnData()
    SaveResults_CDF( ResultsFilename, "" ) 
    print( Matches, "satellite positions where matched inside bins." )
    try:
        CDFroot.close()
    except:
        print (".")

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
DiskAccessLock = threading.Lock()   
class Thread_ValueAssigner (threading.Thread):
    """
    This thread executes the actual calculation using a single source file (DataFilename) and producing one result file (ResultsFilename): 
        - reads the netcdf orbit or tiegcm file
        - checks every space-time position
        - assign the position's data to the corresponding Bin 
        - saves the above data into a netcdf results-file
    Threads are employed in order to speed up the calculation when there are many source files. 
    There will be one thread for each source file
    """
    def __init__(self, DataFilename, ResultsFilename):
        threading.Thread.__init__(self)
        self.DataFilename = DataFilename
        self.ResultsFilename = ResultsFilename
    def run(self):
        global Bins
        global all_JH_values
        DataFilename = self.DataFilename
        ResultsFilename = self.ResultsFilename
        print( "Thread start",  datetime.now().strftime("%d-%m-%Y %H:%M:%S"), ResultsFilename, "\n" )
        MagLat_min =  1000
        MagLat_max = -1000
        MLT_min    =  1000
        MLT_max    = -1000
        Altitude_min    =  1000
        Altitude_max    = -1000
        Lat_min     =  1000
        Lat_max     = -1000    
        Kp_min     =  1000
        Kp_max     = -1000
        localBins = copy.deepcopy(Bins)
        for B in localBins:
            B.reset()
            if B.MagLat_min < MagLat_min: MagLat_min = B.MagLat_min 
            if B.MagLat_max > MagLat_max: MagLat_max = B.MagLat_max
            if B.MLT_min < MLT_min: MLT_min = B.MLT_min 
            if B.MLT_max > MLT_max: MLT_max = B.MLT_max
            if B.Altitude_min < Altitude_min: Altitude_min = B.Altitude_min 
            if B.Altitude_max > Altitude_max: Altitude_max = B.Altitude_max
            if B.Lat_min < Lat_min: Lat_min = B.Lat_min 
            if B.Lat_max > Lat_max: Lat_max = B.Lat_max                        
            if B.Kp_min < Kp_min: Kp_min = B.Kp_min 
            if B.Kp_max > Kp_max: Kp_max = B.Kp_max            
        all_JH_values.clear()
        all_MagLat_values.clear()
        all_MLT_values.clear()
        all_Altitude_values.clear()
        all_Lat_values.clear()
        all_Kp_values.clear()
        all_Time_values.clear()
        all_HittedBin_IDs.clear()
        all_EEX_values.clear()
        all_EEY_values.clear()
        all_Pedersen_values.clear()
        all_Density_values.clear()
        all_Lev_values.clear()
        all_Hall_values.clear()
        all_ConvectionHeating_values.clear()
        all_WindHeating_values.clear()
        Matches = 0
        
        # parse TIEGCM file
        try:
            CDFroot = Dataset( DataFilename, 'r' )
            print( "Reading", DataFilename )
        except:
            print ( "WRONG FORMAT:", DataFilename )
            return
        try:
            FileStartTimeStamp = calendar.timegm( datetime.strptime( CDFroot.variables['time'].units[14:],  "%Y-%m-%d %H:%M:%S" ).utctimetuple() ) # ex: "minutes since 2015-1-1 0:0:0"
        except:
            print ( "WRONG CONTENTS:", DataFilename )
            return
        length_time = CDFroot.variables['Ohmic'].shape[0]
        length_lev  = CDFroot.variables['Ohmic'].shape[1]
        length_lat  = CDFroot.variables['Ohmic'].shape[2]
        length_lon  = CDFroot.variables['Ohmic'].shape[3]
        # wait until disk is released
        DiskAccessLock.acquire()
        # Load or calculate all basic values from the netcdf file
        try:
            TIMEs   = CDFroot.variables['time'][:] # minutes since the start time
            LATs    = CDFroot.variables['lat'][:] 
            ALTs    = CDFroot.variables['ZGMID'][:, :, :, :] / 100000 # it is stored in cm inside the file
            JHs     = CDFroot.variables['Ohmic'][:, :, :, :]
            KPs     = CDFroot.variables['Kp'][:]
            MAGLATs = CDFroot.variables['mlat_qdf'][:, :, :, :] 
            MLTs    = CDFroot.variables['mlt_qdf'][:, :, :, :] 
            EEXs    = CDFroot.variables['EEX'][:, :, :, :] 
            EEYs    = CDFroot.variables['EEY'][:, :, :, :] 
            PEDs    = CDFroot.variables['SIGMA_PED'][:, :, :, :] 
            HALs    = CDFroot.variables['SIGMA_HAL'][:, :, :, :]
            DENs    = CDFroot.variables['DEN'][:, :, :, :] 
            LEVs    = CDFroot.variables['lev'][:] 
            try:
                CONV_H  = CDFroot.variables['Convection_heating'][:, :, :, :]
            except:
                CONV_H  = CDFroot.variables['Convenction_heating'][:, :, :, :]
            WIND_H  = CDFroot.variables['Wind_heating'][:, :, :, :]
        except Exception as e:
            print( "Thread aborted while reading",  datetime.now().strftime("%d-%m-%Y %H:%M:%S"), ResultsFilename[-26:], ":", e, repr(e), "\n" )
            DiskAccessLock.release()
            return 
        DiskAccessLock.release()
        print( "Thread file read done",  datetime.now().strftime("%d-%m-%Y %H:%M:%S"), ResultsFilename[-26:], "\n" )
    
        step = 1
        for idx_lat in range(0, length_lat, step):
            if idx_lat%2==0: print("Thread Calculating Lat",  idx_lat, ResultsFilename[-26:])
            current_Lat = LATs[idx_lat] 
            if current_Lat < Lat_min  or  current_Lat > Lat_max: continue
            for idx_lon in range(0, length_lon, step):
                for idx_lev in range(0, length_lev, step):
                    for idx_time in range(0, length_time, step):                    
                        in_Altitude_range = in_MagLat_range = in_MLT_range = in_Kp_range = False
                            
                        current_Altitude = ALTs[idx_time, idx_lev, idx_lat, idx_lon]
                        if current_Altitude >= Altitude_min and current_Altitude <= Altitude_max:
                            in_Altitude_range = True
                        
                        if in_Altitude_range:
                            current_MagLat = MAGLATs[ idx_time, idx_lev, idx_lat, idx_lon ]
                            if current_MagLat >= MagLat_min and current_MagLat <= MagLat_max:
                                in_MagLat_range = True
                                
                        if in_MagLat_range:
                            current_MLT = MLTs[ idx_time, idx_lev, idx_lat, idx_lon ]
                            if in_MagLat_range:
                                in_MLT_range = is_MLT_inside_range( current_MLT, MLT_min, MLT_max )
                        
                        if in_MLT_range:
                            current_Kp = KPs[idx_time]
                            if current_Kp >= Kp_min and current_Kp <= Kp_max:
                                in_Kp_range = True   
                                
                        if in_Kp_range:                    
                            matchedBin = GetMatchedBin( current_MLT, current_MagLat, current_Altitude, current_Kp, current_Lat )
                            if matchedBin is not None:
                                for B in localBins:
                                    if B.ID == matchedBin.ID:
                                        matchedBin = B
                                current_time = int( FileStartTimeStamp + TIMEs[idx_time]*120*60 )
                                current_JH = JHs[idx_time, idx_lev, idx_lat ,idx_lon] #CDFroot.variables['Joule Heating'][idx_time, idx_lev, idx_lat, idx_lon]
                                matchedBin.JH_values.append( current_JH )
                                matchedBin.MagLat_values.append( current_MagLat )
                                matchedBin.MLT_values.append( current_MLT )
                                matchedBin.Altitude_values.append( current_Altitude )
                                matchedBin.Kp_values.append( current_Kp )
                                matchedBin.Time_values.append( current_time )
                                matchedBin.EEX_values.append( EEXs[ idx_time, idx_lev, idx_lat, idx_lon ] ) 
                                matchedBin.EEY_values.append( EEYs[ idx_time, idx_lev, idx_lat, idx_lon ] ) 
                                matchedBin.Pedersen_values.append( PEDs[ idx_time, idx_lev, idx_lat, idx_lon ] ) 
                                matchedBin.Hall_values.append( HALs[ idx_time, idx_lev, idx_lat, idx_lon ] ) 
                                matchedBin.Density_values.append( DENs[ idx_time, idx_lev, idx_lat, idx_lon ] ) 
                                matchedBin.Lev_values.append( LEVs[ idx_lev ] ) 
                                matchedBin.ConvectionHeating_values.append( CONV_H[ idx_time, idx_lev, idx_lat, idx_lon ] ) 
                                matchedBin.WindHeating_values.append( WIND_H[ idx_time, idx_lev, idx_lat, idx_lon ] ) 
                                all_JH_values.append( current_JH )
                                all_MagLat_values.append( current_MagLat )
                                all_MLT_values.append( current_MLT )
                                all_Altitude_values.append( current_Altitude )
                                all_Kp_values.append( current_Kp )
                                all_Time_values.append( current_time )
                                all_HittedBin_IDs.append( matchedBin.ID )
                                all_EEX_values.append( EEXs[ idx_time, idx_lev, idx_lat, idx_lon ] )
                                all_EEY_values.append( EEYs[ idx_time, idx_lev, idx_lat, idx_lon ] )
                                all_Pedersen_values.append( PEDs[ idx_time, idx_lev, idx_lat, idx_lon ] )
                                all_Hall_values.append( HALs[ idx_time, idx_lev, idx_lat, idx_lon ] )
                                all_Density_values.append( DENs[ idx_time, idx_lev, idx_lat, idx_lon ] )
                                all_Lev_values.append( LEVs[ idx_lev ] )
                                all_ConvectionHeating_values.append( CONV_H[ idx_time, idx_lev, idx_lat, idx_lon ] ) 
                                all_WindHeating_values.append( WIND_H[ idx_time, idx_lev, idx_lat, idx_lon ] )
                                Matches += 1
                    #break
                #break
        CDFroot.close()
        # wait until disk is released
        #DiskAccessLock.acquire()
        #### SAVE Results ####
        try:
            # save general info
            resultsCDF = Dataset( ResultsFilename, 'a' )
            resultsCDF.DateOfUpdate = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            resultsCDF.Region = CALCULATIONS_RegionName
            resultsCDF.DataPath = CALCULATIONS_TIEGCMfolder
            # save data for each bin seperately 
            for B in localBins:
                # save data about the hits inside the bin
                if len(B.Time_values) > 0:
                    resultsCDF.variables[B.ID+"_TimeValues"][:]      = B.Time_values
                    resultsCDF.variables[B.ID+"_JHValues"][:]        = B.JH_values        
                    resultsCDF.variables[B.ID+"_MagLatValues"][:]    = B.MagLat_values
                    resultsCDF.variables[B.ID+"_MLTValues"][:]       = B.MLT_values
                    resultsCDF.variables[B.ID+"_AltitudeValues"][:]  = B.Altitude_values
                    resultsCDF.variables[B.ID+"_LatValues"][:]       = B.Lat_values
                    resultsCDF.variables[B.ID+"_KpValues"][:]        = B.Kp_values
                    resultsCDF.variables[B.ID+"_EEXValues"][:]       = B.EEX_values        
                    resultsCDF.variables[B.ID+"_EEYValues"][:]       = B.EEY_values
                    resultsCDF.variables[B.ID+"_PedersenValues"][:]  = B.Pedersen_values
                    resultsCDF.variables[B.ID+"_HallValues"][:]      = B.Hall_values
                    resultsCDF.variables[B.ID+"_DensityValues"][:]   = B.Density_values
                    resultsCDF.variables[B.ID+"_LevValues"][:]       = B.Lev_values
                    resultsCDF.variables[B.ID+"_ConvectionHeatingValues"][:] = B.ConvectionHeating_values
                    resultsCDF.variables[B.ID+"_WindHeatingValues"][:] = B.WindHeating_values
            ## save data for all hits
            resultsCDF.variables["allTimeValues"][:]     = all_Time_values
            resultsCDF.variables["allJHValues"][:]       = all_JH_values    
            resultsCDF.variables["allMagLatValues"][:]   = all_MagLat_values
            resultsCDF.variables["allMLTValues"][:]      = all_MLT_values
            resultsCDF.variables["allAltitudeValues"][:] = all_Altitude_values
            resultsCDF.variables["allLatValues"][:]      = all_Lat_values
            resultsCDF.variables["allKpValues"][:]       = all_Kp_values
            #resultsCDF.variables["allHittedBinIDs"][:]   = netCDF4.stringtochar(np.array(all_HittedBin_IDs[:], 'S8'))
            resultsCDF.variables["allEEXValues"][:]      = all_EEX_values
            resultsCDF.variables["allEEYValues"][:]      = all_EEY_values
            resultsCDF.variables["allPedersenValues"][:] = all_Pedersen_values
            resultsCDF.variables["allHallValues"][:]     = all_Hall_values
            resultsCDF.variables["allDensityValues"][:]  = all_Density_values
            resultsCDF.variables["allLevValues"][:]      = all_Lev_values
            resultsCDF.variables["allConvectionHeatingValues"][:] = all_ConvectionHeating_values
            resultsCDF.variables["allWindHeatingValues"][:] = all_WindHeating_values
            #
            resultsCDF.close()    
        except Exception as e:
            print( "!!!! Thread error while writing",  datetime.now().strftime("%d-%m-%Y %H:%M:%S"), ResultsFilename[-26:], "\n" )
            print( e )
            #DiskAccessLock.release()
        #DiskAccessLock.release()
    
        print( "Thread finish",  datetime.now().strftime("%d-%m-%Y %H:%M:%S"), ResultsFilename[-26:], "\n", Matches, "matches", len(localBins[0].JH_values), len(Bins[0].JH_values) )
        print( "" )

        
        

        
        
def CalculateStatsOnData():
    """
    This function uses the values assigned into the Bins to calculate mean, variance, deviation and stores them into the Bin class.
    """
    global Bins
    for B in Bins:
        if len(B.JH_values) > 0:
            # calculate the mean value
            for aJHvalue in B.JH_values:
                if B.JH_min > aJHvalue: B.JH_min = aJHvalue
                if B.JH_max < aJHvalue: B.JH_max = aJHvalue
                B.JH_mean += aJHvalue
            B.JH_mean = B.JH_mean / len(B.JH_values)
            
            # calculate the median value
            B.JH_median = np.percentile(B.JH_values, 50)
            
            # for Variance (around mean):
            for aJHvalue in B.JH_values:
                B.JH_variance += abs(aJHvalue - B.JH_mean)**2
            B.JH_variance = B.JH_variance / len(B.JH_values)
            
            # for Median Variance (around median):
            for aJHvalue in B.JH_values:
                B.JH_medianVariance += abs(aJHvalue - B.JH_median)**2
            B.JH_medianVariance = B.JH_medianVariance / len(B.JH_values)
            
            # for Median absolute deviation
            AbsoluteDeviations = B.JH_values.copy()
            for i in range(0, len(AbsoluteDeviations)):
                AbsoluteDeviations[i] = abs(B.JH_median - AbsoluteDeviations[i])
            B.JH_medianAbsDev = np.percentile(AbsoluteDeviations, 50)
        
        
        
        
def AssignValuesPerBin_MultipleResultFiles( TIEGCMfilesPath, ResultFilesPath ):
    """
    This function initiates the calculation. 
    It creates a Thread_ValueAssigner for each source file which resides in TIEGCMfilesPath
    It also tells the thread to store the result file into ResultFilesPath
    """
    startSecs = time.time()

    if path.exists( ResultFilesPath ) == False:
        os.mkdir( ResultFilesPath )
    
    AllThreads = list()
    AllDataFiles = sorted( glob.glob( TIEGCMfilesPath + "/*/*.nc", recursive=True ) )
    for currentDataFile in AllDataFiles:
        if '\\' in currentDataFile: #windows
            prefix = currentDataFile[ currentDataFile.rfind('\\')+1 : -3 ]
        else: # linux
            prefix = currentDataFile[ currentDataFile.rfind('/')+1 : -3 ]
        ResultsFilename = ResultFilesPath + currentDataFile[ currentDataFile.rfind('\\')+1 : -3 ] + ".stats.nc"
        if path.exists( ResultsFilename ): 
            print("Skipping because exists:", ResultsFilename)
            continue
        else:
            # wait if there are plenty alive threads
            alive_counter = 0
            for aThread in AllThreads:
                if aThread.is_alive():
                    alive_counter += 1
            while alive_counter >= 5:
                time.sleep(random.randint(10, 15))
                alive_counter = 0
                for aThread in AllThreads:
                    if aThread.is_alive():
                        alive_counter += 1
            # spawn new thread
            CreateResults_CDF( ResultsFilename )
            T = Thread_ValueAssigner(currentDataFile, ResultsFilename)
            AllThreads.append(T)
            T.start()
            time.sleep(2)

    # wait for all threads to terminate
    for T in AllThreads: T.join()
    # finish it
    finishSecs = time.time()
    print( finishSecs-startSecs, " sec")    
    
    





    
    
    
    
    
    
    
    
    
