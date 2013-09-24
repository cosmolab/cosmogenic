"""
Functions for calculating exposure ages.

We generally follow the notation of Tibor Dunai (2010), Cosmogenic Nuclides:
Principles, Concepts and Application in the Earth Surface Sciences, Cambridge
University Press, Cambridge. pp. 187.
"""
from __future__ import division, print_function, unicode_literals

import numpy as np
import scipy.optimize as opt

from cosmogenic import production, sim

def exposure_age(C, P, nuclide, z0=0.0, erosion_rate=None, z=None):
    """
    Parameters:
    ----------
    C:  concentration of cosmogenic nuclide (CN) (atoms / g)
    P:  function
        local production rate at depth in g/cm**2
        units: (atoms / g / yr)
    nuclide: a cosmogenic nuclide object
    z0: modern depth (g / cm**2)
    erosion_rate (optional): assumed constant rate of erosion (g / cm**2 / yr),
                             default is no erosion
    z (optional): Function z(t) that returns depth in cm
    erosion_rate: (optional) Rate of steady erosion to assume (ignored if z is
                  supplied.
    """

    
    # construct z(t) function if one was not supplied
    if z is None:
        if erosion_rate is None:
            z = lambda t: z0
        else:
            def z(t):
                return z0 + erosion_rate * t
    
    def residual(t):
        C_model, _ = sim.nexpose(P, nuclide, z, t)
        return np.abs(C - C_model)
    
    # go out to 7 half lives... this is really pushing it
    # the sample would be saturated at this age
    upper_age_bound = 7 * np.log(2) / nuclide.LAMBDA
    bounds = (0.0, upper_age_bound)

    res = opt.minimize_scalar(residual, bounds=bounds, method='bounded')
    if res.success:
        t = res.x
        return sim.nexpose(P, nuclide, z, t)
    else:
        raise Error("Something went wrong in the inversion")
