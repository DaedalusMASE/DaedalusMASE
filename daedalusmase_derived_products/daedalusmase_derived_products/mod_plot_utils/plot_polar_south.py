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

def plot_polar_south(param, Bound_lat, orbit_file,timer,savefig=True):
    
    x_value=alloc.maplon[:]
    y_value=alloc.maplat[:]
    
    time_begin=datetime.datetime(2015,3,15,0,0,0)
    time_plot=time_begin+datetime.timedelta(minutes=alloc.maptime[timer])
    
    X,Y = np.meshgrid(x_value,y_value)
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
        
   
    fig = plt.figure(figsize=(10,10))
    #m.fillcontinents(color='gray',lake_color='gray')
    m = Basemap(projection='spstere',boundinglat=-Bound_lat,lon_0=0,resolution='l', round=True,)
#     parameter, lons=addcyclic(parameter,x_value)
    lons, parameter = m.shiftdata(x_value, datain = parameter, lon_0=0)
    
    lon, lat = np.meshgrid(lons,y_value)
    x, y = m(lon, lat)
    fig = plt.figure(figsize=(10,10))
    #m.fillcontinents(color='gray',lake_color='gray')
    m.drawcoastlines()
    m.drawparallels(np.arange(-80.,81.,20.))
    m.drawmeridians(np.arange(-180.,181.,20.))
    m.drawmapboundary(fill_color='white')
    
       
    if param == 'Joule Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();
    if param == 'Frictional Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();
    if param == 'Ohmic Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();
    if param == 'Ohmic Heating per mass':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();
    if param == 'Ohmic Heating per pressure':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();
    if param == 'Convenction Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();
        
    if param == 'Ion Heating Rate':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();
        
    if param == 'Pressure_Ohmic ratio':
        cs = m.contourf(x,y,parameter,60,cmap='gist_ncar')
        plt.colorbar();
    if param == 'O+':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.colorbar();
    if param == 'O2+':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.colorbar();
    if param == 'NO+':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.colorbar();
    if param == 'σNO+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.colorbar();
    if param == 'σO2+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.colorbar();
    if param == 'σ':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.colorbar();
    if param == 'vNO+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.colorbar();
        
    if param == 'Wind Heating':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();
    if param == 'Energy':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();
    if param == 'Mechanical Power':
        cs = m.contourf(x,y,parameter,60,cmap='jet')
        plt.colorbar();  
    if param == 'Pedersen':
        cs = m.contourf(x,y,parameter,60,cmap='afmhot')
        plt.colorbar();
    if param == 'Hall':
        cs = m.contourf(x,y,parameter,60,cmap='afmhot')
        plt.colorbar();
    if param == 'O':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.colorbar();
    if param == 'O2':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.colorbar();
    if param == 'N2':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.colorbar();
    if param == 'Ne':
        cs = m.contourf(x,y,parameter,60,cmap='cubehelix')
        plt.colorbar();
    if param == 'Potential':
        cs = m.contourf(x,y,parameter,60,cmap='BrBG')
        plt.colorbar();
        m.contour(x,y,parameter,20,alpha=0.7, colors='k')
    if param == 'Ti':
        cs = m.contourf(x,y,parameter,60,cmap='gnuplot')
        plt.colorbar(); 
    if param == 'Te':
        cs = m.contourf(x,y,parameter,60,cmap='gnuplot')
        plt.colorbar(); 
    if param == 'Tn':
        cs = m.contourf(x,y,parameter,60,cmap='gnuplot')
        plt.colorbar(); 
    if param == 'νO+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.colorbar(); 
    if param == 'νO2+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.colorbar(); 
    if param == 'νin':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.colorbar(); 
    if param == 'νen':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.colorbar(); 
    if param == 'σO+n':
        cs = m.contourf(x,y,parameter,60,cmap='CMRmap')
        plt.colorbar(); 
    if param == 'Parallel':
        cs = m.contourf(x,y,parameter,60,cmap='afmhot')
        plt.colorbar(); 
    if param == 'Pressure':
        cs = m.contourf(x,y,parameter,60,cmap='RdPu')
        plt.colorbar();     
    
    
    # if night_checkbox.value == True:
    #     CS=m.nightshade(time_plot)
        
        
    if param == 'Joule Heating':
