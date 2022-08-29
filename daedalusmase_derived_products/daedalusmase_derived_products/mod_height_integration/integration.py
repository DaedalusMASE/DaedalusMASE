import numpy as np
from netCDF4 import Dataset
import warnings

from daedalusmase_derived_products.mod_tiegcm_utils import read_tiegcm_whole 

def integration(tiegcm_file,timer_value,parameter,minlat,maxlat,minlon,maxlon,minalt,maxalt):
 
    glat = read_tiegcm_whole(tiegcm_file,'lat')
    glon = read_tiegcm_whole(tiegcm_file,'lon')
    height = read_tiegcm_whole(tiegcm_file,'height')
    gtime = read_tiegcm_whole(tiegcm_file,'time')

    dalt=height[timer_value,1]-height[timer_value,0]
    min_lat=glat[minlat]
    max_lat=glat[maxlat]
    min_lon=glon[minlon]
    max_lon=glon[maxlon]
    min_height=height[timer_value,minalt]
    max_height=height[timer_value,maxalt]

    latrange=len(np.arange(minlat,maxlat))
    lonrange=len(np.arange(minlon,maxlon))
    altrange=len(np.arange(minalt,maxalt))


    param=read_tiegcm_whole(tiegcm_file,parameter)

    alloc_lat=np.zeros((altrange, latrange, lonrange),order='F')
    alloc_h_lat=np.zeros((altrange,lonrange),order='F')
    alloc_lon=np.zeros((altrange, lonrange),order='F')
    alloc_h_lon=np.zeros((altrange),order='F')
    aloc_lev=np.zeros((altrange),order='F')
    alloc_glob=[]



    for timer in range(timer_value,timer_value+1):
            # time_plot=gtime[timer]
            # maptime[timer]=time_plot

        for lev in range(0,altrange-1):

            for lat in range(0, latrange):

                for lon in range(0, lonrange):

                    QJ=((param[timer,lev,lat,lon]+param[timer,lev,lat+1,lon])/2)
                    radius=(6370+height[timer, lev])*1000 #radius in meters
                    dlat=(2.5*np.pi)/180
                    delta_z=radius*dlat #m
                    QJOULE_T=QJ*delta_z
                    alloc_lat[lev,lat,lon]=QJOULE_T

    for lev in range(0,altrange-1):
        for lon in range(0, lonrange):

            alloc_h_lat[lev,lon]=np.sum(alloc_lat[lev,:,lon])
            warnings.simplefilter('ignore')


    for lev in range(0,altrange-1):
        for lon in range(0, lonrange-1):
            QJLON=(alloc_h_lat[lev,lon]+alloc_h_lat[lev,lon+1])/2
            radius=(6370+height[timer, lev])*1000 #radius in meters
            dlon=(2.5*np.pi)/180
            delta_z=radius*dlon #m
            QJOULE_Tl=QJLON*delta_z
            alloc_lon[lev,lon]=QJOULE_Tl

            warnings.filterwarnings("ignore")
        
    for lev in range(0, altrange-1):
        alloc_h_lon[lev]=np.sum(alloc_lon[lev,:])
        warnings.filterwarnings("ignore")

    for lev in range(0,altrange-1):
        QJLEV=(alloc_h_lon[lev]+alloc_h_lon[lev+1])/2       
        delta_z=dalt*1000 #1km dalt
        QJ_temp_levd2=QJLEV*delta_z
        aloc_lev[lev]=QJ_temp_levd2


    QJ_global=np.sum(aloc_lev[:])
    alloc_glob.append(QJ_global/(10**12))

    warnings.filterwarnings("ignore")
    print("Calculation executed!")
    print('The total heating in the region is:')
    print(alloc_glob[0],'GW')

# warnings.simplefilter('ignore')