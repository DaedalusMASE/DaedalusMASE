import numpy as np
from netCDF4 import Dataset
import warnings

from daedalusmase_derived_products.mod_tiegcm_utils import read_tiegcm_whole 

def height_integration(tiegcm_file,timer_value,parameter,minlat,maxlat,minlon,maxlon,minalt,maxalt):

    nc=Dataset(tiegcm_file)
    # Get data from TIEGCM Model file
    glat = tiegcm_file.variables['lat'][:] #geographic latitude in deg
    glon = tiegcm_file.variables['lon'][:] #geographic longitude in deg
    glev = tiegcm_file.variables['ilev'][:] #interface levels
    gtime = tiegcm_file.variables['time'][:]
    zg = tiegcm_file.variables['ZGMID'][:] #Geometric height in cm
    tiegcm_file.close() #close input file

    min_lat=glat[minlat]
    max_lat=glat[maxlat]
    min_lon=glat[minlon]
    max_lon=glat[maxlon]

    print(min_lat)
    print(max_lat)
    print(min_lon)
    print(max_lon)

    param=read_tiegcm_whole(tiegcm_file,parameter)
    #allocations
    alloc=np.zeros((72,144),order='F')

    Sigma_P_tmp=np.zeros((len(glev), len(glat), len(glon)),order='F')
    Sigma_H_tmp=np.zeros((len(glev), len(glat), len(glon)),order='F')
    QA_temp=np.zeros((len(glev), len(glat), len(glon)),order='F')
    QW_temp=np.zeros((len(glev), len(glat), len(glon)),order='F')
    QJ_temp=np.zeros((len(glev), len(glat), len(glon)),order='F')

    for timer in range(timer_value,timer_value+1):
            time_plot=gtime[timer]
            maptime[timer]=time_plot

            for lev in range(0, len(glev)-1):

                for lat in range(0, len(glat)):

                    for lon in range(0, len(glon)):

                            # GEO coordinates of desired point
                        alt_p_0 = zg[timer, lev, lat, lon] / 100 #cm to m
                        alt_p_1 = zg[timer, lev+1, lat, lon] / 100 #cm to m
                        lat_p = glat[lat]   #deg
                        lon_p = glon[lon]   #deg
                        maplat[lat]=glat[lat] #output 
                        maplon[lon]=glon[lon] #output 
                        timeg=gtime[timer]

                        delta_z=(alt_p_1-alt_p_0)

                        SP=(PED_all[timer,lev,lat,lon]+PED_all[timer,lev+1,lat,lon])/2

                        SH=(HALL_all[timer,lev,lat,lon]+HALL_all[timer,lev+1,lat,lon])/2

                        QA=(QAMIE_all[timer,lev,lat,lon]+QAMIE_all[timer,lev+1,lat,lon])/2

                        QW=(QWIND_all[timer,lev,lat,lon]+QWIND_all[timer,lev+1,lat,lon])/2
                        
                        QJ=((QAMIE_all[timer,lev,lat,lon]+QWIND_all[timer,lev,lat,lon]
                             +QAMIE_all[timer,lev+1,lat,lon]+QWIND_all[timer,lev+1,lat,lon])/2)

                        SIGMAPEDERSEN=SP*delta_z

                        SIGMAHALL=SH*delta_z
                        QAMIE_T=QA*delta_z
                        QWIND_T=QW*delta_z
                        QJOULE_T=QJ*delta_z

                        Sigma_P_tmp[lev,lat,lon]=SIGMAPEDERSEN
                        Sigma_H_tmp[lev,lat,lon]=SIGMAHALL
                        QA_temp[lev,lat,lon]=QAMIE_T
                        QW_temp[lev,lat,lon]=QWIND_T
                        QJ_temp[lev,lat,lon]=QJOULE_T
                        
                        
                        
                        warnings.simplefilter('ignore')

                        # print (SIGMAPEDERSEN)
    


    for lat in range(0, len(glat)):

        for lon in range(0, len(glon)):

            Sigma_P[lat,lon]=np.sum(Sigma_P_tmp[:-2,lat,lon])
            Sigma_H[lat,lon]=np.sum(Sigma_H_tmp[:-2,lat,lon])
            QA_h[lat,lon]=np.sum(QA_temp[:-2,lat,lon])
            QW_h[lat,lon]=np.sum(QW_temp[:-2,lat,lon])
            QJ_h[lat,lon]=np.sum(QJ_temp[:-2,lat,lon])
            warnings.simplefilter('ignore')

    


    print("Calculation executed!")

warnings.simplefilter('ignore')