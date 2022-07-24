'''
This module contains functions which plot the coverage results.
'''

import csv
import time
import math
import plotly
import chart_studio.plotly as py 
import plotly.graph_objects as go
import plotly.offline as offline
import seaborn as sns
import matplotlib.pyplot as matplt

from data import *
from utils import *
from datetime import datetime
import calendar

# colors used at plotting
MyColors = ["#217ca3", "#e29930", "#919636", "#af1c1c", "#e7552c", "#1b4b5a", "#e4535e", "#aebd38", "#ffbb00", "#2c7873"]


def PlotCoverage_Bars( PlotTitle = "" ):
    """
    Plots the Bins as vertical bars. The altitude is at the Vertical Axis. Kp index and Magnetic Local Time is at the Horizontal Axis.
    Bins are colored and labeled according to the time the satellite spends inside them.
    One plot per Magnetic Latitude range is created.
    Args:
         PlotTitle: a title to be displayed on the top of the plot (if not empty)
    """
    ColumnWidth = 80
            
    All_MagLatRanges = list()
    for B in Bins:
        if [B.MagLat_min, B.MagLat_max] not in All_MagLatRanges:
            All_MagLatRanges.append( [B.MagLat_min, B.MagLat_max] )            
    
    for aMagLatRange in All_MagLatRanges:
        # We will create one plot for each MagLatRange 
        fig = go.Figure()
        # init
        Xposition = 20
        XaxisTickPositions = list()
        XaxisTickLabels = list()
        TheLowestAltitudeInThePlot  = 10000
        TheHighestAltitudeInThePlot = 0
        
        # find out all MLT ranges for this MagLat range
        All_MLTRanges = list()
        tickValues = list()
        for B in Bins:
            if B.MagLat_min==aMagLatRange[0] and  B.MagLat_max==aMagLatRange[1]:
                # remember all Altitudes in order to display them as tick values on the y axis
                if B.Altitude_min not in tickValues: tickValues.append( B.Altitude_min )
                if B.Altitude_max not in tickValues: tickValues.append( B.Altitude_max )
                #
                if [B.MLT_min, B.MLT_max] not in All_MLTRanges:
                    All_MLTRanges.append( [B.MLT_min, B.MLT_max] )
        
        # find out all Kp ranges for this MagLat range and this MLTrange 
        for aMLTrange in All_MLTRanges:
            All_KpRanges = list()
            for B in Bins:
                if B.MagLat_min==aMagLatRange[0] and  B.MagLat_max==aMagLatRange[1]:
                    if B.MLT_min==aMLTrange[0] and  B.MLT_max==aMLTrange[1]:
                        if [B.Kp_min, B.Kp_max] not in All_KpRanges:
                            All_KpRanges.append( [B.Kp_min, B.Kp_max] )

            # find out all Altitude ranges for this MagLat range, this MLT range and this Kp range            
            for aKpRange in All_KpRanges:
                XaxisTickPositions.append( Xposition + ColumnWidth/2 )
                XaxisTickLabels.append( "Kp " + str(aKpRange[0]) + "-" + str(aKpRange[1]) + "<br>" + str(aMLTrange[0]) + "-" + str(aMLTrange[1]) )
                ####
                All_AltitudeRanges = list()
                for B in Bins:
                    if B.MagLat_min==aMagLatRange[0] and  B.MagLat_max==aMagLatRange[1]:
                        if B.MLT_min==aMLTrange[0] and  B.MLT_max==aMLTrange[1]:
                            if B.Kp_min==aKpRange[0] and  B.Kp_max==aKpRange[1]:
                                All_AltitudeRanges.append( [B.Altitude_min, B.Altitude_max] )
                                # calculate the range of the Vertical Axis
                                if B.Altitude_min<TheLowestAltitudeInThePlot: TheLowestAltitudeInThePlot=B.Altitude_min
                                if B.Altitude_max>TheHighestAltitudeInThePlot: TheHighestAltitudeInThePlot=B.Altitude_max
            
                # create one figure per altitude range
                for anAltitudeRange in All_AltitudeRanges:
                    currentBin = getBinByItsProperties( aMLTrange[0], aMLTrange[1], aMagLatRange[0], aMagLatRange[1], anAltitudeRange[0], anAltitudeRange[1], aKpRange[0], aKpRange[1] )
                    fig.add_shape(go.layout.Shape(
                        type="rect", xref="x", yref="y", 
                        x0=Xposition, y0=currentBin.Altitude_min, x1=Xposition+ColumnWidth, y1=currentBin.Altitude_max,
                        line=dict( color="RoyalBlue", width=3,), fillcolor=getColor(currentBin.CumulativeTime, 0, currentBin.DesirableCumulativeTime, "BuPu"), opacity=0.8, 
                    ))
                    BinTitle = currentBin.ID + "<br>" + "{:3.0f}".format(currentBin.CumulativeTime/60) +  " / " + "{:2.0f}".format(currentBin.DesirableCumulativeTime/60)
                    fig.add_trace(go.Scatter(x=[Xposition + ColumnWidth/2],y=[(currentBin.Altitude_max+currentBin.Altitude_min)/2],text=["<b>"+BinTitle+"</b>"],mode="text", ))
                Xposition += ColumnWidth + 10
            Xposition += 28
        
        FigureTitle = ""
        if len(PlotTitle) > 0: FigureTitle += PlotTitle
        FigureTitle += "<b>Magnetic Latitudes from " + str(aMagLatRange[0]) + "&#176; to "+str(aMagLatRange[1])+"&#176;"+"</b><br>"
        fig.update_layout(width=1100, height=1640, showlegend=False, title=FigureTitle,
                          xaxis_title="Kp index range<br>Magnetic Local Time range", yaxis_title="Altitude (km)", 
                          margin=go.layout.Margin(b=150,t=150) ) 
        # add a colorbar
        fig.add_trace(go.Scatter( x=[0,0], y=[0,0], opacity=0,  mode="markers",
            marker=dict(colorscale="BuPu", color=[0,100], colorbar=dict(tickvals=[0,100], ticktext=['empty','full'] ),),
        ))
        
        fig.update_xaxes(range=[0, Xposition-10], showgrid=False)
        fig.update_xaxes( tickmode = 'array', tickvals=XaxisTickPositions,  ticktext=XaxisTickLabels )
        fig.update_yaxes(type="log", range=[ math.log(TheLowestAltitudeInThePlot,10)-0.004, math.log(TheHighestAltitudeInThePlot,10)+0.008], tickvals=tickValues ) 
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig) 
        
        
def PlotCoverage_Bars_GroupedByRegion(PlotTitle="", RegionGroups=[["AEE", "AEM","AED"],  ["AFM","CF","PCF"],  ["EPB", "SQ"],  ["EEJ"]]):
    """
    Plots the Bins as vertical bars. The altitude is at the Vertical Axis. Kp index Magnetic Local Time and Magnetic Latitude is at the Horizontal Axis.
    Bins are colored and labeled according to the time the satellite spends inside them.
    One plot per Region Group is created.
    Args:
        PlotTitle: a title to be displayed on the top of the plot (if not empty)
        RegionGroups: a list o lists containing region names to be pllotted together
    """
    Xposition = 20
    ColumnWidth = 100
    DistanceBetweenColumns = 15
    DistanceBetweenRegions = 40
    
    # populate groups with full Bin-IDs 
    Groups =list()
    for i in range(0, len(RegionGroups)):
        Groups.append( list() )
        for BinGeneralID in RegionGroups[i]:
            for B in Bins:
                if B.ID.startswith( BinGeneralID ):
                    Groups[i].append( B.ID )
    
    for G in Groups:
        # We will create one plot for each group
        fig = go.Figure()
        
        # contruct X-axis labels 
        currentTickPosition = 20 + ColumnWidth / 2
        XaxisTickPositions = list()
        XaxisTickLabels = list()
        for BinID in G:
            currentBin = getBinByItsID( BinID )
            aLabel =  "Kp " + str(currentBin.Kp_min) + "-" + str(currentBin.Kp_max) + "<br>MLT " + str(currentBin.MLT_min) + "-" + str(currentBin.MLT_max) + "<br>" + str(currentBin.MagLat_min) + "&#xb0;-" + str(currentBin.MagLat_max) + "&#xb0;"
            if aLabel not in XaxisTickLabels:                
                XaxisTickLabels.append( aLabel )
                if len(XaxisTickLabels) >= 2:
                    currentTickPosition += ColumnWidth + DistanceBetweenColumns 
                    if XaxisTickLabels[-1][XaxisTickLabels[-1].find("MLT"):] !=  XaxisTickLabels[-2][XaxisTickLabels[-2].find("MLT"):]:
                        currentTickPosition += DistanceBetweenRegions
                XaxisTickPositions.append( currentTickPosition )   
        
        # remember all Altitudes in order to display them as tick values on the y axis
        AllAltitudes = list()
        for i in range(0, len(G)):
            currentBinID = G[i]
            currentBin = getBinByItsID( currentBinID )
            if currentBin.Altitude_min not in AllAltitudes: AllAltitudes.append( currentBin.Altitude_min )
            if currentBin.Altitude_max not in AllAltitudes: AllAltitudes.append( currentBin.Altitude_max )
        # find min and max altitude
        try:
            TheLowestAltitudeInThePlot  = min( AllAltitudes )
        except:
            TheLowestAltitudeInThePlot = 100
        try:
            TheHighestAltitudeInThePlot = max( AllAltitudes )
        except:
            TheHighestAltitudeInThePlot = 500
    
        for i in range(0, len(G)): # create one rectangle per bin
            currentBinID = G[i]
            currentBin = getBinByItsID( currentBinID )
            currentBinGeneralID = currentBinID[ : currentBinID.find('_') ]
            
            #### calculate the X position where the rectanlge will be drawn ####
            group_idx = 0
            for aGeneralGroup in RegionGroups:
                if currentBinGeneralID in aGeneralGroup:
                    group_idx = 0
                    for i in  range(0, len(aGeneralGroup)):
                        if aGeneralGroup[i] == currentBinGeneralID: group_idx = i
            #
            KpRanges = list()
            for B in Bins:
                if B.ID.startswith( currentBinGeneralID ):
                    if [B.Kp_min, B.Kp_max] not in KpRanges:
                        KpRanges.append( [B.Kp_min, B.Kp_max] )
            KPrange_idx = 0
            for i in range( 0, len(KpRanges) ):
                if currentBin.Kp_min==KpRanges[i][0] and currentBin.Kp_max==KpRanges[i][1]: KPrange_idx = i
            #
            Xposition = 20 + group_idx*(len(KpRanges)*(ColumnWidth+DistanceBetweenColumns)+DistanceBetweenRegions) + KPrange_idx*(ColumnWidth+DistanceBetweenColumns)
            
            
            fig.add_shape(go.layout.Shape( type="rect", xref="x", yref="y", 
                        x0=Xposition, y0=currentBin.Altitude_min, x1=Xposition+ColumnWidth, y1=currentBin.Altitude_max,
                        line=dict( color="RoyalBlue", width=3,), fillcolor=getColor(currentBin.CumulativeTime, 0, currentBin.DesirableCumulativeTime, "BuPu"), opacity=0.8, 
            ))
            BinTitle = currentBin.ID + "<br>" + "{:3.0f}".format(currentBin.CumulativeTime/60) +  " / " + "{:2.0f}".format(currentBin.DesirableCumulativeTime/60)
            fig.add_trace(go.Scatter(x=[Xposition + ColumnWidth/2],y=[(currentBin.Altitude_max+currentBin.Altitude_min)/2],text=["<b>"+BinTitle+"</b>"],mode="text", ))
                            
        FigureTitle = ""
        if len(PlotTitle) > 0: FigureTitle += PlotTitle
        #FigureTitle += "(boxes contain minutes of cummulative time the satellite spends inside each bin)"
        fig.update_layout(width=1100, height=650, showlegend=False, title=FigureTitle,
                          xaxis_title="Kp index range<br>Magnetic Local Time range (hours)<br>Magnetic Latitude (degrees)", yaxis_title="Altitude (km)", 
                          margin=go.layout.Margin(b=150,t=150) ) 
        # add a colorbar
        fig.add_trace(go.Scatter( x=[0,0], y=[0,0], opacity=0,  mode="markers",
            marker=dict(colorscale="BuPu", color=[0,100], colorbar=dict(tickvals=[0,100], ticktext=['empty','full'] ),),
        ))
        
        fig.update_xaxes(range=[0, Xposition+ColumnWidth+20], showgrid=False)
        fig.update_xaxes( tickmode = 'array', tickvals=XaxisTickPositions,  ticktext=XaxisTickLabels )
        fig.update_yaxes(range=[TheLowestAltitudeInThePlot,TheHighestAltitudeInThePlot+1+int((TheHighestAltitudeInThePlot-TheLowestAltitudeInThePlot)/30)], tickvals=AllAltitudes ) 
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig) 
        
        
        
        
def PlotCoverage_PolarChart( PlotTitle = "",  size_multiplicator = 1 ):
    """
    Plots the Bins in a polar chart. The radial axis contains the Magnetic Latitude and the Arcs represent Magnetic Local Time.
    Bins are colored and the coverage results are displayed beside the chart.
    One plot per Altitude range is created.
    Args:
        PlotTitle: a title to be displayed on the top of the plot (if not empty).
        size_multiplicator: changes the chart's size by multipling its dimensions by this number.
    """
    PlotBackgroundColor = "Gainsboro"
    MyColorsIndex = 0
    AltitudeREGIONS = [ [115,140], [140,500] ]
    num_of_extra_legend_lines = 0
    
    for anAltitudeREGION in AltitudeREGIONS:    
        MyColorsIndex = 0
        # Find out all Magnetic Latitude Values which will be displayed in the plot, at the radial axis
        AllMagLatValues = list()
        for B in Bins:
            if B.Altitude_min>=anAltitudeREGION[0] and B.Altitude_max<=anAltitudeREGION[1]:
                if B.MagLat_min not in AllMagLatValues: AllMagLatValues.append(B.MagLat_min)
                if B.MagLat_max not in AllMagLatValues: AllMagLatValues.append(B.MagLat_max)
                
        # for each bin which belongs to the region
        fig = go.Figure()
        for B in Bins:
            if B.Altitude_min>=anAltitudeREGION[0] and B.Altitude_max<=anAltitudeREGION[1]:
                # convert bin values in order to be displayed on the polar plot
                MLTmin = B.MLT_min
                MLTmax = B.MLT_max
                if MLTmin > MLTmax: MLTmax += 24 # takes account of durations like 22:00-02:00
                SliceAngle  = 15*(MLTmin+(MLTmax - MLTmin)/2) -90 # 360degrees/24hours=15
                SliceWidth  = 15*(MLTmax - MLTmin)
                # construct the bin info string
                BinInfo = "{:3.0f}".format(B.Altitude_min) + "-" + "{:3.0f}".format(B.Altitude_max) + "km " + ": Kp"+ str(B.Kp_min) + "-" + str(B.Kp_max) + ": " 
                if B.CumulativeTime > B.DesirableCumulativeTime: BinInfo += "<b>"
                BinInfo += "{:3.0f}".format(B.CumulativeTime/60) 
                if B.CumulativeTime >= B.DesirableCumulativeTime: BinInfo += "</b>"
                BinInfo += "/" + "{:3.0f}".format(B.DesirableCumulativeTime/60)  + "min"
                    
                # check if this slice has been already plotted
                FoundFigureIndex = -1
                for i in range( len(fig.data) ):
                    if fig.data[i]["theta"][0]==SliceAngle and fig.data[i]["width"][0]==SliceWidth:
                        FoundFigureIndex = i
                        break

                # plot a new slice for this bin or add info about this bin to the legend text
                if FoundFigureIndex >= 0:
                    fig.data[ FoundFigureIndex ][ "name" ] += BinInfo + "<br>"
                    num_of_extra_legend_lines += 1
                else:
                    fig.add_trace(go.Barpolar( base=[B.MagLat_min], r=[B.MagLat_max-B.MagLat_min], theta=[SliceAngle], width=[SliceWidth], 
                        text=[B.ID], marker_color=[MyColors[MyColorsIndex]],   opacity=0.84,
                        name = "<b>" + B.Description + "</b>" + "<br>" + BinInfo + "<br>"
                    ))
                    num_of_extra_legend_lines += 2
                    MyColorsIndex += 1
                    if MyColorsIndex >= len(MyColors): MyColorsIndex = 0
            
        # construct the radial axis values
        if 0 not in AllMagLatValues:
            there_are_positives = there_are_negatives = False
            for aMagLatVal in AllMagLatValues:
                if aMagLatVal > 0: there_are_positives = True
                if aMagLatVal < 0: there_are_negatives = True
            if there_are_positives and there_are_negatives: 
                AllMagLatValues.append(0)
                fig.add_trace(go.Barpolar( base=[0], r=[1], theta=[0], width=[360], 
                        text=["Equator"], marker_color="gray",   opacity=0.84,
                        name = "<b>" + "Equator" + "</b>"
                ))
        #
        if 90 not in AllMagLatValues: AllMagLatValues.append(90)
        RadialAxisTickValues= list()
        for i in range( len(AllMagLatValues) ):
            RadialAxisTickValues.append( "<b>" + str(AllMagLatValues[i]) + "&#176;" + "</b>")
             
        
        # Construct the plot's title
        FigureTitle = ""
        if len(PlotTitle) > 0: FigureTitle += PlotTitle
        FigureTitle += "<b>Altitude from " + str(anAltitudeREGION[0]) + " to " + str(anAltitudeREGION[1]) + "</b>" + "<br>"
        # define the plot's layout
        num_of_extra_legend_lines -= 33
        if num_of_extra_legend_lines < 0 : num_of_extra_legend_lines = 0
        size_multiplicator = 1
        fig.update_layout(width=780*size_multiplicator, height=900 + num_of_extra_legend_lines*18 + (size_multiplicator-1)*200, showlegend=True, title=FigureTitle, 
                          polar = dict(
                            bgcolor=PlotBackgroundColor, 
                            radialaxis  =  dict(range = [90, min(AllMagLatValues)], tickvals=AllMagLatValues, ticktext=RadialAxisTickValues, tickangle=90, categoryorder = "category descending" ), 
                            angularaxis = dict(tickvals=[      0,      30,      60,      90,     120,     150,     180,     210,     240,     270,     300,     330], 
                                               ticktext=['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '00:00', '02:00', '04:00'])
                         ),
                         margin=go.layout.Margin(b=150,t=150), )
        # plot it
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig) 
        

        
def PlotOrbit_KpScatter(OrbitFileName, kp_startYear, from_date_str, to_date_str, from_Altitude, to_Altitude):
    """
    This plot displays all satellite positions as points colored by Kp-index. 
    The Kp-indexes related to the orbit can be chosen by setting kp_startYear.
    The Magnetic Latitude is at Vertical Axis and Magnetic Local Time is at the Horizontal Axis.
    Args:
        OrbitFileName: the filename of the csv file describing the satellite's orbit
        kp_startYear: decides which Kp-index values to assign to each satellite position
        from_date_str: the first satellite position to be displayed
        to_date_str: the last satellite position to be displayed
        from_Altitude: include only positions from this altitude and above
        to_Altitude: include only positions until this altitude.
    """
    StartSecs = time.time()
    
    with open( OrbitFileName ) as CSVfile:
        CSVreader = csv.reader( CSVfile )
        # locate the column numnbers of interest inside the csv file
        CSVheader = next( CSVreader )
        Time_idx     = CSVheader.index( "Epoch(UTCG)" ) #CSVheader.index( "EpochText" )
        Lat_idx      = CSVheader.index( "Lat_GEOD(deg)" ) #CSVheader.index( "Latitude" )
        Lon_idx      = CSVheader.index( "Lon_GEOD(deg)" ) #CSVheader.index( "Longitude" )
        Altitude_idx = CSVheader.index( "Height_WGS84 (km)" ) #CSVheader.index( "Height" )
        MagLat_idx   = CSVheader.index( "Magnetic Latitude" )
        MLT_idx      = CSVheader.index( "MLT" )
        # read the satellite positions and add them to lists for ploting
        new_x_axis = list()
        new_y_axis = list()
        kp_array   = list()
        lineNum=0
        for row in CSVreader: # for each satellite position
            lineNum += 1
            if lineNum == 1: OrbitStartYear = parseDate( row[Time_idx] ).year
            CURR_Altitude = float( row[Altitude_idx] )
            CURR_time = parseDate( row[Time_idx] )
            if CURR_time == None:
                print( "ERROR during Kp-scatter while reading", OrbitFileName, ": Wrong time format:", row[Time_idx] )
                return 0, 0, "", 0 # <<<<
            CURR_timestamp = calendar.timegm( CURR_time.utctimetuple() ) 
            FROM_timestamp = calendar.timegm( datetime.strptime( from_date_str,  "%d-%m-%Y" ).utctimetuple() ) 
            TO_timestamp   = calendar.timegm( datetime.strptime( to_date_str,  "%d-%m-%Y" ).utctimetuple() ) 
            if CURR_Altitude>=from_Altitude and CURR_Altitude<=to_Altitude and CURR_timestamp>=FROM_timestamp and CURR_timestamp<=TO_timestamp:
                year  = CURR_time.year
                month = CURR_time.month
                day   = CURR_time.day
                hour  = CURR_time.hour
                Kp = -1
                try: # calculate the Kp index for this particular time
                    Kp = GeomagneticIndices[(num_to_2digit_str(day), num_to_2digit_str(month), num_to_2digit_str(kp_startYear+year-OrbitStartYear), str(hour//3))]
                except:
                    if month==2 and day==29: # the leap years may correspond to non-leap years at the selected range of years for Kp calculation
                        Kp = GeomagneticIndices[(num_to_2digit_str(28), num_to_2digit_str(month), num_to_2digit_str(kp_startYear.value+year-OrbitStartYear), str(hour//3))]
                # remember some useful properties of this satellite position
                new_x_axis.append( float( row[MLT_idx]    ) )
                new_y_axis.append( float( row[MagLat_idx] ) )
                kp_array.append  ( Kp )
    
    #df['MLT'] = df['MLT'][0::3]
    #df['Magnetic Latidude'] = df['Magnetic Latidude'][0::3]
    #df['Kp'] = df['Kp'][0::3]
    
    # thin out the data because thery are too many 
    #new_x_axis = new_x_axis[::3]
    #new_y_axis = new_y_axis[::3]
    #kp_array   = kp_array[::3]
    print( "I will plot", len(new_x_axis), "dots")

    # create the Kp scatter 
    fig = go.Figure()
    fig.add_trace(go.Scattergl( x=new_x_axis, y=new_y_axis,
                              mode='markers', marker=dict(color=kp_array, cmin=0, cmax=9, size=1, colorscale='rainbow',showscale=True, 
                                                          colorbar=dict(title="Kp", xanchor="left", x=-0.26, tick0=0, dtick=1, tickvals=[0,1,2,3,4,5,6,7,8,9], ticks="inside") ) ))
    fig.update_layout( width=3000, height=2000, showlegend=False, coloraxis_showscale=False, title="Orbit file:" + OrbitFileName + "<br>" + "Kp values start year is " + str(kp_startYear) + "<br>" + "<b>Kp Indices during " + from_date_str + " - " + to_date_str +  " for Altitudes: "+str(from_Altitude)+"-"+str(to_Altitude)+" km</b>")
    fig.update_xaxes(title="Magnetic Local Time", showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_layout(xaxis = dict(tickmode = 'linear',tick0 = 0,dtick = 2))    
    fig.update_yaxes(title="Magnetic Latitude (deg)", showgrid=True, gridwidth=0.5, gridcolor='gray') 
    fig.update_layout(yaxis = dict(tickmode = 'linear',tick0 = -90,dtick =30), margin=go.layout.Margin(b=150,t=150), width=1000, height=800, showlegend=True)
    fig.update_xaxes(range=[0, 24],  showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(range=[-90, 90],showline=True, linewidth=2, linecolor='gray', mirror=True)
    # draw rectangles to represent the bins on the figure        
    MyColorsIndex = 0
    for B in Bins:
        if B.Altitude_min>=from_Altitude and B.Altitude_max<=to_Altitude:
            BinInfo = "{:3.0f}".format(B.Altitude_min) + "-" + "{:3.0f}".format(B.Altitude_max) + "km " + ": Kp"+ str(B.Kp_min) + "-" + str(B.Kp_max) + ": " 
            if B.CumulativeTime > B.DesirableCumulativeTime: BinInfo += "<b>"
            BinInfo += "{:3.0f}".format(B.CumulativeTime/60) 
            if B.CumulativeTime > B.DesirableCumulativeTime: BinInfo += "</b>"
            BinInfo += "/" + "{:3.0f}".format(B.DesirableCumulativeTime/60)  + "min"
            if B.MLT_min <= B.MLT_max: # ex: 10:00-14:00
                Xmin1 = B.MLT_min
                Xmax1 = B.MLT_max
                Xmin2 = -1
                Xmax2 = -1

            else: # ex: 22:00-02:00
                Xmin1 = B.MLT_min
                Xmax1 = 24
                Xmin2 = 0
                Xmax2 = B.MLT_max
            # check if this rectangle has been already plotted
            FoundFigureIndex = -1 
            for i in range( len(fig.layout['shapes']) ):
                if fig.layout['shapes'][i]["x0"]==Xmin1 and fig.layout['shapes'][i]["y0"]==B.MagLat_min and fig.layout['shapes'][i]["x1"]==Xmax1 and fig.layout['shapes'][i]["y1"]==B.MagLat_max:
                    FoundFigureIndex = i
                    break
            # add info about this bin to the legend text and/or draw a new rectangle
            if FoundFigureIndex >= 0: 
                for i in range( len(fig['data']) ):
                    if fig['data'][i]['name'] is not None  and   B.Description in fig['data'][i]['name']:
                        fig['data'][i]['name'] += BinInfo + "<br>"
            else:
                # draw a rectangle representing the bin
                fig.add_shape(go.layout.Shape( type="rect", xref="x", yref="y", opacity=0.7, layer="above",
                    x0=Xmin1, y0=B.MagLat_min, x1=Xmax1, y1=B.MagLat_max, 
                    line=dict(color=MyColors[MyColorsIndex], width=2,), fillcolor=MyColors[MyColorsIndex], 
                ))
                # add a trace so that a legend about the rectangle is created
                fig.add_trace(go.Scatter( x=[0], y=[0], marker=dict(color=MyColors[MyColorsIndex], size=0, opacity=0), 
                              name="<b>" + B.Description + "<br>" + BinInfo + "<br>" ))
                # draw a 2nd rectangle if necessary for this bin (when for ex it is 22:00-02:00)
                if Xmin1>=0 and Xmin2>=0:
                    fig.add_shape(go.layout.Shape( type="rect", xref="x", yref="y", opacity=0.7, layer="above",
                        x0=Xmin2, y0=B.MagLat_min, x1=Xmax2, y1=B.MagLat_max, 
                        line=dict(color=MyColors[MyColorsIndex], width=2,), fillcolor=MyColors[MyColorsIndex],
                    ))
                MyColorsIndex += 1
                
    # plot it
    fig.update_layout( width=1000, height=1240, legend_orientation="h" )
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig) 

    
    
def PlotOrbit_Heatmap( OrbitFileName ):
    """
    Plots the satellite positions as heatmap using seaborn.JointGrid.
    Altitude is at the Vertical Axis and Magnetic Latitude at the Horizontal Axis.
    The color represents the time spent at each area.
    Args:
        OrbitFileName: the filename of the csv file describing the satellite's orbit
    """
    
    with open( OrbitFileName ) as CSVfile:  # read data from the orbit file
        CSVreader = csv.reader( CSVfile )
        # locate the column numnbers of interest inside the csv file
        CSVheader = next( CSVreader )
        Time_idx     = CSVheader.index( "Epoch(UTCG)"  ) #CSVheader.index( "EpochText" ) "Time (UTCG)"
        Lat_idx      = CSVheader.index( "Lat_GEOD(deg)" ) #CSVheader.index( "Latitude" ) "Lat (deg)"
        Lon_idx      = CSVheader.index( "Lon_GEOD(deg)" ) #CSVheader.index( "Longitude" ) "Lon (deg)"
        Altitude_idx = CSVheader.index( "Height_WGS84 (km)" ) #CSVheader.index( "Height" ) "Alt (km)"
        MagLat_idx   = CSVheader.index( "Magnetic Latitude" )
        MLT_idx      = CSVheader.index( "MLT" )
        X = list()
        Y = list()
        lineNum = 0
        for row in CSVreader: # for each satellite position
            lineNum += 1
            if lineNum > 1:
                if float( row[Altitude_idx] ) < 500: # only low altitudes are useful for this plot
                    X.append( float(row[MagLat_idx]) )
                    Y.append( float(row[Altitude_idx]) )

    # Create a JointGrid seaborn-plot
    joint_kws=dict(gridsize=50) #hex bin size; the higher the gridsize number the smaller the bins
    plot = sns.jointplot(X, Y, kind="hex", cmap='rainbow', joint_kws=joint_kws)
    # style Axes
    sns.set(style="ticks")
    plot.ax_marg_x.set_xlim(-90, 90)
    plot.ax_marg_y.set_ylim(80, 500)
    plot.set_axis_labels(xlabel='Magnetic Latitude (degrees)', ylabel='Altitude (km)')
    # add a colorbar
    cbar_ax = plot.fig.add_axes([.85, .25, .05, .4])  # x, y, width, height
    cbar    = matplt.colorbar(cax=cbar_ax)
    matplt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2) # shrink fig so cbar is visible
    # display
    matplt.show()
    

