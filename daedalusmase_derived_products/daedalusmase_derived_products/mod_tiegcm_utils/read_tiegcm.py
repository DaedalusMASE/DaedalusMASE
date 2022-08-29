"""
tiegcm_utils.read_tiegcm

**Description**:
_____________________________________________________________________________________________________________________

Read tiegcm input file
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

"""

from netCDF4 import Dataset

def read_tiegcm(tiegcm_file,variable,timer, lev, lat, lon):

    TIEGCM = Dataset(tiegcm_file)

        #frid related parameters
    
    if variable == 'lat':
        var=TIEGCM.variables[variable][lat]
        return var
    elif variable == 'lon':
        var=TIEGCM.variables[variable][lon]
        return var
    elif variable == 'time':
        var=TIEGCM.variables[variable][timer]
        return var

    elif variable == 'BX':
        bmag=TIEGCM.variables['BMAG'][timer,lat, lon]
        var=bmag*TIEGCM.variables['BX'][timer,lat, lon]*0.0001
        return var
    elif variable == 'BY':
        bmag=TIEGCM.variables['BMAG'][timer,lat, lon]
        var=bmag*TIEGCM.variables['BY'][timer,lat, lon]*0.0001
        return var
    elif variable == 'BZ':
        bmag=TIEGCM.variables['BMAG'][timer,lat, lon]
        var=bmag*TIEGCM.variables['BZ'][timer,lat, lon]*0.0001
        return var
    else:
        var=TIEGCM.variables[variable][timer, lev, lat, lon]
    
    if variable == 'Ui_lev':
        var=var /100
    if variable == 'Vi_lev':
        var=var /100
    if variable == 'Wi_lev':
        var=var /100  
    if variable == 'UN':
        var=var /100
    if variable == 'VN':
        var=var /100
    if variable == 'WN_lev':
        var=var /100   
    if variable == 'ZGMID':
        var=var / 1e5    
    if variable == 'EEX':
        var=var*100  
    if variable == 'EEY':
        var=var*100    
    if variable == 'EEZ':
        var=var*100   
    if variable == 'DEN':
        var=var*1000
          
    TIEGCM.close() #close input file

    return var


