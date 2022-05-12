# -*- coding: utf-8 -*-
"""
Created on Thu May 12 11:17:25 2022

@author: gawe
"""


import traceback
import sys

try:
    from IO.utils import Struct
except:
    from .utils import Struct
# end try


if sys.version_info < (3,0):
    import cPickle as pickle
else:
    import pickle
# end if

try:
    # the hdf5_io module has a nice function that works with pickle files
    try:
        from IO.hdf5_io import save, load
    except ImportError:
        from .hdf5_io import save, load
    # end try
except ImportError:
    # No h5py ... maybe
    def save(data, filename, mode='w'):
        """Save `data` to file with given `filename`.

        This function guesses the type of the file from the filename ending.
        Supported endings:

        ============ ===============================
        ending       description
        ============ ===============================
        .txt, .dat    ASCII without compression
        ------------ -------------------------------
        .pkl, .pickle Pickle without compression
        ------------ -------------------------------
        .pklz        Pickle with gzip compression.
        ============ ===============================

        Parameters
        ----------
        filename : str
            The name of the file where to save the data.
        mode : str
            File mode for opening the file. ``'w'`` for write (discard existing file),
            ``'a'`` for append (add data to exisiting file).
            See :py:func:`open` for more details.
        """
        if filename.endswith('.txt') or filename.endswidth('.dat'):
            with open(filename, mode=mode) as file:
                # pickle.dump(data, file))
                file.write(pickle.dumps(data))

        elif filename.endswith('.pkl') or filename.endswith('.pickle'):
            with open(filename, mode + 'b') as file:
                pickle.dump(data, file)

        elif filename.endswith('.pklz'):
            import gzip
            with gzip.open(filename, mode + 'b') as file:
                pickle.dump(data, file)

        else:
            raise ValueError("Don't recognise file ending of " + repr(filename))
        # end if
    # end def save


    def load(filename):
        """Load data from file with given `filename`.

        Guess the type of the file from the filename ending, see :func:`save` for possible endings.

        Parameters
        ----------
        filename : str
            The name of the file to load.

        Returns
        -------
        data : obj
            The object loaded from the file.
        """
        filename = str(filename)
        if filename.endswith('.txt') or filename.endswith('.dat'):
            with open(filename, 'r') as file:
                data = pickle.loads(file.read())

        elif filename.endswith('.pkl') or filename.endswith('.pickle'):
            with open(filename, 'rb') as file:
                data = pickle.load(file)

        elif filename.endswith('.pklz'):
            import gzip
            with gzip.open(filename, 'rb') as file:
                data = pickle.load(file)

        else:
            raise ValueError("Don't recognise file ending of " + repr(filename))
        return data
# end try

# ========================== #
# ========================== #


class pickle_io(Struct):
    __ext__ = 'pickle'

    def save(self, ext=None, mode=None):
        """save class as self.name.(ext)"""
        if ext is None:
            ext = self.__ext__
        else:
            self.__ext__ = ext
        # end if

        if mode is None:
            if ext.find('pkl')>-1 or ext.find('pickle')>-1:
                # binary write
                mode = 'wb'
            else:
                mode = 'w'
            # end if
        # end if

        filename = '%s.%s'%(self.name, self.ext)

        try:
            with open(filename, mode=mode) as file:
                file.write(pickle.dumps(self.__dict__))
        except:
            file = open(filename, mode=mode)
            file.write(pickle.dumps(self.__dict__))
            file.close()
        finally:
            try: file.close()
            except: pass
        # end try
    # end def

    def load(self, ext=None, mode=None):
        """try load self.name.(ext)"""
        if ext is None:
            ext = self.__ext__
        else:
            self.__ext__ = ext
        # end if

        if mode is None:
            if ext.find('pkl')>-1 or ext.find('pickle')>-1:
                # binary read
                mode = 'rb'
            else:
                mode = 'r'
            # end if
        # end if

        filename = '%s.%s'%(self.name, self.ext)

        try:
            with open(filename, mode=mode) as file:
                dataPickle = file.read()
        except:
            file = open(filename, mode)
            dataPickle = file.read()
            file.close()
        finally:
            try: file.close()
            except: pass
        # end try
        self.__dict__ = pickle.loads(dataPickle)
    # end def load
# end class


class class_io(pickle_io):
    """
    This file will load a class from a (pickle read/writable) file with the instance name:
        myClass = class_io()
        myClass.load()        # loads myClass.txt into the myClass instance

        or

        myClass = class_io()
        myClass.ext =
    """
    __ext__ = 'txt'

    def __init__(self):
        #set name from variable name. http://stackoverflow.com/questions/1690400/getting-an-instance-name-inside-class-init
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        def_name = text[:text.find('=')].strip()
        self.name = def_name

    def example(self):
        try:
            self.load()
        except:
            ##############
            #to demonstrate
            self.someAttribute = 'bla'
            self.someAttribute2 = ['more']
            ##############

            self.save()
        # end try
    # end def exampel

# end def

# ==================================================================== #
# ==================================================================== #





# ==================================================================== #
# ==================================================================== #