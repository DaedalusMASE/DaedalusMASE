import numpy as np
import SupportFuctions as SF
import IO as IO
from tqdm import tqdm

def TrilinearInterpolation(gtime,glat,glon,dtime,dlat,dlon,dalt,zg,ne):
    """
    This function performs Trilinear interpolation of a given orbit in TIEGCM grid
    Args: 
        gtime(array): array of times of TIEGCM
        glat(array): array of latitudes of TIEGCM
        glon(array): array of longitudes of TIEGCM
        dtime(array): time of interpolation orbit
        dlat(array): latitude of interpolation orbit
        dlon(array): longitude of interpolation orbit
        dalt(array): altitude of interpolation orbit
        zg(4D array): altitude of TIEGCM midpoint levels
        ne(4D array): variable values on gridded point of TIEGCM grid
    Returns:
        m(1D array): Trilinear Interpolation Results
    """
    deltaphi= np.abs(glon[2]-glon[1])
    deltatheta=np.abs(glat[2]-glat[1])
    Re=6378137.0/1e3
    # arc_theta=2*np.pi*Re*(deltatheta/360)
    # arc_phi=2*np.pi*Re*(deltaphi/360)

    m=np.zeros((len(dalt)))
    

    for i in range(0,len(dalt)):
        counter=SF.local(dtime[i],gtime)
        phi_local=SF.local(dlon[i],glon)
        theta_local=SF.local(dlat[i],glat)


        if dlon[i] >= 177.5 :
            phi_local=len(glon)-2
            lonbnd=1

        if dlon[i] <= -177.5:
            phi_local=1

        if dlat[i] >= 87.5:
            theta_local=len(glat)-2
            latbnd=1

        if dlat[i] <= -87.5:
            theta_local=0


        alts=zg[counter,:,theta_local,phi_local]/1e5
        r_local=SF.local(dalt[i],alts)
        deltarho=alts[r_local+1]-alts[r_local]
        dx=(((dalt[i]-alts[r_local])/deltarho))
        dy=(((dlat[i]-glat[theta_local])/deltatheta))
        dz=np.abs(((dlon[i]-glon[phi_local])/deltaphi))

        # Calculate Weights
                
        w1=np.abs((1-dx)*(1-dy)*(1-dz))
        w2=np.abs((dx)*(1-dy)*(1-dz))
        w3=np.abs((1-dx)*(dy)*(1-dz))
        w4=np.abs((dx)*(dy)*(1-dz))
        w5=np.abs((1-dx)*(1-dy)*(dz))
        w6=np.abs((dx)*(1-dy)*(dz))
        w7=np.abs((1-dx)*(dy)*(dz))
        w8=np.abs((dx)*(dy)*(dz))

        
        m[i]=0.0
        m[i]=       ne[counter,r_local,theta_local,phi_local]*w1
        m[i]=m[i]+  ne[counter,r_local+1,theta_local,phi_local]*w2
        m[i]=m[i]+  ne[counter,r_local,theta_local+1,phi_local]*w3
        m[i]=m[i]+  ne[counter,r_local+1,theta_local+1,phi_local]*w4

        m[i]=m[i]+  ne[counter,r_local,theta_local,phi_local+1]*w5
        m[i]=m[i]+  ne[counter,r_local+1,theta_local,phi_local+1]*w6
        m[i]=m[i]+  ne[counter,r_local,theta_local+1,phi_local+1]*w7
        m[i]=m[i]+  ne[counter,r_local+1,theta_local+1,phi_local+1]*w8

    return m

