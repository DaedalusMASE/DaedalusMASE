
"""
This module contains functions which plot the data contained at the Bins.
These functions should be called after the results of a calculation have been loaded from a netcdf result-file.
"""

# python imports
import plotly
import chart_studio.plotly as py 
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from scicolorscales import *
import matplotlib.cm
import matplotlib.pyplot as matplt
import math
import random
from scipy.stats import ranksums
from scipy.stats import mannwhitneyu
# module imports
from data import *

# colors used at plotting
MyColors = ["#217ca3", "#e29930", "#919636", "#af1c1c", "#e7552c", "#1b4b5a", "#e4535e", "#aebd38", "#ffbb00", "#2c7873"]
def Hex_to_RGB(  HexColor ): # "#e29930" -->
    RGB = tuple(int(HexColor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    return str(RGB).strip('(').strip(')').strip()




def plot_variable( RegionName, Variable_toPlot, Units_of_Variable="", Variable_toPlot_longname="" ):
    """
        Creates the following plots based on the values of the chosen Variable:
            1. Variable vs Magnetic Latitude. The Bins' ranges and mean values are also displayed
            2. Variable vs Magnetic Local Time. The Bins' ranges and mean values are also displayed
            3. Variable vs Altitude. The Bins' ranges and mean values are also displayed
            4. Altitude vs Magnetic Latitude. Scatter plot colored according to the values of the Variable
            
        Args:
            RegionName (string): this region's Bins will be displayed at the plot. They are the Bins whose ID starts from RegionName.  
            Variable_toPlot (string): the name of the Variable to be plotted. See at the start of data.py for available names.  
            Units_of_Variable (string): the units that will be displayed on the plot. If empty, then default is automatically chosen.  
            Variable_toPlot_longname (string): A longer name of the Variable in order to be displayed at the plots.  
    """
    if len(Units_of_Variable)==0:
        if Variable_toPlot == "Ohmic":
            Units_of_Variable = "W/m^3"
        elif Variable_toPlot == "DEN":
            Units_of_Variable = "g/cm^3"    
        elif Variable_toPlot == "SIGMA_PED" or Variable_toPlot == "SIGMA_HAL":
            Units_of_Variable = "S/m"
        elif Variable_toPlot == "Convection_heating" or Variable_toPlot == "Wind_heating":
            Units_of_Variable = "W/m^3"           
        elif Variable_toPlot == "EEX" or Variable_toPlot == "EEY":
            Units_of_Variable = "V/m"      
        else:
            Units_of_Variable = "?" 
    
    if len(Variable_toPlot_longname)==0: Variable_toPlot_longname=Variable_toPlot
    
    # choose which bins we are going to work with
    if "(" in RegionName:
        RegionName = RegionName[ RegionName.find('(')+1 : RegionName.rfind(')') ]
    else:
        RegionName = RegionName
    BinsIncludedAtPlot = list()
    for B in Bins:
        if B.ID.startswith(RegionName): BinsIncludedAtPlot.append( B )

    # remember the Kp ranges of these bins. Each Kp-range will have its own sub-plot
    TMP_KpRanges = list()
    for B in BinsIncludedAtPlot:
        if [B.Kp_min, B.Kp_max] not in TMP_KpRanges: TMP_KpRanges.append( [B.Kp_min, B.Kp_max] )  
            
    # --- init various plotting parameters ---
    max_num_of_points = 10000
    plot_step = int(  len(all_JH_values) / max_num_of_points  )
    if plot_step <= 0: plot_step = 1
    n = max_num_of_points
    if n > len(all_JH_values):  n = len(all_JH_values)
    print( "I will plot", n, "out of", len(all_JH_values), "points (1 per", plot_step, ")")
    TMP_JH_values       = list()
    TMP_MagLat_values   = list()
    TMP_MLT_values      = list()
    TMP_Altitude_values = list()
    for idx in range( 0, len(all_JH_values) ):
        if int(idx / 1) % int(plot_step) == 0: 
            TMP_JH_values.append( all_JH_values[idx] )
            TMP_MagLat_values.append( all_MagLat_values[idx] )
            TMP_MLT_values.append( all_MLT_values[idx] )
            TMP_Altitude_values.append( all_Altitude_values[idx] )
    
    # handle MLT ranges like 22:00-02:00
    MLT_min_toPlot = BinsIncludedAtPlot[0].MLT_min
    MLT_max_toPlot = BinsIncludedAtPlot[0].MLT_max
    if BinsIncludedAtPlot[0].MLT_min > BinsIncludedAtPlot[0].MLT_max:
        MLT_max_toPlot += 24
        for i in range(0, len(TMP_MLT_values)):
            if TMP_MLT_values[i] < BinsIncludedAtPlot[0].MLT_min: TMP_MLT_values[i] += 24
    # define altitude range for X-axis
    Altitude_max_toPlot = max(all_Altitude_values)
    if Altitude_max_toPlot < 140: Altitude_max_toPlot = 140
                
    # define max JH value to be plotted
    if Variable_toPlot == "Ohmic" or Variable_toPlot == "Convection_heating":
        JHmax = 1.4e-7
        if RegionName.startswith( "SQ" ): JHmax = max(all_JH_values)
    else:
        JHmax = max(all_JH_values)
        
    if len(all_MagLat_values) > 0:
        print( "Plotting ", len(TMP_MagLat_values), "points" )
        MyColorsIndex = 0
        fig = go.Figure()        
        fig.add_trace( go.Scatter(name=Variable_toPlot_longname, x=TMP_MagLat_values, y=TMP_JH_values, mode='markers', marker_size=2) )
        BinAnnotations = list()
        prevKpMin = -1
        BinIdx = 0
        for B in BinsIncludedAtPlot:
            if len(B.JH_values) > 0:
                # choose color for mean line
                if prevKpMin >= 0 and prevKpMin != B.Kp_min:
                    MyColorsIndex += 1
                    if MyColorsIndex>len(MyColors)-1: MyColorsIndex = 0
                prevKpMin = B.Kp_min                        
                # add visuals for the mean line
                fig.add_shape( type="line", x0=B.MagLat_min, y0=B.JH_mean,     x1=B.MagLat_max, y1=B.JH_mean,     line=dict( color=MyColors[MyColorsIndex], width=2, ), )    
                print(">>", B.MagLat_min, B.MagLat_max, "   :   ", B.JH_mean)
                # add info as legend for this bin
                fig.add_trace( go.Scatter(name=B.ID + ":  " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + "  <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b>" + "  Mean=" + "{:.3e}".format(B.JH_mean) + "  " + "Variance=" + "{:.3e}".format(B.JH_variance) + "  St.Deviation=" + "{:.3e}".format(B.JH_variance**(1/2)) , x=[-1], y=[-1], mode='markers', marker_size=1, marker_color=MyColors[MyColorsIndex]) )
                # add bin name above the mean line
                BinAnnotations.append( dict( x=B.MagLat_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.MagLat_max-B.MagLat_min)*3/4, y=B.JH_mean, xref="x", yref="y", text=B.ID, showarrow=False, yshift=8, font=dict(color=MyColors[MyColorsIndex])) )
                # add visuals for standard deviation
                fig.add_shape( type="line", x0=B.MagLat_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.MagLat_max-B.MagLat_min)*7/8, y0=B.JH_mean+(B.JH_variance)**(1/2)/2,     x1=B.MagLat_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.MagLat_max-B.MagLat_min)*7/8, y1=B.JH_mean-(B.JH_variance)**(1/2)/2,     line=dict( color=MyColors[MyColorsIndex], width=1, ), ) 
                #
                BinIdx += 1
        fig.update_layout( annotations=BinAnnotations )
        fig.update_layout( title=Variable_toPlot_longname+" vs Magnetic Latitude - " + getBinDescription(RegionName), 
                           width=1000, height=1300, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
        fig.update_xaxes(range=[min(all_MagLat_values), max(all_MagLat_values)], title="Magnetic Latitude (degrees)")
        fig.update_yaxes(range=[min(all_JH_values), JHmax], title=Variable_toPlot+" ("+Units_of_Variable+")", showexponent = 'all', exponentformat = 'e')
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig)
    else:
        pass
        #print( "There are no points for MagLat plot" )                

    if len(all_MLT_values) > 0:
        MyColorsIndex = 0
        fig = go.Figure()
        print( "Plotting ", len(TMP_MLT_values), "points" )
        fig.add_trace( go.Scatter(name=Variable_toPlot_longname, x=TMP_MLT_values, y=TMP_JH_values, mode='markers', marker_size=2) )
        prevKpMin = -1
        BinAnnotations = list()
        BinIdx = 0
        for B in BinsIncludedAtPlot:
            if len(B.JH_values) > 0:
                # choose color for mean line
                if prevKpMin >= 0 and prevKpMin != B.Kp_min:
                    MyColorsIndex += 1
                    if MyColorsIndex>len(MyColors)-1: MyColorsIndex = 0
                prevKpMin = B.Kp_min                        
                # add visuals for the mean line             
                fig.add_shape( type="line", x0=MLT_min_toPlot, y0=B.JH_mean,     x1=MLT_max_toPlot, y1=B.JH_mean,     line=dict( color=MyColors[MyColorsIndex], width=2, ), )    
                # add info as legend for this bin
                fig.add_trace( go.Scatter(name=B.ID + ":  " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + "  <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b>" + "  Mean=" + "{:.3e}".format(B.JH_mean) + "  " + "Variance=" + "{:.3e}".format(B.JH_variance) + "St.Deviation=" + "{:.3e}".format(B.JH_variance**(1/2)), x=[-1], y=[-1], mode='markers', marker_size=1, marker_color=MyColors[MyColorsIndex]) )
                # add bin name above the mean line
                BinAnnotations.append( dict( x=MLT_min_toPlot+((BinIdx+1)/len(BinsIncludedAtPlot))*(MLT_max_toPlot-MLT_min_toPlot)*3/4, y=B.JH_mean, xref="x", yref="y", text=B.ID, showarrow=False, yshift=8, font=dict(color=MyColors[MyColorsIndex])) )
                # add visuals for standard deviation
                fig.add_shape( type="line", x0=MLT_min_toPlot+((BinIdx+1)/len(BinsIncludedAtPlot))*(MLT_max_toPlot-MLT_min_toPlot)*7/8, y0=B.JH_mean+(B.JH_variance)**(1/2)/2,     x1=MLT_min_toPlot+((BinIdx+1)/len(BinsIncludedAtPlot))*(MLT_max_toPlot-MLT_min_toPlot)*7/8, y1=B.JH_mean-(B.JH_variance)**(1/2)/2,     line=dict( color=MyColors[MyColorsIndex], width=1, ), )
                #
                BinIdx += 1
        fig.update_layout( annotations=BinAnnotations )
        fig.update_layout( title=Variable_toPlot_longname+" vs Magnetic Local Time - " + getBinDescription(RegionName), 
                           width=1000, height=1300, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
        fig.update_xaxes(range=[MLT_min_toPlot, MLT_max_toPlot], title="Magnetic Local Time (hours)") #fig.update_xaxes(range=[min(TMP_MLT_values), max(TMP_MLT_values)], title="Magnetic Local Time (hours)")
        fig.update_yaxes(range=[min(all_JH_values), JHmax], title=Variable_toPlot+" ("+Units_of_Variable+")", showexponent = 'all', exponentformat = 'e')
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig)
    else:
        pass
        #print( "There are no points for MLT plot" )        
    
    if len(TMP_Altitude_values) > 0:
        MyColorsIndex = 0
        fig = go.Figure()
        print( "Plotting ", len(TMP_Altitude_values), "points" )
        fig.add_trace( go.Scatter(name=Variable_toPlot_longname, x=TMP_Altitude_values, y=TMP_JH_values, mode='markers', marker_size=2) )
        prevKpMin = -1
        BinAnnotations = list()
        BinIdx = 0
        for B in BinsIncludedAtPlot:
            if len(B.JH_values) > 0:
                # choose color for mean line
                if prevKpMin >= 0 and prevKpMin != B.Kp_min:
                    MyColorsIndex += 1
                    if MyColorsIndex>len(MyColors)-1: MyColorsIndex = 0
                prevKpMin = B.Kp_min                        
                # add visuals for the mean line
                fig.add_shape( type="line", x0=B.Altitude_min, y0=B.JH_mean,     x1=B.Altitude_max, y1=B.JH_mean,     line=dict( color=MyColors[MyColorsIndex], width=2, ), )    
                # add info as legend for this bin
                fig.add_trace( go.Scatter(name=B.ID + ":  " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + "  <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b>" + "  Mean=" + "{:.3e}".format(B.JH_mean) + "  " + "Variance=" + "{:.3e}".format(B.JH_variance) + "  St.Deviation=" + "{:.3e}".format(B.JH_variance**(1/2)), x=[-1], y=[-1], mode='markers', marker_size=1, marker_color=MyColors[MyColorsIndex]) )
                # add bin name above the mean line
                BinAnnotations.append( dict( x=B.Altitude_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.Altitude_max-B.Altitude_min)*3/4, y=B.JH_mean, xref="x", yref="y", text=B.ID, showarrow=False, yshift=8, font=dict(color=MyColors[MyColorsIndex])) )
                # add visuals for standard deviation
                fig.add_shape( type="line", x0=B.Altitude_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.Altitude_max-B.Altitude_min)*7/8, y0=B.JH_mean+(B.JH_variance)**(1/2)/2,     x1=B.Altitude_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.Altitude_max-B.Altitude_min)*7/8, y1=B.JH_mean-(B.JH_variance)**(1/2)/2,     line=dict( color=MyColors[MyColorsIndex], width=1, ), )
                #
                BinIdx += 1
        fig.update_layout( annotations=BinAnnotations )
        fig.update_layout( title=Variable_toPlot_longname+" vs Altitude - " + getBinDescription(RegionName), 
                           width=1000, height=1300, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
        fig.update_xaxes(range=[115, Altitude_max_toPlot], title="Altitude (km)")
        fig.update_yaxes(range=[min(all_JH_values), JHmax], title=Variable_toPlot+" ("+Units_of_Variable+")", showexponent = 'all', exponentformat = 'e')
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig)
    else:
        pass
        #print( "There are no points for Altitude plot" )
    
    
    if len(TMP_JH_values) > 0:
        MyColorsIndex = 0
        fig = go.Figure()
        print( "Plotting ", len(TMP_JH_values), "points" )
        
        colorMean = 0
        for n in TMP_JH_values: colorMean += n
        colorMean = float( colorMean / len(TMP_JH_values) )
        colorMin = float(colorMean / 10)
        colorMax = float(colorMean * 10)
        fig.add_trace( go.Scatter(name=Variable_toPlot_longname, x=TMP_MagLat_values, y=TMP_Altitude_values, mode='markers', 
                       marker=dict( size=2, color=TMP_JH_values, colorscale="Jet", cmin=colorMin, cmax=colorMax, colorbar=dict(title=Variable_toPlot+" ("+Units_of_Variable+")" )) ) )
        for B in BinsIncludedAtPlot:
            if len(B.JH_values) > 0:
                #fig.add_shape( type="line", x0=B.MagLat_min, y0=B.JH_mean,     x1=B.MagLat_max, y1=B.JH_mean,     line=dict( color=MyColors[MyColorsIndex], width=1, ), )    
                #fig.add_trace( go.Scatter(name="Bin Mean: " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + " <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b> Variance=" + str(B.JH_variance), x=[-1], y=[-1], mode='markers', marker_size=1, marker_color=MyColors[MyColorsIndex]) )
                MyColorsIndex += 1
                if MyColorsIndex>len(MyColors)-1: MyColorsIndex = 0
        fig.update_layout( title="Altitude vs Magnetic Latitude - " + RegionName, 
                           width=1000, height=1300, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
        fig.update_xaxes(range=[min(all_MagLat_values), max(all_MagLat_values)], title="Magnetic Latitude (degrees)" )
        fig.update_yaxes(range=[min(all_Altitude_values), max(all_Altitude_values)], title="Altitude(km)")
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig)
    else:
        pass
        #print( "There are no points for Altitude-MagLat plot" )                

    


