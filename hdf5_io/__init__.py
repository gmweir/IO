# -*- coding: utf-8 -*-
"""
Created on Thu May 12 15:28:17 2022

@author: gawe
"""

# ========================================================================== #

from __future__ import absolute_import, with_statement, \
                       division, print_function, unicode_literals

__version__ = "2022.05.12.16"

__all__ = ['hdf5_io']

# ========================================================================== #
# ========================================================================== #

import sys as _sys

ispy3 = True
if _sys.version_info < (3,0):
    ispy3 = False
# end if

# Custom specialty methods ... works with W7-X data where None is saves as 'None', and Struct classes are also saved / loaded.
from . import hdf5_io  # analysis:ignore
from .hdf5_io import loadHDF5data as loadHDF5  # analysis:ignore
from .hdf5_io import ReportInterface  # analysis:ignore

# General use / non- custom HDF5 files
if ispy3:
    from . import hdf5_io_py3   # analysis:ignore
    from .hdf5_io_py3 import save, load, save_to_hdf5, load_from_hdf5, valid_hdf5_path_component   # analysis:ignore
else:
    from . import hdf5_io_py2   # analysis:ignore
    from .hdf5_io_py2 import save, load, save_to_hdf5, load_from_hdf5, valid_hdf5_path_component   # analysis:ignore
# end if

# ========================================================================== #

# backwards compatibility
from . import hdf5_io as __old_save_hdf5



# ========================================================================== #
# ========================================================================== #


