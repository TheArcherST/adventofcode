import rich

from fastaoc import AdventOfCodePuzzle

from enum import Enum


BLIZZARD_COLORS = ['cyan1']  # index++ : deep++
ME_COLOR = 'deep_pink2'


RENDER = False


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


def draw(console, blizzards: dict[tuple[int, int], list[Direction]]):
    area = get_area(blizzards.keys())
    result = ''
    for y in range(0, area[1][1]):
        for x in range(0, area[0][1]):
            if (x, y) in blizzards:
                directions = blizzards[(x, y)]
                color_index = min(len(directions), len(BLIZZARD_COLORS)) - 1
                if len(directions) == 1:
                    if directions[0] == Direction.ME:
                        color = ME_COLOR
                    else:
                        color = BLIZZARD_COLORS[color_index]
                    result += f'[{color}]{directions[0].value}[/{color}]'
                else:
                    result += f'[{BLIZZARD_COLORS[color_index]}]{len(directions)}[/{BLIZZARD_COLORS[color_index]}]'
            else:
                result += '.'
        result += '\n'

    console.update_screen(result)


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


def process_trip(console,
                 blizzards: dict[tuple[int, int], list[Direction]],
                 area: tuple[int, int, int, int],
                 start_point: tuple[int, int], end_point: tuple[int, int]):

    me_points = {start_point}
    possible_me_moves = ((0, 1), (1, 0), (-1, 0), (0, -1))
    counter = 0

    min_x, min_y, max_x, max_y = area

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
            me_points -= blizzards.keys()

            if end_point in new_me_points:
                return blizzards, counter

        if RENDER:
            draw(console, blizzards | ({k: [Direction.ME] for k in me_points - {start_point}}))


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
            18

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
        area = min_x, min_y, max_x, max_y

        console = rich.console.Console(color_system='truecolor', highlight=False)

        if RENDER:
            console.set_alt_screen(True)

        result = process_trip(console, blizzards, area, (0, -1), (max_x, max_y+1))
        return str(result[1])

    def task_0(self, data):
        """Some task solution

        :input 1:
            #.######
            #>>.<^<#
            #.<..<<#
            #>v.><>#
            #<^v^^>#
            ######.#
        :output 1:
            54

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
        area = min_x, min_y, max_x, max_y

        console = rich.console.Console(color_system='truecolor', highlight=False)

        if RENDER:
            console.set_alt_screen(True)

        blizzards, a = process_trip(console, blizzards, area, (0, -1), (max_x, max_y+1))
        blizzards, b = process_trip(console, blizzards, area, (max_x, max_y+1), (0, -1))
        blizzards, c = process_trip(console, blizzards, area, (0, -1), (max_x, max_y+1))
        return str(a + b + c)
