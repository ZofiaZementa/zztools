import tempfile
import validators
import uuid
import os

from .step import Step
from downloader import download
from unpacker import unpack


class UnpackStep(Step):
    """A step that unpacks something

    this is an \"abstract\" class, it only implements fromjson and the
    constructor and should not be instaciated. All child classes should
    implement the following methods:

    exceute(self) -- execute the step

    class methods:
    fromjson() -- returns an object of this class from a json

    instance variables:
    archive -- the path or url to the archive which to unpack
    to -- the path to where to unpack the archive, this can be None
    """

    def fromjson(json):
        """Return an object of this class from a json

        If the to value in the json command is a valid url (using the vaildators
        package), a DownloadUnpackStep is returned, otherwise a LocalUnpackStep.
        This means the \"https\" part of the url can't be omitted, because
        otherwis it is indistinguishable from a path.

        arguments:
        json -- the json of the whole step already imported into python

        exceptions:
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        """
        try:
            command = json['command']
            archive = command['archive']
        except KeyError as e:
            e.message = 'Missing attribute {} in unpack step'.format(e.args[0])
            raise
        to = command.get('to', None)
        if validators.url(archive):
            return DownloadUnpackStep(archive, to)
        else:
            return LocalUnpackStep(archive, to)

    def __init__(self, archive, to=None):
        """Constructor

        arguments:
        archive -- the path or url to the archive which to unpack
        to -- the directory where to unpack the archive to (default=None)
              if none is given, the archive will be unpacked in the current
              directory
        """
        self.archive = archive
        self.to = to


class LocalUnpackStep(UnpackStep):
    """Regular unpack step that unpacks a local file

    This class inherits from UnpackStep

    instance methods:
    execute() -- executes the step
    """

    def execute(self):
        """Unpacks the archive at the given path"""
        unpack(self.archive, self.to)


class DownloadUnpackStep(UnpackStep):
    """Unpack step which downloads the archive first

    This class inherits from UnpackStep

    instance methods:
    execute() -- executes the step
    """

    def execute(self):
        """Downloads the archive from the given url and unpacks it

        This method downloads the archive from the url in self to a random
        filename in the tempdir, unpacks that file to the path in self and
        deletes the tempfile
        """
        path = '{}/{}'.format(tempfile.gettempdir(), uuid.uuid4())
        download(self.archive, tofile=path)
        unpack(path, self.to)
        os.remove(path)