def TriCubicSplineInterpolation(gtime,glat,glon,dtime,dlat,dlon,dalt,zg,ne):
    """
    This function performs Tricubic interpolation of a given orbit in TIEGCM grid
    Args: 
        gtime(array): array of times of TIEGCM
        glat(array): array of latitudes of TIEGCM
        glon(array): array of longitudes of TIEGCM
        dtime(array): time of interpolation orbit
        dlat(array): latitude of interpolation orbit
        dlon(array): longitude of interpolation orbit
        dalt(array): altitude of interpolation orbit
        zg(4D array): altitude of TIEGCM midpoint levels
        ne(4D array): variable values on gridded point of TIEGCM grid
    Returns:
        m(1D array): Trilinear Interpolation Results
    """
    deltaphi= np.abs(glon[2]-glon[1])
    deltatheta=np.abs(glat[2]-glat[1])
    Re=6378137.0/1e3
    # arc_theta=2*np.pi*Re*(deltatheta/360)
    # arc_phi=2*np.pi*Re*(deltaphi/360)

    m=np.zeros((len(dalt)))
    fval=np.zeros(8)
    fdx=np.zeros(8)
    fdy=np.zeros(8)
    fdz=np.zeros(8)
    fdxdy=np.zeros(8)
    fdxdz=np.zeros(8)
    fdydz=np.zeros(8)
    fdxdydz=np.zeros(8)
    x=np.zeros(64)

    for i in range(0,len(dalt)):
        counter=SF.local(dtime[i],gtime)
        phi_local=SF.local(dlon[i],glon)
        theta_local=SF.local(dlat[i],glat)

        if dlon[i] >= 177.5 :
            phi_local=len(glon)-2
            lonbnd=1

        if dlon[i] <= -177.5:
            phi_local=1

        if dlat[i] >= 87.5:
            theta_local=len(glat)-2
            latbnd=1

        if dlat[i] <= -87.5:
            theta_local=0



        alts=zg[counter,:,theta_local,phi_local]/1e5
        r_local=SF.local(dalt[i],alts)
        deltarho=alts[r_local+1]-alts[r_local]
        dx=(((dalt[i]-alts[r_local])/deltarho))
        dy=np.abs((((dlat[i]-glat[theta_local])/deltatheta)))
        dz=np.abs(((dlon[i]-glon[phi_local])/deltaphi))
        


        # Get 8 Nearest Neighbors Values
        fval[0]=ne[counter,r_local,theta_local,phi_local]
        fval[1]=ne[counter,r_local+1,theta_local,phi_local]
        fval[2]=ne[counter,r_local,theta_local+1,phi_local]
        fval[3]=ne[counter,r_local+1,theta_local+1,phi_local]
        fval[4]=ne[counter,r_local,theta_local,phi_local+1]
        fval[5]=ne[counter,r_local+1,theta_local,phi_local+1]
        fval[6]=ne[counter,r_local,theta_local+1,phi_local+1]
        fval[7]=ne[counter,r_local+1,theta_local+1,phi_local+1]
        
        # Get 1st Order Derivatives Nearest Neighbors Values
        fdx[0]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local,phi_local,"X")  
        fdx[1]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local,phi_local,"X")  
        fdx[2]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local+1,phi_local,"X")  
        fdx[3]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local+1,phi_local,"X")  
        fdx[4]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local,phi_local+1,"X")  
        fdx[5]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local,phi_local+1,"X")  
        fdx[6]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local+1,phi_local+1,"X")  
        fdx[7]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local+1,phi_local+1,"X")  

        fdy[0]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local,phi_local,"Y")  
        fdy[1]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local,phi_local,"Y")  
        fdy[2]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local+1,phi_local,"Y")  
        fdy[3]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local+1,phi_local,"Y")  
        fdy[4]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local,phi_local+1,"Y")  
        fdy[5]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local,phi_local+1,"Y")  
        fdy[6]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local+1,phi_local+1,"Y")  
        fdy[7]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local+1,phi_local+1,"Y")  

        fdz[0]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local,phi_local,"Z")  
        fdz[1]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local,phi_local,"Z")  
        fdz[2]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local+1,phi_local,"Z")  
        fdz[3]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local+1,phi_local,"Z")  
        fdz[4]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local,phi_local+1,"Z")  
        fdz[5]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local,phi_local+1,"Z")  
        fdz[6]=SF.FirstOrderDerivative(ne,counter,r_local,theta_local+1,phi_local+1,"Z")  
        fdz[7]=SF.FirstOrderDerivative(ne,counter,r_local+1,theta_local+1,phi_local+1,"Z")  


     
        # Get 2nd Order Mixed Derivatives Nearest Neighbors Values
        fdxdy[0]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local,phi_local,"XY")  
        fdxdy[1]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local,phi_local,"XY")  
        fdxdy[2]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local+1,phi_local,"XY")  
        fdxdy[3]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local+1,phi_local,"XY")  
        fdxdy[4]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local,phi_local+1,"XY")  
        fdxdy[5]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local,phi_local+1,"XY")  
        fdxdy[6]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local+1,phi_local+1,"XY")  
        fdxdy[7]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local+1,phi_local+1,"XY")  

        
        fdxdz[0]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local,phi_local,"XZ")  
        fdxdz[1]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local,phi_local,"XZ")  
        fdxdz[2]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local+1,phi_local,"XZ")  
        fdxdz[3]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local+1,phi_local,"XZ")  
        fdxdz[4]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local,phi_local+1,"XZ")  
        fdxdz[5]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local,phi_local+1,"XZ")  
        fdxdz[6]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local+1,phi_local+1,"XZ")  
        fdxdz[7]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local+1,phi_local+1,"XZ")  
        
        fdydz[0]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local,phi_local,"YZ")  
        fdydz[1]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local,phi_local,"YZ")  
        fdydz[2]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local+1,phi_local,"YZ")  
        fdydz[3]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local+1,phi_local,"YZ")  
        fdydz[4]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local,phi_local+1,"YZ")  
        fdydz[5]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local,phi_local+1,"YZ")  
        fdydz[6]=SF.SecondOrderMixedDerivative(ne,counter,r_local,theta_local+1,phi_local+1,"YZ")  
        fdydz[7]=SF.SecondOrderMixedDerivative(ne,counter,r_local+1,theta_local+1,phi_local+1,"YZ")  

        
        # Get 3rd Order Mixed Derivatives Nearest Neighbors Values

        fdxdydz[0]=SF.ThirdOrderMixedDerivative(ne,counter,r_local,theta_local,phi_local)  
        fdxdydz[1]=SF.ThirdOrderMixedDerivative(ne,counter,r_local+1,theta_local,phi_local)  
        fdxdydz[2]=SF.ThirdOrderMixedDerivative(ne,counter,r_local,theta_local+1,phi_local)  
        fdxdydz[3]=SF.ThirdOrderMixedDerivative(ne,counter,r_local+1,theta_local+1,phi_local)  
        fdxdydz[4]=SF.ThirdOrderMixedDerivative(ne,counter,r_local,theta_local,phi_local+1)  
        fdxdydz[5]=SF.ThirdOrderMixedDerivative(ne,counter,r_local+1,theta_local,phi_local+1)  
        fdxdydz[6]=SF.ThirdOrderMixedDerivative(ne,counter,r_local,theta_local+1,phi_local+1)  
        fdxdydz[7]=SF.ThirdOrderMixedDerivative(ne,counter,r_local+1,theta_local+1,phi_local+1)  


        for ii in range(8):
            x[0+ii]=fval[ii]
            x[8+ii]=fdx[ii]
            x[16+ii]=fdy[ii]
            x[24+ii]=fdz[ii]
            x[32+ii]=fdxdy[ii]
            x[40+ii]=fdxdz[ii]
            x[48+ii]=fdydz[ii]
            x[56+ii]=fdxdydz[ii]


        a =np.zeros(64)
        for ii in range(64):
            a[ii]=0.0
            for j in range(64):
                a[ii]+=SF.A[ii,j]*x[j]

        m[i]=0.0

        for ii in range(4):
            for j in range(4):
                for k in range(4):
                    m[i]+=a[ii+4*j+16*k]*pow(dx,ii)*pow(dy,j)*pow(dz,k)

        
    min=np.zeros((len(dtime)))
    for i in range(0,len(dtime)):
        min[i] = (dtime[i] - SF.startTime)/1000/60
        

    return m

