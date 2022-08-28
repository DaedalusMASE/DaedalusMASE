'''
This module contains the data holders necessary to calculate coverage and the Coverage-Calculation function.
The main data element is the "Bin". A Bin is defined by ranges of Magnetic Local Time, Magnetic Latitude, Altitude and Kp.
Every position of the satellite that falls inside these ranges is assigned to the respective Bin.
Thus the coverage for this Bin can be calculated.
'''

# imports used by the coverage calculation
import csv
import time
from os import path
from utils import *

Orbit_Files_Path = "../../Sample_Data/orbital_data/"  # holds the csv files which describe the orbit. Columns: Time Latitude Longitude MagneticLatitude MagneticLongitude MagneticLocalTime
CoverageResults_Files_Path = "../ResultFiles/"  # holds the files
GeomagneticIndices_Files_Path = "../../Sample_Data/geomagnetic_indices/"  # holds the files with the Kp index of the sun for several years. 


def set_orbit_files_path( path ):
    """
        Sets the path where the csv files describing the satellite orbit are located.
        The csv file must contain the following columns:
        Epoch(UTCG),Lat_GEOD(deg),Lon_GEOD(deg),Height_WGS84 (km),Magnetic Latitude,Magnetic Longitude,MLT

        Args:
            path (string): a path to the files
    """
    Orbit_Files_Path = path
    
def set_coverage_results_files_path( path ):
    """
        Sets the path where the results of the coverage calculation are stored.
        The results are plain text files which describe the coverage results for each bin.

        Args:
            path (string): a path to the files
    """
    CoverageResults_Files_Path = path
    
def set_geomagnetic_indices_files_path( path ):
    """
        Sets the path where the files holding the Kp indexes are located. There must be òne file for each year of interest.
        The Kp-index is a value from 0 to 9 which characterizes the magnitude of geomagnetic storms. 
        Explanation of Kp files: https://www.ngdc.noaa.gov/stp/GEOMAG/kp_ap.html   
        Download location of Kp files: ftp://ftp.ngdc.noaa.gov/STP/GEOMAGNETIC_DATA/INDICES/KP_AP  

        Args:
            path (string): a path to the files
    """
    GeomagneticIndices_Files_Path = path
    

# Holds the Geomagnetic kp Indices. 
# Accessing examples: GeomagneticIndices[("23", "05", "2011", "0")] stores the kp index for 23-05-2001 00:00-03:00
#                     GeomagneticIndices[("23", "05", "2011", "3")] stores the kp index for 23-05-2001 09:00-12:00
# Explanation: https://www.ngdc.noaa.gov/stp/GEOMAG/kp_ap.html   
# Download location: ftp://ftp.ngdc.noaa.gov/STP/GEOMAGNETIC_DATA/INDICES/KP_AP  
GeomagneticIndices = dict()


'''
Define a class which to describe a bin
'''
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
    NumOfBins      = 0 # How many parts will the Altitude range be splitted in
    CumulativeTime = 0 # (sec)
    DesirableCumulativeTime = 0 # (sec)
    
    def __init__(self, ID, Description, MLT_min, MLT_max, MagLat_min, MagLat_max, Altitude_min, Altitude_max, Kp_min, Kp_max, DesirableCumulativeTime):
        self.ID             = ID
        self.Description    = Description
        self.MLT_min        = MLT_min 
        self.MLT_max        = MLT_max
        self.MagLat_min     = MagLat_min
        self.MagLat_max     = MagLat_max
        self.Altitude_min   = Altitude_min
        self.Altitude_max   = Altitude_max
        self.Kp_min         = Kp_min
        self.Kp_max         = Kp_max
        self.DesirableCumulativeTime = DesirableCumulativeTime
        
    def getInfo(self):
        s  = self.ID.ljust(8, ' ') + ": "
        s += "{:02.0f}".format(self.MLT_min)      + "<MLT<="    + "{:02.0f}".format(self.MLT_max)      + " "
        s += "{:03.0f}".format(self.MagLat_min)   + "<MagLat<=" + "{:03.0f}".format(self.MagLat_max)   + " "
        s += "{:03.0f}".format(self.Altitude_min) + "<Alt<="    + "{:03.0f}".format(self.Altitude_max) + " "
        s += str(self.Kp_min)             + "<Kp<="     + str(self.Kp_max)       + " "
        s += "Coverage=" 
        s += ConvertLeadingZerosToSpaces( "{:09.3f}".format(self.CumulativeTime/60) ) + "/" 
        s += ConvertLeadingZerosToSpaces( "{:06.2f}".format(self.DesirableCumulativeTime/60) ) + "min "
        s += ConvertLeadingZerosToSpaces( "{:08.0f}".format(self.CumulativeTime) ) + "/" 
        s += ConvertLeadingZerosToSpaces( "{:05.0f}".format(self.DesirableCumulativeTime) ) + "sec"
        return s
    
    def printMe(self):
        print( self.getInfo() )

