class BasicBlock:
    def __init__(self, id):
        self.id = id
        self.instructions = []
        self.next_blocks = []


from graphviz import Digraph

def visualize_cfg(blocks, filename="cfg", title="CFG"):

    dot = Digraph()

    dot.attr(label=title, labelloc="t", fontsize="20")

    for block in blocks:
        label = ""

        for instr in block.instructions:
            label += str(instr) + "\\l"

        dot.node(str(block.id), label)

    for block in blocks:
        for nxt in block.next_blocks:
            dot.edge(str(block.id), str(nxt.id))

    dot.render(filename, format="png", view=False)

def build_blocks(program):

    blocks = []
    current_block = BasicBlock(0)
    block_id = 1

    for instr in program:

        
        if instr.inst_type == "END":
            if current_block.instructions:
                blocks.append(current_block)
            return blocks

        current_block.instructions.append(instr)

        
        if instr.inst_type in ["IF", "WHILE", "RETURN", "ENDIF", "ENDWHILE"]:
            blocks.append(current_block)
            current_block = BasicBlock(block_id)
            block_id += 1

   
    if current_block.instructions:
        blocks.append(current_block)

    return blocks


def connect_blocks(blocks):

    for i in range(len(blocks)):

        if not blocks[i].instructions:
            continue

        last_instr = blocks[i].instructions[-1]

        if last_instr.inst_type == "RETURN":
            continue

        elif last_instr.inst_type == "IF":

            if i + 1 < len(blocks):
                blocks[i].next_blocks.append(blocks[i+1])

            if i + 2 < len(blocks):
                blocks[i].next_blocks.append(blocks[i+2])

        elif last_instr.inst_type == "WHILE":

            if i + 1 < len(blocks):
                blocks[i].next_blocks.append(blocks[i+1])

            if i + 2 < len(blocks):
                blocks[i].next_blocks.append(blocks[i + 2])

        elif last_instr.inst_type == "ENDWHILE":

            for j in range(i, -1, -1):
                if blocks[j].instructions and blocks[j].instructions[-1].inst_type == "WHILE":
                    blocks[i].next_blocks.append(blocks[j])
                    break

            if i + 1 < len(blocks):
                blocks[i].next_blocks.append(blocks[i+1])

        else:

            if i + 1 < len(blocks):
                blocks[i].next_blocks.append(blocks[i+1])

    return blocks


def print_cfg(blocks):

    for block in blocks:
        print(f"\nBlock {block.id}:")

        for instr in block.instructions:
            print("   ", instr)

        print("   ->", [b.id for b in block.next_blocks])
        

def visualize_program(program, filename="cfg", title="CFG"):

    dot = Digraph()
    dot.attr(label=title, labelloc="t", fontsize="20")

    functions = []
    current = []

    # --- split functions ---
    for instr in program:
        if instr.inst_type == "FUNC":
            current = [instr]
        elif instr.inst_type == "END":
            current.append(instr)
            functions.append(current)
        else:
            current.append(instr)

    global_id = 0

    for func in functions:

        func_name = func[0].lhs

        # 🔥 create cluster
        with dot.subgraph(name=f"cluster_{func_name}") as sub:
            sub.attr(label=f"Function: {func_name}")

            blocks = build_blocks(func)
            blocks = connect_blocks(blocks)

            id_map = {}

            # nodes
            for block in blocks:
                new_id = str(global_id)
                id_map[block.id] = new_id

                label = ""
                for instr in block.instructions:
                    label += str(instr) + "\\l"

                sub.node(new_id, label)
                global_id += 1

            # edges
            for block in blocks:
                for nxt in block.next_blocks:
                    sub.edge(id_map[block.id], id_map[nxt.id])

    dot.render(filename, format="png", view=False)