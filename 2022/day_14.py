from fastaoc import AdventOfCodePuzzle

from enum import IntEnum
from typing import Optional
from itertools import islice

from utils.coordinates import Coordinates


class MoveOffset:
    DOWN = Coordinates(1, 0)
    LEFT = Coordinates(0, -1)
    RIGHT = Coordinates(0, 1)


class GridCell(IntEnum):
    AIR = 0
    SEND = 1
    ROCK = 2


SEND_SOURCE = Coordinates(0, 500)


def abs_range(*args, addition: int = 0):
    if len(args) >= 2:
        start, end, *_ = args
        if start > end:
            args = (end, start+addition, *_)
        else:
            args = (start, end+addition, *_)

    return range(*args)


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            498,4 -> 498,6 -> 496,6
            503,4 -> 502,4 -> 502,9 -> 494,9
        :output 1:
            24

        """

        # to normally use grid indexing, let's normalize `y` coordinates (set most left to zero)

        rocks = []

        y_offset = float('inf')

        max_x = 0
        max_y = 0

        for i in data.strip().split('\n'):
            coordinates = [Coordinates(*map(int, reversed(j.split(',')))) for j in i.split(' -> ')]
            for start, end in zip(coordinates, islice(coordinates, 1, None)):
                for x in abs_range(start.x, end.x, addition=1):
                    for y in abs_range(start.y, end.y, addition=1):
                        y_offset = min(y_offset, y)

                        max_x = max(max_x, x)
                        max_y = max(max_y, y)

                        coordinate = Coordinates(x, y)
                        rocks.append(coordinate)

        grid: list[list[GridCell]] = [
            [GridCell.AIR for _ in range(max_y + 1 - y_offset)]
            for _ in range(max_x + 1)
        ]

        # -   0  1  2 -> y (y is column)
        #
        # 0   0  0  0
        # 1   0  1  0
        # 2   2  2  2
        # |
        # v
        # x (x is row)
        #
        # selecting element for point (x, y): grid[x][y]

        for i in rocks:
            grid[i.x][i.y - y_offset] = GridCell.ROCK

        current_send_coord: Optional[Coordinates] = None
        new_send = True

        ox_range = range(0, max_x + 1)
        oy_range = range(0, max_y - y_offset + 1)

        result = 0

        def prt():
            for _1 in grid:
                for _2 in _1:
                    if _2 is GridCell.AIR:
                        l_ = '.'
                    elif _2 is GridCell.SEND:
                        l_ = 'o'
                    else:
                        l_ = '#'

                    print(l_, end=' ')
                print()
            print('======'*4)

        while True:
            if new_send:
                current_send_coord = SEND_SOURCE - (0, y_offset) + MoveOffset.DOWN
                new_send = False

            for i in (MoveOffset.DOWN, MoveOffset.DOWN+MoveOffset.LEFT, MoveOffset.DOWN+MoveOffset.RIGHT):
                test_send_coord = current_send_coord + i

                if (
                    test_send_coord.x not in ox_range
                    or test_send_coord.y not in oy_range
                ):
                    return str(result)

                test_send_coord_val = grid[test_send_coord.x][test_send_coord.y]

                if test_send_coord_val is GridCell.AIR:
                    current_send_coord = test_send_coord
                    break
                elif test_send_coord_val in (GridCell.ROCK, GridCell.SEND):
                    continue
                else:
                    raise RuntimeError()
            else:
                result += 1
                new_send = True
                grid[current_send_coord.x][current_send_coord.y] = GridCell.SEND

    def task_2(self, data):

        # TODO: fix algorithm. puzzle answer evaluating took 30s.
        # possible optimisation...
        #
        # 1. Getting nearest down surface by indexes sort (optimize iterating over air)
        # 2. `Coordinate` object copying in many places, maybe it is took the most of time
        #     here. First solution: throw it out. Second: make calls in the object that
        #     avoid copying, and use them here.

        """Some task solution

        :input 1:
            498,4 -> 498,6 -> 496,6
            503,4 -> 502,4 -> 502,9 -> 494,9
        :output 1:
            93

        """

        # to normally use grid indexing, let's normalize `y` coordinates (set most left to zero)

        rocks = []

        y_offset = float('inf')

        max_x = 0
        max_y = 0

        for i in data.strip().split('\n'):
            coordinates = [Coordinates(*map(int, reversed(j.split(',')))) for j in i.split(' -> ')]
            for start, end in zip(coordinates, islice(coordinates, 1, None)):
                for x in abs_range(start.x, end.x, addition=1):
                    for y in abs_range(start.y, end.y, addition=1):
                        y_offset = min(y_offset, y)

                        max_x = max(max_x, x)
                        max_y = max(max_y, y)

                        coordinate = Coordinates(x, y)
                        rocks.append(coordinate)

        y_offset = 0

        grid: list[list[GridCell]] = [
            [GridCell.AIR for _ in range(int((max_y + 1 - y_offset) * 1.5))]
            for _ in range((max_x + 1) + 2)
        ]

        # -   0  1  2 -> y (y is column)
        #
        # 0   0  0  0
        # 1   0  1  0
        # 2   2  2  2
        # |
        # v
        # x (x is row)
        #
        # selecting element for point (x, y): grid[x][y]

        for i in rocks:
            grid[i.x][i.y - y_offset] = GridCell.ROCK

        current_send_coord: Optional[Coordinates] = None
        new_send = True

        ox_range = range(0, max_x + 1)
        oy_range = range(0, max_y - y_offset + 1)

        result = 0

        def prt():
            for _1 in grid:
                for _2 in _1:
                    if _2 is GridCell.AIR:
                        l_ = '.'
                    elif _2 is GridCell.SEND:
                        l_ = 'o'
                    else:
                        l_ = '#'

                    print(l_, end=' ')
                print()
            print('======'*4)

        while True:
            if new_send:
                current_send_coord = SEND_SOURCE - (0, y_offset)

                if grid[current_send_coord.x][current_send_coord.y] is GridCell.SEND:
                    prt()
                    return str(result)

                new_send = False

            for i in (MoveOffset.DOWN, MoveOffset.DOWN+MoveOffset.LEFT, MoveOffset.DOWN+MoveOffset.RIGHT):
                test_send_coord = current_send_coord + i

                if (
                    test_send_coord.x not in ox_range
                    or test_send_coord.y not in oy_range
                ):
                    # return str(result)
                    pass

                if test_send_coord.x == len(grid) - 1:
                    test_send_coord_val = GridCell.ROCK
                else:
                    test_send_coord_val = grid[test_send_coord.x][test_send_coord.y]

                if test_send_coord_val is GridCell.AIR:
                    current_send_coord = test_send_coord
                    break
                elif test_send_coord_val in (GridCell.ROCK, GridCell.SEND):
                    continue
                else:
                    raise RuntimeError()
            else:
                result += 1
                new_send = True
                grid[current_send_coord.x][current_send_coord.y] = GridCell.SEND
