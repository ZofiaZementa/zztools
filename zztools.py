import os
import argparse
import sys
import warnings

from todolist import TodoList
from packagemanager import PackageManager
from collection import Collection
import pseudopackages
from exceptions import ConfigValueError, UnsupportedFileTypeError
import utilities.executor
import utilities.usertextio


def _collectionsfromargs(args):
    try:
        pseudopackags = pseudopackages.getpackagesfromfile(args.pseudopackages_file)
        packagemanagers = PackageManager.multiplefromfile(args.packagemanager_file, \
                args.packagemanagers)
        collections = Collection.multiplefromfile(args.collection_file, \
                pseudopackags, packagemanagers, args.collections)
    except (KeyError, FileNotFoundError) as e:
        errstr = 'Unknown {} while importing the todolist(s)'.format(type(e))
        print('Error: ' + getattr(e, 'message', errstr), file=sys.stderr)
        sys.exit(1)
    return collections


def _commandfunctionmapping(key=None):
    mapping = {None: None, 'execute': execute, 'install': install, 'uninstall': uninstall}
    return mapping[key]


def execute(args):
    try:
        todolists = TodoList.multiplefromfile(args.file, args.todolists)
    except (KeyError, FileNotFoundError, UnsupportedFileTypeError, \
            ConfigValueError) as e:
        errstr = 'Unknown {} while importing the todolist(s)'.format(type(e))
        print('Error: ' + getattr(e, 'message', errstr), file=sys.stderr)
        sys.exit(1)
    for todolist in todolists:
        todolist.execute()


def install(args):
    collections = _collectionsfromargs(args)
    try:
        collections = _collectionsfromargs(args)
    except (KeyError, FileNotFoundError, UnsupportedFileTypeError, \
            ConfigValueError) as e:
        errstr = 'Unknown {} while importing the collection(s)'.format(type(e))
        print('Error: ' + getattr(e, 'message', errstr), file=sys.stderr)
        sys.exit(1)
    for collection in collections:
        collection.install()


def uninstall(args):
    collections = _collectionsfromargs(args)
    try:
        collections = _collectionsfromargs(args)
    except (KeyError, FileNotFoundError, UnsupportedFileTypeError, \
            ConfigValueError) as e:
        errstr = 'Unknown {} while importing the collection(s)'.format(type(e))
        print('Error: ' + getattr(e, 'message', errstr), file=sys.stderr)
        sys.exit(1)
    for collection in collections:
        collection.uninstall()

def _parser():
    parser = argparse.ArgumentParser('zztools', \
            description='Install packages and execute' \
            'commands based on a todolist in a json')
    parser.add_argument('-q', '--quiet', \
            action='store_true', \
            help='output to stdout is supressed', \
            dest='quiet')
    subparser_action = parser.add_subparsers(title='actions', \
            dest='action', \
            help='')
    parser_action_execute = subparser_action.add_parser('execute', \
            description='Executes the given todolists')
    parser_action_execute.add_argument('-f', '--file', \
            required=True, \
            help='specifies the file containing the todolist(s)', \
            dest='file')
    parser_action_execute.add_argument('todolists', \
            nargs='*', \
            help='specifies the todolists and order which to install', \
            metavar='TODOLIST')
    packagemanager_sudo_group = parser.add_mutually_exclusive_group()
    packagemanager_sudo_group.add_argument('--sudo', \
            action='store_true', \
            help='override the sudo value for all packagemanagers', \
            dest='sudo')
    packagemanager_sudo_group.add_argument('--no-sudo', \
            action='store_false', \
            help='override the sudo value for all packagemanager', \
            dest='sudo')
    packagemanager_parser = argparse.ArgumentParser(add_help=False)
    packagemanager_parser.add_argument('-c', '--collection-file', \
            required=True, \
            help='specifies the file with the collections', \
            metavar='FILE', \
            dest='collection_file')
    packagemanager_parser.add_argument('-m', '--packagemanager-file', \
            required=True, \
            help='specifies the file with the packagemanagers', \
            metavar='FILE', \
            dest='packagemanager_file')
    packagemanager_parser.add_argument('-p', '--package-file', \
            required=True, \
            help='specifies the file with the packages', \
            metavar='FILE', \
            dest='pseudopackages_file')
    packagemanager_parser.add_argument('-g', '--packagemanager-list', \
            nargs='+', \
            help='use only the packagemanagers in the order given in the list', \
            metavar='PACKAGEMANAGER', \
            dest='packagemanagers')
    packagemanager_parser.add_argument('-l', '--collection-list', \
            nargs='+', \
            help='use only the collections given in the list', \
            metavar='COLLECTION', \
            dest='collections')
    parser_action_install = subparser_action.add_parser('install', \
            description='Installs the given collections', \
            parents=[packagemanager_parser])
    parser_action_uninstall = subparser_action.add_parser('uninstall', \
            description='Uninstalls the given collections', \
            parents=[packagemanager_parser])
    return parser


def _handle_general_args(args):
    """Handles the general arguments given to the program"""
    if args.sudo is not None:
        utilities.executor.override_sudo = args.sudo
    if args.quiet:
        utilities.usertextio.override_quiet = args.quiet


def _main():
    args = _parser().parse_args()
    _handle_general_args(args)
    function = _commandfunctionmapping(args.action)
    if not function:
        _parser().print_usage(file=sys.stderr)
    else:
        function(args)


def _clean_formatwarning(message, category, filename, lineno, line=None):
    """Monkeypatch for the formatwarning method of warnings

    This ist there to output nice looking warnings
    """
    return 'Warning: ' + str(message) + '\n'

#Monkeypatch to output nice looking warnings
warnings.formatwarning = _clean_formatwarning

if __name__ == '__main__':
    _main()
