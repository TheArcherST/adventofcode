from typing import Dict, Tuple

from .models import TaskResolution
from .utils import docstring_to_tests


class AdventOfCodePuzzle:
    """AdventOfCodePuzzle class

    This classs is container to declare puzzles.


    Puzzle resolution declaration
    -----------------------------

    >>> class Resolution(AdventOfCodePuzzle):
    ...     def task_1(self, data):
    ...         pass

    Here, we initialized class Resolution, that represents puzzle
    resolution for some day. Here, you can declare your tasks resolutions
    in functions, named in match with regex `task_[0-9]`.

    Also, you can specify puzzle date by providing classvars __day__
    and __year__ to class instance, while initializing sublass or later.

    By base class, you can access all sublasses by declarated interface,
    to get tasks for sepcified date, and also to get latest resolution (
    to fastly testing active puzzles)


    Resolution testing
    ------------------

    To create autotests to your alghoritm, declare excepted behaviour
    in function's docstring, using reStructiuredText syntax, pass input
    and output data in following format:

    >>> class Resolution(AdventOfCodePuzzle):
    ...     def task_1(self, data):
    ...         '''
    ...         :input:
    ...             string
    ...         :output:
    ...             resolved-string
    ...         '''
    ...
    ...         return 'resolved-' + data

    You can pass multiply test, by providing multiply input and output fields.

    """

    # public protocol
    __year__ = None
    __day__ = None

    # private protocol
    _resolutions_: Dict[Tuple[int, int, int], TaskResolution] = dict()

    @classmethod
    def register_resolutions(cls):
        """Register resolutions method

        Registering methods, that matched by specified resolution method regex,
        and registering them in static variables of the class. You can call it
        again to update information about solution (this method not making factory
        that synchronized with subclass state)

        """

        for k, func in cls.__dict__.items():
            if k.startswith('task_'):
                if getattr(func, '__doc__', None):
                    tests = docstring_to_tests(func.__doc__)
                else:
                    tests = []

                number = int(k.removeprefix('task_'))
                resolution = TaskResolution(
                    cls.__year__, cls.__day__, number, func, tests
                )
                cls._resolutions_.update({(cls.__year__, cls.__day__, number): resolution})

    @classmethod
    def get_latest(cls) -> TaskResolution:
        return cls._resolutions_[max(cls._resolutions_.keys())]
