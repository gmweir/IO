# -*- coding: utf-8 -*-
"""
Created on Wed May 11 12:00:17 2022

@author: gawe
"""

# ========================================================================== #
# ========================================================================== #
from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals


import sys as _sys
import numpy as _np
# import os as _os

from time import gmtime as _gmtime
from time import strftime as _strftime

from pybaseutils.Struct import Struct as StructObj
from pybaseutils.utils import versiontuple  # analysis:ignore


__metaclass__ = type

# ========================================================================== #
# ========================================================================== #

# ispy3 = _sys.version_info.pyver > (3,)   # analysis:ignore
# ispy2 = _sys.version_info.pyver < (3,)   # analysis:ignore

class Struct(StructObj):
    """
    This is the custom structure class thatis used for data storage and
    fast conversion back and forth between dictionaries and objects.

    ex//

        d1 = {...}   # original dictionary

        dataObj = Struct(d1)   # data keys as variables: dataObj.key1 = val1

        d2 = dataObj.dict_from_class()
    """
    pass
# end class


class egDataFormat(Struct):
    """
    LHD style data format.  Useful for exchanging data in text format. See "egDataFormatIO"
    """


    def new(self, dimno=int(1), valno=int(1), dimsize=[int()]):
        """
        The 'new' function initializes the necessary variables to write an empty
        'LHD format' text file.  See 'writeHeader' for specifics of LHD Format.
        """
        self.Name = ''          # Name of the
        self.ShotNo = 0
        self.SubNo = 0
        self.Date = ''
        self.DimNo = int(dimno)
        self.DimSize = [int(_dim) for _dim in dimsize] # [list of ints], the number of dimensions of the data
        self.DimName=[str()]  # [str], a descriptive name of the dimensions
        self.DimUnit=[str()]  # [str], Units of data in each dimension

        n = int(_np.prod(self.DimSize))  # [int], the total length of the data from this Value after reshaping to a vector
        self.ValNo = int(valno)  # [int], the number of 'Values' saved (data sets)
        self.ValName=[str()]  # [list of str's], a descriptive name for each value saved in data
        self.ValUnit=[str()]  # [list of str's], the units of each value
        self.comments = [str()]  # [list of str's], any useful comments
        self.data = _np.zeros((n,valno))    # The data to be written (ex // datasets stored by column)
        # self.data = _np.zeros((n,dimno+valno))    # The data to be written (ex // datasets stored by column)
    # end def


    def copy(self, source):
        self.Name     = source.Name
        self.ShotNo   = source.ShotNo
        self.SubNo    = source.SubNo
        self.Date     = source.Date
        self.DimNo    = source.DimNo
        self.DimSize  = source.DimSize
        self.DimName  = source.DimName
        self.DimUnit  = source.DimUnit
        self.ValNo    = source.ValNo
        self.ValName  = source.ValName
        self.ValUnit  = source.ValUnit
        self.comments = source.comments
        self.data     = source.data
    # end def copy


    def getDimData(self, dimid=int(0)):
        """
        Returns a slice of the data corresponding to the proper dimension
        (reshaped to be the proper shape DimSize)
        """
        if self.DimNo > 7 :
             _sys.exit('egDataFormat support dimno < 8')
             _sys.exit(-1)
        # end if

        if self.DimNo == 1 :
            dim = self.data[:,dimid]
        elif self.DimNo == 2 :
            dim = self.data[:,dimid].reshape(self.DimSize[0],self.DimSize[1])
        elif self.DimNo == 3 :
            dim = self.data[:,dimid].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2])
        elif self.DimNo == 4 :
            dim = self.data[:,dimid].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2],self.DimSize[3])
        elif self.DimNo == 5 :
            dim = self.data[:,dimid].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2],self.DimSize[3],self.DimSize[4])
        elif self.DimNo == 6 :
            dim = self.data[:,dimid].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2],self.DimSize[3],self.DimSize[4],self.DimSize[5])
        elif self.DimNo == 7 :
            dim = self.data[:,dimid].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2],self.DimSize[3],self.DimSize[4],self.DimSize[5],self.DimSize[6])
        # end if
        return dim


    def getValData(self, valid=0):
        indx = self.DimNo + valid
        if self.DimNo > 7 :
            _sys.exit('egDataFormat support dimno < 8')
            _sys.exit(-1)
        # end if

        if self.DimNo == 1 :
            val = self.data[:,indx]
        elif self.DimNo == 2 :
            val = self.data[:,indx].reshape(self.DimSize[0],self.DimSize[1])
        elif self.DimNo == 3 :
            val = self.data[:,indx].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2])
        elif self.DimNo == 4 :
            val = self.data[:,indx].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2],self.DimSize[3])
        elif self.DimNo == 5 :
            val = self.data[:,indx].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2],self.DimSize[3],self.DimSize[4])
        elif self.DimNo == 6 :
            val = self.data[:,indx].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2],self.DimSize[3],self.DimSize[4],self.DimSize[5])
        elif self.DimNo == 7 :
            val = self.data[:,indx].reshape(self.DimSize[0],self.DimSize[1],self.DimSize[2],self.DimSize[3],self.DimSize[4],self.DimSize[5],self.DimSize[6])
        # end if
        return val


    def setDimData(self, data, dimid=0):
        n = _np.prod(self.DimSize)
        if self.DimNo == 1 :
            self.data[:,dimid] = data
        elif self.DimNo > 1 :
            self.data[:,dimid] = data.reshape(n)
        # end if


    def setValData(self, data, valid=0):
        indx = self.DimNo + int(valid)
        n = _np.prod(self.DimSize)
        if self.DimNo == 1 :
            self.data[:,indx] = data
        elif self.DimNo > 1 :
            self.data[:,indx] = data.reshape(n)
        # end if


    def convert1to2(self, source, ydata, yname="", yunit="", zname="", zunit=""):
        self.new(dimno=2, valno=1, dimsize=[source.DimSize[0],source.ValNo])
        self.Name     = source.Name
        self.ShotNo   = source.ShotNo
        self.SubNo    = source.SubNo
        self.Date     = _strftime("%m/%d/%Y %H:%M", _gmtime())
        self.DimName.append(source.DimName)
        self.DimName.append(yname)
        self.DimUnit.append(source.DimUnit)
        self.DimUnit.append(yunit)
        self.ValName.append(zname)
        self.ValUnit.append(zunit)
        self.comments = source.comments

        xx, yy = _np.meshgrid(source.data[:,0], ydata)
        self.data[:,0] = xx.reshape(_np.prod(self.DimSize),order='F')
        self.data[:,1] = yy.reshape(_np.prod(self.DimSize),order='F')
        self.data[:,2] = source.data[:,1:].reshape(_np.prod(self.DimSize))


    def convert2to1(self, source, idx=1, idz=[1]):
        idy = 2
        if idx == 2 :
            idy = 1
        # end if
        nx = source.DimSize[idx-1]
        ny = source.DimSize[idy-1]
        nz = len(idz)
        self.new(dimno=1, valno=ny*nz, dimsize=[nx])
        self.Name     = source.Name
        self.ShotNo   = source.ShotNo
        self.SubNo    = source.SubNo
        self.Date     = _strftime("%m/%d/%Y %H:%M", _gmtime())
        self.DimName  = [source.DimName[idx-1]]
        self.DimUnit  = [source.DimUnit[idx-1]]
        self.ValName  = []
        self.ValUnit  = []
        self.comments = source.comments
        if idx == 1 :
            xx = source.getDimData(dimid=idx-1)
            yy = source.getDimData(dimid=idy-1)
            for ii in range(nz):
                self.data[:,ii+1::nz] = source.getValData(valid=idz[ii]-1)
            # end for
        else :
            xx = source.getDimData(dimid=idx).transpose()
            yy = source.getDimData(dimid=idy).transpose()
            for ii in range(nz):
                self.data[:,ii+1::nz] = source.getValData(valid=idz[ii]-1).transpose()
            # end for
        # end if

        self.data[:,0] = xx[:,0]
        for j in range(ny):
            for ii in range(nz) :
                valname = source.ValName[idz[ii]-1] + "@%.6E" % yy[0,j] + "(%s)" % source.DimUnit[idy-1]
                self.ValName.append(valname)
                self.ValUnit.append(source.ValUnit[idz[ii]-1])
            # end for
        # end for

    def addLog(self):
        argvs = _sys.argv
        command = "%s " % _strftime("%B-%d-%Y %H:%M", _gmtime())
        for ii in range(len(argvs)):
            command = command + " " + argvs[ii]
        # end for
        self.comments.append("   ")
        self.comments.append(command)
