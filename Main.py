import io
import os
import time
from PythonParser import parse_python_program
from Parser import parse_program
import Optimizer
from CFG import visualize_program


def generate_code_to_string(program):
    output = io.StringIO()
    indent = 0
    declared = set()

    for instr in program:

        if instr.inst_type == "FUNC":
            output.write(f"\nint {instr.lhs}() {{\n")
            indent = 1
            declared.clear()

        elif instr.inst_type == "END":
            indent = 0
            output.write("}\n")

        elif instr.inst_type == "IF":
            prefix = "    " * indent
            output.write(f"{prefix}if({instr.lhs}) {{\n")
            indent += 1

        elif instr.inst_type == "ENDIF":
            indent = max(0, indent - 1)
            prefix = "    " * indent
            output.write(f"{prefix}}}\n")

        elif instr.inst_type == "WHILE":
            prefix = "    " * indent
            output.write(f"{prefix}while({instr.lhs}) {{\n")
            indent += 1

        elif instr.inst_type == "ENDWHILE":
            indent = max(0, indent - 1)
            prefix = "    " * indent
            output.write(f"{prefix}}}\n")

        elif instr.inst_type == "ASSIGN":
            prefix = "    " * indent
            if instr.lhs not in declared:
                output.write(f"{prefix}int {instr.lhs} = {' '.join(instr.rhs)};\n")
                declared.add(instr.lhs)
            else:
                output.write(f"{prefix}{instr.lhs} = {' '.join(instr.rhs)};\n")

        elif instr.inst_type == "RETURN":
            prefix = "    " * indent
            output.write(f"{prefix}return {instr.lhs};\n")

        elif instr.inst_type == "CALL":
            prefix = "    " * indent
            args_str = "".join(instr.rhs)
            output.write(f"{prefix}{instr.lhs}({args_str});\n")

        elif instr.inst_type == "BREAK":
            prefix = "    " * indent
            output.write(f"{prefix}break;\n")

        elif instr.inst_type == "CONTINUE":
            prefix = "    " * indent
            output.write(f"{prefix}continue;\n")

    return output.getvalue()


def generate_python_code_to_string(program):
    output = io.StringIO()
    indent = 0

    for instr in program:

        prefix = "    " * indent

        if instr.inst_type == "FUNC":
            output.write(f"\ndef {instr.lhs}():\n")
            indent = 1

        elif instr.inst_type == "END":
            indent = 0

        elif instr.inst_type == "IF":
            output.write(f"{prefix}if {instr.lhs}:\n")
            indent += 1

        elif instr.inst_type == "ENDIF":
            indent = max(0, indent - 1)

        elif instr.inst_type == "WHILE":
            output.write(f"{prefix}while {instr.lhs}:\n")
            indent += 1

        elif instr.inst_type == "ENDWHILE":
            indent = max(0, indent - 1)

        elif instr.inst_type == "ASSIGN":
            output.write(f"{prefix}{instr.lhs} = {' '.join(instr.rhs)}\n")

        elif instr.inst_type == "RETURN":
            output.write(f"{prefix}return {instr.lhs}\n")

        elif instr.inst_type == "CALL":
            args = "".join(instr.rhs)
            output.write(f"{prefix}{instr.lhs}({args})\n")

        elif instr.inst_type == "BREAK":
            output.write(f"{prefix}break\n")

        elif instr.inst_type == "CONTINUE":
            output.write(f"{prefix}continue\n")

    return output.getvalue()


def run_secure_optimization(input_code, language):

    # -------- PARSE --------
    temp_filename = "temp_input_code.txt"
    
    with open(temp_filename, "w") as f:
        f.write(input_code)

    if language == "C":
        program = parse_program(temp_filename)

    elif language == "Python":
        program = parse_python_program(temp_filename)

    else:
        program = []

    
    print("\n===== PARSED IR =====")
    for instr in program:
        print(instr)
    original_program = program.copy()
    original_len = len(program)

    # -------- CFG BEFORE --------
    before_file = "cfg_before"

    visualize_program(original_program, f"static/{before_file}", "Before Optimization")

    # -------- OPTIMIZATION --------
    while True:
        start = len(program)

        program = Optimizer.remove_dead_branches(program)
        program = Optimizer.remove_dead_after_break_continue(program)
        program = Optimizer.remove_unreachable(program)
        program = Optimizer.remove_overwritten_assignments(program)
        program = Optimizer.remove_dead_assignments(program)        
        
        if language == "C":
            program = Optimizer.remove_unused_functions(program)       

        if len(program) == start:
            break

    # -------- CFG AFTER --------
    after_file = "cfg_after"

    visualize_program(program, f"static/{after_file}", "After Optimization")

    # -------- OUTPUT --------
    if language == "C":
        optimized_code = generate_code_to_string(program)

    elif language == "Python":
        optimized_code = generate_python_code_to_string(program)

    else:
        optimized_code = ""


    logs = [
        "Optimization completed",
        "Dead code removed",
        "CFG generated successfully"
    ]

    return (
        optimized_code,
        logs,
        original_len - len(program),
        program,
        before_file + ".png",
        after_file + ".png"
    )