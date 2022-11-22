import pickle

def dump_pickle(obj, filename):
    """
    saves a file/object as a pickle file
    """
    with open(filename, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(filename):
    """
    loads a pickle file back as a variable/object
    """
    with open(filename, 'rb') as handle:
        return pickle.load(handle)
