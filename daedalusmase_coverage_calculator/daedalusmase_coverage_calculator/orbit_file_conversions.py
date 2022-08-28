'''
This module is used for calculating magnetic coordinates from geographic coordinates.
It reads a CSV-formated file describing an orbit in geographic coordinates and 
creates a new CSV file with extra fields for the corresponding magnetic coordinates for each position.
'''


import pandas as pd
import apexpy as ap
import numpy as np
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import csv
import plotly
import chart_studio.plotly as py 
import plotly.graph_objects as go

import Conversions

def parseDaedalusDate( dateString ):
    """
    utility which parses a string to a date object.
    """
    result = None
    try:
        result = datetime.strptime(dateString, '%d %b %Y %H:%M:%S.%f')
    except:
        try:
            result = datetime.strptime(dateString, '%b %d %Y %H:%M:%S.%f')
        except:
            try:
                result = datetime.strptime(dateString[0:24], '%b %d %Y %H:%M:%S.%f')                
            except:
                result = None
    return result



def add_magnetic_coordinates( sourceFilename, resultFilename ):
    ''' 
    Reads a csv orbit file (sourceFilename) with format:  
    
        | Field Description | Example value            | Column Name in CSV file |
        | ----------------- | ------------------------ | ----------------------- |
        | Time (UTCG)       | 01 Jan 2015 00:00:00.000 | "Epoch(UTCG)"           |
        | Latitude (deg)    | -22.048                  | "Lat_GEOD(deg)"         |
        | Longitude (deg)   | 83.92                    | "Lon_GEOD(deg)"         |
        | Altitude (km)     | 218.728507               | "Height_WGS84 (km)"     |
          
    and creates a new csv orbit file (resultFilename) with the same fields plus the extra fields:

        | Field Description         | Example value        | Column Name in CSV file |
        | ------------------------- | -------------------- | ----------------------- |
        | Magnetic Latitude (deg)   | -34.185760498046875  | "Magnetic Latitude"     |
        | Magnetic Longitude (deg)  | 153.52354431152344   | "Magnetic Longitude"    |
        | Magnetic Local Time       | 5.061925760904948    | "MLT"                   |
           
    The values are calculated for modified apex at 90 km - used by TIEGCM as well
    '''
    startSecs = time.time()
    prev_time = current_time = None
    timestep  = 0 
    linenum   = 0
    CSVfileOUT = open(resultFilename, 'w')
    CSVwriter  = csv.writer(CSVfileOUT, delimiter=',')
    CSVwriter.writerow( ["Epoch(UTCG)", "Lat_GEOD(deg)", "Lon_GEOD(deg)", "Height_WGS84 (km)", "Magnetic Latitude", "Magnetic Longitude", "MLT"] )
    with open( sourceFilename ) as CSVfileIN:        
        CSVreader = csv.reader( CSVfileIN )
        # locate the column numnbers of interest inside the csv file
        CSVheader = next( CSVreader )
        try:
            Time_idx     = CSVheader.index( "Epoch(UTCG)" ) 
        except:
            Time_idx     = CSVheader.index( "Daedalus.EpochText" )
        try:
            Lat_idx      = CSVheader.index( "Lat_GEOD(deg)" ) 
        except:
            Lat_idx      = CSVheader.index( "Daedalus.Latitude" )
        try:
            Lon_idx      = CSVheader.index( "Lon_GEOD(deg)" )
        except:
            Lon_idx      = CSVheader.index( "Daedalus.Longitude" )
        try:
            Alt_idx      = CSVheader.index( "Height_WGS84 (km)" )
        except:
            Alt_idx      = CSVheader.index( "Daedalus.Longitude" )
        # read the orbit file
        for row in CSVreader: # for each satellite position
            if len(list(row))==0: break # <<<<
            linenum += 1
            resultItems = list()
            # add the standard fields to the result file
            resultItems.append( row[Time_idx] )
            resultItems.append( row[Lat_idx] ) # Latitude is geodetic inside the orbit file
            resultItems.append( row[Lon_idx] ) 
            resultItems.append( row[Alt_idx] )
            # Calculate the extra fields    
            prev_time    = current_time
            current_time = parseDaedalusDate( row[Time_idx] )  # read time for the current orbit position 
            if current_time == None:
                print( "ERROR - Wrong time format at line", linenum, ":", row[Time_idx] )
                continue       
            if prev_time is not None:
                if timestep==0:
                    timestep = calendar.timegm(current_time.utctimetuple()) - calendar.timegm(prev_time.utctimetuple())
                else:
                    if calendar.timegm(current_time.utctimetuple()) - calendar.timegm(prev_time.utctimetuple()) != timestep:
                        print( "Time leap at line", linenum, ":", row, "(", calendar.timegm(current_time.utctimetuple()) - calendar.timegm(prev_time.utctimetuple()) ,"sec)", "\n", prev_time, "\n", current_time )
            # take care of time so that it is compatible with igrf
            #if current_time.year > 2024:  
            #    time_for_igrf = current_time - relativedelta(years=13)
            #else:
            #    time_for_igrf = current_time
            time_for_igrf = current_time
            MagneticLatitude, MagneticLongitude, MagneticLocalTime = Conversions.getMagneticProperties( time_for_igrf, float(row[Lat_idx]), float(row[Lon_idx]), float(row[Alt_idx]) )
            # add the extra fields to the result file
            resultItems.append( MagneticLatitude )
            resultItems.append( MagneticLongitude )
            resultItems.append( MagneticLocalTime )
            # write it
            CSVwriter.writerow( resultItems )
    # clean up
    CSVfileOUT.close()
    finishSecs = time.time()
    print( "Processed", linenum, "lines in" , finishSecs-startSecs, "sec")

    

    
