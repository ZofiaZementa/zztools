from .executor import execute_command

def make(path, target=None, sudo=False):
    """Make the Makefile at the given path

    arguments:
    path -- the path to the Makefile
    target -- target whicht to make (default: None)
    sudo -- whether to install with sudo rights (default: False)
    """
    command = 'make -C {}'.format(path)
    if target:
        command += ' {}'.format(target)
    execute_command(command, sudo)
