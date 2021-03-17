from .step import Step
import utilities.executor


class ExecuteStep(Step):
    """A step that executes another program/command

    class methods:
    fromjson() -- returns an ExecuteStep object from json

    instance methods:
    execute() -- executes the step

    instance variables:
    command -- the command as one in a string
    """

    def fromjson(stepjson, listjson):
        """Return an object of this class from a json

        arguments:
        stepjson -- the json of the whole step already imported into python
        listjson -- the json of the whole list file the step was in

        exceptions:
        KeyError -- if a needed attribute in the json is not found
                    this error contains an attribute \"message\", which
                    contains the errormessage
        """
        try:
            command = stepjson['command']
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
        utilities.executor.execute_command(self.command)
