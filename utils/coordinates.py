from typing import overload, Iterator, TypeVar
from copy import copy

from .algebra import ScalarAlias, CoordinatesAlias


T = TypeVar('T')


class Coordinates(CoordinatesAlias):
    """
    Coordinates object
    """

    __slots__ = ('x', 'y')

    @overload
    def __init__(self, obj: CoordinatesAlias):
        pass

    @overload
    def __init__(self, x: ScalarAlias, y: ScalarAlias):
        pass

    def __init__(self,
                 x: ScalarAlias = None,
                 y: ScalarAlias = None,
                 obj: CoordinatesAlias = None):

        if obj is not None:
            x, y = obj

        self.x = x
        self.y = y

    def __getitem__(self, index: int) -> ScalarAlias:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError(f"Coordinate object has no scalar value with index {index!r}")

    def __iter__(self) -> Iterator[ScalarAlias]:
        return iter((self.x, self.y))

    def __add__(self: T, other: CoordinatesAlias) -> T:
        result = copy(self)

        other_x, other_y = other

        result.x += other_x
        result.y += other_y

        return result

    def __iadd__(self, other: CoordinatesAlias):
        other_x, other_y = other

        self.x += other_x
        self.y += other_y

        return self

    def __sub__(self: T, other: CoordinatesAlias) -> T:
        result = copy(self)

        other_x, other_y = other

        result.x -= other_x
        result.y -= other_y

        return result

    def __isub__(self, other: CoordinatesAlias):
        other_x, other_y = other

        self.x -= other_x
        self.y -= other_y

        return self

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'Coordinates({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]
