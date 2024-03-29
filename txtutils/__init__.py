# -*- coding: utf-8 -*-
"""
    Mimicing scanf and sscanf from the standard c-library

     first try to use the standard c library implementation of sscanf
      ... if the library can't be found, use a small pure python implementation

@author:
    Gavin Weir <gavin.weir@ipp.mpg.de>
 """

# ======================================================================== #
# ======================================================================== #

from __future__ import absolute_import, with_statement, \
                       division, print_function, unicode_literals

__version__ = "2022.05.11.14"

from . import base   # analysis:ignore
from .base import ftell, fseek, frewind, fgets, fgetl, findstr   # analysis:ignore

try:
    #     The functions in this try block requires the standard C library
    #        full power c!
    from . import clib_sscanf   # analysis:ignore
    from .clib_sscanf import scanf, sscanf, fscanf   # analysis:ignore
except:
    # No c-library found on path

    try:
        # use a tiny pure python implementation with pure python
        #    this one uses regular expressions
        from . import mini_sscanf   # analysis:ignore
        from .mini_sscanf import scanf, sscanf, fscanf   # analysis:ignore
    except:
        # pure python version is a bit faster than the matlab-like inmplementation

        try:
            # use the MATLAB like implementation
            from . import matlab_sscanf   # analysis:ignore
            from .matlab_sscanf import scanf, sscanf, fscanf   # analysis:ignore

        except:
            # use a buggy pure python implementation with pure python
            #
            from . import buggy_sscanf   # analysis:ignore
            from .buggy_sscanf import scanf, sscanf, fscanf   # analysis:ignore
        # end try
    # end try
# end try:


# ======================================================================== #
# ======================================================================== #


