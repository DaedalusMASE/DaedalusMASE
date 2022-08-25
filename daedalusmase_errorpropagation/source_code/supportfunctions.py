import numpy as np
def enu_ecef(lat_phi, lon_lmd, Fe, Fn, Fup):
    fac = np.pi / 180
    lat_phi = lat_phi * fac
    lon_lmd = lon_lmd * fac

    north_temp_unit = [-np.cos(lon_lmd) * np.sin(lat_phi), - np.sin(lon_lmd) * np.sin(lat_phi), np.cos(lat_phi)]
    east_temp_unit = [-np.sin(lon_lmd), np.cos(lon_lmd), 0]
    up_temp_unit = [np.cos(lon_lmd) * np.cos(lat_phi), np.sin(lon_lmd) * np.cos(lat_phi), np.sin(lat_phi)]

    Fnorth_vector = [Fn * north_temp_unit[0], Fn * north_temp_unit[1], Fn * north_temp_unit[2]]
    Feast_vector = [Fe * east_temp_unit[0], Fe * east_temp_unit[1], Fe * east_temp_unit[2]]
    Fup_vector = [Fup * up_temp_unit[0], Fup * up_temp_unit[1], Fup * up_temp_unit[2]]

    Fx = Fnorth_vector[0] + Feast_vector[0] + Fup_vector[0]
    Fy = Fnorth_vector[1] + Feast_vector[1] + Fup_vector[1]
    Fz = Fnorth_vector[2] + Feast_vector[2] + Fup_vector[2]

    return Fx, Fy, Fz

# ##