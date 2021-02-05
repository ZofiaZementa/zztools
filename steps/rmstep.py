import os
import shutil

from .step import Step


class RmStep(Step):
    """A step that removes something

    this step isn't (yet) intended to be used by the user directly, hence it
    has no fromjson() method

    instance methods:
    execute() -- executes the step
    """

    def __init__(self, path):
        """Constructor

        arguments:
        path -- the path which to delete
        """
        self.path = path

    def execute(self):
        """Execute this step"""
        if os.path.isdir(self.path):
            shutil.rmtree(self.path)
        else:
            os.remove(self.path)
