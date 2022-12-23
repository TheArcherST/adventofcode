from utils.algebra import PointAlias
from typing import overload, Iterable, TypeVar
import abc


_GridValue = TypeVar('_GridValue')


class Grid(abc.ABC):
    """The 2D grid standard implementation

    By greed we mean some space, that contains object, indexed
    be coordinates.

    There are two standard ways of keeping grid in the memory.
    As set of points, or as array[array[point]]. There are
    matches to definitions `mapped_grid` and `fractionated_grid`.

    """

    @overload
    def __init__(self, *, mapped_grid: Iterable[Iterable[_GridValue]]):
        pass

    @overload
    def __init__(self, *, fractionated_grid: Iterable[set[PointAlias, _GridValue]]):
        pass

    def __init__(self, *args, **kwargs):
        raise NotImplementedError
