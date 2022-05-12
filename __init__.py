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

__version__ = "2022.05.12.16"
__all__ = ['lhd_io','hdf5_io', 'fdf_io', 'txtutils'] #, 'save_txt']

from . import lhd_io       # analysis:ignore
from . import hdf5_io      # analysis:ignore
from . import fdf_io       # analysis:ignore
from . import txtutils as txt_io  # analysis:ignore

from .hdf5_io import loadHDF5  # analysis:ignore
from .lhd_io import egDataFormatIO as eg  # analysis:ignore
from .fdf_io import Fdf as fdf # analysis:ignore
from .txtutils import scanf, sscanf, fscanf, ftell, fseek, frewind, fgets, fgetl, findstr  # analysis:ignore


# ===================================== #

#  Backwards compatibility  # annoyingly filling the namespace
#  -->  Needs to be cleaned up
egDataFormatIO = lhd_io
save_hdf5 = hdf5_io.__old_save_hdf5
saveHDF5 = save_hdf5.ReportInterface  # analysis:ignore

# ===================================================================== #
# ===================================================================== #





