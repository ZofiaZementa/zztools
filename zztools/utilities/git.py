import os
import urllib

from git import Repo

from zztools.exceptions import ConfigValueError


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
        reponame = get_repo_name_from_url(url)
        todir = os.path.join(os.getcwd(), reponame)
    Repo.clone_from(url, todir)


def is_git_url(url):
    """Check whether an url is an url to a git repo

    arguments:
    url -- the url which to check
    """
    return url.endswith('.git')


def get_repo_name_from_url(url):
    """Get the repo name from a git url

    arguments:
    url -- the url which to get the name from

    exceptions:
    ValueError -- if the name of the repo cound't be found in the url
    """
    reponame_with_git = os.path.basename(urllib.parse.urlparse(url).path)
    if not reponame_with_git:
        message = 'couldn\'t find name of repository in url {}'.format(url)
        v = ValueError(message)
        v.message = message
        raise v
    return reponame_with_git.removesuffix('.git')
