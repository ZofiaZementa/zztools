import json
import yaml
import os
import sys


def _getconfigfromjsonfile(path):
    """Returns the imported contents of the given json file

    arguments:
    path -- path to the json file

    exceptions:
    FileNotFoundError -- if the file at the given path is not found
    """
    with open(path) as file:
        return json.load(file)


def _getconfigfromyamlfile(path):
    """Returns the imported contents of the given yaml file

    arguments:
    path -- path to the yaml file

    exceptions:
    FileNotFoundError -- if the file at the given path is not found
    """
    with open(path) as file:
        return yaml.safe_load(file)


def getconfigfromfile(path):
    """Returns a json type object from the file at the given path

    Reads and converts the file at the given path to a json type object in
    python. Currently only json and yaml filetypes are supported

    arguments:
    path -- path to the file

    exceptions:
    FileNotFoundError -- if the file at the given path is not found
    """
    filetype = os.path.splitext(path)[1]
    if filetype == '.json':
        return _getconfigfromjsonfile(path)
    elif filetype == '.yaml':
        return _getconfigfromyamlfile(path)
    else:
        if not filetype:
            print('Error: Filename has no extension', file=sys.stderr)
        else:
            print('Error: Filetype {} not supported'.format(filetype), \
                    file=sys.stderr)
        sys.exit(1)
