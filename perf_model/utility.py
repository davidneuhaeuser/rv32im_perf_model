import os


def print_program(program: list):
    for i in program:
        print(str(i))


def instr_str(instruction: list[str]) -> str:
    instr: str = ""
    for s in instruction:
        instr += s + " "
    return instr


def generate_asm(instructions: list, name: str) -> list[str]:
    os.system("mkdir -p asm")

    path: str = "asm/" + name + ".asm"

    if os.path.isfile(path):
        path = "asm/" + name + "-1" + ".asm"

    for i in range(2, 100):
        if os.path.isfile(path):
            path = "asm/" + name + "-" + str(i) + ".asm"
        else:
            break

    f = open(path, "w")

    for i in instructions:
        f.write(str(i) + "\n")
    f.close()


def get_program(instructions: list) -> list[list[str]]:

    program: list[list[str]] = [[""]] * (len(instructions))

    for i in range(len(instructions)):
        program[i] = simplify_instr(str(instructions[i])).split(" ")
        # for j in range(1, len(program[i])):
        #     program[i][j] = program[i][j].replace("x", "")

    return program


def btd_conversion(num: int):
    if (0x80000000 & num) and (num > 0):
        num = -1 * ((num ^ 0xFFFFFFFF) + 1)
    return num


def simplify_instr(instr: str) -> str:
    i = instr.replace(",", "")
    i = i.replace(".", "")
    i = i.replace("+", "")
    i = i.replace("0x", "H")
    i = i.replace("(", " ")
    i = i.replace(")", "")
    i = i.replace(" x", " ")
    i = i.replace("H", "0x")
    return i


def print_help():
    print("\nrun.py [OPTIONS] [EXECUTABLES] ")
    print(
        "\n[EXECUTABLES]\ta path to an executable"
        + "or to a folder containing multiple executables"
    )
    print("[OPTIONS]\ta set of the listed options:\n")
    print("\t-v\tverbose; prints simulation runtime info (e.g. memory acceses, ...)")
    print("\t-p\tprogram; outputs the simulated asm programs to the command line")
    print("\t--asm\tgenerates the asm files for all simulated executables")
    print(
        "\t-i\tprogram instruction histogram;"
        + "generates a histogram of instructions of simulated programs"
    )
    print(
        "\t-I\texecution instruction histogram;"
        + "generates a histogram of instructions of the simulated programs execution\n"
    )


def print_header(header: str = None, width: int = 50, nl: bool = True):
    if header == None:
        print("\n" + "#" * width)
        return

    space = width - len(header)
    pos = space // 2

    if nl:
        print("\n" + "-" * pos, header, "-" * (space - pos))
    else:
        print("-" * pos, header, "-" * (space - pos))


def print_prog_hist(program: list[list[str]]):
    allops: list[str] = []
    ops: list[str] = []
    zipped: list[list[str, int]] = []

    for i in program:
        allops += [i[0]]

    for i in allops:
        if i not in ops:
            ops += [i]

    for op in ops:
        zipped += [[op, allops.count(op)]]

    zipped.sort(key=lambda x: x[1], reverse=True)

    for op in zipped:
        print(op[0] + ":", "\t\t", op[1])


def print_exec_hist(history: list[list[str]]):
    ops: list[str] = []
    zipped: list[list[str, int]] = []

    for op in history:
        if op not in ops:
            ops += [op]

    for op in ops:
        zipped += [[op, history.count(op)]]

    zipped.sort(key=lambda x: x[1], reverse=True)

    for op in zipped:
        print(op[0] + ":", "\t\t", op[1])


def get_executables(dir: str) -> list[str]:
    executables: list[str] = []

    for (_, dirnames, filenames) in os.walk(dir):
        for f in filenames:
            executables.append(dir + "/" + f)

    for i in range(len(executables)):
        executables[i] = executables[i].replace("//", "/")

    if executables == []:
        return [dir]

    return executables
