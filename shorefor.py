#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Equilibrium cross-shore model ShoreFor with optimization by Dakota.

Main script

Author: Alexandre Paris
"""

import sys
#import datetime
#import subprocess
#import yaml
#import pandas
#import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas
from matplotlib import dates

sys.path.append('./libs')
from dates_functions import _from_ordinal, datenum
from tools import match, find_nearest, rmse, bss
from optimization import optimization
from read_files import reading_files
from dean import dean
from shorecore import shorecore
from plot_functions import plot_calibration, plot_future
from configuration import config

###############################################################################

(shoreline_file, forcing_file, future, tzero_fut,
 tfin_fut, time_initial, time_final, case_name, evolution) = config()

opti_b, opti_c, opti_phi = optimization()

(time_S, time_Sy, loc_init, loc_extra,
 time_F, dt, ii0, iif, vecind, same,
 XS, frag, hsf, tpf, power, fall_velocity) = reading_files(forcing_file,
                                                           shoreline_file,
                                                           time_initial,
                                                           time_final) #WARNING

erosion_ratio, FF_mi, FF_pl, omega_F, omega_eq = dean(hsf, tpf,
                                                      fall_velocity,
                                                      dt, power, same,
                                                      opti_phi, time_F)

shoreline_calib, time_Fy_c, vec_ind_c = shorecore(opti_b,
                                                  opti_c,
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

if future == True:
    tiempofinal = time_F
else:
    tiempofinal = time_Fy_c

fig1, (ax_1, ax_2) = plot_calibration(time_Sy,
                                      tiempofinal, #time_Fy_c,#time_F,
                                      omega_F,
                                      vec_ind_c,
                                      omega_eq,
                                      shoreline_calib,
                                      XS,
                                      evolution,
                                      frag)

if future == True:
    shoreline_future, time_Fy_f, vec_ind_f = shorecore(opti_b,
                                                       opti_c,
                                                       erosion_ratio,
                                                       FF_mi,
                                                       FF_pl,
                                                       time_F,
                                                       time_S,
                                                       dt,
                                                       XS,
                                                       evolution,
                                                       fut=True,
                                                       tzero=tzero_fut,
                                                       tfinal=tfin_fut)

    plot_future(time_Sy, time_Fy_c, time_Fy_f, shoreline_future, XS, evolution, ax_1, ax_2)

plt.show()

# OUTPUT PART; TO DO    
#    general_time = time_Fy_c + time_Fy_f
#    # Fills series with NaN
#    calib_shoreline = shoreline_calib.tolist() + ['NaN']*len(time_Fy_f)
#    future_shoreline = ['NaN']*len(time_Fy_c) + shoreline_future.tolist()

#else:
#    general_time = time_Fy_c
#    calib_shoreline = shoreline_calib.tolist()
#    future_shoreline = ['NaN']*len(time_Fy_c)

#general_time_num = [datenum(t) for t in general_time]
#dict_results = {'time': general_time,
#                'datenum': general_time_num,
#                'calib_shoreline': calib_shoreline,
#                'future_shoreline': future_shoreline}
#results = pandas.DataFrame(dict([(k, pandas.Series(v)) for k, v in dict_results.items()]))
#if os.path.isdir('results') == False:
#    os.system('mkdir results')
#results.to_csv('./results/results_shorefor_'+case_name+'_'+evolution
#               +'_b'+str(opti_b)+'_c'+str(opti_c)+'_phi'+str(opti_phi)+'.csv', index=False)
