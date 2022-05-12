

from __future_ import with_statement

import h5py


def WriteToH5(filename, variable_dict, verbose=True):
    """
    function to write all variables in the dictionary to an hdf5 file
    given a dictionary of variable names and the variables,
    the variables will be stored in the given HDF5 file

    usage example:

        WriteToH5(fname+'.hdf5', {'gammas':gammas,
                          'omegas':omegas,
                          'eigenmodes':eigenmodes,
                          'locations':locations,
                          'm_nums':m_nums,
                          'bfields':bfields})
    """

    if filename[-5:] != '.hdf5':
        filename=filename+'.hdf5'
    # end if


    def code_to_execute():
        for var_name in var_names:
            dataset=h5f.create_dataset(var_name, data=variable_dict[var_name])
        # end for
        dt= h5py.special_dtype(vlen=str)
        dataset=h5f.create_dataset('var_names', data=var_names, dtype=dt)
    # end def

    var_names=variable_dict.keys()
    # if 1:
    try:
        with h5py.File(filename, 'w') as h5f:
            code_to_execute()
        # end with open
    # else:
    except IOError:
        if verbose:
            print('The file %s does not appear to exist or is not accessible')
        # end if
        raise
    except:
        h5f = h5py.File(filename, 'w')
        code_to_execute()
    finally:
        try: h5f.close()
        except: pass
    # end try
