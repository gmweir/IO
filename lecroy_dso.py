#! /usr/bin/env python
# coding: utf-8
import struct
import re
import numpy as np

class LecroyDSO():
   def __init__(self, filename=None):
      if filename is None :
         self.DESCRIPTION_NAME = ''
         self.TEMPLATE_NAME = ''
         self.COMM_TYPE = 0
         self.COMM_ORDER = 0
         self.WAVE_DESCRIPTOR = 0
         self.USER_TEXT = 0
         self.RES_DESC = 0
         self.TRIGTIME_ARRAY = 0
         self.RIS_TIME_ARRAY = 0
         self.RES_TIME_ARRAY = 0
         self.WAVE_ARRAY_1 = 0
         self.WAVE_ARRAY_2 = 0
         self.RES_ARRAY_2 = 0
         self.RES_ARRAY_3 = 0
         self.INSTRUMENT_NAME = ''
         self.INSTRUMENT_NUMBER = 0
         self.TRACE_LABEL = ''
         self.WAVE_ARRAY_COUNT = 0
         self.PNTS_PER_SCREEN = 0
         self.FIRST_VALID_PNT = 0
         self.LAST_VALID_PNT = 0 
         self.FIRST_POINT = 0
         self.SPARSING_FACTOR = 0
         self.SEGMENT_INDEX = 0
         self.SUBARRAY_COUNT = 0
         self.SWEEPS_PER_ACQ = 0
         self.POINTS_PER_PAIR = 0
         self.PAIR_OFFSET = 0
         self.VERTICAL_GAIN = 0.0
         self.VERTICAL_OFFSET = 0.0
         self.MAX_VALUE = 0.0
         self.MIN_VALUE = 0.0
         self.NOMINAL_BITS =0
         self.NOM_SUBARRAYT_COUNT = 0
         self.HORIZ_INTERVAL = 0.0
         self.HORIZ_OFFSET = 0.0
         self.PIXEL_OFFSET = 0.0
         self.fid = 0
         self.seek_offset = 0
      else:
         self.openFile(filename)

   def openFile(self, filename):
      self.fid = open(filename,'rb')
      temp = self.fid.read(11)            #Read up to 11th bit index.  This is where, 'WAVEDESC' starts
      self.seek_offset = 11
      if temp[1] == "A":
         temp = self.fid.read(1)
         self.seek_offset = self.seek_offset + 1
      bindata = self.fid.read(346)
      #Description
      self.DESCRIPTION_NAME = struct.unpack('16s',bindata[0:16])[0]
      self.TEMPLATE_NAME = struct.unpack('16s',bindata[16:16+16])[0]
      self.COMM_TYPE = struct.unpack('H',bindata[32:32+2])[0]
      self.COMM_ORDER = struct.unpack('H',bindata[34:34+2])[0]
      self.WAVE_DESCRIPTOR = struct.unpack('I',bindata[36:36+4])[0]
      self.USER_TEXT = struct.unpack('I',bindata[40:40+4])[0]
      self.RES_DESC = struct.unpack('I',bindata[44:44+4])[0]
      self.TRIGTIME_ARRAY = struct.unpack('I',bindata[48:48+4])[0]
      self.RIS_TIME_ARRAY = struct.unpack('I',bindata[52:52+4])[0]
      self.RES_TIME_ARRAY = struct.unpack('I',bindata[56:56+4])[0]
      self.WAVE_ARRAY_1 = struct.unpack('I',bindata[60:60+4])[0]
      self.WAVE_ARRAY_2 = struct.unpack('I',bindata[64:64+4])[0]
      self.RES_ARRAY_2 = struct.unpack('I',bindata[68:68+4])[0]
      self.RES_ARRAY_3 = struct.unpack('I',bindata[72:72+4])[0]
      self.INSTRUMENT_NAME = struct.unpack('16s',bindata[76:76+16])[0]
      self.INSTRUMENT_NUMBER = struct.unpack('I',bindata[92:92+4])[0]
      self.TRACE_LABEL = struct.unpack('16s',bindata[96:96+16])[0]
      self.WAVE_ARRAY_COUNT = struct.unpack('I',bindata[116:116+4])[0]
      self.PNTS_PER_SCREEN = struct.unpack('I',bindata[120:120+4])[0]
      self.FIRST_VALID_PNT = struct.unpack('I',bindata[124:124+4])[0]
      self.LAST_VALID_PNT = struct.unpack('I',bindata[128:128+4])[0]
      self.FIRST_POINT = struct.unpack('I',bindata[132:132+4])[0]
      self.SPARSING_FACTOR = struct.unpack('I',bindata[136:136+4])[0]
      self.SEGMENT_INDEX = struct.unpack('I',bindata[140:140+4])[0]
      self.SUBARRAY_COUNT = struct.unpack('I',bindata[144:144+4])[0]
      self.SWEEPS_PER_ACQ = struct.unpack('I',bindata[148:148+4])[0]
      self.POINTS_PER_PAIR = struct.unpack('H',bindata[152:152+2])[0]
      self.PAIR_OFFSET = struct.unpack('H',bindata[154:154+2])[0]
      self.VERTICAL_GAIN = struct.unpack('f',bindata[156:156+4])[0]
      self.VERTICAL_OFFSET = struct.unpack('f',bindata[160:160+4])[0]
      self.MAX_VALUE = struct.unpack('f',bindata[164:164+4])[0]
      self.MIN_VALUE = struct.unpack('f',bindata[168:168+4])[0]
      self.NOMINAL_BITS = struct.unpack('H',bindata[172:172+2])[0]
      self.NOM_SUBARRAYT_COUNT = struct.unpack('H',bindata[174:174+2])[0]
      self.HORIZ_INTERVAL = struct.unpack('f',bindata[176:176+4])[0]
      self.HORIZ_OFFSET = struct.unpack('d',bindata[180:180+8])[0]
      self.PIXEL_OFFSET = struct.unpack('d',bindata[188:188+8])[0]
      Wave_Pos = self.WAVE_DESCRIPTOR + self.USER_TEXT + self.RES_DESC + self.TRIGTIME_ARRAY + self.RIS_TIME_ARRAY + self.RES_TIME_ARRAY

      self.seek_offset = self.seek_offset + Wave_Pos
      self.DESCRIPTION_NAME = re.sub(chr(0), " ", self.DESCRIPTION_NAME)
      self.TEMPLATE_NAME  = re.sub(chr(0), " ",  self.TEMPLATE_NAME)
      self.INSTRUMENT_NAME = re.sub(chr(0), " ", self.INSTRUMENT_NAME)
      self.TRACE_LABEL = re.sub(chr(0), " ", self.TRACE_LABEL) 

      
   def writeInfo(self) :
      print("# DESCRIPTION_NAME = "+self.DESCRIPTION_NAME)
      print("# TEMPLATE_NAME = "+self.TEMPLATE_NAME)
      print("# COMM_TYPE = "+str(self.COMM_TYPE))
      print("# COMM_ORDER = "+str(self.COMM_ORDER))
      print("# WAVE_DESCRIPTOR = "+str(self.WAVE_DESCRIPTOR))
      print("# USER_TEXT = "+str(self.USER_TEXT))
      print("# RES_DESC = "+str(self.RES_DESC))
      print("# TRIGTIME_ARRAY = "+str(self.TRIGTIME_ARRAY))
      print("# RIS_TIME_ARRAY = "+str(self.RIS_TIME_ARRAY))
      print("# RES_TIME_ARRAY = "+str(self.RES_TIME_ARRAY))
      print("# WAVE_ARRAY_1 = "+str(self.WAVE_ARRAY_1))
      print("# WAVE_ARRAY_2 = "+str(self.WAVE_ARRAY_2))
      print("# RES_ARRAY_2 = "+str(self.RES_ARRAY_2))
      print("# RES_ARRAY_3 = "+str(self.RES_ARRAY_3))
      print("# INSTRUMENT_NAME = "+self.INSTRUMENT_NAME)
      print("# INSTRUMENT_NUMBER = "+str(self.INSTRUMENT_NUMBER))
      print("# TRACE_LABEL = "+self.TRACE_LABEL)
      print("# WAVE_ARRAY_COUNT = "+str(self.WAVE_ARRAY_COUNT))
      print("# PNTS_PER_SCREEN = "+str(self.PNTS_PER_SCREEN))
      print("# FIRST_VALID_PNT = "+str(self.FIRST_VALID_PNT))
      print("# LAST_VALID_PNT = "+str(self.LAST_VALID_PNT))
      print("# FIRST_POINT = "+str(self.FIRST_POINT))
      print("# SPARSING_FACTOR = "+str(self.SPARSING_FACTOR))
      print("# SEGMENT_INDEX = "+str(self.SEGMENT_INDEX))
      print("# SUBARRAY_COUNT = "+str(self.SUBARRAY_COUNT))
      print("# SWEEPS_PER_ACQ = "+str(self.SWEEPS_PER_ACQ))
      print("# POINTS_PER_PAIR = "+str(self.POINTS_PER_PAIR))
      print("# PAIR_OFFSET = "+str(self.PAIR_OFFSET))
      print("# VERTICAL_GAIN = "+str(self.VERTICAL_GAIN))
      print("# VERTICAL_OFFSET = "+str(self.VERTICAL_OFFSET))
      print("# MAX_VALUE = "+str(self.MAX_VALUE))
      print("# MIN_VALUE = "+str(self.MIN_VALUE))
      print("# NOMINAL_BITS = "+str(self.NOMINAL_BITS))
      print("# NOM_SUBARRAYT_COUNT = "+str(self.NOM_SUBARRAYT_COUNT))
      print("# HORIZ_INTERVAL = "+str(self.HORIZ_INTERVAL))
      print("# HORIZ_OFFSET = "+str(self.HORIZ_OFFSET))
      print("# PIXEL_OFFSET = "+str(self.PIXEL_OFFSET))

   def readFile(self, buffsize, data_offset=0):
      endpos = buffsize + data_offset
      if self.WAVE_ARRAY_COUNT >= endpos:
         ReadBuffSize = buffsize
      else :
         ReadBuffSize = self.WAVE_ARRAY_COUNT - data_offset
      data = np.zeros((ReadBuffSize,2), order='F')
      self.fid.seek(data_offset+self.seek_offset)
      if self.COMM_TYPE == 0:
         bindata = self.fid.read(ReadBuffSize)
         intd = struct.unpack(str(ReadBuffSize)+'b',bindata[0:ReadBuffSize])
      else:
         bindata = self.fid.read(ReadBuffSize*2)
         intd = struct.unpack(str(ReadBuffSize)+'h',bindata[0:ReadBuffSize*2])
      for i in range(len(intd)):
         data[i,1] = intd[i]*self.VERTICAL_GAIN - self.VERTICAL_OFFSET
         data[i,0] = (i+data_offset)*self.HORIZ_INTERVAL + self.HORIZ_OFFSET
      return data

   def closeFile(self):
      self.fid.close()

if __name__ == "__main__":
   import lecroy_dso as dso
   import numpy as np
   import sys

   file = "Reflectometer/C1BKGND57717.trc"
   fid = dso.LecroyDSO(file)
   fid.writeInfo()
   dat = fid.readFile(10000, data_offset=10)   
   np.savetxt(sys.stdout, dat, delimiter=", ", fmt='%.12E')
   fid.closeFile()