# end def egDataFormat


# ======================================= #


def pretty(d, indent=4):
    print(' '*(indent-4)+'{')
    for key, value in d.items():
        if isinstance(value, dict):
            print(' '*indent + str(key))
            pretty(value, indent+4)
        else:
            print(' '*(indent) + f"{key}: {value}")
        # end if
    # end for
    print(' '*(indent-4)+'}')
# end def


def print_dict(my_dict, indent=4):
    try:
    # if 1:
        import pprint
        pp = pprint.PrettyPrinter(indent=indent)
        pp.pprint(my_dict)
    except ImportError:
    # else:
        try:
        # if 0:
            import json as _jsn
            print(_jsn.dumps(my_dict, sort_keys=True, indent=indent))
        # else:
        except (ImportError, TypeError):
            # Object of type int64 is not JSON serializable
            try:
            # if 1:
                pretty(my_dict, indent=indent)
            except:
            # else:
                print(my_dict)
            # end if
        # end try
    # end try
# end def



# ========================================================================== #
# ========================================================================== #


def test_dict():
    ex = {
        'name': 'GMW\xb0' + chr(255),   # 'GMW°ÿ'
        'exdict': {'str': 'new'},
        'age':  _np.int64(29),          # written t-minus 6-years ago
        "90's BoyBand?": '98\xb0',
        'unicode': 'The reäl öüt: \xb1!'+ chr(255),
        'tricky': None,
        'strarr': ['My','Name','is','the','Hoss'],
        'fav_numbers': _np.array([3,5,87]),
        'fav_tensors': {
            'levi_civita3d': _np.array([
                [[1,0,0],[0,0,-1],[0,-1,0]],
                [[0,0,0],[0,1,0],[1,0,-1]],
                [[0,0,0],[0,0,0],[0,0,1]]
            ]),
            'kronecker2d': _np.identity(3)
        },
        'dictarray': _np.array([{'a':1,'b':2}, {'soup':10,'weasel':-10}]),
        'strarray': _np.asarray(['w7x_ref_175', 'w7x_ref_175']),
        'nan': _np.nan,
        'nan_array': _np.nan*_np.ones( (5,1), dtype=_np.float64),
        'imaginary_numbers': _np.ones( (5,1), dtype=_np.float64)+ 1j*_np.random.normal(0.0, 1.0, (5,1)),
        'empty_array':_np.asarray([]),
        'empty_list':[],
#        'objectlist':[tst],
    }
    return ex


def test_Struct():

    ex1 = test_dict()

    # test dictionary conversion to object
    exObj = Struct(ex1)

    ex2 = exObj.dict_from_class()

    _np.testing.assert_equal(ex1, ex2)

    # test storage and access
    ex1['a'] = 0;     ex1['b'] = 1

    exObj.a = 0;      exObj.b = 1

    ex2 = exObj.dict_from_class()

    _np.testing.assert_equal(ex1, ex2)
# end def


# ======================================= #


def test_print_dict():
    ex = test_dict()
    print_dict(ex)
# end def


# ======================================= #


if __name__ == "__main__":
    test_Struct()
    test_print_dict()
# endif





# ========================================================================== #
# ========================================================================== #