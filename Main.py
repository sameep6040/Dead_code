from Parser import parse_program
from Optimizer import remove_dead_assignments, remove_unreachable, remove_unused_functions, remove_dead_branches


def generate_code(program, filename):

    indent = 0
    declared = set()

    with open(filename, "w") as f:

        for instr in program:

            if instr.inst_type == "FUNC":
                f.write(f"\nint {instr.lhs}() {{\n")
                indent += 1
                declared.clear()

            elif instr.inst_type == "END":
                indent -= 1
                f.write("}\n")

            elif instr.inst_type == "ASSIGN":

                if instr.lhs not in declared:
                    f.write("    " * indent + f"int {instr.lhs} = {' '.join(instr.rhs)};\n")
                    declared.add(instr.lhs)
                else:
                    f.write("    " * indent + f"{instr.lhs} = {' '.join(instr.rhs)};\n")

            elif instr.inst_type == "RETURN":
                f.write("    " * indent + f"return {instr.lhs};\n")

            elif instr.inst_type == "CALL":
                f.write("    " * indent + f"{instr.lhs}();\n")

            elif instr.inst_type == "IF":
                f.write("    " * indent + f"if({instr.lhs}) {{\n")
                indent += 1

            elif instr.inst_type == "ENDIF":
                indent -= 1
                f.write("    " * indent + "}\n")

            elif instr.inst_type == "WHILE":
                f.write("    " * indent + f"while({instr.lhs}) {{\n")
                indent += 1

            elif instr.inst_type == "ENDWHILE":
                indent -= 1
                f.write("    " * indent + "}\n")


program = parse_program("Input.c")

print(" Original Code ")
for instr in program:
    print(instr)

original_len = len(program)

program = remove_dead_assignments(program)
program = remove_unreachable(program)
program = remove_unused_functions(program)
program = remove_dead_branches(program)

optimized_len = len(program)

print("\nWriting filtered code to output.c.\n")

generate_code(program, "output.c")

print("Check output.c file for ouput!")
print("Lines removed:", original_len - optimized_len)