def plot_variable_KpSeparated( RegionName, Variable_toPlot, Units_of_Variable="", Variable_toPlot_longname="" ):
    """
        Creates the following plots based on the values of the chosen Variable:
            1. Variable vs Magnetic Latitude. The Bins' ranges and mean values are also displayed
            2. Variable vs Magnetic Local Time. The Bins' ranges and mean values are also displayed
            3. Variable vs Altitude. The Bins' ranges and mean values are also displayed
        Each plot is separated to two subplots according to Kp value: 0-3 and 3-9. 
        
        Args:
            RegionName (string): this region's Bins will be displayed at the plot. They are the Bins whose ID starts from RegionName.  
            Variable_toPlot (string): the name of the Variable to be plotted. See at the start of data.py for available names.  
            Units_of_Variable (string): the units that will be displayed on the plot.  
            Variable_toPlot_longname (string): A longer name of the Variable in order to be displayed at the plots.  
    """
    if len(Units_of_Variable)==0:
        if Variable_toPlot == "Ohmic":
            Units_of_Variable = "W/m^3"
        elif Variable_toPlot == "DEN":
            Units_of_Variable = "g/cm^3"    
        elif Variable_toPlot == "SIGMA_PED" or Variable_toPlot == "SIGMA_HAL":
            Units_of_Variable = "S/m"
        elif Variable_toPlot == "Convection_heating" or Variable_toPlot == "Wind_heating":
            Units_of_Variable = "W/m^3"           
        elif Variable_toPlot == "EEX" or Variable_toPlot == "EEY":
            Units_of_Variable = "V/m"      
        else:
            Units_of_Variable = "?" 
    
    if len(Variable_toPlot_longname)==0: Variable_toPlot_longname=Variable_toPlot

    # choose which bins we are going to work with
    if "(" in RegionName:
        RegionName = RegionName[ RegionName.find('(')+1 : RegionName.rfind(')') ]
    else:
        RegionName = RegionName
    BinsIncludedAtPlot = list()
    for B in Bins:
        if B.ID.startswith(RegionName): BinsIncludedAtPlot.append( B )          

    # --- init various plotting parameters ---
    # handle MLT ranges like 22:00-02:00
    MLT_min_toPlot = BinsIncludedAtPlot[0].MLT_min
    MLT_max_toPlot = BinsIncludedAtPlot[0].MLT_max
    if BinsIncludedAtPlot[0].MLT_min > BinsIncludedAtPlot[0].MLT_max:
        MLT_max_toPlot += 24
        for i in range(0, len(all_MLT_values)):
            if all_MLT_values[i] < BinsIncludedAtPlot[0].MLT_min: all_MLT_values[i] += 24
        for B in BinsIncludedAtPlot:
            for i in range(0, len(B.MLT_values)):
                if B.MLT_values[i] < BinsIncludedAtPlot[0].MLT_min: B.MLT_values[i] += 24
    # define altitude range for X-axis
    Altitude_max_toPlot = max(all_Altitude_values)
    if Altitude_max_toPlot < 140: Altitude_max_toPlot = 140
    # define max JH value to be plotted
    if Variable_toPlot == "Ohmic" or Variable_toPlot == "Convection_heating":
        JHmax = 1.4e-7
        if RegionName.startswith( "SQ" ): JHmax = max(all_JH_values)
    else:
        JHmax = max(all_JH_values)

    # CONSTRUCT DATA per Kp-range
    # remember the Kp ranges of the plot's bins. Each Kp-range will have its own sub-plot
    All_KpRanges = list()
    for B in BinsIncludedAtPlot:
        if [B.Kp_min, B.Kp_max] not in All_KpRanges: 
            All_KpRanges.append( [B.Kp_min, B.Kp_max] )  
    # group data according to Kp-range
    JH_values_perKp       = list() # 2d-list: one row for each Kp-range
    MagLat_values_perKp   = list() # 2d-list: one row for each Kp-range
    MLT_values_perKp      = list() # 2d-list: one row for each Kp-range
    Altitude_values_perKp = list() # 2d-list: one row for each Kp-range
    Time_values_perKp     = list()
    for i in range(0, len(All_KpRanges)): 
        JH_values_perKp.append( list() )
        MagLat_values_perKp.append( list() )
        MLT_values_perKp.append( list() )
        Altitude_values_perKp.append( list() )
        Time_values_perKp.append( list() )
        for B in BinsIncludedAtPlot:
            if B.Kp_min==All_KpRanges[i][0] and B.Kp_max==All_KpRanges[i][1]: 
                JH_values_perKp[i]       += B.JH_values
                MagLat_values_perKp[i]   += B.MagLat_values
                MLT_values_perKp[i]      += B.MLT_values
                Altitude_values_perKp[i] += B.Altitude_values
                Time_values_perKp[i]     += B.Time_values
    # make the data set smaller so that it can be plotted
    max_num_of_points = 80000
    print( "\n" ) 
    for i in range(0, len(All_KpRanges)):
        plot_step = int(  len(JH_values_perKp[i]) / max_num_of_points  )
        n = max_num_of_points 
        if n > len(JH_values_perKp[i]):  n = len(JH_values_perKp[i])
        print( "I will plot", n, "out of", len(JH_values_perKp[i]), "points (1 per", plot_step, ")" + " for " + str(All_KpRanges[i][0]) + "<Kp<" + str(All_KpRanges[i][1]) )
        if plot_step > 0:
            #JH_values_perKp[i]       = JH_values_perKp[i][0::plot_step]
            #MagLat_values_perKp[i]   = MagLat_values_perKp[i][0::plot_step]
            #MLT_values_perKp[i]      = MLT_values_perKp[i][0::plot_step]
            #Altitude_values_perKp[i] = Altitude_values_perKp[i][0::plot_step]
            TMP_JH_values       = list()
            TMP_MagLat_values   = list()
            TMP_MLT_values      = list()
            TMP_Altitude_values = list()
            TMP_Time_values     = list()
            for idx in range( 0, len(JH_values_perKp[i]) ):
                if int(idx / 1) % int(plot_step) == 0: 
                    TMP_JH_values.append( JH_values_perKp[i][idx] )
                    TMP_MagLat_values.append( MagLat_values_perKp[i][idx] )
                    TMP_MLT_values.append( MLT_values_perKp[i][idx] )
                    TMP_Altitude_values.append( Altitude_values_perKp[i][idx] )
                    try:
                        TMP_Time_values.append( Time_values_perKp[i][idx] )
                    except:
                        pass
            JH_values_perKp[i]       = TMP_JH_values
            MagLat_values_perKp[i]   = TMP_MagLat_values
            MLT_values_perKp[i]      = TMP_MLT_values
            Altitude_values_perKp[i] = TMP_Altitude_values
            Time_values_perKp[i] = TMP_Time_values
            
    # PLOT
    if len(all_MagLat_values) > 0:
        fig = make_subplots(rows=len(All_KpRanges), cols=1, shared_xaxes=False, vertical_spacing=0.05)
        for i in range(0, len(All_KpRanges)):
            fig.append_trace( go.Scatter(name=Variable_toPlot_longname, x=MagLat_values_perKp[i], y=JH_values_perKp[i], mode='markers', marker_size=2, marker_color=MyColors[i]), row=i+1, col=1 )
        #
        BinAnnotations = list()
        FigureShapes = list()
        MyColorsIndex = 0
        BinIdx = 0
        for B in BinsIncludedAtPlot:
            if len(B.JH_values) > 0:
                # choose which sub-plot will host this Bin's data
                SubPlotIdx = 1
                for i in range(0, len(All_KpRanges)):
                    if B.Kp_min==All_KpRanges[i][0] and B.Kp_max==All_KpRanges[i][1]: SubPlotIdx = i+1
                # choose color for mean line
                MyColorsIndex = SubPlotIdx - 1
                # add visuals for the mean line
                FigureShapes.append( dict(type="line", x0=B.MagLat_min, y0=B.JH_mean,     x1=B.MagLat_max, y1=B.JH_mean,   line=dict( color=MyColors[MyColorsIndex], width=2, ),  xref= 'x'+str(SubPlotIdx), yref= 'y'+str(SubPlotIdx))  )  #fig.append_shape( dict(type="line", x0=B.MagLat_min, y0=B.JH_mean,     x1=B.MagLat_max, y1=B.JH_mean,   line=dict( color=MyColors[MyColorsIndex], width=2, )), row=SubPlotIdx, col=1 )    
                # add info as legend for this bin
                fig.append_trace( go.Scatter(name=B.ID + ":  " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + "  <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b>" + "  Mean=" + "{:.3e}".format(B.JH_mean) + "  " + "Variance=" + "{:.3e}".format(B.JH_variance) + "  St.Deviation=" + "{:.3e}".format(B.JH_variance**(1/2)), x=[-1], y=[-1], mode='markers', marker_size=1, marker_color=MyColors[MyColorsIndex]), row=SubPlotIdx, col=1 )
                # add bin name above the mean line
                BinAnnotations.append( dict( x=B.MagLat_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.MagLat_max-B.MagLat_min)*3/4, y=B.JH_mean, text=B.ID, showarrow=False, yshift=8, font=dict(color=MyColors[MyColorsIndex]), xref='x1', yref='y'+str(SubPlotIdx) ) )
                # add visuals for standard deviation
                FigureShapes.append( dict(type="line", x0=B.MagLat_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.MagLat_max-B.MagLat_min)*7/8, y0=B.JH_mean+(B.JH_variance)**(1/2)/2,     x1=B.MagLat_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.MagLat_max-B.MagLat_min)*7/8, y1=B.JH_mean-(B.JH_variance)**(1/2)/2,     line=dict( color=MyColors[MyColorsIndex], width=2, ), xref= 'x1', yref='y'+str(SubPlotIdx) )  )
                #
                BinIdx += 1
        fig.update_layout( annotations=BinAnnotations )
        fig.update_layout(shapes=FigureShapes)
        fig.update_layout( title=Variable_toPlot_longname+" vs Magnetic Latitude - " + getBinDescription(RegionName), 
                           width=1000, height=1500, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
        for i in range(0, len(All_KpRanges)):
            fig.update_xaxes(range=[min(all_MagLat_values), max(all_MagLat_values)], title="Magnetic Latitude (degrees) for " + str(All_KpRanges[i][0]) + "<Kp<"+  str(All_KpRanges[i][1]), row=i+1, col=1 )
        fig.update_yaxes(range=[min(all_JH_values), JHmax], title=Variable_toPlot+" ("+Units_of_Variable+")", showexponent = 'all', exponentformat = 'e')
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig)
    else:
        print( "There are no points for MagLat per-Kp-range plot" )                
    
    ##
    if len(all_MLT_values) > 0:
        fig = make_subplots(rows=len(All_KpRanges), cols=1, shared_xaxes=False, vertical_spacing=0.05)
        for i in range(0, len(All_KpRanges)):
            fig.append_trace( go.Scatter(name=Variable_toPlot_longname, x=MLT_values_perKp[i], y=JH_values_perKp[i], mode='markers', marker_size=2, marker_color=MyColors[i]), row=i+1, col=1 )
        #
        BinAnnotations = list()
        FigureShapes = list()
        MyColorsIndex = 0
        BinIdx = 0
        for B in BinsIncludedAtPlot:
            if len(B.JH_values) > 0:
                # choose which sub-plot will host this Bin's data
                SubPlotIdx = 1
                for i in range(0, len(All_KpRanges)):
                    if B.Kp_min==All_KpRanges[i][0] and B.Kp_max==All_KpRanges[i][1]: SubPlotIdx = i+1
                    #fig.update_xaxes(range=[min(MLT_values_perKp), max(MLT_values_perKp)], title="Magnetic Local Time (hours) for " + str(All_KpRanges[i][0]) + "<Kp<"+  str(All_KpRanges[i][1]), row=SubPlotIdx, col=1 )                
                # choose color for mean line
                MyColorsIndex = SubPlotIdx - 1
                # add visuals for the mean line             
                FigureShapes.append( dict(type="line", x0=MLT_min_toPlot, y0=B.JH_mean,     x1=MLT_max_toPlot, y1=B.JH_mean,   line=dict( color=MyColors[MyColorsIndex], width=2, ),  xref= 'x'+str(SubPlotIdx), yref= 'y'+str(SubPlotIdx))  ) 
                # add info as legend for this bin
                fig.append_trace( go.Scatter(name=B.ID + ":  " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + "  <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b>" + "  Mean=" + "{:.3e}".format(B.JH_mean) + "  " + "Variance=" + "{:.3e}".format(B.JH_variance) + "  St.Deviation=" + "{:.3e}".format(B.JH_variance**(1/2)), x=[-1], y=[-1], mode='markers', marker_size=1, marker_color=MyColors[MyColorsIndex]), row=SubPlotIdx, col=1 )
                # add bin name above the mean line
                BinAnnotations.append(          dict( x=MLT_min_toPlot+((BinIdx+1)/len(BinsIncludedAtPlot))*(MLT_max_toPlot-MLT_min_toPlot)*3/4, y=B.JH_mean, text=B.ID, showarrow=False, yshift=8, font=dict(color=MyColors[MyColorsIndex]), xref='x1', yref='y'+str(SubPlotIdx)) )
                FigureShapes.append( dict(type="line", x0=MLT_min_toPlot+((BinIdx+1)/len(BinsIncludedAtPlot))*(MLT_max_toPlot-MLT_min_toPlot)*7/8, y0=B.JH_mean+(B.JH_variance)**(1/2)/2,     x1=MLT_min_toPlot+((BinIdx+1)/len(BinsIncludedAtPlot))*(MLT_max_toPlot-MLT_min_toPlot)*7/8, y1=B.JH_mean-(B.JH_variance)**(1/2)/2,     line=dict( color=MyColors[MyColorsIndex], width=2, ), xref= 'x1', yref= 'y'+str(SubPlotIdx) )  )
                #
                BinIdx += 1
        fig.update_layout( annotations=BinAnnotations )
        fig.update_layout( shapes=FigureShapes )
        fig.update_layout( title=Variable_toPlot_longname+" vs Magnetic Local Time - " + getBinDescription(RegionName), 
                           width=1000, height=1500, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
        #fig.update_xaxes(range=[MLT_min_toPlot, MLT_max_toPlot], title="Magnetic Local Time (hours)")
        for i in range(0, len(All_KpRanges)):
            fig.update_xaxes(range=[MLT_min_toPlot, MLT_max_toPlot], title="Magnetic Local Time (hours) for " + str(All_KpRanges[i][0]) + "<Kp<"+  str(All_KpRanges[i][1]), row=i+1, col=1 )
        fig.update_yaxes(range=[min(all_JH_values), JHmax], title=Variable_toPlot+" ("+Units_of_Variable+")", showexponent = 'all', exponentformat = 'e')
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig)
    else:
        print( "There are no points for MLT per-Kp-range plot" )        
    
    if len(all_Altitude_values) > 0:
        # the main scatter plot
        fig = make_subplots(rows=len(All_KpRanges), cols=1, shared_xaxes=False, vertical_spacing=0.05)
        for i in range(0, len(All_KpRanges)):
            fig.append_trace( go.Scatter(name=Variable_toPlot_longname, x=Altitude_values_perKp[i], y=JH_values_perKp[i], mode='markers', marker_size=2, marker_color=MyColors[i]), row=i+1, col=1 )
        # lines along neighbor points (according to time, only for orbit results)
        if len(CALCULATIONS_OrbitFilesPath) > 0: 
            neighbors_JH   = list()
            neighbors_Alt = list()
            for i in range(0, len(All_KpRanges)):
                for t in range(0, len(Time_values_perKp[i])):
                    if t>0 and Time_values_perKp[i][t]-Time_values_perKp[i][t-1]<=10: # orbit file has 1 entry per 10 sec
                        if len(neighbors_JH)==0:
                            neighbors_JH.append( JH_values_perKp[i][t-1] )
                            neighbors_Alt.append( Altitude_values_perKp[i][t-1] )
                        neighbors_JH.append( JH_values_perKp[i][t] )
                        neighbors_Alt.append( Altitude_values_perKp[i][t] )
                    else:
                        fig.append_trace( go.Scatter(x=neighbors_Alt, y=neighbors_JH, mode='lines', line_width=1, line_color="rgba("+Hex_to_RGB(MyColors[i])+", 0.18)", showlegend=False ), row=i+1, col=1)
                        neighbors_JH   = list()
                        neighbors_Alt = list()
        # annotations, shapes etc
        BinAnnotations = list()
        FigureShapes = list()
        MyColorsIndex = 0
        BinIdx = 0
        for B in BinsIncludedAtPlot:
            if len(B.JH_values) > 0:
                # choose which sub-plot will host this Bin's data
                SubPlotIdx = 0
                for i in range(0, len(All_KpRanges)):
                    if B.Kp_min==All_KpRanges[i][0] and B.Kp_max==All_KpRanges[i][1]: SubPlotIdx = i+1
                    fig.update_xaxes(range=[115, Altitude_max_toPlot], title="Altitude (km) for " + str(All_KpRanges[i][0]) + "<Kp<"+  str(All_KpRanges[i][1]), row=i+1, col=1 )
                # choose color for mean line
                MyColorsIndex = SubPlotIdx - 1                
                # add visuals for the mean line
                FigureShapes.append( dict(type="line", x0=B.Altitude_min, y0=B.JH_mean,     x1=B.Altitude_max, y1=B.JH_mean,   line=dict( color=MyColors[MyColorsIndex], width=2, ),  xref= 'x'+str(SubPlotIdx), yref= 'y'+str(SubPlotIdx))  )                
                # add info as legend for this bin
                fig.append_trace( go.Scatter(name=B.ID + ":  " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + "  <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b>" + "  Mean=" + "{:.3e}".format(B.JH_mean) + "  " + "Variance=" + "{:.3e}".format(B.JH_variance) + "  St.Deviation=" + "{:.3e}".format(B.JH_variance**(1/2)), x=[-1], y=[-1], mode='markers', marker_size=1, marker_color=MyColors[MyColorsIndex]), row=SubPlotIdx, col=1 )
                # add bin name above the mean line
                BinAnnotations.append( dict( x=B.Altitude_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.Altitude_max-B.Altitude_min)*3/4, y=B.JH_mean, text=B.ID, showarrow=False, yshift=8, font=dict(color=MyColors[MyColorsIndex]), xref='x1', yref='y'+str(SubPlotIdx) ) )
                # add visuals for standard deviation
                FigureShapes.append( dict(type="line", x0=B.Altitude_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.Altitude_max-B.Altitude_min)*7/8, y0=B.JH_mean+(B.JH_variance)**(1/2)/2,     x1=B.Altitude_min+((BinIdx+1)/len(BinsIncludedAtPlot))*(B.Altitude_max-B.Altitude_min)*7/8, y1=B.JH_mean-(B.JH_variance)**(1/2)/2,     line=dict( color=MyColors[MyColorsIndex], width=2, ), xref= 'x1', yref= 'y'+str(SubPlotIdx) )  )
                #
                BinIdx += 1
        fig.update_layout( annotations=BinAnnotations )
        fig.update_layout( shapes=FigureShapes )
        fig.update_layout( title=Variable_toPlot_longname+" vs Altitude - " + getBinDescription(RegionName), 
                           width=1000, height=1500, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
        #fig.update_xaxes(range=[115, Altitude_max_toPlot], title="Altitude (km)")
        fig.update_yaxes(range=[min(all_JH_values), JHmax], title=Variable_toPlot+" ("+Units_of_Variable+")", showexponent = 'all', exponentformat = 'e')
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig)
    else:
        print( "There are no points for Altitude per-Kp-range plot" )
    
    

    
    
    
    
    
