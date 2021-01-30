import pseudopackages
from . import step
from packagemanager import PackageManager
from collection import Collection
from exceptions import ConfigValueError


class CollectionStep(step.Step):
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

    def fromjson(stepjson, listjson):
        """Return a Step object of a child step

        Returns an object of a child class of CollectionStep, either a
        CollectionInstallStep or a CollectionUninstallStep

        arguments:
        stepjson -- the json of the whole step already imported into python
        listjson -- the json of the whole list file the step was in

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
            json_command = stepjson['command']
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
            return CollectionUninstallStep(stepjson)
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
