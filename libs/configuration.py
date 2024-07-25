#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Alexandre Paris
"""

import yaml
from dates_functions import datenum


def config():
    """
    Read the configuration file, extract data
    and write parameters in Dakota files

    shor_file: file with survey data
    for_file: forcing file
    b_min, b_max, c_min, c_max, phi_min, phi_max: limits of parameters
    extrapolate: future evolution or not
    tzero_future, tfin_future: time limits for future extrapolation
    case_na: name of the study
    evol: type of data (shoreline, bar)
    
    dakota_pstudy.in is the input file for Dakota
    
    parameters.txt.template is the parameters file for Dakota,
    and will be added to each directory by Dakota during the optimization
    """
    with open(r'./config_shorefor.yaml') as file:
        clef = yaml.full_load(file)
    
    shor_file = clef['input_files']['shoreline_file']
    for_file = clef['input_files']['waves_file']
    b_min = clef['dakota_params']['b_min']
    b_max = clef['dakota_params']['b_max']
    c_min = clef['dakota_params']['c_min']
    c_max = clef['dakota_params']['c_max']
    phi_min = clef['dakota_params']['phi_min']
    phi_max = clef['dakota_params']['phi_max']
    # Calculate the initial parameters from previous limits
    b_init = round(((b_max - b_min)/2)+b_min, 1)
    c_init = round(((c_max - c_min)/2)+c_min, 1)
    phi_init = round(((phi_max - phi_min)/2)+phi_min, 1)
    # Times for calibration
    time_init = datenum(clef['calibration']['time_initial'])
    time_fin = datenum(clef['calibration']['time_final'])
    # Extrapolation and first time for future
    extrapolate = clef['future']['extrapolate']
    tzero_future = datenum(clef['future']['begin_future_time'])
    tfin_future = datenum(clef['future']['final_future_time'])
    case_na = clef['case']['study']
    evol = clef['case']['evolution']
    
    if evol == 1:
        evolut = 'shoreline'
    elif evol == 2:
        evolut = 'bars'
    
    if extrapolate == 1:
        fut = True
    else:
        fut = False
    
    with open('./dakota_pstudy.in', 'r') as file:
        get_all = file.readlines()
    
    with open('./dakota_pstudy.in', 'w') as file:
        for i, line in enumerate(get_all, 1):
            if 'initial_point' in line:
                file.writelines('    initial_point    {}        {}        {}\
                                \n'.format(b_init, c_init, phi_init))
            elif 'lower_bounds' in line:
                file.writelines('    lower_bounds    {}        {}        {}\
                                \n'.format(b_min, c_min, phi_min))
            elif 'upper_bounds' in line:
                file.writelines('    upper_bounds    {}        {}        {}\
                                \n'.format(b_max, c_max, phi_max))
            else:
                file.writelines(line)
    
    with open('parameters.txt.template', 'w') as file:
        lines = ['# b c phi\n',
                 '{} {} {} #min\n'.format(b_min, c_min, phi_min),
                 '{} {} {} #max\n'.format(b_max, c_max, phi_max),
                 '{b} {c} {phi} #start\n']
        file.writelines(lines)
    
    return (shor_file, for_file, fut, tzero_future, tfin_future,
            time_init, time_fin, case_na, evolut)
