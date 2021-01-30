from .step import Step
from exceptions import ConfigValueError
import todolist


class ListStep(Step):
    """A step that is another todolist

    This step shouldn't be instanciated, since the fromjson method doesn't
    actually return a ListStep object, but a Todolist object, since both use
    the execute funtions to execute, this class is mainly there if this has to
    be changed in the future, and for continuity.

    class methods:
    fromjson() -- return a todolist object
    """

    def fromjson(stepjson, listjson):
        """Return a todolist object from a liststep json

        This doesn't actually return a ListStep object, but a Todolist object,
        since the Todolist object is very similar to this object.
        This method doesn't check for circular todolist calls, so be careful
        with that.

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
        except KeyError as e:
            e.message = 'Missing command attribute in ListStep'
            raise
        path = command.get('path', None)
        name = command.get('name', None)
        if path:
            return todolist.TodoList.fromfile(path, name)
        elif name:
            return todolist.TodoList.fromjson(listjson, name)
        else:
            message = 'Found neither path nor name in todolist step'
            raise ConfigValueError(message)

    def fromsteps(steps):
        """Return a todolist object from a liststep json

        This doesn't actually return a ListStep object, but a Todolist object,
        since the Todolist object is very similar to this object.
        This method doesn't check for circular todolist calls, so be careful
        with that.

        arguments:
        steps -- a list of steps for the todolist
        """
        return todolist.TodoList(steps)
