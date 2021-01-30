from .step import Step
from executor import execute_command


class ExecuteStep(Step):
    """A step that executes another program/command

    class methods:
    fromjson() -- returns an ExecuteStep object from json

    instance methods:
    execute() -- executes the step

    instance variables:
    command -- the command as one in a string
    """

    def fromjson(json):
        """Return an object of this class from a json

        arguments:
        json -- the json of the whole step already imported into python

        exceptions:
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        """
        try:
            command = json['command']
        except KeyError as e:
            e.message = 'Missing command for execute step'
            raise
        return ExecuteStep(command)

    def __init__(self, command):
        """Constructor

        arguments:
        command -- the command of this step as a string
        """
        self.command = command

    def execute(self):
        """Executes the command of this step"""
        execute_command(self.command)
