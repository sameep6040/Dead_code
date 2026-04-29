from instractions import Instruction


def parse_program(filename):
    program = []
    stack = []

    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if line == "":
            continue

        # -------- FUNCTION --------
        if line.startswith("int") and "(" in line and ")" in line and "{" in line:
            name = line.split()[1]
            name = name[:name.index("(")]

            program.append(Instruction("FUNC", lhs=name))
            stack.append("FUNC")

        # -------- IF --------
        elif line.startswith("if"):
            start = line.index("(")
            end = line.rindex(")")
            cond = line[start + 1:end]

            program.append(Instruction("IF", lhs=cond))
            stack.append("IF")

        # -------- WHILE --------
        elif line.startswith("while"):
            start = line.index("(")
            end = line.rindex(")")
            cond = line[start + 1:end]

            program.append(Instruction("WHILE", lhs=cond))
            stack.append("WHILE")

        # -------- BREAK --------
        elif line == "break;":
            program.append(Instruction("BREAK"))

        # -------- CONTINUE --------
        elif line == "continue;":
            program.append(Instruction("CONTINUE"))

        # -------- RETURN --------
        elif line.startswith("return"):
            val = line.replace("return", "").replace(";", "").strip()
            program.append(Instruction("RETURN", lhs=val))

        # -------- FUNCTION CALL --------
        elif (
            "(" in line and ")" in line and ";" in line
            and not line.startswith("if")
            and not line.startswith("while")
            and not line.startswith("return")
        ):
            name = line.split("(")[0].strip()

            start_arg = line.index("(") + 1
            end_arg = line.rindex(")")
            args = line[start_arg:end_arg]

            program.append(Instruction("CALL", lhs=name, rhs=[args]))

        # -------- DECLARATION ASSIGNMENT --------
        elif line.startswith("int") and "=" in line:
            temp = line.replace("int", "").replace(";", "").strip()

            parts = temp.split("=")
            left = parts[0].strip()
            right = parts[1].strip().split()

            program.append(Instruction("ASSIGN", lhs=left, rhs=right))

        # -------- NORMAL ASSIGNMENT --------
        elif "=" in line:
            temp = line.replace(";", "")

            parts = temp.split("=")
            left = parts[0].strip()
            right = parts[1].strip().split()

            program.append(Instruction("ASSIGN", lhs=left, rhs=right))

        # -------- CLOSING BRACES --------
        elif line == "}":
            if stack:
                block = stack.pop()

                if block == "FUNC":
                    program.append(Instruction("END"))

                elif block == "IF":
                    program.append(Instruction("ENDIF"))

                elif block == "WHILE":
                    program.append(Instruction("ENDWHILE"))

    return program