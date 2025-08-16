import sys
import time
from os import walk

from perf_model.backend.utils.load_binary import advanced_parse
from perf_model.perf_model_config import (
    BLOCK_SIZE,
    CACHE_ERROR_CORRECTION,
    CACHED,
    DMEM_OFFSET,
    MEM_SIZE,
    MULT_DELAY,
    READ_DELAY,
    SETS,
    WAYS,
    WRITE_DELAY,
)
from perf_model.perf_model_rv32im import RV32IMCachedProcessor
from perf_model.utility import generate_asm, get_program, print_program


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


def run():

    executables: list[str] = []

    args: list[str] = sys.argv[1:]

    verbose: bool = False
    print_prog: bool = False
    gen_asm: bool = False
    prog_hist: bool = False
    exec_hist: bool = False

    if ("-h" in args) or ("--help" in args):
        print_help()
        return

    if "-v" in args:
        verbose = True
        args.remove("-v")

    if "-p" in args:
        print_prog = True
        args.remove("-p")

    if "--asm" in args:
        args.remove("--asm")
        gen_asm = True

    if "-i" in args:
        args.remove("-i")
        prog_hist = True

    if "-I" in args:
        args.remove("-I")
        exec_hist = True

    if len(args) < 1:
        print("missing required argument: <executable_path>")

    for i in range(len(args)):
        executables += get_executables(args[i])

    executables.sort()

    for executable in executables:

        print_header()

        program: str = executable.split("/")[-1]

        print_header(f"RUNNING '{program}'")

        mem_init, instructions, _ = advanced_parse(executable)
        proc = RV32IMCachedProcessor(
            program=get_program(instructions),
            mem_size=MEM_SIZE,
            mem_init=mem_init,
            read_delay=READ_DELAY,
            write_delay=WRITE_DELAY,
            mult_delay=MULT_DELAY,
            ways=WAYS,
            sets=SETS,
            blsz=BLOCK_SIZE,
            dmem_offset=DMEM_OFFSET,
            cache_error_correction=CACHE_ERROR_CORRECTION,
            cached=CACHED,
        )

        if print_prog:
            print_header("PROGRAM")
            print_program(instructions)

        print_header("STARTED SIMULATION")
        start = time.time()
        proc.simulate(track_exec=True)
        end = time.time()

        print_header(f"SIMULATION FINISHED AFTER")
        print_header(header=f"{proc.ccs:,} CYCLES", nl=False)
        print_header(f"RETURN VALUE: {proc.return_value()}")
        print_header(f"SIMULATION TIME: {(end - start):.4f} seconds")

        if gen_asm:
            generate_asm(instructions, program)

        if verbose:
            print_header("RUNTIME INFO")
            proc.print_runtime_info()
            print_header("CACHE")
            proc.print_cache()

        if prog_hist:
            print_header("PROGRAM INSTRUCTION HISTOGRAM")
            allops: list[str] = []
            ops: list[str] = []
            zipped: list[list[str, int]] = []

            for i in proc.program:
                allops += [i[0]]

            for i in allops:
                if i not in ops:
                    ops += [i]

            for op in ops:
                zipped += [[op, allops.count(op)]]

            zipped.sort(key=lambda x: x[1], reverse=True)

            for op in zipped:
                print(op[0] + ":", "\t\t", op[1])

        if exec_hist:
            print_header("EXECUTION INSTRUCTION HISTOGRAM")
            ops: list[str] = []
            zipped: list[list[str, int]] = []

            for op in proc.exec_history:
                if op not in ops:
                    ops += [op]

            for op in ops:
                zipped += [[op, proc.exec_history.count(op)]]

            zipped.sort(key=lambda x: x[1], reverse=True)

            for op in zipped:
                print(op[0] + ":", "\t\t", op[1])


def get_executables(dir: str) -> list[str]:
    executables: list[str] = []

    for (_, dirnames, filenames) in walk(dir):
        for f in filenames:
            executables.append(dir + "/" + f)

    for i in range(len(executables)):
        executables[i] = executables[i].replace("//", "/")

    if executables == []:
        return [dir]

    return executables
