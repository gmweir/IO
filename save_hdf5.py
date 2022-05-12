# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 17:32:02 2016

@author: gawe


History:
This module has been hacked together over a period of roughly 10 years.

The orignal version was written by GMW and worked great in python27 and python3
up until the release of python3.9. After reinstalling Anaconda python,
I had to rewrite most of my codebase. Annoying. But Worth it?

I updated in 2022 to use some of the methodologies from the hdf5_io module
from tenpy

.. note ::
    The tenpy/hdf5_io module is maintained in the repository
    https://github.com/tenpy/hdf5_io.git




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
    from IO.utils import Struct, print_dict, test_dict, versiontuple
except:
    from .utils import Struct, print_dict, test_dict, versiontuple
# end try

__metaclass__ = type

# ========================================================================== #
# ========================================================================== #


if versiontuple(_h5.__version__) <= versiontuple('2.9.0'):
    """
    the dataset.value attribute was deprecates. It worked with
    h5py 2.9.0 (released in 2014), but the current version, h5py 3.2
    (2022) use a different format:
    """
    def get_item(h5file, key, item):
        """  """
        return h5file[key].value
        # return item.value
else:
    def get_item(h5file, key, item):
        """  """
        return h5file[key][()]
        # return item[()]   # item
        # return h5file.get(key).value   # item
# end if



class ReportInterface(object):

    # . ..more details about this class...

    def __init__(self, dic=None, filename=None):
        if dic is not None and filename is not None:
            self.__save_dict_to_hdf5__(dic, filename)
        # end if
    # end def

    @classmethod
    def __save_dict_to_hdf5__(cls, dic, filename, verbose=False):
        """..."""
        if _os.path.exists(filename):
