#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This function processes calculates the Dean parameter,
the equilibrium Dean parameter and the erosion ratio

Author: Alexandre Paris
"""

import numpy as np


def dean(hsf, tpf, fall_velocity, deltat, power, same, opti_phi, timef):
    # Dean parameter calculated on forcing time
    with np.errstate(divide='ignore', invalid='ignore'):
        omegaf = hsf/(tpf*fall_velocity)
    omegaf[np.isnan(omegaf)] = 0
    
    phi = round(opti_phi)  # memory decay in days
    num_per_day = round(1/deltat)  # 1/dt_forcing, number of values per day)
    ddd = 2*phi*num_per_day  # number of values in the computation of omega_eq
    qqq = 10**(-1/(phi*num_per_day))
    deno = (1-qqq**(ddd+1))/(1-qqq)  #geometric series

    omega_eq = np.zeros(len(timef))
    vqq = np.ones(((ddd+1), 1))
    for i in range(1, ddd+1):
        vqq[i] = qqq**i
    vqq = np.flipud(vqq)

    for k in range(ddd+1, len(timef)):
        omega_eq[k] = np.matmul(omegaf[(k-ddd-1):k], vqq)
    omega_eq = omega_eq / deno
    delta_omega = omega_eq - omegaf
    sigma_domega = np.sqrt(np.nanmean((delta_omega
                                       - np.nanmean(delta_omega))**2))

    # Calculate the 2nd term of the formulation for every time interval
    fff = np.zeros(len(timef))
    fff_plus = np.zeros(len(timef))
    fff_minus = np.zeros(len(timef))
    # Forcing term, erosion or accretion
    fff = delta_omega * np.sqrt(power) / sigma_domega
    fff_plus[fff > 0] = fff[fff > 0]
    fff_minus[fff < 0] = fff[fff < 0]
    # Calculate mean value of fff_plus and fff_minus for every survey time interval
    indr = np.arange(same[0], same[-1]+1)
    ratio_erosion = np.absolute(np.nansum(fff_plus[indr])
                                /
                                np.nansum(fff_minus[indr]))
    print('erosion ratio', ratio_erosion)
    
    mff_pl = np.zeros(len(timef))
    mff_mi = np.zeros(len(timef))
    for i in range(len(same)-1):
        m = same[i]
        n = same[i+1]
        # n-m is the number of forcing values between 2 surveys    
        if (m+1) == n:     # they is no gap            
            mff_pl[i] = fff_plus[n]*deltat
            mff_mi[i] = fff_minus[n]*deltat
        else:
            mff_pl[i] = np.sum(fff_plus[m+1:n])*deltat
            mff_mi[i] = np.sum(fff_minus[m+1:n])*deltat

    return ratio_erosion, fff_minus, fff_plus, omegaf, omega_eq
