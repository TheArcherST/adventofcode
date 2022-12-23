import time
from typing import Optional

from fastaoc import AdventOfCodePuzzle

from utils.vector import Vector


RENDER = False


MAX_VEC_LENGTH = Vector((0, 0), (1, 1)).len()
# vector length in following case
# . T
# H .
# if vector len is lager, we detect that 
# requires update of tail.


SPEC_LENGTH = Vector((0, 0), (2, 2)).len()


# this case not desribed in first part of task...


def _build_point_map(points: list[Vector], shape: tuple[Vector, Vector]) -> list[list[Optional[Vector]]]:
    points = points
    result: list[list[Optional[Vector]]] = [
        [
            None
            for _ in range(shape[1].x - shape[0].x + 1)
        ]
        for _ in range(shape[1].y - shape[0].y + 1)
    ]

    for i in points:
        norm_y, norm_x = i.y - shape[0].y, i.x - shape[0].y

        if result[norm_y][norm_x] is None:
            result[norm_y][norm_x] = i

    return result


def _print_points(points, shape):
    for row in reversed(_build_point_map(points, shape)):
        for i in row:
            if i is None:
                print('.', end=' ')
            else:
                print(i.__dict__.get('label', '#'), end=' ')
        print()


def resolve_physics(head: Vector, tail: Vector):
    """Resolve physics method
    
    Update pair of nodes, by finding shortest move vector length.
    Also, checks if update is need. Returns True on update.
    
    """

    if not ((head - tail).len() > MAX_VEC_LENGTH):
        return False

    new_tail = None
    best_movement_len = float('inf')

    if (head - tail).len() != SPEC_LENGTH:
        cases = ((1, 0), (0, 1), (-1, 0), (0, -1))
    else:
        cases = ((1, 1), (-1, -1), (-1, 1), (1, -1))

    for i in cases:
        if (movement_len := Vector(tail, head + i).len()) < best_movement_len:
            new_tail = head + i
            best_movement_len = movement_len

    tail.x, tail.y = new_tail

    return True


class Solution(AdventOfCodePuzzle):
    def __init__(self):
        self.visited = set()

    def task_1(self, data):

        """Some task solution

        :input 1:
            R 4
            U 4
            L 3
            D 1
            R 4
            D 1
            L 5
            R 2
        :output 1:
            13

        """
        tail, head = (Vector(0, 0), Vector(0, 0))
        visited = {tuple(tail)}
        for i in data.strip().split('\n'):
            direction, count = i.split()
            count = int(count)
            offset = {
                'L': (-1, 0),
                'R': (1, 0),
                'U': (0, 1),
                'D': (0, -1)
            }[direction]

            for i in range(count):
                head += offset
                resolve_physics(head, tail)
                visited.add(tuple(tail))

        return str(len(visited))

    def task_2(self, data):

        """Some task solution

        :input 1:
            R 5
            U 8
            L 8
            D 3
            R 17
            D 10
            L 25
            U 20
        :output 1:
            36

        """
        nodes_count = 10  # H + 1..9
        nodes = [Vector(0, 0) for _ in range(nodes_count)]

        def node_labels():
            yield 'H'
            yield from map(str, range(1, 10))

        for i, l in zip(nodes, node_labels()):
            i.label = l

        visited = {tuple(nodes[0])}
        for i in data.strip().split('\n'):
            direction, count = i.split()
            count = int(count)
            offset = {
                'L': (-1, 0),
                'R': (1, 0),
                'U': (0, 1),
                'D': (0, -1)
            }[direction]

            shape = (Vector(-5, -10) - (5, 5), Vector(15, 10) + (5, 5))

            for _ in range(count):
                nodes[0] += offset

                for j in range(len(nodes) - 1):

                    is_updated = resolve_physics(nodes[j], nodes[j + 1])

                    if RENDER:
                        _print_points(nodes, shape)
                        print()
                        print()
                        time.sleep(0.05)

                    if not is_updated:
                        break

                visited.add(tuple(nodes[-1]))

        return str(len(visited))
