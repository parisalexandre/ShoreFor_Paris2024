#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
These functions plot the calibration part and the extrapolation if needed
"""

import pandas
import matplotlib.pyplot as plt
from matplotlib import dates
import seaborn as sns
import numpy as np
from dates_functions import _from_ordinal

sns.set_theme()
sns.set_context('talk')


def on_resize(event):
    plt.tight_layout()
    plt.draw()


def plot_calibration(time_shor, time_for, omega_for, vecind,
                     omega_eq, shoreline, data, evolution, frag):
    """
    Plot the Dean parameter evolution in top of Figure.
    Below, plot of the shoreline or bar evolution
    calculated with calibrated parameters
    """
    fig, (ax1, ax2) = plt.subplots(2, 1)

    ## DEAN EVOLUTION
    # time_for_full = [_from_ordinal(t) for t in timef_full]
    # x1_datef = dates.date2num(time_for_full)
    if isinstance(time_for[0], float):
        x1_dates = [_from_ordinal(t) for t in time_for]
        x1_dates_shor = x1_dates[vecind[0]:vecind[-1]+1]
        y1_omegaf = omega_for
        y2_omegaeq = omega_eq
    else:
        x1_dates = dates.date2num(time_for)
        x1_dates_shor = x1_dates
        y1_omegaf = omega_for[vecind]
        y2_omegaeq = omega_eq[vecind]
    x2_dates = dates.date2num(time_shor)

    if len(frag) > 0:
        y3_data = pandas.DataFrame({'date': x2_dates, 'data': data, 'frag': frag})
        y3_data['frag'] = y3_data['frag'] * 2
    else:
        y3_data = data
    
    # Time parameters
    ax1.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
    locator = dates.MonthLocator(interval=6)
    ax1.xaxis.set_major_locator(locator)
    ax1.set_xlim(left=x1_dates[0], right=x1_dates[-1])
    ax1.tick_params(axis='x', rotation=70)

    ax1.plot(x1_dates, y1_omegaf, linestyle='solid', color='black')
    ax1.set(ylabel='Dean parameter')
    ax1.plot(x1_dates, y2_omegaeq*1.0, linestyle='dashed', color='red',
             label='equilibrium Dean number',
             linewidth=4)
    ax1.legend()

    ## CALIBRATED SHORELINE/BAR EVOLUTION
    if evolution == 'shoreline':
        ax2.plot(x1_dates_shor, shoreline, label='Calibrated shoreline',
                 color='green', zorder=2, linewidth=3)
                 #color='gold', zorder=2, linewidth=3) #, marker='d', markersize=8, markevery=72,
                 #markeredgecolor='goldenrod')
                 #color='royalblue', zorder=2, linewidth=3, marker='s', markersize=6, markevery=72,
                 #markeredgecolor='mediumblue')
                 #color='mediumpurple', zorder=2, linewidth=3, marker='*', markersize=10,
                 #markevery=72, markeredgecolor='indigo')
    elif evolution == 'bars':
        ax2.plot(x1_dates_shor, shoreline, label='Calibrated bar position',
                 #color='green', zorder=2, linewidth=3)
                 #color='gold', zorder=2, linewidth=3, marker='d', markersize=8, markevery=72,
                 #markeredgecolor='goldenrod')
                 #color='royalblue', zorder=2, linewidth=3, marker='s', markersize=6, markevery=72,
                 #markeredgecolor='mediumblue')
                 color='mediumpurple', zorder=2, linewidth=3, marker='*', markersize=10,
                 markevery=72, markeredgecolor='indigo')

    ## SURVEY DATA
    rms_error = np.sqrt(np.nansum((data - np.mean(data))**2) / len(data))
    if evolution == 'shoreline':    
        ax2.errorbar(x2_dates, y3_data, yerr=rms_error,
                     ecolor='mediumseagreen', fmt='o', color='mediumseagreen',
                     markeredgecolor='green', capsize=5, zorder=1,
                     label='Shoreline data', alpha=1, elinewidth=4)
        ax2.set(xlabel='Time', ylabel='Shoreline position (m)')
    elif evolution == 'bars':
        sns.scatterplot(data=y3_data, x='date', y='data', hue='frag',
                        palette='Greens', ax=ax2, legend=False, zorder=10)
        ax2.errorbar(y3_data['date'], y3_data['data'], yerr=rms_error,
                     ecolor='mediumseagreen', fmt='o', color='mediumseagreen',
                     markeredgecolor='green', capsize=5, zorder=1,
                     label='Bar data', alpha=1, elinewidth=4)
        ax2.set(xlabel='Time', ylabel='Bar position (m)')

    # Time parameters
    ax2.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_locator(locator)
    ax2.set_xlim(left=x1_dates[0], right=x1_dates[-1])
    ax2.tick_params(axis='x', rotation=70)
    ax2.legend()

    ax1.set_xticklabels([])

    # Arrows for direction of evolution
    if evolution == 'shoreline':
        ax2.annotate('accretion', xy=(0.98, 0.98), xycoords='axes fraction',
                     xytext=(0.98, 0.80), textcoords='axes fraction',
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     horizontalalignment='center')
        ax2.annotate('erosion', xy=(0.98, 0.02), xycoords='axes fraction',
                     xytext=(0.98, 0.15), textcoords='axes fraction',
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     horizontalalignment='center')
    elif evolution == 'bars':
        ax2.annotate('offshore', xy=(0.98, 0.98), xycoords='axes fraction',
                     xytext=(0.98, 0.80), textcoords='axes fraction',
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     horizontalalignment='center')
        ax2.annotate('onshore', xy=(0.98, 0.02), xycoords='axes fraction',
                     xytext=(0.98, 0.15), textcoords='axes fraction',
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     horizontalalignment='center')

    plt.tight_layout()
    fig.canvas.mpl_connect('resize_event', on_resize)

    return fig, (ax1, ax2)


def plot_future(time_shor, time_for_c, time_for_f, shoreline_fut, data, evolution,
		ax_1, ax_2):
    """
    Plot the future shoreline/bar evolution on the same figure as before
    """
    if evolution == 'shoreline':
        ax_2.plot(dates.date2num(time_for_f), shoreline_fut,
                  label='Future shoreline', color='blue')
                  #label='Future shoreline', color='gold', marker='d', markersize=8, markevery=72,
                  #markeredgecolor='goldenrod', linewidth=3)
                  #label='Future shoreline', color='royalblue', marker='s', markersize=6,
                  #markevery=72, markeredgecolor='mediumblue', linewidth=3)
                  #label='Future shoreline', color='mediumpurple', marker='*', markersize=10,
                  #markevery=72, markeredgecolor='indigo', linewidth=3)
    elif evolution == 'bars':
        ax_2.plot(dates.date2num(time_for_f), shoreline_fut,
                  #label='Future bar position', color='blue')
                  #label='Future bar position', color='gold', marker='d', markersize=8, markevery=72,
                  #markeredgecolor='goldenrod', linewidth=3)
                  #label='Future bar position', color='royalblue', marker='s', markersize=6,
                  #markevery=72, markeredgecolor='mediumblue', linewidth=3)
                  label='Future bar position', color='mediumpurple', marker='*', markersize=10,
                  markevery=72, markeredgecolor='indigo', linewidth=3)
    
    ax_2.set_xlim(left=dates.date2num(time_for_c)[0],
                  right=dates.date2num(time_for_f)[-1])
    ax_1.set_xlim(left=dates.date2num(time_for_c)[0],
                  right=dates.date2num(time_for_f)[-1])
    ax_2.legend()
