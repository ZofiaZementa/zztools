from .step import Step
from utilities import git
from exceptions import ConfigValueError


class GitStep(Step):
    """A step that executes a git action

    class methods:
    fromjson() -- returns a GitStep object from json

    instance variables:
    path -- path to the repo
    remoteurl -- url to the remote repository
    """

    def fromjson(stepjson, listjson):
        """Return a GitStep object of a child step

        arguments:
        stepjson -- the json of the whole step already imported into python
        listjson -- the json of the whole list file the step was in
        """
        try:
            command = stepjson['command']
            action = command['action']
        except KeyError as e:
            e.message = 'Missing attribute {} in git step'.format(e.args[0])
            raise
        if action == 'clone':
            try:
                remoteurl = command['url']
            except KeyError as e:
                e.message = 'Missing attribute {} in git clone step'.format(e.args[0])
                raise
            path = command.get('path', None)
            return GitCloneStep(remoteurl, path)
        else:
            message = 'Invalid action type {} for git step'.format(action)
            raise ConfigValueError(message)

    def __init__(self, path, remoteurl=None):
        """Constructor

        arguments:
        path -- path of the repository
        remoturl -- url of the remote repository, this can be None
        """
        self.path = path
        self.remoteurl = remoteurl


class GitCloneStep(GitStep):
    """A step that installs a given repository

    This class inherits from GitStep. due to it's inherently different nature
    from any other operation on a git repository, this class doesn't use the
    constructor of GitStep, but defines its own

    instance methods:
    execute -- execute this step
    """

    def __init__(self, remoteurl, path=None):
        """Constructor

        since with this constructor, only the priorities are different, it only
        calls the constructor of GitStep, with the given values

        arguments:
        remoturl -- url of the remote repository
        path -- path for the repository to be cloned into, if none is given,
                it is cloned into the current working directory
        """
        super(GitCloneStep, self).__init__(path, remoteurl)

    def execute(self):
        """Execute this step"""
        git.clone(self.remoteurl, self.path)
