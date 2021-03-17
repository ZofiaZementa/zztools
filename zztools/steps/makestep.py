import validators

from .step import Step
from .gitstep import GitCloneStep
from .unpackstep import DownloadUnpackStep
from .liststep import ListStep
from .rmstep import RmStep
import zztools.todolist as todolist_mod
from zztools.utilities import maker
from zztools.utilities import git
from zztools.utilities import temp

class MakeStep(Step):
    """A step that makes something

    this step uses the wellknown make program to compile something

    class methods:
    fromjson() -- returns an object from this class from a json

    instance variables:
    path -- the path to the makefile
    target -- the target which to make
    """

    def fromjson(stepjson, listjson):
        """Return an object of this class from a json

        when the path in the json is an actual path, a normal MakeStep is
        returnd. If it is a url, it is checked whether it is a git url or not.
        If it is a git url, a ListStep containing a GitCloneStep and a
        MakeStep is returned. If it is just a normal url, a ListStep containing
        a DownloadUnpackStep and a MakeStep is returned.

        arguments:
        stepjson -- the json of the whole step already imported into python
        listjson -- the json of the whole list file the step was in

        exceptions:
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        ValueError -- if the name of the repo cound't be found in the url
        """
        try:
            command = stepjson['command']
            path = command['path']
        except KeyError as e:
            e.message = 'Missing attribute {} in make step'.format(e.args[0])
            raise
        target = command.get('target', None)
        if validators.url(path):
            if git.is_git_url(path):
                return gitmakestep(path, target)
            else:
                return downloadmakestep(path, target)
        else:
            return MakeStep(path, target)

    def __init__(self, path, target=None):
        """Constructor

        arguments:
        path -- path to the makefile
        target -- targte which to make
        """
        self.path = path
        self.target = target

    def execute(self):
        """Execute this step"""
        maker.make(self.path, self.target)


def gitmakesteps(path, target=None):
    """Return a list of steps that represent a GitMakeStep

    arguments:
    path -- path to the makefile
    target -- targte which to make
    """
    intermediate_path = temp.new_temp_dir_path()
    steps = [GitCloneStep(path, intermediate_path)]
    steps.append(MakeStep(intermediate_path, target))
    steps.append(RmStep(intermediate_path))
    return steps


def gitmakestep(*args, **kwargs):
    """Return a ListStep containing the steps representing a GitMakeStep"""
    todolist = todolist_mod.TodoList(gitmakesteps(*args, **kwargs))
    return ListStep(todolist)


def downloadmakesteps(path, target=None):
    """Return a list of steps that represent a DownloadMakeStep

    arguments:
    path -- path to the makefile
    target -- targte which to make
    """
    intermediate_path = temp.new_temp_dir_path()
    steps = [DownloadUnpackStep(path, intermediate_path)]
    steps.append(MakeStep(intermediate_path, target))
    steps.append(RmStep(intermediate_path))
    return steps


def downloadmakestep(*args, **kwargs):
    """Return a ListStep containing the steps representing a DownloadMakeStep"""
    todolist = todolist_mod.TodoList(downloadmakesteps(*args, **kwargs))
    return ListStep(todolist)
