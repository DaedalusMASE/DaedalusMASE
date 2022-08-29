"""
tiegcm_utils.read_tiegcm

**Description**:
_____________________________________________________________________________________________________________________

Read tiegcm input file
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

"""

from netCDF4 import Dataset

def read_tiegcm_whole(tiegcm_file,variable):

    TIEGCM = Dataset(tiegcm_file)

    var=TIEGCM.variables[variable][:]
          
    TIEGCM.close() #close input file

    return var


