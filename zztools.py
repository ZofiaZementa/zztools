import os
import argparse
import sys

from todolist import TodoList
from packagemanager import PackageManager
from collection import Collection
import pseudopackages


def _collectionsfromargs(args):
    pseudopackags = pseudopackages.getpackagesfromfile(args.pseudopackages_file)
    packagemanagers = PackageManager.multiplefromfile(args.packagemanager_file, \
            args.packagemanagers)
    return Collection.multiplefromfile(collection_file, pseudopackags, \
            packagemanagers, collections)


def _commandfunctionmapping(key=None):
    mapping = {'execute': execute, 'install': install, 'uninstall': uninstall}
    if not key:
        return mapping
    else:
        return mapping[key]


def execute(args):
    todolists = TodoList.multiplefromfile(args.file, args.todolists)
    for todolist in todolists:
        todolist.execute()


def install(args):
    collections = _collectionsfromargs(args)
    for collection in collections:
        collection.install()


def uninstall(args):
    collections = _collectionsfromargs(args)
    for collection in collections:
        collection.uninstall()


def parseargs():
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
    packagepanager_parser = argparse.ArgumentParser(add_help=False)
    packagepanager_parser.add_argument('-c', '--collection-file', \
            required=True, \
            help='specifies the file with the collections', \
            metavar='FILE', \
            dest='collection_file')
    packagepanager_parser.add_argument('-m', '--packagemanager-file', \
            required=True, \
            help='specifies the file with the packagemanagers', \
            metavar='FILE', \
            dest='packagemanager_file')
    packagepanager_parser.add_argument('-p', '--package-file', \
            required=True, \
            help='specifies the file with the packages', \
            metavar='FILE', \
            dest='pseudopackages_file')
    packagepanager_parser.add_argument('-g', '--packagemanager-list', \
            nargs='+', \
            help='use only the packagemanagers in the order given in the list', \
            metavar='PACKAGEMANAGER', \
            dest='packagemanagers')
    packagepanager_parser.add_argument('-l', '--collection-list', \
            nargs='+', \
            help='use only the collections given in the list', \
            metavar='COLLECTION', \
            dest='collections')
    parser_action_install = subparser_action.add_parser('install', \
            description='Installs the given collections', \
            parents=[packagepanager_parser], \
            add_help=False)
    parser_action_uninstall = subparser_action.add_parser('uninstall', \
            description='Uninstalls the given collections', \
            parents=[packagepanager_parser], \
            add_help=False)
    return parser.parse_args()


def main():
    args = parseargs()
    _commandfunctionmapping(args.action)(args)


if __name__ == '__main__':
    main()
