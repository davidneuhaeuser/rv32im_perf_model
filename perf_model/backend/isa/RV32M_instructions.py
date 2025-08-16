from perf_model.backend.isa.constants import (
    FUNCT3_START,
    FUNCT7_START,
    RD_START,
    RS1_START,
    RS2_START,
)
from perf_model.backend.utils.reg_names_util import map_reg_name


class MultiplyInstr:
    opcode = 0b0110011
    funct7 = 0x01

    def __init__(self, rd: int = 0, rs1: int = 0, rs2: int = 0):
        self.rd = map_reg_name(rd)
        self.rs1 = map_reg_name(rs1)
        self.rs2 = map_reg_name(rs2)

    def encode(self):
        funct7 = self.funct7 << FUNCT7_START
        rs2 = self.rs2 << RS2_START
        rs1 = self.rs1 << RS1_START
        funct3 = self.funct3 << FUNCT3_START
        rd = self.rd << RD_START
        opcode = self.opcode

        instruction = funct7 | rs2 | rs1 | funct3 | rd | opcode

        return instruction


class MUL(MultiplyInstr):
    funct3 = 0x0

    def __str__(self):
        return "mul x" + str(self.rd) + ", x" + str(self.rs1) + ", x" + str(self.rs2)


class MULH(MultiplyInstr):
    funct3 = 0x1

    def __str__(self):
        return "mulh x" + str(self.rd) + ", x" + str(self.rs1) + ", x" + str(self.rs2)


class MULHSU(MultiplyInstr):
    funct3 = 0x2

    def __str__(self):
        return "mulhsu x" + str(self.rd) + ", x" + str(self.rs1) + ", x" + str(self.rs2)


class MULHU(MultiplyInstr):
    funct3 = 0x3

    def __str__(self):
        return "mulhu x" + str(self.rd) + ", x" + str(self.rs1) + ", x" + str(self.rs2)


class DIV(MultiplyInstr):
    funct3 = 0x4

    def __str__(self):
        return "div x" + str(self.rd) + ", x" + str(self.rs1) + ", x" + str(self.rs2)


class DIVU(MultiplyInstr):
    funct3 = 0x5

    def __str__(self):
        return "divu x" + str(self.rd) + ", x" + str(self.rs1) + ", x" + str(self.rs2)


class REM(MultiplyInstr):
    funct3 = 0x6

    def __str__(self):
        return "rem x" + str(self.rd) + ", x" + str(self.rs1) + ", x" + str(self.rs2)


class REMU(MultiplyInstr):
    funct3 = 0x7

    def __str__(self):
        return "remu x" + str(self.rd) + ", x" + str(self.rs1) + ", x" + str(self.rs2)
