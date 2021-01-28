import sys
import subprocess


def execute_command(command, sudo=False):
    """Executes the given command, with sudo of the given value

    arguments:
    command -- the command which to execute
    sudo -- whether or not to use sudo (default: False)
    """
    command = command.split(' ')
    if sudo:
        command = ['sudo'] + command
    subprocess.run(command, stderr=sys.stderr)
