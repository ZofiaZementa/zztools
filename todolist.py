import steps as Steps
import configfilemanager
from exceptions import ConfigValueError


class TodoList():
    """A List of steps which can be executed

    class methods:
    fromjson() -- returns a TodoList object from json
    fromfile() -- returns a TodoList object from a file
    multiplefromjson() -- returns multiple TodoList objects from json
    multiplefromfile() -- returns multiple TodoList objects from a file

    instance methods:
    execute() -- executes the todolist

    instance variables:
    name -- the name of the todolistu
    steps -- a list/tuple of the steps of the todolist
    """

    def fromjson(json, name=None):
        """Returns a TodoList object from the given json

        arguments:
        json -- the json of the whole todolist file already imported into python
        name -- the name of the todolist in the json, if none is provided, it
                is assumed that there is only one todolist in the json, if not,
                an error is thrown (default None)

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
        if name is None:
            if len(json) == 1:
                name = list(json)[0]
            else:
                message = 'No name for todolist was provided and ' \
                        'there were more than one todolist in the file'
                raise ConfigValueError(message)
        try:
            json_todolist = json[name]
        except KeyError as e:
            e.message = 'Todolist {} could not be found'.format(name)
            raise
        steps = [Steps.fromjson(json_step) for json_step in json_todolist]
        return TodoList(steps)

    def fromfile(path, name=None):
        """Returns a TodoList object from the given file

        The contents of the file are converted to json by the configfilemanager,
        the real content of the file could be in json, yaml or something
        similar.

        arguments:
        path -- the path to the file containing the todolist
        name -- the name of the todolist in the json, if none is provided, it
                is assumed that there is only one todolist in the json, if not,
                an error is thrown (default None)

        execptions:
        FileNotFoundError -- if the file at the given path is not found
                             this error contains an attribute \"message\", which
                             contains the errormessage
        UnsupportedFileTypeError -- if the file has the wrong type (extension)
                                    this error contains an attribute
                                    \"message\", which contains the
                                    errormessage and an attribute filename
                                    which contains the message
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        ConfigValueError -- if some attribute in the config has an invalid value
                            this error contains an attribute \"message\", which
                            contains the errormessage
        """
        try:
            json = configfilemanager.getconfigfromfile(path)
        except FileNotFoundError as e:
            e.message = 'File with todolists at {} could not be found'.format(e.filename)
            raise
        try:
            todolist = fromjson(json)
        except (KeyError, ConfigValueError) as e:
            e.message = e.message + ' at {}'.format(path)
            e.filename = path
            raise
        return todolist

    def multiplefromjson(json, names=None):
        """Returns multiple TodoList objects from the given file

        arguments:
        json -- the json of the whole todolist file already imported into python
        names -- the names of the todolists in the json, if none are provided,
                 all todolists in the json are imported (default None)

        exceptions:
        FileNotFoundError -- if the file at the given path is not found
                             This error comes from the collections and similar
                             objects which have seperate config files
                             this error contains an attribute \"message\", which
                             contains the errormessage
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        ConfigValueError -- if some attribute in the config has an invalid value
                            this error contains an attribute \"message\", which
                            contains the errormessage
        """
        if not names:
            return [TodoList.fromjson(json, name) for name in json]
        else:
            return [TodoList.fromjson(json, name) for name in names]

    def multiplefromfile(path, names=None):
        """Returns multiple TodoList objects from the given file

        The contents of the file are converted to json by the configfilemanager,
        the real content of the file could be in json, yaml or something
        similar.

        arguments:
        path -- the path to the file containing the todolists
        names -- the names of the todolists in the json, if none are provided,
                all todolists in the json are imported (default None)

        execptions:
        FileNotFoundError -- if the file at the given path is not found
                             This error comes from the collections and similar
                             objects which have seperate config files
                             this error contains an attribute \"message\", which
                             contains the errormessage
        UnsupportedFileTypeError -- if the file has the wrong type (extension)
                                    this error contains an attribute
                                    \"message\", which contains the
                                    errormessage and an attribute filename
                                    which contains the message
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        ConfigValueError -- if some attribute in the config has an invalid value
                            this error contains an attribute \"message\", which
                            contains the errormessage
        """
        try:
            json = configfilemanager.getconfigfromfile(path)
        except FileNotFoundError as e:
            e.message = 'File with todolists at {} could not be found'.format(e.filename)
            raise
        try:
            todolists = TodoList.multiplefromjson(json, names)
        except (KeyError, ConfigValueError) as e:
            e.message += ' at {}'.format(path)
            e.filename = path
            raise
        return todolists

    def __init__(self, steps):
        """Constructor

        arguments:
        steps -- a list/tuple of the steps which to execute
        """
        self.steps = steps

    def execute(self):
        """Executes the steps of this todolist in order"""
        for step in self.steps:
            step.execute()
