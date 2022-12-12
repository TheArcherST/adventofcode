from fastaoc import AdventOfCodePuzzle
from utils.coordinates import Coordinates
import collections


SINGLE_PATHS = ((-1, 0), (0, 1), (0, -1), (1, 0))


def make_graph(grid: list[list[int]]):
    graph: dict[tuple[int, int], set[Coordinates]] = dict()

    for y, yv in enumerate(grid):
        for x, xv in enumerate(yv):
            point = Coordinates(x, y)
            graph.update({tuple(point): set()})

            for i in SINGLE_PATHS:
                new_point = point + i
                if new_point.x < 0 or new_point.y < 0:
                    continue
                elif new_point.y + 1 > len(grid):
                    continue
                elif new_point.x + 1 > len(grid[0]):
                    continue
                else:

                    nxv = grid[new_point.y][new_point.x]
                    if xv <= nxv-2:
                        continue

                    graph[tuple(point)].add(new_point)

    return graph


def bfs(graph, roots: set, end):
    visited, queue = set(), collections.deque([(i, 0) for i in roots])
    visited.update(roots)

    while queue:
        vertex, depth = queue.popleft()

        if tuple(vertex) == tuple(end):
            return depth

        for neighbour in graph[tuple(vertex)]:
            if neighbour not in visited:
                queue.append((neighbour, depth + 1))
                visited.add(neighbour)


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            Sabqponm
            abcryxxl
            accszExk
            acctuvwj
            abdefghi
        :output 1:
            29

        """

        mp: list[list[int]] = []
        start = None
        end = None

        for y, yv in enumerate(data.split("\n")):
            if not yv:
                continue
            mp.append([])
            for x, xv in enumerate(yv):
                if xv == "S":
                    start = Coordinates(x, y)
                    xv = "a"
                elif xv == "E":
                    end = Coordinates(x, y)
                    xv = "z"

                mp[y].append(ord(xv) - ord("a"))

        graph = make_graph(mp)
        result = bfs(graph, {start}, end)
        return str(result)

    def task_2(self, data):
        """Some task solution

                :input 1:
                    Sabqponm
                    abcryxxl
                    accszExk
                    acctuvwj
                    abdefghi
                :output 1:
                    31

                """

        mp: list[list[int]] = []
        start = None
        end = None
        roots = set()
        for y, yv in enumerate(data.split("\n")):
            if not yv:
                continue
            mp.append([])
            for x, xv in enumerate(yv):
                if xv == "S":
                    start = Coordinates(x, y)
                    xv = "a"
                elif xv == "E":
                    end = Coordinates(x, y)
                    xv = "z"

                if xv == 'a':
                    roots.add((x, y))

                mp[y].append(ord(xv) - ord("a"))

        graph = make_graph(mp)
        result = bfs(graph, roots, end)
        return str(result)
