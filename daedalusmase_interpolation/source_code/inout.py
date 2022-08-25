from netCDF4 import Dataset
import matplotlib.pyplot as plt
# %matplotlib inline  
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import warnings
import supportfuctions as SF
warnings.filterwarnings('ignore')


class model:

    """
    Model class handles basic IO of the Model Data extracting grid quintities and variables as selected by the user to be used in the interpolation.
      
    """
    def __init__(self,name, maxAltitude, minAltitude):
        """
            Model class load the TIEGCM file and the corresponding variable for interpolation 
            Args:
                name (String): the name of TIEGCM input file
                maxAltitude (float): maximum efficent altitude of model
                minAltitude (float): minimum efficent altitude of model
            
            
        """
        self.name=name
        self.maxAltitude=maxAltitude
        self.minAltitude=minAltitude
        self.dt=0.0


    def readgrid(self,name):
        """
            readgrid is model class function used to read TIEGCM grid
            Args:
                name (String): the name of TIEGCM input file
            Returns:
                glat (float): geodetic latitude as numpy array
                glon (float): geodetic longitute as numpy array
                glev (float): pressure level as numpy array
                gtime (float): time as numpy as numpy array
                zg (float): altitude of midpoint levels in km as numpy array
        """

        TIEGCM=Dataset(name)
        glat=TIEGCM.variables['lat'][:]
        glon=TIEGCM.variables['lon'][:]
        glev=TIEGCM.variables['lev'][:]
        gtime=TIEGCM.variables['time'][:] 
        zg=TIEGCM.variables['ZGMID'][:]
        TIEGCM.close()
        self.dt= gtime[2]- gtime[1]
        gtime=np.asarray(gtime)
        glat=np.asarray(glat)
        glon=np.asarray(glon)
        glev=np.asarray(glev)
        zg=np.asarray(zg)
        return gtime,glat,glon,glev,zg

    
    def readvar(self,modelname,name):
        """
            readvar is model class function used to read variable for interpolation of TIEGCM input file
            Args:
                modelname (Model): the created model
                name (String): the name of TIEGCM input file
            Returns:
                var (String): Variable for interpolation
        """
        TIEGCM=Dataset(modelname)
        var=TIEGCM.variables[name][:]
        TIEGCM.close()
        return var



class orbit:
    """
        orbit class handles basic IO of Daedalus' orbit allocating arrays for the spatial components. The longitudinal component is matched to TIEGCM's and points in a specific altitudinal range are extracted to be passed to the interpolation routine. There is also an option for creating a Rocket orbit for getting vertical profiles of the said model.

    """
    
    def __init__(self,name):
        """
            Orbit class loads the orbit file and the corresponding variables
            Args:
                name (String): the name of orbit input file
        """
        self.name=name
        self.dt=1/16

   

    def createorbit(self,filename,minalt,maxalt,outfile,save=True):
        """
            Orbit class function reads the orbit definition variables
            Args:
                name (String): the name of orbit input file
                minAlt (float): the minimum altitude for interpolation
                maxAlt (float): the maximum altitude for interpolation
                outfile (String): filename to save the Interpolation results
                save (bool): index to append orbit variables to interpolation results
        """
        orbit=Dataset(filename,"r")
        daed_lat_temp = orbit.variables['lat'][:]
        daed_lon_temp = orbit.variables['lon'][:]
        daed_alt_temp = orbit.variables['altitude'][:]
        daed_time_temp = orbit.variables['time'][:] #unix time
        
        SF.startTime = daed_time_temp[0]
        

#         self.dt=daed_time_temp[2]-daed_time_temp[1]
        self.save=save
        
        if self.save==True:
            self.openfile(outfile,daed_time_temp,daed_lat_temp,daed_lon_temp,daed_alt_temp)
        
        stop=False
        counter=0
        for i in range(0,len(daed_alt_temp)):
            if (daed_alt_temp[i] < maxalt and daed_alt_temp[i] > minalt):
                counter=counter+1

        
        
        daed_lat=np.zeros((counter))
        daed_lon=np.zeros((counter))
        daed_alt=np.zeros((counter))
        daed_time=np.zeros((counter),dtype=datetime)
        index=[None]*counter
        int_final=[None]*len(daed_alt_temp)
  
        counter2=0
        
        for i in range(0,len(daed_alt_temp)):
    
            if (daed_alt_temp[i] < maxalt and daed_alt_temp[i] > minalt):
         
                daed_time[counter2]=daed_time_temp[i]
                daed_lat[counter2]=daed_lat_temp[i]
                if max(daed_lon_temp)>180:
                    daed_lon[counter2]=daed_lon_temp[i]-180 #match TIEGCM grid
                else:
                    daed_lon[counter2]=daed_lon_temp[i]
                daed_alt[counter2]=daed_alt_temp[i]
                
                index[counter2]=i          #keep indices for merging data
                counter2=counter2+1
        

        return(daed_time,daed_lat,daed_lon,daed_alt,index,int_final)

    # def rockeorbit(self,lat,lon,alt,nop,dz):
    #     Rlat=np.zeros(nop)
    #     Rlon=np.zeros(nop)
    #     Ralt=np.zeros(nop)

    #     Rlat[:]=lat
    #     Rlon[:]=lon
    #     Ralt[0]=alt
    #     for i in range(1,nop):
    #         Ralt[i]=Ralt[i-1]+dz

    #     return Rlat,Rlon,Ralt

    # def mergedata(self,index,int_final,m):
    #     for i in range(0,len(m)):
    #         int_final[index[i]]=m[i]

    #     return int_final    



    def openfile(self,outfile,time,lat,lon,alt):
        """
            Function to save orbit parameters to netCDF output file
            Args:
                time (String): list of timesteps of orbit
                lat (float): list of latitudes of orbit
                lon (float): list of longitudes of orbit
                alt (float): list of altitudes of orbit                
        """
        print("Output File Path:",outfile)
        ncout = Dataset(outfile, "w", format="NETCDF4")    
        ncout.createDimension("time", len(time))
        xaxis=np.arange(0,len(time)) #time axis based on Daedalus Sampling rate
        data = ncout.createVariable("time","f4","time")
        data[:]=xaxis
        ncout.createDimension("lat",len(lat))
        data = ncout.createVariable("lat","f4","lat")
        data[:]=lat
        ncout.createDimension("lon",len(lon))
        data = ncout.createVariable("lon","f4","lon")
        data[:]=lon
        ncout.createDimension("altitude",len(alt))
        data = ncout.createVariable("altitude","f4","time")
        data[:]=alt
        ncout.close()   
        return True


def write(outfile,m,varname):
    """
        Function to save interpolation results to netCDF output file
        Args:
            outfile (String): name of output file
            m (float): 1D array of interpolation results
            varname (String): name of interpolated variable
    """

    ncout = Dataset(outfile, "a", format="NETCDF4")
    data = ncout.createVariable(varname,"f4",('time'))
    data[:]=m
    ncout.close()