def IDWInterpolation(gtime,glat,glon,dtime,dlat,dlon,dalt,zg,ne):
    """
    This function performs Inverse Distanse Weight interpolation of a given orbit in TIEGCM grid, using 8 closest gridded points
    Args: 
        gtime(array): array of times of TIEGCM
        glat(array): array of latitudes of TIEGCM
        glon(array): array of longitudes of TIEGCM
        dtime(array): time of interpolation orbit
        dlat(array): latitude of interpolation orbit
        dlon(array): longitude of interpolation orbit
        dalt(array): altitude of interpolation orbit
        zg(4D array): altitude of TIEGCM midpoint levels
        ne(4D array): variable values on gridded point of TIEGCM grid
    Returns:
        m(1D array): Inverse Distanse Weight Interpolation Results
    """
   
    m=np.zeros((len(dalt)))
    p=2 #IDW parameter
    for i in range(0,len(dalt)):
        counter=SF.local(dtime[i],gtime)
        phi_local=SF.local(dlon[i],glon)
        theta_local=SF.local(dlat[i],glat)
        alts=zg[counter,:,theta_local,phi_local]/1e5
        r_local=SF.local(dalt[i],alts)


        if dlon[i] >= 177.5 :
            phi_local=len(glon)-2
            lonbnd=1

        if dlon[i] <= -177.5:
            phi_local=1

        if dlat[i] >= 87.5:
            theta_local=len(glat)-2
            latbnd=1

        if dlat[i] <= -87.5:
            theta_local=0

        p_0=[dlat[i],dlon[i],dalt[i]]

        p_1=[glat[theta_local],glon[phi_local],alts[r_local]]
        p_2=[glat[theta_local],glon[phi_local],alts[r_local+1]]
        p_3=[glat[theta_local+1],glon[phi_local],alts[r_local]]
        p_4=[glat[theta_local+1],glon[phi_local],alts[r_local+1]]
        p_5=[glat[theta_local],glon[phi_local+1],alts[r_local]]
        p_6=[glat[theta_local],glon[phi_local+1],alts[r_local+1]]
        p_7=[glat[theta_local+1],glon[phi_local+1],alts[r_local]]
        p_8=[glat[theta_local+1],glon[phi_local+1],alts[r_local+1]]

        d_01=SF.euclidianDistance(p_0,p_1)
        d_02=SF.euclidianDistance(p_0,p_2)
        d_03=SF.euclidianDistance(p_0,p_3)
        d_04=SF.euclidianDistance(p_0,p_4)
        d_05=SF.euclidianDistance(p_0,p_5)
        d_06=SF.euclidianDistance(p_0,p_6)
        d_07=SF.euclidianDistance(p_0,p_7)
        d_08=SF.euclidianDistance(p_0,p_8)

        if d_01==0: m[i]=ne[counter,r_local,theta_local,phi_local] 
        if d_02==0: m[i]=ne[counter,r_local+1,theta_local,phi_local] 
        if d_03==0: m[i]=ne[counter,r_local,theta_local+1,phi_local] 
        if d_03==0: m[i]=ne[counter,r_local+1,theta_local+1,phi_local] 
        if d_04==0: m[i]=ne[counter,r_local,theta_local,phi_local+1] 
        if d_05==0: m[i]=ne[counter,r_local+1,theta_local,phi_local+1] 
        if d_06==0: m[i]=ne[counter,r_local,theta_local+1,phi_local+1] 
        if d_07==0: m[i]=ne[counter,r_local+1,theta_local+1,phi_local+1] 

        p_1_weight=1/d_01**p
        p_2_weight=1/d_02**p
        p_3_weight=1/d_03**p
        p_4_weight=1/d_04**p
        p_5_weight=1/d_05**p
        p_6_weight=1/d_06**p
        p_7_weight=1/d_07**p
        p_8_weight=1/d_08**p
        
        WeightsSum = p_1_weight+p_2_weight+p_3_weight+p_4_weight+p_5_weight+p_6_weight+p_7_weight+p_8_weight
        WeightsMultSum = p_1_weight*ne[counter,r_local,theta_local,phi_local]+p_2_weight*ne[counter,r_local+1,theta_local,phi_local]+\
                        p_3_weight*ne[counter,r_local,theta_local+1,phi_local]+p_4_weight*ne[counter,r_local+1,theta_local+1,phi_local]+\
                        p_5_weight*ne[counter,r_local,theta_local,phi_local+1]+p_6_weight*ne[counter,r_local+1,theta_local,phi_local+1]+\
                        p_7_weight*ne[counter,r_local,theta_local+1,phi_local+1]+p_8_weight*ne[counter,r_local+1,theta_local+1,phi_local+1]

        m[i] = WeightsMultSum / WeightsSum

    return m



