Cosmogenic
==========

Cosmogenic is a Python library for modeling in-situ cosmogenic nuclide production and geomorphic processes.
It includes total nuclide production rates (from reactions due to spallation + muons) for Be-10 and Al-26 in quartz, and Cl-36 in K-feldspar.
Muon production is modeled after Heisinger (2002a,b) with some modified constants.
Production rates can be scaled to a site latitude and altitude using the Lal/Stone scaling scheme (Stone 2000).
More scaling schemes and production pathways are planned to be implemented in the future.

In the "sim" module, Cosmogenic provides functions to integrate the production rate functions over time in different exposure, erosion, and burial scenarios.
It provides the tools to model and predict cosmogenic nuclide concentrations in surface samples or depth profiles given a specific erosion history.

In the "na" module, Cosmogenic provides a way to invert cosmogenic nuclide data for model parameters of your choice using the Neighborhood Algorithm (Sambridge 2000a,b).
The Neighborhood Algorithm is completely general, and can be used to invert for the parameters of any model callable from Python.
The user must write a misfit function to determine the goodness of fit to the data for a set of model parameters.

This library is still under heavy development.
Predictive models of cosmogenic concentrations for a prescribed erosion history are robust.
Tools for calculating exposure ages are still experimental.
If you want to calculate exposure ages, you would be best served by using the exposure age calculator at http://hess.ess.washington.edu.

Cosmogenic is beta software. We welcome contributions in the form of pull requests and bug reports.

Modules
-------

* muon:          production from muons
* production:    spallation and total production rate functions
* scaling:       functions for scaling cosmogenic nuclide production rates
* sim:           geomorphic and exposure models
* na:            Cython implementation of the neighborhood algorithm
* nuclide:       specific nuclides / target material models
* util:          utility functions

Experimental modules still in heavy development:
* dating:        functions for calculating exposure ages
* datareduction: functions for reducing AMS data


Installation
------------

To work properly, Cosmogenic expects that you have already installed a recent version of the SciPy stack.
See here for your options:

http://www.scipy.org/install.html

The simplest way to get a working development system is to install Enthought Canopy or Anaconda from Continuum Analytics.
On Linux systems you may want to install the dependencies using your distribution's package manager.
The author prefers to install development headers and build the package using pip inside a virtualenv.
This can be accomplished by running "pip install -r pip-requirements" in the project root directory.

Until we begin to produce official release tarballs, you will need Cython and a working C compiler to build this project. Testing has been done using GCC.

To build, execute the following commands:

```
$ python setup.py build_ext --inplace
```

Then install with either:

```
$ python setup.py install
```

Or if you intend to make changes to the library's code, you can use:

```
$ python setup.py develop
```

This will allow any changes you make to the library code to be available without reinstalling each time.
