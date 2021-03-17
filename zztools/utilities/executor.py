import types
import sys
import subprocess
import os

from zztools.utilities import usertextio

class Executor(types.ModuleType):

    _override_sudo = None

    def is_sudo_overridden(self) -> bool:
        """returns whether sudo is overridden or not"""
        return self._override_sudo is not None

    @property
    def override_sudo(self):
        """Return the actual value of _override_sudo"""
        return self._override_sudo

    @override_sudo.setter
    def override_sudo(self, sudo):
        """override sudo

        overrides the sudo value given in execute_command with the vaule given
        to this function

        arguments:
        sudo -- what to override sudo with
        """
        self._override_sudo = bool(sudo)

    @override_sudo.getter
    def override_sudo(self) -> bool:
        """returns the vaule of _override_sudo

        exceptions:
        AttributeError -- if override_sudo is not set
        """
        if self.is_sudo_overridden():
            return self._override_sudo
        else:
            message = 'Attribute override_sudo is no set'
            raise AttributeError(message)

    @override_sudo.deleter
    def override_sudo(self):
        """deletes the current value of _override_sudo"""
        self._override_sudo = None

    def execute_command(self, command: str, sudo=False, quiet=False):
        """Executes the given command, with sudo of the given value

        Warning: this functions behavior depends on the value of the override_sudo
        property of this module

        arguments:
        command -- the command which to execute
        sudo -- whether or not to use sudo (default: False)
        quiet -- whether or not to silence stdout (default: False)
        """
        # check if quiet is overridden globally
        if usertextio.is_quiet_overridden():
            quiet = usertextio.override_quiet
        # check whether to execute quietly and apply the set value
        if quiet:
            out = subprocess.DEVNULL
        else:
            out = sys.stdout
        # check whether sudo is overridden globally
        if self.is_sudo_overridden():
            sudo = self.override_sudo
        command = command.split(' ')
        if sudo:
            command = ['sudo'] + command
        subprocess.run(command, stderr=sys.stderr, stdout=out)


# change out the module for the class, so properties can be used
if __name__ != '__main__':
    sys.modules[__name__] = Executor(__name__)