# this list holds the definitions of all bins
Bins = list()
#                ID        Description                          MLT      MagLat    Altitude                Kp       DesirableTime(sec)
Bins.append( Bin("AEM_L1", "Auroral E region, midnight sector", 22, 2,   60, 75,   115, 120,               0, 2,   50*60 ) )
Bins.append( Bin("AEM_L2", "Auroral E region, midnight sector", 22, 2,   60, 75,   120, 125,               0, 2,   50*60 ) )
Bins.append( Bin("AEM_L3", "Auroral E region, midnight sector", 22, 2,   60, 75,   125, 130,               0, 2,   50*60 ) )
Bins.append( Bin("AEM_L4", "Auroral E region, midnight sector", 22, 2,   60, 75,   130, 135,               0, 2,   50*60 ) )
Bins.append( Bin("AEM_L5", "Auroral E region, midnight sector", 22, 2,   60, 75,   135, 140,               0, 2,   50*60 ) )
Bins.append( Bin("AEM_L6", "Auroral E region, midnight sector", 22, 2,   60, 75,   140, 145,               0, 2,   50*60 ) )
Bins.append( Bin("AEM_L7", "Auroral E region, midnight sector", 22, 2,   60, 75,   145, 150,               0, 2,   50*60 ) )
Bins.append( Bin("AEM_M1", "Auroral E region, midnight sector", 21, 3,   60, 75,   115, 122,               2, 4,   30*60 ) )
Bins.append( Bin("AEM_M2", "Auroral E region, midnight sector", 21, 3,   60, 75,   122, 129,               2, 4,   30*60 ) )
Bins.append( Bin("AEM_M3", "Auroral E region, midnight sector", 21, 3,   60, 75,   129, 136,               2, 4,   30*60 ) )
Bins.append( Bin("AEM_M4", "Auroral E region, midnight sector", 21, 3,   60, 75,   136, 143,               2, 4,   30*60 ) )
Bins.append( Bin("AEM_M5", "Auroral E region, midnight sector", 21, 3,   60, 75,   143, 150,               2, 4,   30*60 ) )    
Bins.append( Bin("AEM_H1", "Auroral E region, midnight sector", 22, 2,   60, 75,   115, 150,               4, 9,   20*60 ) )

