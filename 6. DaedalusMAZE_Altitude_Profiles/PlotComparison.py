import Data as D


import numpy as np
import plotly
import chart_studio.plotly as py 
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import scipy.io

def plot_AltProfiles_Comparison( ResultFilename1, ResultFilename2, VariableName, x_axis_min, x_axis_max, MultiplicationFactor=1, Units="", SuperTitle="" ):
    """
    Creates a plot depicting the altitude profiles of two result files at the same time in order to compare them.
    For each Bin the median value is displayed.
    
    Args:
        ResultFilename1: a results netcdf filename
        ResultFilename2: a results netcdf filename
        VariableName: a name of the variable used for the calculations
        x_axis_min: the minimum value for the horizontal axis
        y_axis_max: the maximum value for the horizontal axis
        MultiplicationFactor: All values will be multiplied by this one before plotting
        Units: to be displayed on the plot.
        SuperTitle: to be displayed on top of the plot.
    """
    
    # Read data from the first result file
    if ResultFilename1[-3:] == ".nc" or ResultFilename1[-4:] == ".cdf" : # it is a netcdf file
        Bins, BinSums, BinLens, VariableName, Units = D.LoadResultsCDF( ResultFilename1 )
    elif ResultFilename1[-4:] == ".mat": # it is a matlab  file
        pass
    
    # Read data from the second result file
    if ResultFilename2[-3:] == ".nc" or ResultFilename2[-4:] == ".cdf" : # it is a netcdf file
        Bins2, BinSums2, BinLens2, VariableName2, Units2 = D.LoadResultsCDF( ResultFilename2 )
    elif ResultFilename2[-4:] == ".mat": # it is a matlab  file
        pass
    
    
    # alter visibleALTsequence so that the point is displayed in the middle of the sub-bin
    visibleALTsequence = D.ALTsequence.copy()
    for i in range(1, len(visibleALTsequence)-1):
        visibleALTsequence[i] += D.ALT_distance_of_a_bin/2
    visibleALTsequence[0] = D.ALTsequence[0]
    visibleALTsequence[-1] = D.ALTsequence[-1] + D.ALT_distance_of_a_bin
    
    # plot
    Color1 = '#79C000' #'#B1624E' #'#FC766A' #'rgba(25, 149, 173, 0.2)' 
    Color2 = '#FF7F41' #'#5CC8D7' #'#5B84B1' #'rgba(0, 140, 120, 0.2)' 
    
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
            Values1 = list()            
            Values2 = list()            
            
            # compute percentiles
            for anALT in D.ALTsequence:
                if ResultFilename1[-4:] == ".mat":  # it is a matlab  file
                    Values1.append( get_MATLAB_value( ResultFilename1, VariableName, aKP, anALT, aMLT) * MultiplicationFactor )
                else: # it is a netcdf file
                    Values1.append( Bins[aKP, anALT, D.LAT_min, aMLT, "Percentile50"] * MultiplicationFactor )
                    
                if ResultFilename2[-4:] == ".mat":  # it is a matlab  file
                    Values2.append( get_MATLAB_value( ResultFilename2, VariableName, aKP, anALT, aMLT) * MultiplicationFactor )
                else: # it is a netcdf file   
                    Values2.append( Bins2[aKP, anALT, D.LAT_min, aMLT, "Percentile50"] * MultiplicationFactor )
            
            
            fig.add_trace( go.Scatter(x=Values1, y=visibleALTsequence, mode='lines', fill='none', fillcolor=Color1, line=dict(color=Color1,width=3,), showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
            
            fig.add_trace( go.Scatter(x=Values2, y=visibleALTsequence, mode='lines', fill='none', fillcolor=Color2, line=dict(color=Color2,width=3,), showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
            
            # add a trace in order to display secondary y-axis at the right
            fig.add_trace( go.Scatter(x=[-1000], y=[-1000], showlegend=False), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1, secondary_y=True )
            
    ##################################### Format axis, legends etc #########################################################
            
    # display legends
    fig.add_trace( go.Scatter(name='50th Perc.('+ResultFilename1+')', x=[-100], y=[-100], mode='lines', fill='none', fillcolor=Color1, line=dict(color=Color1,width=3,), showlegend=True), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )
    fig.add_trace( go.Scatter(name='50th Perc.('+ResultFilename2+')', x=[-100], y=[-100], mode='lines', fill='none', fillcolor=Color2, line=dict(color=Color2,width=3,), showlegend=True), row=D.KPsequence.index(aKP)+1, col=D.MLTsequence.index(aMLT)+1 )

    # update x axis ranges
    x_axis_range=[x_axis_min, x_axis_max]
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
    
    
    
    
    
    
    
    
    
    
    
    
def get_MATLAB_value( Filename, Variable,    Kp, Altitude, MLT ):
    """
    Reads a matlab File and returns the value of the Variable for a certain Kp, Altitude, MLT combination
    """
    if '/' in Filename: # linux
        struct_name = Filename[Filename.rindex('/')+1:-4]
    elif '\\' in Filename: # windows
        struct_name = Filename[Filename.rindex('\\')+1:-4]
    else:
        struct_name = Filename[:-4]

    Result = 0
    matlabStruct = scipy.io.loadmat( Filename )
    ALTsequence = list(np.array( matlabStruct[ struct_name ][0][0][0] ).flatten() )
    allKPs  = list( np.array( matlabStruct[ struct_name ][0][0][1][0] ) )
    MLTsequence = list( np.array( matlabStruct[ struct_name ][0][0][2][0] )[:-1] )
    KPsequence = [ 0, 2, 4 ]
    if Variable == "Joule Heating":
        allJHs  = np.array( matlabStruct[ struct_name  ][0][0][3] )
        Values = allJHs
    else:
        allPEDs = np.array( matlabStruct[ struct_name  ][0][0][4] )
        Values = allPEDs
    
    
    if MLT > 24: MLT -= 24
    
    try:
        n = KPsequence.index(int(Kp))
    except:
        print(Kp, " >>> ", KPsequence)    
        
    try:
        n = ALTsequence.index(int(Altitude))
    except:
        print(Altitude, " >>> ", ALTsequence)    
        
    try:
        n = MLTsequence.index(int(MLT))
    except:
        print(MLT, " >>> ", MLTsequence)    
    
    
    Result = Values[KPsequence.index(int(Kp)), MLTsequence.index(int(MLT)), ALTsequence.index(int(Altitude)), 2]
    return Result
    
