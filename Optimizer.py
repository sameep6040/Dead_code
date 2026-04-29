def remove_dead_branches(program):
    new_program = []
    skip = False
    skip_type = None

    for instr in program:

        if instr.inst_type in ["IF", "WHILE"]:
            result = evaluate_condition(instr.lhs)

            # only remove always-false blocks
            if result is False:
                skip = True
                skip_type = "ENDIF" if instr.inst_type == "IF" else "ENDWHILE"
                continue

        if skip:
            if instr.inst_type == skip_type:
                skip = False
                skip_type = None
            continue

        new_program.append(instr)

    return new_program


def remove_dead_after_break_continue(program):
    new_program = []
    skip = False
    depth = 0

    for instr in program:

        if skip:
            if instr.inst_type == "IF":
                depth += 1

            elif instr.inst_type == "ENDIF":
                if depth == 0:
                    new_program.append(instr)
                    skip = False
                    continue
                else:
                    depth -= 1

            elif instr.inst_type == "ENDWHILE":
                new_program.append(instr)
                skip = False
                continue

            continue

        new_program.append(instr)

        if instr.inst_type in ["BREAK", "CONTINUE"]:
            skip = True
            depth = 0

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


def remove_overwritten_assignments(program):
    new_program = []
    last_assignment = {}

    for instr in program:

        if instr.inst_type == "ASSIGN":
            var = instr.lhs

            # only remove old assignment if current RHS does NOT use same variable
            if var in last_assignment and var not in instr.rhs:
                old_index = last_assignment[var]

                if old_index < len(new_program):
                    new_program[old_index] = None

            last_assignment[var] = len(new_program)
            new_program.append(instr)

        elif instr.inst_type in ["CALL", "RETURN", "IF", "WHILE"]:
            used_vars = []

            if instr.lhs:
                used_vars.extend(instr.lhs.split())

            used_vars.extend(instr.rhs)

            for used in used_vars:
                if used in last_assignment:
                    del last_assignment[used]

            new_program.append(instr)

        else:
            new_program.append(instr)

    return [instr for instr in new_program if instr is not None]


def remove_dead_assignments(program):

    live = set()
    new_program = []

    for instr in reversed(program):

        if instr.inst_type == "RETURN":
            if instr.lhs and instr.lhs.isidentifier():
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
        
        elif instr.inst_type == "CALL":
           
            for arg in instr.rhs:
                clean_arg = arg.strip().strip('"').strip("'")
                if clean_arg.isidentifier():
                    live.add(clean_arg)
            
            if instr.lhs.isidentifier():
                live.add(instr.lhs)

            new_program.append(instr)
        

        else:
            new_program.append(instr)

    new_program.reverse()
    return new_program





def remove_unused_functions(program):

    called = set()
    called.add("main")

    for instr in program:
        if instr.inst_type == "CALL":
            called.add(instr.lhs)

    new_program = []
    keep = False

    for instr in program:

        if instr.inst_type == "FUNC":
            if instr.lhs in called:
                keep = True
            else:
                keep = False

        if keep:
            new_program.append(instr)

        if instr.inst_type == "END":
            keep = False

    return new_program


def evaluate_condition(condition):
    condition = condition.strip()

    if condition == "1":
        return True

    if condition == "0":
        return False

    # Convert C-style operators to Python
    condition = condition.replace("&&", " and ")
    condition = condition.replace("||", " or ")

    # careful with !
    if "!=" not in condition:
        condition = condition.replace("!", " not ")

    try:
        result = eval(condition)

        if isinstance(result, bool):
            return result

        if isinstance(result, int):
            return result != 0

    except:
        pass

    return None