# Y = a*X^k + c
def func_powerlaw(x,  a, k, c):
    return a * (x**k)  +  c

# Y = a * log(X) + c
def func_logarithmic(x,  a, c):
    return [ (a * math.log(x_i) + c)  for x_i in x ]

# Y = a / e ^ (bx) + c
def func_euler(x,  a, b, c):
    return [ (a / (math.e**(b*x_i)) + c) for x_i in x ]

def func_maxwellian(x,  a, b, c):
    return [ (a * x_i*x_i * (math.e**(-b*x_i)) + c) for x_i in x ]

def plot_distributions( RegionName, Variable_toPlot, Units_of_Variable="", RegressionType="Maxwell", Variable_toPlot_longname="" ):
    """
        Plots the distribution of the values of the Variable.
        If a RegressionType is chosen then the function tries to find a curve of that type to fit the distribution. 
        User is warned with a message in case of failure.
        
        Args:
            RegionName (string): this region's Bins will be displayed at the plot. They are the Bins whose ID starts from RegionName.  
            Variable_toPlot (string): the name of the Variable to be plotted. See at the start of data.py for available names.  
            Units_of_Variable (string): the units that will be displayed on the plot.  
            Variable_toPlot_longname (string): A longer name of the Variable in order to be displayed at the plots.  
            RegressionType (string): Valid values are: 
                "None", 
                "Polynomial - degree 1", 
                "Polynomial - degree 2", 
                "Polynomial - degree 3", 
                "Polynomial - degree 4", 
                "Polynomial - degree 5", 
                "Polynomial - degree 6", 
                "Power law", 
                "Logarithmic", 
                "Euler", 
                "Maxwell"
    """
    
    if len(Units_of_Variable)==0:
        if Variable_toPlot == "Ohmic":
            Units_of_Variable = "W/m^3"
        elif Variable_toPlot == "DEN":
            Units_of_Variable = "g/cm^3"    
        elif Variable_toPlot == "SIGMA_PED" or Variable_toPlot == "SIGMA_HAL":
            Units_of_Variable = "S/m"
        elif Variable_toPlot == "Convection_heating" or Variable_toPlot == "Wind_heating":
            Units_of_Variable = "W/m^3"           
        elif Variable_toPlot == "EEX" or Variable_toPlot == "EEY":
            Units_of_Variable = "V/m"      
        else:
            Units_of_Variable = "?" 
    
    if len(Variable_toPlot_longname)==0: Variable_toPlot_longname=Variable_toPlot
        
    num_of_slots = 20
    # choose which bins we are going to work with
    if "(" in RegionName:
        RegionName = RegionName[ RegionName.find('(')+1 : RegionName.rfind(')') ]
    else:
        RegionName = RegionName
    BinsIncludedAtPlot = list()
    for B in Bins:
        if B.ID.startswith(RegionName): BinsIncludedAtPlot.append( B )
    
    # init 
    #generalMean = sum(all_JH_values) / len(all_JH_values)
    upper_value = 0
    for B in BinsIncludedAtPlot:
        if upper_value < B.JH_mean:
            upper_value = B.JH_mean
    upper_value = 2 * upper_value
    lower_value = 0
    #upper_value = max(all_JH_values)
    #lower_value = min(all_JH_values)
    if lower_value > upper_value: # negative mean
        tmp = lower_value
        lower_value = upper_value
        upper_value = tmp
    slot_length = (upper_value - lower_value) / num_of_slots
    print("upper_value=",upper_value, "lower_value=", lower_value, "num_of_slots=", num_of_slots, "Bins=", len(BinsIncludedAtPlot))
    if slot_length == 0: 
        print( "No values for Distribution Plot" )
        return
    
    # calculate distribution for each bin
    for B in BinsIncludedAtPlot:
        B.JH_distribution = [0] * num_of_slots
        #print(B.ID, "distribution:")
        for aJHval in B.JH_values:
            if aJHval >= lower_value  and    aJHval <= upper_value:
                slot_idx = int(   (aJHval - lower_value) / slot_length  )
            else:
                continue
            #print( ">>>>>> ", slot_idx, len(B.JH_distribution) )
            if  slot_idx >= len(B.JH_distribution): slot_idx = num_of_slots-1
            B.JH_distribution[ slot_idx ] += 1
        #print(B.JH_distribution, "\n")    
    
    # Normalize the distribution to [0,1] at y-axis
    #for B in BinsIncludedAtPlot:
    #    num_of_all_points_in_bin_distribution = sum(B.JH_distribution)
    #    for slot_idx in range(0, len(B.JH_distribution)):
    #        B.JH_distribution[ slot_idx ]  /=  num_of_all_points_in_bin_distribution
    
    # plot the distribution of all bins on the same figure
    if len(all_JH_values) > 0:
        MyColorsIndex = 0
        prevKpMin = -1
        BinAnnotations = list()
        BinIdx = 0
        fig = go.Figure()        
        print( "Plotting " + Variable_toPlot_longname + " Distribution" )
        for B in BinsIncludedAtPlot:
            if len(B.JH_values) > 0:
                # choose color for this bin's points
                if prevKpMin >= 0 and prevKpMin != B.Kp_min:
                    MyColorsIndex += 1
                    if MyColorsIndex>len(MyColors)-1: MyColorsIndex = 0
                prevKpMin = B.Kp_min                        

                if RegressionType.startswith( "Polynomial" ):
                    # calculate the Polynomial Regression
                    degree = int( RegressionType[-1] )
                    myPolynomial = np.polyfit( list(range(0,num_of_slots)), B.JH_distribution, degree )
                    # construct the equation to display
                    poly_str = "y = "
                    for i in range(0, len(myPolynomial)): 
                        if i>0 and myPolynomial[i] > 0: poly_str += "+ "
                        poly_str += "{:.2e}".format(myPolynomial[i])
                        if i < len(myPolynomial)-1: poly_str += "x^" + str(len(myPolynomial)-1-i) + " "
                    # draw the Polynomial Regression
                    mymodel = np.poly1d(myPolynomial)
                    myline = np.linspace(1, num_of_slots, num_of_slots)
                    fig.add_trace( go.Scatter(name=B.ID+":  "+poly_str, mode='lines', x=myline, y=mymodel(myline), line=dict(color=MyColors[MyColorsIndex], width=1) ) )
                elif RegressionType == "Power law":
                    try:
                        OptimalParams, OptParamsCovariance = curve_fit(func_powerlaw, list(range(0,num_of_slots)), B.JH_distribution)
                        poly_str = "y = " + "{:.2e}".format(OptimalParams[0]) + " * x^" + "{:.2e}".format(OptimalParams[1]) + " + " + "{:.2e}".format(OptimalParams[2])
                        fig.add_trace( go.Scatter(name=B.ID+":  "+poly_str, mode='lines', x=list(range(0,num_of_slots)), y=func_powerlaw(list(range(0,num_of_slots)), *OptimalParams), line=dict(color=MyColors[MyColorsIndex], width=1) ) )
                    except:
                        print( "Warning: Curve fit failed for", B.ID )                                               
                elif RegressionType == "Logarithmic":
                    try:
                        OptimalParams, OptParamsCovariance = curve_fit(func_logarithmic, list(range(1,num_of_slots)), B.JH_distribution[1:])
                        poly_str = "y = " + "{:.2e}".format(OptimalParams[0]) + " * log(x) +" + "{:.2e}".format(OptimalParams[1])
                        fig.add_trace( go.Scatter(name=B.ID+":  "+poly_str, mode='lines', x=list(range(1,num_of_slots)), y=func_logarithmic(list(range(1,num_of_slots)), *OptimalParams), line=dict(color=MyColors[MyColorsIndex], width=1) ) )
                    except:
                        print( "Warning: Curve fit failed for", B.ID )                        
                elif RegressionType == "Euler":
                    try:
                        OptimalParams, OptParamsCovariance = curve_fit(func_euler, list(range(1,num_of_slots)), B.JH_distribution[1:])
                        poly_str = "y = " + "{:.2e}".format(OptimalParams[0]) + " / e^(" + "{:.2e}".format(OptimalParams[1]) + "*x) + " + "{:.2e}".format(OptimalParams[2])
                        fig.add_trace( go.Scatter(name=B.ID+":  "+poly_str, mode='lines', x=list(range(1,num_of_slots)), y=func_euler(list(range(1,num_of_slots)), *OptimalParams), line=dict(color=MyColors[MyColorsIndex], width=1) ) )
                    except:
                        print( "Warning: Curve fit failed for", B.ID )                        
                elif RegressionType == "Maxwell":
                    try:
                        OptimalParams, OptParamsCovariance = curve_fit(func_maxwellian, list(range(1,num_of_slots)), B.JH_distribution[1:])
                        poly_str = "y = " + "{:.2e}".format(OptimalParams[0]) + " * x^2 * e^(-" + "{:.2e}".format(OptimalParams[1]) + "*x) + " + "{:.2e}".format(OptimalParams[2])
                        fig.add_trace( go.Scatter(name=B.ID+":  "+poly_str, mode='lines', x=list(range(1,num_of_slots)), y=func_maxwellian(list(range(1,num_of_slots)), *OptimalParams), line=dict(color=MyColors[MyColorsIndex], width=1) ) )                    
                    except:
                        print( "Warning: Curve fit failed for", B.ID )                        

                # draw the distribution
                bin_desciption = B.ID + ":  " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + "  <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b>" + "  Mean=" + "{:.3e}".format(B.JH_mean) + "  " + "Variance=" + "{:.3e}".format(B.JH_variance) + "  St.Deviation=" + "{:.3e}".format(B.JH_variance**(1/2))
                fig.add_trace( go.Scatter(name=bin_desciption, x=list(range(0,num_of_slots)), y=B.JH_distribution, mode='markers', marker_size=3, marker_color=MyColors[MyColorsIndex]  ) )
                
                # add visuals for the mean line                
                mean_slot_idx = int(   (B.JH_mean - lower_value) / slot_length  )
                fig.add_shape( type="line", x0=mean_slot_idx, y0=0,     x1=mean_slot_idx, y1=(95/100)*max(B.JH_distribution),     line=dict( color=MyColors[MyColorsIndex], width=1, ), )    
                # add bin name above the mean line
                BinAnnotations.append( dict( x=mean_slot_idx, y=(95/100)*max(B.JH_distribution), xref="x", yref="y", text=B.ID, showarrow=False, yshift=8, font=dict(color=MyColors[MyColorsIndex])) )
                
                # add visuals for standard deviation
                #StDev_slots_width = int(   ((B.JH_variance)**(1/2)/2) / slot_length  )
                #fig.add_shape( type="line", x0=mean_slot_idx-StDev_slots_width, y0=(95/100)*max(B.JH_distribution),     x1=mean_slot_idx+StDev_slots_width, y1=(95/100)*max(B.JH_distribution),     line=dict( color=MyColors[MyColorsIndex], width=1, ), )
                
                BinIdx += 1
                
        # draw correct ticks at the x-axis, containing the JH values
        XaxisTickPositions = list()
        XaxisTickLabels = list()
        for i in range( 0, num_of_slots, int(num_of_slots/5) ):
            XaxisTickPositions.append( i )
            XaxisTickLabels.append(  "{:.3e}".format(lower_value + i*slot_length)  )            
        XaxisTickPositions.append( num_of_slots-1 )
        XaxisTickLabels.append(  "{:.3e}".format(upper_value)  )
        fig.update_xaxes( tickmode = 'array', tickvals=XaxisTickPositions,  ticktext=XaxisTickLabels )
                
        fig.update_layout( annotations=BinAnnotations )
        fig.update_layout( title=Variable_toPlot_longname+" Distribution per Bin - " + getBinDescription(RegionName), 
                           width=1000, height=900, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
        fig.update_xaxes(range=[0,num_of_slots-1], title=Variable_toPlot+" ("+Units_of_Variable+")", showexponent = 'all', exponentformat = 'e')
        fig.update_yaxes(title="Number of hits inside the bin") #rangemode='nonnegative'
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(fig)


        

        
        
        


        
        
        
        
        
def plot_comparison( results_filename1, results_filename2, Variable_toPlot, PlotTitle="" ):
    """
        Loads two result-files and plots a comparison of their values.
        A bar-chart is plotted with one bar for each Bin mean.
        Useful for comparing the results of an orbit to those of tiegcm in order to see if a satellite can describe adequately a region.
        
        Args:
            results_filename1 (string): a NetCDF results file.  
            results_filename2 (string): a NetCDF results file.  
            Variable_toPlot (string): the name of the Variable to be plotted. See at the start of data.py for available names.  
            PlotTitle (string): a title which will be displayed on top of the plot.  
    """
    ColorTriplet = ["#EEEEEE", "#FF4447", "#257985"] # white red petrol
    # init
    BinIDs = list()
    Means1 = list()
    Means2 = list()
    StDev1 = list()
    StDev2 = list()
    RegionDescription = ""
    # load results no1
    load_results( results_filename1, Variable_toPlot )
    for B in Bins:
        RegionDescription = B.Description
        BinIDs.append( B.ID )
        Means1.append( B.JH_mean )
        StDev1.append( math.sqrt(B.JH_variance) )
        #print( B.ID, B.JH_mean, math.sqrt(B.JH_variance), B.JH_variance**(1/2) )
    # clean up
    for B in Bins:
        B.reset()
    # load results no2
    load_results( results_filename2, Variable_toPlot )
    for B in Bins:
        Means2.append( B.JH_mean )
        StDev2.append( math.sqrt(B.JH_variance) )
    # plot bars chart
    Bars = list()
    fig = go.Figure(data=[
        go.Bar(name='TIEGCM - JH Mean', x=BinIDs, y=Means1, marker_color=ColorTriplet[1], offsetgroup=0),
        go.Bar(name='Orbit  - JH Mean', x=BinIDs, y=Means2, marker_color=ColorTriplet[2], offsetgroup=1),
        #go.Bar(name='JH StDv 1', x=BinIDs, y=StDev1, marker_color="red",  offsetgroup=0, base=Means1),
        #go.Bar(name='JH StDv 2', x=BinIDs, y=StDev2, marker_color="cyan", offsetgroup=1, base=Means2)
    ])
    fig.update_layout(barmode='group', title=PlotTitle, plot_bgcolor=ColorTriplet[0], yaxis=dict(showexponent='all',exponentformat='e'))
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig) 

    
    
    
    

    
    
    
    

    
def CalculateStandardDeviation( Data ):
    """
    Takes a list of real numbers and returns their standard deviation
    
    Args:
        a list of real numbers.  
    
    Returns:
        the standard deviation of the numbers inside the argument
    """
    mean = sum(Data) / len(Data)
    variance = 0 
    for n in Data:
        variance += abs(n - mean)**2
    stdev = variance / len(Data)
    return stdev


