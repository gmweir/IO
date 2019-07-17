# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 10:23:56 2016

@author: gawe
"""

# ===================================================================== #
# ===================================================================== #


from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals
import sys

__metaclass__ = type


#import numpy as _np
#import pybaseutils as _pyut
#import os as _os


# ===================================================================== #

def getv(s=''):
    """
    Read 1 number/line using eval() from <stdin> or 'file' if specified.
    If the first non-whitespace is not valid number characters
    '(+-.0123456789', then the line will be skipped.
    """
    try:
        if s == '':
            fid = sys.stdin
        else:
            fid = open(s, 'r')
        # end if

        x = []
        for a in fid:
            a = a.strip()
            if a != '' and a[0] in '(+-.0123456789':
                x.append(eval(a))
            # end if
        # end for
    except:
        raise
    finally:
        try: fid.close()
        except: pass
    # end try
    return x
# end def getv

def getv2(s=''):
    """
    Read 2 numbers/line using eval() from <stdin> or 'file' if specified.
    If the first non-whitespace is not valid number characters
    '(+-.0123456789', then the line will be skipped.
    """
    try:
        if s == '':
            fid = sys.stdin
        else:
            fid = open(s, 'r')
        # end if
        x, y = [], []
        for a in fid:
            a = a.strip()
            if a != '' and a[0] in '(+-.0123456789':
                b = a.split()
                x.append(eval(b[0]))
                y.append(eval(b[1]))
            # end if
        # end for
    except:
        raise
    finally:
        try: fid.close()
        except: pass
    # end try
    return x, y
# end def getv2# ========================================================================== #


def printv(x, s=''):
    """
    Write 1 number/line to <stdout> or 'file' if specified.
    """
    out = ''
    for a in x:
        out += repr(a) + '\n'
    if s == '':
        sys.stdout.write(out)
    else:
        try:
            fid = open(s, 'w')
            fid.write(out)
        except:
            raise
        finally:
            fid.close()
        # end try
    # end if

# end def printv


# ========================================================================== #
# ========================================================================== #




#class txtdata(_pyut.Struct):
#    """
#    Class for saving data to a text file
#    - sfilname - str - File name (one txt file)
#            OR - list - List of file names (multiple txt files)
#    - datain   - object - data structure
#            OR - list - List of data structures (multiple txt files)
#    """
#    def __init__(self, sfilname=None, datain=None):
#        self.sfilname = sfilname
#        self.data = datain
#        if (sfilname is not None) and (datain is not None):
#            self.__runsav__()
#        # endif
#    # end def __init__
#
#    def __runsav__(self):
#        if isinstance(sfilname, list):
#            self.nfils = len(sfilname)
#            self.savmult(sfilname, datain)
#        else:
#            self.nfils = 1
#            self.savall(sfilname, datain)
#        # endif
#    # end def __runsav__
#
##    def mkfil(self, sfil):
##        """
##        Make the text file that will hold data
##        input:
##            sfil - str - text file name
##        output:
##            hfil - handle - Handle to open text file
##        """
##
##        return hfil
#
#
#    def savall(self, sfil, dat):
#
#        _np.savetxt(sfil, dat)
#        return 1
#    # enddef openclose
#
#    if isinstance(var, str):
#        fmt = '%s'
#    elif isinstance(var, float):
#        fmt = '%f'
#    elif isinstance(var, int):
#        fmt = '%i'
#    elif isinstance(var, )
## end class txtdata()