#         plt.title("Joule Heating Rate (mW/m^3)_North Pole- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
#         cbJH.set_label('Joule Heating Rate [$mW/m^{3}$]')
        fig.text(0.35, 0.90, 'Joule Heating Rate', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/m^{3}$]" , fontsize=17)
    
    if param == 'Frictional Heating':
        fig.text(0.35, 0.90, 'Frictional Heating Rate', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/m^{3}$]" , fontsize=17)
    if param == 'Ohmic Heating':
        fig.text(0.35, 0.90, 'Ohmic Heating Rate', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/m^{3}$]" , fontsize=17)
    if param == 'Ohmic Heating per mass':
        fig.text(0.35, 0.90, 'Ohmic Heating per Mass', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/kg$]" , fontsize=17)
    if param == 'Ohmic Heating per pressure':
        fig.text(0.35, 0.90, 'Ohmic Heating per Pressure', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$1/s$]" , fontsize=17)
    if param == 'Convenction Heating':
        fig.text(0.35, 0.90, 'Convenction Heating Rate', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/m^{3}$]" , fontsize=17)
    if param == 'Wind Heating':
        fig.text(0.35, 0.90, 'Wind Heating Rate', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/m^{3}$]" , fontsize=17)
    if param == 'Energy':
        fig.text(0.35, 0.90, 'Energy Dissipation/Generation', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/m^{3}$]" , fontsize=17)
    if param == 'Mechanical Power':
        fig.text(0.35, 0.90, 'Mechanical Power Rate', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/m^{3}$]" , fontsize=17)   
        
    if param == 'Ion Heating Rate':
        fig.text(0.35, 0.90, 'Ion Heating Rate', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/m^{3}$]" , fontsize=17) 
        
    if param == 'Ti':
        fig.text(0.35, 0.90, 'Ion Temperature', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$K$]" , fontsize=17)  
    if param == 'Te':
        fig.text(0.35, 0.90, 'Electron Temperature', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$K$]" , fontsize=17)  
    if param == 'Tn':
        fig.text(0.35, 0.90, 'Neutral Temperature', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$mW/m^{3}$]" , fontsize=17)  
    if param == 'νO+n':
        fig.text(0.35, 0.90, 'O+ Collision Frequency', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$Hz$]" , fontsize=17)  
    if param == 'νO2+n':
        fig.text(0.35, 0.90, 'O2+ Collision Frequency', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$Hz$]" , fontsize=17)  
    if param == 'νin':
        fig.text(0.35, 0.90, 'Ion-Neutral Collision Frequency', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$Hz$]" , fontsize=17)  
    if param == 'νen':
        fig.text(0.35, 0.90, 'Electron-Neutral Collision Frequency', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$Hz$]" , fontsize=17)  
    if param == 'σO+n':
        fig.text(0.35, 0.90, 'O+ Cross Section', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$m^{2}$]" , fontsize=17)  
    if param == 'Parallel':
        fig.text(0.35, 0.90, 'Pendersen Conductivity', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$10^{-5} mho/m$]" , fontsize=17)  
    if param == 'Pressure_Ohmic ratio':
        fig.text(0.35, 0.90, 'Pressure/Heaitng ratio', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$s$]" , fontsize=17)
    if param == 'O+':
        fig.text(0.35, 0.90, 'O+ Density', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.70, 0.90, "[$cm^{-3}$]" , fontsize=17)
    if param == 'O2+':
        fig.text(0.35, 0.90, 'O2+ Density', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.70, 0.90, "[$cm^{-3}$]" , fontsize=17)
    if param == 'NO+':
        fig.text(0.35, 0.90, 'NO+ Density', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.70, 0.90, "[$cm^{-3}$]" , fontsize=17)
    if param == 'σNO+n':
        fig.text(0.35, 0.90, 'NO+ Cross Section', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$Hz$]" , fontsize=17)  
    if param == 'σO2+n':
        fig.text(0.35, 0.90, 'O2+ Cross Section', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$Hz$]" , fontsize=17)  
    if param == 'σ':
        fig.text(0.35, 0.90, 'Ion Cross Section', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$Hz$]" , fontsize=17)  
    if param == 'vNO+n':
        fig.text(0.35, 0.90, 'NO+ Collision Frequency', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.68, 0.90, "[$Hz$]" , fontsize=17)  
        
    if param == 'Pedersen':
#         plt.title("Pendersen Conductivity ($10^{-5}$ mho/m)_North Pole- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
#         cbJH.set_label('Pendersen Conductivity ($10^{-5}$ mho/m)')
        fig.text(0.35, 0.90, 'Pendersen Conductivity', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.64, 0.90, "[$10^{-5} mho/m$]" , fontsize=17)
        
    if param == 'Hall':
#         plt.title("Hall Conductivity (Si/m)_North Pole- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
#         cbJH.set_label('Hall Conductivity (Si/m)')
        fig.text(0.35, 0.90, 'Hall Conductivity', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.64, 0.90, "[$10^{-5} mho/m$]" , fontsize=17)
        
    if param == 'O':
#         plt.title("O ($cm_{-3}$)_North Pole- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
#         cbJH.set_label('O ($cm^{-3}$)')
        fig.text(0.35, 0.90, 'Atomic Oxygen', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.70, 0.90, "[$m^{-3}$]" , fontsize=17)
        
    if param == 'O2':
#         plt.title("$O_{2}$ ($cm^{-3}$)_North Pole- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
#         cbJH.set_label('$O_{2}$ ($cm^{-3}$)')
        fig.text(0.35, 0.90, 'Molecular Oxygen', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.70, 0.90, "[$m^{-3}$]" , fontsize=17)
        
    if param == 'N2':
#         plt.title("$N_{2}$ ($cm^{-3}$)_North Pole- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
#         cbJH.set_label('$N_{2}$ ($cm^{-3}$)')
        fig.text(0.35, 0.90, 'Molecular Nitrogen', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.70, 0.90, "[$m^{-3}$]" , fontsize=17)
        
    if param == 'Ne':
#         plt.title("Electron Density ($m^{-3}$)_North Pole- %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
#         cbJH.set_label('$N_{e}$ ($m^{-3}$)')
        fig.text(0.35, 0.90, 'Electron Density', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.70, 0.90, "[$m^{-3}$]" , fontsize=17)
        
    if param == 'Potential':
        fig.text(0.35, 0.90, 'Electric Potential', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.70, 0.90, "[$kV$]" , fontsize=17)
    if param == 'Pressure':
        fig.text(0.35, 0.90, 'Pressure', fontsize=17, fontweight='bold')
        fig.text(0.35, 0.13, "%s" % time_plot.strftime("%d %b %Y"), fontsize=15)
        fig.text(0.68, 0.13, "%s" % time_plot.strftime("%H:%M:%S"), fontsize=15)
        fig.text(0.70, 0.90, "[$Pa$]" , fontsize=17) 


    if savefig:
        plt.savefig('Figures/'+param+'_polar_south.jpg',dpi=300)    
    plt.show()