def plot_ColorSpread_KpSeparated( RegionName, Variable_toPlot, Variable_toPlot_longname="" ):
    """
        Creates plots with several sub-plots, according to Kp-index and Altitude.
        Each subplot is a colored surface of Magnetic Latitude against Magnetic Local Time.
        The colors represent the values of Variable_toPlot
        In total four plots are created for depicting:
            the Mean value of the Variable_toPlot inside the RegionName
            the 10th percentile of the Variable_toPlot inside the RegionName
            the 90th percentile of the Variable_toPlot inside the RegionName
            the Standard Deviation of the Variable_toPlot inside the RegionName
        
        Args:
            RegionName (string): this region's Bins will be displayed at the plot. They are the Bins whose ID starts from RegionName.  
            Variable_toPlot (string): the name of the Variable to be plotted. See at the start of data.py for available names.  
            Variable_toPlot_longname (string): A longer name of the Variable in order to be displayed at the plots.  
    """
    # init parameters
    if Variable_toPlot == "Ohmic":
        MultiplicationFactor = 10**8 
        new_units = "10^-8 W/m3"
    elif Variable_toPlot == "SIGMA_PED":
        MultiplicationFactor = 10**3 
        new_units = "mS/m"
    elif Variable_toPlot == "SIGMA_HAL":
        MultiplicationFactor = 10**3 
        new_units = "mS/m"        
    elif Variable_toPlot == "Convection_heating":
        MultiplicationFactor = 10**8 
        new_units = "10^-8 W/m3"           
    elif Variable_toPlot == "Wind_heating":
        MultiplicationFactor = 10**8 
        new_units = "10^-8 W/m3"                   
    elif Variable_toPlot == "EEX_si" or Variable_toPlot == "EEY_si":
        MultiplicationFactor = 1
        new_units = "mV/m"      
    elif Variable_toPlot == "JH/mass":
        MultiplicationFactor = 1 
        new_units = "W/kg"
    elif Variable_toPlot == "JH/pressure":
        MultiplicationFactor = 1 
        new_units = "sec^-1"        
    else:
        MultiplicationFactor = 1
        new_units = "?" 
       
    if len(Variable_toPlot_longname)==0: Variable_toPlot_longname = Variable_toPlot
        
    print("Variable_toPlot=", Variable_toPlot)

    # Region specific binning:
    regionMLTmin = 999
    regionMLTmax = -999
    regionMagLatMin = 999
    regionMagLatMax = -999
    regionAltMin = 999
    regionAltMax = -999
    for B in Bins:
        if B.ID.startswith( RegionName ):
            if regionMLTmin>B.MLT_min: regionMLTmin = B.MLT_min
            if regionMLTmax<B.MLT_max: regionMLTmax = B.MLT_max
            if regionMagLatMin>B.MagLat_min: regionMagLatMin = B.MagLat_min
            if regionMagLatMax<B.MagLat_max: regionMagLatMax = B.MagLat_max
            if regionAltMin>B.Altitude_min: regionAltMin = B.Altitude_min
            if regionAltMax<B.Altitude_max: regionAltMax = B.Altitude_max
    if regionMLTmax <= regionMLTmin: regionMLTmax += 24
    x_axes_range = [regionMLTmin, regionMLTmax]
    print("REGION=",RegionName)
    # init data structures
    Buckets = dict()
    MLT_duration_of_a_bucket   = 1
    MagLat_degrees_of_a_bucket = 1
    ALT_distance_of_a_bucket   = 10
    ALTsequence     = list( range( regionAltMin, regionAltMax, ALT_distance_of_a_bucket ) )
    MLTsequence     = list( range( regionMLTmin,  regionMLTmax, MLT_duration_of_a_bucket) )
    MagLatSequence  = list( range( regionMagLatMin,  regionMagLatMax, MagLat_degrees_of_a_bucket) )
    KPsequence      = [ 0, 3 ] 
    for aMLT in MLTsequence:
        for aMagLat in MagLatSequence:
            for anALT in ALTsequence:
                for aKP in KPsequence:
                    Buckets[(aKP, anALT, aMagLat, aMLT)] = list()
    
    print("Processing", len(all_JH_values), "values")
    for i in range( 0, len(all_JH_values) ):
        #if all_JH_values[i] < 0: print("NEGATIF at", i, all_JH_values[i])
        #if i % 10000000 == 0: print( "Processing value No", i, datetime.now().strftime("%d-%m-%Y %H:%M:%S") )
        mlt_to_fall = alt_to_fall = maglat_to_fall = -1  
        # find correct Alt
        for seq_idx in range(0, len(ALTsequence)):
            if all_Altitude_values[i]>=ALTsequence[seq_idx] and all_Altitude_values[i]<ALTsequence[seq_idx]+ALT_distance_of_a_bucket:
                alt_to_fall=ALTsequence[seq_idx]
                break
        if alt_to_fall == -1: continue # ignore highest altitudes        
        # find correct kp
        if all_Kp_values[i] < 3: 
            kp_to_fall = 0
        else:
            kp_to_fall = 3
        # find correct MLT
        MLT_tocheck = all_MLT_values[i]
        if regionMLTmax>24  and  MLT_tocheck<=regionMLTmax-24:
            MLT_tocheck += 24
        for seq_idx in range(0, len(MLTsequence)):
            if MLT_tocheck>=MLTsequence[seq_idx] and MLT_tocheck<MLTsequence[seq_idx]+MLT_duration_of_a_bucket: 
                mlt_to_fall=MLTsequence[seq_idx]
                break
        if MLT_tocheck == MLTsequence[len(MLTsequence)-1]+MLT_duration_of_a_bucket: mlt_to_fall = MLTsequence[len(MLTsequence)-1] # for last MLT position
        # find correct MagLat
        for seq_idx in range(0, len(MagLatSequence)):
            if all_MagLat_values[i]>=MagLatSequence[seq_idx] and all_MagLat_values[i]<MagLatSequence[seq_idx]+MagLat_degrees_of_a_bucket:
                maglat_to_fall=MagLatSequence[seq_idx]
                break
        if maglat_to_fall == -1: continue # ignore 
        # store the value at the right place
        Buckets[ (kp_to_fall, alt_to_fall, maglat_to_fall, mlt_to_fall) ].append( all_JH_values[ i ] )

    # plot
    
    # construct the column titles 
    ColumnTitles = list()    
    for i in range(0, len(ALTsequence)):
        ColumnTitles.append( "<b>" + str(ALTsequence[i]) + "-"  + str(ALTsequence[i]+ALT_distance_of_a_bucket) + "km" + "</b>")
        
    #make plot
    HitsStr = ""
    fig1 = make_subplots(rows=len(KPsequence), cols=len(ALTsequence), shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.035, horizontal_spacing=0.01, subplot_titles=ColumnTitles)
    fig2 = make_subplots(rows=len(KPsequence), cols=len(ALTsequence), shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.035, horizontal_spacing=0.01, subplot_titles=ColumnTitles)
    fig3 = make_subplots(rows=len(KPsequence), cols=len(ALTsequence), shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.035, horizontal_spacing=0.01, subplot_titles=ColumnTitles)
    fig4 = make_subplots(rows=len(KPsequence), cols=len(ALTsequence), shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.035, horizontal_spacing=0.01, subplot_titles=ColumnTitles)
    figs = [fig1, fig2, fig3, fig4]
    
    # bundle data, min and max values
    allPercentiles10_min = allPercentiles10_logscale_min = 999999
    allPercentiles10_max = allPercentiles10_logscale_max = -99999
    allPercentiles90_min = allPercentiles90_logscale_min = 999999
    allPercentiles90_max = allPercentiles90_logscale_max = -99999
    allMeans_min = allMeans_logscale_min = 999999
    allMeans_max = allMeans_logscale_max = -99999
    allStDevs_min = allStDevs_logscale_min = 999999
    allStDevs_max = allStDevs_logscale_max = -99999    
    for aKP in KPsequence:
        for anALT in ALTsequence:
            Percentiles10 = np.zeros( ( len(MagLatSequence), len(MLTsequence)) )
            Percentiles90 = np.zeros( ( len(MagLatSequence), len(MLTsequence)) )
            Means         = np.zeros( ( len(MagLatSequence), len(MLTsequence)) )
            StDevs        = np.zeros( ( len(MagLatSequence), len(MLTsequence)) )
            hits  = 0

            for aMLT in MLTsequence:
                for aMagLat in MagLatSequence:
                    hits += len(Buckets[(aKP, anALT, aMagLat, aMLT)])
                    i = MagLatSequence.index(aMagLat)
                    j = MLTsequence.index(aMLT)
                    if len(Buckets[(aKP, anALT, aMagLat, aMLT)]) > 0: 
                        Percentiles10[ i, j ] = np.percentile(Buckets[(aKP, anALT, aMagLat, aMLT)], 10) 
                        Percentiles90[ i, j ] = np.percentile(Buckets[(aKP, anALT, aMagLat, aMLT)], 90)
                        Means        [ i, j ] = sum(Buckets[(aKP, anALT, aMagLat, aMLT)]) / len(Buckets[(aKP, anALT, aMagLat, aMLT)]) 
                        StDevs       [ i, j ] = CalculateStandardDeviation( Buckets[(aKP, anALT, aMagLat, aMLT)] )
                        
            print( "Kp = ", aKP, "ALT =", anALT, "   Hits =", hits)
            HitsStr += "Kp=" + str(aKP) + " ALT=" + str(anALT) + "   Hits=" + str(hits) + "\n"
            
            # change units
            Percentiles10 *= MultiplicationFactor
            Percentiles90 *= MultiplicationFactor
            Means         *= MultiplicationFactor
            StDevs        *= MultiplicationFactor
            
            # logScale
            Percentiles10_logscale = np.log10(Percentiles10)
            #for i in range(0, len(Percentiles10_logscale)):
            #    for j in range(0, len(Percentiles10_logscale[i])):
            #        if np.isnan( Percentiles10_logscale[i, j] ):
            #            print( i, j, Percentiles10[i, j] )
            Percentiles10_logscale_min = np.nanmin(Percentiles10_logscale)
            Percentiles10_logscale_max = np.nanmax(Percentiles10_logscale)
            Percentiles10_min = np.nanmin(Percentiles10)
            Percentiles10_max = np.nanmax(Percentiles10)
            if Percentiles10_logscale_min==float("-inf"): Percentiles10_logscale_min = 0
            if Percentiles10_logscale_max==float("-inf"): Percentiles10_logscale_max = 0
            if allPercentiles10_min > Percentiles10_min: allPercentiles10_min = Percentiles10_min
            if allPercentiles10_max < Percentiles10_max: allPercentiles10_max = Percentiles10_max
            if allPercentiles10_logscale_min > Percentiles10_logscale_min: allPercentiles10_logscale_min = Percentiles10_logscale_min
            if allPercentiles10_logscale_max < Percentiles10_logscale_max: allPercentiles10_logscale_max = Percentiles10_logscale_max                            
            #Percentiles10_logscale = np.nan_to_num( Percentiles10_logscale, nan=np.nan, posinf=Percentiles10_logscale_max, neginf=Percentiles10_logscale_min )
            #
            Percentiles90_logscale = np.log10(Percentiles90)
            Percentiles90_logscale_min = np.nanmin(Percentiles90_logscale)
            Percentiles90_logscale_max = np.nanmax(Percentiles90_logscale)
            Percentiles90_min = np.nanmin(Percentiles90)
            Percentiles90_max = np.nanmax(Percentiles90)
            if Percentiles90_logscale_min==float("-inf"): Percentiles90_logscale_min = 0
            if Percentiles90_logscale_max==float("-inf"): Percentiles90_logscale_max = 0
            if allPercentiles90_min > Percentiles90_min: allPercentiles90_min = Percentiles90_min
            if allPercentiles90_max < Percentiles90_max: allPercentiles90_max = Percentiles90_max
            if allPercentiles90_logscale_min > Percentiles90_logscale_min: allPercentiles90_logscale_min = Percentiles90_logscale_min
            if allPercentiles90_logscale_max < Percentiles90_logscale_max: allPercentiles90_logscale_max = Percentiles90_logscale_max                
            #Percentiles90_logscale = np.nan_to_num( Percentiles90_logscale, nan=np.nan, posinf=Percentiles90_logscale_max, neginf=Percentiles90_logscale_min )
            #
            Means_logscale = np.log10(Means)
            Means_logscale_min = np.nanmin(Means_logscale)
            Means_logscale_max = np.nanmax(Means_logscale)
            
            Means_min =  999999
            Means_max = -999999
            for i in range(0, len(Means)):
                for j in range(0, len(Means[i])):
                    if Means[i][j] is not None and Means[i][j]!=0 and Means_min>Means[i][j]: Means_min = Means[i][j]
                    if Means[i][j] is not None and Means[i][j]!=0 and Means_max<Means[i][j]: Means_max = Means[i][j]
                        
            if Means_logscale_min==float("-inf"): Means_logscale_min = 0
            if Means_logscale_max==float("-inf"): Means_logscale_max = 0
            if allMeans_min > Means_min: allMeans_min = Means_min
            if allMeans_max < Means_max: allMeans_max = Means_max
            if allMeans_logscale_min > Means_logscale_min: allMeans_logscale_min = Means_logscale_min
            if allMeans_logscale_max < Means_logscale_max: allMeans_logscale_max = Means_logscale_max                
            #Means_logscale = np.nan_to_num( Means_logscale, nan=np.nan, posinf=Means_logscale_max, neginf=Means_logscale_min )
            #
            StDevs_logscale = np.log10(StDevs)
            StDevs_logscale_min = np.nanmin(StDevs_logscale)
            StDevs_logscale_max = np.nanmax(StDevs_logscale)
            StDevs_min = np.nanmin(StDevs)
            StDevs_max = np.nanmax(StDevs)
            if StDevs_logscale_min==float("-inf"): StDevs_logscale_min = 0
            if StDevs_logscale_max==float("-inf"): StDevs_logscale_max = 0
            if allStDevs_min > StDevs_min: allStDevs_min = StDevs_min
            if allStDevs_max < StDevs_max: allStDevs_max = StDevs_max
            if allStDevs_logscale_min > StDevs_logscale_min: allStDevs_logscale_min = StDevs_logscale_min
            if allStDevs_logscale_max < StDevs_logscale_max: allStDevs_logscale_max = StDevs_logscale_max                
            #StDevs_logscale = np.nan_to_num( StDevs_logscale, nan=np.nan, posinf=StDevs_logscale_max, neginf=StDevs_logscale_min )

            # plot heatmap
            figs[0].add_trace( go.Heatmap(z=Percentiles10_logscale.tolist(), x=MLTsequence, y=MagLatSequence, showlegend=False, coloraxis="coloraxis1"), row=KPsequence.index(aKP)+1, col=ALTsequence.index(anALT)+1,  )
            figs[1].add_trace( go.Heatmap(z=Percentiles90_logscale.tolist(), x=MLTsequence, y=MagLatSequence, showlegend=False, coloraxis="coloraxis1"), row=KPsequence.index(aKP)+1, col=ALTsequence.index(anALT)+1,  )
            figs[2].add_trace( go.Heatmap(z=Means_logscale.tolist(),         x=MLTsequence, y=MagLatSequence, showlegend=False, coloraxis="coloraxis1"), row=KPsequence.index(aKP)+1, col=ALTsequence.index(anALT)+1,  )
            figs[3].add_trace( go.Heatmap(z=StDevs_logscale.tolist(),        x=MLTsequence, y=MagLatSequence, showlegend=False, coloraxis="coloraxis1"), row=KPsequence.index(aKP)+1, col=ALTsequence.index(anALT)+1,  )

    for i in range(0,  len(figs)):
        figs[i].update_layout(coloraxis=dict(colorscale=allojal), showlegend=False) #fig.update_traces(zmin=0.07687949e-02, zmax=3.07687949e-01, selector=dict(type="heatmap"))
        # display titles
        figs[i].update_yaxes( title_text="<b>" + "Kp 0-3" + "</b>" + "<br><br>" + "Magnetic Latitude (deg)", row=1, col=1, side='left', secondary_y=False)
        figs[i].update_yaxes( title_text="<b>" + "Kp 3-9" + "</b>" + "<br><br>" + "Magnetic Latitude (deg)", row=2, col=1, side='left', secondary_y=False)
        for aMLT in MLTsequence: figs[i].update_xaxes( title_text="MLT (hours)", row=len(KPsequence), col=MLTsequence.index(aMLT)+1)
        #
        mainTitle = "" 
        if   i == 0: 
            figs[i].update_traces(zmin=allPercentiles10_min, zmax=allPercentiles10_max)
            mainTitle += RegionName + " - 10th Percentile of " + Variable_toPlot
            #figs[i].update_layout(coloraxis_colorbar=dict( title="Log scale<br>colors",  tickvals=[Percentiles10_logscale_min, Percentiles10_logscale_max],  ticktext=["{:.3e}".format(Percentiles10_min) , "{:.3e}".format(Percentiles10_max) ], ))
            my_Tickvals    = np.linspace(allPercentiles10_min, allPercentiles10_max, 5, endpoint=True)
        elif i == 1:
            figs[i].update_traces(zmin=allPercentiles90_min, zmax=allPercentiles90_max)
            mainTitle += RegionName + " - 90th Percentile of " + Variable_toPlot
            #figs[i].update_layout(coloraxis_colorbar=dict( title="Log scale<br>colors",  tickvals=[Percentiles90_logscale_min, Percentiles90_logscale_max],  ticktext=["{:.3e}".format(Percentiles90_min) , "{:.3e}".format(Percentiles90_max) ], ))
            my_Tickvals    = np.linspace(allPercentiles90_min, allPercentiles90_max, 5, endpoint=True)
        elif i == 2:
            figs[i].update_traces(zmin=allMeans_min, zmax=allMeans_max)
            mainTitle += RegionName + " - Mean of " + Variable_toPlot
            #figs[i].update_layout(coloraxis_colorbar=dict( title="Log scale<br>colors",  tickvals=[Means_logscale_min, Means_logscale_max],  ticktext=["{:.3e}".format(Means_min) , "{:.3e}".format(Means_max) ], ))
            my_Tickvals    = np.linspace(allMeans_min, allMeans_max, 5, endpoint=True)
        elif i == 3:
            figs[i].update_traces(zmin=allStDevs_min, zmax=allStDevs_max)
            mainTitle += RegionName + " - Standard Deviation of " + Variable_toPlot
            #figs[i].update_layout(coloraxis_colorbar=dict( title="Log scale<br>colors",  tickvals=[StDevs_logscale_min, StDevs_logscale_max],  ticktext=["{:.3e}".format(StDevs_min) , "{:.3e}".format(StDevs_max) ], ))
            my_Tickvals    = np.linspace(allStDevs_min, allStDevs_max, 5, endpoint=True)
        # tick values at the color bar
        my_logTickvals = list()
        my_Ticktexts   = list()
        for t in range( 0, len(my_Tickvals) ):
            try:
                my_logTickvals.append( math.log10(my_Tickvals[t]) )
                my_Ticktexts.append( "{:.3e}".format(my_Tickvals[t]) )                
            except Exception as ex:
                #print(ex)
                pass
        figs[i].update_layout(coloraxis_colorbar=dict( title="Log scale<br>colors",  tickvals=my_logTickvals,  ticktext=my_Ticktexts, ))
        #
        figs[i].update_yaxes( range=[regionMagLatMin,  regionMagLatMax] )
        mainTitle += Variable_toPlot_longname + " (" + new_units + ")"
        figs[i].update_layout( title = mainTitle, width=400+len(ALTsequence)*150, height=220+200*len(KPsequence), showlegend=True, legend_orientation="h", legend_y=-0.04) 
        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot(figs[i])
        
    print( HitsStr )    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
