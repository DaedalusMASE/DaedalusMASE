# Error Propagation of TIEGCM
## Introduction
Error Propagtion calculates products of Daedalus Science Study, using TIEGCM outputs as in-situ measuremenents estimation.
Values of products, errors and error contribution are calculated using proper functions located in productDerivation.py and ErrorPropagation.py and stores in proper arrays created in factors.py

## Usage
A sample usage of the software is demonstrated in python code below:
```
import productDerivation as pD
import Plots
import ErrorProgation as EP
filename="tiegcm2.0_res2.5_3years_sech_016.nc"
timer=5
lat_value=0 #63.75 deg
lon_value=49 #-57.5 deg
# Load variables needed from TIEGCM file
pD.models_input(filename, timer, lat_value, lon_value)
# Calculate Products
pD.products(lat_value, lon_value)

min_alt=100
max_alt=400
# Plot of conductivities
Plots.plot_conductivities(lat_value, lon_value, min_alt, max_alt)
error_flag=True
# Error calculation
EP.error(error_flag=error_flag, lat_value=lat_value, lon_value=lon_value)
Plots error of conductivities
Plots.plot_conductivities_error(lat_value, lon_value, min_alt, max_alt)

```

## Data

## TIEGCM
The Thermosphere is described in several TIEGCM files of netCDF type, stored in a user-specified folder.
This code uses the variables stored in the source files produced by TIEGCM and calculates the derived products according to Daedalus Science Study and the correspoding error propagation and error contribution of each variable.
Sample TIEGCM data file can be provided upon request (because of the size), or can be produced running TIEGCM according to it's manual.

## Results
Results Stored in preceated, in factor.py, arrays. These arrays can be used to export results in the desired data file format.

## Algorith Description
- User selects the input file (output of TIEGCM)
- Calls models_input and products function to load and calculate the LTI (Lower Atmosphere-Ionoshpere) products, located in productDerivation.py. user should call these functions according to the calculation wants to implement. Lat-Lon profile, Height Profile or Lat-Alt profile. Depending on values of lat_value, lon_value and pressure_level, code distinguish between the different options. These values are intergers according to TIEGCM files' indices.
- Calls error function using same arguments as previous
- Calls the desired Plot function depending on what wants to plot.
