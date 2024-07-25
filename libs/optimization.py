#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This functions reads the configuration file.
If the optimization is required to be done with Dakota,
the functions runs the optimization and reads the final optimized parameters.

Author: Alexandre Paris 
"""

import sys
import yaml
import subprocess


def optimization():
    """
    Read the configuration file and run the optimization
    of the parameters b, c and phi or read their values
    """
    with open(r'./config_shorefor.yaml') as f:
        clef = yaml.full_load(f)

    opti = clef['optimization']['dakota']
    if opti == 1:
        with subprocess.Popen(['dakota', '-i', 'dakota_pstudy.in']) as process:
            process.wait()

        # Best RMSE and BSS
        with open('dakota_results.txt', 'r') as f:
            params = f.readlines()[5:8]
            bopti = float(params[0])
            copti = float(params[1])
            phiopti = float(params[2])

        print('Otimized coefficients:\n')
        print('b: ', bopti)
        print('c: ', copti)
        print('phi: ', phiopti)
    
    elif opti == 2:
        bopti = clef['optimization']['b']
        copti = clef['optimization']['c']
        phiopti = clef['optimization']['phi']
    
    else:
        print('ERROR: Optimization choice in the configuration file is not recognized')
        sys.exit()

    return bopti, copti, phiopti
