

class Step():
    """A step in a Todolist

    This is an \"abstract\" class, it should not be instanciated.
    All subclasses should implement the following methods:

    fromjson(stepjson, listjson) -- return an object of that class or a child
                                    class from the given json of the step, where
                                    stepjson is said json and listjson is the
                                    json of the whole list

    Additionally, each step that can be instantiated should have a constructor
    that allows it to be created without a json and an execute(self) method,
    which executes the step.
    """
