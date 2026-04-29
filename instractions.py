class Instruction:

    def __init__(self, inst_type, lhs=None, rhs=None):
        self.inst_type = inst_type
        self.lhs = lhs
        self.rhs = rhs if rhs else []

    def __str__(self):

        if self.inst_type == "FUNC":
            return f"func {self.lhs}"

        if self.inst_type == "END":
            return "endfunc"

        if self.inst_type == "ASSIGN":
            return f"{self.lhs} = {' '.join(self.rhs)}"

        if self.inst_type == "RETURN":
            return f"return {self.lhs}"

        if self.inst_type == "CALL":
            return f"call {self.lhs}"

        if self.inst_type == "IF":
            return f"if {self.lhs}"

        if self.inst_type == "ENDIF":
            return "endif"

        if self.inst_type == "WHILE":
            return f"while {self.lhs}"

        if self.inst_type == "ENDWHILE":
            return "endwhile"
        
        if self.inst_type == "BREAK":
            return "break"

        if self.inst_type == "CONTINUE":
            return "continue"

        return self.inst_type