def plot_PDFperSubBin( TIEGCMresults_filename, ORBITresults_filename, RegionName, Variable_toPlot, Variable_toPlot_longname="" ):
    """
        Plots Probability Densities of the Variable_toPlot for two result-files (usually TIEGCM and ORBIT) at the same chart.
        Two plots are created, one having linear values ofr the x-axis (=Variable_toPlot values) and the other logarithmic.
        Useful for comparing the results of an orbit to those of tiegcm in order to see if a satellite can describe adequately a region.
        
        Args:
            TIEGCMresults_filename: a netcdf results-file.  
            ORBITresults_filename: a netcdf results-file.  
            RegionName (string): this region's Bins will be displayed at the plot. They are the Bins whose ID starts from RegionName.  
            Variable_toPlot (string): the name of the Variable to be plotted. See at the start of data.py for available names.  
            Variable_toPlot_longname (string): A longer name of the Variable in order to be displayed at the plots.  
    """
    # init parameters
    if Variable_toPlot == "Ohmic":
        MultiplicationFactor = 10**8 
        new_units = "10^-8 W/m3"
        JH_min = 0
        JH_max = 7 #197 #1.538087e-06 * 10**8 / 10 #1.4e-7
    elif Variable_toPlot == "SIGMA_PED":
        MultiplicationFactor = 10**3 
        new_units = "mS/m"
    elif Variable_toPlot == "SIGMA_HAL":
        MultiplicationFactor = 10**3 
        new_units = "mS/m"        
    elif Variable_toPlot == "Convection_heating":
        MultiplicationFactor = 10**8 
        new_units = "10^-8 W/m3"           
    elif Variable_toPlot == "Wind_heating":
        MultiplicationFactor = 10**8 
        new_units = "10^-8 W/m3"                   
    elif Variable_toPlot == "EEX_si" or Variable_toPlot == "EEY_si":
        MultiplicationFactor = 1
        new_units = "mV/m"      
    elif Variable_toPlot == "JH/mass":
        MultiplicationFactor = 1 
        new_units = "W/kg"
    elif Variable_toPlot == "JH/pressure":
        MultiplicationFactor = 1 
        new_units = "sec^-1"        
    else:
        MultiplicationFactor = 1
        new_units = "?"         
        
    if len(Variable_toPlot_longname)==0: Variable_toPlot_longname = Variable_toPlot    
        
    print("Variable_toPlot=", Variable_toPlot)

    
    # Region info:
    regionAltMin = regionMLTmin = regionMagLatMin =  99999
    regionAltMax = regionMLTmax = regionMagLatMax = -99999
    All_KpRanges = list()        
    for B in Bins:
        if B.ID.startswith( RegionName ):
            if [B.Kp_min, B.Kp_max] not in All_KpRanges: 
                All_KpRanges.append( [B.Kp_min, B.Kp_max] )  
            if regionAltMin>B.Altitude_min: regionAltMin = B.Altitude_min
            if regionAltMax<B.Altitude_max: regionAltMax = B.Altitude_max
            if regionMLTmin>B.MLT_min: regionMLTmin = B.MLT_min
            if regionMLTmax<B.MLT_max: regionMLTmax = B.MLT_max
            if regionMagLatMin>B.MagLat_min: regionMagLatMin = B.MagLat_min
            if regionMagLatMax<B.MagLat_max: regionMagLatMax = B.MagLat_max
    if regionMLTmax <= regionMLTmin: regionMLTmax += 24    
    print("REGION=", RegionName, "    (", regionAltMin, regionAltMax, ") (", regionMLTmin,  regionMLTmax, ") (", regionMagLatMin,  regionMagLatMax, ")" )

    
    DataFiles = [ TIEGCMresults_filename, ORBITresults_filename ]
    fig_log = make_subplots(rows=1, cols=len(All_KpRanges), shared_yaxes=True, horizontal_spacing=0.015)
    fig_lin = make_subplots(rows=1, cols=len(All_KpRanges), shared_yaxes=True, horizontal_spacing=0.015)

    for input_file_idx in range(0, len(DataFiles)):
        aDataFile = DataFiles[input_file_idx]
        load_results( aDataFile, Variable_toPlot, loadGlobalValues=False, loadTimeValues=False, loadMagLatValues=True, loadMLTvalues=True, loadAltValues=True, loadLatValues=False )
        
        # decide line type and opacity
        if input_file_idx == 1: # it is orbit data
            LineType = "dot"
            LineFade = 0.5
        else: # it is tiegcm-grid data
            LineType = "solid"
            LineFade = 0
            
        #### apply the MultiplicationFactor to fix the variable's units and the log-scale if necessary
        num_of_subBins = 0
        for B in Bins:
            if B.ID.startswith(RegionName) and len(B.JH_values)>0:
                num_of_subBins += 1
                for i in range(0, len(B.JH_values)):
                    B.JH_values[i] *= MultiplicationFactor
        CalculateStatsOnData()            
    
        #### Plot 
        BinAnnotations = list()
        FigureShapes = list()
        MyColorsIndex = 0
        SubPlotIdx = 0
        BinIdx = 0
        Npercentage = 0
        for B in Bins:
            if B.ID.startswith(RegionName) and len(B.JH_values)>0:
                
                Tmin = "{:.3f}".format( min(B.JH_values) )
                Tmax = "{:.3f}".format( max(B.JH_values) )
                Tmean = "{:.3f}".format( np.mean(B.JH_values) )
                Tmedian = "{:.3f}".format( np.percentile(B.JH_values, 50) )
                Tper10 = "{:.3f}".format( np.percentile(B.JH_values, 10) )
                Tper90 = "{:.3f}".format( np.percentile(B.JH_values, 90) )
                print(B.ID, B.Kp_min,"<Kp<",B.Kp_max, B.Altitude_min,"<Alt<",B.Altitude_max)
                print( "    min =", Tmin, " max=", Tmax, " mean =", Tmean, " median =", Tmedian, " percentile10 =", Tper10, " percentile90 =", Tper90)
                
                # choose which sub-plot will host this Bin's data
                #SubPlotIdx += 1
                # find out the plot team
                for i in range(0, len(All_KpRanges)):
                    if B.Kp_min==All_KpRanges[i][0] and B.Kp_max==All_KpRanges[i][1]: PlotTeam = i+1 
                SubPlotIdx = PlotTeam
                # decide  color
                MyColorsIndex = PlotTeam - 1
                #if "Hz" in aDataFile or "Tricubic" in aDataFile: MyColorsIndex += 5
                currentColor = MyColors[MyColorsIndex]
                # decide how many data points will be plotted 
                #if Npercentage == 0: Npercentage = 2000 / len(B.JH_values)
                #num_of_points_to_plot = int( len(B.JH_values) * Npercentage )
                #step_per_subBin = int ( len(B.JH_values) / num_of_points_to_plot )
                #print( "Alt", B.Altitude_min, B.Altitude_max, " Kp", B.Kp_min, B.Kp_max, "  Ploting", num_of_points_to_plot, " out of ", len(B.JH_values), "points" )
                # **** add info as legend for this bin
                if input_file_idx == 1:
                    prefix = "Orbit "
                else:
                    prefix = "TIEGCM "
                fig_log.append_trace( go.Scatter(name=prefix + B.ID + ": " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + " <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b>" + " Median=" + "{:.3f}".format(B.JH_mean) + " Variance=" + "{:.3f}".format(B.JH_variance) + " St.Dev.=" + "{:.3f}".format(B.JH_variance**(1/2)), x=[-1], y=[-1], mode='markers', marker_size=1, marker_color=currentColor), row=1, col=SubPlotIdx )
                fig_lin.append_trace( go.Scatter(name=prefix + B.ID + ": " + str(B.Altitude_min) + "<Alt<"+ str(B.Altitude_max) + " <b>" + str(B.Kp_min) + "<Kp<" + str(B.Kp_max) + "</b>" + " Median=" + "{:.3f}".format(B.JH_mean) + " Variance=" + "{:.3f}".format(B.JH_variance) + " St.Dev.=" + "{:.3f}".format(B.JH_variance**(1/2)), x=[-1], y=[-1], mode='markers', marker_size=1, marker_color=currentColor), row=1, col=SubPlotIdx )
                # **** plot data points
                #fig_log.append_trace( go.Scatter(name=Variable_toPlot_longname, x=B.JH_values[::step_per_subBin], y=B.Altitude_values[::step_per_subBin], mode='markers', marker_size=2, marker_color=currentColor, opacity=0.5, showlegend=False), row=1, col=SubPlotIdx )
                #fig_lin.append_trace( go.Scatter(name=Variable_toPlot_longname, x=B.JH_values[::step_per_subBin], y=B.Altitude_values[::step_per_subBin], mode='markers', marker_size=2, marker_color=currentColor, opacity=0.5, showlegend=False), row=1, col=SubPlotIdx )
                #################
                # find the values which fall in this bin
                num_of_buckets = 150
                bucket_widths  = list()
                bucket_starts  = list()
                Buckets        = [0] * num_of_buckets
                factor1 = 1.2 # 1.085
                factor2 = 2.2 # 1
                for j in range( 0, num_of_buckets ):
                    bucket_widths.append( 0.02 + factor1**((j+1)/factor2) - factor1**(j/factor2) )
                bucket_widths = [0.020, 0.024, 0.029, 0.035, 0.041, 0.050, 0.060, 0.072, 0.086, 0.103, 0.124, 0.149, 0.178, 0.214, 0.257, 0.308, 0.370, 0.444, 0.532, 0.639, 0.767, 0.920, 1.104, 1.325, 1.590, 1.908, 2.290, 2.747, 3.297]
                bucket_widths = [JH_max/num_of_buckets] * (num_of_buckets-1)
                
                for j in range( 0, num_of_buckets ):
                    if j == 0:
                        bucket_starts.append( JH_min )
                    else:
                        bucket_starts.append( bucket_starts[-1] + bucket_widths[j-1] )
                        
                #if '1' in B.ID:
                #    print( "bucket_widths", bucket_widths )
                #    print( "bucket_starts", bucket_starts )
                    
                # calculate Probability Density
                for i in range(0, len(B.JH_values)):
                    dropped = False
                    for j in range( 1, num_of_buckets ):
                        if B.JH_values[i] < bucket_starts[j]:
                            Buckets[ j-1 ] += 1
                            dropped = True
                            break
                    if dropped==False and B.JH_values[i]<bucket_starts[-1]+bucket_widths[-1]: # this goes into the last bucket
                        Buckets[-1] += 1
                #print( "Buckets", Buckets )
                # normalize to [0,1] * Bin Altitude
                localMax = max( Buckets )
                for j in range( 0, num_of_buckets ):
                    Buckets[j] = (Buckets[j] / localMax) * (B.Altitude_max-B.Altitude_min) + B.Altitude_min
                # eliminate zero values in case of log scale - only for plotting reasons
                bucket_starts_logscale = bucket_starts.copy()
                Buckets_logscale = Buckets.copy()
                if bucket_starts_logscale[0] <= 0: 
                    #del bucket_starts_logscale[0:2]
                    #del Buckets_logscale[0:2]
                    bucket_starts_logscale[0] = (JH_max / num_of_buckets) / 2
                # expand end of line
                #bucket_starts[num_of_buckets-1] = JH_max                    
                # **** plot Probability Density Function for this bin
                fig_log.add_trace( go.Scatter(x=bucket_starts_logscale, y=Buckets_logscale, mode='lines', line=dict(color=currentColor,width=6,dash=LineType), opacity=1-LineFade, showlegend=False), row=1, col=SubPlotIdx)
                fig_lin.add_trace( go.Scatter(x=bucket_starts,          y=Buckets,          mode='lines', line=dict(color=currentColor,width=6,dash=LineType), opacity=1-LineFade, showlegend=False), row=1, col=SubPlotIdx)
                #print( ">>>> bucket values: ", Buckets[0], Buckets[1] )
            
                # **** add visuals for the median line
                Percentile50 = B.JH_median #np.percentile(B.JH_values, 50)
                fig_log.add_trace( go.Scatter(x=[Percentile50,Percentile50], y=[B.Altitude_min,B.Altitude_max], mode='lines', line=dict(color=currentColor,width=6,dash=LineType), opacity=1-LineFade, showlegend=False), row=1, col=SubPlotIdx)
                fig_lin.add_trace( go.Scatter(x=[Percentile50,Percentile50], y=[B.Altitude_min,B.Altitude_max], mode='lines', line=dict(color=currentColor,width=6,dash=LineType), opacity=1-LineFade, showlegend=False), row=1, col=SubPlotIdx)
                # **** add visuals for standard deviation
                fig_log.add_trace( go.Scatter(x=[Percentile50-(B.JH_medianVariance)**(1/2)/2,Percentile50+(B.JH_medianVariance)**(1/2)/2], y=[B.Altitude_min+(B.Altitude_max-B.Altitude_min)/2, B.Altitude_min+(B.Altitude_max-B.Altitude_min)/2], mode='lines', line=dict(color=currentColor,width=4,dash=LineType), opacity=1-LineFade, showlegend=False), row=1, col=SubPlotIdx)            
                fig_lin.add_trace( go.Scatter(x=[Percentile50-(B.JH_medianVariance)**(1/2)/2,Percentile50+(B.JH_medianVariance)**(1/2)/2], y=[B.Altitude_min+(B.Altitude_max-B.Altitude_min)/2, B.Altitude_min+(B.Altitude_max-B.Altitude_min)/2], mode='lines', line=dict(color=currentColor,width=4,dash=LineType), opacity=1-LineFade, showlegend=False), row=1, col=SubPlotIdx)            

    # update layout
    fig_log.update_layout( annotations=BinAnnotations )
    fig_log.update_layout( shapes=FigureShapes )
    fig_log.update_layout( title=getBinDescription(RegionName) + "<br>" + Variable_toPlot_longname + " (" + new_units + "). Probability Density for TIEGCM grid (solid) and for ORBIT (dotted) ", width=4800, height=1800, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
    fig_log.update_yaxes(title="Altitude (km)", row=1, col=1)
    fig_lin.update_layout( annotations=BinAnnotations )
    fig_lin.update_layout( shapes=FigureShapes )
    fig_lin.update_layout( title=getBinDescription(RegionName) + "<br>" + Variable_toPlot_longname + " (" + new_units + "). Probability Density for TIEGCM grid (solid) and Daedalus orbit (dotted) ", width=4800, height=1800, legend_orientation="h", legend= {'itemsizing': 'constant'}) 
    fig_lin.update_yaxes(title="Altitude (km)", row=1, col=1)
    # increase font size
    fig_log.update_xaxes( tickfont=dict(size=34) )
    fig_log.update_yaxes( tickfont=dict(size=34) )
    fig_lin.update_xaxes( tickfont=dict(size=34) )
    fig_lin.update_yaxes( tickfont=dict(size=34) )
    # ======== plot log scale
    i = 0
    for B in Bins:
        if B.ID.startswith(RegionName) and len(B.JH_values)>0:
            fig_log.update_yaxes(range=[regionAltMin, regionAltMax], row=1, col=i+1)
            fig_log.update_xaxes(type="log", row=1, col=i+1 )
            i = i + 1
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig_log)    
    # ======== plot linear scale
    i = 0
    for B in Bins:
        if B.ID.startswith(RegionName) and len(B.JH_values)>0:
            fig_lin.update_yaxes(range=[regionAltMin, regionAltMax], row=1, col=i+1)
            fig_lin.update_xaxes(range=[JH_min, JH_max], row=1, col=i+1 )
            i = i + 1
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig_lin)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def WriteListToTextFile(TheList, TheFilename):
    fd = open(TheFilename, "w") 
    for i in range(0, len(TheList)):
        fd.write( str(TheList[i]) + "\n" )
    fd.close() 


