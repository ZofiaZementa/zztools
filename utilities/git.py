import os
import urllib

from git import Repo

from exceptions import ConfigValueError


def clone(url, todir=None):
    """Clone a repository

    arguments:
    url -- the url to the repo, eiter ssh or https
    todir -- the directory to where to clone the repository, if none is
             specified, it is cloned into the current directory

    exceptions:
    ConfigValueError -- if no todir is given and the name of the repo couldnt
                        be found in the repository url
    """
    if not todir:
        reponame_with_git = os.path.basename(urllib.parse.urlparse(url).path)
        if not reponame_with_git:
            message = 'couldn\'t find name of repository in url {}'.format(url)
            raise ConfigValueError(message)
        reponame = reponame_with_git.removesuffix('.git')
        todir = os.path.join(os.getcwd(), reponame)
    Repo.clone_from(url, todir)
