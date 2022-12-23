from utils.algebra import PointAlias
from typing import overload, Iterable, TypeVar
import abc
from enum import IntEnum


_GridValue = TypeVar('_GridValue')


class IndexNormalizingMode(IntEnum):
    OVERFLOW = 1


class GridImplementation(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def normalize_coordinates(self, index, mode: IndexNormalizingMode = IndexNormalizingMode.OVERFLOW):
        """Resolve coordinates method

        :mode OVERFLOW:
            Cut the both axis by maximum or minimum possible
        :mode CYCLE:
            Out of range value will be mapped as continuation
            of the map within the same axis.

        """

        pass

    @abc.abstractmethod
    def remove_area(self):
        pass
