import sys

import pseudopackages
from packagemanager import PackageManager
import configfilemanager


class Collection():
    """A collection of pseudopackages

    A Collection is a a collection of pseudopackages which can be installed or
    uninstalled in one go. These pseudopackages dont have to be all from one
    packagemanager, since they are only \"pseudo\"packages.

    class methods:
    fromjson() -- returns a Collection object from json
    fromfile() -- returns a Collection object from a file
    multiplefromfile() -- returns multiple Collection objects from json
    multiplefromjson() -- returns multiple Collection objects from a file

    instance methods:
    getpackages() -- get the packages of the collection
    install() -- install the collection
    uninstall() -- uninstall the collection

    instance variables:
    name -- the name of the collection
    packages_by_pm -- a dict mapping each packagemanager name to a list of
                      tuples, one for each package to install, containing the
                      pseudoname and the actual name in the packagemanager
    pms_by_name -- a dict mapping each packagemanager name to its corresponding
                   PackageManager object
    """

    def fromjson(json, pseudopacks, packagemanagers, name=None):
        """Returns a Collection object from the given json

        arguments:
        json -- the json of the whole collection file already imported into
                python
        pseudopacks -- the psudopackages as imported directly from json into
                       python
        packagemanagers -- a list of PackageManager objects which also specify
                           the order in of which packagemanager to use first
        name -- the name of the collection in the json, if none is provided, it
                is assumed that there is only one collection in the json, if not,
                an error is thrown (default None)
        """
        if name is None:
            if len(json) == 1:
                name = list(json)[0]
            else:
                print('Error: No name for collection was provided and '
                        'there were more than one collection in the file', \
                        file=sys.stderr)
                sys.exit(1)
        try:
            json_collection = json[name]
        except KeyError:
            print('Error: Collection {} could not be found'.format(name), \
                    file=sys.stderr)
            sys.exit(1)
        return Collection(name, json_collection, pseudopacks, packagemanagers)

    def fromfile(path, pseudopacks, packagemanagers, name=None):
        """Returns a TodoList object from the given file

        The contents of the file are converted to json by the configfilemanager,
        the real content of the file could be in json, yaml or something
        similar.

        arguments:
        path -- the path to the file containing the collection
        pseudopacks -- the psudopackages as imported directly from json into
                       python
        packagemanagers -- a list of PackageManager objects which also specify
                           the order in of which packagemanager to use first
        name -- the name of the collection in the json, if none is provided, it
                is assumed that there is only one collection in the json, if not,
                an error is thrown (default None)
        """
        try:
            json = configfilemanager.getconfigfromfile(path)
        except FileNotFoundError:
            print('Error: File with collections could not be found', \
                    file=sys.stderr)
            sys.exit(1)
        return Collection.fromjson(json, pseudopacks, packagemanagers, name)

    def multiplefromjson(json, pseudopacks, packagemanagers, names=None):
        """Returns multiple Collection objects from the given json

        arguments:
        json -- the json of the whole collection file already imported into
                python
        pseudopacks -- the psudopackages as imported directly from json into
                       python
        packagemanagers -- a list of PackageManager objects which also specify
                           the order in of which packagemanager to use first
        name -- the name of the collection in the json, if none is provided, it
                is assumed that there is only one collection in the json, if not,
                an error is thrown (default None)
        """
        if not names:
            return [Collection.fromjson(json, pseudopacks, packagemanagers, \
                    name) for name in json]
        else:
            return [Collection.fromjson(json, pseudopacks, packagemanagers, \
                    name) for name in names]

    def multiplefromfile(path, pseudopacks, packagemanagers, names=None):
        """Returns multiple Collection objects from the given file

        The contents of the file are converted to json by the configfilemanager,
        the real content of the file could be in json, yaml or something
        similar.

        arguments:
        path -- the path to the file containing the collections
        pseudopacks -- the psudopackages as imported directly from json into
                       python
        packagemanagers -- a list of PackageManager objects which also specify
                           the order in of which packagemanager to use first
        name -- the name of the collection in the json, if none is provided, it
                is assumed that there is only one collection in the json, if not,
                an error is thrown (default None)
        """
        try:
            json = configfilemanager.getconfigfromfile(path)
        except FileNotFoundError:
            print('Error: File with collections could not be found', \
                    file=sys.stderr)
            sys.exit(1)
        return Collection.multiplefromjson(json, pseudopacks, packagemanagers, \
                name)

    def __init__(self, name, packages, pseudopacks, packagemanagers):
        """Constructor

        arguments:
        name -- name of this collection
        packages -- list of packagnames as strings which to install
        pseudopacks -- the psudopackages as imported directly from json into
                       python
        packagemanagers -- a list of PackageManager objects which also specify
                           the order in of which packagemanager to use first
        """
        packages_by_pm = {pm.name : dict() for pm in packagemanagers}
        for pseudoname in packages:
            for pm in packagemanagers:
                try:
                    if pm.name in pseudopacks[pseudoname]:
                        packages_by_pm[pm.name][pseudoname] = pseudopacks[pseudoname][pm.name]
                        break
                except KeyError:
                    print('Warnig: Package {} is not available, skipping'.format(pseudoname), \
                            file=sys.stderr)
                    break
            else:
                print('Warning: Package {} has no valid packagemanager, skipping'.format(pseudoname), \
                        file=sys.stderr)
        self.name = name
        self.packages_by_pm = packages_by_pm
        self.pms_by_name = {pm.name : pm for pm in packagemanagers}

    def getpackages(self, packagemanager=None):
        """Get the packages of this collection

        Get the packages of this collection, optionally only the ones to be
        installed with the given packagemanager

        arguments:
        packagemanager -- the packagemanager of which to return the packages
                          if none is provided, all packages are returned,
                          grouped in a dict by the name of their packagemanager
                          (default None)
        """
        if packagemanager is None:
            return self.packages_by_pm
        else:
            return self.packages_by_pm[packagemanager]

    def install(self):
        """Install all the packages of the collection"""
        for pm_name in self.packages_by_pm:
            self.pms_by_name[pm_name].install(list(self.packages_by_pm[pm_name].values()))

    def uninstall(self):
        """Uninstall all the pakages of the collection"""
        for pm_name in self.packages_by_pm:
            self.pms_by_name[pm_name].uninstall(list(self.packages_by_pm[pm_name].values()))
