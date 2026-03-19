from instractions import Instruction

def parse_program(filename):

    program = []
    stack = []

    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    for line in lines:

        line = line.strip()

        if line == "":
            continue

        if line.startswith("int") and "(" in line and ")" in line and "{" in line:
            name = line.split()[1]
            name = name[:name.index("(")]
            program.append(Instruction("FUNC", name))
            stack.append("FUNC")

        elif line.startswith("if"):
            start = line.index("(")
            end = line.index(")")
            cond = line[start+1:end]
            program.append(Instruction("IF", cond))
            stack.append("IF")

        elif line.startswith("while"):
            start = line.index("(")
            end = line.index(")")
            cond = line[start+1:end]
            program.append(Instruction("WHILE", cond))
            stack.append("WHILE")

        elif line == "}":
            if stack:
                block = stack.pop()

                if block == "FUNC":
                    program.append(Instruction("END"))

                elif block == "IF":
                    program.append(Instruction("ENDIF"))

                elif block == "WHILE":
                    program.append(Instruction("ENDWHILE"))

        elif line.startswith("return"):
            val = line.replace("return", "").replace(";", "").strip()
            program.append(Instruction("RETURN", val))

        elif "(" in line and ")" in line and ";" in line and not line.startswith("if") and not line.startswith("while"):
            name = line.split("(")[0].strip()
            program.append(Instruction("CALL", name))

        elif line.startswith("int") and "=" in line:
            temp = line.replace("int", "").replace(";", "").strip()
            parts = temp.split("=")
            left = parts[0].strip()
            right = parts[1].strip().split()
            program.append(Instruction("ASSIGN", left, right))

        elif "=" in line:
            temp = line.replace(";", "")
            parts = temp.split("=")
            left = parts[0].strip()
            right = parts[1].strip().split()
            program.append(Instruction("ASSIGN", left, right))

    return program