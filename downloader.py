from executor import execute_command

def download(url, to=None):
    """Download a given url

    arguments:
    url -- the url which to download
    """
    if to:
        command = 'wget -P {} {}'.format(to, url)
    else:
        command = 'wget {}'.format(url)
    execute_command(command)
