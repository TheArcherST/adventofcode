from fastaoc import AdventOfCodePuzzle


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            2,2,2
            1,2,2
            3,2,2
            2,1,2
            2,3,2
            2,2,1
            2,2,3
            2,2,4
            2,2,6
            1,2,5
            3,2,5
            2,1,5
            2,3,5
        :output 1:
            64

        """
        seen = list()
        result = 0
        for i in data.strip().split('\n'):
            x, y, z = map(int, i.split(','))
            tp_coordinate = {(x, 0), (y, 1), (z, 2)}
            result += 6
            for j in seen:
                if len(j & tp_coordinate) == 2:
                    diff = j.symmetric_difference(tp_coordinate)
                    assert len(diff) == 2
                    a, b = diff
                    if abs(a[0] - b[0]) in range(0, 2):
                        result -= 2

            seen.append(tp_coordinate)
        return str(result)

    def task_2(self, data):

        """Some task solution

        To find isolated air, we x-ray each line, and detect,
        if each point is isolated from all directions.

        To split on lines, we match points that have two common
        coordinates.

        :input 1:
            0,0,0
            1,0,2
            1,0,1
            0,2,0
            0,1,0
            1,1,0
            2,1,0
            2,2,1
            2,2,2
            1,2,2
            1,1,2
            2,1,1
            1,2,0
            1,2,1
            0,1,1
            3,1,1
            2,0,1
            2,1,3
            2,0,2
            3,1,3
            3,2,2
        :output 1:
            72

        :input 2:
            2,2,2
            1,2,2
            3,2,2
            2,1,2
            2,3,2
            2,2,1
            2,2,3
            2,2,4
            2,2,6
            1,2,5
            3,2,5
            2,1,5
            2,3,5
        :output 2:
            58

        """

        lines: dict[tuple[int, int, int], list[int]] = dict()
        coords = set()
        for i in data.strip().split('\n'):
            x, y, z = map(int, i.split(','))
            coords.add((x, y, z))
            line_indices = {(0, y, z): x,
                            (1, x, z): y,
                            (2, x, y): z}
            for k, v in line_indices.items():
                if k not in lines:
                    lines[k] = [v]
                else:
                    lines[k].append(v)

        lines = {k: sorted(v) for k, v in lines.items()}
        blocked_points: dict[tuple[int, int, int], list[int]] = dict()

        for line_index, line_axe_values in lines.items():
            line_axis_marker, *line_coordinates = line_index

            for a, b in zip(line_axe_values, line_axe_values[1:]):

                # blocked key is coordinate on current axis, that placed between other shapes

                hole = range(a+1, b)

                for blocked_key in hole:
                    assert len(line_coordinates) == 2

                    if line_axis_marker == 0:
                        point = (blocked_key, *line_coordinates)
                    elif line_axis_marker == 1:
                        point = (line_coordinates[0], blocked_key, line_coordinates[1])
                    elif line_axis_marker == 2:
                        point = (*line_coordinates, blocked_key)
                    else:
                        raise RuntimeError()

                    if point not in blocked_points:
                        blocked_points[point] = [0, 0]

                    blocked_points[point][0] += 1

                    if len(hole) == 1:
                        blocked_points[point][1] += 2
                    elif blocked_key in (a+1, b-1):
                        blocked_points[point][1] += 1

        result = 0

        for k, (blocked_sides_count, possible_square) in blocked_points.items():
            if blocked_sides_count == 3:
                result += possible_square

        return str(int(Solution().task_1(data)) - result)