def plot_MagneticProperties_ofTwoOrbits( orbitfilename1, orbitfilename2, plot_title1, plot_title2, num_of_points_to_plot=5000):
    """
    Plots the Magnetic Coordinates of the two orbits together in order to compare them.
    It creates 3 plots: for Magnetic Latitude, Magnetic Longitude and Magnetic Local Time
    
    Args:
        orbitfilename1: the filename of the 1st csv orbit file
        orbitfilename2: the filename of the 2nd csv orbit file
        plot_title1: the title related to the 1st orbit file, to be displayed on the chart.
        plot_title2: the title related to the 2nd orbit file, to be displayed on the chart.
        num_of_points_to_plot: how many positions (points) will be displayed on the chart. 
        If they are too many it will be cpu-intensive to be displayed, if they are too few then very little information will be shown.
    """
    print( "Reading files", orbitfilename1, orbitfilename2 )
    # read data from orbit1 file
    fd1 = pd.read_csv( orbitfilename1 ) 
    MAGLATs1 = np.array(fd1["Magnetic Latitude"])
    MAGLONs1 = np.array(fd1["Magnetic Longitude"])
    MAGTIMs1 = np.array(fd1["MLT"])
    # read data from orbit2 file
    fd2 = pd.read_csv( orbitfilename2 ) 
    MAGLATs2 = np.array(fd2["Magnetic Latitude"])
    MAGLONs2 = np.array(fd2["Magnetic Longitude"])
    MAGTIMs2 = np.array(fd2["MLT"])
    
    # make data smaller so that they can be plotted
    plot_step = int( len(MAGLATs1) / num_of_points_to_plot )
    MAGLATs1 = MAGLATs1[0::plot_step]
    MAGLONs1 = MAGLONs1[0::plot_step]
    MAGTIMs1 = MAGTIMs1[0::plot_step]
    MAGLATs2 = MAGLATs2[0::plot_step]
    MAGLONs2 = MAGLONs2[0::plot_step]
    MAGTIMs2 = MAGTIMs2[0::plot_step]
    print( "plotting totally", num_of_points_to_plot, "points. That is one every", plot_step )
    '''
    MAGLATs1 = MAGLATs1[0:num_of_points_to_plot]
    MAGLONs1 = MAGLONs1[0:num_of_points_to_plot]
    MAGTIMs1 = MAGTIMs1[0:num_of_points_to_plot]
    MAGLATs2 = MAGLATs2[0:num_of_points_to_plot]
    MAGLONs2 = MAGLONs2[0:num_of_points_to_plot]
    MAGTIMs2 = MAGTIMs2[0:num_of_points_to_plot]
    '''
        
    # plot the Magnetic Latitudes of the two orbits together
    fig = go.Figure()
    fig.add_trace( go.Scatter(name=plot_title1, x=list(range(0,len(MAGLATs1))), y=MAGLATs1, mode='markers', marker_size=3, marker_color="red"  ) )
    fig.add_trace( go.Scatter(name=plot_title2, x=list(range(0,len(MAGLATs2))), y=MAGLATs2, mode='markers', marker_size=3, marker_color="blue"  ) )
    fig.update_layout( title="Magnetic Latitudes comparison", width=1000, height=900, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
    fig.update_xaxes( title="time step number" )
    fig.update_yaxes( title="Magnetic Latitude") 
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig)
    # plot the Magnetic Longitudes of the two orbits together
    fig = go.Figure()
    fig.add_trace( go.Scatter(name=plot_title1, x=list(range(0,len(MAGLONs1))), y=MAGLONs1, mode='markers', marker_size=3, marker_color="red"  ) )
    fig.add_trace( go.Scatter(name=plot_title2, x=list(range(0,len(MAGLONs2))), y=MAGLONs2, mode='markers', marker_size=3, marker_color="blue"  ) )
    fig.update_layout( title="Magnetic Longitudes comparison", width=1000, height=900, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
    fig.update_xaxes( title="time step number" )
    fig.update_yaxes( title="Magnetic Longitude") 
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig)
    # plot the Magnetic Local Times of the two orbits together
    fig = go.Figure()
    fig.add_trace( go.Scatter(name=plot_title1, x=list(range(0,len(MAGTIMs1))), y=MAGTIMs1, mode='markers', marker_size=3, marker_color="red"  ) )
    fig.add_trace( go.Scatter(name=plot_title2, x=list(range(0,len(MAGTIMs2))), y=MAGTIMs2, mode='markers', marker_size=3, marker_color="blue"  ) )
    fig.update_layout( title="Magnetic Local Time comparison", width=1000, height=900, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
    fig.update_xaxes( title="time step number" )
    fig.update_yaxes( title="Magnetic Local Time") 
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig)
    
    
