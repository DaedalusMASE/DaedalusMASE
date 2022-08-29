"""
environment_mod.const

**Description**:
_____________________________________________________________________________________________________________________

File with all the needed constants for the simulations
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

"""
timer = 0  # counter used for incrementing TIEGCM timestep
deltalmd = 2.5  # TIEGCM grid resolution in deg
deltaphi = 2.5  # TIEGCM grid resolution in deg
Re = 6378.1370  # Earths Radius (km)
electron = 1.602176565 * 10 ** (- 19) #electron charge in C
boltzmann_si=1.38064852 * 10**(-23)
boltzmann=1.380645852 * 10 ** (-16) #Boltzmann constant in cm^2*g*s^(-2)*K^(-1)
me=9.10938356 * 10 ** (- 31) #electron mass in kg
mO=16 # Oxygen atomic mass in g/mol
mN2=28  #N2 molecular mass in g/mol
mO2=32 #O2 molecular mass in g/mol
mNO=30 #NO molecular mass in g/mol
mN=14 #N molecular mass in g/mol
NA=6.02214086 * 10 ** 23 #Avogadro's constant in mol^-1
fcor=1.5 #Burnside facor (default=1.5)
Ar_argon=39.948
Ar_helium=4.002
Ar_NO=30
