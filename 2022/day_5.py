from fastaof import AdventOfCodePuzzle
from pprint import pp

class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
          ell

          ell
        :output 1:
          CMZ

        """
        first, second = data.split("\n\n")
        
        lsts = [[] for _ in range(20)]

        lines = first.split('\n')
        for i in lines:
          for nj, j in enumerate(i[1::4]):
            if j.isnumeric():continue
            if j == ' ':
              continue
            lsts[nj].append(j)
        lsts=list(map(lambda x: list(reversed(x)),lsts))
        
        for i in second.split("\n"):
            if len(i)<5:continue
            fromc, fromn, ton = map(int, i.split()[1::2])
            sel=lsts[fromn-1]
            lsts[ton-1] += reversed(sel[len(sel)-fromc:])
            for _ in range(fromc):
              lsts[fromn-1].pop()

        res = ""
      
        for i in lsts:
          try:
            res+=i[-1]
          except: pass

        return res

    def task_2(self, data):

        """Some task solution

        :input 1:
          ell

          ell
        :output 1:
          CMZ

        """
        first, second = data.split("\n\n")
        
        lsts = [[] for _ in range(20)]

        lines = first.split('\n')
        for i in lines:
          for nj, j in enumerate(i[1::4]):
            if j.isnumeric():continue
            if j == ' ':
              continue
            lsts[nj].append(j)
        lsts=list(map(lambda x: list(reversed(x)),lsts))
        
        for i in second.split("\n"):
            if len(i)<5:continue
            fromc, fromn, ton = map(int, i.split()[1::2])
            sel=lsts[fromn-1]
            lsts[ton-1] += sel[len(sel)-fromc:]
            for _ in range(fromc):
              lsts[fromn-1].pop()

        res = ""
      
        for i in lsts:
          try:
            res+=i[-1]
          except: pass

        return res
