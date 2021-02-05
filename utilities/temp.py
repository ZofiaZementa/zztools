import os
import uuid
import tempfile

_tempprefix = 'zztools'

def new_temp_dir_path(dirname=None):
    """Return a path to a new temporary directory

    this function only returns the path, it doesn't actually make the directory

    arguments:
    dirname -- the name of the temporary directory
               if none is given, a random name is constructed
    """
    if not dirname:
        dirname = '{}-{}'.format(_tempprefix, str(uuid.uuid4()))
    return os.path.join(tempfile.gettempdir(), dirname)


def new_temp_file_path(filename=None):
    """Return a path to a new temporary file

    this function only returns the path, it doesn't actually make the file

    arguments:
    filename -- the name of the temporary file
                if none is given, a random name is constructed
    """
    if not filename:
        filename = '{}-{}'.format(_tempprefix, str(uuid.uuid4()))
    return os.path.join(tempfile.gettempdir(), filename)
