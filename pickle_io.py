# -*- coding: utf-8 -*-
"""
Created on Thu May 12 11:17:25 2022

@author: gawe
"""

import cPickle
import traceback

try:
    from IO.utils import Struct
except:
    from .utils import Struct
# end try


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
                file.write(cPickle.dumps(self.__dict__))
        except:
            file = open(filename, mode=mode)
            file.write(cPickle.dumps(self.__dict__))
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
        self.__dict__ = cPickle.loads(dataPickle)
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