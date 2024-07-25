#!/usr/bin/env python

"""
This function computes the RMSE of the shoreline position, based on the
ShoreFor model of Splinter et al. (2014b).

Inputs:
    - a forcing file with wave heights and periods
    - a data file with shoreline position
    - a parameters file with initial values of b, c, and phi

Output:
    - rmse.txt with the value of the RMSE

Author: Alexandre Paris
"""

import sys
import datetime
import yaml
import numpy as np
import pandas

sys.path.append('../libs')
from dates_functions import _from_ordinal, datenum
from tools import match, rmse, nmse, bss
from constants import GAMMA, G, RHO, DEIL, NU, D50
from read_files import reading_files
from dean import dean
from shorecore import shorecore


def bss_shoreline(coef_b, coef_c, dt_time_survey):
    """
    Calculates the shoreline variation and the associated 1/BSS.
    Negative BSS are set to 1 and so 1/BSS=1 is the worse value Dakota
    could select during the optimization.

    This function can be minimized to obtain the values of coefficients b and c

    WARNING : b_opti, c_opti and dt_time_survey excepted, all the variables
    are defined in the code and are not arguments of the function
    """
    for line, delta_t in enumerate(dt_time_survey):
        delta_s[line] = (coef_c*(erosion_ratio*mff_mi[line]
                         + mff_pl[line])) + coef_b * delta_t
        shoreline_calib[line+1] = shoreline_calib[line] + delta_s[line]

    return bss(XS, shoreline_calib, coef_b)


def rmse_shoreline(coef_b, coef_c, dt_time_survey):
    """
    Calculates the shoreline variation and the associated RMSE

    This function can be minimized to obtain the values of coefficients b and c

    WARNING : b_opti, c_opti and dt_time_survey excepted, all the variables
    are defined in the code and are not arguments of the function
    """
    for line, delta_t in enumerate(dt_time_survey):
        delta_s[line] = (coef_c*(erosion_ratio*FF_mi[line]
                         + FF_pl[line])) + coef_b * delta_t
        shoreline_calib[line+1] = shoreline_calib[line] + delta_s[line]
    
    return rmse(XS, shoreline_calib)


def nmse_shoreline(coef_b, coef_c, dt_time_survey):
    """
    Calculates the shoreline variation and the associated NMSE

    This function can be minimized to obtain the values of coefficients b and c

    WARNING : b_opti, c_opti and dt_time_survey excepted, all the variables
    are defined in the code and are not arguments of the function
    """
    for line, delta_t in enumerate(dt_time_survey):
        delta_s[line] = (coef_c*(erosion_ratio*mff_mi[line]
                         + mff_pl[line])) + coef_b * delta_t
        shoreline_calib[line+1] = shoreline_calib[line] + delta_s[line]

    return nmse(XS, shoreline_calib)


def open_files():
    with open(r'../config_shorefor.yaml') as file:
        cl = yaml.full_load(file)

    shoreline_file = '.' + cl['input_files']['shoreline_file']
    forcing_file = '.' + cl['input_files']['waves_file']
    time_initial = datenum(cl['calibration']['time_initial'])
    time_final = datenum(cl['calibration']['time_final'])
    evol = cl['case']['evolution']
    if evol == 1:
        evolution = 'shoreline'
    elif evol == 2:
        evolution = 'bars'
    return shoreline_file, forcing_file, time_initial, time_final, evolution 


###############################################################################
# Reading .dat files with forcing and shoreline data
shoreline_file, forcing_file, time_initial, time_final, evolution = open_files()
# Reading the parameters for the optimization
inputs = np.loadtxt('parameters.txt')
b_opti = inputs[2, 0]
c_opti = inputs[2, 1]
phi_opti = inputs[2, 2]

print(b_opti, c_opti, phi_opti)

(time_S, time_Sy, loc_init, loc_extra,
 time_F, dt, ii0, iif, vecind, same,
 XS, frag, hsf, tpf, power, fall_velocity) = reading_files(forcing_file,
                                                           shoreline_file,
                                                           time_initial,
                                                           time_final)

erosion_ratio, FF_mi, FF_pl, omega_F, omega_eq = dean(hsf, tpf, fall_velocity,
                                                      dt, power, same,
                                                      phi_opti, time_F)

shoreline_calib, time_Fy_c, vec_ind_c = shorecore(b_opti,
                                                  c_opti,
                                                  erosion_ratio,
                                                  FF_mi,
                                                  FF_pl,
                                                  time_F,
                                                  time_S,
                                                  dt,
                                                  XS,
                                                  evolution,
                                                  tzero=time_initial,
                                                  tfinal=time_final)

# Resize shoreline_calib to XS size
# time_Fy_c shoreline_calib // time_S XS

time_match_obs_in_data = match(time_Sy, time_Fy_c)
time_match_data_in_obs = match(time_Fy_c, time_Sy)
time_match_obs_in_data = [i for i in time_match_obs_in_data if i is not None]
time_match_data_in_obs = [i for i in time_match_data_in_obs if i is not None]

data = [shoreline_calib[i] for i in time_match_obs_in_data]
obs = [XS[i] for i in time_match_data_in_obs]

RMSE = rmse(np.array(data), np.array(obs))

#with open('nmse.txt', 'w') as f:
#    f.write(repr(NMSE) + '   NMSE ')

#with open('rmse.txt', 'w') as f:
#    f.write(repr(RMSE) + '   RMSE ')

#with open('bss.txt', 'w') as f:
#    f.write(repr(BSS) + '   BSS ')

with open('results.txt', 'w') as f:
    f.write(repr(RMSE) + '   RMSE \n')
    #f.write(repr(BSS) + '   BSS ')
