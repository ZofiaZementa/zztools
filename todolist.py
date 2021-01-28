import configfilemanager
import pseudopackages
from downloader import download
from executor import execute_command
from packagemanager import PackageManager
from collection import Collection
from exceptions import ConfigValueError


class Step():
    """A step in a Todolist

    This is an \"abstract\" class, it should not be instanciated.
    All subclasses should implement the following methods:

    fromjson() -- return an object of that class or a child class from the
                      given json of the step

    Additionally, each step that can be instantiated should have a constructor
    that allows it to be created without a json and an execute(self) method,
    which executes the step.

    class methods:
    fromjson() -- Return a Step object of a child step
    """

    def fromjson(json):
        """Return a Step object of a child step

        Returns an object of a child class of Step, either a CollectionStep or
        a ExecuteStep

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
            return [Step.fromjson(step) for step in json]
        else:
            try:
                type = json['type']
            except KeyError:
                e.message = 'Missing type in step'
                raise
            if type == 'collection':
                return CollectionStep.fromjson(json)
            elif type == 'execute':
                return ExecuteStep.fromjson(json)
            elif type == 'download':
                return DownloadStep.fromjson(json)
            else:
                message = 'Invalid step type {}'.format(json['type'])
                raise ConfigValueError(message)


class CollectionStep(Step):
    """A step that executes an action on a given collection

    This is an \"abstract\" class, it should not be instanciated.
    All subclasses should implement the following methods:

    fromjson() -- return an object of that class or a child class from the
                      given json of the step

    Additionally, each step that can be instantiated should have a constructor
    that allows it to be created without a json and an execute(self) method,
    which executes the step.
    The constructor is provided by this class and should not be overridden.

    class methods:
    fromjson() -- Returns a Step object of a child step

    instance variables:
    collection -- holds the collection for the step
    """

    def fromjson(json):
        """Return a Step object of a child step

        Returns an object of a child class of CollectionStep, either a
        CollectionInstallStep or a CollectionUninstallStep

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
        try:
            json_command = json['command']
            collection_path = json_command['collection']['path']
            packagemanagers_path = json_command['packagemanagers']['path']
            pseudopackages_path = json_command['pseudopackages']['path']
        except KeyError as e:
            e.message = 'Missing attribute {} in collection step'.format(e.args[0])
            raise
        pseudopacks = pseudopackages.getpackagesfromfile(pseudopackages_path)
        if 'allowed_packagemanagers' in json_command['packagemanagers']:
            packagemanagers = PackageManager.multiplefromfile(packagemanagers_path, \
                    json_command['packagemanagers']['allowed_packagemanagers'])
        else:
            packagemanagers = PackageManager.multiplefromfile(packagemanagers_path)
        if 'name' in json_command['collection']:
            collection = Collection.fromfile(collection_path, pseudopacks, \
                    packagemanagers, name=json_command['collection']['name'])
        else:
            collection = Collection.fromfile(collection_path, pseudopacks, \
                    packagemanagers)
        if json_command['action'] == 'install':
            return CollectionInstallStep(collection)
        elif json_command['action'] == 'uninstall':
            return CollectionUninstallStep(json)
        else:
            message = 'Invalid action type {} for step {}'.format(json_command['action'], \
                    json_command['action'])
            raise ConfigValueError(message)

    def __init__(self, collection):
        """Constructor

        arguments:
        collection -- the collection which this step operates on
        """
        self.collection = collection


class CollectionInstallStep(CollectionStep):
    """A step that installs a given collection

    instance methods:
    execute() -- executes the step
    """

    def execute(self):
        """Installs the collection this step is responsible for"""
        self.collection.install()

class CollectionUninstallStep(CollectionStep):
    """A step that uninstalls a given collection

    instance methods:
    execute() -- executes the step
    """

    def execute(self):
        """Uninstalls the collection this step is responsible for"""
        self.collection.uninstall()

class ExecuteStep(Step):
    """A step that executes another program/command

    class methods:
    fromjson() -- returns an ExecuteStep object from json

    instance methods:
    execute() -- executes the step

    instance variables:
    command -- the command as one in a string
    """

    def fromjson(json):
        """Return an object of this class from a json

        arguments:
        json -- the json of the whole step already imported into python

        exceptions:
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        """
        try:
            command = json['command']
        except KeyError as e:
            e.message = 'Missing command for execute step'
            raise
        return ExecuteStep(command)

    def __init__(self, command):
        """Constructor

        arguments:
        command -- the command of this step as a string
        """
        self.command = command

    def execute(self):
        """Executes the command of this step"""
        execute_command(self.command)


class DownloadStep(Step):

    def fromjson(json):
        """Return an object of this class from a json

        arguments:
        json -- the json of the whole step already imported into python

        exceptions:
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        """
        try:
            command = json['command']
            url = command['url']
        except KeyError as e:
            e.message = 'Missing attribute {} in get step'.format(e.args[0])
            raise
        return DownloadStep(url)

    def __init__(self, url):
        """Constructor

        arguments:
        url -- the url which to download
        tool -- tool which to use to download the url
        """
        self.url = url

    def execute(self):
        """Downloads the url with the given tool"""
        download(self.url)


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
        steps = [Step.fromjson(json_step) for json_step in json_todolist]
        return TodoList(name, steps)

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

    def __init__(self, name, steps):
        """Constructor

        arguments:
        name -- the name of this TodoList
        steps -- a list/tuple of the steps which to execute
        """
        self.name = name
        self.steps = steps

    def execute(self):
        """Executes the steps of this todolist in order"""
        for step in self.steps:
            step.execute()
