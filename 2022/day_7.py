from fastaof import AdventOfCodePuzzle


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            10 a
        :output 1:
            None

        """

        current = ""
        d=dict()
        for i in data.split("\n"):
          i=i.removeprefix("$ ")
          if i.startswith("cd"):
            arg = i.split()[1]
            if arg == "..":
              current="/".join(current.split("/")[:-1])
            elif arg == "/":
              current=""
            else:
              current+="/"+arg
          elif i.startswith(("ls","dir")):
              pass
          else:
            if not i: continue
            k = []
            for j in current.split("/"):
              k.append(j)
              path = "/".join(k)
              d.update({path: d.get(path, 0)+int(i.split()[0])})
            
        r =0
        for i in d.values():
          if i <= 100000:
            r+=i
        
        return r
    def task_2(self, data):

        """Some task solution

        :input 1:
            10 a
        :output 1:
            None

        """

        current = ""
        d=dict()
        s=0
        for i in data.split("\n"):
          i=i.removeprefix("$ ")
          if i.startswith("cd"):
            arg = i.split()[1]
            if arg == "..":
              current="/".join(current.split("/")[:-1])
            elif arg == "/":
              current=""
            else:
              current+="/"+arg
          elif i.startswith(("ls","dir")):
              pass
          else:
            if not i: continue
            k = []
            s+=int(i.split()[0])
            for j in current.split("/"):
              k.append(j)
              path = "/".join(k)
              d.update({path: d.get(path, 0)+int(i.split()[0])})

        unused = 70000000-s
        need_to_free = 30000000 - unused
        print("s",need_to_free)
        
      
        
        for i in sorted(d.values()):
          if i >= need_to_free:
            return i
        
        
