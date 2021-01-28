from executor import execute_command

def download(url):
    """Download a given url

    arguments:
    url -- the url which to download
    """
    command = '{} {}'.format('wget', url)
    execute_command(command)
