#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 10:03:26 2017

@author: weir

This is a MATLAB port
"""

from numpy import arange, array
import warnings

try:
    from debug_ import debug_
except:
    from warnings import warn
    def debug_(debug, msg='', *args, **kwargs):
        if str(debug) != '0': warn('attempt to debug ' + msg +
              " need boyd's debug_.py to debug most effectively")

debug=1

# the correspondence will depend on the c-compiler definitions
# see http://docs.python.org/library/array.html
typedict = {'int32':'i', 'char':'c', 'float32':'f', 'double':'d', 'int16':'h'}
typedict.update({'uint32': 'I', 'uint16':'H', 'uint8':'B'})

def fread(file, num, typ):
    """ Imitate the matlab fread function -
        typ is 'f' for 4 byte float, 'c', i for 2 byte? 'l' for 4 byte?
    """
    from array import array as arr
    if len(typ)>1:
        typ = typedict[typ]

    ar =arr(typ)
    ar.fromfile(file, num)
    if typ == 'c':
        return(''.join(ar.tolist()))
    elif num == 1:
        return(ar[0])
    else:
        return(ar)

def myseek(fileHandle,bytesLeft,mode,debug=1):
    """ this was misbehaving - probably because it was not marked as binary
    OK now
    """
    action = ['seeking to', 'skipping']
    if bytesLeft!=0:
        if debug>0: print('%s %d bytes' % (action[mode], bytesLeft))
        if debug>3:
            import pdb; pdb.set_trace()
            'debugging seek, c to continue'
        fileHandle.seek(bytesLeft,mode)

def importAgilentBin(inputFile, varargin = None, debug = 1):
    """ ImportAgilentBin reads the Agilent Binary Waveform filetype.
    [timeVector, voltageVectordict] = importAgilentBin(inputFilename)
    [timeVector, voltageVectordict] = importAgilentBin(inputFilename, waveform_index)
    if waveformIndex is not provided, the first waveform will be read
    voltageVector may contain two columns [MIN, MAX]



    """

    if type(inputFile) == type(""):
        fileHandle = open(inputFile,'rb')
    else:
        fileHandle = inputFile

    # read file header
    fileCookie = fread(fileHandle, 2, 'char');
    fileVersion = fread(fileHandle, 2, 'char');
    fileSize = fread(fileHandle, 1, 'int32');
    nWaveforms = fread(fileHandle, 1, 'int32');

    # verify cookie
    # fileCookie = char(fileCookie);
    if (fileCookie != 'AG'):
        fileHandle.close()
        raise ValueError('Unrecognized file format.');

    # determine which waveform to read
    waveformSelect = [1];
    if (varargin != None and max(varargin[0]) <= nWaveforms):
        waveformSelect = varargin[0];

    voltageVector = {}
    timelen = None
    for waveformIndex in range(1,nWaveforms+1):
        # read waveform header
        headerSize = fread(fileHandle, 1, 'int32'); bytesLeft = headerSize - 4;
        waveformType = fread(fileHandle, 1, 'int32'); bytesLeft = bytesLeft - 4;
        nWaveformBuffers = fread(fileHandle, 1, 'int32'); bytesLeft = bytesLeft - 4;
        nPoints = fread(fileHandle, 1, 'int32'); bytesLeft = bytesLeft - 4;
        count = fread(fileHandle, 1, 'int32');  bytesLeft = bytesLeft - 4;
        xDisplayRange = fread(fileHandle, 1, 'float32');  bytesLeft = bytesLeft - 4;
        xDisplayOrigin = fread(fileHandle, 1, 'double');  bytesLeft = bytesLeft - 8;
        xIncrement = fread(fileHandle, 1, 'double');  bytesLeft = bytesLeft - 8;
        xOrigin = fread(fileHandle, 1, 'double');  bytesLeft = bytesLeft - 8;
        xUnits = fread(fileHandle, 1, 'int32');  bytesLeft = bytesLeft - 4;
        yUnits = fread(fileHandle, 1, 'int32');  bytesLeft = bytesLeft - 4;
        dateString = fread(fileHandle, 16, 'char'); bytesLeft = bytesLeft - 16;
        timeString = fread(fileHandle, 16, 'char'); bytesLeft = bytesLeft - 16;
        frameString = fread(fileHandle, 24, 'char'); bytesLeft = bytesLeft - 24;
        waveformString = fread(fileHandle, 16, 'char'); bytesLeft = bytesLeft - 16;
        timeTag = fread(fileHandle, 1, 'double'); bytesLeft = bytesLeft - 8;
        segmentIndex = fread(fileHandle, 1, 'uint32'); bytesLeft = bytesLeft - 4;

        if debug>0:
            print(waveformSelect, varargin)
            print('Waveform %d, nWaveformBuffers %d, wfstring=%s, headerSize = %d, bytesLeft = %d' %
                  (waveformIndex,nWaveformBuffers,waveformString, headerSize, bytesLeft))
            print("count={0}, nPoints={1}".format(count, nPoints))
        # skip over any remaining data in the header
        if debug>3:
            import pdb; pdb.set_trace()
            'debugging, c to continue'

        myseek(fileHandle,bytesLeft,1)

    # generate time vector from xIncrement and xOrigin values
        if (waveformIndex in waveformSelect):
            timeVector = (xIncrement * arange(nPoints)) + xOrigin;
            if timelen != None:
                if timelen!=len(timeVector):
                    print('** Warning: unequal trace lengths {0} != {1} **'.
                          format(timelen,len(timeVector)))
            timelen = len(timeVector)

        for bufferIndex in range(nWaveformBuffers):
            # read waveform buffer header
            headerSize = fread(fileHandle, 1, 'int32'); bytesLeft = headerSize - 4;
            bufferType = fread(fileHandle, 1, 'int16'); bytesLeft = bytesLeft - 2;
            bytesPerPoint = fread(fileHandle, 1, 'int16'); bytesLeft = bytesLeft - 2;
            bufferSize = fread(fileHandle, 1, 'int32'); bytesLeft = bytesLeft - 4;

            # skip over any remaining data in the header
            myseek(fileHandle,bytesLeft,1)

            if debug>2:
                import pdb; pdb.set_trace()
                'debugging, c to continue'

            if (waveformIndex in waveformSelect):
                if bufferIndex>1: warnings.warn('bufferIndex>1')
                if debug>2:
                    import pdb; pdb.set_trace()
                    'debugging, c to continue'

                if ((bufferType == 1) | (bufferType == 2) | (bufferType == 3)):
                    # use a dictionary to simulate what appear to be matlab pointers.
                    # but maybe there is something tricky relating to do with multiple buffers?
                    # bufferType is PB_DATA_NORMAL, PB_DATA_MIN, or PB_DATA_MAX (float)
#                    voltageVector[:, bufferIndex] = fread(fileHandle, nPoints, 'float');
                    voltageVector.update({waveformIndex: array(fread(fileHandle, nPoints, 'float32'))})
                elif (bufferType == 4):
                    # bufferType is PB_DATA_COUNTS (int32)  bdb was *int32
                    voltageVector.update({waveformIndex: array(fread(fileHandle, nPoints, 'int32'))})
                elif (bufferType == 5):
                    # bufferType is PB_DATA_LOGIC (int8)  bdb was *uint8
                    voltageVector.update({waveformIndex: array(fread(fileHandle, nPoints, 'uint8'))})
                else:
                    # unrecognized bufferType read as unformatted bytes was *unit8
                    #voltageVector[:, waveformIndex] = fread(fileHandle, bufferSize, 'uint8');
                    voltageVector.update({waveformIndex: array(fread(fileHandle, bufferSize, 'uint8'))})
            else:
                myseek(fileHandle,bufferSize,1)



    fileHandle.close();
    return(timeVector,voltageVector)


