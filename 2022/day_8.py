from fastaof import AdventOfCodePuzzle


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            30373
            25512
            65332
            33549
            35390
        :output 1:
            21

        """
        input=data.strip()
        grid = [list(map(int, l)) for l in input.split('\n')]
        height, width = len(grid), len(grid[0])
        visible = [[False for _ in range(width)] for _ in range(height)]
        best_scenic = 0
        
        for x0 in range(width):
            for y0 in range(height):
                ss, h = 1, grid[y0][x0]
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    x1, y1, s1 = x0+dx, y0+dy, 1
                    while 0 <= x1 < width and 0 <= y1 < height and grid[y1][x1] < h:
                        x1, y1, s1 = x1 + dx, y1 + dy, s1 + 1
                    if not (0 <= x1 < width and 0 <= y1 < height):
                        visible[y0][x0] = True
                        s1 -= 1
                    ss *= s1
                best_scenic = max(best_scenic, ss)
        
        return str(sum(map(sum, visible)))

    def task_2(self, data):
        """Some task solution
    
        :input 1:
            30373
            25512
            65332
            33549
            35390
        :output 1:
            8
    
        """
        input=data.strip()
        grid = [list(map(int, l)) for l in input.split('\n')]
        height, width = len(grid), len(grid[0])
        visible = [[False for _ in range(width)] for _ in range(height)]
        best_scenic = 0
        
        for x0 in range(width):
            for y0 in range(height):
                ss, h = 1, grid[y0][x0]
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    x1, y1, s1 = x0+dx, y0+dy, 1
                    while 0 <= x1 < width and 0 <= y1 < height and grid[y1][x1] < h:
                        x1, y1, s1 = x1 + dx, y1 + dy, s1 + 1
                    if not (0 <= x1 < width and 0 <= y1 < height):
                        visible[y0][x0] = True
                        s1 -= 1
                    ss *= s1
                best_scenic = max(best_scenic, ss)
        
        return str(best_scenic)
