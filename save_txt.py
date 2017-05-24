# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 10:23:56 2016

@author: gawe
"""

import numpy as _np
import pybaseutils as _pyut
import os as _os

class txtdata(_pyut.Struct):
    """
    Class for saving data to a text file
    - sfilname - str - File name (one txt file) 
            OR - list - List of file names (multiple txt files) 
    - datain   - object - data structure
            OR - list - List of data structures (multiple txt files)
    """
    def __init__(self, sfilname=None, datain=None):
        self.sfilname = sfilname
        self.data = datain
        if (sfilname is not None) and (datain is not None):        
            self.__runsav__()
        # endif
    # end def __init__        

    def __runsav__(self):
        if isinstance(sfilname, list):
            self.nfils = len(sfilname)
            self.savmult(sfilname, datain)
        else:
            self.nfils = 1
            self.savall(sfilname, datain)
        # endif
    # end def __runsav__
            
#    def mkfil(self, sfil):
#        """
#        Make the text file that will hold data
#        input:
#            sfil - str - text file name
#        output:
#            hfil - handle - Handle to open text file
#        """            
#        
#        return hfil


    def savall(self, sfil, dat):
                
        _np.savetxt(sfil, dat)
        return 1
    # enddef openclose                

    if isinstance(var, str):
        fmt = '%s'
    elif isinstance(var, float):
        fmt = '%f'
    elif isinstance(var, int):
        fmt = '%i'
    elif isinstance(var, )
# end class txtdata()