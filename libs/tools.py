#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple useful functions

Author: Alexandre Paris
"""

import numpy as np


def match(vector_a, vector_b):
    """
    Equivalent of the match() function in R
    """
    return [vector_b.index(x) if x in vector_b else None for x in vector_a]


def find_nearest(array, value):
    """
    Find the nearest item of a value in an array
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def rmse(data, model):
    """
    Calculates the Root Mean Square Error between data and model
    """
    return np.sqrt(np.nanmean((data - model)**2))


def nmse(data, model):
    """
    Calculates the Normalized Mean Square Error
    """
    return np.nansum((data - model)**2)/np.nansum(data**2)


def bss(data, model, b):
    """
    Calculates the Brier Skill Score between a model and the data
    data: observations
    model: results of modelling
    b: linear trend

    WARNING: this function is only used by Dakota to optimize the
    parameters b and c. However, Dakota will look for the min value
    of BSS, so here 1/value is return to avoid Dakota selecting the
    worse BSS (negative value) as the best.
    """
    baseline = np.zeros(len(data))
    dt_data = np.diff(data)
    baseline[0] = data[0]
    for i in range(1, len(data)):
        baseline[i] = baseline[i-1] + b * dt_data[i-1]
    value = 1 - np.nansum((data - model)**2)/np.nansum((data - baseline)**2)
    if value < 0:
        value = float(1)
        print('WARNING: negative BSS')
    return 1/value
