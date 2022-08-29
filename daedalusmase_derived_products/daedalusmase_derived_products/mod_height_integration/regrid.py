import numpy as np
from netCDF4 import Dataset
import sys
from tqdm import tqdm
from daedalusmase_derived_products.mod_tiegcm_utils import read_tiegcm_whole 
import os
def regrid(minAlt,maxAlt,dz,tiegcm_file,timesteps,params,output_path):

#
    Nz=int((maxAlt-minAlt)/dz)

    def local(y,x):
        local_pos=0
        
        if y>=x[-1]:
            return int(len(x)-1)
        if y<=x[0]:
            return 0

        for i in range(0,len(x)-1):
            if y >= x[i] and y < x[i+1]:
                local_pos=i
                return (local_pos)
        
        print("No local neighbors...")

    dictOfvars = {} #Make a Dictionary fro variables

    nc=Dataset(tiegcm_file)
    ZGMID=nc.variables["ZGMID"][:]
    time=nc.variables["time"][:]
    lat=nc.variables["lat"][:]
    lon=nc.variables["lon"][:]
    lev=nc.variables["ilev"][:]
    nc.close()

    for i in range(0,len(params)):
        # print(params[i])
        x=params[i]
        dictOfvars[x]=read_tiegcm_whole(tiegcm_file,params[i])   

    nalt=len(lev)
    ntimesT=len(time)
    ntimes=len(timesteps)
    nlat=len(lat)
    nlon=len(lon)
    print("Dimensions are time x alt x loat x lon",ntimesT,nalt,nlat,nlon)
    print("Dimensions Of Regridded: time x alt x loat x lon",ntimes,Nz,nlat,nlon)
    print("Timesteps to calculate-->",timesteps)

    dictOfallocs={} #Make a Dictionary fro allocations
    
    for j in range(len(dictOfvars)):
        dictOfallocs["retval{0}".format(j)] = np.zeros((ntimesT,Nz,nlat,nlon))

    # print(list(dictOfallocs.keys())[0])


    # print(dictOfallocs["retval{0}".format(0)])
    # print('shape',np.shape(dictOfallocs["retval{0}".format(0)]))
    height_out=np.zeros((ntimes, Nz),order='F')
    for i in range(ntimes):
        for j in tqdm(range (Nz)):
            height=minAlt+j*dz
            height_out[i,j]=height
            for k in range(nlat):
                for z in range(nlon):
                    for jj in range(0,len(dictOfvars)):

                        alts=ZGMID[timesteps[i],:,k,z]/1.e5
                        lrho=local(height,alts)
                        dr=alts[lrho+1]-alts[lrho]
                        dictOfallocs["retval{0}".format(jj)][timesteps[i],j,k,z]=((height-alts[lrho])/(dr))*dictOfvars[params[jj]][timesteps[i],lrho,k,z]+(1-((height-alts[lrho])/(dr)))*dictOfvars[params[jj]][timesteps[i],lrho+1,k,z]

    # # Write out
    file_name = os.path.basename(tiegcm_file)
    ncout = Dataset(output_path+os.path.splitext(file_name)[0]+"_regrid.nc", "w", format="NETCDF4")    
    ncout.createDimension("time",ntimesT )
    ncout.createDimension("height",Nz )
    ncout.createDimension("lat",nlat )
    ncout.createDimension("lon",nlon )

    data_lat = ncout.createVariable("lat","f4",("lat"))
    data_lat[:]=lat
    data_lon = ncout.createVariable("lon","f4",("lon"))
    data_lon[:]=lon
    data_heigh = ncout.createVariable("height","f4",("time","height"))
    data_heigh[:]=height_out
    data_time = ncout.createVariable("time","f4",("time"))
    data_time[:]=time

    for jj in range(len(dictOfvars)):
        data = ncout.createVariable(params[jj],"f4",("time","height","lat","lon"))
        data[:]=dictOfallocs["retval{0}".format(jj)]  
    ncout.close()