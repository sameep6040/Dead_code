from instractions import Instruction


def parse_python_program(filename):
    program = []
    indent_stack = []

    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip() == "":
            continue

        if line.strip().startswith("#"):
            continue

        current_indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        while indent_stack and indent_stack[-1][1] != "FUNC":
            top_indent, block_type = indent_stack[-1]

            if current_indent <= top_indent:
                indent_stack.pop()

                if block_type == "IF":
                    program.append(Instruction("ENDIF"))

                elif block_type == "WHILE":
                    program.append(Instruction("ENDWHILE"))

            else:
                break

        if stripped.startswith("def "):

            while indent_stack:
                block_type = indent_stack.pop()[1]

                if block_type == "IF":
                    program.append(Instruction("ENDIF"))

                elif block_type == "WHILE":
                    program.append(Instruction("ENDWHILE"))

                elif block_type == "FUNC":
                    program.append(Instruction("END"))

            func_name = stripped.split()[1].split("(")[0]

            program.append(Instruction("FUNC", lhs=func_name))
            indent_stack.append((current_indent, "FUNC"))

        elif stripped.startswith("if "):
            condition = stripped[3:].replace(":", "").strip()

            program.append(Instruction("IF", lhs=condition))
            indent_stack.append((current_indent, "IF"))

        elif stripped.startswith("while "):
            condition = stripped[6:].replace(":", "").strip()

            program.append(Instruction("WHILE", lhs=condition))
            indent_stack.append((current_indent, "WHILE"))

        elif stripped == "break":
            program.append(Instruction("BREAK"))

        elif stripped == "continue":
            program.append(Instruction("CONTINUE"))

        elif stripped.startswith("return "):

            while indent_stack and indent_stack[-1][1] in ["IF", "WHILE"]:
                block_type = indent_stack.pop()[1]

                if block_type == "IF":
                    program.append(Instruction("ENDIF"))

                elif block_type == "WHILE":
                    program.append(Instruction("ENDWHILE"))

            value = stripped.replace("return", "").strip()
            program.append(Instruction("RETURN", lhs=value))

        elif stripped.startswith("print("):
            start = stripped.index("(") + 1
            end = stripped.rindex(")")
            args = stripped[start:end]

            program.append(Instruction("CALL", lhs="print", rhs=[args]))

        elif "=" in stripped and "==" not in stripped:
            parts = stripped.split("=")

            left = parts[0].strip()
            right = parts[1].strip().split()

            program.append(Instruction("ASSIGN", lhs=left, rhs=right))

    while indent_stack:
        block_type = indent_stack.pop()[1]

        if block_type == "IF":
            program.append(Instruction("ENDIF"))

        elif block_type == "WHILE":
            program.append(Instruction("ENDWHILE"))

        elif block_type == "FUNC":
            program.append(Instruction("END"))

    return program