from .step import Step
from zztools.utilities import downloader


class DownloadStep(Step):
    """A step that downloads something

    class methods:
    fromjson() -- returns an DownloadStep object from json

    instance methods:
    execute -- executes the step

    instance variables:
    url -- the url from which to download
    to -- where to download to, can be None
    """

    def fromjson(stepjson, listjson):
        """Return an object of this class from a json

        arguments:
        stepjson -- the json of the whole step already imported into python
        listjson -- the json of the whole list file the step was in

        exceptions:
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        """
        try:
            command = stepjson['command']
            url = command['url']
        except KeyError as e:
            e.message = 'Missing attribute {} in download step'.format(e.args[0])
            raise
        to = command.get('to', None)
        return DownloadStep(url, to)

    def __init__(self, url, to=None):
        """Constructor

        arguments:
        url -- the url which to download
        to -- where to download it to
        """
        self.url = url
        self.to = to

    def execute(self):
        """Downloads the url with the given tool"""
        downloader.download(self.url, todir=self.to)
