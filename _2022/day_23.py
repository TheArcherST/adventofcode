import itertools

from fastaoc import AdventOfCodePuzzle
from utils.coordinates import Coordinates
from utils.algebra import coordinates_sum


def get_area(points):
    line_x = (min(i[0] for i in points), max(i[0] for i in points) + 1)
    line_y = (min(i[1] for i in points), max(i[1] for i in points) + 1)
    return line_x, line_y


def draw(points):
    area = get_area(points)
    for y in range(area[1][0], area[1][1]+1):
        print(y, end='\t')
        for x in range(area[0][0], area[0][1]+1):
            if (x, y) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            .. raw:: txt

                ....#..
                ..###.#
                #...#.#
                .#...##
                #.###..
                ##.#.##
                .#..#..
        :output 1:
            110

        """

        points: set[Coordinates] = set()

        for ni, i in enumerate(data.strip().split('\n')):
            for nj, j in enumerate(i):
                if j == '#':
                    points.add(Coordinates(nj, ni))

        moves = [
            (((0, -1), (1, -1), (-1, -1)), (0, -1)),
            (((0, 1), (1, 1), (-1, 1)), (0, 1)),
            (((-1, 0), (-1, 1), (-1, -1)), (-1, 0)),
            (((1, 0), (1, 1), (1, -1)), (1, 0))
        ]

        check_area = set(itertools.product((0, 1, -1), (0, 1, -1))) - {(0, 0)}

        def switch_move():
            moves.append(moves.pop(0))

        for _ in range(10):
            baked = points.copy()
            moves_to_exec: dict[Coordinates, set[tuple[int, int]]] = dict()

            for i in baked:
                if all(i + j not in baked for j in check_area):
                    continue

                for conditions_offset, offset in moves:

                    for c in conditions_offset:
                        if i + c in baked:
                            break
                    else:
                        if i not in moves_to_exec:
                            moves_to_exec[i] = set()
                        moves_to_exec[i].add(offset)
                        break

            obtained: dict[tuple[int, int], int] = dict()

            for from_, offsets in moves_to_exec.items():
                target = Coordinates(obj=from_)
                for i in offsets:
                    target += i

                target = tuple(target)

                obtained[target] = obtained.get(target, 0) + 1

            for from_, offsets in moves_to_exec.items():
                target = Coordinates(obj=from_)

                for i in offsets:
                    target += i

                if obtained[tuple(target)] == 1:
                    points.remove(from_)
                    points.add(target)

            switch_move()

        area = get_area(points)
        draw(points)
        area_s = (area[0][1]-area[0][0]) * (area[1][1]-area[1][0])
        return str(area_s - len(points))

    def task_2(self, data):

        """Some task solution

        :input 1:
            .. raw:: txt

                ....#..
                ..###.#
                #...#.#
                .#...##
                #.###..
                ##.#.##
                .#..#..
        :output 1:
            20

        """

        points: set[Coordinates] = set()

        for ni, i in enumerate(data.strip().split('\n')):
            for nj, j in enumerate(i):
                if j == '#':
                    points.add(Coordinates(nj, ni))

        moves = [
            (((0, -1), (1, -1), (-1, -1)), (0, -1)),
            (((0, 1), (1, 1), (-1, 1)), (0, 1)),
            (((-1, 0), (-1, 1), (-1, -1)), (-1, 0)),
            (((1, 0), (1, 1), (1, -1)), (1, 0))
        ]

        check_area = set(itertools.product((0, 1, -1), (0, 1, -1))) - {(0, 0)}

        def switch_move():
            moves.append(moves.pop(0))
        counter = 0
        while True:
            counter += 1
            baked = points.copy()
            moves_to_exec: dict[Coordinates, set[tuple[int, int]]] = dict()

            for i in baked:
                if all(i + j not in baked for j in check_area):
                    continue

                for conditions_offset, offset in moves:

                    for c in conditions_offset:
                        if i + c in baked:
                            break
                    else:
                        if i not in moves_to_exec:
                            moves_to_exec[i] = set()
                        moves_to_exec[i].add(offset)
                        break

            obtained: dict[tuple[int, int], int] = dict()

            for from_, offsets in moves_to_exec.items():
                target = Coordinates(obj=from_)
                for i in offsets:
                    target += i

                target = tuple(target)

                obtained[target] = obtained.get(target, 0) + 1

            for from_, offsets in moves_to_exec.items():
                target = Coordinates(obj=from_)

                for i in offsets:
                    target += i

                if obtained[tuple(target)] == 1:
                    points.remove(from_)
                    points.add(target)
            if baked == points:
                break
            else:
                switch_move()

        return str(counter)