Bins.append( Bin("AFM_L1", "Auroral F region, midnight sector", 21, 3,   60, 75,   150, 185,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_L2", "Auroral F region, midnight sector", 21, 3,   60, 75,   185, 220,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_L3", "Auroral F region, midnight sector", 21, 3,   60, 75,   220, 255,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_L4", "Auroral F region, midnight sector", 21, 3,   60, 75,   255, 290,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_L5", "Auroral F region, midnight sector", 21, 3,   60, 75,   290, 325,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_L6", "Auroral F region, midnight sector", 21, 3,   60, 75,   325, 360,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_L7", "Auroral F region, midnight sector", 21, 3,   60, 75,   360, 395,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_L8", "Auroral F region, midnight sector", 21, 3,   60, 75,   395, 430,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_L9", "Auroral F region, midnight sector", 21, 3,   60, 75,   430, 465,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_L10","Auroral F region, midnight sector", 21, 3,   60, 75,   465, 500,               0, 2,   50*60 ) )
Bins.append( Bin("AFM_M1", "Auroral F region, midnight sector", 21, 3,   60, 75,   150.0, 237.5,           2, 4,   30*60 ) )
Bins.append( Bin("AFM_M2", "Auroral F region, midnight sector", 21, 3,   60, 75,   237.5, 325.0,           2, 4,   30*60 ) )
Bins.append( Bin("AFM_M3", "Auroral F region, midnight sector", 21, 3,   60, 75,   325.0, 412.5,           2, 4,   30*60 ) )
Bins.append( Bin("AFM_M4", "Auroral F region, midnight sector", 21, 3,   60, 75,   412.5, 500.0,           2, 4,   30*60 ) )
Bins.append( Bin("AFM_H1", "Auroral F region, midnight sector", 21, 3,   60, 75,   150, 265,               4, 9,   20*60 ) )
Bins.append( Bin("AFM_H2", "Auroral F region, midnight sector", 21, 3,   60, 75,   265, 380,               4, 9,   20*60 ) )
Bins.append( Bin("AFM_H3", "Auroral F region, midnight sector", 21, 3,   60, 75,   380, 500,               4, 9,   20*60 ) )

Bins.append( Bin("AEE_L1", "Auroral E region, evening sector",  15, 21,  60, 75,   115, 120,               0, 2,   50*60 ) )
Bins.append( Bin("AEE_L2", "Auroral E region, evening sector",  15, 21,  60, 75,   120, 125,               0, 2,   50*60 ) )
Bins.append( Bin("AEE_L3", "Auroral E region, evening sector",  15, 21,  60, 75,   125, 130,               0, 2,   50*60 ) )
Bins.append( Bin("AEE_L4", "Auroral E region, evening sector",  15, 21,  60, 75,   130, 135,               0, 2,   50*60 ) )
Bins.append( Bin("AEE_L5", "Auroral E region, evening sector",  15, 21,  60, 75,   135, 140,               0, 2,   50*60 ) )
Bins.append( Bin("AEE_L6", "Auroral E region, evening sector",  15, 21,  60, 75,   140, 145,               0, 2,   50*60 ) )
Bins.append( Bin("AEE_L7", "Auroral E region, evening sector",  15, 21,  60, 75,   145, 150,               0, 2,   50*60 ) )
Bins.append( Bin("AEE_M1", "Auroral E region, evening sector",  15, 21,  60, 75,   115, 122,               2, 4,   30*60 ) )
Bins.append( Bin("AEE_M2", "Auroral E region, evening sector",  15, 21,  60, 75,   122, 129,               2, 4,   30*60 ) )
Bins.append( Bin("AEE_M3", "Auroral E region, evening sector",  15, 21,  60, 75,   129, 136,               2, 4,   30*60 ) )
Bins.append( Bin("AEE_M4", "Auroral E region, evening sector",  15, 21,  60, 75,   136, 143,               2, 4,   30*60 ) )
Bins.append( Bin("AEE_M5", "Auroral E region, evening sector",  15, 21,  60, 75,   143, 150,               2, 4,   30*60 ) )
Bins.append( Bin("AEE_H1", "Auroral E region, evening sector",  15, 21,  60, 75,   115, 150,               4, 9,   20*60 ) )

Bins.append( Bin("AED_L1", "Auroral E region, dawn sector",     3, 9,   60, 75,   115, 120,                 0, 2,   50*60 ) )
Bins.append( Bin("AED_L2", "Auroral E region, dawn sector",     3, 9,   60, 75,   120, 125,                 0, 2,   50*60 ) )
Bins.append( Bin("AED_L3", "Auroral E region, dawn sector",     3, 9,   60, 75,   125, 130,                 0, 2,   50*60 ) )
Bins.append( Bin("AED_L4", "Auroral E region, dawn sector",     3, 9,   60, 75,   130, 135,                 0, 2,   50*60 ) )
Bins.append( Bin("AED_L5", "Auroral E region, dawn sector",     3, 9,   60, 75,   135, 140,                 0, 2,   50*60 ) )
Bins.append( Bin("AED_L6", "Auroral E region, dawn sector",     3, 9,   60, 75,   140, 145,                 0, 2,   50*60 ) )
Bins.append( Bin("AED_L7", "Auroral E region, dawn sector",     3, 9,   60, 75,   145, 150,                 0, 2,   50*60 ) )
Bins.append( Bin("AED_M1", "Auroral E region, dawn sector",     3, 9,   60, 75,   115, 122,                 2, 4,   30*60 ) )
Bins.append( Bin("AED_M2", "Auroral E region, dawn sector",     3, 9,   60, 75,   122, 129,                 2, 4,   30*60 ) )
Bins.append( Bin("AED_M3", "Auroral E region, dawn sector",     3, 9,   60, 75,   129, 136,                 2, 4,   30*60 ) )
Bins.append( Bin("AED_M4", "Auroral E region, dawn sector",     3, 9,   60, 75,   136, 143,                 2, 4,   30*60 ) )
Bins.append( Bin("AED_M5", "Auroral E region, dawn sector",     3, 9,   60, 75,   143, 150,                 2, 4,   30*60 ) )
Bins.append( Bin("AED_H1", "Auroral E region, dawn sector",     3, 9,   60, 75,   115, 150,                 4, 9,   20*60 ) )

Bins.append( Bin("EEJ_A1", "Equatorial E-region",             10, 13,  -7,  7,   115,   127,               0, 9,   10*60 ) )
Bins.append( Bin("EEJ_A2", "Equatorial E-region",             10, 13,  -7,  7,   127,   139,               0, 9,   10*60 ) )
Bins.append( Bin("EEJ_A3", "Equatorial E-region",             10, 13,  -7,  7,   139,   150,               0, 9,   10*60 ) )

Bins.append( Bin("EPB_A1", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   150, 185,                  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A2", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   185, 220,                  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A3", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   220, 255,                  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A4", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   255, 290,                  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A5", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   290, 325,                  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A6", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   325, 360,                  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A7", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   360, 395,                  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A8", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   395, 430,                  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A9", "Equatorial Plasma Bubbles",       18,  4, -30, 30,   430, 465,                  0, 9,   150*60 ) )
Bins.append( Bin("EPB_A10","Equatorial Plasma Bubbles",       18,  4, -30, 30,   465, 500,                  0, 9,   150*60 ) )

Bins.append( Bin("SQ_A1",  "Sq & midlat F region currents",    6, 19, -60, 60,   150, 185,                  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A2",  "Sq & midlat F region currents",    6, 19, -60, 60,   185, 220,                  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A3",  "Sq & midlat F region currents",    6, 19, -60, 60,   220, 255,                  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A4",  "Sq & midlat F region currents",    6, 19, -60, 60,   255, 290,                  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A5",  "Sq & midlat F region currents",    6, 19, -60, 60,   290, 325,                  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A6",  "Sq & midlat F region currents",    6, 19, -60, 60,   325, 360,                  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A7",  "Sq & midlat F region currents",    6, 19, -60, 60,   360, 395,                  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A8",  "Sq & midlat F region currents",    6, 19, -60, 60,   395, 430,                  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A9",  "Sq & midlat F region currents",    6, 19, -60, 60,   430, 465,                  0, 3,   150*60 ) )
Bins.append( Bin("SQ_A10", "Sq & midlat F region currents",    6, 19, -60, 60,   465, 500,                  0, 3,   150*60 ) )

Bins.append( Bin("CF_L1", "Dayside Cusp F-region",            10, 14,   70,  80,   140, 185,                0, 2,   50*60 ) )
Bins.append( Bin("CF_L2", "Dayside Cusp F-region",            10, 14,   70,  80,   185, 230,                0, 2,   50*60 ) )
Bins.append( Bin("CF_L3", "Dayside Cusp F-region",            10, 14,   70,  80,   230, 275,                0, 2,   50*60 ) )
Bins.append( Bin("CF_L4", "Dayside Cusp F-region",            10, 14,   70,  80,   275, 320,                0, 2,   50*60 ) )
Bins.append( Bin("CF_L5", "Dayside Cusp F-region",            10, 14,   70,  80,   320, 365,                0, 2,   50*60 ) )
Bins.append( Bin("CF_L6", "Dayside Cusp F-region",            10, 14,   70,  80,   365, 410,                0, 2,   50*60 ) )
Bins.append( Bin("CF_L7", "Dayside Cusp F-region",            10, 14,   70,  80,   410, 455,                0, 2,   50*60 ) )
Bins.append( Bin("CF_L8", "Dayside Cusp F-region",            10, 14,   70,  80,   455, 500,                0, 2,   50*60 ) )
Bins.append( Bin("CF_M1", "Dayside Cusp F-region",            10, 14,   70,  80,   140, 230,               2, 4,   30*60 ) )
Bins.append( Bin("CF_M2", "Dayside Cusp F-region",            10, 14,   70,  80,   230, 320,               2, 4,   30*60 ) )
Bins.append( Bin("CF_M3", "Dayside Cusp F-region",            10, 14,   70,  80,   320, 410,               2, 4,   30*60 ) )
Bins.append( Bin("CF_M4", "Dayside Cusp F-region",            10, 14,   70,  80,   410, 500,               2, 4,   30*60 ) )
Bins.append( Bin("CF_H1", "Dayside Cusp F-region",            10, 14,   70,  80,   140, 260,               4, 9,   20*60 ) )
Bins.append( Bin("CF_H2", "Dayside Cusp F-region",            10, 14,   70,  80,   260, 380,               4, 9,   20*60 ) )
Bins.append( Bin("CF_H3", "Dayside Cusp F-region",            10, 14,   70,  80,   380, 500,               4, 9,   20*60 ) )

Bins.append( Bin("PCF_L1", "Polar cap F-region",              14, 10,   70,  90,   140, 185,               0, 2,   50*60 ) )
Bins.append( Bin("PCF_L2", "Polar cap F-region",              14, 10,   70,  90,   185, 230,               0, 2,   50*60 ) )
Bins.append( Bin("PCF_L3", "Polar cap F-region",              14, 10,   70,  90,   230, 275,               0, 2,   50*60 ) )
Bins.append( Bin("PCF_L4", "Polar cap F-region",              14, 10,   70,  90,   275, 320,               0, 2,   50*60 ) )
Bins.append( Bin("PCF_L5", "Polar cap F-region",              14, 10,   70,  90,   320, 365,               0, 2,   50*60 ) )
Bins.append( Bin("PCF_L6", "Polar cap F-region",              14, 10,   70,  90,   365, 410,               0, 2,   50*60 ) )
Bins.append( Bin("PCF_L7", "Polar cap F-region",              14, 10,   70,  90,   410, 455,               0, 2,   50*60 ) )
Bins.append( Bin("PCF_L8", "Polar cap F-region",              14, 10,   70,  90,   455, 500,               0, 2,   50*60 ) )
Bins.append( Bin("PCF_M1", "Polar cap F-region",              14, 10,   70,  90,   140, 230,               2, 4,   30*60 ) )
Bins.append( Bin("PCF_M2", "Polar cap F-region",              14, 10,   70,  90,   230, 320,               2, 4,   30*60 ) )
Bins.append( Bin("PCF_M3", "Polar cap F-region",              14, 10,   70,  90,   320, 410,               2, 4,   30*60 ) )
Bins.append( Bin("PCF_M4", "Polar cap F-region",              14, 10,   70,  90,   410, 500,               2, 4,   30*60 ) )
Bins.append( Bin("PCF_H1", "Polar cap F-region",              14, 10,   70,  90,   140, 260,               4, 9,   20*60 ) )
Bins.append( Bin("PCF_H2", "Polar cap F-region",              14, 10,   70,  90,   260, 380,               4, 9,   20*60 ) )
Bins.append( Bin("PCF_H3", "Polar cap F-region",              14, 10,   70,  90,   380, 500,               4, 9,   20*60 ) )

def clear_bins():
    """
        Removes all Bins.
    """
    Bins.clear()     

def create_new_bin( ID, Description, MagneticLocalTime_from, MagneticLocalTime_to, MagneticLatitude_from, MagneticLatitude_to, Altitude_from, Altitude_to, Kp_from, Kp_to, DesirableTime ):
    """
        Defines a new Bin according to the specified ranges.
        All satellite positions which fall in these ranges will be assigned to this Bin. 
        The plots will be created according to all the defined Bins.
        The library initializes certain predefined Bins. Call ClearBins() in order to remove them.
        Args:
            ID (string): a code name for this Bin. It will be displayed on the plots. Naming example: AEM_L1, AEM_L2 etc for the general region AEM and sub-regions L1 L2 etc.
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
    
    
def GetMatchedBin( MLT, MagLat, Altitude, Kp ):
    """
        Finds and returns the Bin object which matches the position of the satellite described by the arguments.
        
        Args:
                MLT: the Magnetic Local Time
                MagLat: The Magnetic Latitude
                Altitude: The Altitude
                Kp: the Kp-index
        Returns:
                Bin: the Bin in which the position represented by the arguments is matched.
    """
    
    MatchedBin = None
    for B in Bins:
        Kp_min_to_check = B.Kp_min
        if Kp_min_to_check == 0: Kp_min_to_check = -1
        ####
        if is_MLT_inside_range(MLT, B.MLT_min, B.MLT_max):
            if         MagLat   > B.MagLat_min    and  MagLat   <= B.MagLat_max:
                if     Altitude > B.Altitude_min  and  Altitude <= B.Altitude_max:
                    if Kp       > Kp_min_to_check and  Kp       <= B.Kp_max:
                        MatchedBin = B
                        break
    return MatchedBin



def getBinByItsProperties( MLT_min, MLT_max, MagLat_min, MagLat_max, Altitude_min, Altitude_max, Kp_min, Kp_max ):
    """
        Finds and returns the Bin object having the ranges of the arguments.
        
        Args:
                MLT_min: the Magnetic Local Time minimum
                MLT_max: the Magnetic Local Time maximum
                MagLat_min: The Magnetic Latitude minimum
                MagLat_max: The Magnetic Latitude maximum
                Altitude_min: The Altitude minimum
                Altitude_max: The Altitude maximum
                Kp_min: the Kp-index minimum
                Kp_max: the Kp-index maximum
                
        Returns:
                Bin: the Bin in which the position represented by the arguments is matched
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


# returns: the bin object which matches the arguments
def getBinByItsID( IDstr ):
    """
        Finds and returns a Bin object given its ID.
        
        Args:
                IDstr (string): an ID                 
        Returns:
                Bin: the Bin which has the same ID as the argument
    """

    CorrectBin = None
    for B in Bins:
        if B.ID == IDstr:
            CorrectBin = B
            break
    return CorrectBin


def read_geomagnetic_indices(fromYear, toYear):
    """
        Reads the Geomagnetic kp Indices from text files and stores them in a dictionary.
        Geomagnetic kp Indices Files Source (explanation): https://www.ngdc.noaa.gov/stp/GEOMAG/kp_ap.html
        Geomagnetic kp Indices Files Source (download)   : ftp://ftp.ngdc.noaa.gov/STP/GEOMAGNETIC_DATA/INDICES/KP_AP
        Allows the user to select which yeats to load in order to speed up execution.
        
        Args:
                fromYear: the first year for which the Geomagnetic kp Indices will be loaded
                toYear: the last year for which the Geomagnetic kp Indices will be loaded
        Returns:
                -
    """
    
    global GeomagneticIndices
    for Y in range(fromYear, toYear): # this range should be small for execution speed
        with open(GeomagneticIndices_Files_Path + str(Y)) as fp:
            for line in fp:
                year  = "20" + line[0:2]
                month = line[2:4]
                day   = line[4:6]
                kp00  = float(line[12:14]) / 10
                kp03  = float(line[14:16]) / 10
                kp06  = float(line[16:18]) / 10
                kp09  = float(line[18:20]) / 10
                kp12  = float(line[20:22]) / 10
                kp15  = float(line[22:24]) / 10
                kp18  = float(line[24:26]) / 10
                kp21  = float(line[26:28]) / 10
                GeomagneticIndices[(day, month, year, "0")] = kp00
                GeomagneticIndices[(day, month, year, "1")] = kp03
                GeomagneticIndices[(day, month, year, "2")] = kp06
                GeomagneticIndices[(day, month, year, "3")] = kp09
                GeomagneticIndices[(day, month, year, "4")] = kp12
                GeomagneticIndices[(day, month, year, "5")] = kp15
                GeomagneticIndices[(day, month, year, "6")] = kp18
                GeomagneticIndices[(day, month, year, "7")] = kp21
            fp.close()



def is_MLT_inside_range( MLT, MLT_min, MLT_max ):
    """
        Checks if certain Magnetic-Local-Time lies in a certain range. It can handle ranges like 22-2
        Returns:
            true if MLT falls inside [MLT_min, MLT_max]
    """
    if MLT_min <= MLT_max: # example: from 13 to 18 hour
        return (MLT > MLT_min  and  MLT <= MLT_max)
    else: # example: from 22 to 3 hour
        return (MLT > MLT_min  or   MLT <= MLT_max)

            
            
def calculate_coverage( Title, Description, OrbitFilename, KpStartYear, ResultsFilename="" ):
    """
        Read an orbit file and for each position of the satellite calculates how much time the satellite spends inside each bin.
        The results are stored in a text file for later usage.
        Args:
            Title: to be stored inside the results text file
            Description: to be stored inside the results text file
            OrbitFilename: the csv file which describes a satellite orbit. Can be relative path or full path. If not found, the function tries to find the file in Orbit_Files_Path which can br set by set_OrbitFilesPath function.
            KpStartYear (string): the Kp-indexes to be used for the calculation. Choose a period during which the Sun's activity was similar to the one anticipated during your future satellite mission. 
            ResultsFilename (string): At this file the calculation results will be saved for later loading. if it is an empty string then a file at the CoverageResults_Files_Path location will be created with the name OrbitFilename+"."+KpStartYear+".CoverageResults.txt"
        Returns: 
            int: how many bin misses occured
            int: how many bin hits occured
            string: the filename where the coverage results are stored
            int: the duration of execution in seconds
    """
    KpStartYear = str(KpStartYear)
    if len(ResultsFilename)==0: 
        s = OrbitFilename.replace( "\\", "/" )
        if "/" in s:
            s = s[ s.rindex("/")+1 : ]
        ResultsFilename = CoverageResults_Files_Path + s + "." + KpStartYear + ".CoverageResults.txt"    
    ####
    Kp = 0
    startSecs = time.time()
    BinMisses = BinHits = 0
    PREV_time  = CURR_time  = None
    PREV_BinID = CURR_BinID = ""
    if path.exists( ResultsFilename ):
        print( "File " + ResultsFilename + " already exists. Cannot continue in order to prevent overwriting useful data." )
        return 0, 0, "", 0 # <<<<
    ########
    if path.exists( OrbitFilename ):
        orbit_filename_to_load = OrbitFilename
    elif path.exists( Orbit_Files_Path + OrbitFilename ):
        orbit_filename_to_load = Orbit_Files_Path + OrbitFilename
    else:
        print( "File", OrbitFilename, "not found, neither in ./ neither in", Orbit_Files_Path )
        return 0, 0, "", 0
    ########
    with open( orbit_filename_to_load ) as CSVfile:        
        CSVreader = csv.reader( CSVfile )
        # locate the column numnbers of interest inside the csv file
        CSVheader = next( CSVreader )
        Time_idx     = CSVheader.index( "Epoch(UTCG)" ) 
        Lat_idx      = CSVheader.index( "Lat_GEOD(deg)" )
        Lon_idx      = CSVheader.index( "Lon_GEOD(deg)" )
        Altitude_idx = CSVheader.index( "Height_WGS84 (km)" )
        try:
            MagLat_idx   = CSVheader.index( "Magnetic Latitude" )
        except:
            MagLat_idx   = CSVheader.index( "Daedalus.Magnetic Latitude" )
        try:
            MLT_idx      = CSVheader.index( "MLT" )
        except:
            MLT_idx      = CSVheader.index( "Daedalus.MLT" )
        # read the satellite positions and try to fill the bins
        n = 0
        num_of_errors = 0
        for row in CSVreader: # for each satellite position
            n = n + 1
            if n == 1: OrbitStartYear = parseDate( row[Time_idx] ).year
            PREV_time = CURR_time
            # parse the date-time of this satellite position
            CURR_time = parseDate( row[Time_idx] ) 
            if CURR_time == None:
                print( "ERROR during coverage calculation while reading", orbit_filename_to_load, ": Wrong time format:",row[Time_idx],".:  ", row )
                num_of_errors += 1
                if num_of_errors < 50:
                    continue
                else:
                    print("Too many errors. Aborting.")
                    return 0, 0, "", 0 # <<<<
            year  = CURR_time.year
            month = CURR_time.month
            day   = CURR_time.day
            hour  = CURR_time.hour
            # calculate the Kp index for this particular time
            try:
                Kp = GeomagneticIndices[(num_to_2digit_str(day), num_to_2digit_str(month), num_to_2digit_str(Years_Dropdown.value+year-OrbitStartYear), str(hour//3))]
            except:
                if month==2 and day==29: # the leap years may correspond to non-leap years at the selected range of years for Kp calculation
                    Kp = GeomagneticIndices[(num_to_2digit_str(28), num_to_2digit_str(month), num_to_2digit_str(Years_Dropdown.value+year-OrbitStartYear), str(hour//3))]
            # remember some useful properties of this satellite position
            MLT      = float( row[MLT_idx] )
            MagLat   = float( row[MagLat_idx] )
            Altitude = float( row[Altitude_idx] )
            # Check if the satellite position can be assigned to a bin
            mathedBin = GetMatchedBin( MLT, MagLat, Altitude, Kp )
            # If the satellite is inside a bin during the last 2 positions then calculate the duration
            PREV_BinID = CURR_BinID
            if mathedBin is None:
                CURR_BinID = ""
            else:
                CURR_BinID = mathedBin.ID            
            if len(CURR_BinID) > 0  and  CURR_BinID == PREV_BinID:
                BinHits = BinHits + 1
                DurationInsideBin = (CURR_time - PREV_time).seconds
                mathedBin.CumulativeTime += DurationInsideBin 
            elif len(CURR_BinID) > 0:
                BinMisses = BinMisses + 1
    # calculate duration of execution
    finishSecs = time.time()
    DurationOfExecution = finishSecs-startSecs
    # Save the results in a text file
    nowstr = datetime.now().strftime("%d-%m-%Y %H:%M:%S")    
    F = open(ResultsFilename, 'w')
    F.write( "# -- COVERAGE RESULTS -- " + "\n"  )
    F.write( "# Date of execution: " + nowstr + "\n" )
    F.write( "# Title: " + Title + "\n" )
    F.write( "# Description: " + Description + "\n")
    F.write( "# Parsed " + str(n) + " lines from orbit file " + orbit_filename_to_load + "\n")
    F.write( "# Used Kp indices starting from year " + KpStartYear + "\n")
    F.write( "# Bin Misses: " + str(BinMisses) + "     Bin Hits: " + str(BinHits) + "\n")
    F.write( "# Duration of execution: " + ConvertLeadingZerosToSpaces("{0:.0f}".format(DurationOfExecution)) + " seconds  or  " + ConvertLeadingZerosToSpaces("{0:.2f}".format(DurationOfExecution/60))  + " minutes" + "\n" )
    F.write( "# " + "\n")    
    for B in Bins:
        F.write( B.getInfo() + "\n" )
    F.close()
    #
    return BinMisses, BinHits, ResultsFilename, DurationOfExecution
            
    
    
def load_coverage_results( ResultsFilename ):
    """
        Loads a coverage-results file and store the information in the Bins. 
        Args:
            ResultsFilename: the coverage-results file to read
        Returns:
            (string): the title of the loaded calculation.
            (string): the description of the loaded calculation.
            (string): the orbit filename used for the loaded calculation.
            (string): the Kp-start-year used for the loaded calculation.
    """
    with open(ResultsFilename, 'r') as F:
        for line in F:
            if line[0:1] == '#': # this line contains a comment, print it as it is.
                print ( line[1:len(line)-1] )
                if line.startswith("# Title:"): COVERAGE_Title = line[8:].strip()
                if line.startswith("# Description:"): COVERAGE_Description = line[14:].strip()
                if line.startswith("# Parsed"): COVERAGE_OrbitFilename = line[line.find("orbit file")+11:].strip()
                if line.startswith("# Used Kp"): COVERAGE_KpStartYear = line[37:].strip()
            else: # this line contains bin info, print it and store them in the correct bin.
                print ( line[:len(line)-1] )
                aBinID = line[:line.find(":")].strip()
                secondsInBin = float( line[line.rfind("min")+3:line.rfind("/")] )
                for B in Bins:
                    if B.ID == aBinID:
                        B.CumulativeTime = secondsInBin
                        break
    F.close()
    return COVERAGE_Title, COVERAGE_Description, COVERAGE_OrbitFilename, COVERAGE_KpStartYear
