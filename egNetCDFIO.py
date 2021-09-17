# -*- coding: utf-8 -*-
"""
Created on Mon May  3 16:24:18 2021

@author: weir
"""
# ========================================================================== #
# ========================================================================== #
from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals

import numpy as _np
import os as _os
import netCDF4 as _nc4

#from scipy.io import savemat #,loadmat,whosmat
try:
    from pybaseutils.Struct import Struct
except:
    from ..Struct import Struct
# end try

__metaclass__ = type

# ========================================================================== #
# ========================================================================== #

def print_dict(my_dict, indent=1):
#    try:
#        import json as _jsn
#        _jsn.dumps(my_dict, indent=indent)
#    except:
    print(my_dict)
#    # end if
# end def

class ReportInterface(object):
    fmt = 'NETCDF4'
    # . ..more details about this class...

    def __init__(self, dic=None, filename=None):
        if filename is not None and filename.find('.nc')<0:
            filename += '.nc'
        if dic is not None and filename is not None:
            self.__save_dict_to_netCDF__(dic, filename)
        # end if
    # end def

    @classmethod
    def __save_dict_to_netCDF__(cls, dic, filename):
        """..."""
        if _os.path.exists(filename):
#            raise ValueError('File %s exists, will not overwrite.' % filename)
            with _nc4.Dataset(filename, 'r+', format=self.fmt) as ncfile:
                cls.__recursively_save_dict_contents_to_group__(ncfile, dic)
        else:
            with _nc4.Dataset(filename, 'w') as ncfile:
                cls.__recursively_save_dict_contents_to_group__(ncfile, dic)
        # end if

        try:
            ncfile.close()
        except:
            pass
        # end if