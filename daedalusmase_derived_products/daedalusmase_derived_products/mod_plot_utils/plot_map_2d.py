"""
sub_heating_sources.plot_map_2d

**Description**:
_____________________________________________________________________________________________________________________

Plot quantities in 2D map
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

def plot_map_2d(param,timer,savefig=True):

    x_value=alloc.maplon[:]
    y_value=alloc.maplat[:][::-1]
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
      
    plt.rcParams['figure.figsize'] = (15, 8)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1,  aspect='equal')

  
    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # resolution = 'c' means use crude resolution coastlines.
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
                llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    
#     lonsout,parameter=m.shiftdata(x_value, datain = background, lon_0=0)
    
    lon, lat = np.meshgrid(x_value,y_value)
    
    

    x, y = m(lon, lat)
    if param == 'Pedersen':
        sc=m.imshow(parameter,cmap='afmhot',interpolation = 'bicubic')
    if param == 'Joule Heating':
        
#         sc = m.contourf(x,y,np.log(parameter), np.arange(-13, -2, .05),cmap='jet',extend='both')  
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')
    if param == 'Ohmic Heating per mass':
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')
    if param == 'Ohmic Heating per pressure':
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')
    if param == 'Frictional Heating':
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')
    if param == 'Ohmic Heating':
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')
    if param == 'Convenction Heating':
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')
    if param == 'Wind Heating':
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')
    if param == 'Energy':
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')
    if param == 'Mechanical Power':
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')

    if param == 'Ion Heating Rate':
        sc=m.imshow(parameter,cmap='jet',interpolation = 'bicubic')

    if param == 'Pressure_Ohmic ratio':
        sc=m.imshow(parameter,cmap='gist_ncar',interpolation = 'bicubic')
    if param == 'O+':
        sc=m.imshow(parameter,cmap='cubehelix',interpolation = 'bicubic')
    if param == 'O2+':
        sc=m.imshow(parameter,cmap='cubehelix',interpolation = 'bicubic')
    if param == 'NO+':
        sc=m.imshow(parameter,cmap='cubehelix',interpolation = 'bicubic')
    if param == 'σNO+n':
        sc=m.imshow(parameter,cmap='CMRmap',interpolation = 'bicubic')
    if param == 'σO2+n':
        sc=m.imshow(parameter,cmap='CMRmap',interpolation = 'bicubic')
    if param == 'σ':
        sc=m.imshow(parameter,cmap='CMRmap',interpolation = 'bicubic')
    if param == 'vNO+n':
        sc=m.imshow(parameter,cmap='CMRmap',interpolation = 'bicubic')
    
        
    if param == 'Ti':
        sc=m.imshow(parameter,cmap='gnuplot',interpolation = 'bicubic')
    if param == 'Te':
        sc=m.imshow(parameter,cmap='gnuplot',interpolation = 'bicubic')
    if param == 'Tn':
        sc=m.imshow(parameter,cmap='gnuplot',interpolation = 'bicubic')
    if param == 'νO+n':
        sc=m.imshow(parameter,cmap='CMRmap',interpolation = 'bicubic')
    if param == 'νO2+n':
        sc=m.imshow(parameter,cmap='CMRmap',interpolation = 'bicubic')
    if param == 'νin':
        sc=m.imshow(parameter,cmap='CMRmap',interpolation = 'bicubic')
    if param == 'νen':
        sc=m.imshow(parameter,cmap='CMRmap',interpolation = 'bicubic')
    if param == 'σO+n':
        sc=m.imshow(parameter,cmap='CMRmap',interpolation = 'bicubic')
    if param == 'Parallel':
        sc=m.imshow(parameter,cmap='afmhot',interpolation = 'bicubic')
        
    if param == 'Ne':
        sc=m.imshow(parameter,cmap='cubehelix',interpolation = 'bicubic')
    if param == 'Hall':
        sc=m.imshow(parameter,cmap='afmhot',interpolation = 'bicubic')
    if param == 'O':
        sc=m.imshow(parameter,cmap='cubehelix',interpolation = 'bicubic')
    if param == 'O2':
        sc=m.imshow(parameter,cmap='cubehelix',interpolation = 'bicubic')
    if param == 'N2':
        sc=m.imshow(parameter,cmap='cubehelix',interpolation = 'bicubic')
    if param == 'Potential':
        sc=m.imshow(parameter,cmap='BrBG',interpolation = 'bicubic')
    if param == 'Pressure':
        sc=m.imshow(parameter,cmap='RdPu',interpolation = 'bicubic')
        
        
    # if night_checkbox.value == True:
    #     CS=m.nightshade(time_plot, alpha=0.3)
        
    #m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels(np.arange(-90.,91.,30.))
    m.drawmeridians(np.arange(-180.,181.,60.))
    #m.drawmapboundary(fill_color='aqua')
    plt.xticks(np.arange(-180.,181.,60.))
    plt.yticks(np.arange(-90.,91.,30.))
    plt.xlabel('Lon (deg)')
    plt.ylabel('Lat (deg)')

  
    if param == 'Joule Heating':
        plt.title("Joule Heating Rate (log($mW/m^{3}$)) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Frictional Heating':
        plt.title("Frictional Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Ohmic Heating':
        plt.title("Ohmic Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Ohmic Heating per mass':
        plt.title("Ohmic Heating per Mass (mW/kg) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Ohmic Heating per pressure':
        plt.title("Ohmic Heating per pressure (1/s) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Convenction Heating':
        plt.title("Convenction Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Wind Heating':
        plt.title("Wind Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Energy':
        plt.title("Energy Dissipation/Generation (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Mechanical Power':
        plt.title("Mechanical Power (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        
    if param == 'Ion Heating Rate':
        plt.title("Ion Heating Rate (mW/m^3) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        
    if param == 'Pressure_Ohmic ratio':
        plt.title("Pressure/Heating Ratio (s) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'O+':
        plt.title("O+ Density ($cm^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'O2+':
        plt.title("O2+ Density ($cm^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'NO+':
        plt.title("NO+ Density ($cm^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'σNO+n':
        plt.title("NO+ cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'σO2+n':
        plt.title("O2+ cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'σ':
        plt.title("Ion cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'vNO+n':
        plt.title("NO+-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    
    if param == 'Ti':
        plt.title("Ion Temperature (K) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Te':
        plt.title("Electron Temeperature (K) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Tn':
        plt.title("Neutral Temperature (K) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'νO+n':
        plt.title("O+-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'νO2+n':
        plt.title("O2+-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'νin':
        plt.title("Ion-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'νen':
        plt.title("Electron-Neutral collision frequency (Hz) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'σO+n':
        plt.title("O+ cross section (m^2) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Parallel':
        plt.title("Parallel Conductivity (Si/m) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))

    if param == 'Pedersen':
        plt.title("Pendersen Conductivity ($10^{-5}$ mho/m) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Hall':
        plt.title("Hall Conductivity (Si/m) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'O':
        plt.title("O ($m^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'O2':
        plt.title("$O_{2}$ ($m^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'N2':
        plt.title("$N_{2}$ ($m^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Ne':
        plt.title("Electron Density ($m^{-3}$) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
    if param == 'Pressure':
        plt.title("Pressure (Pa) - %s" % time_plot.strftime("%d %b %Y %H:%M:%S"))
        
    
        
    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.2, aspect=20, label='[w/m^3]')
    cbar = plt.colorbar(sc, cax = cax1)
    if savefig:
        plt.savefig('Figures/'+param+'_map.jpg',dpi=300)
    plt.show() 