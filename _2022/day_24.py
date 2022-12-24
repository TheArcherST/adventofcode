from fastaoc import AdventOfCodePuzzle

from enum import Enum


class Direction(Enum):
    R = '>'
    D = 'v'
    L = '<'
    U = '^'
    ME = 'E'

    __move_diffs__ = {
        R: (1, 0),
        D: (0, 1),
        L: (-1, 0),
        U: (0, -1)
    }

    def get_move_difference(self):
        return self.__move_diffs__[self.value]


def get_area(points):
    line_x = (min(i[0] for i in points), max(i[0] for i in points) + 1)
    line_y = (min(i[1] for i in points), max(i[1] for i in points) + 1)
    return line_x, line_y


def draw(blizzards: dict[tuple[int, int], list[Direction]]):
    area = get_area(blizzards.keys())
    for y in range(0, area[1][1]):
        print(y, end='\t')
        for x in range(0, area[0][1]):
            if (x, y) in blizzards:
                directions = blizzards[(x, y)]
                if len(directions) == 1:
                    print(directions[0].value, end='')
                else:
                    print(len(directions), end='')
            else:
                print('.', end='')
        print()


def resolve_blizzards_minute(blizzards: dict[tuple[int, int], list[Direction]], min_x, min_y, max_x, max_y):
    result: dict[tuple[int, int], list[Direction]] = dict()

    for (src_x, src_y), directions in blizzards.items():
        for direction in directions:
            x, y = src_x, src_y
            diff = direction.get_move_difference()
            x += diff[0]
            y += diff[1]

            if x < min_x:
                x = max_x
            elif x > max_x:
                x = min_x

            if y < min_y:
                y = max_y
            elif y > max_y:
                y = min_y

            new_point = (x, y)

            if new_point in result:
                result[new_point].append(direction)
            else:
                result.update({new_point: [direction]})

    return result


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            #.######
            #>>.<^<#
            #.<..<<#
            #>v.><>#
            #<^v^^>#
            ######.#
        :output 1:
            None

        """

        blizzards: dict[tuple[int, int], list[Direction]] = dict()

        for i_n, i in enumerate(data.strip().split('\n')):
            for j_n, j in enumerate(i):
                if j in ('#', '.'):  # yep, erase borders
                    continue
                direction = Direction(j)
                blizzards.update({(j_n - 1, i_n - 1): [direction]})

        # coordination limit for blizzards
        # WARNING: if map not filled with blizzards, this logic will be failed.
        min_x, min_y = 0, 0
        max_x, max_y = max(i[0] for i in blizzards), max(i[1] for i in blizzards)

        end_point = (max_x, max_y+1)

        # simulate blizzards before exit achievement.

        me_points: set = {(0, -1)}
        possible_me_moves = ((0, 1), (1, 0), (-1, 0), (0, -1))
        counter = 0

        while True:
            counter += 1

            blizzards = resolve_blizzards_minute(blizzards, min_x, min_y, max_x, max_y)

            for me in me_points.copy():
                new_me_points = set()

                for j in possible_me_moves:
                    target = me[0] + j[0], me[1] + j[1]

                    x, y = target
                    if target != end_point:
                        if (min_x > x) or (x > max_x):
                            continue
                        if (min_y > y) or (y > max_y):
                            continue

                    if target not in blizzards:
                        new_me_points.add(target)

                me_points |= new_me_points
                me_points = me_points.difference(blizzards.keys())

                if end_point in new_me_points:
                    return str(counter)

            # draw(blizzards)
            # print()
            # draw(blizzards | {k: [Direction.ME] for k in me_points})
            # print('===='*20)
