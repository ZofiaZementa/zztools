class UnsupportedFileTypeError(TypeError):
    """If a file has an unsupported type

    Its not really different from TypeError, its just there to differentiate
    between an actual TypeError and this Error.

    instance variables:
    args -- the arguments in order
    message -- the errormessage
    filename -- the path to file which has the wrong format
    """

    def __init__(self, message, filename):
        """Constructor

        arguments:
        message -- the errormessage
        filename -- the path to file which has the wrong format
        """
        self.args = [message, filename]
        self.message = message
        self.filename = filename

class ConfigValueError(ValueError):
    """If a config has an invalid value

    Its not really different from ValueError, its just there to differentiate
    between an actual ValueError and this Error. One may add an attribute
    \"filename\" to this if the error is in a config file

    instance variables:
    args -- the arguments in order
    message -- the errormessage
    """

    def __init__(self, message):
        """Constructor

        arguments:
        message -- the errormessage
        """
        self.args = [message]
        self.message = message
