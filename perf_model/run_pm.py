import sys
import time

from perf_model.backend.utils.load_binary import advanced_parse
from perf_model.perf_model_rv32im import RV32IMCachedProcessor
from perf_model.utility import (
    generate_asm,
    get_executables,
    get_program,
    print_exec_hist,
    print_header,
    print_help,
    print_prog_hist,
    print_program,
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

        program_name: str = executable.split("/")[-1]

        mem_init, instructions, _ = advanced_parse(executable)
        proc = RV32IMCachedProcessor(
            program=get_program(instructions),
            mem_init=mem_init,
        )

        print_header()
        print_header(f"RUNNING '{program_name}'")
        print_header("STARTED SIMULATION")

        start = time.time()
        proc.simulate(track_exec=exec_hist)
        end = time.time()

        print_header(f"SIMULATION FINISHED AFTER")
        print_header(header=f"{proc.ccs:,} CYCLES", nl=False)
        print_header(f"RETURN VALUE: {proc.return_value()}")
        print_header(f"SIMULATION TIME: {(end - start):.4f} seconds")

        if print_prog:
            print_header("EXECUTED PROGRAM")
            print_program(instructions)

        if gen_asm:
            generate_asm(instructions, program_name)

        if verbose:
            print_header("RUNTIME INFO")
            proc.print_runtime_info()
            print_header("FINAL CACHE STATE")
            proc.print_cache()

        if prog_hist:
            print_header("PROGRAM INSTRUCTION HISTOGRAM")
            print_prog_hist(proc.program)

        if exec_hist:
            print_header("EXECUTION INSTRUCTION HISTOGRAM")
            print_exec_hist(proc.exec_history)
