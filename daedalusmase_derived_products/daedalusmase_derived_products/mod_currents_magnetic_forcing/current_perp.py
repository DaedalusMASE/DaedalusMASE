"""
**sub_Heating_Sources.current_perp**

**Description**:

$$j_\\perp=e\\Big( N_{O^+} \\vec{v}_{O^+} + N_{O2^+} \\vec{v}_{O_2^+} +  N_{NO^+} \\vec{v}_{NO^+} - N_e \\vec{v}_e  \\Big) \\approx e N_e \\Big( \\vec{v}_i - \\vec{v}_e \\Big) $$
_____________________________________________________________________________________________________________________

Calculate Perpendicular current density
_____________________________________________________________________________________________________________________
_____________________________________________________________________________________________________________________

**Inputs**:
_____________________________________________________________________________________________________________________

`sigmaPed`: Pedersen conductivity in S/m

`sigmaHall`: Hall conductivity in S/m

`Un`: neutral velocity in m/s [ENU]

`B`: magnetic field vector in T [ENU]

`E`: electric field vector in V/m [ENU]

_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

**Outputs**:
_____________________________________________________________________________________________________________________

`J_perp`: perpendicular current density vector in \(A/m^2\)

`J_perpe`: perpendicular current density in \(A/m^2\) [east]

`J_perpn`: perpendicular current density in \(A/m^2\) [north]

`J_perpu`: perpendicular current density in \(A/m^2\) [up]
_____________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

**Reference**:
_____________________________________________________________________________________________________________________

Richmond, A. and Thayer, J. (2000). Ionospheric electrodynamics: A tutorial. Magnetospheric current
systems 118, 131–146
______________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

"""


import numpy as np

def current_perp(sigmaPed,sigmaHall,Un,B,E):

    bnorm = np.sqrt(B[0] * B[0] + B[1] * B[1] + B[2] * B[2])
    b_unit = [B[0] / bnorm, B[1]/ bnorm, B[2] / bnorm]

    Unvert=np.cross(Un,b_unit)

    Estar=E+np.cross(Unvert,B)

    J_perp=sigmaPed*Estar+sigmaHall*np.cross(b_unit,Estar)
    J_perpe=J_perp[0]
    J_perpn=J_perp[1]
    J_perpu=J_perp[2]

    return J_perp,J_perpe,J_perpn,J_perpu
