def remove_dead_assignments(program):

    live = set()
    new_program = []

    for instr in reversed(program):

        if instr.inst_type == "RETURN":
            live.add(instr.lhs)
            new_program.append(instr)

        elif instr.inst_type == "IF" or instr.inst_type == "WHILE":
            parts = instr.lhs.split()
            for p in parts:
                if p.isidentifier():
                    live.add(p)
            new_program.append(instr)

        elif instr.inst_type == "ASSIGN":

            used = False

            if instr.lhs in live:
                used = True

            for var in instr.rhs:
                if var in live:
                    used = True
            
            if instr.lhs in instr.rhs:
                used = True

            if used:
                if instr.lhs in live:
                    live.remove(instr.lhs)

                for var in instr.rhs:
                    if var.isidentifier():
                        live.add(var)

                new_program.append(instr)

        else:
            new_program.append(instr)

    new_program.reverse()
    return new_program


def remove_unreachable(program):

    new_program = []
    stop = False

    for instr in program:

        if instr.inst_type == "FUNC":
            stop = False

        if instr.inst_type == "END":
            new_program.append(instr)
            stop = False
            continue

        if stop:
            continue

        new_program.append(instr)

        if instr.inst_type == "RETURN":
            stop = True

    return new_program


def remove_unused_functions(program):

    called = set()

    for instr in program:
        if instr.inst_type == "CALL":
            called.add(instr.lhs)

    new_program = []
    keep = False

    for instr in program:

        if instr.inst_type == "FUNC":
            if instr.lhs == "main" or instr.lhs in called:
                keep = True
            else:
                keep = False

        if keep:
            new_program.append(instr)

    return new_program


def remove_dead_branches(program):

    new_program = []
    skip = False

    for instr in program:

        if instr.inst_type == "IF":
            if instr.lhs.strip() == "0":
                skip = True
                continue

        if instr.inst_type == "ENDIF":
            skip = False
            continue

        if skip:
            continue

        new_program.append(instr)

    return new_program