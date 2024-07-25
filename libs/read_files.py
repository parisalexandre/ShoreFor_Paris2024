#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The forcing() function processes input data related to wave characteristics
and survey data

TODO: tests on the files formats

Author: Alexandre Paris
"""

import pandas
import numpy as np
from tools import find_nearest, match
from dates_functions import _from_ordinal
from constants import GAMMA, G, RHO, DEIL, NU, D50


def reading_files(file_forcing, file_shoreline, init_c, init_f):
    """
    Read the files and extract times
    shoreline or bar file: time position (frag if bar)
    forcing file: time hs tp
    init_c: initial time of calibration in 7***** format
    init_f: initial time of extrapolation (future) in 7***** format
    """
    #shoreline_data = np.loadtxt(file_shoreline, usecols=(0, 1))
    #shoreline_data = pandas.DataFrame(data=shoreline_data).replace('NaN', np.nan).dropna().to_numpy()

    shoreline_data = pandas.read_csv(file_shoreline, sep=' ')
    shoreline_data = shoreline_data.replace('NaN', np.nan).dropna().to_numpy()
    forcing_data = np.loadtxt(file_forcing)

    ## Survey data
    times = shoreline_data[:, 0]
    # time_shor: time in date format
    time_shor = [_from_ordinal(times[i]).strftime('%Y-%m-%d %H:%M:%S')
                 for i in range(len(times))]
    # Find the position of initial times in time of data
    nearest_init = find_nearest(np.asarray(times), value=init_c)
    loc_init = np.where(times==nearest_init)
    nearest_extra = find_nearest(np.asarray(times), value=init_f)
    loc_extra = np.where(times==nearest_extra)

    #data = shoreline_data[:, 1]
    data = -shoreline_data[:, 1]

    # In case the data file contains information about bar fragmentation
    if np.shape(shoreline_data)[1] > 2:
        frag = shoreline_data[:, 2]
    else:
        frag = []

    ## Wave data - offshore values
    timef = forcing_data[:, 0]
    deltat = np.mean(np.diff(timef))  # number of days between each point
    # Limit time forcing to the size of time data
    if times[0] >= timef[0]:  # case with waves before data
        tzero = times[0]
        ii0 = np.min(np.where((timef <= (tzero + deltat))
                  & (timef >= (tzero - deltat))))
    else:  # case with data before waves
        tzero = timef[0]
        ii0 = 0

    if times[-1] < timef[-1]:  # case with waves after data
        tfinal = times[-1]
        iif = np.max(np.where((timef <= (tfinal + deltat))
                              & (timef >= (tfinal - deltat))))
    else:  # case with data after waves
        tfinal = timef[-1]
        iif = len(timef)

    # List of all the indices for the length of the overlapping between data and forcing times
    vecind = np.arange(ii0, iif+1)
    
    # List of indices where times = timef
    times_list = times.tolist()
    timef_list = timef.tolist()
    same = match(times_list, timef_list)
    same = [i for i in same if i is not None]
    
    # Waves characteristics
    hs = forcing_data[:, 1]  # waves height
    tpf = forcing_data[:, 2]  # waves period
    hsf = 0.39*(9.81**0.2)*((tpf*hs**2)**(2/5))  # hs breaking Komar 1974
    depth_break = hsf / GAMMA  # depth of breaking
    celgroup = np.sqrt(depth_break * G)  # shallow water group velocity
    power = hsf**2*RHO*G*celgroup/16  # waves energy flux
    var_dst = D50*((DEIL*G/(NU**2))**(1/3))
    fall_velocity = NU*((np.sqrt(25+1.2*var_dst**2)-5)**1.5)/D50  # sediments fall velocity

    return (times, time_shor, loc_init, loc_extra,
            timef, deltat, ii0, iif, vecind, same, data, frag,
            hsf, tpf, power, fall_velocity)

