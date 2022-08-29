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

def plot_ortho(param, center_lat,center_lon,timer,savefig=True):
    x_value=alloc.maplon[:]
    y_value=alloc.maplat[:]
    
    time_begin=datetime.datetime(2015,3,15,0,0,0)
    time_plot=time_begin+datetime.timedelta(minutes=alloc.maptime[timer])
    
    
    if param == 'Pedersen':
        parameter = alloc.pedersen_2D
    if param == 'Joule Heating':
        parameter = alloc.joule_2D
    if param == 'O+':
        parameter = alloc.NOp_2D
    if param == 'O2+':
        parameter = alloc.NO2p_2D
    if param == 'NO+':
        parameter = alloc.NNOp_2D
    if param == 'σ':
        parameter = alloc.cross_in_2D
        
    if param == 'Ion Heating Rate':
        parameter = alloc.qDTi_n_2D
        
        
    if param == 'Frictional Heating':
        parameter = alloc.frictional_2D
    if param == 'Ohmic Heating':
        parameter = alloc.ohmic_2D
    if param == 'Convenction Heating':
        parameter = alloc.convection_heating_2D
    if param == 'Wind Heating':
        parameter = alloc.wind_heating_2D
    if param == 'Mechanical Power':
        parameter = alloc.mech_power_2D
        
    if param == 'Ti':
        parameter = alloc.Ti_2D
    if param == 'Te':
        parameter = alloc.Te_2D
    if param == 'Tn':
        parameter = alloc.Tn_2D
    if param == 'νin':
        parameter = alloc.vin_2D
    if param == 'νen':
        parameter = alloc.ven_2D
    if param == 'Parallel':
        parameter = alloc.parallel_2D
        
    if param == 'Hall':
        parameter = alloc.hall_2D
    if param == 'O':
        parameter = alloc.NO_2D
    if param == 'O2':
        parameter = alloc.NO2_2D
    if param == 'N2':
        parameter = alloc.NN2_2D
    if param == 'Ne':
        parameter = alloc.Ne_2D
    if param == 'Potential':
        parameter = alloc.Pot_2D
               

    m = Basemap(projection='ortho',lat_0=center_lat,lon_0=center_lon,resolution='l')
#     parameter, lons=addcyclic(parameter,x_value)
    lons, parameter = m.shiftdata(x_value, datain = parameter, lon_0=0)
    
    lon, lat = np.meshgrid(lons,y_value)
    x, y = m(lon, lat)
    fig = plt.figure(figsize=(10,10))
#     m.fillcontinents(color='gray',lake_color='gray')
    m.drawcoastlines()
#     m.bluemarble()
    m.drawparallels(np.arange(-80.,81.,20.))
    m.drawmeridians(np.arange(-180.,181.,20.))
    m.drawmapboundary(fill_color='white')
    m.bluemarble()
    # if night_checkbox.value == True:
    #     CS=m.nightshade(time_plot)
    if param == 'Joule Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Joule Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        
    if param == 'Frictional Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Frictional Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Ohmic Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Ohmic Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Ohmic Heating per mass':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Ohmic Heating per Mass (mW/kg) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Ohmic Heating per pressure':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Ohmic Heating per Mass (mW/(Pa*m^3)) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Convenction Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Convenction Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Wind Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Wind Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Energy':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Energy Dissipation/Generation (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Mechanical Power':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Mechanical Power (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S")) 
        
    if param == 'Ion Heating Rate':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.title("Ion Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    
    if param == 'Pressure_Ohmic ratio':
        cs = m.contourf(x,y,parameter,60,cmap='gist_ncar')
        plt.title("Pressure/Heating ratio (s) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S")) 
    if param == 'O+':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.title("O+ Density ($cm^{-3}$)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'O2+':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.title(")2+ Density ($cm^{-3}$)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'NO+':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.title("NO+ Density ($cm^{-3}$)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'σNO+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.title("NO+ cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'σO2+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.title("O2+ cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'σ':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.title("Ion cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'vNO+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.title("NO+-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        
    if param == 'Ti':
        cs = m.contourf(x,y,parameter,60,cmap='gnuplot')
        plt.title("Ion Temperature (K) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Te':
        cs = m.contourf(x,y,parameter,60,cmap='gnuplot')
        plt.title("Electron Temeperature (K) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Tn':
        cs = m.contourf(x,y,parameter,60,cmap='gnuplot')
        plt.title("Neutral Temperature (K) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'νO+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.title("O+-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'νO2+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.title("O2+-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'νin':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.title("Ion-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'νen':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.title("Electron-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'σO+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.title("O+ cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Parallel':
        cs = m.contourf(x,y,parameter,60,cmap='afmhot')
        plt.title("Parallel Conductivity (Si/m) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        
    if param == 'Pedersen':
        cs = m.contourf(x,y,parameter,60,cmap='afmhot')
        plt.title("Pendersen Conductivity ($10^{-5}$ mho/m)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Hall':
        cs = m.contourf(x,y,parameter,60,cmap='afmhot')
        plt.title("Hall Conductivity ($10^{-5}$ mho/m)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'O':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.title("O ($m_{-3}$)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'O2':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.title("$O_{2}$ ($m^{-3}$)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'N2':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.title("$N_{2}$ ($m^{-3}$)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Ne':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.title("Electron Density ($m^{-3}$)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Potential':
        cs = m.contourf(x,y,parameter,60,cmap='BrBG')
        plt.title("Electirc Potential (kV)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Pressure':
        cs = m.contourf(x,y,parameter,60,cmap='RdPu')
        plt.title("Pressure (Pa)- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        
    plt.colorbar(cs);
    if savefig:
        plt.savefig('Figures/'+param+'_ortho.jpg',dpi=300)
    plt.show()