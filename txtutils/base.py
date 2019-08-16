# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 21:36:05 2019

@author: gawe
"""
# ===================================================================== #
# ===================================================================== #


from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals
import sys

__metaclass__ = type


# ===================================================================== #
# ===================================================================== #


def ftell(fid):
    """
        A python function that mimics ftell from MATLAB
            returns the current file position
    """
    return fid.tell()


def fseek(fid, offset, origin='currentposition'):
    """
        A python function that mimics fseek from MATLAB
            sets the current file position
    inputs:
        fid    - file object identifier
        offset - integer number of bytes to move the current file position
        origin - reference from where to offset the file position

    In text files only seeks relative to the beginning of the file are allowed
    (except for seeking to the very end of the file with seek(0, 2))

    The only valid offset values are those returned from fid.tell or 0
    """
    if type(origin) == type(''):
        if origin.lower().find('currentposition')>-1:   # default
            origin = 1
        elif origin.lower().find('start-of-file')>-1:
            origin = 0
        elif origin.lower().find('end-of-file')>-1:
            origin = 2
        # end if
    # end if
    return fid.seek(offset, origin)


def frewind(fid):
    return fseek(fid, 0, 'start-of-file')


def fgets(fid):
    """
        A python function that mimics fgets from MATLAB
            returns the next line of a file while including the new line character
    """
    return fid.readline()


def fgetl(fid):
    """
        A python function that mimics fgetl from MATLAB
            returns the next line of a file while stripping the new line character
    """
    return fgets(fid).replace('\n','')

# ===================================================================== #


def findstr(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

# ===================================================================== #
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
# end def getv2

# ========================================================================== #


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



# ========================================================================== #
# ========================================================================== #







# ========================================================================== #
# ========================================================================== #
