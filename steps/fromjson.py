from .stepmap import stepmap
from exceptions import ConfigValueError

def fromjson(json):
    """Return a Step object

    Returns an object of a child class of Step, a CollectionStep, ExecuteStep,
    DownloadStep or UnpackStep

    arguments:
    json -- the json of the whole step already imported into python

    exceptions:
    FileNotFoundError -- if the file at the given path is not found
                            this error contains an attribute \"message\", which
                            contains the errormessage
    KeyError -- if a needed attribute in the json is not found
                this error contains an attribute \"message\", which
                contains the errormessage
    ConfigValueError -- if some attribute in the config has an invalid value
                        this error contains an attribute \"message\", which
                        contains the errormessage
    """
    if isinstance(json, list):
        return [fromjson(step) for step in json]
    try:
        type = json['type']
    except KeyError as e:
        e.message = 'Missing type in step'
        raise
    try:
        stepfromjson = stepmap[type]
    except KeyError:
        message = 'Invalid step type {}'.format(json['type'])
        raise ConfigValueError(message)
    return stepfromjson(json)
