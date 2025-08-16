def print_program(program: list):
    for i in program:
        print(str(i))


def instr_str(instruction: list[str]) -> str:
    instr: str = ""
    for s in instruction:
        instr += s + " "
    return instr


def generate_asm(instructions: list, name: str) -> list[str]:
    f = open("perf_model/asm_files/" + name + ".asm", "w")
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
