import itertools

from fastaoc import AdventOfCodePuzzle
from utils.vector import Vector
import re
import math
from typing import Optional


def union_fractions(first: tuple, second: tuple):
    """
    (0, 2); (1, 3) -> (0, 3)
    """

    result = min(first[0], second[0]), max(first[1], second[1])
    if range(*result):
        return result
    else:
        return None


def functions_overlay(first: tuple[int, int, tuple[int, ...]],
                      second: tuple[int, int, tuple[int, ...]]) -> Optional[tuple[Optional[int], tuple[int, ...]]]:
    """

    I've review vectors as functions y1 = a1*x + b1 and y2 = a2*x + b2.
    So, pass as two first vector arguments a1 and b1.

    Warning: support only `a` values that excepts the task. It is 1 and -1.

    Thirst argument is a quarter of the barrier. For example:

    ...
    #  v  .  .  .
    .  #  v  .  .
    .  .  #  v  .
    o  .  .  #  v
    .  .  #  .  .
    .  #  .  .  .
    ...

    # - barrier
    v - vector
    o - circle center

    Here, vector have quarter 1. Remember quarter circle:

     2  #  1
     #  o  #
     3  #  4

    This function returns combined vector(s). Possible outcomes:
    1. Vectors is equals. Returns one combined vector.
    2. Vectors is intersects. Returns one combined vector with length 0 (coordinate)
    3. Vectors never intersects (parallel and not equal). **Return None**

    """

    a1, b1, d1 = first
    a2, b2, d2 = second
    d = d1 + d2
    if a1 + a2 == 0:
        y = int((b1 + b2) / 2)
    else:
        if b1 == b2:  # a1 * y1 == a2 * y2  ===>  b1 = b2
            y = None  # any
        else:
            return None  # no intersections

    return y, d


def fractions_overlay(first: tuple[int, int, tuple[int, ...]],
                      second: tuple[int, int, tuple[int, ...]]) -> list[tuple[int, int, tuple[int, ...]]]:
    """
    Difference with functions_overlay: seconds and first's first
    two args is coordinates. Results automatically cuts. Can be returned
    1, 2, 3 different fractions.

    """

    if first[0] < first[1]:
        a = -1
    else:
        a = 1


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            Sensor at x=8, y=7: closest beacon is at x=2, y=10
            Sensor at x=2, y=18: closest beacon is at x=-2, y=15
            Sensor at x=9, y=16: closest beacon is at x=10, y=16
            Sensor at x=13, y=2: closest beacon is at x=15, y=3
            Sensor at x=12, y=14: closest beacon is at x=10, y=16
            Sensor at x=10, y=20: closest beacon is at x=10, y=16
            Sensor at x=14, y=17: closest beacon is at x=10, y=16
            Sensor at x=2, y=0: closest beacon is at x=2, y=10
            Sensor at x=0, y=11: closest beacon is at x=2, y=10
            Sensor at x=20, y=14: closest beacon is at x=25, y=17
            Sensor at x=17, y=20: closest beacon is at x=21, y=22
            Sensor at x=16, y=7: closest beacon is at x=15, y=3
            Sensor at x=14, y=3: closest beacon is at x=15, y=3
            Sensor at x=20, y=1: closest beacon is at x=15, y=3
        :output 1:
            26

        """

        global_y = 2000000

        fractions = set()
        beacons = set()

        for i in data.strip().split("\n"):
            sensor_x, sensor_y, beacon_x, beacon_y = map(lambda m: int(i[m.start():m.end()].split("=")[1]),
                                                         re.finditer(r"[ a-zA-Z]=([-]?[0-9]+)", i))

            beacons.add((beacon_x, beacon_y))
            radius = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

            max_y_coordinate = sensor_y + radius
            min_y_coordinate = sensor_y - radius
            if (global_y < min_y_coordinate) or (global_y > max_y_coordinate):
                continue

            # let's find fraction of sensor's explore circle within specified y

            # find length
            radius_length_at = sensor_y
            diff = abs(radius_length_at - global_y)  # deviation from radius

            offset = radius - diff  # right-left offset of the fraction from middle

            # find start/end x coord
            x_middle = sensor_x
            x_start = x_middle - offset
            x_end = x_middle + offset

            fraction = (x_start, x_end)

            # compare with others, union if need
            for j in fractions:
                if new_fraction := union_fractions(fraction, j):
                    fractions.remove(j)
                    fractions.add(new_fraction)
                    break
            else:
                # compare pair not found
                fractions.add(fraction)

        # count beacons that in the fractions

        intersected_beacons_count = 0

        for i in beacons:
            if i[1] != global_y:
                continue
            for j in fractions:
                if j[0] <= i[0] <= j[1]:
                    intersected_beacons_count += 1

        # and count length of all fractions...

        result = -intersected_beacons_count

        for i in fractions:
            result += abs(i[1] - i[0]) + 1

        return str(result)

    def task_0(self, data):

        """Some task solution

        :input 1:
            Sensor at x=8, y=7: closest beacon is at x=2, y=10
            Sensor at x=2, y=18: closest beacon is at x=-2, y=15
            Sensor at x=9, y=16: closest beacon is at x=10, y=16
            Sensor at x=13, y=2: closest beacon is at x=15, y=3
            Sensor at x=12, y=14: closest beacon is at x=10, y=16
            Sensor at x=10, y=20: closest beacon is at x=10, y=16
            Sensor at x=14, y=17: closest beacon is at x=10, y=16
            Sensor at x=2, y=0: closest beacon is at x=2, y=10
            Sensor at x=0, y=11: closest beacon is at x=2, y=10
            Sensor at x=20, y=14: closest beacon is at x=25, y=17
            Sensor at x=17, y=20: closest beacon is at x=21, y=22
            Sensor at x=16, y=7: closest beacon is at x=15, y=3
            Sensor at x=14, y=3: closest beacon is at x=15, y=3
            Sensor at x=20, y=1: closest beacon is at x=15, y=3
        :output 1:
            26

        """

        global_y = 2000000

        fractions = set()
        beacons = set()

        for i in data.strip().split("\n"):
            sensor_x, sensor_y, beacon_x, beacon_y = map(lambda m: int(i[m.start():m.end()].split("=")[1]),
                                                         re.finditer(r"[ a-zA-Z]=([-]?[0-9]+)", i))

            beacons.add((beacon_x, beacon_y))
            radius = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

            max_y_coordinate = sensor_y + radius
            min_y_coordinate = sensor_y - radius
            if (global_y < min_y_coordinate) or (global_y > max_y_coordinate):
                continue

            # let's find fraction of sensor's explore circle within specified y

            # find length
            radius_length_at = sensor_y
            diff = abs(radius_length_at - global_y)  # deviation from radius

            offset = radius - diff  # right-left offset of the fraction from middle

            # find start/end x coord
            x_middle = sensor_x
            x_start = x_middle - offset
            x_end = x_middle + offset

            fraction = (x_start, x_end)

            # compare with others, union if need
            for j in fractions:
                if new_fraction := union_fractions(fraction, j):
                    fractions.remove(j)
                    fractions.add(new_fraction)
                    break
            else:
                # compare pair not found
                fractions.add(fraction)

        # count beacons that in the fractions

        intersected_beacons_count = 0

        for i in beacons:
            if i[1] != global_y:
                continue
            for j in fractions:
                if j[0] <= i[0] <= j[1]:
                    intersected_beacons_count += 1

        # and count length of all fractions...

        result = -intersected_beacons_count

        for i in fractions:
            result += abs(i[1] - i[0]) + 1

        return str(result)
