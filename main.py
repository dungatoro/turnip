import re

class Machine:
    r"""
        010
        001
        111
        A(2,1)
        A{01>0B .<1B 1\}
        B{01>0A .<0>0B 1<\}
    """

    def __init__(self, *, src=""):
        """
        table = { state: { 0: (code, new_state), ... }, ... }
        """
        self.table = {}

        """ 
        Find the grid e.g.
            010
            001
            111
        """
        lines = src.strip().split('\n')
        finding_grid = True
        grid = []
        idx = 0
        while finding_grid:
            line = lines[idx]
            if re.match(r"[.01]+", line):
                if len(line) != len(lines[0]):
                    print(line)
                    raise Exception("Grid has inconsistent row lenghts!")
                else:
                    grid.append(list(line))
            else:
                finding_grid = False
            idx += 1

        """ Find the start state and coordinates e.g. A(2,1) """
        start_syntax = r"([a-zA-z]\w*.?)\(\s*(\d+.?)\s*,\s*(\d+.?)\s*\)"
        start_state, x, y = re.findall(start_syntax, src)[0]
        try:
            self.state = start_state
            self.x = int(x)
            self.y = int(y)
        except:
            raise Exception("Start state and coordinates not found!")

        """ Find all the state transition table definitions """
        state_syntax = r"[a-zA-Z_]\w*\s*\{(?:\s*[.01]\s*[.01^v<>\s]*[a-zA-Z_]\w*\s*\|){0,2}\s*[.01]\s*[.01^v<>\s]*[a-zA-Z_]\w*\s*}"
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
                    elif transition[idx] not in ".01^v<>\r\n\t\f\v ":
                        finding_new_state = False
                    else:
                        idx += 1

                code = transition[1:idx]
                new_state = transition[idx:]
                transition_table[ip] = (code, new_state)

            self.table[state] = transition_table

src = r"""
.00010110
.00000011
sub1(8,0)
sub1{._|01<sub1|10<pass}
pass{.^<write0|0<pass|1<pass}
write0{.<vsub1|00<write0|10<write1}
write1{.<vsub1|01<write0|11<write1}
"""

machine = Machine(src=src)
print(src)
print(machine.table)


