
'''
This file contains all the necessary funtions to create plots in order to visualize all the calculated quantities.
Functions included in this files are not necessary by any means in calculation of LTI quantities.
User who are going to use productDerivation and ErrorPropagation of DaedalusMASE can use other ways for plot
creation, according to his needs.
'''
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib import ticker
from matplotlib.colors import LogNorm
from cmcrameri import cm
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import factors
my_dpi = 300

# ############################ Vertical Profile Plots ############################

def plot_collisions(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot collission frequencies vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
    Returns plot in live window

    '''
    print("Plotting.....")
    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # mean value of ion collisions
    mean_ion_collisions = (
        factors.nu_Op_sum[lat, lon, :-1] + factors.nu_O2p_sum[lat, lon, :-1] + factors.nu_NOp_sum[lat, lon, :-1]) / 3

    fig1 = go.Figure()

    # adding the various plots
    fig1.add_trace(go.Scatter(x=factors.nu_Op_sum[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νO+", mode='lines',
                              line=dict(shape='spline', color='red')))
    fig1.add_trace(go.Scatter(x=factors.nu_O2p_sum[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νO2+", mode='lines',
                              line=dict(shape='spline', color='blue')))
    fig1.add_trace(go.Scatter(x=factors.nu_NOp_sum[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νNO+", mode='lines',
                              line=dict(shape='spline', color='yellow')))
    fig1.add_trace(go.Scatter(x=mean_ion_collisions, y=factors.heights[lat, lon, :-1], name="νion", mode='lines',
                              line=dict(shape='spline', color='orange')))
    fig1.add_trace(go.Scatter(x=factors.nu_e_sum[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νe", mode='lines',
                              line=dict(shape='spline', color='purple')))
    fig1.add_trace(go.Scatter(x=factors.Omega_ion[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Ωi", mode='lines',
                              line=dict(shape='spline', color='brown')))
    fig1.add_trace(go.Scatter(x=factors.Omega_e[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Ωe", mode='lines',
                              line=dict(shape='spline', color='black')))

    # updating the layout of the figure
    fig1.update_layout(xaxis_type="log", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                       tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 10)), xaxis_title="$Frequency \ (Hz)$",
                       yaxis_title="$Altitude \ (km)$", width=900, height=650,
                       title={'text': 'Collision-Gyro Frequencies' + factors.title, 'y': 0.9, 'x': 0.46, 'xanchor': 'center', 'yanchor': 'top'})

    fig1.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig1.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig1.update_xaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)
    fig1.update_yaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)

    fig1.show()

    
def plot_heating_rates(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Heating Rates vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.Ohmic_Heating[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Ohmic Heating", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.Frictional_Heating[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Frictional Heating", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.Joule_Heating[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Joule Heating", mode='lines',
                             line=dict(shape='spline', color='green')))

    x_range = max(factors.Joule_Heating[lat, lon, :-1])

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 10)), xaxis=dict(range=[0, x_range + x_range/4]),
                      xaxis_title="$(W/m^{3})$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Heating Rates' + factors.title, 'y': 0.9, 'x': 0.41, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()


def plot_conductivities(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot conductivities vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.pedersen_con[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="σPedersen", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.hall_con[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="σHall", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.parallel_con[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="σParallel", mode='lines',
                             line=dict(shape='spline', color='green')))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="log", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 10)), xaxis_title="$(S/m)$", yaxis_title="$Altitude \ (km)$",
                      width=900, height=650,
                      title={'text': 'Conductivities' + factors.title, 'y': 0.9, 'x': 0.41, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()



def plot_currents(lat_value, lon_value, min_alt, max_alt):

    '''
    This function used to plot currents vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.J_pedersen[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Pedersen Current", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.J_hall[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Hall Current", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.J_ohmic[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Ohmic Current", mode='lines',
                             line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=factors.J_dens[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Densities Current", mode='lines',
                             line=dict(shape='spline', color='black')))
    x_range = max(factors.J_ohmic[lat, lon, :-1])
    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 10)), xaxis=dict(range=[0, x_range + x_range/4]),
                      xaxis_title="$(A/m^{2})$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Perpendicular Currents' + factors.title, 'y': 0.9, 'x': 0.45, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()



def plot_cross_sections(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Ctoss Sections vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.C_Op[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="O+", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.C_O2p[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="O2+", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.C_NOp[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="NO+", mode='lines',
                             line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=factors.C_ion[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Avg", mode='lines',
                             line=dict(shape='spline', color='black')))

    x_range = max(factors.C_Op[lat, lon, :-1])

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 10)), xaxis=dict(range=[0, x_range + x_range/4]),
                      xaxis_title="$(m^{2})$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Cross Sections' + factors.title, 'y': 0.9, 'x': 0.42, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()



def plot_collisions_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Collission Frequencies error vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.nuOp_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="$ν_{O^{+}}$ error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.nuO2p_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="$ν_{O2^{+}}$ error", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.nuNOp_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="$ν_{NO^{+}}$ error", mode='lines',
                             line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=factors.nue_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="$ν_{e}$ error", mode='lines',
                             line=dict(shape='spline', color='purple')))

    
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()



def plot_collisions_plus_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Collission Frequencies vertical profile, including Error

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.nuOp_error[lat, lon, :-1] + factors.nu_Op_sum[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νO+ +error",
                             mode='lines', line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.nu_Op_sum[lat, lon, :-1] - factors.nuOp_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νO+ -error",
                             mode='lines', line=dict(shape='spline', color='red', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.nuO2p_error[lat, lon, :-1] + factors.nu_O2p_sum[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νO2+ + error",
                             mode='lines', line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.nu_O2p_sum[lat, lon, :-1] - factors.nuO2p_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νO2+ - error",
                             mode='lines', line=dict(shape='spline', color='blue', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.nuNOp_error[lat, lon, :-1] + factors.nu_NOp_sum[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νNO+ + error",
                             mode='lines', line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=factors.nu_NOp_sum[lat, lon, :-1] - factors.nuNOp_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νNO+ - error",
                             mode='lines', line=dict(shape='spline', color='green', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.nue_error[lat, lon, :-1] + factors.nu_e_sum[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νe + error", mode='lines',
                             line=dict(shape='spline', color='purple')))
    fig.add_trace(go.Scatter(x=factors.nu_e_sum[lat, lon, :-1] - factors.nue_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="νe - error", mode='lines',
                             line=dict(shape='spline', color='purple', dash="dash")))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="log", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="$Frequency \ (Hz)$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Collision Frequencies With Error' + factors.title, 'y': 0.9, 'x': 0.48, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()



def plot_collisions_rel_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Collission Frequencies vertical profile, Relative Error

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    nuOp_rel = factors.nuOp_error[lat, lon,
                                  :-1] / factors.nu_Op_sum[lat, lon, :-1]
    nuO2p_rel = factors.nuO2p_error[lat, lon,
                                    :-1] / factors.nu_O2p_sum[lat, lon, :-1]
    nuNOp_rel = factors.nuNOp_error[lat, lon,
                                    :-1] / factors.nu_NOp_sum[lat, lon, :-1]
    nu_ion = (factors.nu_Op_sum[lat, lon, :-1] + factors.nu_O2p_sum[lat,
              lon, :-1] + factors.nu_NOp_sum[lat, lon, :-1]) / 3
    nuion_error = (factors.nuOp_error[lat, lon, :-1] + factors.nuO2p_error[lat,
                   lon, :-1] + factors.nuNOp_error[lat, lon, :-1]) / 3
    nuion_rel = nuion_error / nu_ion
    nue_rel = factors.nue_error[lat, lon, :-1] / \
        factors.nu_e_sum[lat, lon, :-1]

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=nuOp_rel, y=factors.heights[lat, lon, :-1], name="$ν_{O^{+}}$ error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=nuO2p_rel, y=factors.heights[lat, lon, :-1], name="$ν_{O2^{+}}$ error", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=nuNOp_rel, y=factors.heights[lat, lon, :-1], name="$ν_{NO^{+}}$ error", mode='lines',
                             line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=nue_rel, y=factors.heights[lat, lon, :-1], name="$ν_{e}$ error", mode='lines',
                             line=dict(shape='spline', color='purple')))
    fig.add_trace(go.Scatter(x=nuion_rel, y=factors.heights[lat, lon, :-1], name="$ν_{ion}$ error", mode='lines',
                             line=dict(shape='spline', color='yellow')))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="log", yaxis=dict(range=[min_alt, max_alt], tickmode='array',
                      tickvals=np.arange(min_alt, max_alt + 5, 5)), xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Collision Frequencies Relative Error' + factors.title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()




def plot_collisions_contr(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot cotibution of error of each variable to Collission Frequencies calculation in vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    nu_ion = (factors.nu_Op_sum[lat, lon, :-1] + factors.nu_O2p_sum[lat,
              lon, :-1] + factors.nu_NOp_sum[lat, lon, :-1]) / 3
    nuion_error = (factors.nuOp_error[lat, lon, :-1] + factors.nuO2p_error[lat,
                   lon, :-1] + factors.nuNOp_error[lat, lon, :-1]) / 3
    nuion_rel = nuion_error / nu_ion
    nue_rel = factors.nue_error[lat, lon, :-1] / \
        factors.nu_e_sum[lat, lon, :-1]

    dnui_Tn = factors.dnuion_Tn[lat, lon, :-1] ** (1/2) / nu_ion
    dnui_Ti = factors.dnuion_Ti[lat, lon, :-1] ** (1/2) / nu_ion
    dnui_Nn = factors.dnuion_Nneutral[lat, lon, :-1] ** (1 / 2) / nu_ion

    dnu_e_Te = factors.dnue_Te[lat, lon, :-
                               1] ** (1/2) / factors.nu_e_sum[lat, lon, :-1]
    dnu_e_Nneutral = factors.dnue_Nneutral[lat, lon,
                                           :-1] ** (1/2) / factors.nu_e_sum[lat, lon, :-1]

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=nuion_rel, y=factors.heights[lat, lon, :-1], name="νion error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=dnui_Tn, y=factors.heights[lat, lon, :-1], name="dTn(i)", mode='lines',
                             line=dict(shape='spline', dash="dot", color='red')))
    fig.add_trace(go.Scatter(x=dnui_Ti, y=factors.heights[lat, lon, :-1], name="dTi(i)", mode='lines',
                             line=dict(shape='spline', dash="dash", color='red')))
    fig.add_trace(go.Scatter(x=dnui_Nn, y=factors.heights[lat, lon, :-1], name="dNn(i)", mode='lines',
                             line=dict(shape='spline', dash="dot", color='brown')))

    fig.add_trace(go.Scatter(x=nue_rel, y=factors.heights[lat, lon, :-1], name="νe error", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=dnu_e_Te, y=factors.heights[lat, lon, :-1], name="dTe(e)", mode='lines',
                             line=dict(shape='spline', dash="dot", color='blue')))
    fig.add_trace(go.Scatter(x=dnu_e_Nneutral, y=factors.heights[lat, lon, :-1], name="dNn(e)", mode='lines',
                             line=dict(shape='spline', dash="dash", color='blue')))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)), xaxis_title="",
                      yaxis_title="$Altitude \ (km)$", width=970, height=650,
                      title={'text': 'Collision Frequencies Relative Error Contributions' + factors.title, 'y': 0.9, 'x': 0.51, 'xanchor': 'center',
                             'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()



def plot_heating_rates_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Heating Rates vertical profile
    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.Ohmic_Heating_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Ohmic Heating error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.Frictional_Heating_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Frictional Heating error", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.Joule_Heating_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Joule Heating error", mode='lines',
                             line=dict(shape='spline', color='green')))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="$(W/m^{3})$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Heating Rates Absolute Error' + factors.title, 'y': 0.9, 'x': 0.47, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    

