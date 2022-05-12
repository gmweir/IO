# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:11:07 2016

@author: gawe
"""
# ========================================================================== #

from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals

# ========================================================================== #
# ========================================================================== #

__version__ = "2018.05.24.17"
__all__ = ['egDataFormatIO','HDF', 'fdf', 'txtutils'] #, 'save_txt']

from . import egDataFormatIO as lhd_io # analysis:ignore
from . import HDF as hdf5_io      # analysis:ignore
from . import fdf as fdf_io       # analysis:ignore
from . import txtutils as txt_io  # analysis:ignore

# ======== #

#  Backwards compatibility  # annoyingly filling the namespace
#  -->  Needs to be cleaned up
from . import egDataFormatIO, HDF, fdf , txtutils #save_txt  # analysis:ignore
from .HDF import save_hdf5   # backwards compatibility
from .HDF.save_hdf5 import ReportInterface as saveHDF5  # analysis:ignore
from .HDF.save_hdf5 import loadHDF5data as loadHDF5  # analysis:ignore
from .egDataFormatIO import egDataFormatIO as eg  # analysis:ignore
from .fdf import Fdf as fdf # analysis:ignore
from .txtutils import scanf, sscanf, fscanf, ftell, fseek, frewind, fgets, fgetl, findstr  # analysis:ignore

# ======== #


# ===================================================================== #
# ===================================================================== #





