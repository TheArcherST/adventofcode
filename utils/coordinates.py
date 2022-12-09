# source: https://github.com/TheArcherST/terminalGame/blob/main/render/geometry/coordinates.py


from typing import TYPE_CHECKING
from .point import BasePoint

if TYPE_CHECKING:
    from render.geometry.vector import Vector


class Coordinates(BasePoint):
    @property
    def vec(self) -> 'Vector':
        from .vector import Vector
        return Vector(obj=self)
