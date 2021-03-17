from .step import Step
from zztools.exceptions import ConfigValueError
import zztools.todolist as todolist_mod


class ListStep(Step):
    """A step that is another todolist

    class methods:
    fromjson() -- return an object of this class from a json
    """

    def fromjson(stepjson, listjson):
        """Return an object of this class from a json

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
            todolist = todolist_mod.TodoList.fromfile(path, name)
        elif name:
            todolist = todolist_mod.TodoList.fromjson(listjson, name)
        else:
            message = 'Found neither path nor name in todolist step'
            raise ConfigValueError(message)
        return ListStep(todolist)

    def __init__(self, todolist):
        """Constructor

        arguments:
        todolist -- the todolist item for this step
        """
        self.todolist = todolist

    def execute(self):
        """Execute this step"""
        self.todolist.execute()