def execute_stat_test( TIEGCMresults_filename, ORBITresults_filename, RegionName, VariableToLoad, number_of_samples=50 ):
    """
    Executes several statistical tests in order to compare the distributions of two data sets.
    (Z-test, Wilcoxon, scipy-ranksums, mannwhitneyu)
    The results are printed as text on screen
    """
    
    # create temporary folder
    if( os.path.exists("../RESULTS/tmp/") == False ): os.makedirs("../RESULTS/tmp/")
    
    # Region info:
    print("REGION =", RegionName )

    # number of samples to be taken from each data set. Set to -1 in order to take account all data
    k = number_of_samples
    
    # init data structures to hold the statistical calculations
    Stats1 = dict()
    Stats2 = dict()
    Ztest_means = dict()
    Ztest_medians = dict()
    for B in Bins:
        if B.ID.startswith(RegionName):
            Stats1[( B.ID, "AllData" )] = list()            
            Stats1[( B.ID, "Sample" )] = list()
            Stats1[( B.ID, "Median" )] = 0
            Stats1[( B.ID, "MAD" )] = 0
            Stats1[( B.ID, "Mean" )] = 0
            Stats1[( B.ID, "StDev" )] = 0
            Stats1[( B.ID, "num_of_datapoints" )] = 0
            Stats2[( B.ID, "AllData" )] = list()            
            Stats2[( B.ID, "Sample" )] = list()
            Stats2[( B.ID, "Median" )] = 0
            Stats2[( B.ID, "MAD" )] = 0
            Stats2[( B.ID, "Mean" )] = 0
            Stats2[( B.ID, "StDev" )] = 0
            Stats2[( B.ID, "num_of_datapoints" )] = 0
            Ztest_means[( B.ID, "Z" )] = 0
            Ztest_medians[( B.ID, "Z" )] = 0
    
    # ---------------- Load data set 1
    print("------------ Loading TIEGCM data set:", TIEGCMresults_filename)
    load_results( TIEGCMresults_filename, VariableToLoad, loadGlobalValues=False, loadTimeValues=False, loadMagLatValues=False, loadMLTvalues=False, loadAltValues=False, loadLatValues=False )
    for B in Bins:
        if B.ID.startswith(RegionName):
            if len(B.JH_values) > 0: WriteListToTextFile(B.JH_values, "../RESULTS/tmp/dataset1_"+B.ID+".txt")
            Stats1[( B.ID, "AllData" )] = B.JH_values.copy()
    # reduce data to samples
    if k > 0:
        for B in Bins:
            if B.ID.startswith(RegionName):
                if len(B.JH_values) > k:
                    B.JH_values = random.sample(B.JH_values, k) 
                    Stats1[( B.ID, "Sample" )] = B.JH_values.copy()
                    #print("-------- TIEGCM", B.ID, "--------")
                    #print( Stats1[( B.ID, "Sample" )] )
                else:
                    Stats1[( B.ID, "Sample" )] = B.JH_values.copy()
                    print( "WARNING:", B.ID, "has a only", len(B.JH_values), "items,  which is less than number of samples." )
        CalculateStatsOnData()
        print("Data reduced to a sample of", k)
    for B in Bins:
        if B.ID.startswith(RegionName):
            Stats1[( B.ID, "Median" )] = B.JH_median
            Stats1[( B.ID, "Mean" )] = B.JH_mean
            Stats1[( B.ID, "StDev" )] = math.sqrt( B.JH_variance )
            Stats1[( B.ID, "MAD" )] = B.JH_medianAbsDev
            Stats1[( B.ID, "num_of_datapoints" )] = len( B.JH_values )
            print( " ", B.ID, " Mean =", "{:.3e}".format(Stats1[( B.ID, "Mean" )]), " StDev =", "{:.3e}".format(Stats1[( B.ID, "StDev" )]), " Median =", "{:.3e}".format(Stats1[( B.ID, "Median" )]), " MAD =","{:.3e}".format(Stats1[( B.ID, "MAD" )]), " points =",Stats1[(B.ID, "num_of_datapoints" )] )
            
            
    # ---------------- Load data set 2
    print("------------ Loading ORBIT data set:", ORBITresults_filename)
    for B in Bins:
        B.reset()
    load_results( ORBITresults_filename, VariableToLoad, loadGlobalValues=False, loadTimeValues=False, loadMagLatValues=False, loadMLTvalues=False, loadAltValues=False, loadLatValues=False )
    for B in Bins:
        if B.ID.startswith(RegionName):
            if len(B.JH_values) > 0: WriteListToTextFile(B.JH_values, "../RESULTS/tmp/dataset2_"+B.ID+".txt")
            Stats2[( B.ID, "AllData" )] = B.JH_values.copy()
    # reduce data to samples
    if k > 0:
        for B in Bins:
            if B.ID.startswith(RegionName):
                if len(B.JH_values) > k:
                    B.JH_values = random.sample(B.JH_values, k) 
                    Stats2[( B.ID, "Sample" )] = B.JH_values.copy()
                    #print("-------- Orbit", B.ID, "--------")
                    #print( Stats2[( B.ID, "Sample" )] )
                else:
                    Stats2[( B.ID, "Sample" )] = B.JH_values.copy()
                    print( "WARNING:", B.ID, "has a only", len(B.JH_values), "items,  which is less than number of samples." )
        CalculateStatsOnData()
        print("Data reduces to a sample of", k)
    for B in Bins:
        if B.ID.startswith(RegionName):
            Stats2[( B.ID, "Median" )] = B.JH_median
            Stats2[( B.ID, "Mean" )] = B.JH_mean
            Stats2[( B.ID, "StDev" )] = math.sqrt( B.JH_variance )
            Stats2[( B.ID, "MAD" )] = B.JH_medianAbsDev
            Stats2[( B.ID, "num_of_datapoints" )] = len( B.JH_values )
            print( " ", B.ID, " Mean =", "{:.3e}".format(Stats2[( B.ID, "Mean" )]), " StDev =", "{:.3e}".format(Stats2[( B.ID, "StDev" )]), " Median =", "{:.3e}".format(Stats2[( B.ID, "Median" )]), " MAD =","{:.3e}".format(Stats2[( B.ID, "MAD" )]), " points =", Stats2[(B.ID, "num_of_datapoints" )] )
            
    ''' testing with numbers from the example
    for B in Bins:
        if B.ID.startswith(RegionName):            
            Stats1[( B.ID, "Mean" )] = 51.5 
            Stats2[( B.ID, "Mean" )] = 39.5 
    
            Stats1[( B.ID, "StDev" )] = 8
            Stats2[( B.ID, "StDev" )] = 7

            Stats1[( B.ID, "num_of_datapoints" )] = 25
            Stats2[( B.ID, "num_of_datapoints" )] = 25
    '''
    
    # ######## Execute the Z-test http://homework.uoregon.edu/pub/class/es202/ztest.html
    print("\n", "Z-test (wikipedia)")
    for B in Bins:
        if B.ID.startswith(RegionName):
            # ------------ for mean values
            a = Stats1[( B.ID, "Mean" )] - Stats2[( B.ID, "Mean" )]
            try:
                s1 = Stats1[( B.ID, "StDev" )] / math.sqrt( Stats1[( B.ID, "num_of_datapoints" )] )
            except:
                s1 = 0
            try:
                s2 = Stats2[( B.ID, "StDev" )] / math.sqrt( Stats2[( B.ID, "num_of_datapoints" )] )
            except:
                s2 = 0
            b = math.sqrt( s1**2 + s2**2 )
            if b!=0: Ztest_means[( B.ID, "Z" )] = a / b
            #if b!=0: print("s1=",s1, "  s2=",s2, "  a=",a, "  b=",b, " z=", a/b)
            # ------------ for median values
            a = Stats1[( B.ID, "Median" )] - Stats2[( B.ID, "Median" )]
            try:
                s1 = Stats1[( B.ID, "MAD" )] / math.sqrt( Stats1[( B.ID, "num_of_datapoints" )] )
            except:
                s1 = 0
            try:
                s2 = Stats2[( B.ID, "MAD" )] / math.sqrt( Stats2[( B.ID, "num_of_datapoints" )] )
            except:
                s2 = 0
            b = math.sqrt( s1**2 + s2**2 )
            if b!=0 : Ztest_medians[( B.ID, "Z" )] = a / b
            # ----------------- from wikipedia
            try:
                SE = Stats1[( B.ID, "StDev" )] / math.sqrt( Stats2[( B.ID, "num_of_datapoints" )] )
                z = (Stats2[( B.ID, "Mean" )] - Stats1[( B.ID, "Mean" )]) / SE
                print( "\t", B.ID, "Z =", z )
            except:
                print( "\t", B.ID, "Z = NaN",  )
            
    # display results of the z-test
    print("\nZ-test results for region", RegionName, ":")
    for B in Bins:
        if B.ID.startswith(RegionName) and len(B.JH_values)>0:
            print("   ", B.ID, "  ", B.Kp_min,"<Kp<",B.Kp_max, "  ", B.Altitude_min,"<Alt<",B.Altitude_max, "   Z of means =", "{:.3f}".format(Ztest_means[( B.ID, "Z" )]), "   Z of medians =", "{:.3f}".format(Ztest_medians[( B.ID, "Z" )]) )
        
    # ############ execute Wilcoxon test
    #Stats1[( "AEM_L2", "Sample" )] = [2.5951188e-08, 5.3817932e-09, 4.5183768e-08, 1.551039e-10, 1.0724093e-09, 4.962505e-09, 5.4119514e-10, 3.945805e-09, 5.9539945e-10, 1.8923414e-08, 1.960878e-09, 4.055865e-09, 1.7519519e-10, 1.3301345e-08, 1.2372746e-07, 1.2138809e-08, 8.16415e-09, 3.289174e-10, 8.7328536e-09, 3.827526e-08, 5.4933094e-09, 3.4882688e-09, 1.7631713e-08, 4.8599507e-09, 1.0905276e-09, 6.7475585e-09, 5.2583008e-08, 1.3054376e-08, 2.8305527e-09, 3.3543217e-09, 6.1289263e-09, 2.352899e-08, 2.0256745e-09, 6.2435213e-09, 1.1858019e-08, 8.533459e-09, 2.687838e-09, 1.875761e-08, 9.90745e-12, 4.014579e-10, 5.657707e-10, 4.473683e-09, 4.9620965e-09, 1.695748e-09, 1.5530714e-08, 5.283186e-10, 2.5974272e-09, 1.3884176e-08, 5.4488223e-09, 1.8228039e-09]
    #Stats1[( "AEM_L3", "Sample" )] = [2.925222e-08, 2.8446618e-09, 1.2962599e-08, 4.0733735e-08, 1.13316e-08, 3.9474628e-08, 1.04909297e-10, 1.15847726e-07, 1.0136927e-09, 1.9383768e-10, 6.831934e-09, 1.0782474e-08, 1.2424795e-10, 4.196759e-09, 5.1174908e-08, 1.7030825e-08, 1.0095899e-08, 1.1140663e-08, 4.077417e-09, 9.559168e-09, 4.920846e-08, 2.398426e-08, 1.690071e-08, 2.2489953e-08, 9.672096e-12, 1.4901229e-10, 1.8795976e-09, 3.1964256e-10, 1.7421792e-09, 4.656256e-09, 7.853907e-09, 1.7165107e-08, 9.6540695e-09, 3.952511e-09, 1.9861e-09, 5.2326378e-08, 6.117663e-09, 1.224011e-08, 7.4337563e-09, 5.351637e-08, 1.4914312e-08, 5.9796363e-09, 2.1843855e-08, 2.0803566e-10, 9.217002e-09, 1.5518825e-08, 3.8406185e-09, 3.002403e-08, 2.3402782e-08, 1.03541e-08]
    #Stats2[( "AEM_L2", "Sample" )] = [2.0343393e-08, 2.32117e-09, 2.813346e-08, 1.3160446e-08, 3.800517e-11, 7.743971e-09, 6.345863e-10, 2.7468875e-08, 4.077262e-08, 4.4672564e-08, 5.474968e-10, 1.2188225e-10, 3.517082e-08, 8.0183016e-10, 6.559348e-10, 5.1463047e-09, 1.8888866e-08, 1.3424133e-09, 1.0823237e-08, 4.31503e-10, 2.7409655e-08, 1.0387256e-08, 1.2501109e-08, 1.1267671e-09, 5.51157e-10, 4.859329e-09, 2.7400797e-09, 2.6947452e-08, 4.282332e-09, 1.0266081e-10, 1.7017069e-08, 3.041313e-10, 1.6484906e-08, 1.4166748e-09, 1.649007e-09, 1.0126844e-09, 6.2378396e-09, 8.235802e-11, 6.797095e-09, 5.0539932e-09, 5.7199996e-09, 1.6371768e-09, 3.067749e-10, 2.7308031e-09, 2.9056872e-09, 1.0407587e-09, 5.1806275e-09, 4.0906154e-09, 4.3983903e-08, 2.6597846e-10]
    #Stats2[( "AEM_L3", "Sample" )] = [9.518898e-09, 1.27464e-09, 3.8833985e-08, 1.4651571e-09, 2.8009433e-09, 1.3584062e-09, 6.11956e-09, 3.107995e-09, 4.24684e-09, 3.2873103e-08, 8.475515e-09, 4.165824e-09, 3.908122e-08, 7.2805566e-09, 4.0665938e-08, 1.7837495e-08, 1.8128925e-09, 5.285636e-08, 6.3407826e-09, 5.5626117e-09, 1.4412362e-07, 1.7359745e-09, 2.1320249e-08, 1.463807e-08, 2.950494e-09, 5.9469514e-08, 1.0799843e-08, 8.250815e-09, 4.218044e-08, 6.5836275e-10, 5.35778e-10, 1.9661668e-08, 1.4192106e-07, 4.732321e-09, 1.7882544e-10, 1.223656e-08, 6.950843e-11, 6.5227748e-09, 8.1680875e-09, 7.553436e-09, 7.1417494e-10, 1.8003114e-08, 3.772138e-09, 1.3795659e-08, 8.2685325e-09, 2.240433e-10, 9.484356e-09, 3.31965e-08, 2.0636206e-08, 4.9476892e-08]
    print("\nWilcoxon-test results for region", RegionName, ":")
    for B in Bins:
        if B.ID.startswith(RegionName) and len(B.JH_values)>0:
            # calculate diference of each pair
            Diffs = list()
            Signs = list()
            for i in range(0, k):
                if i < len(Stats2[( B.ID, "Sample" )])  and  i < len(Stats1[( B.ID, "Sample" )]):
                    n = Stats2[( B.ID, "Sample" )][i] - Stats1[( B.ID, "Sample" )][i]
                    if n > 0:
                        Diffs.append( abs(n) )
                        Signs.append( 1 )
                    elif n < 0:
                        Diffs.append( abs(n) )
                        Signs.append( -1 ) 
            # sort diferrences
            zipped = list(zip(Diffs, Signs))
            zipped.sort()
            Diffs, Signs = zip(*zipped)
            Diffs = list(Diffs)
            Signs = list(Signs)
            #  calculate W
            W = 0
            Wplus = 0
            Wminus = 0
            for i in range(0, len(Diffs)):
                W += Signs[i] * (i+1)
                if Signs[i] == +1: Wplus  += (i+1)
                if Signs[i] == -1: Wminus += (i+1)
            # calculate variance etc for the W distribution
            N = len(Diffs)
            W_variance = N*(N+1)*(2*N+1)/6
            W_stdev = math.sqrt(W_variance)
            W_score = W / W_stdev
            # display
            print("   ", B.ID, " ", B.Kp_min,"<Kp<",B.Kp_max, " ", B.Altitude_min,"<Alt<",B.Altitude_max, "  Wplus =", Wplus, " Wminus =", Wminus, "  W =", W, " W-score =", W_score )

    # ############ execute scipy-ranksums test (Compute the Wilcoxon rank-sum statistic for two samples) https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ranksums.html
    print("\nscipy-ranksums-test results for region", RegionName, ":")
    for B in Bins:
        if B.ID.startswith(RegionName) and len(B.JH_values)>0:
            TestStatistic, Pvalue = ranksums( Stats1[( B.ID, "AllData" )], Stats2[( B.ID, "AllData" )] )
            print(" ", B.ID, B.Kp_min,"<Kp<",B.Kp_max, B.Altitude_min,"<Alt<",B.Altitude_max, "DataLen:", len(Stats1[( B.ID, "AllData" )]), "&" ,len(Stats2[( B.ID, "AllData" )]) ,"TestStatistic =", TestStatistic, "Pvalue =", Pvalue)
    # ############ execute mannwhitneyu-test. Mann–Whitney U test, also called Mann–Whitney–Wilcoxon.  https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html#scipy.stats.mannwhitneyu
    print("\nmannwhitneyu-test results for region", RegionName, ":")
    for B in Bins:
        if B.ID.startswith(RegionName) and len(B.JH_values)>0:
            print(" ", B.ID, B.Kp_min,"<Kp<",B.Kp_max, B.Altitude_min,"<Alt<",B.Altitude_max, "DataLen:", len(Stats1[( B.ID, "AllData" )]), "&" ,len(Stats2[( B.ID, "AllData" )]))
            TestStatistic, Pvalue = mannwhitneyu( Stats1[( B.ID, "AllData" )], Stats2[( B.ID, "AllData" )], use_continuity=True, alternative='two-sided' )
            print( "     Continuity=True Alternative=two-sided:",  "  TestStatistic =", TestStatistic, "Pvalue =", Pvalue)
            TestStatistic, Pvalue = mannwhitneyu( Stats1[( B.ID, "AllData" )], Stats2[( B.ID, "AllData" )], use_continuity=True, alternative='less' )
            print( "     Continuity=True Alternative=less:     ",  "  TestStatistic =", TestStatistic, "Pvalue =", Pvalue)
            TestStatistic, Pvalue = mannwhitneyu( Stats1[( B.ID, "AllData" )], Stats2[( B.ID, "AllData" )], use_continuity=True, alternative='greater' )
            print( "     Continuity=True Alternative=greater:  ",  "  TestStatistic =", TestStatistic, "Pvalue =", Pvalue)
            TestStatistic, Pvalue = mannwhitneyu( Stats1[( B.ID, "AllData" )], Stats2[( B.ID, "AllData" )], use_continuity=False, alternative='two-sided' )
            print( "     Continuity=False Alternative=two-sided:",  "  TestStatistic =", TestStatistic, "Pvalue =", Pvalue)
            TestStatistic, Pvalue = mannwhitneyu( Stats1[( B.ID, "AllData" )], Stats2[( B.ID, "AllData" )], use_continuity=False, alternative='less' )
            print( "     Continuity=False Alternative=less:     ",  "  TestStatistic =", TestStatistic, "Pvalue =", Pvalue)
            TestStatistic, Pvalue = mannwhitneyu( Stats1[( B.ID, "AllData" )], Stats2[( B.ID, "AllData" )], use_continuity=False, alternative='greater' )
            print( "     Continuity=False Alternative=greater:  ",  "  TestStatistic =", TestStatistic, "Pvalue =", Pvalue)
     
    # clean up
    for f in glob.glob("RESULTS/tmp/*.txt"):
        os.remove(f)
            
            
            
            
            
            
            
  








    
