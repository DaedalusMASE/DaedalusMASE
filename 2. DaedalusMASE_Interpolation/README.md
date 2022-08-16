# InterpolationMASE
## Introduction
InterpolationMASE estimates the products along given orbit of satellite or orbit
Values of simulated measuremets, are estimated using classes and functionslocated in IO.py, SupportFunctions and InterpolationMASE_MainFunc.py and stores the results in a netCDF4 output file

## Usage
A sample usage of the software is demonstrated in python code below:
```
import InterpolationMASE_MainFunc as INT
ModelName="tiegcm2.0_res2.5_3years_sech_016.nc"
OrbitFile="orbit.nc"
INT.RunInterpolator(ModelName,OrbitFile,TGvar="TN",Interpolation="Trilinear",Save=True,outfileName="InterResults.nc")

```

## Data

## TIEGCM
The Thermosphere is described in several TIEGCM files of netCDF type, stored in a user-specified folder.
This code uses the variables stored in the source files produced by TIEGCM and calculates the derived products according to Daedalus Science Study and the correspoding error propagation and error contribution of each variable.
Sample TIEGCM data file can be provided upon request (because of the size), or can be produced running TIEGCM according to it's manual.

## Results
Results Stored in a netCDF4 output file

## Algorith Description
- User gives the input file (output of TIEGCM) and the orbit file
- User Selects the desired Interpolation method between Trilinear, Tricubic and IDW
- Runs the interpolator calling RunInterpolator function
