from __future__ import annotations

from fastaoc import AdventOfCodePuzzle

from enum import IntEnum
from dataclasses import dataclass

from utils.algebra import CoordinatesAlias, coordinates_sum


DIRECTIONS_COUNT = 4


class Direction(IntEnum):
    R = 0
    D = 1
    L = 2
    U = 3

    __move_diffs__ = {
        R: (1, 0),
        D: (0, 1),
        L: (-1, 0),
        U: (0, -1)
    }

    def rotated(self, rotation: Rotation):
        return Direction((self.value + rotation.value) % DIRECTIONS_COUNT)

    def get_move_difference(self):
        return self.__move_diffs__[self.value]


class Rotation(IntEnum):
    R = 1
    L = -1


class Jungle:
    """The jungle class

    Implement the jungle from tasks as an object.

    I sets the jungle by set of the walls and portals, that portals, that wraps the map.
    Walls sets by single coordinate, otherwise, portals sets by dictionary of start/end coordinates.

    Such structure allows processing all search by hash tables. Implied that all coordinates between portals
    and walls is empty points.

    Map indexation rules:

    0 ------> x
    | row
    |
    v c
    y o
      l

    """

    def __init__(self,
                 walls: set[CoordinatesAlias],
                 portals: dict[CoordinatesAlias, CoordinatesAlias],
                 initial_face: Direction = Direction.R,
                 initial_position: CoordinatesAlias = (0, 0)):

        self.walls = walls
        self.portals = portals

        self.face: Direction = initial_face
        self.position = initial_position

    def step_into(self):
        diff = self.face.get_move_difference()
        self.position = coordinates_sum(self.position, diff)

    def rotate(self, rotation: Rotation):
        self.face = self.face.rotated(rotation)


class Tile(IntEnum):
    SPACE = 0
    EMPTY = 1
    WALL = 2

    __literals__ = {
        ' ': SPACE,
        '.': EMPTY,
        '#': WALL
    }

    @classmethod
    def from_literal(cls, literal):
        return Tile(cls.__literals__[literal])


def get_portals(tile_map_expanded: list[list[Tile]]):
    cached = 0
    for row_n, row in enumerate(tile_map_expanded):
        for col_n, tile in enumerate(row):
            current = (col_n, row_n)


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):
        """Some task solution

        :input 1:
            .. raw:: txt

                        ...#
                        .#..
                        #...
                        ....
                ...#.......#
                ........#...
                ..#....#....
                ..........#.
                        ...#....
                        .....#..
                        .#......
                        ......#.

                10R5L5R10L4R5L5
        :output 1:
            6032

        """

        tile_map_str, path = data.split('\n')
        # tile_map_expanded: list[list[Tile]] = []
        lims_x: dict[int, list[int, int]] = {}  # index is x, value is y
        lims_y: dict[int, list[int, int]] = {}  # index is x, value is y
        all_real_points_coordinates: set[PointAlias] = set()

        row_n = -1
        col_n = -1

        for row_n, row_str in enumerate(tile_map_str):
            # tile_map_expanded.append([])
            for col_n, col_literal in enumerate(row_str):
                tile = Tile.from_literal(col_literal)
                # tile_map_expanded[row_n].append(tile)
                if tile is not Tile.SPACE:
                    all_real_points_coordinates.add((col_n, row_n))

        for x in range(col_n + 1):
            lims_x.update({x})

        for y in range(row_n + 1):
            pass

        for row_n, row in enumerate(tile_map_expanded):
            for col_n, col_i in enumerate(row):
                ...