Profiles = dict()    
MLTsequence = list()
ALTsequence = list()
MLT_duration_of_a_profile = 0
ALT_distance_of_a_bucket = 0
regionMLTmax = 0
regionMLTmin = 0
ProfilesUpdateLock = threading.Lock()   
class Thread_AltProfBinner (threading.Thread):
    def __init__(self, from_idx, to_idx):
        threading.Thread.__init__(self)
        self.from_idx = from_idx
        self.to_idx = to_idx
    def run(self):
        global Profiles
        for i in range( self.from_idx, self.to_idx ):
            mlt_to_fall = alt_to_fall = -1  
            # find correct Alt
            for seq_idx in range(0, len(ALTsequence)):
                if all_Altitude_values[i]>=ALTsequence[seq_idx] and all_Altitude_values[i]<ALTsequence[seq_idx]+ALT_distance_of_a_bucket:
                    alt_to_fall=ALTsequence[seq_idx]
                    break
            if alt_to_fall == -1: continue # ignore highest altitudes        
            # find correct kp
            if all_Kp_values[i] < 3: 
                kp_to_fall = 0
            else:
                kp_to_fall = 3
            # find correct MLT
            MLT_tocheck = all_MLT_values[i]
            if regionMLTmax>24  and  MLT_tocheck<=regionMLTmax-24:
                MLT_tocheck += 24
            for seq_idx in range(0, len(MLTsequence)):
                if MLT_tocheck>=MLTsequence[seq_idx] and MLT_tocheck<MLTsequence[seq_idx]+MLT_duration_of_a_profile: 
                    mlt_to_fall=MLTsequence[seq_idx]
                    break
            if MLT_tocheck == MLTsequence[len(MLTsequence)-1]+MLT_duration_of_a_profile: mlt_to_fall = MLTsequence[len(MLTsequence)-1] # for last MLT position
            # store the value at the right place
            #ProfilesUpdateLock.acquire()
            if all_JH_values[ i ] > 10: print("!!!!!!!!!!!!!!!! JH=",all_JH_values[ i ], "at",i, kp_to_fall, mlt_to_fall, alt_to_fall)
            Profiles[ (kp_to_fall, mlt_to_fall, alt_to_fall) ].append( all_JH_values[ i ] )
            #ProfilesUpdateLock.release()   

    
