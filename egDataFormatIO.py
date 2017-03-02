#!/usr/bin/env python
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals

__metaclass__ = type
    
# note on python 2 and python 3 compatability:
# in py2: print >> fp, s    prints string "s" to text file fp
# in py3: print(s, file=fp) ... print(s, end="\n", file=fp) (end="\n" default)

# -------------------------------------------------------------------------- #


from time import gmtime, strftime
import re
import sys
import numpy as _np
# from ..utils import Struct
from pybaseutils.utils import Struct

class egDataFormatIO(Struct):
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
         self.Name     = ''
         self.ShotNo   = 0
         self.SubNo    = 0
         self.Date     = ''
         self.DimNo    = 0
         self.DimSize  = []
         self.DimName  = []
         self.DimUnit  = []
         self.ValNo    = 0
         self.ValName  = []
         self.ValUnit  = []
         self.comments = []     
      else : 
         self.readFile(filename)    

   def new(self, dimno=1, valno=1, dimsize=[]):
      self.Name = ''
      self.ShotNo = 0
      self.SubNo = 0
      self.Date = ''
      self.DimNo = dimno
      self.DimSize = dimsize
      self.DimName=[]
      self.DimUnit=[]
      self.ValNo = valno
      n = _np.prod(self.DimSize)
      self.ValName=[]
      self.ValUnit=[]
      self.comments = []  
      self.data = _np.zeros((n,dimno+valno))

   def readFile(self, filename=None):
      self.readHeader(filename)
      self.readData(filename)
      
   def readData(self, filename=None):
      if filename is None :
         self.data = _np.loadtxt(sys.stdin, comments='#', delimiter=',')
      else :
         self.data = _np.loadtxt(filename, comments='#', delimiter=',')
    
   def readHeader(self, filename=None):
      parametersFlg = False
      commentsFlg = False
      reobjBlock = re.compile(r'\s*\[(.+)\]\s*')
      params=[]
      numcom = 0
      self.DimSize  = []
      self.DimName  = []
      self.DimUnit  = []
      self.ValName  = []
      self.ValUnit  = []
      self.comments = [] 
      if filename is None :
         for line in sys.stdin :
            if line[0] == "#":        
               matchblock = reobjBlock.match(line[1:])
               if matchblock:
                  key = matchblock.groups()[0].upper()
                  if 'PARAMETERS' == key:
                     parametersFlg = True
                     commentsFlg = False
                  if 'COMMENTS' == key:
                     parametersFlg = False
                     commentsFlg = True
                     line = '#'
                  if 'DATA' == key:
                     break
               if commentsFlg:
                  if numcom == 0 :
                     numcom = 1
                  else :
                     self.comments.append(line[1:].strip())
               if parametersFlg:
                  params.append(line[1:].strip())
            else:
               break
      else :
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
                  if 'COMMENTS' == key:
                     parametersFlg = False
                     commentsFlg = True
                     line = '#'
                  if 'DATA' == key:
                     break
               if commentsFlg:
                  if numcom == 0 :
                     numcom = 1
                  else:
                     self.comments.append(line[1:].strip())                 
               if parametersFlg:
                  params.append(line[1:].strip())
            else:
               break
         fp.close()
      self.parseLines(params)
      numcom = len(self.comments)
      for i in range(numcom-1,-1,-1) :
         if len(self.comments[i]) == 0 :
            self.comments.pop(i)
         else:
            break

   def parseLines(self, params):
      """
      parsing a line of headder and getting the size of the data.
      """

      reobjItem  = re.compile(r'(.+)\s*=\s*(.+)')
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
            if 'SHOTNO' == key:
               self.ShotNo = int(val)
            if 'SUBNO' == key:
               self.SubNo = int(val)
            if 'DATE' == key:
               clm = val.strip()
               clm = val.strip('\'')
               self.Date = clm
            if 'DIMNO' == key:
               self.DimNo = int(val)
            if 'DIMSIZE' == key:
               for i in range(self.DimNo):
                  clm = val.split(',')
                  self.DimSize.append(int(clm[i]))
            if 'DIMNAME' == key:
               for i in range(self.DimNo):
                  clm = val.split(',')
                  clmd = clm[i].strip()
                  clmd = clmd.strip('\'')
                  self.DimName.append(clmd)
            if 'DIMUNIT' == key:
               for i in range(self.DimNo):
                  clm = val.split(',')
                  clmd = clm[i].strip()
                  clmd = clmd.strip('\'')
                  self.DimUnit.append(clmd)
            if 'VALNO' == key:
               self.ValNo = int(val)
            if 'VALNAME' == key:
               for i in range(self.ValNo):
                  clm = val.split(',')
                  clmd = clm[i].strip()
                  clmd = clmd.strip('\'')
                  self.ValName.append(clmd)
            if 'VALUNIT' == key:
               for i in range(self.ValNo):
                  clm = val.split(',')
                  clmd = clm[i].strip()
                  clmd = clmd.strip('\'')
                  self.ValUnit.append(clmd)

   def writeFile(self, filename=None, filefmt='LHD', datafmt='%.6E'):
      if filefmt is 'LHD':
        self.writeHeader(filename)
      else :
        self.writeTitle(filename)
      self.writeData(filename, datafmt)

   def writeHeader(self, filename=None):
      self.Date = strftime("%m/%d/%Y %H:%M", gmtime())
      for i in range(self.DimNo):
         if i == 0:
            dimname = "'%s'" % self.DimName[i]
            dimsize = "%d" % self.DimSize[i]
            dimunit = "'%s'" % self.DimUnit[i]
         else:
            dimname = dimname + ", '%s'" % self.DimName[i]
            dimsize = dimsize + ", %d" % self.DimSize[i]
            dimunit = dimunit + ", '%s'" % self.DimUnit[i]

      for i in range(self.ValNo):
         if i == 0:
            valname = "'%s'" % self.ValName[i]
            valunit = "'%s'" % self.ValUnit[i]
         else:
            valname = valname + ", '%s'" % self.ValName[i]
            valunit = valunit + ", '%s'" % self.ValUnit[i]         

      if filename is None :
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

   def writeData(self, filename=None, datafmt='%.6E'):
      if filename is None :
         _np.savetxt(sys.stdout, self.data, delimiter=", ", fmt=datafmt)
      else :
         fp = open(filename, 'a')
         _np.savetxt(fp, self.data, delimiter=", ", fmt=datafmt)
         fp.close()

   def writeTitle(self, filename=None, datafmt='%.6E'):
      if len(self.DimUnit[0]) > 0 :
         for i in range(self.DimNo) :
            if i == 0:
               title = "%s(%s)" % (self.DimName[i], self.DimUnit[i])
            else:
               title = title + ", %s(%s)" % (self.DimName[i], self.DimUnit[i])
      else :
         for i in range(self.DimNo) :
            if i == 0:
               title = self.DimName[i]
            else:
               title = title + ", %s" % self.DimName[i]
      if len(self.ValUnit[0]) > 0 :
         for i in range(self.ValNo):
            title = title + ", %s(%s)" % (self.ValName[i], self.ValUnit[i])
      else :
         for i in range(self.ValNo):
            title = title + ", %s" % self.ValName[i]
      if filename is None :
         print(title)
      else :
         fp = open(filename, 'w')
         print(title, file=fp)
         fp.close()

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

   def getDimData(self,dimid=0):
      if self.DimNo > 7 :
         sys.exit('egDataFormatIO support dimno < 8') 
         sys.exit(-1)
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
      return dim

   def getValData(self,valid=0):
      indx = self.DimNo + valid
      if self.DimNo > 7 :
         sys.exit('egDataFormatIO support dimno < 8') 
         sys.exit(-1)
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
      return val

   def setDimData(self,data,dimid=0):
      n = _np.prod(self.DimSize)
      if self.DimNo == 1 :
         self.data[:,dimid] = data
      elif self.DimNo > 1 :
         self.data[:,dimid] = data.reshape(n) 

   def setValData(self,data,valid=0):
      indx = self.DimNo + valid
      n = _np.prod(self.DimSize)
      if self.DimNo == 1 :
         self.data[:,indx] = data
      elif self.DimNo > 1 :
         self.data[:,indx] = data.reshape(n) 

   def convert1to2(self, source, ydata, yname="", yunit="", zname="", zunit=""):
      self.new(dimno=2, valno=1, dimsize=[source.DimSize[0],source.ValNo])
      self.Name     = source.Name
      self.ShotNo   = source.ShotNo
      self.SubNo    = source.SubNo
      self.Date     = strftime("%m/%d/%Y %H:%M", gmtime())
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
      nx = source.DimSize[idx-1] 
      ny = source.DimSize[idy-1] 
      nz = len(idz)
      self.new(dimno=1, valno=ny*nz, dimsize=[nx])
      self.Name     = source.Name
      self.ShotNo   = source.ShotNo
      self.SubNo    = source.SubNo
      self.Date     = strftime("%m/%d/%Y %H:%M", gmtime())
      self.DimName  = [source.DimName[idx-1]]
      self.DimUnit  = [source.DimUnit[idx-1]]
      self.ValName  = []
      self.ValUnit  = []
      self.comments = source.comments
      if idx == 1 :
         xx = source.getDimData(dimid=idx-1)
         yy = source.getDimData(dimid=idy-1)
         for i in range(nz):
            self.data[:,i+1::nz] = source.getValData(valid=idz[i]-1)
      else :
         xx = source.getDimData(dimid=idx).transpose()
         yy = source.getDimData(dimid=idy).transpose()
         for i in range(nz):
            self.data[:,i+1::nz] = source.getValData(valid=idz[i]-1).transpose()

      self.data[:,0] = xx[:,0]
      for j in range(ny):
         for i in range(nz) :
            valname = source.ValName[idz[i]-1] + "@%.6E" % yy[0,j] + "(%s)" % source.DimUnit[idy-1]
            self.ValName.append(valname)
            self.ValUnit.append(source.ValUnit[idz[i]-1])

   def addLog(self):
      argvs = sys.argv 
      command = "%s " % strftime("%B-%d-%Y %H:%M", gmtime())
      for i in range(len(argvs)):
         command = command + " " + argvs[i]
      self.comments.append("   ")
      self.comments.append(command)


if __name__=="__main__":
    eg = egDataFormatIO()
    eg.writeFile('temp.dat')
