from fastaoc import AdventOfCodePuzzle

from typing import Optional
from itertools import islice

from utils.coordinates import Coordinates


SEND_SOURCE = (0, 500)


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

        obtained = set()

        for i in data.strip().split('\n'):
            coordinates = [Coordinates(*map(int, reversed(j.split(',')))) for j in i.split(' -> ')]
            for start, end in zip(coordinates, islice(coordinates, 1, None)):
                for x in abs_range(start.x, end.x, addition=1):
                    for y in abs_range(start.y, end.y, addition=1):

                        obtained.add((x, y))

        max_x = max(*(i[0] for i in obtained))
        max_y = max(*(i[1] for i in obtained))

        current_send_coord = SEND_SOURCE

        result = 0

        while True:
            for x_offset, y_offset in ((1, 0), (1, -1), (1, 1)):

                test_send_coord = (current_send_coord[0] + x_offset,
                                   current_send_coord[1] + y_offset)

                if not (
                    (0 <= test_send_coord[0] <= max_x)
                    and (0 <= test_send_coord[1] <= max_y)
                ):
                    return str(result)

                if test_send_coord not in obtained:
                    current_send_coord = test_send_coord
                    break

            else:
                result += 1
                obtained.add(current_send_coord)
                current_send_coord = SEND_SOURCE

    def task_2(self, data):

        """Some task solution

        :input 1:
            498,4 -> 498,6 -> 496,6
            503,4 -> 502,4 -> 502,9 -> 494,9
        :output 1:
            93

        """

        obtained = set()
        for i in data.strip().split('\n'):
            coordinates = [Coordinates(*map(int, reversed(j.split(',')))) for j in i.split(' -> ')]

            for start, end in zip(coordinates, islice(coordinates, 1, None)):
                for x in abs_range(start.x, end.x, addition=1):
                    for y in abs_range(start.y, end.y, addition=1):
                        obtained.add((x, y))

        result = 0

        barrier_line__x = max(*(i[0] for i in obtained)) + 2
        current_send_coord = SEND_SOURCE

        while True:
            for x_offset, y_offset in (1, 0), (1, -1), (1, 1):  # standard movements **in right order**

                test_send_coord = (current_send_coord[0] + x_offset,
                                   current_send_coord[1] + y_offset)

                if not (test_send_coord in obtained or test_send_coord[0] == barrier_line__x):
                    current_send_coord = test_send_coord
                    break
            else:
                result += 1
                obtained.add(current_send_coord)
                if SEND_SOURCE in obtained:
                    return str(result)
                else:
                    current_send_coord = SEND_SOURCE
