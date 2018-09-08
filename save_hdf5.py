# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 17:32:02 2016

@author: gawe
"""

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals

import numpy as _np
import h5py as _h5
import os as _os

#from scipy.io import savemat #,loadmat,whosmat
try:
    from pybaseutils.Struct import Struct
except:
    from ..Struct import Struct
# end try

__metaclass__ = type

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

class ReportInterface(object):

    # . ..more details about this class...

    @classmethod
    def __save_dict_to_hdf5__(cls, dic, filename):
        """..."""
        if _os.path.exists(filename):
#            raise ValueError('File %s exists, will not overwrite.' % filename)
            with _h5.File(filename, 'r+') as h5file:
                cls.__recursively_save_dict_contents_to_group__(h5file, dic)
        else:
            with _h5.File(filename, 'w') as h5file:
                cls.__recursively_save_dict_contents_to_group__(h5file, dic)
        #endif

    def __bytesit(item):
        if item is '':
            item = ' '
        # endif
        item = item.encode('ascii', 'xmlcharrefreplace')
#        try:
#            # fails with some unicode, strict utf-8
#            item = item.encode('ascii')  # item.encode('utf-8')
#        except UnicodeEncodeError:
#            item = item.encode('utf-32')
#        # endtry
        item = _np.string_(item)
#                    # item = item.encode('ascii','ignore')
#                    item = _np.string_(item)
        return item

    def __unbytesit(value):
        tmp = (value).decode("utf-8")
        ileft = tmp.find('&#')  # find first index from left
        iright = tmp.find(';')  # find first index from left
        while (ileft>-1) and (iright>-1):
            # Contains xml translated unicode text
            tmp = tmp[:ileft]+chr(int(tmp[ileft+2:iright]))+tmp[iright+1:]
            ileft = tmp.find('&#')  # find first index from left
            iright = tmp.find(';')  # find first index from left
        # end while
        return tmp

    @classmethod
    def __fixlist(cls, item):
        if item is None:
            item = 'None'
#       # Save string types
        if isinstance(item, (str,)):
            item = cls.__bytesit(item)
        if isinstance(item, (int,)):
            item = _np.int64(item)
        if isinstance(item, (bool,)):
            item = _np.uint8(item)
        if isinstance(item, (float,)):
            item = _np.float64(item)
#        if isinstance(item, (type(_np.nan)))
        if isinstance(item, (list,)) and len(item)==0:
            return item
        try:
            if isinstance(item, (_np.ndarray,)) and isinstance(_np.atleast_1d(item)[0],(_np.str_,)):
                item = [cls.__fixlist(ii) for ii in item] #item.tolist()
        except:
            pass
        if isinstance(item,(list,)):
            # Go through each data type in the list
            item = [cls.__fixlist(ii) for ii in item]
            item = _np.asarray(item)
            item = _np.atleast_1d(item)

        return item

    @classmethod
    def __recursively_save_dict_contents_to_group__(cls, h5file, dic):
        """..."""
        # argument type checking
        if not isinstance(dic, dict):
            raise ValueError("must provide a dictionary")
        # if not isinstance(h5file, _h5._hl.files.File):
        #   raise ValueError("must be an open h5py file")
        # save items to the hdf5 file
        for key, item in dic.items():
#            print( key, item )
            if not isinstance(key, str):
                raise ValueError("dict keys must be strings to save to hdf5")

            # Go through each data type and convert it to H5PY compatible
            item = cls.__fixlist(item)

            try:
                if isinstance(item, (bytes,)):
                    # save string types (byte-strings)
                    print(h5file, key, item)
                    grp = (h5file[key] if key in h5file
                           else h5file.create_dataset(key, data=item, dtype=item.dtype))

                # save dictionaries
                elif isinstance(item, dict): # or isinstance(item.any(), dict):
                    print('Dictionary:', h5file, key)
                    grp = h5file[key] if key in h5file else h5file.create_group(key)
                    cls.__recursively_save_dict_contents_to_group__(grp, item)

                # other types cannot be saved and will result in an error
                elif isinstance(item, (Struct, )):
                    print('Structure:', h5file, key)
    #                print('Skipping the user defined class with internal methods')
                    grp = h5file[key] if key in h5file else h5file.create_group(key)
                    cls.__recursively_save_dict_contents_to_group__(
                         grp, item.dict_from_class() )

                elif isinstance(item, (_np.ndarray,)) and isinstance(_np.atleast_1d(item)[0], (dict,)):
                   # item = _np.atleast_1d(item)
                   grp = h5file[key] if key in h5file else h5file.create_group(key)
                   #cls.__recursively_save_dict_contents_to_group__(grp, item.tolist())
                   for ii in range(len(item)):
                       keyii = key + "/list" + str(ii) + "/"
                       grp = h5file[keyii] if keyii in h5file else h5file.create_group(keyii)
                       cls.__recursively_save_dict_contents_to_group__(grp, item[ii])
                   # end for

                elif isinstance(item, (_np.ScalarType, _np.ndarray)):
                # elif isinstance(item, (_np.ScalarType,)):
                    # print(key, item, type(key), type(item))
                    print(h5file, key, item)

                    # If the key already exists in the file, delete it for overwriting
                    if key in h5file:
                        del(h5file[key])
                    # end if

                    h5file.create_dataset(key, data=item, dtype=item.dtype)

                    try:
                        if not _np.all(h5file[key].value == item):
                            raise ValueError('The data representation in the HDF5 file does not match the original dict.')
                    except:
                        print('# == FAILURE == #:', h5file, key, item, h5file[key])
                    # endtry

                elif item is None:
                    print(h5file, key, item)
                    h5file[key] = _np.asarray([])

                else:
                    print('Cannot save key: '+key)
                    raise ValueError('Cannot save %s type.' % type(item))
            except:
                print('What?')
            # end try
    @classmethod
    def __load_dict_from_hdf5__(cls, filename, path=None):
        """..."""
        if path is None:
            path = '/'
        else:
            path = '/'+path
        # end if
        with _h5.File(filename, 'r') as h5file:
            return cls.__recursively_load_dict_contents_from_group__(h5file, path)

    @classmethod
    def __iteratively_load_dict_contents_from_list__(cls, h5file, path):

        ni = len(h5file[path])
        ans = []
        for ii in range(ni):
            ans.append( cls.__recursively_load_dict_contents_from_group__(
                h5file, path + '/' + 'list'+str(ii) + '/') )
        # end for
        return _np.asarray(ans)


    @classmethod
    def __recursively_load_dict_contents_from_group__(cls, h5file, path):
        """..."""
        ans = {}
        for key, item in h5file[path].items():
            if isinstance(item, _h5._hl.dataset.Dataset):
                if isinstance(item.value, bytes):
                    # print(item.value)
                    if item.value == b'None':
                        ans[key] = None
                    else:
                        ans[key] = cls.__unbytesit(item.value)
                    # endif
                elif isinstance(_np.atleast_1d(item.value)[0], bytes):
                    tmp = []
                    for ii in item:
                        if ii == b'None':
                            tmp.append(None)
                        else:
                            tmp.append(cls.__unbytesit(ii))
                        # end if
                    # end for
                    ans[key] = _np.asarray(tmp)
                else:
                    ans[key] = item.value
                # endif
            elif len(key)>3 and key[0:4] == 'list':
                ans = cls.__iteratively_load_dict_contents_from_list__(
                                h5file, path)

            elif isinstance(item, _h5._hl.group.Group):
                ans[key] = cls.__recursively_load_dict_contents_from_group__(
                                h5file, path + '/' + key + '/')
        return ans

# -------------------------------------------------------------------------- #

def loadHDF5data(sfilename, path=None, sepfield=False, verbose=True):

    HDF5data = ReportInterface.__load_dict_from_hdf5__(sfilename, path)

    if verbose:
        print('### Successfully loaded dictionary from HDF5 file ###')
        print('### From name '+sfilename+' ###')
    # endif

    if sepfield:
        HDF5data = [HDF5data[keys] for keys in HDF5data]
        HDF5data = tuple(HDF5data)
    # endif

    return HDF5data
#end def load_HDF5


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #


def test():
    ex = {
        'name': 'GMW\xb0' + chr(255),
        'exdict': {'str': 'new'},
        'age':  _np.int64(29),
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
        'imaginary_numbers': _np.ones( (5,1), dtype=_np.float64)+ 1j*_np.random.normal(0.0, 1.0, (5,1))
    }
    print('ex')
    filename = 'foo.hdf5'
    if _os.path.exists(filename):
        _os.remove(filename)
    # endif

    ReportInterface.__save_dict_to_hdf5__(ex, filename)

    # Load and test
    loaded = ReportInterface.__load_dict_from_hdf5__(filename)
    print('loaded using built-in function')
    _np.testing.assert_equal(loaded, ex)
    print('check 1 passed!')


    loaded = loadHDF5data(filename, sepfield=False, verbose=True)
    print('loaded using wrapper function')
    _np.testing.assert_equal(loaded, ex)
    print('check 2 passed!')

    return ex, loaded


if __name__ == "__main__":
    ex, loaded = test()
# endif

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

