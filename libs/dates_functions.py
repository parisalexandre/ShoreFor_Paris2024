#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Conversion dates fonction, inspired from Matlab functions

Author: Alexandre Paris
"""

import sys
import datetime


def _from_ordinal(serial_dn):
    """
    This function converts a serial date number into a datetime object

    The reference for datetime.fromordinal is 0001/01/01

    Example:
    _from_ordinal(728182)
    >>> datetime.datetime(1993, 9, 10, 0,0)

    str(_from_ordinal(728182))
    >>> '1993-09-10 00:00:00'
    """
    i_x = int(serial_dn)
    classic_date = datetime.datetime.fromordinal(i_x-366)
    remainder = float(serial_dn) - i_x
    hour, remainder = divmod(24 * remainder, 1)
    minute, remainder = divmod(60 * remainder, 1)
    second, remainder = divmod(60 * remainder, 1)
    microsecond = int(1e6 * remainder)
    if microsecond < 10:
        microsecond = 0  # compensate for rounding errors
        classic_date = datetime.datetime(classic_date.year, classic_date.month,
                                         classic_date.day, int(hour), int(minute),
                                         int(second), microsecond)

    if microsecond > 999990:  # compensate for rounding errors
        classic_date += datetime.timedelta(microseconds=1e6 - microsecond)

    return classic_date


def datenum(date):
    """
    Equivalent of datenum Matlab function

    Example:
    datenum('1993-09-10')
    >>> 728182.0
    """
    date_patterns = ["%Y-%m-%d", "%Y%m%d%H%M", "%Y-%m-%d %H:%M:%S"]
    for pattern in date_patterns:
        try:
            date_d = datetime.datetime.strptime(date, pattern)
            return (366 + date_d.toordinal()
                    + (date_d -
                    datetime.datetime.fromordinal(date_d.toordinal())).total_seconds()
                    / (24 * 60 * 60)
                   )
        except:
            pass

    print('Error: the date pattern is not {} or {}'.format(date_patterns[0],
           date_patterns[1]))
    sys.exit()
