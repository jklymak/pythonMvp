# -*- coding: utf-8 -*-
"""
Created on Thu May 16 17:37:14 2013

@author: FoxR
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys

def bindata2(x, y, z, xi, yi, ppbin=False, binval='median'):
    """
    Bin irregularly spaced data on a regular grid (center of the bins).

    Computes the median (default) or mean value within bins defined by
    regularly spaced xi and yi coordinates (the grid defining the bins).

    Parameters
    ----------
    x, y : ndarray (1D)
        The idependent variables x- and y-axis of the grid.
    z : ndarray (1D)
        The dependent variable in the form z = f(x,y).
    xi, yi : ndarray (1D)
        The coordinates defining the x- and y-axis of the grid.
    ppbin : boolean, optional
        The function returns `bins` variable (see below for description): 
        [False | True].
    binval : string, optional
        The statistical operator used to compute the value of each 
        bin: ['median' | 'mean'].

    Returns
    -------
    grid : ndarray (2D)
        The evenly binned data. The value of each cell is the median
        (or mean) value of the contents of the bin.
    bins : ndarray (2D)
        A grid the same shape as `grid`, except the value of each cell
        is the number of points per bin. Returns only if `ppbin` is set
        to True.

    Revisions
    ---------
    2010-11-06 Fernando Paolo, Initial version 
    """

    if binval == 'median':
        median = True
    else:
        median = False

    # make the grid
    nrow = yi.shape[0]
    ncol = xi.shape[0]
    grid = np.empty((nrow,ncol), dtype=xi.dtype)
    if ppbin: bins = np.copy(grid)

    # step size (rectangular cells)
    dx = xi[1]-xi[0]
    dy = yi[1]-yi[0]
    hx = dx/2.
    hy = dy/2.

    # bin the data
    for row in xrange(nrow):
        for col in xrange(ncol):
            xc = xi[col]          # xc,yc = center of the bin
            yc = yi[row]
            ind, = np.where((xc-hx <= x) & (x < xc+hx) & \
                            (yc-hy <= y) & (y < yc+hy))
            npts = len(ind)
            if npts > 0:
                if median:
                    grid[row,col] = np.median(z[ind])
                else:
                    grid[row,col] = np.mean(z[ind])
                if ppbin: bins[row,col] = npts
            else:
                grid[row,col] = np.nan
                if ppbin: bins[row,col] = 0

    # return the grid
    if ppbin:
        return grid, bins
    else:
        return grid