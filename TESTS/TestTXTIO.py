# -*- coding: utf-8 -*-
"""
Created on Tue May 23 18:30:52 2017

@author: gawe
"""
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals

# Unit Testing!
import unittest

# Functions to be tested
from IO.lhd_io import egDataFormatIO

# Required for tests
import numpy as _np
import os as _os

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

class TestTXTIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
#        cls.filname = 'temp.dat'
#        cls.data = _np.zeros( (1, 2), dtype=float)

#        {
#            'name': 'GMW\xb0' + chr(255),
#            'exdict': {'str': 'new'},
#            'age':  _np.int64(29),
#            "90's BoyBand?": '98\xb0',
#            'unicode': 'The reäl öüt: \xb1!'+ chr(255),
#            'tricky': None,
#            'strarr': ['My','Name','is','the','Hoss'],
#            'fav_numbers': _np.array([3,5,87]),
#            'fav_tensors': {
#                'levi_civita3d': _np.array([
#                    [[1,0,0],[0,0,-1],[0,-1,0]],
#                    [[0,0,0],[0,1,0],[1,0,-1]],
#                    [[0,0,0],[0,0,0],[0,0,1]]
#                ]),
#                'kronecker2d': _np.identity(3)  },
#            'dictarray': _np.array([{'a':1,'b':2}, {'soup':10,'weasel':-10}])
#                }
#        # print('ex')
#
#        cls.filename = 'temp_TestH5PY.hdf5'
#        if _os.path.exists(cls.filename):
#            _os.remove(cls.filename)
#        # endif
#
#        ReportInterface.__save_dict_to_hdf5__(cls.ex, cls.filename)
    # end def setupClass

    @classmethod
    def tearDownClass(cls):
        _os.remove(cls.filename)
    # end def tearDownClass

    # ==================== #

    def testWriteAnEmptyLHDfmtFile(self):
        """
        First verify that the module can create a temporary data file, and
        that it does so

        """
        eg = egDataFormatIO()
        filename = 'temp.dat'
        eg.writeFile(filename, filefmt='LHD', datafmt='%.6E')  # Defaults
        self.assertTrue(_os.path.exists(filename))
    # end def testWriteAnEmptyLHDfmtFile


    # ==================== #


#    def test_LoadComplexHDF5WithBuiltIns(self):
#        # Load and test
#        loaded = ReportInterface.__load_dict_from_hdf5__(self.filename)
#        # print('loaded using built-in function')
#        _np.testing.assert_equal(loaded, self.ex)
#        #print('check 1 passed!')
#        # self.assertDictEqual(loaded, self.ex)   # bug in unittest?!
#
#    def test_LoadComplexHDF5WithWrapper(self):
#        loaded = loadHDF5data(self.filename, sepfield=False, verbose=True)
#        # print('loaded using wrapper function')
#        _np.testing.assert_equal(loaded, self.ex)
#        # print('check 2 passed!')
#        # self.assertDictEqual(loaded, self.ex)   # bug in unittest?!
# end class Test_HDF5IO

if __name__ == "__main__":
    unittest.main(verbosity=2)
# endif



