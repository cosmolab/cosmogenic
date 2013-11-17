"""
Functions to calculation production rates
"""

from __future__ import division, print_function, unicode_literals

import numpy as np
import numexpr as ne

from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.interpolate import dfitpack

from cosmogenic import muon
from cosmogenic import scaling

LAMBDA_h = 160.0 # attenuation length of hadronic component in atm, g / cm2
LAMBDA_fast = 4320.0 # after Heisinger 2002


def P_sp(z, n, scaling=None, alt=0, lat=75):
    """
    Returns production rate due to spallation reactions (atoms/g/yr)

    ::math P_{sp} = f_{scaling} * P_0 * exp(-z / \Lambda)

    where f_scaling is a scaling factor. It currently scales for altitude
    and latitude after Stone (2000).

    z: depth in g / cm**2 (vector or scalar)
    alt: site altitude in meters
    lat: site latitude (degrees)
    n: nuclide object
    """
    if scaling == 'stone':
        f_scaling = scal.stone2000_sp(lat, alt)
    else:
        f_scaling = 1.0
    
    return f_scaling * n.P0 * np.exp(-z / LAMBDA_h)


def P_tot(z, alt, lat, n, scaling=None):
    """
    Total production rate of nuclide n in atoms / g of material / year
    
    z: depth in g / cm**2 (vector or scalar)
    alt: site altitude in meters
    lat: site latitude (degrees)
    n: nuclide object
    """
    return P_sp(z, n, scaling, alt, lat) + muon.P_mu_total(z, alt, n)


def interpolate_P_tot(max_depth, npts, alt, lat, n, scaling='stone'):
    """
    Interpolates the production rate function using a spline interpolation.

    max_depth: maximum depth to interpolate to (g / cm**2)
    alt: site altitude in meters
    lat: site latitude (degrees)
    n: nuclide object
    """
    zs = np.unique(np.logspace(0, np.log2(max_depth + 1), npts, base=2)) - 1
    prod_rates = P_tot(zs, alt, lat, n, scaling)
    p = ProductionSpline(zs, prod_rates)
    return p, zs, prod_rates

class ProductionSpline(InterpolatedUnivariateSpline):
    
    def __init__(self, x=None, y=None, w=None, bbox = [None]*2, k=3, s=None, 
                       filename=None):
        """
        Input:
          x,y   - 1-d sequences of data points (x must be
                  in strictly ascending order)

        Optional input:
          w          - positive 1-d sequence of weights
          bbox       - 2-sequence specifying the boundary of
                       the approximation interval.
                       By default, bbox=[x[0],x[-1]]
          k=3        - degree of the univariate spline.
          s          - positive smoothing factor defined for
                       estimation condition:
                         sum((w[i]*(y[i]-s(x[i])))**2,axis=0) <= s
                       Default s=len(w) which should be a good value
                       if 1/w[i] is an estimate of the standard
                       deviation of y[i].
          filename   - file to load a saved spline from
          
          

        """
        
        if (x == None) or (y == None) and (filename != None):
            with open(filename, "br") as fd:
                self._data = pickle.load(fd)
        else:
            self._data = dfitpack.fpcurf0(x,y,k,w=w,
                                      xb=bbox[0],xe=bbox[1],s=0)
                                    
        self._reset_class()

    def __call__(self, x, nu=0):
        res = super(ProductionSpline, self).__call__(x, nu)
        res_arr = np.atleast_1d(res)
        res_arr[res_arr < 0.0] = 0.0
        return res_arr[0] if res_arr.size == 1 else res_arr
        
    def save(self, filename):
        """
        What gets saved is pretty specific to the version of scipy that we are use
        so is important to test that this works with new versions of scipy. For
        now, the only important values for the spline interpolation are stored in
        the spline's _data member, but could change, as could the structure of
        _eval_args. To be safe, do not depend on this to load old interpolations.
        It is probably safest to create a new interpolation for a new scipy
        version.
        """
        with open(filename, "bw") as fd:
            pickle.dump(self._data, fd)


def load_interpolation(name):
    """
    Load a spline interpolation from disk.

    name: (string) name of file to load from
    """
    return ProductionSpline(filename=name)


def save_interpolation(name, spline):
    """
    Save a spline interpolation to disk.
    """
    return spline.save(name)
