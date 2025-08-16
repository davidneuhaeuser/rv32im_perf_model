from typing import Literal

import readelf

# import readelf.const
from riscvmodel.code import MachineDecodeError, decode
from riscvmodel.isa import Instruction, Variant

from perf_model.backend.isa.constants import BYTE, INSTRUCTION_WIDTH
from perf_model.backend.isa.i_type import ADDI, EBREAK, JALR
from perf_model.backend.isa.u_type import LUI
from perf_model.backend.utils.int32 import int32_to_int, int_to_int32
from perf_model.backend.utils.memnonic_dictonary import mem_dict

IBYTES = INSTRUCTION_WIDTH // BYTE
assert IBYTES * BYTE == INSTRUCTION_WIDTH, "Instruction Width not byte aligned"

ZEROBYTE = bytes(1)  # A zero byte, for padding

# stores an instruction-bit-value when there is no
# instruction available from riscvmodel
class InstructionValueWrapper:
    def __init__(self, bit_value):
        self.value = bit_value

    def encode(self):
        return self.value


LEGACY_INSTRUCTION_PARSE: bool = False


def parse_machinecode_instruction(
    b: bytes, endianness: Literal["big", "little"] = "little"
) -> Instruction:
    """
    Converts the bytes of compiled machinecode to the corresponding instruction object

    Parameters
    ----------
    b: bytes
        The bytes to be converted into an instructinon object
    endianness: "big" | "little"
        The endianness of the machinecode. Default is little.

    Returns
    -------
    Instruction
        The Instruction object correspondingto the given bytes
    """
    if not LEGACY_INSTRUCTION_PARSE:
        instr_int = int.from_bytes(b, endianness)
        if instr_int == 0x100073:
            return EBREAK(0, 0, 0)
        try:
            return decode(instr_int, Variant("RV32IM"))
        except MachineDecodeError:
            # as decode does not properly decode instructions for RV32IF
            # this wrapper is used
            return InstructionValueWrapper(instr_int)

    # convert to integer since that is what the riscv model decoder takes as input
    i = int.from_bytes(b, endianness)
    ins = decode(i)
    # Check the precomputed dictionary that links the mnemonic to the field layout and instruction class
    inst_info = mem_dict[ins.mnemonic]
    values = []
    # Add each field of the read instruction (stuff like rd and imm) in the correct order
    for field in inst_info.Fields:
        v = ins.__getattribute__(field)
        if not isinstance(v, int):
            v = v.value
        values.append(v)
    # and then create the corresponding class with those values as initial values.
    return inst_info.IClass(*values)


# Constants for parsing
errstr = "Please contact the maintainer (Chris) and give them ELF file that caused the error/warning. Where applicable also give them the source code and compile steps (e.g. makefile + linkerscript)."
dynsht = [
    readelf.const.SHT.SHT_DYNAMIC,
    readelf.const.SHT.SHT_DYNSYM,
    readelf.const.SHT.SHT_RELA,
    readelf.const.SHT.SHT_REL,
]
dynsn = [".got", ".got.plt", ".data.rel.ro", ".rel.dyn", ".rel.plt"]
supported = [".text", ".data", ".bss", ".text.start"]
supported_prefix = [".text"]
discard = [".eh_frame"]  # We dont have interrupts so its lot like well be using this


def is_supported(section_name: str) -> bool:
    if section_name in supported:
        return True
    for prefix in supported_prefix:
        if section_name.startswith(prefix):
            return True
    return False


def advanced_parse(
    file_name: str,
    a0: int | None = None,
    a1: int | None = None,
    code_section_first=False,
) -> tuple[list[int], list[Instruction], int]:
    """
    Parses a given ELF file into the datamemory contents, the list of instructions, and the offset IMEM is located at in "virtual" storage

    Parameters
    ----------
    file_name: str
        The path to the ELF file
    a0: int
        optional value to initialize register a0 to
    a1: int
        optional value to initialize register a1 to
    Returns
    -------
    memory: list[int]
        Contents of Data Memory
    instructions: list[instruction]
        List of instructions in the executable sections
    IMEMOffset: int
        offset that the executable part of the code has from what the linker thinks it has
    """
    file = readelf.readelf(file_name)

    symboltab = file.find_section(".symtab")
    IMEMOffset = symboltab.get_symbol("IMEMO")._value
    RAMSize = symboltab.get_symbol("RAMSIZE")._value

    memory = [0] * RAMSize

    imem_sections: list[readelf.Section] = []
    for section in file.sections:
        if section.type in dynsht or section.name in dynsn:
            # raise ValueError(
            #     "Section type assosciated with dynamic linking detected!\n" + errstr
            # )
            continue
        if section.name in discard:
            continue
        flags: list[readelf.const.SHF] = section.flags
        if readelf.const.SHF.SHF_ALLOC in flags:
            if not is_supported(section.name):
                # print("WARNING: Unknown section " + section.name + " \n" + errstr)
                continue

            # Code section # TODO: replace with proper implementation
            check_section = (
                section.name[0:5]
                == ".text"
                # section.addr <= IMEMOffset
                # if code_section_first
                # else section.addr >= IMEMOffset
            )

            if check_section:
                imem_sections.append(section)

            # Memory section
            elif section.name[0:5] == ".data":
                # non executable section, so it shouldnt be executable
                if readelf.const.SHF.SHF_EXECINSTR in flags:
                    # raise ValueError("Executable section in RAM!\n" + errstr)
                    continue
                if section.type == readelf.const.SHT.SHT_NOBITS:
                    # .bss, we dont need to do anything since we allocate the full memory
                    continue

                address = 0  # section.addr # TODO: should probably be fixed for multipe sections
                content = section.content
                # Set memory bytes
                for byte in content:
                    intbyte = int(byte)
                    memory[address] = intbyte
                    address += 1

    code: bytes = bytes(0)
    # sort sections by where they have to be in memory
    imem_sections.sort(key=lambda section: section.addr)
    # Put all the code sections in the right order, and pad any possible empty space between them
    for i in range(len(imem_sections)):
        section = imem_sections[i]
        code += section.content
        if i + 1 < len(imem_sections):
            space = section.addr + section.size - imem_sections[i + 1].addr
            if space > 0:
                # Pad any empty space between instruction sections
                code += ZEROBYTE * space
    inum = len(code) // IBYTES
    instructions = []
    for i in range(inum):
        # TODO: This needs to be adjusted once compressed instructions get added
        readBytes = code[i * 4 : i * 4 + IBYTES]
        instruction = parse_machinecode_instruction(readBytes)
        instructions.append(instruction)

    # set a0 and a1 if neccessary:
    if a0 != None:
        l0, l1 = li(a0)
        instructions[1] = LUI(10, l1)
        if li != 0:
            instructions[0] = ADDI(10, 0, l0)

    if a1 != None:
        l0, l1 = li(a1)
        instructions[3] = LUI(10, l1)
        if li != 0:
            instructions[2] = ADDI(10, 0, l0)
    return memory, instructions, IMEMOffset


LOWMASK = (2**12) - 1
HIMASK = ~LOWMASK


def li(i: int) -> tuple[int, int]:
    """
    Splits i into two integers so it can be loaded into a register
    using addi with the first, and lui with the second returned integer.
    """

    # We can just use addi here
    if i >= -2048 and i <= 2047:
        return i, 0

    i32 = int_to_int32(i)
    lower = i32 & LOWMASK
    highr = (i32 & HIMASK) >> 12

    if lower > 2047:
        lower -= 4096
        highr += 1

    assert int32_to_int(lower + (highr << 12)) == i
    return lower, highr
