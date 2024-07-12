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
    def __init__(*, src=""):
        """
        table = { state: { 0: (code, new_state), ... }, ... }
        """

        """ 
        Find the grid e.g.
            010
            001
            111
        """

        lines = src.split('\n')
        finding_grid = True
        grid = []
        while finding_grid:
            if re.match(r"[.01]*", row):
                if len(row) != len(lines[0]):
                    raise Exception("Grid has inconsistent row lenghts!")
                else:
                    grid.append(list(row))
            else:
                finding_grid = False

        """ Find the start state and coordinates e.g. A(2,1) """
        start_syntax = r"([a-zA-z]\w*.?)\(\s*(\d+.?)\s*,\s*(\d+.?)\s*\)"
        start_state, x, y = re.findall(start_def, src)
        try:
            self.state = start_state
            self.x = int(x)
            self.y = int(y)
        except:
            raise Exception("Start state and coordinates not found!")

        """ Find all the state transition table definitions """
        state_syntax = r"[a-zA-Z_]\w*\s*\{(?:\s*[.01]\s*[.01^v<>\s]*[a-zA-Z_]\w*\s*\|){0,2}\s*[.01]\s*[.01^v<>\s]*[a-zA-Z_]\w*\s*}"

        state_defs = re.findall(state_def, src)
        for state_

        def tick(self):
            pass

src = r"""
        010
        001
        111
        A(2,1)
        Abc{01>0B| .<1B| 1_}
        B{01>0A|.<0>0B|1<_}
    """
