from perf_model.backend.isa.constants import (
    FUNCT2_START,
    FUNCT3_START,
    FUNCT7_START,
    IMM_I_START,
    IMM_LOWER_START,
    IMM_UPPER_START,
    RD_START,
    RS1_START,
    RS2_START,
    RS3_START,
)
from perf_model.backend.utils.reg_names_util import map_imm_arg, map_reg_name

# NOTE: rm fields are currently unused!!!


class FPRTypeInstruction_B_Usr:
    opcode = 0b1010011
    funct3 = 0

    def __init__(self, rd: int = 0, rs1: int = 0, rs2: int = 0, funct3: int = funct3):
        self.rd = map_reg_name(rd)
        self.rs1 = map_reg_name(rs1)
        self.rs2 = map_reg_name(rs2)
        self.funct3 = funct3

    def encode(self):
        funct7 = self.funct7 << FUNCT7_START
        rs2 = self.rs2 << RS2_START
        rs1 = self.rs1 << RS1_START
        funct3 = self.funct3 << FUNCT3_START
        rd = self.rd << RD_START
        opcode = self.opcode

        instruction = funct7 | rs2 | rs1 | funct3 | rd | opcode

        return instruction


class FPRTypeInstruction_B_Pre(FPRTypeInstruction_B_Usr):
    """
    For binary operations with predefined funct3/rm
    """

    def __init__(self, rd: int = 0, rs1: int = 0, rs2: int = 0):
        self.rd = map_reg_name(rd)
        self.rs1 = map_reg_name(rs1)
        self.rs2 = map_reg_name(rs2)


class FPRTypeInstruction_U_Usr(FPRTypeInstruction_B_Usr):
    """
    For unary operations and user defined funct3/rm
    """

    def __init__(self, rd: int = 0, rs1: int = 0, funct3: int = 0):
        self.rd = map_reg_name(rd)
        self.rs1 = map_reg_name(rs1)
        self.funct3 = funct3


class FPRTypeInstruction_U_Pre(FPRTypeInstruction_B_Usr):
    """
    For unary operations with predefined funct3/rm
    """

    def __init__(self, rd: int = 0, rs1: int = 0):
        self.rd = map_reg_name(rd)
        self.rs1 = map_reg_name(rs1)


class FPR4TypeInstruction:

    funct2 = 0

    def __init__(
        self,
        rd: int = 0,
        rs1: int = 0,
        rs2: int = 0,
        rs3: int = 0,
        funct3: int = 0,
    ):
        self.rd = map_reg_name(rd)
        self.rs1 = map_reg_name(rs1)
        self.rs2 = map_reg_name(rs2)
        self.rs3 = map_reg_name(rs3)
        self.funct3 = funct3

    def encode(self):
        rs3 = self.rs3 << RS3_START
        funct2 = self.funct2 << FUNCT2_START
        rs2 = self.rs2 << RS2_START
        rs1 = self.rs1 << RS1_START
        funct3 = self.funct3 << FUNCT3_START
        rd = self.rd << RD_START
        opcode = self.opcode

        instruction = rs3 | funct2 | rs2 | rs1 | funct3 | rd | opcode

        return instruction


class FLW:
    opcode = 0b0000111
    funct3 = 0b010

    def __init__(
        self,
        rd: int = 0,
        rs1: int = 0,
        imm: int = 0,
    ):
        self.rd = map_reg_name(rd)
        self.rs1 = map_reg_name(rs1)
        imm = map_imm_arg(imm)
        if imm < 0:
            imm = (0b111111111111 ^ (-1 * imm)) + 1
        self.imm = imm

    def encode(self):
        imm = self.imm << IMM_I_START
        rs1 = self.rs1 << RS1_START
        funct3 = self.funct3 << FUNCT3_START
        rd = self.rd << RD_START
        opcode = self.opcode

        instruction = imm | rs1 | funct3 | rd | opcode

        return instruction


class FSW:
    opcode = 0b0100111
    funct3 = 0b010

    def __init__(
        self,
        rs1: int = 0,
        rs2: int = 0,
        imm: int = 0,
    ):
        self.rs1 = map_reg_name(rs1)
        self.rs2 = map_reg_name(rs2)
        imm = map_imm_arg(imm)
        if imm < 0:
            imm = (0b111111111111 ^ (-1 * imm)) + 1
        self.imm = imm

    def encode(self):
        imm2 = (self.imm >> 5) << IMM_UPPER_START
        rs2 = self.rs2 << RS2_START
        rs1 = self.rs1 << RS1_START
        funct3 = self.funct3 << FUNCT3_START
        imm1 = (self.imm & 0b11111) << IMM_LOWER_START
        opcode = self.opcode

        instruction = imm2 | rs2 | rs1 | funct3 | imm1 | opcode

        return instruction


class FADD_S(FPRTypeInstruction_B_Usr):
    funct7 = 0b0000000


class FSUB_S(FPRTypeInstruction_B_Usr):
    funct7 = 0b0000100


class FMUL_S(FPRTypeInstruction_B_Usr):
    funct7 = 0b0001000


class FDIV_S(FPRTypeInstruction_B_Usr):
    funct7 = 0b0001100


class FSGNJ_S(FPRTypeInstruction_B_Pre):
    funct7 = 0b0010000
    funct3 = 0b000


class FSGNJN_S(FPRTypeInstruction_B_Pre):
    funct7 = 0b0010000
    funct3 = 0b001


class FSGNJX_S(FPRTypeInstruction_B_Pre):
    funct7 = 0b0010000
    funct3 = 0b010


class FMIN_S(FPRTypeInstruction_B_Pre):
    funct7 = 0b0010100
    funct3 = 0b000


class FMAX_S(FPRTypeInstruction_B_Pre):
    funct7 = 0b0010100
    funct3 = 0b001


class FEQ_S(FPRTypeInstruction_B_Pre):
    funct7 = 0b1010000
    funct3 = 0b010


class FLT_S(FPRTypeInstruction_B_Pre):
    funct7 = 0b1010000
    funct3 = 0b001


class FLE_S(FPRTypeInstruction_B_Pre):
    funct7 = 0b1010000
    funct3 = 0b000


class FSQRT_S(FPRTypeInstruction_U_Usr):
    funct7 = 0b0101100
    rs2 = 0b00000


class FCVT_W_S(FPRTypeInstruction_U_Usr):
    funct7 = 0b1100000
    rs2 = 0b00000


class FCVT_WU_S(FPRTypeInstruction_U_Usr):
    funct7 = 0b1100000
    rs2 = 0b00001


class FCVT_S_W(FPRTypeInstruction_U_Usr):
    funct7 = 0b1101000
    rs2 = 0b00000


class FCVT_S_WU(FPRTypeInstruction_U_Usr):
    funct7 = 0b1101000
    rs2 = 0b00001


class FMV_X_W(FPRTypeInstruction_U_Pre):
    funct7 = 0b1110000
    funct3 = 0b00000
    rs2 = 0b000


class FCLASS_S(FPRTypeInstruction_U_Pre):
    funct7 = 0b1110000
    funct3 = 0b001
    rs2 = 0b0000


class FMV_W_X(FPRTypeInstruction_U_Pre):
    funct7 = 0b1111000
    funct3 = 0b00000
    rs2 = 0b000


class FMADD_S(FPR4TypeInstruction):
    opcode = 0b1000011


class FMSUB_S(FPR4TypeInstruction):
    opcode = 0b1000111


class FNMSUB_S(FPR4TypeInstruction):
    opcode = 0b1001011


class FNMADD_S(FPR4TypeInstruction):
    opcode = 0b1001111