def plot_heating_rates_plus_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Heating Error vertical profile, including Error

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.Ohmic_Heating_error[lat, lon, :-1] + factors.Ohmic_Heating[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Ohmic Heating + error", mode='lines', line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.Ohmic_Heating[lat, lon, :-1] - factors.Ohmic_Heating_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Ohmic Heating - error", mode='lines', line=dict(shape='spline', color='red', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.Frictional_Heating_error[lat, lon, :-1] + factors.Frictional_Heating[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Frictional Heating + error", mode='lines', line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.Frictional_Heating[lat, lon, :-1] - factors.Frictional_Heating_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Frictional Heating - error", mode='lines', line=dict(shape='spline', color='blue', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.Joule_Heating_error[lat, lon, :-1] + factors.Joule_Heating[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Joule Heating + error", mode='lines', line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=factors.Joule_Heating[lat, lon, :-1] - factors.Joule_Heating_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Joule Heating - error", mode='lines', line=dict(shape='spline', color='green', dash="dash")))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="$(W/m^{3})$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Heating Rates With Error' + factors.title, 'y': 0.9, 'x': 0.45, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    

def plot_heating_rates_rel_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Heating Error vertical profile, relative Error

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    Ohmic_rel = factors.Ohmic_Heating_error[lat, lon,
                                            :-1] / factors.Ohmic_Heating[lat, lon, :-1]
    Frict_rel = factors.Frictional_Heating_error[lat, lon,
                                                 :-1] / factors.Frictional_Heating[lat, lon, :-1]
    Joule_rel = factors.Joule_Heating_error[lat, lon,
                                            :-1] / factors.Joule_Heating[lat, lon, :-1]

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=Ohmic_rel, y=factors.heights[lat, lon, :-1], name="Ohmic Heating error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=Frict_rel, y=factors.heights[lat, lon, :-1], name="Frictional Heating error", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=Joule_rel, y=factors.heights[lat, lon, :-1], name="Joule Heating error", mode='lines',
                             line=dict(shape='spline', color='green')))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt], tickmode='array',
                      tickvals=np.arange(min_alt, max_alt + 5, 5)), xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Heating Rates Relative Error' + factors.title, 'y': 0.9, 'x': 0.47, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    
