from typing import Union, overload

from .aliases import CoordinatesAlias, ScalarAlias, is_scalar
from .coordinates import Coordinates


class Vector(Coordinates):
    """
    Vector object
    """

    __slots__ = ('x', 'y')

    @overload
    def __init__(self, *, obj: CoordinatesAlias):
        pass

    @overload
    def __init__(self,
                 x: Union[ScalarAlias, CoordinatesAlias],
                 y: Union[ScalarAlias, CoordinatesAlias]):

        pass

    def __init__(self,
                 x: Union[ScalarAlias, CoordinatesAlias] = None,
                 y: Union[ScalarAlias, CoordinatesAlias] = None,
                 obj: CoordinatesAlias = None):

        if obj is not None:
            x, y = obj
        else:
            status = is_scalar(x) + is_scalar(y)

            if status not in (0, 2):
                raise ValueError("Can't initialize `Vector`, arguments must be exactly points or scalars")

            elif status == 0:  # no scalar => transformation required
                origin_x, origin_y = x
                target_x, target_y = y
                x, y = (target_x - origin_x, target_y - origin_y)

        super().__init__(x, y)

    def len(self):
        result = (self.x ** 2 + self.y ** 2) ** 0.5

        return result

    def __abs__(self):
        return self.len()

    def __str__(self):
        return '{' + str(self.x) + ', ' + str(self.y) + '}'

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'