def RunInterpolator(model_data_file,orbit_file,TGvar="TN",Interpolation="Trilinear",Save=True,outfileName="InterResults.nc"):
    """
    This function begins the execution of the selected interpolation scheme
    Args: 
        model_data_file(String): name of TIEGCM input file, netCDF4 file
        orbit_file (String): name of orbit file, netCDF4 file
        TGvar(String): Variables for interpolation, select between 'XNMBAR','TI','TN',s'OP','DEN','HALL','HE','PEDERSEN','POTEN','TE',
                        'O2_CM3', 'EEX', 'EEY', 'EEZ', 'ELECDEN', 'N2_CM3', 'NOP_LAM', 'NPLUS', '02P', 'O_CM3'
                        'UN', 'VN', 'WN_lev', 'HALL', 'N2D', 'N4S', 'NO', 'Ui_lev', 'Vi_lev', 'WI_LEV'
                        in case that "All" is selected then intepolation implemented on all of the above variables
                        default selection is "TN"
        Interpolation(String): Select between "Trilinear", "Tricubic" and "IDW"
        Save(bool): Enables the saving of orbit parameters in the ouput file the results
        outfileName (String): The name of the output file, default name is "InterResults.nc"
    """
    model=IO.Model(model_data_file ,500,100)  #initialize model
    orbit=IO.Orbit(orbit_file)                #initialize  orbit
    outfile=outfileName
    dtime,dlat,dlon,dalt,index,int_final=orbit.createorbit(orbit.name,model.minAltitude,model.maxAltitude,outfile,Save)
    gtime,glat,glon,glev,zg=model.readGrid(model.name)                                     #get model stats
    if TGvar=='All':
        TGvar=['XNMBAR','TI','TN','OP','DEN','HALL','HE','PEDERSEN','POTEN','TE',
                'O2_CM3', 'EEX', 'EEY', 'EEZ', 'ELECDEN', 'N2_CM3', 'NOP_LAM', 'NPLUS', '02P', 'O_CM3'
                'UN', 'VN', 'WN_lev', 'HALL', 'N2D', 'N4S', 'NO', 'Ui_lev', 'Vi_lev', 'WI_LEV']  
    #select variable
    if Interpolation=="Trilinear":
        for jj in tqdm(range(len(TGvar))):
            var=model.readVar(model.name,TGvar[jj])
            interpolatedDataTrilinear=TrilinearInterpolation(glat,glon,glev,dtime, dlat,dlon,dalt,zg,var)
            interpolatedData=orbit.mergeData(index,int_final,interpolatedDataTrilinear)

            if Save == True: 
                IO.Write(outfile,interpolatedData,TGvar[jj])
                
    if Interpolation=="Tricubic":
        for jj in tqdm(range(len(TGvar))):
            var=model.readVar(model.name,TGvar[jj])

            interpolatedDataTricubic=TriCubicSplineInterpolation(gtime,glat,glon,glev,dtime, dlat,dlon,dalt,zg,var)
            interpolatedData=orbit.mergeData(index,int_final,interpolatedDataTricubic)
            
            if Save == True: 
                IO.Write(outfile,interpolatedData,TGvar[jj])

    if Interpolation=="IDW":
        for jj in tqdm(range(len(TGvar))):
            var=model.readVar(model.name,TGvar[jj])

            interpolatedDataTricubic=IDWInterpolation(gtime,glat,glon,glev,dtime, dlat,dlon,dalt,zg,var)
            interpolatedData=orbit.mergeData(index,int_final,interpolatedDataTricubic)
            
            if Save == True: 
                IO.Write(outfile,interpolatedData,TGvar[jj])
