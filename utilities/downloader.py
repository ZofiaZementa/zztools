from .executor import execute_command

def download(url, todir=None, tofile=None):
    """Download a given url

    arguments:
    url -- the url which to download
    todir -- the path to the directory to download to
    tofile -- the path to the file to download to
    """
    if todir:
        command = 'wget -P {} {}'.format(todir, url)
    elif tofile:
        command = 'wget -O {} {}'.format(tofile, url)
    execute_command(command)