def plot_heating_rates_contr(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot cotibution of error of each variable to Heating Rates calculation in vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Ohmic Heating
    Ohmic_rel = factors.Ohmic_Heating_error[lat, lon,
                                            :-1] / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dB = factors.dOH_B[lat, lon, :-
                            1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dE = factors.dOH_E[lat, lon, :-
                            1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dNneutral = factors.dOH_Nneutral[lat, lon, :-
                                          1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dNion = factors.dOH_Nion[lat, lon, :-
                                  1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dUn = factors.dOH_Un[lat, lon, :-
                              1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dNe = factors.dOH_Ne[lat, lon, :-
                              1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dTe = factors.dOH_Te[lat, lon, :-
                              1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dTi = factors.dOH_Ti[lat, lon, :-
                              1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dTn = factors.dOH_Tn[lat, lon, :-
                              1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]
    dOhm_dsp = factors.dOH_sp[lat, lon, :-
                              1] ** (1/2) / factors.Ohmic_Heating[lat, lon, :-1]

    fig1 = go.Figure()

    # adding the various plots
    fig1.add_trace(go.Scatter(x=Ohmic_rel, y=factors.heights[lat, lon, :-1], name="Ohmic Heating error", mode='lines',
                              line=dict(shape='spline', color='red')))
    fig1.add_trace(go.Scatter(x=dOhm_dB, y=factors.heights[lat, lon, :-1], name="dB", mode='lines',
                              line=dict(shape='spline', dash="dot", color='red')))
    fig1.add_trace(go.Scatter(x=dOhm_dE, y=factors.heights[lat, lon, :-1], name="dE", mode='lines',
                              line=dict(shape='spline', dash="dash", color='red')))
    fig1.add_trace(go.Scatter(x=dOhm_dNneutral, y=factors.heights[lat, lon, :-1], name="dNn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='lightcoral')))
    fig1.add_trace(go.Scatter(x=dOhm_dNion, y=factors.heights[lat, lon, :-1], name="dNion", mode='lines',
                              line=dict(shape='spline', dash="dot", color='lightcoral')))
    fig1.add_trace(go.Scatter(x=dOhm_dUn, y=factors.heights[lat, lon, :-1], name="dUn", mode='lines',
                              line=dict(shape='spline', dash="dot", color='maroon')))
    fig1.add_trace(go.Scatter(x=dOhm_dNe, y=factors.heights[lat, lon, :-1], name="dNe", mode='lines',
                              line=dict(shape='spline', dash="dash", color='maroon')))
    fig1.add_trace(go.Scatter(x=dOhm_dTe, y=factors.heights[lat, lon, :-1], name="dTe", mode='lines',
                              line=dict(shape='spline', dash="dot", color='sienna')))
    fig1.add_trace(go.Scatter(x=dOhm_dTi, y=factors.heights[lat, lon, :-1], name="dTi", mode='lines',
                              line=dict(shape='spline', dash="dash", color='sienna')))
    fig1.add_trace(go.Scatter(x=dOhm_dTn, y=factors.heights[lat, lon, :-1], name="dTn", mode='lines',
                              line=dict(shape='spline', dash="dot", color='rosybrown')))
    fig1.add_trace(go.Scatter(x=dOhm_dsp, y=factors.heights[lat, lon, :-1], name="dσPedersen", mode='lines',
                              line=dict(shape='spline', dash="dash", color='rosybrown')))

    # updating the layout of the figure
    fig1.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt], tickmode='array',
                       tickvals=np.arange(min_alt, max_alt + 5, 5)), xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                       title={'text': 'Ohmic Heating Error Contributions' + factors.title, 'y': 0.9, 'x': 0.49, 'xanchor': 'center', 'yanchor': 'top'})

    fig1.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig1.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig1.update_xaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)
    fig1.update_yaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)

    fig1.show()

    
    # Frictional Heating
    Frict_rel = factors.Frictional_Heating_error[lat, lon,
                                                 :-1] / factors.Frictional_Heating[lat, lon, :-1]
    dFric_dB = factors.dFH_B[lat, lon, :-
                             1] ** (1/2) / factors.Frictional_Heating[lat, lon, :-1]
    dFric_dNneutral = factors.dFH_Nneutral[lat, lon, :-
                                           1] ** (1/2) / factors.Frictional_Heating[lat, lon, :-1]
    dFric_dNion = factors.dFH_Nion[lat, lon, :-
                                   1] ** (1/2) / factors.Frictional_Heating[lat, lon, :-1]
    dFric_dUn = factors.dFH_Un[lat, lon, :-
                               1] ** (1/2) / factors.Frictional_Heating[lat, lon, :-1]
    dFric_dVi = factors.dFH_Vi[lat, lon, :-
                               1] ** (1/2) / factors.Frictional_Heating[lat, lon, :-1]
    dFric_dTn = factors.dFH_Tn[lat, lon, :-
                               1] ** (1/2) / factors.Frictional_Heating[lat, lon, :-1]
    dFric_dTi = factors.dFH_Ti[lat, lon, :-
                               1] ** (1/2) / factors.Frictional_Heating[lat, lon, :-1]
    dFric_dnu = factors.dFH_nu[lat, lon, :-
                               1] ** (1/2) / factors.Frictional_Heating[lat, lon, :-1]

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=Frict_rel, y=factors.heights[lat, lon, :-1], name="Frictional Heating error", mode='lines',
                              line=dict(shape='spline', color='blue')))
    fig2.add_trace(go.Scatter(x=dFric_dB, y=factors.heights[lat, lon, :-1], name="dB", mode='lines',
                              line=dict(shape='spline', dash="dot", color='blue')))
    fig2.add_trace(go.Scatter(x=dFric_dNneutral, y=factors.heights[lat, lon, :-1], name="dNn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='blue')))
    fig2.add_trace(go.Scatter(x=dFric_dNion, y=factors.heights[lat, lon, :-1], name="dNion", mode='lines',
                              line=dict(shape='spline', dash="dot", color='turquoise')))
    fig2.add_trace(go.Scatter(x=dFric_dUn, y=factors.heights[lat, lon, :-1], name="dUn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='turquoise')))
    fig2.add_trace(go.Scatter(x=dFric_dVi, y=factors.heights[lat, lon, :-1], name="dVi", mode='lines',
                              line=dict(shape='spline', dash="dot", color='darkslategrey')))
    fig2.add_trace(go.Scatter(x=dFric_dTn, y=factors.heights[lat, lon, :-1], name="dTn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='darkslategrey')))
    fig2.add_trace(go.Scatter(x=dFric_dTi, y=factors.heights[lat, lon, :-1], name="dTi", mode='lines',
                              line=dict(shape='spline', dash="dot", color='steelblue')))
    fig2.add_trace(go.Scatter(x=dFric_dnu, y=factors.heights[lat, lon, :-1], name="dν", mode='lines',
                              line=dict(shape='spline', dash="dash", color='steelblue')))
    # updating the layout of the figure
    fig2.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt],
                       tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                       xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                       title={'text': 'Frictional Heating Error Contributions' + factors.title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    fig2.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig2.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig2.update_xaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)
    fig2.update_yaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)

    fig2.show()

    
    # Joule Heating
    Joule_rel = factors.Joule_Heating_error[lat, lon,
                                            :-1] / factors.Joule_Heating[lat, lon, :-1]
    dJoule_dB = factors.dJH_B[lat, lon, :-
                              1] ** (1/2) / factors.Joule_Heating[lat, lon, :-1]
    dJoule_dE = factors.dJH_E[lat, lon, :-
                              1] ** (1/2) / factors.Joule_Heating[lat, lon, :-1]
    dJoule_dVi = factors.dJH_Vi[lat, lon, :-
                                1] ** (1/2) / factors.Joule_Heating[lat, lon, :-1]
    dJoule_dUn = factors.dJH_Un[lat, lon, :-
                                1] ** (1/2) / factors.Joule_Heating[lat, lon, :-1]
    dJoule_dNe = factors.dJH_Ne[lat, lon, :-
                                1] ** (1/2) / factors.Joule_Heating[lat, lon, :-1]

    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(x=Joule_rel, y=factors.heights[lat, lon, :-1], name="Joule Heating error", mode='lines',
                              line=dict(shape='spline', color='green')))
    fig3.add_trace(go.Scatter(x=dJoule_dB, y=factors.heights[lat, lon, :-1], name="dB", mode='lines',
                              line=dict(shape='spline', dash="dot", color='green')))
    fig3.add_trace(go.Scatter(x=dJoule_dE, y=factors.heights[lat, lon, :-1], name="dE", mode='lines',
                              line=dict(shape='spline', dash="dash", color='green')))
    fig3.add_trace(go.Scatter(x=dJoule_dVi, y=factors.heights[lat, lon, :-1], name="dVi", mode='lines',
                              line=dict(shape='spline', dash="dot", color='lime')))
    fig3.add_trace(go.Scatter(x=dJoule_dUn, y=factors.heights[lat, lon, :-1], name="dUn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='lime')))
    fig3.add_trace(go.Scatter(x=dJoule_dNe, y=factors.heights[lat, lon, :-1], name="dNe", mode='lines',
                              line=dict(shape='spline', dash="dot", color='greenyellow')))

    # updating the layout of the figure
    fig3.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]),
                       yaxis=dict(range=[min_alt, max_alt], tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)), xaxis_title="",
                       yaxis_title="$Altitude \ (km)$", width=900, height=650,
                       title={'text': 'Joule Heating Error Contributions' + factors.title, 'y': 0.9, 'x': 0.49, 'xanchor': 'center', 'yanchor': 'top'})

    fig3.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig3.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig3.update_xaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)
    fig3.update_yaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)

    fig3.show()

    


def plot_conductivities_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot conductivities in vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.pedersen_con_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="σPedersen error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.hall_con_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="σHall error", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.parallel_con_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="σParallel error",
                             mode='lines', line=dict(shape='spline', color='green'), visible="legendonly"))
    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="$(S/m)$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Conductivities Absolute Error' + factors.title, 'y': 0.9, 'x': 0.47, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    

def plot_conductivities_plus_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Conductivities including Error in vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.pedersen_con_error[lat, lon, :-1] + factors.pedersen_con[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="σPedersen + error", mode='lines', line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.pedersen_con[lat, lon, :-1] - factors.pedersen_con_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="σPedersen - error", mode='lines', line=dict(shape='spline', color='red', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.hall_con_error[lat, lon, :-1] + factors.hall_con[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="σHall + error", mode='lines', line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.hall_con[lat, lon, :-1] - factors.hall_con_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="σHall - error", mode='lines', line=dict(shape='spline', color='blue', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.parallel_con_error[lat, lon, :-1] + factors.parallel_con[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="σParallel + error", mode='lines', line=dict(shape='spline', color='green'), visible="legendonly"))
    fig.add_trace(go.Scatter(x=factors.parallel_con[lat, lon, :-1] - factors.parallel_con_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="σParallel - error", mode='lines', line=dict(shape='spline', color='green', dash="dash"), visible="legendonly"))
    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="$(S/m)$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Conductivities With Error' + factors.title, 'y': 0.9, 'x': 0.45, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    


def plot_conductivities_rel_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Conductivities Relative Error in vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    pedersen_rel = factors.pedersen_con_error[lat,
                                              lon, :-1] / factors.pedersen_con[lat, lon, :-1]
    hall_rel = factors.hall_con_error[lat, lon,
                                      :-1] / factors.hall_con[lat, lon, :-1]
    parallel_rel = factors.parallel_con_error[lat,
                                              lon, :-1] / factors.parallel_con[lat, lon, :-1]

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=pedersen_rel, y=factors.heights[lat, lon, :-1], name="σPedersen error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=hall_rel, y=factors.heights[lat, lon, :-1],
                  name="σHall error", mode='lines', line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=parallel_rel, y=factors.heights[lat, lon, :-1], name="σParallel error", mode='lines',
                             line=dict(shape='spline', color='green'), visible="legendonly"))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Conductivities Relative Error' + factors.title, 'y': 0.9, 'x': 0.47, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    
def plot_conductivities_contr(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot cotibution of error of each variable to Conductivities calculation in vertical profile

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Pedersen Conductivity
    pedersen_rel = factors.pedersen_con_error[lat,
                                              lon, :-1] / factors.pedersen_con[lat, lon, :-1]
    dped_dB = factors.dsp_B[lat, lon, :-
                            1] ** (1/2) / factors.pedersen_con[lat, lon, :-1]
    dped_dTe = factors.dsp_Te[lat, lon, :-
                              1] ** (1/2) / factors.pedersen_con[lat, lon, :-1]
    dped_dTi = factors.dsp_Ti[lat, lon, :-
                              1] ** (1/2) / factors.pedersen_con[lat, lon, :-1]
    dped_dTn = factors.dsp_Tn[lat, lon, :-
                              1] ** (1/2) / factors.pedersen_con[lat, lon, :-1]
    dped_dNion = factors.dsp_Nion[lat, lon, :-
                                  1] ** (1/2) / factors.pedersen_con[lat, lon, :-1]
    dped_dNneutral = factors.dsp_Nneutral[lat, lon, :-
                                          1] ** (1/2) / factors.pedersen_con[lat, lon, :-1]
    dped_dNe = factors.dsp_Ne[lat, lon, :-
                              1] ** (1/2) / factors.pedersen_con[lat, lon, :-1]

    fig1 = go.Figure()

    # adding the various plots
    fig1.add_trace(go.Scatter(x=pedersen_rel, y=factors.heights[lat, lon, :-1], name="σPedersen error", mode='lines',
                              line=dict(shape='spline', color='red')))
    fig1.add_trace(go.Scatter(x=dped_dB, y=factors.heights[lat, lon, :-1], name="dB", mode='lines',
                              line=dict(shape='spline', dash='dot', color='red')))
    fig1.add_trace(go.Scatter(x=dped_dTe, y=factors.heights[lat, lon, :-1], name="dTe", mode='lines',
                              line=dict(shape='spline', dash='dot', color='gold')))
    fig1.add_trace(go.Scatter(x=dped_dTn, y=factors.heights[lat, lon, :-1], name="dTn", mode='lines',
                              line=dict(shape='spline', dash='dash', color='coral')))
    fig1.add_trace(go.Scatter(x=dped_dTi, y=factors.heights[lat, lon, :-1], name="dTi", mode='lines',
                              line=dict(shape='spline', dash='dot', color='sienna')))
    fig1.add_trace(go.Scatter(x=dped_dNion, y=factors.heights[lat, lon, :-1], name="dNion", mode='lines',
                              line=dict(shape='spline', dash='dash', color='brown')))
    fig1.add_trace(go.Scatter(x=dped_dNneutral, y=factors.heights[lat, lon, :-1], name="dNn", mode='lines',
                              line=dict(shape='spline', dash='dot', color='tan')))
    fig1.add_trace(go.Scatter(x=dped_dNe, y=factors.heights[lat, lon, :-1], name="dNe", mode='lines',
                              line=dict(shape='spline', dash='dash', color='peru')))

    # updating the layout of the figure
    fig1.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt],
                       tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                       xaxis_title="", yaxis_title="$Altitude \ (km)$", width=950, height=650,
                       title={'text': 'Pedersen Conductivity Error Contributions' + factors.title, 'y': 0.9, 'x': 0.5,
                              'xanchor': 'center', 'yanchor': 'top'})

    fig1.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig1.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig1.update_xaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)
    fig1.update_yaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)

    fig1.show()

    
    # Hall Conductivity
    hall_rel = factors.hall_con_error[lat, lon,
                                      :-1] / factors.hall_con[lat, lon, :-1]
    dhall_dB = factors.dsh_B[lat, lon, :-
                             1] ** (1/2) / factors.hall_con[lat, lon, :-1]
    dhall_dTe = factors.dsh_Te[lat, lon, :-
                               1] ** (1/2) / factors.hall_con[lat, lon, :-1]
    dhall_dTi = factors.dsh_Ti[lat, lon, :-
                               1] ** (1/2) / factors.hall_con[lat, lon, :-1]
    dhall_dTn = factors.dsh_Tn[lat, lon, :-
                               1] ** (1/2) / factors.hall_con[lat, lon, :-1]
    dhall_Nion = factors.dsh_Nion[lat, lon, :-
                                  1] ** (1/2) / factors.hall_con[lat, lon, :-1]
    dhall_dNe = factors.dsh_Ne[lat, lon, :-
                               1] ** (1/2) / factors.hall_con[lat, lon, :-1]
    dhall_dNneutral = factors.dsh_Nneutral[lat, lon,
                                           :-1] ** (1/2) / factors.hall_con[lat, lon, :-1]

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=hall_rel, y=factors.heights[lat, lon, :-1],
                   name="σHall error", mode='lines', line=dict(shape='spline', color='blue')))
    fig2.add_trace(go.Scatter(x=dhall_dB, y=factors.heights[lat, lon, :-1], name="dB", mode='lines',
                              line=dict(shape='spline', dash="dot", color='blue')))
    fig2.add_trace(go.Scatter(x=dhall_dTe, y=factors.heights[lat, lon, :-1], name="dTe", mode='lines',
                              line=dict(shape='spline', dash="dash", color='blue')))
    fig2.add_trace(go.Scatter(x=dhall_dTi, y=factors.heights[lat, lon, :-1], name="dTi", mode='lines',
                              line=dict(shape='spline', dash="dot", color='dodgerblue')))
    fig2.add_trace(go.Scatter(x=dhall_dTn, y=factors.heights[lat, lon, :-1], name="dTn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='dodgerblue')))
    fig2.add_trace(go.Scatter(x=dhall_Nion, y=factors.heights[lat, lon, :-1], name="dNion", mode='lines',
                              line=dict(shape='spline', dash="dot", color='deepskyblue')))
    fig2.add_trace(go.Scatter(x=dhall_dNe, y=factors.heights[lat, lon, :-1], name="dNe", mode='lines',
                              line=dict(shape='spline', dash="dash", color='deepskyblue')))
    fig2.add_trace(go.Scatter(x=dhall_dNneutral, y=factors.heights[lat, lon, :-1], name="dNn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='indigo')))

    # updating the layout of the figure
    fig2.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt],
                       tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                       xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                       title={'text': 'Hall Conductivity Error Contributions' + factors.title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    fig2.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig2.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig2.update_xaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)
    fig2.update_yaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)

    fig2.show()

    


def plot_currents_error(lat_value, lon_value, min_alt, max_alt):

    '''
    This function used to plot Error of Currents calculation

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.J_pedersen_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Pedersen Current error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.J_hall_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Hall Current error", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.J_ohmic_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Ohmic current error", mode='lines',
                             line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=factors.J_dens_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Densities current error", mode='lines',
                             line=dict(shape='spline', color='black')))

    x_range = max(factors.J_dens_error[lat, lon, :-1])

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)), xaxis=dict(range=[0, x_range + x_range/8]),
                      xaxis_title="$(A/m^{2})$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Perpendicular Currents Absolute Error' + factors.title, 'y': 0.9, 'x': 0.51, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    


def plot_currents_plus_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Currents inclunding Error

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.J_pedersen_error[lat, lon, :-1] + factors.J_pedersen[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Pedersen Current + error", mode='lines', line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.J_pedersen[lat, lon, :-1] - factors.J_pedersen_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Pedersen Current - error", mode='lines', line=dict(shape='spline', color='red', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.J_hall_error[lat, lon, :-1] + factors.J_hall[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Hall Current + error", mode='lines', line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.J_hall[lat, lon, :-1] - factors.J_hall_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Hall Current - error", mode='lines', line=dict(shape='spline', color='blue', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.J_ohmic_error[lat, lon, :-1] + factors.J_ohmic[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Ohmic current + error", mode='lines', line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=factors.J_ohmic[lat, lon, :-1] - factors.J_ohmic_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Ohmic current - error", mode='lines', line=dict(shape='spline', color='green', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.J_dens_error[lat, lon, :-1] + factors.J_dens[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Densities current + error", mode='lines', line=dict(shape='spline', color='black')))
    fig.add_trace(go.Scatter(x=factors.J_dens[lat, lon, :-1] - factors.J_dens_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1],
                             name="Densities current - error", mode='lines', line=dict(shape='spline', color='black', dash="dash")))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="$(A/m^{2})$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Perpendicular Currents With Error' + factors.title, 'y': 0.9, 'x': 0.49, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    
def plot_currents_rel_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Relative Error of Currents calculation

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    Jp_rel = factors.J_pedersen_error[lat, lon,
                                      :-1] / factors.J_pedersen[lat, lon, :-1]
    Jh_rel = factors.J_hall_error[lat, lon,
                                  :-1] / factors.J_hall[lat, lon, :-1]
    Johmic_rel = factors.J_ohmic_error[lat,
                                       lon, :-1] / factors.J_ohmic[lat, lon, :-1]
    Jdens_rel = factors.J_dens_error[lat, lon,
                                     :-1] / factors.J_dens[lat, lon, :-1]

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=Jp_rel, y=factors.heights[lat, lon, :-1], name="Pedersen Current error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=Jh_rel, y=factors.heights[lat, lon, :-1], name="Hall Current error", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=Johmic_rel, y=factors.heights[lat, lon, :-1], name="Ohmic current error", mode='lines',
                             line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=Jdens_rel, y=factors.heights[lat, lon, :-1], name="Densities current error", mode='lines',
                             line=dict(shape='spline', color='black')))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Perpendicular Currents Relative Error' + factors.title, 'y': 0.9, 'x': 0.51, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    

def plot_currents_contr(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot contribution of each variable error to the total Error of Currents calculation

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # JOhmic
    Johmic_rel = factors.J_ohmic_error[lat,
                                       lon, :-1] / factors.J_ohmic[lat, lon, :-1]
    dJohm_dB = factors.dJohm_B[lat, lon, :-
                               1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dE = factors.dJohm_E[lat, lon, :-
                               1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dUn = factors.dJohm_Un[lat, lon, :-
                                 1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dsp = factors.dJohm_sp[lat, lon, :-
                                 1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dsh = factors.dJohm_sh[lat, lon, :-
                                 1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dTi = factors.dJohm_Ti[lat, lon, :-
                                 1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dTn = factors.dJohm_Tn[lat, lon, :-
                                 1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dTe = factors.dJohm_Te[lat, lon, :-
                                 1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dNe = factors.dJohm_Ne[lat, lon, :-
                                 1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dNn = factors.dJohm_Nneutral[lat, lon,
                                       :-1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]
    dJohm_dNion = factors.dJohm_Nion[lat, lon, :-
                                     1] ** (1/2) / factors.J_ohmic[lat, lon, :-1]

    fig1 = go.Figure()

    # adding the various plots
    fig1.add_trace(go.Scatter(x=Johmic_rel, y=factors.heights[lat, lon, :-1], name="Ohmic current error", mode='lines',
                              line=dict(shape='spline', color='green')))
    fig1.add_trace(go.Scatter(x=dJohm_dB, y=factors.heights[lat, lon, :-1], name="dB", mode='lines',
                              line=dict(shape='spline', dash="dot", color='green')))
    fig1.add_trace(go.Scatter(x=dJohm_dE, y=factors.heights[lat, lon, :-1], name="dE", mode='lines',
                              line=dict(shape='spline', dash="dot", color='coral')))
    fig1.add_trace(go.Scatter(x=dJohm_dUn, y=factors.heights[lat, lon, :-1], name="dUn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='coral')))
    fig1.add_trace(go.Scatter(x=dJohm_dsp, y=factors.heights[lat, lon, :-1], name="dσP", mode='lines',
                              line=dict(shape='spline', dash="dash", color='sienna')))
    fig1.add_trace(go.Scatter(x=dJohm_dsh, y=factors.heights[lat, lon, :-1], name="dσH", mode='lines',
                              line=dict(shape='spline', dash="dot", color='gold')))
    fig1.add_trace(go.Scatter(x=dJohm_dTi, y=factors.heights[lat, lon, :-1], name="dTi", mode='lines',
                              line=dict(shape='spline', dash="dot", color='orange')))
    fig1.add_trace(go.Scatter(x=dJohm_dTn, y=factors.heights[lat, lon, :-1], name="dTn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='orange')))
    fig1.add_trace(go.Scatter(x=dJohm_dTe, y=factors.heights[lat, lon, :-1], name="dTe", mode='lines',
                              line=dict(shape='spline', dash="dash", color='crimson')))
    fig1.add_trace(go.Scatter(x=dJohm_dNe, y=factors.heights[lat, lon, :-1], name="dNe", mode='lines',
                              line=dict(shape='spline', dash="dot", color='crimson')))
    fig1.add_trace(go.Scatter(x=dJohm_dNn, y=factors.heights[lat, lon, :-1], name="dNn", mode='lines',
                              line=dict(shape='spline', dash="dot", color='mediumblue')))
    fig1.add_trace(go.Scatter(x=dJohm_dNion, y=factors.heights[lat, lon, :-1], name="dNion", mode='lines',
                              line=dict(shape='spline', dash="dash", color='mediumblue')))

    # updating the layout of the figure
    fig1.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt],
                       tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                       xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                       title={'text': 'Ohmic Current Contributions' + factors.title, 'y': 0.9, 'x': 0.47, 'xanchor': 'center', 'yanchor': 'top'})

    fig1.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig1.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig1.update_xaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)
    fig1.update_yaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)

    fig1.show()

    
    # Jdensities
    Jdens_rel = factors.J_dens_error[lat, lon,
                                     :-1] / factors.J_dens[lat, lon, :-1]
    Jdens_dB = factors.dJd_B[lat, lon, :-
                             1] ** (1/2) / factors.J_dens[lat, lon, :-1]
    Jdens_dE = factors.dJd_E[lat, lon, :-
                             1] ** (1/2) / factors.J_dens[lat, lon, :-1]
    Jdens_dVi = factors.dJd_Vi[lat, lon, :-
                               1] ** (1/2) / factors.J_dens[lat, lon, :-1]
    Jdens_dUn = factors.dJd_Un[lat, lon, :-
                               1] ** (1/2) / factors.J_dens[lat, lon, :-1]
    Jdens_dNe = factors.dJd_Ne[lat, lon, :-
                               1] ** (1/2) / factors.J_dens[lat, lon, :-1]

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=Jdens_rel, y=factors.heights[lat, lon, :-1], name="Densities current error", mode='lines',
                              line=dict(shape='spline', color='black')))
    fig2.add_trace(go.Scatter(x=Jdens_dB, y=factors.heights[lat, lon, :-1], name="dB", mode='lines',
                              line=dict(shape='spline', dash="dot", color='gold')))
    fig2.add_trace(go.Scatter(x=Jdens_dE, y=factors.heights[lat, lon, :-1], name="dE", mode='lines',
                              line=dict(shape='spline', dash="dash", color='gold')))
    fig2.add_trace(go.Scatter(x=Jdens_dVi, y=factors.heights[lat, lon, :-1], name="dVi", mode='lines',
                              line=dict(shape='spline', dash="dot", color='red')))
    fig2.add_trace(go.Scatter(x=Jdens_dUn, y=factors.heights[lat, lon, :-1], name="dUn", mode='lines',
                              line=dict(shape='spline', dash="dash", color='red')))
    fig2.add_trace(go.Scatter(x=Jdens_dNe, y=factors.heights[lat, lon, :-1], name="dNe", mode='lines',
                              line=dict(shape='spline', dash="dash", color='coral')))

    # updating the layout of the figure
    fig2.update_layout(xaxis_type="linear", xaxis=dict(range=[0, 1]), yaxis=dict(range=[min_alt, max_alt],
                       tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                       xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                       title={'text': 'Densities Current Contributions' + factors.title, 'y': 0.9, 'x': 0.48, 'xanchor': 'center', 'yanchor': 'top'})

    fig2.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig2.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig2.update_xaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)
    fig2.update_yaxes(showline=True, linewidth=2,
                      linecolor='black', mirror=True)

    fig2.show()

    

def plot_csections_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Error of Cross Sections

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.C_Op_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="$O^{+}$", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=factors.C_O2p_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="$O_{2}^{+}$", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=factors.C_NOp_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="$NO^{+}$", mode='lines',
                             line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=factors.C_ion_error[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="$Avg$", mode='lines',
                             line=dict(shape='spline', color='black')))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)), xaxis=dict(range=[0, max(factors.C_ionC_Op_error[lat, lon, :-1])]),
                      xaxis_title="$(m^{2})$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Cross Sections Absolute Error' + factors.title, 'y': 0.9, 'x': 0.48, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    


def plot_csections_plus_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Cross Sections including Error

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=factors.C_Op_error[lat, lon, :-1] + factors.C_Op[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="O{+} + error",
                             mode='lines', line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=- factors.C_Op_error[lat, lon, :-1] + factors.C_Op[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="O{+} - error",
                             mode='lines', line=dict(shape='spline', color='red', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.C_O2p_error[lat, lon, :-1] + factors.C_O2p[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="O2{+} + error",
                             mode='lines', line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=- factors.C_O2p_error[lat, lon, :-1] + factors.C_O2p[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="O2{+} - error",
                             mode='lines', line=dict(shape='spline', color='blue', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.C_NOp_error[lat, lon, :-1] + factors.C_NOp[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="NO{+} + error",
                             mode='lines', line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=- factors.C_NOp_error[lat, lon, :-1] + factors.C_NOp[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="NO{+} - error",
                             mode='lines', line=dict(shape='spline', color='green', dash="dash")))
    fig.add_trace(go.Scatter(x=factors.C_ion_error[lat, lon, :-1] + factors.C_ion[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Avg + error",
                             mode='lines', line=dict(shape='spline', color='black')))
    fig.add_trace(go.Scatter(x=- factors.C_ion_error[lat, lon, :-1] + factors.C_ion[lat, lon, :-1], y=factors.heights[lat, lon, :-1], name="Avg - error",
                             mode='lines', line=dict(shape='spline', color='black', dash="dash")))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", xaxis_showexponent='all', xaxis_exponentformat='power', yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="$(m^{2})$", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Cross Sections With Error' + factors.title, 'y': 0.9, 'x': 0.46, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    

def plot_csections_rel_error(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot Cross Section Relative Error

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    COp_rel = factors.C_Op_error[lat, lon, :-1] / factors.C_Op[lat, lon, :-1]
    CO2p_rel = factors.C_O2p_error[lat, lon,
                                   :-1] / factors.C_O2p[lat, lon, :-1]
    CNOp_rel = factors.C_NOp_error[lat, lon,
                                   :-1] / factors.C_NOp[lat, lon, :-1]
    Cion_rel = factors.C_ion_error[lat, lon,
                                   :-1] / factors.C_ion[lat, lon, :-1]

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=COp_rel, y=factors.heights[lat, lon, :-1], name="$O^{+}$", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=CO2p_rel, y=factors.heights[lat, lon, :-1], name="$O_{2}^{+}$", mode='lines',
                             line=dict(shape='spline', color='blue')))
    fig.add_trace(go.Scatter(x=CNOp_rel, y=factors.heights[lat, lon, :-1], name="$NO^{+}$", mode='lines',
                             line=dict(shape='spline', color='green')))
    fig.add_trace(go.Scatter(x=Cion_rel, y=factors.heights[lat, lon, :-1], name="$Avg$", mode='lines',
                             line=dict(shape='spline', color='black')))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="", yaxis_title="$Altitude \ (km)$", width=900, height=650,
                      title={'text': 'Cross Sections Relative Error' + factors.title, 'y': 0.9, 'x': 0.48, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

    


def plot_csections_contr(lat_value, lon_value, min_alt, max_alt):
    '''
    This function used to plot contibution of each variable Error to the total Error fo Cross Section

    Args:
        lat_value (int): Latitude as index of TIEGCM file 
        lon_value (int): Longitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lat = lat_value
    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    Cion_rel = factors.C_ion_error[lat, lon,
                                   :-1] / factors.C_ion[lat, lon, :-1]
    Cion_dTi = factors.dCion_Ti[lat, lon, :-
                                1] ** (1/2) / factors.C_ion[lat, lon, :-1]
    Cion_dTn = factors.dCion_Tn[lat, lon, :-
                                1] ** (1/2) / factors.C_ion[lat, lon, :-1]
    Cion_dnu = factors.dCion_nu[lat, lon, :-
                                1] ** (1/2) / factors.C_ion[lat, lon, :-1]
    Cion_dNn = factors.dCion_Nneutral[lat, lon,
                                      :-1] ** (1/2) / factors.C_ion[lat, lon, :-1]

    fig = go.Figure()

    # adding the various plots
    fig.add_trace(go.Scatter(x=Cion_rel, y=factors.heights[lat, lon, :-1], name="Avg Ion Csection error", mode='lines',
                             line=dict(shape='spline', color='red')))
    fig.add_trace(go.Scatter(x=Cion_dTi, y=factors.heights[lat, lon, :-1], name="dTi", mode='lines',
                             line=dict(shape='spline', dash="dot", color='blue')))
    fig.add_trace(go.Scatter(x=Cion_dTn, y=factors.heights[lat, lon, :-1], name="dTn", mode='lines',
                             line=dict(shape='spline', dash="dash", color='green')))
    fig.add_trace(go.Scatter(x=Cion_dnu, y=factors.heights[lat, lon, :-1], name="dν", mode='lines',
                             line=dict(shape='spline', dash="dot", color='green')))
    fig.add_trace(go.Scatter(x=Cion_dNn, y=factors.heights[lat, lon, :-1], name="dNn", mode='lines',
                             line=dict(shape='spline', dash="dash", color='blue')))

    # updating the layout of the figure
    fig.update_layout(xaxis_type="linear", yaxis=dict(range=[min_alt, max_alt],
                      tickmode='array', tickvals=np.arange(min_alt, max_alt + 5, 5)),
                      xaxis_title="", yaxis_title="$Altitude \ (km)$", width=950, height=650,
                      title={'text': 'Average Ion Csection Error Contributions' + factors.title, 'y': 0.9, 'x': 0.49, 'xanchor': 'center', 'yanchor': 'top'})

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='grey')
    fig.update_xaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2,
                     linecolor='black', mirror=True)

    fig.show()

   


