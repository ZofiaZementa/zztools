import sys

import configfilemanager


def getpackagesfromjson(json):
    """Returns the all the pseudopackages from the given json

    Since currently there is no object for a package, it just directly returns
    the given json, but this may change in the future

    arguments:
    json -- the json of the whole psudopackages file already imported into
            python
    """
    return json


def getpackagesfromfile(path):
    """Returns all the pseudopackages from the given file in json format

    Imports the pseudopackages at the given path and returns them in a json
    type format. The contents of the file are converted to json by the
    configfilemanager, the real content of the file could be in json, yaml or
    something similar.

    arguments:
    path -- the path to the file containing the pseudopackages

    execptions:
    FileNotFoundError -- if the file at the given path is not found
    """
    try:
        json = configfilemanager.getconfigfromfile(path)
    except FileNotFoundError:
        print('File with Packages could not be found', file=sys.stderr)
        sys.exit(1)
    return getpackagesfromjson(json)
