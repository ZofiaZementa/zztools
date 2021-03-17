import configfilemanager
from exceptions import ConfigValueError
import utilities.executor


class PackageManager():
    """Provides an interface to a real world packagemanager

    This class provides an interface to a real world packagemanager like dnf
    or apt.

    class methods:
    fromjson() -- Returns a PackageManager object from json
    fromfile() -- Returns a PackageManager object from a file
    multiplefromjson() -- Returns multiple PackageManager objects from json
    multiplefromfile() -- Returns multiple PackageManager objects from a file

    instance methods:
    _executecommand() -- executes a command
    install() -- Installs the given packages
    uninstall() -- Uninstalls the given packages

    instance variables:
    name -- the name of the packagemanager
    command -- the base command of the packagemanager
    install_command -- the install command of the packagemanager
    uninstall_command -- the uninstall command of the packagemanager
    accept -- the accept part of the packagemanager command
    sudo -- whether to put sudo in front of the command or not
    """

    def fromjson(json, name=None):
        """Returns a PackageManager object from the given json

        arguments:
        json -- the json of the whole packagemanager file already imported into
                python
        name -- the name of the packagemanager in the json, if none is provided,
                it is assumed that there is only one packagemanager in the json,
                if not, an error is thrown (default None)

        exceptions:
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        ConfigValueError -- if some attribute in the config has an invalid value
                            this error contains an attribute \"message\", which
                            contains the errormessage
        """
        if name is None:
            if len(json) == 1:
                name = len(json)[0]
            else:
                messake = 'No name for packagemanager was provided and ' \
                        'there were more than one packagemanager in the file'
                raise ConfigValueError(message)
        try:
            json_pm = json[name]
        except KeyError as e:
            e.message = 'Packagemanager {} could not be found'.format(name)
            raise
        try:
            install_command = json_pm['install']
            uninstall_command = json_pm['uninstall']
            sudo = json_pm['sudo']
        except KeyError as e:
            e.message = 'Attribute {} of packagemanager {} could not pe found'.format(e.args[0], name)
            raise
        return PackageManager(name, install_command, uninstall_command,  sudo)

    def fromfile(path, name=None):
        """Returns a TodoList object from the given file

        The contents of the file are converted to json by the configfilemanager,
        the real content of the file could be in json, yaml or something
        similar.

        arguments:
        path -- the path to the file containing the packagemanager
        name -- the name of the packagemanager in the json, if none is provided,
                it is assumed that there is only one packagemanager in the json,
                if not, an error is thrown (default None)

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
            e.message = 'File with packagemanagers at {} could not be found'.format(path)
            raise
        try:
            packagemanager = PackageManager.fromjson(json)
        except (KeyError, ConfigValueError) as e:
            e.message += 'at {}'.format(path)
            e.filename = path
            raise
        return packagemanager

    def multiplefromjson(json, names=None):
        """Returns multiple PackageManager object from the given json

        arguments:
        json -- the json of the whole packagemanager file already imported into
                python
        names -- the names of the packagemanagers in the json, if none are
                provided, all todolists in the json are imported (default None)

        exceptions:
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        ConfigValueError -- if some attribute in the config has an invalid value
                            this error contains an attribute \"message\", which
                            contains the errormessage
        """
        if not names:
            return [PackageManager.fromjson(json, name) for name in json]
        else:
            return [PackageManager.fromjson(json, name) for name in names]

    def multiplefromfile(path, names=None):
        """Returns multiple PackageManager object from the given json

        The contents of the file are converted to json by the configfilemanager,
        the real content of the file could be in json, yaml or something
        similar.

        arguments:
        path -- the path to the file containing the packagemanagers
        names -- the names of the packagemanagers in the json, if none are
                provided, all todolists in the json are imported (default None)

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
            e.message = 'File with packagemanagers at {} could not be found'.format(path)
            raise
        try:
            packagemanagers = PackageManager.multiplefromjson(json, names)
        except (KeyError, ConfigValueError) as e:
            e.message += 'at {}'.format(path)
            e.filename = path
            raise
        return packagemanagers

    def __init__(self, name, install_command, uninstall_command, sudo):
        """Constructor

        arguments:
        name -- the name of the packagemanager
        install_command -- the install command of the packagemanager
        uninstall_command -- the uninstall command of the packagemanager
        sudo -- whether to put sudo in front of the command or not
        """
        self.name = name
        self.install_command = install_command
        self.uninstall_command = uninstall_command
        self.sudo = sudo

    def _executecommand(self, command, override_sudo=None):
        """Executes the given command with the proper sudo setting

        arguments:
        command -- a list of the parts of the command seperated at the spaces
                   as strings
        override_sudo -- if None, it doesnt override the sudo setting in the
                         class, if true or false, it uses/doesnt use sudo
                         accordingly (default None)
        """
        if override_sudo is None:
            sudo =self.sudo
        else:
            sudo = override_sudo
        utilities.executor.execute_command(command, sudo=sudo)


    def install(self, packages, override_sudo=None):
        """Install the given packages

        arguments:
        packages -- a list of all the packages to install as strings
        override_sudo -- if None, it doesnt override the sudo setting in the
                         class, if true or false, it uses/doesnt use sudo
                         accordingly (default None)
        """
        if packages:
            command = '{} {}'.format(self.install_command, ' '.join(packages))
            self._executecommand(command, override_sudo)


    def uninstall(self, packages, override_sudo=None):
        """Uninstall the given packages

        arguments:
        packages -- a list of all the packages to uninstall as strings
        override_sudo -- if None, it doesnt override the sudo setting in the
                         class, if true or false, it uses/doesnt use sudo
                         accordingly (default None)
        """
        if packages:
            command = '{} {}'.format(self.uninstall_command, ' '.join(packages))
            self._executecommand(command, override_sudo)
