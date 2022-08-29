import numpy as np
from netCDF4 import Dataset
import warnings

from daedalusmase_derived_products.mod_tiegcm_utils import read_tiegcm_whole 

def integration_limits(tiegcm_file,timer_value,minlat,maxlat,minlon,maxlon,minalt,maxalt):
 
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

    print('minimum latitude:', min_lat, 'deg')
    print('maximum latitude:', max_lat, 'deg')
    print('minimum longitude:', min_lon, 'deg')
    print('maximum longitude:', max_lon, 'deg')
    print('minimum altitude:', min_height, 'km')
    print('maximum altitude:', max_height, 'km')
    print('')
    print('If you agree with the limits hit the Integration button, if not change the input and recalcualte the grid...')