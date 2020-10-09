# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 17:32:02 2016

@author: gawe
"""

# ========================================================================== #
# ========================================================================== #
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

# ========================================================================== #
# ========================================================================== #

def print_dict(my_dict, indent=1):
#    try:
#        import json as _jsn
#        _jsn.dumps(my_dict, indent=indent)
#    except:
    print(my_dict)
#    # end if
# end def

class ReportInterface(object):

    # . ..more details about this class...

    def __init__(self, dic=None, filename=None):
        if dic is not None and filename is not None:
            self.__save_dict_to_hdf5__(dic, filename)
        # end if
    # end def

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
        # end if

        try:
            h5file.close()
        except:
            pass
        # end if

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
        if isinstance(item, (Struct,)):
            item.StructObject = True
            item = item.dict_from_class()
        if isinstance(item, (list,)) and len(item)==0:
            return item
#        if isinstance(item, (_np.ndarray,)) and len(item)==0:
#            return item.tolist()
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
    def __recursively_save_dict_contents_to_group__(cls, h5file, dic, verbose=False):
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

#            if key == 'empty_list':
            # if key == 'dictarray':
#                 print('debugging')

            try:
                if isinstance(item, (bytes,)):
                    # save string types (byte-strings)
                    if verbose:   print(h5file, key, item)  # end if
                    grp = (h5file[key] if key in h5file
                           else h5file.create_dataset(key, data=item, dtype=item.dtype))

                # save dictionaries
                elif isinstance(item, dict): # or isinstance(item.any(), dict):
                    print('Dictionary:', h5file, key)
                    grp = h5file[key] if key in h5file else h5file.create_group(key)
                    cls.__recursively_save_dict_contents_to_group__(grp, item, verbose=verbose)

                # other types cannot be saved and will result in an error
                elif isinstance(item, (Struct, )):
                    print('Structure:', h5file, key)
    #                print('Skipping the user defined class with internal methods')
                    grp = h5file[key] if key in h5file else h5file.create_group(key)
                    cls.__recursively_save_dict_contents_to_group__(
                         grp, item.dict_from_class(), verbose=verbose)

                elif isinstance(item, (_np.ndarray,)) and len(_np.atleast_1d(item))==0:
                    # print('empty numpy array or list')
                    if verbose:   print(h5file, key, item)    # end if
                    h5file.create_dataset(key, data=item, dtype=item.dtype)


                elif isinstance(item, (_np.ndarray,)) and isinstance(_np.atleast_1d(item)[0], (dict,)):
                   # item = _np.atleast_1d(item)
                   grp = h5file[key] if key in h5file else h5file.create_group(key)
                   #cls.__recursively_save_dict_contents_to_group__(grp, item.tolist())
                   try:
                       for ii in range(_np.atleast_1d(len(item))):
                           keyii = key + "/list" + str(ii) + "/"
                           grp = h5file[keyii] if keyii in h5file else h5file.create_group(keyii)
                           cls.__recursively_save_dict_contents_to_group__(grp, item[ii], verbose=verbose)
                       # end for
                   except:
                       for ii in range(len(item)):
                           keyii = key + "/list" + str(ii) + "/"
                           grp = h5file[keyii] if keyii in h5file else h5file.create_group(keyii)
                           cls.__recursively_save_dict_contents_to_group__(grp, item[ii], verbose=verbose)
                       # end for

                elif isinstance(item, (_np.ScalarType, _np.ndarray)):
                # elif isinstance(item, (_np.ScalarType,)):
                    # print(key, item, type(key), type(item))
                    if verbose:   print(h5file, key, item)    # end if

                    # If the key already exists in the file, delete it for overwriting
                    if key in h5file:
                        del(h5file[key])
                    # end if

                    h5file.create_dataset(key, data=item, dtype=item.dtype)

                    try:
                        if not _np.all(h5file[key].value == item) and not _np.isnan(_np.atleast_1d(item)).any():
                            raise ValueError('The data representation in the HDF5 file does not match the original dict.')
                    except:
                        print('# == FAILURE == #:', h5file, key, item, h5file[key])
                    # endtry

                elif item is None:
                    if verbose:   print(h5file, key, item)    # end if
                    h5file[key] = _np.asarray([])

                elif isinstance(item, list) and len(item)==0:
                    h5file[key] = item
                else:
                    if verbose:
                        print('Cannot save key: '+key)
                    raise ValueError('Cannot save %s type.' % type(item))
            except:
                if verbose:
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
#            return cls.__recursively_load_dict_contents_from_group__(h5file, path)
            out = cls.__recursively_load_dict_contents_from_group__(h5file, path)
        try:
            h5file.close()
        except:
            pass
        # end if
        return out

    @classmethod
    def __iteratively_load_dict_contents_from_list__(cls, h5file, path):

        ni = len(h5file[path])
        ans = []
        for ii in range(ni):
            try:
                ans.append( cls.__recursively_load_dict_contents_from_group__(
                    h5file, path + '/' + 'list'+str(ii) + '/') )
            except:
                pass
#                print(1)   # TODO:!  this is due to sometimes saving a Struct object (or multiple) in a list
            # end try
        # end for
        return _np.asarray(ans)


    @classmethod
    def __recursively_load_dict_contents_from_group__(cls, h5file, path):
        """..."""
        ans = {}
        for key, item in h5file[path].items():
#            if key == 'empty_list':
#                print('debugging')
            if isinstance(item, _h5._hl.dataset.Dataset):
                if isinstance(item.value, bytes):
                    # print(item.value)
                    if item.value == b'None':
                        ans[key] = None
                    else:
                        ans[key] = cls.__unbytesit(item.value)
                    # endif
                elif item.shape == (0,):
                    ans[key] = item.value
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
                    try:
                        ans[key] = item.value
                    except:
#                        print(1)
                        pass
                    # end try
            elif len(key)>3 and key[0:4] == 'list':
#                ans[key[4:]] = cls.__iteratively_load_dict_contents_from_list__(
                ans = cls.__iteratively_load_dict_contents_from_list__(
                                h5file, path)
            elif isinstance(item, _h5._hl.group.Group):
#                print('entering group %s'%(key,))
                ans[key] = cls.__recursively_load_dict_contents_from_group__(
                                h5file, path + '/' + key + '/')
        # end for

        if type(ans)==type({}) and 'StructObject' in ans:
            ans.pop('StructObject')
            ans = Struct(ans)
        # end if
        return ans

# ========================================================================== #

def loadHDF5data(sfilename, path=None, sepfield=False, verbose=False):

    HDF5data = ReportInterface.__load_dict_from_hdf5__(sfilename, path)

    if verbose:
        print('### Successfully loaded dictionary from HDF5 file ###')
        print('### From name '+sfilename+' ###')

        print_dict(HDF5data)
    # endif

    if sepfield:
        HDF5data = [HDF5data[keys] for keys in HDF5data]
        HDF5data = tuple(HDF5data)
    # endif

    return HDF5data
#end def load_HDF5


# ========================================================================== #
# ========================================================================== #


def test():
    tst = Struct()
    tst.a = 0;    tst.b = 1
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
        'imaginary_numbers': _np.ones( (5,1), dtype=_np.float64)+ 1j*_np.random.normal(0.0, 1.0, (5,1)),
        'empty_array':_np.asarray([]),
        'empty_list':[],
#        'objectlist':[tst],
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

# ========================================================================== #
# ========================================================================== #

