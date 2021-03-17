import types
import sys


_stdout_save = sys.stdout
_stdout_write_save = sys.stdout.write


def _stdout_write_dummy(*args, **kwargs):
    pass


class UserTextIO(types.ModuleType):

    _override_quiet = None
    _override_yesno = None
    _yesno_answer_map = {'y': True, 'Y': True, 'yes': True, 'Yes': True,
                         'n': False, 'N': False, 'no': False, 'No':False}

    def is_quiet_overridden(self) -> bool:
        """returns whether quiet is overridden or not"""
        return self._override_quiet is not None

    @property
    def override_quiet(self):
        """Return the actual value of _override_quiet"""
        return self._override_quiet

    @override_quiet.setter
    def override_quiet(self, quiet):
        """override quiet

        overrides whether functions should be quiet or not, by setting the
        write function of sys.stdout to _stdout_write_dummy

        arguments:
        quiet -- what to override quiet with
        """
        self._override_quiet = bool(quiet)
        if self._override_quiet:
            sys.stdout.write = _stdout_write_dummy
        else:
            sys.stdout.write = _stdout_write_save

    @override_quiet.getter
    def override_quiet(self) -> bool:
        """returns the vaule of _override_quiet

        exceptions:
        AttributeError -- if override_quiet is not set
        """
        if self.is_quiet_overridden():
            return self._override_yesno
        else:
            message = 'Attribute override_quiet is no set'
            raise AttributeError(message)

    @override_quiet.deleter
    def override_quiet(self):
        """deletes the current value of _override_quiet

        sets the write function of sys.stdout back to the actual function,
        which was saved in _stdout_write_save
        """
        self._override_quiet = None
        sys.stdout = _stdout_save

    def is_yesno_overridden(self) -> bool:
        """returns whether yesno is overridden or not"""
        return self._override_yesno is not None

    @property
    def override_yesno(self):
        """Return the actual value of _override_yesno"""
        return self._override_yesno

    @override_yesno.setter
    def override_yesno(self, yesno):
        """override yesno

        overrides the yes/no questions which would normally be asked

        arguments:
        yesno -- what to override yesno with
        """
        self._override_yesno = bool(yesno)

    @override_yesno.getter
    def override_yesno(self) -> bool:
        """returns the vaule of _override_yesno

        exceptions:
        AttributeError -- if override_yesno is not set
        """
        if self.is_yesno_overridden():
            return self._override_yesno
        else:
            message = 'Attribute override_yesno is no set'
            raise AttributeError(message)

    @override_yesno.deleter
    def override_yesno(self):
        """deletes the current value of _override_yesno"""
        self._override_yesno = None

    def _yesno_choicefield(self, default=False):
        """returns a yesno choice field

        returns a yesno choice field of the form [y/N], depending on default

        arguments:
        default -- which is to be the default, normally No
        """
        field_format = '[{}/{}]'
        if default:
            return field_format.format('Y', 'n')
        else:
            return field_format.format('y', 'N')

    def ask_yesno_question(self, questiontext, default=False) -> bool:
        """Asks the user a question which to answer with yes or no

        Warning: this functions behavior depends on the value of override_yesno
        property of this module, if override_yesno is set, no question will be
        asked, instead the value of override_yesno will be returned

        arguments:
        questiontext -- the text of the question
        default -- the answer which is to be the default, normally No ('N')
        """
        if self.is_yesno_overridden():
            return self.override_yesno
        else:
            text = '{} {}: '.format(questiontext, self._yesno_choicefield(default))
            answer = input(text)
            return self._yesno_answer_map.get(answer, default)

# change out the module for the class, so properties can be used
if __name__ != '__main__':
    sys.modules[__name__] = UserTextIO(__name__)
