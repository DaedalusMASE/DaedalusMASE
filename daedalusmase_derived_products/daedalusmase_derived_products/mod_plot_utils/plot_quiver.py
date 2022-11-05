"""
sub_heating_sources.plot_quiver

**Description**:
_____________________________________________________________________________________________________________________

Plot vector quantities 
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

"""


import numpy as np
from daedalusmase_derived_products.mod_tiegcm_utils import allocations as alloc
import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.mlab as mlab
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_quiver(ploting,back,vec,timer,savefig=True):
    x_value=alloc.maplon[:]
    y_value=alloc.maplat[:]
    
    time_begin=datetime.datetime(2015,3,15,0,0,0)
    time_plot=time_begin+datetime.timedelta(minutes=alloc.maptime[timer])
    
    m = Basemap(projection='npstere',boundinglat=40,lon_0=0,resolution='l', round=True,)
        
    if back == 'Potential':
        background=alloc.Pot_2D
        cmap='BrBG'
    if back == 'Joule Heating':
        background = alloc.joule_2D
        cmap='jet'
    if back == 'Pedersen':
        background = alloc.pedersen_2D
        cmap='afmhot'
    if back == 'Hall':
        background = alloc.hall_2D
        cmap='afmhot'
    if back == 'Current':
        background = alloc.J_mag_2D
        cmap='viridis'
    if back == 'Frictional Heating':
        background = alloc.frictional_2D
        cmap='jet'
    if back == 'Ohmic Heating':
        background = alloc.ohmic_2D
        cmap='jet'
    if back == 'Convenction Heating':
        background = alloc.convection_heating_2D
        cmap='jet'
    if back == 'Wind Heating':
        background = alloc.wind_heating_2D
        cmap='jet'
    if back == 'Mechanical Power':
        background = alloc.mech_power_2D
        cmap='jet'
    if back == 'Ion Drift':
        background = alloc.vi_mag_2D
        cmap='ocean'
    if back == 'Parallel':
        background = alloc.parallel_2D
        cmap='afmhot'
    if back == 'JxB':
        background=alloc.jxb_mag_2D
        cmap='BrBG'

    if vec == 'JxB':
        Veast=alloc.forcing_e_2D
        Vnorth=alloc.forcing_n_2D   
    if vec == 'Electric Field':
        Veast=alloc.Ee_2D
        Vnorth=alloc.En_2D
    if vec == 'Magnetic Field':
        Veast=alloc.Be_2D
        Vnorth=alloc.Bn_2D
    if vec == 'Pedersen Current':
        Veast=alloc.jpede_2D
        Vnorth=alloc.jpedn_2D
    if vec == 'Hall Current':
        Veast=alloc.jhalle_2D
        Vnorth=alloc.jhalln_2D
    if vec == 'Perpendicular Current':
        Veast=alloc.jperpe_2D
        Vnorth=alloc.jperpe_2D
    if vec == 'Ion Velocity':
        Veast=alloc.veli_e_2D
        Vnorth=alloc.veli_n_2D
    if vec == 'Neutral Winds':
        Veast=alloc.Une_2D
        Vnorth=alloc.Unn_2D

    
    lonsout,parameter=m.shiftdata(x_value, datain = background, lon_0=0)
    
    lon, lat = np.meshgrid(lonsout,y_value)
    
    

    x, y = m(lon, lat)

    
    fig = plt.figure(figsize=(10,10))
    m.drawcoastlines()
    m.drawparallels(np.arange(-80.,81.,20.))
    m.drawmeridians(np.arange(-180.,181.,20.))
    m.drawmapboundary(fill_color='white')
 
    
    Eeproj,Enproj,xx,yy = m.transform_vector(Veast,Vnorth,lonsout,y_value,144,72,returnxy=True,masked=True)
    
    Emag=np.sqrt(Eeproj**2+Enproj**2)
    
    if ploting == 'Streamplot':
        cf=m.contourf(x,y,background,50,cmap=cmap)
        cbar=plt.colorbar(cf,fraction=0.046, pad=0.04)
        
        if back == 'Potential':
            cbar.ax.set_ylabel('Electric Potential (V)', rotation=270, size=20, labelpad=30)
        if back == 'Joule Heating':
            cbar.ax.set_ylabel('Joule Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Frictional Heating':
            cbar.ax.set_ylabel('Frictional Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Ohmic Heating':
            cbar.ax.set_ylabel('Ohmic Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Convenction Heating':
            cbar.ax.set_ylabel('Convenction Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Wind Heating':
            cbar.ax.set_ylabel('Wind Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Mechanical Power':
            cbar.ax.set_ylabel('Mechanical Power ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Energy':
            cbar.ax.set_ylabel('Energy Dissipation/Generation ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Ion Drift':
            cbar.ax.set_ylabel('Ion Drift($m/s$)', rotation=270, size=20, labelpad=30)
        if back == 'Pedersen':
            cbar.ax.set_ylabel('Penersen Conductivity ($10^{-5} mho/m$)', rotation=270, size=20, labelpad=30)
        if back == 'Hall':
            cbar.ax.set_ylabel('Hall Conductivity ($10^{-5} mho/m$)', rotation=270, size=20, labelpad=30)
        if back == 'Parallel':
            cbar.ax.set_ylabel('Parallel Conductivity ($10^{-5} mho/m$)', rotation=270, size=20, labelpad=30)
        if back == 'Current':
            cbar.ax.set_ylabel('Current Density ($A/m^{2}$)', rotation=270, size=20, labelpad=30)
        if back == 'JxB':
            cbar.ax.set_ylabel('JxB Forcing', rotation=270, size=20, labelpad=30)            
            
            
            
    if ploting == 'Vector':
        cf=m.contourf(x,y,background,50,cmap=cmap)
        cbar=plt.colorbar(cf,fraction=0.046, pad=0.04)
        if back == 'Potential':
            cbar.ax.set_ylabel('Electric Potential (V)', rotation=270, size=20, labelpad=30)
        if back == 'Joule Heating':
            cbar.ax.set_ylabel('Joule Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Frictional Heating':
            cbar.ax.set_ylabel('Frictional Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Ohmic Heating':
            cbar.ax.set_ylabel('Ohmic Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Convenction Heating':
            cbar.ax.set_ylabel('Convenction Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Wind Heating':
            cbar.ax.set_ylabel('Wind Heating ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Mechanical Power':
            cbar.ax.set_ylabel('Mechanical Power ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Energy':
            cbar.ax.set_ylabel('Energy Dissipation/Generation ($mW/m^{3}$)', rotation=270, size=20, labelpad=30)
        if back == 'Ion Drift':
            cbar.ax.set_ylabel('Ion Drift($m/s$)', rotation=270, size=20, labelpad=30)
        if back == 'Pedersen':
            cbar.ax.set_ylabel('Penersen Conductivity ($10^{-5} mho/m$)', rotation=270, size=20, labelpad=30)
        if back == 'Hall':
            cbar.ax.set_ylabel('Hall Conductivity ($10^{-5} mho/m$)', rotation=270, size=20, labelpad=30)
        if back == 'Parallel':
            cbar.ax.set_ylabel('Parallel Conductivity ($10^{-5} mho/m$)', rotation=270, size=20, labelpad=30)
        if back == 'Current':
            cbar.ax.set_ylabel('Current Density ($A/m^{2}$)', rotation=270, size=20, labelpad=30)
        if back == 'JxB':
            cbar.ax.set_ylabel('JxB Forcing', rotation=270, size=20, labelpad=30)        
   
    if ploting == 'Vector':
        vecplot=m.quiver(xx[::2],yy[::2],Eeproj[::2],Enproj[::2],units='width')
        if vec == 'Neutral Winds':
            qk = plt.quiverkey(vecplot, 0.1, 0.01, 200, '200 m/s', labelpos='W',fontproperties={'size': 20})
            fig.text(0.1, 0.85, 'Neutral Winds', fontsize=25, fontweight='bold')
        if vec == 'Ion Velocity':
            qk = plt.quiverkey(vecplot, 0.1, 0.01, 200, '200 m/s', labelpos='W',fontproperties={'size': 20})
            fig.text(0.1, 0.85, 'Ion Velocity', fontsize=25, fontweight='bold')
        if vec == 'Electric Field':
            qk = plt.quiverkey(vecplot, 0.1, 0.01, 0.1, '0.1 V/m', labelpos='W',fontproperties={'size': 20})
            fig.text(0.1, 0.85, 'Electric Field', fontsize=25, fontweight='bold')
        if vec == 'Pedersen Current':
            qk = plt.quiverkey(vecplot, 0.1, 0.01, 10**(-5), '$10^{-5}$ $A/m^{2}$', labelpos='W',fontproperties={'size': 20})
            fig.text(0.1, 0.87, 'Pedersen current density', fontsize=25, fontweight='bold')
        if vec == 'Hall Current':
            qk = plt.quiverkey(vecplot, 0.1, 0.01, 10**(-6), '$10^{-6}$ $A/m^{2}$', labelpos='W',fontproperties={'size': 20})
            fig.text(0.1, 0.87, 'Hall current density', fontsize=25, fontweight='bold')
        if vec == 'Peprendicular Current':
#             qk = plt.quiverkey(vecplot, 0.1, 0.01, 10**(-6), '$10^{-6}$ $A/m^{2}$', labelpos='W',fontproperties={'size': 20})
            fig.text(0.1, 0.87, 'Perpendicular current density', fontsize=25, fontweight='bold')
        if vec == 'JxB':
#             qk = plt.quiverkey(vecplot, 0.1, 0.01, 10**(-6), '$10^{-6}$ $N/m^{3}$', labelpos='W',fontproperties={'size': 20})
            fig.text(0.1, 0.87, 'JxB', fontsize=25, fontweight='bold')
        if vec == 'Magnetic Field':
#             qk = plt.quiverkey(vecplot, 0.1, 0.01, 10**(-9), '$10^{-9}$ $T$', labelpos='W',fontproperties={'size': 20})
            fig.text(0.1, 0.87, 'Magnetic Field', fontsize=25, fontweight='bold')


    if ploting == 'Streamplot':
        m.streamplot(xx,yy,Eeproj,Enproj, density=[1, 1],linewidth=2,color='royalblue')
        if vec == 'Neutral Winds':
            fig.text(0.1, 0.85, 'Neutral Winds', fontsize=25, fontweight='bold')
        if vec == 'Ion Velocity':
             fig.text(0.1, 0.85, 'Ion Velocity', fontsize=25, fontweight='bold')
        if vec == 'Electric Field':
             fig.text(0.1, 0.85, 'Electric Field', fontsize=25, fontweight='bold')
        if vec == 'Pedersen Current':
             fig.text(0.1, 0.87, 'Pedersen current density', fontsize=25, fontweight='bold')
        if vec == 'Hall Current':
             fig.text(0.1, 0.87, 'Hall current density', fontsize=25, fontweight='bold')
        if vec == 'Peprendicular Current':
             fig.text(0.1, 0.87, 'Perpendicular current density', fontsize=25, fontweight='bold')
        if vec == 'JxB':
             fig.text(0.1, 0.87, 'JxB', fontsize=25, fontweight='bold')
        if vec == 'Magnetic Field':
             fig.text(0.1, 0.87, 'Magnetic Field', fontsize=25, fontweight='bold')
        
    # if night_checkbox.value == True:
    #     m.nightshade(time_plot)
    if savefig:
        plt.savefig('Figures/'+back+'_'+vec+'_quiver.jpg',dpi=300)
    plt.show()