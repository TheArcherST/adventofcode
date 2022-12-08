from fastaof import AdventOfCodePuzzle


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
          mjqjpqmgbljsphdztnvjfqwrcgsmlb
        :output 1:
            7

        """

        for i in range(len(data)-4):
            if len(set(data[i:i+4]))==4:
                return str(i+4)

   
    def task_2(self, data):
        
        """Some task solution

        :input 1:
          mjqjpqmgbljsphdztnvjfqwrcgsmlb
        :output 1:
            19

        """

        for i in range(len(data)-14):
            if len(set(data[i:i+14]))==14:
                return str(i+14)
