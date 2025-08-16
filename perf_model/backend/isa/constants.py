from perf_model.backend.utils.utils import create_float32

DATA_WIDTH = 32
ADDRESS_WIDTH = DATA_WIDTH

BYTE = 8

REG_ADDR_WIDTH = 5

# instruction related
INSTRUCTION_WIDTH = DATA_WIDTH

# from RISC-V Card
OPCODE_R_ARLOG = 0b0110011
OPCODE_I_ARLOG = 0b0010011
OPCODE_I_LOAD = 0b0000011
OPCODE_S = 0b0100011
OPCODE_B = 0b1100011
OPCODE_JAL = 0b1101111
OPCODE_JALR = 0b1100111
OPCODE_LUI = 0b0110111
OPCODE_AUIPC = 0b0010111

OPCODE_FLW = 0b0000111
OPCODE_FSW = 0b0100111
OPCODE_FP_BIN_OP = 0b1010011
OPCODE_FMADD_S = 0b1000011
OPCODE_FMSUB_S = 0b1000111
OPCODE_FNMADD_S = 0b1001111
OPCODE_FNMSUB_S = 0b1001011

OPCODE_WIDTH = 7
RS1_WIDTH = REG_ADDR_WIDTH
RS2_WIDTH = REG_ADDR_WIDTH
RD_WIDTH = REG_ADDR_WIDTH

FUNCT3_WIDTH = 3
FUNCT7_WIDTH = 7

# components related
INSTRUCTION_MEMORY_DEPTH = 1024 * 4

# data memory size in words (4kb)
DATA_MEMORY_DEPTH = 1024 * 4

REG_FILE_DEPTH = 2 ** (REG_ADDR_WIDTH)

PC_WIDTH = ADDRESS_WIDTH

IMM_GEN_INPUT_WIDTH = 25
CONTROL_UNIT_INPUT_WIDTH = OPCODE_WIDTH

ALU_CONTROL_INPUT_WIDTH = 4
ALUCTRL_OP_WIDTH = 2  # signal between control_unit and alu_ctrl
ALU_OP_WIDTH = 4  # signal between alu_ctrl and ALU

DATA_TYPE_WIDTH = 3  # data type for data memory
# 0 == byte
# 1 == half
# 2 == word
# 4 == byte (extend)
# 5 == half (extend)

IMM_MODE_WIDTH = 3


IMEMO = 0x00100000
PUTSA = 0x10000004

GETSBUFS = 32  # Size, in words, of the stdin buffer
GETSA = 0x11000004  # Adress that getchar will read from
GETSA2 = GETSA + DATA_WIDTH * GETSBUFS

# constants for floating-point related components
FLOAT32_SIZE = DATA_WIDTH
FP_ALU_OPERATION_WIDTH = 5
FP_RM_WIDTH = FUNCT3_WIDTH
FP_ALU_CTRL_MODE_WIDTH = 3
FUNCT5_WIDTH = 5
FP_FMT_WIDTH = 2

REGDICTA = {
    "x0": "zero",
    "x1": "ra",
    "x2": "sp",
    "x3": "gp",
    "x4": "tp",
    "x5": "t0",
    "x6": "t1",
    "x7": "t2",
    "x8": "s0",
    "x9": "s1",
    "x10": "a0",
    "x11": "a1",
    "x12": "a2",
    "x13": "a3",
    "x14": "a4",
    "x15": "a5",
    "x16": "a6",
    "x17": "a7",
    "x18": "s2",
    "x19": "s3",
    "x20": "s4",
    "x21": "s5",
    "x22": "s6",
    "x23": "s7",
    "x24": "s8",
    "x25": "s9",
    "x26": "s10",
    "x27": "s11",
    "x28": "t3",
    "x29": "t4",
    "x30": "t5",
    "x31": "t6",
}
REGDICTB = {
    "zero": 0,
    "ra": 1,
    "sp": 2,
    "gp": 3,
    "tp": 4,
    "t0": 5,
    "t1": 6,
    "t2": 7,
    "s0": 8,
    "s1": 9,
    "a0": 10,
    "a1": 11,
    "a2": 12,
    "a3": 13,
    "a4": 14,
    "a5": 15,
    "a6": 16,
    "a7": 17,
    "s2": 18,
    "s3": 19,
    "s4": 20,
    "s5": 21,
    "s6": 22,
    "s7": 23,
    "s8": 24,
    "s9": 25,
    "s10": 26,
    "s11": 27,
    "t3": 28,
    "t4": 29,
    "t5": 30,
    "t6": 31,
}
FLOAT32_POS_INFTY = create_float32(0, 255, 0)
FLOAT32_NEG_INFTY = create_float32(1, 255, 0)
FLOAT32_POS_ZERO = create_float32(0, 0, 0)
FLOAT32_NEG_ZERO = create_float32(1, 0, 0)
FLOAT32_QUIET_NAN = create_float32(0, 255, 1 << 22)
FLOAT32_SIGNALING_NAN = create_float32(0, 255, 1)
FLOAT32_POS_ONE: int = create_float32(0, 127, 0)
FLOAT32_NEG_ONE: int = create_float32(1, 127, 0)
int32_range: tuple[int, int] = (-(2**31), 2**31 - 1)
uint32_range: tuple[int, int] = (0, 2**32 - 1)
float32_range: tuple[float, float] = (-3.4028347e38, 3.4028347e38)
float32_positive_precision_range: tuple[float, float] = (
    1.17549435e-38,
    3.40282347e38,
)
float32_range_small: tuple[float, float] = int32_range

# shift amounts for bit shifts for instruction layouts (floating point)
RD_START = 7
IMM_LOWER_START = 7
FUNCT3_START = 12
RS1_START = 15
RS2_START = 20
IMM_I_START = 20
IMM_UPPER_START = 25
FUNCT2_START = 25
FUNCT7_START = 25
RS3_START = 27
FUNCT5_START = 27

IMM_LOWER_WIDTH = 5
IMM_WIDTH = 12
