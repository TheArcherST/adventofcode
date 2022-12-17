from fastaoc import AdventOfCodePuzzle
import re
from typing import Optional, Literal, NewType
from utils.algebra import (CoordinatesAlias, LineFunctionAlias,
                           coordinates_to_line_function,
                           line_segments_union, line_segments_common)
from enum import Enum
from itertools import combinations


class FunctionOverlayStatus(Enum):
    SINGLE_INTERSECTION = 1
    PARALLEL = 2
    NO_INTERSECTION = 3


QuarterAlias = Literal[1, 2, 3, 4]


def functions_overlay(first: LineFunctionAlias,
                      second: LineFunctionAlias
                      ) -> tuple[FunctionOverlayStatus, Optional[CoordinatesAlias]]:
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

    This function returns combined vector(s). Possible outcomes (FunctionOverlayStatus):
    1. Vectors is intersects. Returns intersection coordinate
    2. Vectors is equals. Returns one combined vector
    3. Vectors never intersects (parallel and not equal). **Return None**

    """

    k1, b1 = first
    k2, b2 = second

    if k1 + k2 == 0:  # mirror functions => one intersection
        y = int((b1 + b2) / 2)
        if k1 > 0:
            x = y - b1
        else:
            x = y - b2
        return FunctionOverlayStatus.SINGLE_INTERSECTION, (x, y)
    else:
        if b1 == b2:  # a1 * y1 == a2 * y2  =>  b1 = b2
            return FunctionOverlayStatus.PARALLEL, None
        else:
            return FunctionOverlayStatus.NO_INTERSECTION, None


FractionAlias = tuple[CoordinatesAlias, CoordinatesAlias, tuple[QuarterAlias, ...]]


def fractions_overlay(first: FractionAlias, second: FractionAlias
                      ) -> tuple[tuple[FractionAlias, ...], Optional[CoordinatesAlias]]:

    """
    Difference with functions_overlay: seconds and first's first
    two args is coordinates. Results automatically cuts.

    To optimize algorithm, we not make true split on intersection. We just return
    the intersection point, and save other in the same form. Lately, we can easy
    iterate over the points, because count of intersections will be very small.
    Changing of fractions structure on parallel intersection is required, because
    count of intersected points can be more than several milliards.

    """

    f1 = coordinates_to_line_function(first[0], first[1])
    f2 = coordinates_to_line_function(second[0], second[1])

    result = functions_overlay(f1, f2)

    # so, we must split infinite vector to lines that corresponds real circles area.
    # there are three cases of result, and there are consequences:

    if result[0] == FunctionOverlayStatus.SINGLE_INTERSECTION:
        # 1. Intersection point found => result we return the single intersection point
        return (first, second), result[1]

    if result[0] == FunctionOverlayStatus.PARALLEL:
        # 2. We found parallel intersection => changing the source lines

        # we can simplify finding because know that |k| = 1
        intersection_x = line_segments_common((first[0][0], first[1][0]), (second[0][0], second[1][0]))
        intersection_y = line_segments_common((first[0][1], first[1][1]), (second[0][1], second[1][1]))

        if not intersection_x or not intersection_y:
            # parallel lines not intersect
            return (first, second), None

        intersection_line = (intersection_x[0], intersection_y[0]), (intersection_x[1], intersection_y[1])

        # note: we not count that intersection can contain only one point. or 10. or 100. I think
        # of course, in some cases it can speed up, but think un most cases it is unnecessary logic.

        first_start, first_end = first[0], first[1]
        second_start, second_end = second[0], second[1]

        first_end = intersection_line[0]
        second_start = intersection_line[1]

        return (
                (first_start, first_end, first[2]),
                (intersection_line[0], intersection_line[1], first[2] + second[2]),
                (second_start, second_end, second[2]),
            ), None

    # 3. There are no intersections with sector. No changes.
    if result[0] == FunctionOverlayStatus.NO_INTERSECTION:
        return (first, second), None

    raise RuntimeError()


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
                if new_fraction := line_segments_union(fraction, j):
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

    def task_2(self, data):

        """Some task solution

        :input 1:
            Sensor at x=2, y=18: closest beacon is at x=-2, y=15
            Sensor at x=9, y=16: closest beacon is at x=10, y=16
            Sensor at x=13, y=2: closest beacon is at x=15, y=3
            Sensor at x=12, y=14: closest beacon is at x=10, y=16
            Sensor at x=10, y=20: closest beacon is at x=10, y=16
            Sensor at x=14, y=17: closest beacon is at x=10, y=16
            Sensor at x=8, y=7: closest beacon is at x=2, y=10
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

        fractions = set()
        beacons = set()
        point_intersection_coordinates: set[tuple[CoordinatesAlias, tuple[QuarterAlias]]] = set()

        for i in data.strip().split("\n"):
            sensor_x, sensor_y, beacon_x, beacon_y = map(lambda m: int(i[m.start():m.end()].split("=")[1]),
                                                         re.finditer(r"[ a-zA-Z]=([-]?[0-9]+)", i))

            beacons.add((beacon_x, beacon_y))
            radius = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

            # lets evaluate the 4 new fractions (for each quarter)
            fraction: FractionAlias
            quarter: QuarterAlias
            for quarter in range(1, 5):
                if quarter == 1:
                    fraction = ((sensor_x + radius, sensor_y - 1),
                                (sensor_x + 1, sensor_y - radius), (1,))
                elif quarter == 2:
                    fraction = ((sensor_x - 1, sensor_y - radius),
                                (sensor_x - radius, sensor_y - 1), (2,))
                elif quarter == 3:
                    fraction = ((sensor_x - radius, sensor_y + 1),
                                (sensor_x - 1, sensor_y + radius), (3,))
                elif quarter == 4:
                    fraction = ((sensor_x + 1, sensor_y + radius),
                                (sensor_x + radius, sensor_y + 1), (4,))
                else:
                    raise RuntimeError()

                if fraction[0] == fraction[1]:
                    point_intersection_coordinates.add((fraction[0], (quarter,)))
                else:
                    fractions.add(fraction)

        final_fractions = set()

        for a, b in combinations(fractions.copy(), 2):
            fractions, point = fractions_overlay(a, b)
            if point is not None:
                point_intersection_coordinates.add((point, a[2] + b[2]))
            else:
                final_fractions.update(fractions)

        del fractions

        quarter_points_intersection_lib: dict[CoordinatesAlias, set[int]] = dict()
        possible_coords = set()
        for i in point_intersection_coordinates:
            for j in final_fractions:
                if not (set(j[2]) & set(i[1])):
                    continue
                else:
                    coord, coord_quarters = i

                    intersection_x = line_segments_common((coord[0], coord[0]), (j[0][0], j[1][0]))
                    if intersection_x is None:
                        continue
                    else:
                        pass

                    if coord not in quarter_points_intersection_lib:
                        quarter_points_intersection_lib.update({coord: set(coord_quarters)})

                    quarter_points_intersection_lib[coord].update(j[2])

                    if len(quarter_points_intersection_lib[coord]) == 4:
                        possible_coords.add(coord)

        for x in range(-2, 25):
            for y in range(-2, 22):
                if (x, y) in possible_coords:
                    print('#',end='')
                else:
                    print('.',end='')
            print()

        # and next, we need to understand which points from possible is empty...
        print(possible_coords)
