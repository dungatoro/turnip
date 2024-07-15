import re
import os
import sys

class Machine:
    def __init__(self, *, src=""):
        # table = { state: { input: (code, new_state), ... }, ... }
        self.table = {}
        self.steps = 0

        """ 
        Find the grid e.g.
           1010
           ..01
           011.
        """
        lines = src.strip().split('\n')
        finding_grid = True
        self.grid = []
        idx = 0
        while finding_grid:
            line = lines[idx]
            if re.match(r"[.01]+", line):
                if len(line) != len(lines[0]):
                    print(line)
                    raise Exception("Grid has inconsistent row lenghts!")
                else:
                    self.grid.append(list(line))
            else:
                finding_grid = False
            idx += 1

        # Find the start state and coordinates e.g. A(2,1)
        start_syntax = r"([a-zA-z]\w*.?)\(\s*(\d+.?)\s*,\s*(\d+.?)\s*\)"
        start_state, x, y = re.findall(start_syntax, src)[0]
        try:
            self.state = start_state
            self.x = int(x)
            self.y = int(y)
        except:
            raise Exception("Start state and coordinates not found!")

        # Find all the state transition table definitions
        state_syntax = r"[a-zA-Z_]\w*\s*\{(?:\s*[.01]\s*[.01^!<>\s]*[a-zA-Z_]\w*\s*\|){0,2}\s*[.01]\s*[.01^!<>\s]*[a-zA-Z_]\w*\s*}"
        state_defs = re.findall(state_syntax, src)

        for state_def in state_defs:
            # Before the '{' is the name of the state.
            state = state_def.split('{')[0].strip()
            # After the '{' is the state definition with a '}' on the end.
            # The possible input transitions are separated by '|'.
            transitions = state_def.split('{')[1][:-1].split('|')
            transition_table = {}
            for transition in transitions:
                transition = transition.strip()
                ip = transition[0]
                finding_new_state = True
                idx = 1
                while finding_new_state:
                    if idx >= len(transition):
                        raise Exception("Missing new state transition!")
                    elif transition[idx] not in ".01^!<>\r\n\t\f\v ":
                        finding_new_state = False
                    else:
                        idx += 1

                code = transition[1:idx]
                new_state = transition[idx:]
                transition_table[ip] = (code, new_state)

            self.table[state] = transition_table

    def __tick(self):
        ip = self.grid[self.y][self.x]
        code, new_state = self.table[self.state][ip]
        for c in code:
            if c in '.01':
                self.grid[self.y][self.x] = c
            elif c == '^':
                self.y = (self.y-1)%len(self.grid)
            elif c == '!':
                self.y = (self.y+1)%len(self.grid)
            elif c == '<':
                self.x = (self.x-1)%len(self.grid[0])
            elif c == '>':
                self.x = (self.x+1)%len(self.grid[0])
        self.state = new_state
        self.steps += 1

    def __nippy(self):
        print(fr"""
     \\/_    In state `{self.state}`
    / ~ _ \  At position ({self.x},{self.y})
    \ ' ' /
      \ / 
        """)

    def manual(self):
        while self.state != '_':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.__nippy()
            for y, row in enumerate(self.grid):
                s = " "
                for x, c in enumerate(row):
                    if x == self.x and y == self.y:
                        s += f"\033[91m{c}\033[0m"
                    else:
                        s += c
                print(s)
            self.__tick()
            input('\n')
        print('\033[91mHALT!\033[0m')

    def quiet(self):
        while self.state != '_':
            self.__tick()
        print(f"Halted after {self.steps} steps")
        show = input("Show final state? (y/N) ")
        if show.lower() in ['y', 'yes']:
            for y, row in enumerate(self.grid):
                s = " "
                for x, c in enumerate(row):
                    if x == self.x and y == self.y:
                        s += f"\033[91m{c}\033[0m"
                    else:
                        s += c
                print(s)



path = sys.argv[1]
with open(path, 'r') as f:
    src = f.read()
    machine = Machine(src=src)

flags = sys.argv[1:]
if "--manual" in flags or "-m" in flags:
    machine.manual()
elif "--quiet" in flags or "-q" in flags:
    machine.quiet()


