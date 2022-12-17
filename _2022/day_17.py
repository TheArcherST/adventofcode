from fastaoc import AdventOfCodePuzzle
from itertools import cycle

from utils.algebra import CoordinatesAlias

FIGURES = [{(0, 0), (1, 0), (2, 0), (3, 0)},
           {(1, 0), (0, 1), (2, 1), (1, 2), (1, 1)},
           {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
           {(0, 0), (0, 1), (0, 2), (0, 3)},
           {(0, 0), (1, 0), (0, 1), (1, 1)}]


def fig_offset(fig: set[CoordinatesAlias], offset) -> set[CoordinatesAlias]:
    result = set()
    for i in fig:
        result.add((i[0] + offset[0], i[1] + offset[1]))
    return result


def draw(points, max_y):
    for y in reversed(range(max_y+1)):
        for x in range(7):
            if (x, y) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()

    print()


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
        :output 1:
            3068

        """

        filled_points: set = set()
        fig_gen = cycle(FIGURES)
        dir_gen = cycle(data.strip())

        current_spawn = [2, 3]
        fig = fig_offset(next(fig_gen), current_spawn)
        down_offset = (0, -1)
        stopped_counter = 0
        while True:
            if stopped_counter == 2022:
                break

            # screen = fig | filled_points
            # max_y = max(i[1] for i in screen)
            # draw(screen, max_y)

            if next(dir_gen) == "<":
                of = (-1, 0)
            else:
                of = (1, 0)

            upd_fig = fig_offset(fig, of)

            min_x, max_x, min_y = min(i[0] for i in upd_fig), max(i[0] for i in upd_fig), min(i[1] for i in upd_fig)

            if (filled_points & upd_fig) or (min_y < 0 or max_x > 6 or min_x < 0):
                pass
            else:
                fig = upd_fig

            upd_fig = fig_offset(fig, down_offset)
            max_y, min_y = max(i[1] for i in upd_fig), min(i[1] for i in upd_fig)

            if (filled_points & upd_fig) or (min_y < 0):
                filled_points.update(fig)
                current_spawn[1] = max(i[1] for i in filled_points) + 4

                fig = fig_offset(next(fig_gen), tuple(current_spawn))

                stopped_counter += 1
            else:
                fig = upd_fig

        max_y = max(i[1] for i in filled_points)
        print(max_y+1)

    def task_2(self, data):

        """Some task solution

        :input 1:
            >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
        :output 1:
            1514285714288

        """

        stopped_target = 1000000000000

        filled_points: set = set()
        fig_gen = cycle(enumerate(FIGURES))
        dir_gen = cycle(enumerate(data.strip()))

        current_spawn = [2, 3]
        fig_n, fig = next(fig_gen)
        fig = fig_offset(fig, current_spawn)
        down_offset = (0, -1)
        stopped_counter = 0
        seen = set()
        seen_dct = dict()
        result_addition = 0
        while True:
            if stopped_counter == stopped_target:
                break
            elif stopped_counter > stopped_target:
                breakpoint()
            dir_n, direction = next(dir_gen)
            if direction == "<":
                of = (-1, 0)
            else:
                of = (1, 0)

            upd_fig = fig_offset(fig, of)

            min_x, max_x, min_y = min(i[0] for i in upd_fig), max(i[0] for i in upd_fig), min(i[1] for i in upd_fig)

            if (filled_points & upd_fig) or (min_y < 0 or max_x > 6 or min_x < 0):
                pass
            else:
                fig = upd_fig

            upd_fig = fig_offset(fig, down_offset)
            min_y, max_y = min(i[1] for i in upd_fig), max(i[1] for i in upd_fig)

            if (filled_points & upd_fig) or (min_y < 0):
                filled_points.update(fig)
                current_spawn[1] = max(i[1] for i in filled_points) + 4

                fig_n, fig = next(fig_gen)
                fig = fig_offset(fig, tuple(current_spawn))
                stopped_counter += 1

                tower_state_unique_key = (fig_n, dir_n,
                                          tuple(map(lambda x: x[0], filter(lambda x: x[1] in range(max_y-4, max_y), filled_points)),))
                if tower_state_unique_key in seen_dct:
                    old_y, old_count = seen_dct[tower_state_unique_key]
                    actual_y = max(i[1] for i in filled_points)
                    y_period = actual_y - old_y
                    count_period = stopped_counter - old_count
                    periods_to_add = max((stopped_target - stopped_counter) // count_period, 0)
                    counts_to_add = periods_to_add * count_period
                    result_addition += periods_to_add * y_period
                    stopped_counter += counts_to_add
                else:
                    seen_dct.update({tower_state_unique_key: (max(i[1] for i in filled_points), stopped_counter)})
            else:
                fig = upd_fig

        max_y = max(i[1] for i in filled_points)
        return str(result_addition + max_y + 1)