#            raise ValueError('File %s exists, will not overwrite.' % filename)
            with _h5.File(filename, mode='r+') as h5file:
                cls.__recursively_save_dict_contents_to_group__(h5file, dic, verbose=verbose)
        else:
            with _h5.File(filename, mode='w') as h5file:
                cls.__recursively_save_dict_contents_to_group__(h5file, dic, verbose=verbose)
        # end if

        try:
            h5file.close()
        except:
            pass
        # end if

    def __bytesit(item):
        if item == '':
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
        # end if

        # save items to the hdf5 file
        for key, item in dic.items():
            if verbose:
                print( key, item )
            # end if

            if not isinstance(key, str):
                raise ValueError("dict keys must be strings to save to hdf5")
            # end if

            # Go through each data type and convert it to H5PY compatible
            item = cls.__fixlist(item)

            try:
            # if 1:
                if isinstance(item, (bytes,)):
                    # save string types (byte-strings)
                    if verbose:   print(h5file, key, item)  # end if
                    grp = (h5file[key] if key in h5file
                            else h5file.create_dataset(key, data=item, dtype=item.dtype))
                            # else ReportInterface.create_dataset(h5file, key, item))

                elif isinstance(item, dict): # or isinstance(item.any(), dict):
                    # save dictionaries
                    if verbose:   print('Dictionary:', h5file, key)  # end if
                    grp = h5file[key] if key in h5file else h5file.create_group(key)
                    cls.__recursively_save_dict_contents_to_group__(grp, item, verbose=verbose)

                # other types cannot be saved and will result in an error
                elif isinstance(item, (Struct, )):
                    if verbose:   print('Structure:', h5file, key)   # end if
                    # print('Skipping the user defined class with internal methods')
                    grp = h5file[key] if key in h5file else h5file.create_group(key)
                    cls.__recursively_save_dict_contents_to_group__(
                         grp, item.dict_from_class(), verbose=verbose)

                elif isinstance(item, (_np.ndarray,)) and len(_np.atleast_1d(item))==0:
                    # print('empty numpy array or list')
                    if verbose:   print(h5file, key, item)    # end if
                    # ReportInterface.create_dataset(h5file, key, item)
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
                    # ReportInterface.create_dataset(h5file, key, item)
                    h5file.create_dataset(key, data=item, dtype=item.dtype)

                    try:
                    # if 1:
                        # if not _np.all(h5file[key].value == item) and not _np.isnan(_np.atleast_1d(item)).any():
                        if not _np.all(get_item(h5file, key, item) == item) and not _np.isnan(_np.atleast_1d(item)).any():
                            raise ValueError('The data representation in the HDF5 file does not match the original dict.')
                    except:
                    # else:
                        if verbose:
                            print('# == FAILURE == #:', h5file, key, item, h5file[key])
                        # end if
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
            # else:
                if verbose:
                    print('What? ... general failure while saving. Consider debugging.')
            # end try

    # ==================== #


    @classmethod
    def create_dataset(cls, h5file, key, item, **kwargs):
        compression = kwargs.setdefault('compression', 'gzip')
        compression_opts = kwargs.setdefault('compression_opts', 9)
        shuffle = kwargs.setdefault('shuffle', True)
        if compression is not None:
            return h5file.create_dataset(key, data=item, dtype=item.dtype, **kwargs)
        else:
            return h5file.create_dataset(key, data=item, dtype=item.dtype)
        # end if
    # end def create_dataset


    # ==================== #


    @classmethod
    def __load_dict_from_hdf5__(cls, filename, path=None):
        """..."""
        if path is None:
            path = '/'
        else:
            path = '/'+path
        # end if
        with _h5.File(filename, 'r') as h5file:
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

    #
    #
    #


    @classmethod
    def __recursively_load_dict_contents_from_group__(cls, h5file, path):
        """
        the dataset.value attribute was deprecates. It worked with
        h5py 2.9.0 (released in 2014), but the current version, h5py 3.2
        (2022) use a different format:
        """
        debugging = False

        ans = {}
        for key, item in h5file[path].items():
            if debugging and 0:
                print('debugging')
            # end if

            # iterate over data sets
            if isinstance(item, _h5._hl.dataset.Dataset):

                item_value = get_item(h5file[path], key, item)

                if debugging:
                    print(item_value)

                if isinstance(item_value, bytes):
                    # if the item is a byte-string
                    if item_value == b'None':
                        ans[key] = None
                    else:
                        ans[key] = cls.__unbytesit(item_value)
                    # endif
                elif item.shape == (0,) or item.shape==():
                    # if the item is a scalar or
                    ans[key] = item_value

                elif isinstance(_np.atleast_1d(item_value)[0], bytes):
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
                        ans[key] = item_value
                    except:
                        pass
                    # end try
            elif len(key)>3 and key[0:4] == 'list':
                ans = cls.__iteratively_load_dict_contents_from_list__(
                                h5file, path)
            elif isinstance(item, _h5._hl.group.Group):
                if debugging:
                    print('entering group %s'%(key,))
                ans[key] = cls.__recursively_load_dict_contents_from_group__(
                                h5file, path + '/' + key + '/')
        # end for

        return ans

        if type(ans)==type({}) and 'StructObject' in ans:
            ans.pop('StructObject')
            ans = Struct(ans)
        # end if
    # end def

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


def test(verbose=False):

    ex = test_dict()
    if verbose:
        print_dict(ex)
    # end if

    filename = 'foo.hdf5'
    filename = _os.path.join(_os.path.dirname(__file__), 'TESTS', 'data', filename)
    if _os.path.exists(filename):
        _os.remove(filename)
    # endif

    ReportInterface.__save_dict_to_hdf5__(ex, filename, verbose=verbose)


    # Load and test
    loaded = ReportInterface.__load_dict_from_hdf5__(filename)
    print('loaded using built-in function')
    _np.testing.assert_equal(loaded, ex)
    print('check 1 passed!')


    loaded = loadHDF5data(filename, sepfield=False, verbose=verbose)
    print('loaded using wrapper function')
    _np.testing.assert_equal(loaded, ex)
    print('check 2 passed!')

    return ex, loaded


if __name__ == "__main__":
    ex, loaded = test()
# endif

# ========================================================================== #
# ========================================================================== #

