"""
sub_heating_sources.parallel_cond

**Description**:
_____________________________________________________________________________________________________________________

Calculate parallel conductivity in S/m
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

Ne: electron density in cm^-3

B: Magnetic field vector in T

Te: Electron temperature in K

NO2: O2 density in cm^-3

NN2: N2 density in cm^-3

NO: O density in cm^-3


_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

sigma0: parallel conductivity in S/m
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""


import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import allocations as alloc
import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.mlab as mlab
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_lat_alt(param,timer,savefig=True):
    time_begin=datetime.datetime(2015,3,15,0,0,0)
    time_plot=time_begin+datetime.timedelta(minutes=alloc.maptimel[timer])
    if param == 'Pedersen':
        parameter = alloc.pedersenl[:-1,:]
    if param == 'Joule Heating':
        parameter = alloc.joulel[:-1,:]
    if param == 'O+':
        parameter = alloc.NOpl[:-1,:]
    if param == 'O2+':
        parameter = alloc.NO2pl[:-1,:]
    if param == 'NO+':
        parameter = alloc.NNOpl[:-1,:]    
    if param == 'Ion Heating Rate':
        parameter = alloc.qDTi_nl[:-1,:]
    if param == 'Frictional Heating':
        parameter = alloc.frictionall[:-1,:]
    if param == 'Ohmic Heating':
        parameter = alloc.ohmicl[:-1,:]
    if param == 'Convenction Heating':
        parameter = alloc.convection_heatingl[:-1,:]
    if param == 'Wind Heating':
        parameter = alloc.wind_heatingl[:-1,:]
    if param == 'Mechanical Power':
        parameter = alloc.mech_powerl[:-1,:]
        
    if param == 'Ti':
        parameter = alloc.Til[:-1,:]
    if param == 'Te':
        parameter = alloc.Tel[:-1,:]
    if param == 'Tn':
        parameter = alloc.Tnl[:-1,:]
    if param == 'νin':
        parameter = alloc.vinl[:-1,:]
    if param == 'νen':
        parameter = alloc.venl[:-1,:]
    if param == 'Parallel':
        parameter = alloc.parallell[:-1,:]
        
    if param == 'Hall':
        parameter = alloc.halll[:-1,:]
    if param == 'O':
        parameter = alloc.NOl[:-1,:]
    if param == 'O2':
        parameter = alloc.NO2l[:-1,:]
    if param == 'N2':
        parameter = alloc.NN2l[:-1,:]
    if param == 'Ne':
        parameter = alloc.Nel[:-1,:]
    if param == 'Potential':
        parameter = Potl[:-1,:]

    x_value=alloc.maplatl[:]
    y_value=alloc.mapaltl[:-1]
    X,Y= np.meshgrid(x_value,y_value)
  
    fig, ax = plt.subplots(figsize=(10, 7))
   
   
    z_min=parameter.min()
    z_max=parameter.max()





    
    if param == 'Joule Heating':
        plt.title("Joule Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"),fontsize=15)
        cmp='jet'
    if param == 'Frictional Heating':
        plt.title("Frictional Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='jet'
    if param == 'Ohmic Heating':
        plt.title("Ohmic Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='jet'
    if param == 'Ohmic Heating per mass':
        plt.title("Ohmic Heating per Mass (mW/kg) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='jet'
    if param == 'Ohmic Heating per pressure':
        plt.title("Ohmic Heating per pressure (1/s) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='gist_ncar'
    if param == 'Convenction Heating':
        plt.title("Convenction Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='jet'
    if param == 'Wind Heating':
        plt.title("Wind Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='jet'
    if param == 'Energy':
        plt.title("Energy Dissipation/Generation (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='jet'
    if param == 'Mechanical Power':
        plt.title("Mechanical Power (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='jet'        
    if param == 'Ion Heating Rate':
        plt.title("Ion Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='jet'        
    if param == 'Pressure_Ohmic ratio':
        plt.title("Pressure/Heating Ratio (s) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='gist_ncar'
    if param == 'O+':
        plt.title("O+ Density ($cm^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='cubehelix'
    if param == 'O2+':
        plt.title("O2+ Density ($cm^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='cubehelix'
    if param == 'NO+':
        plt.title("NO+ Density ($cm^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='cubehelix'
    if param == 'σNO+n':
        plt.title("NO+ cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='CMRmap'
    if param == 'σO2+n':
        plt.title("O2+ cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='CMRmap'
    if param == 'σ':
        plt.title("Ion cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='CMRmap'
    if param == 'vNO+n':
        plt.title("NO+-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='CMRmap'
    
    if param == 'Ti':
        plt.title("Ion Temperature (K) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='gnuplot'
    if param == 'Te':
        plt.title("Electron Temeperature (K) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='gnuplot'
    if param == 'Tn':
        plt.title("Neutral Temperature (K) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='gnuplot'
    if param == 'νO+n':
        plt.title("O+-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='CMRmap'
    if param == 'νO2+n':
        plt.title("O2+-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='CMRmap'
    if param == 'νin':
        plt.title("Ion-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='CMRmap'
    if param == 'νen':
        plt.title("Electron-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='CMRmap'
    if param == 'σO+n':
        plt.title("O+ cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='CMRmap'
    if param == 'Parallel':
        plt.title("Parallel Conductivity (Si/m) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='afmhot'

    if param == 'Pedersen':
        plt.title("Pendersen Conductivity ($10^{-5}$ mho/m) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='afmhot'
    if param == 'Hall':
        plt.title("Hall Conductivity (Si/m) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='afmhot'
    if param == 'O':
        plt.title("O ($m^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='cubehelix'
    if param == 'O2':
        plt.title("$O_{2}$ ($m^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='cubehelix'
    if param == 'N2':
        plt.title("$N_{2}$ ($m^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='cubehelix'
    if param == 'Ne':
        plt.title("Electron Density ($m^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        cmp='cubehelix'
    if param == 'Pressure':
        plt.title("Pressure (Pa) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    
    X,Y= np.meshgrid(x_value,y_value)
    print(parameter.min(),parameter.max())
#     cs = ax.contourf(X, Y, parameter2, locator=ticker.LogLocator(), cmap=cm.PuBu_r)
#     cs = plt.contourf(X,Y,parameter,100,cmap='jet',extend="both")
#     cs=plt.contourf(X, Y, parameter, np.linspace(10**(-10), parameter.max(), 100),cmap='jet',extend="both")
#     cs=plt.contour(X, Y, parameter)
    levels=np.linspace(parameter.min(),parameter.max(),101)
    cs=plt.contourf(X,Y, parameter, levels=levels, cmap=cmp,extend="both")
#     cs = plt.contourf(X, Y, parameter, locator=ticker.LogLocator(), cmap=cm.PuBu_r)

    n_levels = 100
#     cs = plt.contourf(X, Y, parameter, 
#                   levels, cmap=cm.jet,extend="both"
#                  )
    plt.colorbar()
    plt.xlabel('Latitude (deg)')
    plt.ylabel('Altitude (km)')
    plt.ylim(100,250)
    if savefig:
        plt.savefig('Figures/'+param+'_lat_alt.jpg',dpi=300)
    plt.show()