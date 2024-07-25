#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Principal function of ShoreFor

Calculates the shoreline or bar evolution

Author: Alexandre Paris
"""

import numpy as np
from dates_functions import _from_ordinal
from tools import find_nearest
import warnings


def loopw(b, c):
    """
    a: shoreline
    b: data
    c: loc
    """
    i = 10
    while i > 1:
        try:
            with warnings.catch_warnings(record=True) as war:
                warnings.simplefilter('always')
                a = np.mean(b[c[0]-i:c[0]])
                if any(issubclass(warn.category, RuntimeWarning) for warn in war):
                    raise RuntimeWarning
            break
        except RuntimeWarning:
            i =- 1
    if i == 1:
        a = b[c[0]]
    return a


def shorecore(bopti, copti, ratio_erosion, fff_minus, fff_plus,
              timef, times, deltat, data, evolution,
              fut=False, tzero=None, tfinal=None):
    """
    Calculation of the shoreline/bar evolution with the
    optimized parameters
    """
    if tzero is None:
    # If the initial time is not defined
        if times[0] >= timef[0]:  # waves before data
            tzero = times[0]
            ii0 = np.min(np.where((timef <= (tzero+deltat))
                                  & (timef >= (tzero-deltat))))
        else:  # data before waves / not recommended
            tzero = timef[0]
            ii0 = 0
    else:
        ii0 = np.min(np.where((timef <= (tzero+deltat))
                              & (timef >= (tzero-deltat))))

    if tfinal is None:
    # If the final time is not defined
        if times[-1] < timef[-1]:  # waves after data
            tfinal = times[-1]
            iif = np.max(np.where((timef <= (tfinal+deltat))
                                 & (timef >= (tfinal-deltat))))
        else:
            tfinal = timef[-1]
            iif = len(timef)
    else:
        iif = np.max(np.where((timef <= (tfinal+deltat))
                             & (timef >= (tfinal-deltat))))

    vecind = np.arange(ii0, iif+1)
    time_for = [_from_ordinal((float(timef[vecind][i]))).strftime('%Y-%m-%d %H:%M:%S')
                for i in range(len(timef[vecind]))]

    shoreline = np.zeros(len(time_for)+1)
    # If fut == True, tzero is the initial date of extrapolation
    # If fut == False, tzero is the initial date of calibration 
    nearest = find_nearest(np.asarray(times), value=tzero)
    loc = np.where(times==nearest)[0]
    if evolution == 'shoreline':
        shoreline[0] = loopw(data, loc)
    elif evolution == 'bars':
        shoreline[0] = data[loc]

    delta_shor = np.zeros(len(time_for))
    for i in range(len(time_for)):
        varki = ii0 + i
        iff = ((ratio_erosion*fff_minus[varki-1] + fff_plus[varki-1])
               + (ratio_erosion*fff_minus[varki] + fff_plus[varki]))/2
        delta_shor = (bopti + copti*iff) * deltat
        shoreline[i+1] = shoreline[i] + delta_shor
    
    shoreline = shoreline[1::]

    return shoreline, time_for, vecind
