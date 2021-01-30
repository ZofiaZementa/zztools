import patoolib
import os

def unpack(path, todir=None):
    """Unpack the given file

    arguments:
    path -- the path to the file which to unpack
    todir -- the location to which to unpack the file
    """
    path = os.path.expanduser(path)
    if todir:
        todir = os.path.expanduser(todir)
        patoolib.extract_archive(path, outdir=todir)
    else:
        patoolib.extract_archive(path)
