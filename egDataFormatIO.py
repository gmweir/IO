#!/usr/bin/env python
# ======================================================================== #
# ======================================================================== #

from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals

__metaclass__ = type

# note on python 2 and python 3 compatability:
# in py2: print >> fp, s     prints string "s" to text file fp
# in py3: print(s, file=fp) ... print(s, end="\n", file=fp) (end="\n" default)

# ======================================================================== #


from time import gmtime as _gmtime
from time import strftime as _strftime
import re as _re
import sys as _sys
import numpy as _np
import os as _os


try:
    from IO.utils import egDataFormat
except:
    from .utils import egDataFormat
# end try


class egDataFormatIO(egDataFormat):
    """
    egDataFormatIO() is pure python module for parsing eg data-format file.

    if you want to open 'temp.dat', make instance of the file with edgb(),
    and then call readFile() method.
    ex)
        eg = egDataFormatIO('temp.dat')
         or
        eg = egDataFormatIO()
        eg.readFile('temp.dat')
    """


    def __init__(self, filename=None):
        if filename is None :
            self.new()
        else :
            self.readFile(filename)
    # end __init__


    def readFile(self, filename=None):
        self.readHeader(filename)
        self.readData(filename)

    def readData(self, filename=None):
        if filename is None :
            self.data = _np.loadtxt(_sys.stdin, comments='#', delimiter=',')
        else :
            self.data = _np.loadtxt(filename, comments='#', delimiter=',')

    def readHeader(self, filename=None):
        parametersFlg = False
        commentsFlg = False
        reobjBlock = _re.compile(r'\s*\[(.+)\]\s*')
        params=[]
        numcom = 0
        self.DimSize  = []
        self.DimName  = []
        self.DimUnit  = []
        self.ValName  = []
        self.ValUnit  = []
        self.comments = []

        if filename is None :
            """
            read from stdin (command line input)
            """
            for line in _sys.stdin :
                if line[0] == "#":
                    matchblock = reobjBlock.match(line[1:])
                    if matchblock:
                        key = matchblock.groups()[0].upper()
                        if 'PARAMETERS' == key:
                            parametersFlg = True
                            commentsFlg = False
                        elif 'COMMENTS' == key:
                            parametersFlg = False
                            commentsFlg = True
                            line = '#'
                        elif 'DATA' == key:
                            break
                        # end if
                    # end if matchblock

                    if commentsFlg:
                        if numcom == 0 :
                            numcom = 1
                        else :
                            self.comments.append(line[1:].strip())
                        # end if
                    # end if commentsFlg

                    if parametersFlg:
                        params.append(line[1:].strip())
                    # end if parametersFlg
                else:
                    break
                # end if line[0] == "#"
            # end for line in _sys.stdin (reading from command input)
        else :  # filename is not None
            """
            read from textfile
            """
            try:
                with open(filename, 'r') as fp:
                    while 1:
                        line = fp.readline()
                        if line[0] == "#":
                            matchblock = reobjBlock.match(line[1:])
                            if matchblock:
                                key = matchblock.groups()[0].upper()
                                if 'PARAMETERS' == key:
                                    parametersFlg = True
                                    commentsFlg = False
                                elif 'COMMENTS' == key:
                                    parametersFlg = False
                                    commentsFlg = True
                                    line = '#'
                                elif 'DATA' == key:
                                    break
                                # end if
                            # end if matchblock

                            if commentsFlg:
                                if numcom == 0 :
                                    numcom = 1
                                else:
                                    self.comments.append(line[1:].strip())
                                # end if
                            # end if commentsFlg

                            if parametersFlg:
                                params.append(line[1:].strip())
                            # end if parametersFlg
                        else:
                            break
                        # end if line[0] == "#"
                    # end while
                # end with open filename
            except:
                # probably in python2 ... the future import with_open should fix this
                fp = open(filename, 'r')
                while 1:
                    line = fp.readline()
                    if line[0] == "#":
                        matchblock = reobjBlock.match(line[1:])
                        if matchblock:
                            key = matchblock.groups()[0].upper()
                            if 'PARAMETERS' == key:
                                parametersFlg = True
                                commentsFlg = False
                            elif 'COMMENTS' == key:
                                parametersFlg = False
                                commentsFlg = True
                                line = '#'
                            elif 'DATA' == key:
                                break
                            # end if
                        # end if matchblock

                        if commentsFlg:
                            if numcom == 0 :
                                numcom = 1
                            else:
                                self.comments.append(line[1:].strip())
                            # end if
                        # end if commentsFlg

                        if parametersFlg:
                            params.append(line[1:].strip())
                        # end if parametersFlg
                    else:
                        break
                    # end if line[0] == "#"
                # end while loop
                fp.close()
            finally:
                try: fp.close()
                except: pass
            # end try
        # end if filename

        self.parseLines(params)
        numcom = len(self.comments)
        for ii in range(numcom-1,-1,-1) :
            if len(self.comments[ii]) == 0 :
                self.comments.pop(ii)
            else:
                break
            # end if
        # end for
    # end def readHeader


    def parseLines(self, params):
        """
        parsing a line of headder and getting the size of the data.
        """

        reobjItem  = _re.compile(r'(.+)\s*=\s*(.+)')
        for line in params:
            matchitem = reobjItem.match(line)
            if matchitem:
                key = matchitem.groups()[0].upper()
                key = key.strip()
                val = matchitem.groups()[1]
                if 'NAME' == key:
                    clm = val.strip()
                    clm = val.strip('\'')
                    self.Name = clm
                elif 'SHOTNO' == key:
                    self.ShotNo = int(val)
                elif 'SUBNO' == key:
                    self.SubNo = int(val)
                elif 'DATE' == key:
                    clm = val.strip()
                    clm = val.strip('\'')
                    self.Date = clm
                elif 'DIMNO' == key:
                    self.DimNo = int(val)
                elif 'DIMSIZE' == key:
                    for ii in range(self.DimNo):
                        clm = val.split(',')
                        self.DimSize.append(int(clm[ii]))
                    # end for
                elif 'DIMNAME' == key:
                    for ii in range(self.DimNo):
                        clm = val.split(',')
                        clmd = clm[ii].strip()
                        clmd = clmd.strip('\'')
                        self.DimName.append(clmd)
                    # end for
                elif 'DIMUNIT' == key:
                    for ii in range(self.DimNo):
                        clm = val.split(',')
                        clmd = clm[ii].strip()
                        clmd = clmd.strip('\'')
                        self.DimUnit.append(clmd)
                    # end for
                elif 'VALNO' == key:
                    self.ValNo = int(val)
                elif 'VALNAME' == key:
                    for ii in range(self.ValNo):
                        clm = val.split(',')
                        clmd = clm[ii].strip()
                        clmd = clmd.strip('\'')
                        self.ValName.append(clmd)
                    # end for
                elif 'VALUNIT' == key:
                    for ii in range(self.ValNo):
                        clm = val.split(',')
                        clmd = clm[ii].strip()
                        clmd = clmd.strip('\'')
                        self.ValUnit.append(clmd)
                    # end for
                # end if key is ____
            # end if matchitem
        # end for line in params
    # end def parseLines


    def writeFile(self, filename=None, filefmt='LHD', datafmt='%.6E'):
        if filefmt == 'LHD':
            self.writeHeader(filename)
        else :
            self.writeTitle(filename)
        # end if
        self.comments.append('filename = %s (written by egDataFormatIO)'%(filename,))
        self.writeData(filename, datafmt)
    # end def writeFile


    def writeHeader(self, filename=None):
        self.Date = _strftime("%m/%d/%Y %H:%M", _gmtime())
        for ii in range(self.DimNo):
            if ii == 0:
                dimname = "'%s'" % self.DimName[ii]
                dimsize = "%d" % self.DimSize[ii]
                dimunit = "'%s'" % self.DimUnit[ii]
            else:
                dimname = dimname + ", '%s'" % self.DimName[ii]
                dimsize = dimsize + ", %d" % self.DimSize[ii]
                dimunit = dimunit + ", '%s'" % self.DimUnit[ii]
            # end if
        # end for range dimensions

        for ii in range(self.ValNo):
            if ii == 0:
                valname = "'%s'" % self.ValName[ii]
                valunit = "'%s'" % self.ValUnit[ii]
            else:
                valname = valname + ", '%s'" % self.ValName[ii]
                valunit = valunit + ", '%s'" % self.ValUnit[ii]
            # end if
        # end for in range value number

        if filename is None :
            """printing to stdout"""
            print("# [Parameters]")
            print("# Name = '%s'" % self.Name)
            print("# ShotNo = %d" % self.ShotNo)
            print("# SubNo = %d" % self.SubNo)
            print("# Date = '%s'" % self.Date)
            print("#")
            print("# DimNo = %d" % self.DimNo)
            print("# DimName = %s" % dimname)
            print("# DimSize = %s" % dimsize)
            print("# DimUnit = %s" % dimunit)
            print("#")
            print("# ValNo = %d" % self.ValNo)
            print("# ValName = %s" % valname)
            print("# ValUnit = %s" % valunit)
            print("#")
            print("# [Comments]")
            for line in self.comments :
                print("# %s" % line)
            print("#")
            print("# [Data]" )
        else:
            """ printting into a file """
            try:
                with open(filename, 'w') as fp:
                    print("# [Parameters]", file=fp)
                    print("# Name = '%s'" % self.Name, file=fp)
                    print("# ShotNo = %d" % self.ShotNo, file=fp)
                    print("# SubNo = %d" % self.SubNo, file=fp)
                    print("# Date = '%s'" % self.Date, file=fp)
                    print("#", file=fp)
                    print("# DimNo = %d" % self.DimNo, file=fp)
                    print("# DimName = %s" % dimname, file=fp)
                    print("# DimSize = %s" % dimsize, file=fp)
                    print("# DimUnit = %s" % dimunit, file=fp)
                    print("#", file=fp)
                    print("# ValNo = %d" % self.ValNo, file=fp)
                    print("# ValName = %s" % valname, file=fp)
                    print("# ValUnit = %s" % valunit, file=fp)
                    print("#", file=fp)
                    print("# [Comments]", file=fp)
                    for line in self.comments :
                        print("# %s" % line, file=fp)
                    print("# filename = %s (written by egDataFormatIO)" % filename, file=fp)
                    print("#", file=fp)
                    print("# [Data]", file=fp)
                # end with open filename
            except:
                """ python2: when the with_statement fails """
                fp = open(filename, 'w')
                print("# [Parameters]", file=fp)
                print("# Name = '%s'" % self.Name, file=fp)
                print("# ShotNo = %d" % self.ShotNo, file=fp)
                print("# SubNo = %d" % self.SubNo, file=fp)
                print("# Date = '%s'" % self.Date, file=fp)
                print("#", file=fp)
                print("# DimNo = %d" % self.DimNo, file=fp)
                print("# DimName = %s" % dimname, file=fp)
                print("# DimSize = %s" % dimsize, file=fp)
                print("# DimUnit = %s" % dimunit, file=fp)
                print("#", file=fp)
                print("# ValNo = %d" % self.ValNo, file=fp)
                print("# ValName = %s" % valname, file=fp)
                print("# ValUnit = %s" % valunit, file=fp)
                print("#", file=fp)
                print("# [Comments]", file=fp)
                for line in self.comments :
                    print("# %s" % line, file=fp)
                print("# filename = %s (written by egDataFormatIO)" % filename, file=fp)
                print("#", file=fp)
                print("# [Data]", file=fp)
                fp.close()
            finally:
                try: fp.close()
                except: pass
            # end try
        # end if filename
    # end def writeHeader


    def writeData(self, filename=None, datafmt='%.6E'):
        if filename is None :
            _np.savetxt(_sys.stdout, self.data, delimiter=", ", fmt=datafmt)
        else :
            try:
                with open(filename, 'a') as fp:
                    _np.savetxt(fp, self.data, delimiter=", ", fmt=datafmt)
                # end with
            except:
                fp = open(filename, 'a')
                _np.savetxt(fp, self.data, delimiter=", ", fmt=datafmt)
                fp.close()
            finally:
                try: fp.close()
                except: pass
            # end try
        # end if
    # end def


    def writeTitle(self, filename=None, datafmt='%.6E'):
        if len(self.DimUnit[0]) > 0 :
            for ii in range(self.DimNo) :
                if ii == 0:
                    title = "%s(%s)" % (self.DimName[ii], self.DimUnit[ii])
                else:
                    title = title + ", %s(%s)" % (self.DimName[ii], self.DimUnit[ii])
                # end if
            # end for
        else :
            for ii in range(self.DimNo) :
                if ii == 0:
                    title = self.DimName[ii]
                else:
                    title = title + ", %s" % self.DimName[ii]
                # end if
            # end for
        # end if

        if len(self.ValUnit[0]) > 0 :
            for ii in range(self.ValNo):
                title = title + ", %s(%s)" % (self.ValName[ii], self.ValUnit[ii])
            # end for
        else :
            for ii in range(self.ValNo):
                title = title + ", %s" % self.ValName[ii]
            # end for
        # end if

        if filename is None :
            print(title)
        else :
            try:
                with open(filename, 'w') as fp:
                    print(title, file=fp)
                # end with
            except:
                fp = open(filename, 'w')
                print(title, file=fp)
                fp.close()
            finally:
                try: fp.close()
                except: pass
            # end try
        # end if
    # end def writeTitle