def plotAltProfiles_perKpRange(RegionName, Variable_toPlot, x_axis_min, x_axis_max, MultiplicationFactor, PlotTitle, Units_of_Variable=""):
    """
    Creates a plot depicting the altitude profiles of the data as calculated for each bin.
    For each Bin the 10th, 25th, 50th, 75ht and 90th percentiles are displayed. 
    Sub-figures are created for low and high Kp-index and of different Magnetic Local Time ranges.
    
    Args:
        RegionName: the name of the Region of Interest as defined in the Data.  
        Variable_toPlot: the name of the variable to be plotted.  
        x_axis_min: the minimum value for the horizontal axis.  
        x_axis_max: the maximum value for the horizontal axis.  
        MultiplicationFactor: All values will be multiplied by this one before plotting.  
        PlotTitle: the title to be displayed on top of the plot.  
        Units_of_Variable: the units.
    """
    global Profiles, MLTsequence, ALTsequence, MLT_duration_of_a_profile, ALT_distance_of_a_bucket, regionMLTmax, regionMLTmin
    # init parameters
    if len(Units_of_Variable)==0:
        if Variable_toPlot == "Ohmic":
            Units_of_Variable = "W/m^3"
        elif Variable_toPlot == "DEN":
            Units_of_Variable = "g/cm^3"    
        elif Variable_toPlot == "SIGMA_PED" or Variable_toPlot == "SIGMA_HAL":
            Units_of_Variable = "S/m"
        elif Variable_toPlot == "Convection_heating" or Variable_toPlot == "Wind_heating":
            Units_of_Variable = "W/m^3"           
        elif Variable_toPlot == "EEX" or Variable_toPlot == "EEY":
            Units_of_Variable = "V/m"      
        else:
            Units_of_Variable = "?" 

    x_axes_range = [ x_axis_min, x_axis_max]        
    
    # Region specific binning:
    regionMLTmin = 999
    regionMLTmax = -999
    regionALTmin = 999
    regionALTmax = -999
    for B in Bins:
        if B.ID.startswith( RegionName ):
            if regionMLTmin>B.MLT_min: regionMLTmin = B.MLT_min
            if regionMLTmax<B.MLT_max: regionMLTmax = B.MLT_max
            if regionALTmin>B.Altitude_min: regionALTmin = B.Altitude_min
            if regionALTmax<B.Altitude_max: regionALTmax = B.Altitude_max
    if regionMLTmax <= regionMLTmin: regionMLTmax += 24
        
    # find lowest altitude
    LowestAltitude = 999999
    for i in range(0, len(all_Altitude_values)):
        if LowestAltitude > all_Altitude_values[i]: LowestAltitude = all_Altitude_values[i]
    
    # init data structures
    Profiles = dict()
    if "TRO" in RegionName:
        MLT_duration_of_a_profile = 3        
    else:
        MLT_duration_of_a_profile = 6
    ALT_distance_of_a_bucket  = 5
    MLTsequence     = list( range( regionMLTmin, regionMLTmax, MLT_duration_of_a_profile) )
    ALTsequence     = list( range( regionALTmin, regionALTmax, ALT_distance_of_a_bucket ) )
    KPsequence      = [ 0, 3 ] 
    for aMLT in MLTsequence:
        for anALT in ALTsequence:
            for aKP in KPsequence:
                Profiles[(aKP, aMLT, anALT)] = list()

    print( "Parsing", len(all_JH_values), "values.", datetime.now().strftime("%d-%m-%Y %H:%M:%S") )
    # parse all values and decide into which sum they must fall
    AllThreads = list()
    positions_per_thread = int ( len(all_JH_values) / 10 )
    from_pos = 0
    while from_pos < len(all_JH_values):
        # calculate boundaries for thread
        to_pos = from_pos + positions_per_thread
        if to_pos >= len(all_JH_values): to_pos = len(all_JH_values)-1
        if len(all_JH_values)-to_pos<positions_per_thread : to_pos = len(all_JH_values)-1
        # spawn new thread
        print("Thread:", from_pos, "-", to_pos, " of " ,len(all_JH_values), "positions")
        T = Thread_AltProfBinner(from_pos, to_pos)
        AllThreads.append(T)
        T.start()
        # go on
        from_pos += positions_per_thread
        
    # wait for all threads to terminate
    for T in AllThreads: T.join()

    # plot
    Color10 = '#c4dfe6'
    Color25 = '#a1d6e2'
    Color50 = '#1995ad'
    Color75 = '#a1d6e2'
    Color90 = '#c4dfe6'
    
    # construct the column MLT titles #("0-3", "3-6", "6-9", "9-12", "12-15", "15-18", "18-21", "21-24")
    ColumnTitles = list()
    
    for i in range(0, len(MLTsequence)):
        ColumnTitles.append( "MLT " + str(MLTsequence[i]) + "-"  + str(MLTsequence[i]+MLT_duration_of_a_profile) )
    # define secondary y-axis at the right of the plot
    mySpecs = list()
    for row in range(0, len(KPsequence)):
        mySpecs.append( list() )
        for col in range(0, len(MLTsequence)):
            mySpecs[row].append( {"secondary_y": True} )
        
    #make plot
    fig = make_subplots(rows=len(KPsequence), cols=len(MLTsequence), shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.035, horizontal_spacing=0.01, subplot_titles=ColumnTitles, specs=mySpecs)
    for aKP in KPsequence:
        for aMLT in MLTsequence:
            #Means = list()
            Percentiles10 = list()
            Percentiles25 = list()
            Percentiles50 = list()            
            Percentiles75 = list()
            Percentiles90 = list()
            visibleALTsequence = list()
            hits  = 0
            for anALT in ALTsequence:
                print("  ", anALT, "km     hits =",  len(Profiles[(aKP, aMLT, anALT)]))
                hits += len(Profiles[(aKP, aMLT, anALT)])
                if len(Profiles[(aKP, aMLT, anALT)]) > 0:
                    #Means.append(  sum(Profiles[(aKP, aMLT, anALT)]) / len(Profiles[(aKP, aMLT, anALT)]) )
                    Percentiles10.append( np.percentile(Profiles[(aKP, aMLT, anALT)], 10) )
                    Percentiles25.append( np.percentile(Profiles[(aKP, aMLT, anALT)], 25) )
                    Percentiles50.append( np.percentile(Profiles[(aKP, aMLT, anALT)], 50) )                    
                    Percentiles75.append( np.percentile(Profiles[(aKP, aMLT, anALT)], 75) )
                    Percentiles90.append( np.percentile(Profiles[(aKP, aMLT, anALT)], 90) )
                    visibleALTsequence.append( anALT )
                #else:
                    #Means.append( 0 )
                    #Percentiles10.append( 0 )
                    #Percentiles25.append( 0 )
                    #Percentiles50.append( 0 )                    
                    #Percentiles75.append( 0 )
                    #Percentiles90.append( 0 )
            print( "Kp = ", aKP, "MLT =", aMLT, "   Hits =", hits, "  ", datetime.now().strftime("%d-%m-%Y %H:%M:%S") )
            
            # change units
            for i in range(0,len(Percentiles50)): 
                #Means[i] *= MultiplicationFactor
                Percentiles10[i] *= MultiplicationFactor
                Percentiles25[i] *= MultiplicationFactor
                Percentiles50[i] *= MultiplicationFactor
                Percentiles75[i] *= MultiplicationFactor
                Percentiles90[i] *= MultiplicationFactor
            
            # alter visibleALTsequence so that data are displayed correctly
            '''
            for i in range(0, len(visibleALTsequence)):
                visibleALTsequence[i] += ALT_distance_of_a_bucket/2
            '''                
            #for anALT in ALTsequence:
            #    if len(Profiles[(aKP, aMLT, anALT)]) > 0:
            #        visibleALTsequence[0]  = anALT #regionALTmin
            #        break
            '''
            visibleALTsequence[0] = LowestAltitude
            '''
            try:
                visibleALTsequence[-1] = regionALTmax
            except:
                pass
            #print( visibleALTsequence )
            
            fig.add_trace( go.Scatter(x=[0]*len(visibleALTsequence), y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color10, line=dict(color='gray',width=1,), showlegend=False), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1 )
            fig.add_trace( go.Scatter(x=Percentiles10, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color10, line=dict(color='gray',width=1,), showlegend=False), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1 )
            fig.add_trace( go.Scatter(x=Percentiles25, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color25, line=dict(color='gray',width=1,), showlegend=False), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1 )
            fig.add_trace( go.Scatter(x=Percentiles50, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color50, line=dict(color='black',width=2,), showlegend=False), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1 )
            # plot mean
            #fig.add_trace( go.Scatter(x=Means, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor='black', line=dict(color='black',width=1,), showlegend=False), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1 )
            # plot percentiles
            fig.add_trace( go.Scatter(x=Percentiles75, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color75, line=dict(color='gray',width=1,), showlegend=False), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1 )
            fig.add_trace( go.Scatter(x=Percentiles90, y=visibleALTsequence, mode='lines', fill='tonexty', fillcolor=Color90, line=dict(color='gray',width=1,), showlegend=False), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1,  )
            # add a trace in order to display secondary y-axis at the right
            fig.add_trace( go.Scatter(x=[-1000], y=[-1000], showlegend=False), row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1, secondary_y=True )
            
    # display legends
    fig.add_trace( go.Scatter(name='90th Perc.', x=[-10], y=[-10], mode='lines', fill='tonexty', fillcolor=Color90, line=dict(color=Color90,width=1,), showlegend=True), row=1, col=1 )
    fig.add_trace( go.Scatter(name='75th Perc.', x=[-10], y=[-10], mode='lines', fill='tonexty', fillcolor=Color75, line=dict(color=Color75,width=1,), showlegend=True), row=1, col=1 )
    fig.add_trace( go.Scatter(name='50th Perc.', x=[-10], y=[-10], mode='lines', fill='tonexty', fillcolor=Color50, line=dict(color=Color50,width=2,), showlegend=True), row=1, col=MLTsequence.index(aMLT)+1 )
    fig.add_trace( go.Scatter(name='25th Perc.', x=[-10], y=[-10], mode='lines', fill='tonexty', fillcolor=Color25, line=dict(color=Color25,width=1,), showlegend=True), row=1, col=1 )
    fig.add_trace( go.Scatter(name='10th Perc.', x=[-10], y=[-10], mode='lines', fill='tonexty', fillcolor=Color10, line=dict(color=Color10,width=1,), showlegend=True), row=1, col=1 )
    
    #fig.update_yaxes( title="Altitude(km)" )
    for aKP in KPsequence:
        fig.update_yaxes( title_text="Altitude (km)", row=KPsequence.index(aKP)+1, col=1, side='left', secondary_y=False)
        row_title = "Kp " + str(aKP) + " - "
        if aKP == 0:
            row_title +=  "3"
        elif aKP == 3:
            row_title +=  "9"
        else:
            row_title +=  "?"
        fig.update_yaxes( title_text=row_title, row=KPsequence.index(aKP)+1, col=len(MLTsequence),  side='right', secondary_y=True, showticklabels=False )
        for aMLT in MLTsequence:
            fig.update_yaxes( row=KPsequence.index(aKP)+1, col=MLTsequence.index(aMLT)+1, secondary_y=True, showticklabels=False )
    fig.update_xaxes( range=x_axes_range )
    fig.update_yaxes( range=[80, 160], dtick=10 )  
    fig.update_layout( title = PlotTitle,
                       width=250+len(MLTsequence)*300, height=200+260*len(KPsequence) , legend_orientation="h", legend_y=-0.04) 
    
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot(fig) 





            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
