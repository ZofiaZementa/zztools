

class Step():
    """A step in a Todolist

    This is an \"abstract\" class, it should not be instanciated.
    All subclasses should implement the following methods:

    fromjson() -- return an object of that class or a child class from the
                      given json of the step

    Additionally, each step that can be instantiated should have a constructor
    that allows it to be created without a json and an execute(self) method,
    which executes the step.

    class methods:
    fromjson() -- Return a Step object of a child step
    """
