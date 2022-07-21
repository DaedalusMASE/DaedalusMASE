"""
This module contains functions for ploting the results of calculation.
"""

import Data as D

import math
import numpy as np
import plotly
import chart_studio.plotly as py 
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from scicolorscales import *

def plotAltProfiles( VariableLongname, Bins, x_axis_min, x_axis_max, MultiplicationFactor=1, Units="", SuperTitle="" ):
    """
    Creates a plot depicting the altitude profiles of the data as calculated for each bin.
    For each Bin the 10th, 25th, 50th, 75ht and 90th percentiles are displayed.
    
    Args:
        VariableLongname: a name of the variable used for the calculations to be displayed on the plot
        Bins: the data structure containing the data. It can be filled by loading a results file with Data.LoadResultsCDF()
        x_axis_min: the minimum value for the horizontal axis
        y_axis_max: the maximum value for the horizontal axis
        MultiplicationFactor: All values will be multiplied by this one before plotting
        Units: to be displayed on the plot.
        SuperTitle: to be displayed on top of the plot.
    """
    x_axis_range=[x_axis_min, x_axis_max]
    
    # alter visibleALTsequence so that the point is displayed in the middle of the sub-bin
    visibleALTsequence = D.ALTsequence.copy()
    for i in range(1, len(visibleALTsequence)-1):
        visibleALTsequence[i] += D.ALT_distance_of_a_bin/2
    visibleALTsequence[0] = D.ALTsequence[0]
    visibleALTsequence[-1] = D.ALTsequence[-1] + D.ALT_distance_of_a_bin
    
    # plot
    Color10 = '#c4dfe6'
    Color25 = '#a1d6e2'
    Color50 = '#1995ad'
    Color75 = '#a1d6e2'
    Color90 = '#c4dfe6'
    
    # construct the column MLT titles #("0-3", "3-6", "6-9", "9-12", "12-15", "15-18", "18-21", "21-24")
    ColumnTitles = list()
    
    for i in range(0, len(D.MLTsequence)):
        MLTfrom = int(D.MLTsequence[i])
        if MLTfrom > 24: MLTfrom -=24
        MLTto = int(D.MLTsequence[i]+D.MLT_duration_of_a_bin)
        if MLTto > 24: MLTto -=24
        ColumnTitles.append( "MLT " + str(MLTfrom) + "-"  + str(MLTto) )
    # define secondary y-axis at the right of the plot
    mySpecs = list()
    for row in range(0, len(D.KPsequence)):
        mySpecs.append( list() )
        for col in range(0, len(D.MLTsequence)):
            mySpecs[row].append( {"secondary_y": True} )

    #make plot
    print( "\n--- The plot contains data from the Bins with Latitude", D.LAT_min, "degrees. ---")
    if D.LAT_min<=65: print("\nWARNING: LOW LATITUDES MAY HAVE ALMOST ZERO VALUES LEADING TO EMPTY ALTITUDE-PROFILES PLOT.\n")
    fig = make_subplots(rows=len(D.KPsequence), cols=len(D.MLTsequence), shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.035, horizontal_spacing=0.02, subplot_titles=ColumnTitles, specs=mySpecs)
    for aKP in D.KPsequence:
        for aMLT in D.MLTsequence:
            #Means = list()
            Percentiles10 = list()
            Percentiles25 = list()
            Percentiles50 = list()            
            Percentiles75 = list()
            Percentiles90 = list()
            hits  = 0
            
            # compute percentiles
            for anALT in D.ALTsequence:
                Percentiles10.append( Bins[aKP, anALT, D.LAT_min, aMLT, "Percentile10"] * MultiplicationFactor )
                Percentiles25.append( Bins[aKP, anALT, D.LAT_min, aMLT, "Percentile25"] * MultiplicationFactor )
                Percentiles50.append( Bins[aKP, anALT, D.LAT_min, aMLT, "Percentile50"] * MultiplicationFactor )
                Percentiles75.append( Bins[aKP, anALT, D.LAT_min, aMLT, "Percentile75"] * MultiplicationFactor )
                Percentiles90.append( Bins[aKP, anALT, D.LAT_min, aMLT, "Percentile90"] * MultiplicationFactor )
            
            fig.add_trace( go.Scatter(x=[0]*len(visibleALTsequence), y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color10, line=dict(color='gray',width=1,), showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
            fig.add_trace( go.Scatter(x=Percentiles10, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color10, line=dict(color='gray',width=1,), showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
            fig.add_trace( go.Scatter(x=Percentiles25, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color25, line=dict(color='gray',width=1,), showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
            fig.add_trace( go.Scatter(x=Percentiles50, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color50, line=dict(color='black',width=2,), showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
            # plot mean
            #fig.add_trace( go.Scatter(x=Means, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor='black', line=dict(color='black',width=1,), showlegend=False), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1 )
            # plot percentiles
            fig.add_trace( go.Scatter(x=Percentiles75, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color75, line=dict(color='gray',width=1,), showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
            fig.add_trace( go.Scatter(x=Percentiles90, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color90, line=dict(color='gray',width=1,), showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1,  )
            # add a trace in order to display secondary y-axis at the right
            fig.add_trace( go.Scatter(x=[-1000], y=[-1000], showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1, secondary_y=True )
            
    # display legends
    fig.add_trace( go.Scatter(name='10th Perc.', x=Percentiles10, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color10, line=dict(color='gray',width=1,), showlegend=True), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
    fig.add_trace( go.Scatter(name='25th Perc.', x=Percentiles25, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color25, line=dict(color='gray',width=1,), showlegend=True), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
    fig.add_trace( go.Scatter(name='50th Perc.', x=Percentiles50, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color50, line=dict(color='black',width=2,), showlegend=True), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
    #fig.add_trace( go.Scatter(name='Mean value', x=Means, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor='#5cc5ef', line=dict(color='black',width=1,), showlegend=True), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1 )            
    fig.add_trace( go.Scatter(name='75th Perc.', x=Percentiles75, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color75, line=dict(color='gray',width=1,), showlegend=True), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
    fig.add_trace( go.Scatter(name='90th Perc.', x=Percentiles90, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color90, line=dict(color='gray',width=1,), showlegend=True), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )

    # update x axis ranges
    for r in range(1, len(D.KPsequence)+1):
        for c in range(1, len(D.MLTsequence)+1):
            fig.update_xaxes( range=x_axis_range, row=r, col=c)
            
    # udate y axis
    for aKP in D.KPsequence:
        fig.update_yaxes( title_text="Altitude (km)", row=D.KPsequence.index(aKP)+1, col=1, side='left', secondary_y=False)
        row_title = "Kp " + str(aKP) + " - "
        if aKP == 0:
            row_title +=  "2"
        elif aKP == 2:
            row_title +=  "4"
        else:
            row_title +=  "9"
        fig.update_yaxes( title_text=row_title, row=D.KPsequence.index(aKP)+1, col=len(D.MLTsequence),  side='right', secondary_y=True, showticklabels=False )
        for aMLT in D.MLTsequence:
            fig.update_yaxes( row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1, secondary_y=True, showticklabels=False )

    fig.update_yaxes( range=[min(D.ALTsequence)-(D.ALTsequence[1]-D.ALTsequence[0]), max(D.ALTsequence)+(D.ALTsequence[1]-D.ALTsequence[0])], dtick=10 ) 
    
    fig.update_layout( title = SuperTitle,
                       width=400+len(D.MLTsequence)*250, height=200+200*len(D.KPsequence), showlegend=True, legend_orientation="h", legend_y=-0.04) 

    
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig) 

    # plot more zoom versions
    '''
    new_x_axis_range = [x * (2/3) for x in x_axis_range]
    fig.update_xaxes( range=new_x_axis_range )
    plotly.offline.iplot(fig) 
    new_x_axis_range = [x * (1/2) for x in x_axis_range]
    fig.update_xaxes( range=new_x_axis_range )
    plotly.offline.iplot(fig) 
    new_x_axis_range = [x * (3/2) for x in x_axis_range]
    fig.update_xaxes( range=new_x_axis_range )
    plotly.offline.iplot(fig) 
    new_x_axis_range = [x * (2.5) for x in x_axis_range]
    fig.update_xaxes( range=new_x_axis_range )
    plotly.offline.iplot(fig) 
    new_x_axis_range = [x * (10) for x in x_axis_range]
    fig.update_xaxes( range=new_x_axis_range )
    plotly.offline.iplot(fig) 
    '''

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

def plotColoredDistributions( VariableName, Bins, x_axis_min, x_axis_max, MultiplicationFactor=1, Units="", SuperTitle="", LogScale=True, ColorMap=lajolla ):    
    """
    Creates color-spread plot with several sub-plots, similar to the Altitude Profiles plot.
    Color indicates how many values lie inside each bin.
    
    Args:
        VariableName: string, the name of the variable to be plotted
        Bins: the data structure containing the data. It can be filled by loading a results file with Data.LoadResultsCDF()
        x_axis_min: the minimum value for the horizontal axis
        y_axis_max: the maximum value for the horizontal axis
        MultiplicationFactor: All values will be multiplied by this one before plotting
        Units: to be displayed on the plot.
        SuperTitle: a title to be added at the top of the plot
        LogScale: if true then the mean values colors will be plotted in logarithmic scale
        ColorMap: the name of the colormap ot use for ploting.  
           Possible values: from http://www.fabiocrameri.ch/colourmaps.php: acton, bamako, batlow, berlin, bilbao, broc, buda, cork, davos, devon, grayC, hawaii, imola, lajolla, lapaz, lisbon, nuuk, oleron , oslo, roma, tofino, tokyo, turku, vik - romaO, brocO, corkO, vikO   
           Possible values: plotly: Blackbody, Bluered, Blues, Earth, Electric, Greens, Greys, Hot, Jet, Picnic, Portland, Rainbow, RdBu, Reds, Viridis, YlGnBu, YlOrRd  
    """
    x_axis_range=[x_axis_min, x_axis_max]
        
 # construct the column MLT titles #("0-3", "3-6", "6-9", "9-12", "12-15", "15-18", "18-21", "21-24")
    ColumnTitles = list()    
    for i in range(0, len(D.MLTsequence)):
        MLTfrom = int(D.MLTsequence[i])
        if MLTfrom > 24: MLTfrom -=24
        MLTto = int(D.MLTsequence[i]+D.MLT_duration_of_a_bin)
        if MLTto > 24: MLTto -=24
        ColumnTitles.append( "<b>MLT " + str(MLTfrom) + "-"  + str(MLTto) + "</b>" )
    # define secondary y-axis at the right of the plot
    mySpecs = list()
    for row in range(0, len(D.KPsequence)):
        mySpecs.append( list() )
        for col in range(0, len(D.MLTsequence)):
            mySpecs[row].append( {"secondary_y": True} )
            
    #make plot
    HitsStr = ""
    fig = make_subplots(rows=len(D.KPsequence), cols=len(D.MLTsequence), shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.035, horizontal_spacing=0.02, subplot_titles=ColumnTitles, specs=mySpecs)
    
    
    # bundle data, min and max values
    localHits_min = allHits_min = allHits_logscale_min = 999999
    localHits_max = allHits_max = allHits_logscale_max = -99999
    for aKP in D.KPsequence:
        for aMLT in D.MLTsequence:
            Hits = None
            for anALT in D.ALTsequence:            
            
                if Hits is None:
                    Hits = [ Bins[(aKP, anALT, D.LAT_min, aMLT, "Distribution")] ]
                else:
                    Hits = np.append(Hits, [Bins[(aKP, anALT, D.LAT_min, aMLT, "Distribution")]] , axis=0)
            
            
            localHits_min = np.min( Hits )
            localHits_max = np.max( Hits )
            if localHits_min < allHits_min:
                allHits_min = localHits_min
            if localHits_max > allHits_max:
                allHits_max = localHits_max
            
            # compute logScale
            Hits_logscale = np.zeros( Hits.shape )
            for i in range(0, len(Hits)):
                for j in range(0, len(Hits[0])):
                    if Hits[i,j] > 0:
                        Hits_logscale[i,j] = np.log10(Hits[i,j])
                    else:
                        Hits_logscale[i,j] = None
            
            localHits_logscale_min = np.nanmin( Hits_logscale )
            localHits_logscale_max = np.nanmax( Hits_logscale )            
            if localHits_logscale_min < allHits_logscale_min:
                allHits_logscale_min = localHits_logscale_min                
            if localHits_logscale_max > allHits_logscale_min:
                allHits_logscale_min = localHits_logscale_max
            
            print("Min:", localHits_min, "Max:", localHits_max, " Log Min:", localHits_logscale_min, "Log Max:", localHits_logscale_max)
            
            # plot heatmap
            if LogScale:
                fig.add_trace( go.Heatmap(z=Hits_logscale, x=np.linspace(0,5,100), y=D.ALTsequence, zsmooth=False, showlegend=False, coloraxis="coloraxis1",zmin=localHits_logscale_min, zmax=localHits_logscale_max), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1,  )
            else:
                fig.add_trace( go.Heatmap(z=Hits, x=np.linspace(0,5,100), y=D.ALTsequence, zsmooth=False, showlegend=False, coloraxis="coloraxis1", zmin=localHits_min, zmax=localHits_max),row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1,  )

    #print("allHits_logscale_min", "allHits_logscale_max", "allHits_min", "allHits_max" )
    #print(allHits_logscale_min, allHits_logscale_max, allHits_min, allHits_max )
    
    fig.update_layout(coloraxis=dict(colorscale=ColorMap), showlegend=False) #fig.update_traces(zmin=0.07687949e-02, zmax=3.07687949e-01, selector=dict(type="heatmap"))
    # display titles
    fig.update_yaxes( title_text="<b>" + "Kp 0-2" + "</b>" + "<br><br>" + "Altitude (km)", row=1, col=1, side='left', secondary_y=False)
    fig.update_yaxes( title_text="<b>" + "Kp 2-4" + "</b>" + "<br><br>" + "Altitude (km)", row=2, col=1, side='left', secondary_y=False)
    fig.update_yaxes( title_text="<b>" + "Kp 4-9" + "</b>" + "<br><br>" + "Altitude (km)", row=3, col=1, side='left', secondary_y=False)
    for anAlt in D.ALTsequence: fig.update_xaxes( title_text=VariableName + " (" +  Units +")", row=len(D.KPsequence), col=D.ALTsequence.index(anAlt)+1)
        
    # Set the same min/max for all figures
    if LogScale:
        fig.update_traces(zmin=allHits_min, zmax=allHits_max)
    else:
        fig.update_traces(zmin=allHits_logscale_min, zmax=allHits_logscale_max)
    # tick values at the color bar
    if LogScale:
        my_Tickvals    = np.linspace(allHits_min, allHits_max, 5, endpoint=True)
        my_logTickvals = list()
        my_Ticktexts   = list()
        for t in range( 0, len(my_Tickvals) ):
            try:
                my_logTickvals.append( math.log10(my_Tickvals[t]) )
                my_Ticktexts.append( "{:.3e}".format(my_Tickvals[t]) )                
            except Exception as e:
                #print(e)
                pass
        fig.update_layout(coloraxis_colorbar=dict( title="Log scale",  tickvals=my_logTickvals,  ticktext=my_Ticktexts, ))
    
    # update x axis ranges
    for r in range(1, len(D.KPsequence)+1):
        for c in range(1, len(D.MLTsequence)+1):
            fig.update_xaxes( range=x_axis_range, row=r, col=c)

    # udate y axis
    for aKP in D.KPsequence:
        fig.update_yaxes( title_text="Altitude (km)", row=D.KPsequence.index(aKP)+1, col=1, side='left', secondary_y=False)
        row_title = "Kp " + str(aKP) + " - "
        if aKP == 0:
            row_title +=  "2"
        elif aKP == 2:
            row_title +=  "4"
        else:
            row_title +=  "9"
        fig.update_yaxes( title_text=row_title, row=D.KPsequence.index(aKP)+1, col=len(D.MLTsequence),  side='right', secondary_y=True, showticklabels=False )
        for aMLT in D.MLTsequence:
            fig.update_yaxes( row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1, secondary_y=True, showticklabels=False )
    
    fig.update_yaxes( range=[min(D.ALTsequence)-(D.ALTsequence[1]-D.ALTsequence[0]), max(D.ALTsequence)+(D.ALTsequence[1]-D.ALTsequence[0])], dtick=10 ) 
            
    # font
    fig.update_layout(font_family="Helvetica",)
    # Set title
    mainTitle = SuperTitle
    mainTitle += "<br>Distribution: Color indicates how many values lie inside each bin."
    fig.update_layout( title = mainTitle, width=400+len(D.MLTsequence)*180, height=150+180*len(D.KPsequence), showlegend=True, legend_orientation="h", legend_y=-0.04) 
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig)
        
    # resize the Altitude range to its initial values
    #D.ALTsequence = oldALTsequence


    
    
    