# end def egDataFormatIO

def test_egFormatIO():
    # Initialize the object
    eg = egDataFormatIO()

    # test data for 3 sets of 2D data: each with 16 chanenls and 1000 data points
    eg.new(dimno=2, valno=3, dimsize = [16, 1e3])

    # Set the Header information as well
    eg.Name = 'test_data'
    eg.ShotNo = 0
    eg.SubNo = 0
    eg.DimName = ['channels', 'time']
    eg.DimUnit = ['-', 's']
    eg.ValName = ['ECE1', 'ECE2', 'ECE3']
    eg.ValUnit = ['KeV', 'KeV', 'KeV']
    eg.comments = ['test file for egDataFormatIO']

    tt = _np.asarray(range(int(1e3)), dtype=_np.float64)/1e6
    ECE1 = (_np.ones((16,1), dtype=_np.float64)
            * _np.atleast_2d(_np.asarray(range(int(1e3)), dtype=_np.float64)))
    ECE2 = _np.copy(ECE1) + 16
    ECE3 = _np.copy(ECE2) + 32

    eg.setValData(ECE1, 0)
    eg.setValData(ECE2, 1)
    eg.setValData(ECE3, 2)

    # write to stdout (commandline)
    eg.writeFile()

    # write to local temporary data file:
    fil = _os.path.join(_os.path.dirname(__file__),
                        'TESTS', 'data', 'temp.dat')
    eg.writeFile(fil)

    tst = egDataFormatIO(fil)
    _np.testing.assert_equal(eg.dict_from_class(), tst.dict_from_class())
# end def test_

if __name__=="__main__":
    test_egFormatIO()
# end if