# ############################### Lat-Lon Map Profile Plots ###############################
def mapll_heating_rates_plot(pressure_level, night_shade):
    '''
    This function used to plot Heating Rates over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    # Joule Heating
    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow(
        factors.Joule_Heating[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Joule Heating' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc1, cax=cax1)
    cbar.set_label(label='$(W/m^{3})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Joule_Heating_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)
    

    # Ohmic Heating
    fig2 = plt.figure(figsize=(13, 13))
    ax2 = fig2.add_subplot(1, 1, 1, aspect='equal')

    m2 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m2.drawcoastlines()

    sc2 = m2.imshow(
        factors.Ohmic_Heating[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m2.nightshade(factors.title, alpha=0.3)

    m2.drawparallels(np.arange(-90., 91., 5.))
    m2.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Ohmic Heating' + factors.title)

    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc2, cax=cax2)
    cbar.set_label(label='$(W/m^{3})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Ohmic_Heating_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)
    

    # Frictional Heating
    fig3 = plt.figure(figsize=(13, 13))
    ax3 = fig3.add_subplot(1, 1, 1, aspect='equal')

    m3 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m3.drawcoastlines()

    sc3 = m3.imshow(
        factors.Frictional_Heating[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m3.nightshade(factors.title, alpha=0.3)

    m3.drawparallels(np.arange(-90., 91., 5.))
    m3.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Frictional Heating' + factors.title)

    divider = make_axes_locatable(ax3)
    cax3 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc3, cax=cax3)
    cbar.set_label(label='$(W/m^{3})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Frictional_Heating_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)
    plt.show()


def mapll_collisions_plot(pressure_level, night_shade):
    '''
    This function used to plot Collision Frequencies over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    # Average Ion Collision Frequency
    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow((factors.nu_Op_sum[:, :, lev] + factors.nu_O2p_sum[:, :, lev] +
                    factors.nu_NOp_sum[:, :, lev]) / 3, cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Average Ion Collision Frequency' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc1, cax=cax1)
    cbar.set_label(label='$(Hz)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'AvG_Ion_Col_Freq_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)
    

    # Electron Collision Frequency
    fig2 = plt.figure(figsize=(13, 13))
    ax2 = fig2.add_subplot(1, 1, 1, aspect='equal')

    m2 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m2.drawcoastlines()

    sc2 = m2.imshow(factors.nu_e_sum[:, :, lev],
                    cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m2.nightshade(factors.title, alpha=0.3)

    m2.drawparallels(np.arange(-90., 91., 5.))
    m2.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Electron Collision Frequency' + factors.title)

    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc2, cax=cax2)
    cbar.set_label(label='$(Hz)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Electron_Col_Freq_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapll_conductivities_plot(pressure_level, night_shade):
    '''
    This function used to plot Conductivities over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    # Pedersen Conductivity
    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow(
        factors.pedersen_con[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Pedersen Conductivity' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc1, cax=cax1)
    cbar.set_label(label='$(S/m)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Pedersen_Cond_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Hall Conductivity
    fig2 = plt.figure(figsize=(13, 13))
    ax2 = fig2.add_subplot(1, 1, 1, aspect='equal')

    m2 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m2.drawcoastlines()

    sc2 = m2.imshow(factors.hall_con[:, :, lev],
                    cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m2.nightshade(factors.title, alpha=0.3)

    m2.drawparallels(np.arange(-90., 91., 5.))
    m2.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Hall Conductivity' + factors.title)

    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc2, cax=cax2)
    cbar.set_label(label='$(S/m)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Hall_Cond_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Parallel Conductivity
    fig3 = plt.figure(figsize=(13, 13))
    ax3 = fig3.add_subplot(1, 1, 1, aspect='equal')

    m3 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m3.drawcoastlines()

    sc3 = m3.imshow(
        factors.parallel_con[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m3.nightshade(factors.title, alpha=0.3)

    m3.drawparallels(np.arange(-90., 91., 5.))
    m3.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Parallel Conductivity' + factors.title)

    divider = make_axes_locatable(ax3)
    cax3 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc3, cax=cax3)
    cbar.set_label(label='$(S/m)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Parallel_Cond_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapll_currents_plot(pressure_level, night_shade):
    '''
    This function used to plot Currents over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    # Ohmic Current
    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow(factors.J_ohmic[:, :, lev],
                    cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Ohmic Current' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc1, cax=cax1)
    cbar.set_label(label='$(A/m^{2})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Ohmic_Cur_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Densities Current
    fig2 = plt.figure(figsize=(13, 13))
    ax2 = fig2.add_subplot(1, 1, 1, aspect='equal')

    m2 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m2.drawcoastlines()

    sc2 = m2.imshow(factors.J_dens[:, :, lev],
                    cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m2.nightshade(factors.title, alpha=0.3)

    m2.drawparallels(np.arange(-90., 91., 5.))
    m2.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Densities Current' + factors.title)

    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc2, cax=cax2)
    cbar.set_label(label='$(A/m^{2})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Densities_Cur_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapll_csection_plot(pressure_level, night_shade):
    '''
    This function used to plot Cross Sections over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow(factors.C_ion[:, :, lev],
                    cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Average Ion Cross Section' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    cbar = plt.colorbar(sc1, cax=cax1)
    cbar.set_label(label='$(m^{2})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Avg_Ion_CS_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapll_heating_rates_rel_error_plot(pressure_level, night_shade):
    '''
    This function used to plot Heating Rates relative Error over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    # Joule Heating
    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow(factors.Joule_Heating_error[:, :, lev] /
                    factors.Joule_Heating[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Joule Heating Relative Error' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc1, cax=cax1)
    name = 'Joule_Heating_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Ohmic Heating
    fig2 = plt.figure(figsize=(13, 13))
    ax2 = fig2.add_subplot(1, 1, 1, aspect='equal')

    m2 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m2.drawcoastlines()

    sc2 = m2.imshow(factors.Ohmic_Heating_error[:, :, lev] /
                    factors.Ohmic_Heating[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m2.nightshade(factors.title, alpha=0.3)

    m2.drawparallels(np.arange(-90., 91., 5.))
    m2.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Ohmic Heating Relative Error' + factors.title)

    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc2, cax=cax2)
    name = 'Ohmic_Heating_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Frictional Heating
    fig3 = plt.figure(figsize=(13, 13))
    ax3 = fig3.add_subplot(1, 1, 1, aspect='equal')

    m3 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m3.drawcoastlines()

    sc3 = m3.imshow(factors.Frictional_Heating_error[:, :, lev] /
                    factors.Frictional_Heating[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m3.nightshade(factors.title, alpha=0.3)

    m3.drawparallels(np.arange(-90., 91., 5.))
    m3.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Frictional Heating Relative Error' + factors.title)

    divider = make_axes_locatable(ax3)
    cax3 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc3, cax=cax3)
    name = 'Frictional_Heating_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapll_collisions_rel_error_plot(pressure_level, night_shade):
    '''
    This function used to plot Collsion Frequencies Relative Error over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    # Average Ion Collisions Relative Error
    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow(((factors.factors.nuOp_error[:, :, lev] + factors.nuO2p_error[:, :, lev] + factors.nuNOp_error[:, :, lev]) / 3) /
                    ((factors.nu_Op_sum[:, :, lev] + factors.nu_O2p_sum[:,
                     :, lev] + factors.nu_NOp_sum[:, :, lev]) / 3),
                    cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Average Ion Collision Frequency Relative Error' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc1, cax=cax1)
    name = 'Avg_Ion_ColFreq_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Electron Collision Frequency Relative Error
    fig2 = plt.figure(figsize=(13, 13))
    ax2 = fig2.add_subplot(1, 1, 1, aspect='equal')

    m2 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m2.drawcoastlines()

    sc2 = m2.imshow(factors.nue_error[:, :, lev] / factors.nu_e_sum[:,
                    :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m2.nightshade(factors.title, alpha=0.3)

    m2.drawparallels(np.arange(-90., 91., 5.))
    m2.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Electron Collision Frequency Relative Error' + factors.title)

    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc2, cax=cax2)
    name = 'Electron_Ion_ColFreq_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapll_conductivities_rel_error_plot(pressure_level, night_shade):
    '''
    This function used to plot Conductivities Relative Error over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    # Pedersen Conductivity
    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow(factors.pedersen_con_error[:, :, lev] /
                    factors.pedersen_con[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Pedersen Conductivity Relative Error' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc1, cax=cax1)
    name = 'Pedersen_Cond_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Hall Conductivity
    fig2 = plt.figure(figsize=(13, 13))
    ax2 = fig2.add_subplot(1, 1, 1, aspect='equal')

    m2 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m2.drawcoastlines()

    sc2 = m2.imshow(factors.hall_con_error[:, :, lev] /
                    factors.hall_con[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m2.nightshade(factors.title, alpha=0.3)

    m2.drawparallels(np.arange(-90., 91., 5.))
    m2.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Hall Conductivity Relative Error' + factors.title)

    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc2, cax=cax2)
    name = 'Hall_Cond_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Parallel Conductivity
    fig3 = plt.figure(figsize=(13, 13))
    ax3 = fig3.add_subplot(1, 1, 1, aspect='equal')

    m3 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m3.drawcoastlines()

    sc3 = m3.imshow(factors.parallel_con_error[:, :, lev] /
                    factors.parallel_con[:, :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m3.nightshade(factors.title, alpha=0.3)

    m3.drawparallels(np.arange(-90., 91., 5.))
    m3.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Parallel Conductivity Relative Error' + factors.title)

    divider = make_axes_locatable(ax3)
    cax3 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc3, cax=cax3)
    name = 'Parallel_Cond_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapll_currents_rel_error_plot(pressure_level, night_shade):
    '''
    This function used to plot Currents Relative Error over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    # Ohmic Current
    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow(factors.J_ohmic_error[:, :, lev] / factors.J_ohmic[:,
                    :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Ohmic Current Relative Error' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc1, cax=cax1)
    name = 'Ohmic_Cur_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Densities Current
    fig2 = plt.figure(figsize=(13, 13))
    ax2 = fig2.add_subplot(1, 1, 1, aspect='equal')

    m2 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m2.drawcoastlines()

    sc2 = m2.imshow(factors.J_dens_error[:, :, lev] / factors.J_dens[:,
                    :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m2.nightshade(factors.title, alpha=0.3)

    m2.drawparallels(np.arange(-90., 91., 5.))
    m2.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Densities Current Relative Error' + factors.title)

    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc2, cax=cax2)
    name = 'Densities_Cur_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapll_csection_rel_error_plot(pressure_level, night_shade):
    '''
    This function used to plot Cross Section Relative Error over the Earth's map

    Args:
        pressure_value (int): Pressure level as index of TIEGCM file 
        night_shade (bool): to indicate night time in terms of Local Time
    Returns plot in live window

    '''
    print("Plotting.....")

    lev = pressure_level

    fig1 = plt.figure(figsize=(13, 13))
    ax1 = fig1.add_subplot(1, 1, 1, aspect='equal')

    m1 = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                 llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m1.drawcoastlines()

    sc1 = m1.imshow(factors.C_ion_error[:, :, lev] / factors.C_ion[:,
                    :, lev], cmap=cm.batlow, interpolation='bicubic')

    if night_shade:
        m1.nightshade(factors.title, alpha=0.3)

    m1.drawparallels(np.arange(-90., 91., 5.))
    m1.drawmeridians(np.arange(-180., 181., 10.))

    plt.xticks(np.arange(-180., 181., 60.))
    plt.yticks(np.arange(-90., 91., 30.))
    plt.xlabel('$Longitude \ (deg)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Average Ion Cross Section Relative Error' + factors.title)

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=15)
    plt.colorbar(sc1, cax=cax1)
    name = 'Avg_Ion_CS_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


# ####################################### Lat - Alt Profile Plots #######################################
def mapla_heating_rates_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Heating Rates, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Joule Heating
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:],
                       factors.Joule_Heating[:, lon, :-1], cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Joule Heating' + factors.title)
    cbar = plt.colorbar(cp1)
    cbar.set_label(label='$(W/m^{3})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Joule_Heating_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Ohmic Heating
    plt.figure(figsize=(12, 12))
    cp2 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:],
                       factors.Ohmic_Heating[:, lon, :-1], cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Ohmic Heating' + factors.title)
    cbar = plt.colorbar(cp2)
    cbar.set_label(label='$(W/m^{3})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Ohmic_Heating_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Frictional Heating
    plt.figure(figsize=(12, 12))
    cp3 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:],
                       factors.Frictional_Heating[:, lon, :-1], cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Frictional Heating' + factors.title)
    cbar = plt.colorbar(cp3)
    cbar.set_label(label='$(W/m^{3})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Frictional_Heating_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapla_collisions_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Collision Frequencies, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Ion Average Collision Frequency
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], (factors.nu_Op_sum[:, lon, :-1] + factors.nu_O2p_sum[:, lon, :-1] + factors.nu_NOp_sum[:, lon, :-1]) / 3,
                       locator=ticker.LogLocator(), norm=LogNorm(), cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Average Ion Collision Frequency' + factors.title)
    cbar = plt.colorbar(cp1)
    cbar.set_label(label='$(Hz)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Avg_Ion_ColFreq_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Electron Collision Frequency
    plt.figure(figsize=(12, 12))
    cp2 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.nu_e_sum[:, lon, :-1], locator=ticker.LogLocator(subs=[1.0, 5.0]),
                       norm=LogNorm(), cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Electron Collision Frequency' + factors.title)
    cbar = plt.colorbar(cp2)
    cbar.set_label(label='$(Hz)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Electron_Ion_ColFreq_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapla_conductivities_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Conductivities, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Pedersen
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:],
                       factors.pedersen_con[:, lon, :-1], cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Pedersen Conductivity' + factors.title)
    cbar = plt.colorbar(cp1)
    cbar.set_label(label='$(S/m)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Pedersen_Cond_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Hall Conductivity
    plt.figure(figsize=(12, 12))
    cp2 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:],
                       factors.hall_con[:, lon, :-1], cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Hall Conductivity' + factors.title)
    cbar = plt.colorbar(cp2)
    cbar.set_label(label='$(S/m)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Hall_Cond_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Parallel Conductivity
    plt.figure(figsize=(12, 12))
    cp3 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.parallel_con[:, lon, :-1], locator=ticker.LogLocator(subs=[1.0, 5.0]),
                       norm=LogNorm(), cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')
    plt.title('Parallel Conductivity' + factors.title)
    cbar = plt.colorbar(cp3)
    cbar.set_label(label='$(S/m)$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Parallel_Cond_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapla_currents_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Currents, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Ohmic Current
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:],
                       factors.J_ohmic[:, lon, :-1], cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Ohmic Current' + factors.title)
    cbar = plt.colorbar(cp1)
    cbar.set_label(label='$(A/m^{2})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Ohmic_Current_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Densities Current
    plt.figure(figsize=(12, 12))
    cp2 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:],
                       factors.J_dens[:, lon, :-1], cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Densities Current' + factors.title)
    cbar = plt.colorbar(cp2)
    cbar.set_label(label='$(A/m^{2})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Densities_Current_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapla_cross_section_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Cross Sections, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Average Ion Cross Section
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:],
                       factors.C_ion[:, lon, :-1], cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Average Ion Cross Section' + factors.title)
    cbar = plt.colorbar(cp1)
    cbar.set_label(label='$(m^{2})$', size='large',
                   weight='bold', rotation=270, labelpad=30)
    name = 'Avg_Ion_CS_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapla_heating_rates_rel_error_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Heating Rates Relative Error, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Joule Heating
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.Joule_Heating_error[:, lon, :-1] / factors.Joule_Heating[:, lon, :-1],
                       locator=ticker.LogLocator(subs=[1.0, 4.0]), norm=LogNorm(), cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Joule Heating Relative Error' + factors.title)
    cbar = plt.colorbar(cp1)
    name = 'Joule_Heating_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Ohmic Heating
    plt.figure(figsize=(12, 12))
    cp2 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.Ohmic_Heating_error[:, lon, :-1] / factors.Ohmic_Heating[:, lon, :-1],
                       locator=ticker.LogLocator(subs=[1.0, 2.5, 4.0]), norm=LogNorm(), cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Ohmic Heating Relative Error' + factors.title)
    cbar = plt.colorbar(cp2)
    name = 'Ohmic_Heating_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Frictional Heating
    plt.figure(figsize=(12, 12))
    cp3 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.Frictional_Heating_error[:, lon, :-1] / factors.Frictional_Heating[:, lon, :-1],
                       locator=ticker.LogLocator(subs=[1.0, 4.5]), norm=LogNorm(), cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Frictional Heating Relative Error' + factors.title)
    cbar = plt.colorbar(cp3)
    name = 'Frictional_Heating_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapla_collisions_rel_error_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Collision Frequencies Relative Error, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Ion Average Collision Frequency
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], ((factors.nuOp_error[:, lon, :-1] + factors.nuO2p_error[:, lon, :-1] + factors.nuNOp_error[:, lon, :-1]) / 3) /
                       ((factors.nu_Op_sum[:, lon, :-1] + factors.nu_O2p_sum[:,
                        lon, :-1] + factors.nu_NOp_sum[:, lon, :-1]) / 3),
                       cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Average Ion Collision Frequency Relative Error' + factors.title)
    cbar = plt.colorbar(cp1)
    name = 'Ang_Ion_ColFreq_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Electron Collision Frequency
    plt.figure(figsize=(12, 12))
    cp2 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.nue_error[:,
                       lon, :-1] / factors.nu_e_sum[:, lon, :-1], cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Electron Collision Frequency Relative Error' + factors.title)
    cbar = plt.colorbar(cp2)
    name = 'Electron_ColFreq_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapla_conductivities_rel_error_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Conductivities Relative Error, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Pedersen
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.pedersen_con_error[:, lon, :-1] / factors.pedersen_con[:, lon, :-1], cmap=cm.batlow,
                       interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Pedersen Conductivity Relative Error' + factors.title)
    cbar = plt.colorbar(cp1)
    name = 'Pedersen_Cond_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Hall Conductivity
    plt.figure(figsize=(12, 12))
    cp2 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.hall_con_error[:, lon, :-1] / factors.hall_con[:, lon, :-1],
                       locator=ticker.LogLocator(), norm=LogNorm(), cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Hall Conductivity Relative Error' + factors.title)
    cbar = plt.colorbar(cp2)
    name = 'Hall_Cond_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Parallel Conductivity
    plt.figure(figsize=(12, 12))
    cp3 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.parallel_con_error[:, lon, :-1] / factors.parallel_con[:, lon, :-1], cmap=cm.batlow,
                       interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Parallel Conductivity Relative Error' + factors.title)
    cbar = plt.colorbar(cp3)
    name = 'Parallel_Cond_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapla_currents_rel_error_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Currents Relative Error, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Ohmic Current
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.J_ohmic_error[:, lon, :-1] / factors.J_ohmic[:, lon, :-1],
                       locator=ticker.LogLocator(subs=[1.0, 2.0, 4.0]), norm=LogNorm(), cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Ohmic Current Relative Error' + factors.title)
    cbar = plt.colorbar(cp1)
    name = 'Ohmic_Curr_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    # Densities Current
    plt.figure(figsize=(12, 12))
    cp2 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.J_dens_error[:, lon, :-1] / factors.J_dens[:, lon, :-1],
                       locator=ticker.LogLocator(subs=[1.0, 4.0]), norm=LogNorm(), cmap=cm.batlow, interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Densities Current Relative Error' + factors.title)
    cbar = plt.colorbar(cp2)
    name = 'Densities_Curr_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()


def mapla_cross_section_rel_error_plot(lon_value, min_alt, max_alt):
    '''
    This function used to plot Cross Sections Relative Error, Lat vs. Alt

    Args:
        lon_value (int): Longtitude as index of TIEGCM file 
        min_alt (float): the minimum altitude to plot
        max_alt (float): the maximum altitude to plot
    Returns plot in live window

    '''
    print("Plotting.....")

    lon = lon_value
    min_alt = min_alt
    max_alt = max_alt

    # Average Ion Cross Section
    plt.figure(figsize=(12, 12))
    cp1 = plt.contourf(factors.heights_la[:-1], factors.glat_in[:], factors.C_ion_error[:, lon, :-1] / factors.C_ion[:, lon, :-1], cmap=cm.batlow,
                       interpolation='bicubic')

    plt.xlim(min_alt, max_alt)
    plt.xticks(np.arange(min_alt, max_alt + 10, 10))
    plt.yticks(np.arange(-85, 85 + 10, 10))
    plt.xlabel('~$Altitude \ (km)$')
    plt.ylabel('$Latitude \ (deg)$')

    plt.title('Average Ion Cross Section Relative Error' + factors.title)
    cbar = plt.colorbar(cp1)
    name = 'Avg_Ion_CS_REL_'+factors.pngNameMap
    # plt.savefig(name, bbox_inches='tight', pad_inches=0)

    plt.show()
