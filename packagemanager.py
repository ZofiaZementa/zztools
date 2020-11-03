import subprocess
import sys

import configfilemanager


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
        """
        if name is None:
            if len(json) == 1:
                name = len(json)[0]
            else:
                print('Error: No name for packagemanager was provided and '
                        'there were more than one packagemanager in the file', \
                        file=sys.stderr)
                sys.exit(1)
        try:
            json_pm = json[name]
        except KeyError:
            print('Error: Packagemanager {} could not be found'.format(name), \
                    file=sys.stderr)
            sys.exit(1)
        try:
            command = json_pm['command']
            install_command = json_pm['install']
            uninstall_command = json_pm['uninstall']
            accept = json_pm['accept']
            sudo = json_pm['sudo']
        except KeyError as e:
            print('Error: Attribute {} of packagemanager {} could not pe found'.format(e.args[0], name))
            sys.exit(1)
        return PackageManager(name, command, install_command, \
                uninstall_command, accept, sudo)

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
        """
        try:
            json = configfilemanager.getconfigfromfile(path)
        except FileNotFoundError:
            print('Error: File with packagemanagers could not be found', \
                    file=sys.stderr)
            sys.exit(1)
        return PackageManager.fromjson(json)

    def multiplefromjson(json, names=None):
        """Returns multiple PackageManager object from the given json

        arguments:
        json -- the json of the whole packagemanager file already imported into
                python
        names -- the names of the packagemanagers in the json, if none are
                provided, all todolists in the json are imported (default None)
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
        """
        try:
            json = configfilemanager.getconfigfromfile(path)
        except FileNotFoundError:
            print('Error: File with packagemanagers could not be found', \
                    file=sys.stderr)
            sys.exit(1)
        return PackageManager.multiplefromjson(json, names)

    def __init__(self, name, command, install_command, uninstall_command, \
            accept, sudo):
        """Constructor

        arguments:
        name -- the name of the packagemanager
        command -- the base command of the packagemanager
        install_command -- the install command of the packagemanager
        uninstall_command -- the uninstall command of the packagemanager
        accept -- the accept part of the packagemanager command
        sudo -- whether to put sudo in front of the command or not
        """
        self.name = name
        self.command = command
        self.install_command = install_command
        self.uninstall_command = uninstall_command
        self.accept = accept
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
            sudo = self.sudo
        else:
            sudo = override_sudo
        if sudo:
            subprocess.run(['sudo', *command], stderr=sys.stderr)
        else:
            subprocess.run(command, stderr=sys.stderr)


    def install(self, packages, override_sudo=None):
        """Install the given packages

        arguments:
        packages -- a list of all the packages to install as strings
        override_sudo -- if None, it doesnt override the sudo setting in the
                         class, if true or false, it uses/doesnt use sudo
                         accordingly (default None)
        """
        self._executecommand([ self.command, self.install_command, \
                self.accept, *packages], override_sudo)


    def uninstall(self, packages, override_sudo=None):
        """Uninstall the given packages

        arguments:
        packages -- a list of all the packages to uninstall as strings
        override_sudo -- if None, it doesnt override the sudo setting in the
                         class, if true or false, it uses/doesnt use sudo
                         accordingly (default None)
        """
        self._executecommand([self.command, self.uninstall_command, \
                self.accept, *packages], override_sudo)
