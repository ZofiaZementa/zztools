from .step import Step


class DummyStep(self):
    """A dummy step that does nothing

    instance methods:
    execute() -- does nothing
    """

    def execute(self):
        pass

    def __bool__(self):
        return False
