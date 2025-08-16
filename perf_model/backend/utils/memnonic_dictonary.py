from perf_model.backend.isa.b_type import *
from perf_model.backend.isa.i_type import *
from perf_model.backend.isa.j_type import *
from perf_model.backend.isa.r_type import *
from perf_model.backend.isa.s_type import *
from perf_model.backend.isa.u_type import *
from perf_model.backend.utils.mem_dict_gen import Inst

mem_dict: dict[str, Inst] = {
    "add": Inst(IClass=ADD, Fields=["rd", "rs1", "rs2"]),
    "sub": Inst(IClass=SUB, Fields=["rd", "rs1", "rs2"]),
    "sll": Inst(IClass=SLL, Fields=["rd", "rs1", "rs2"]),
    "slt": Inst(IClass=SLT, Fields=["rd", "rs1", "rs2"]),
    "sltu": Inst(IClass=SLTU, Fields=["rd", "rs1", "rs2"]),
    "xor": Inst(IClass=XOR, Fields=["rd", "rs1", "rs2"]),
    "srl": Inst(IClass=SRL, Fields=["rd", "rs1", "rs2"]),
    "sra": Inst(IClass=SRA, Fields=["rd", "rs1", "rs2"]),
    "or": Inst(IClass=OR, Fields=["rd", "rs1", "rs2"]),
    "and": Inst(IClass=AND, Fields=["rd", "rs1", "rs2"]),
    "lb": Inst(IClass=LB, Fields=["rd", "rs1", "imm"]),
    "lh": Inst(IClass=LH, Fields=["rd", "rs1", "imm"]),
    "lw": Inst(IClass=LW, Fields=["rd", "rs1", "imm"]),
    "lbu": Inst(IClass=LBU, Fields=["rd", "rs1", "imm"]),
    "lhu": Inst(IClass=LHU, Fields=["rd", "rs1", "imm"]),
    "jalr": Inst(IClass=JALR, Fields=["rd", "rs1", "imm"]),
    "addi": Inst(IClass=ADDI, Fields=["rd", "rs1", "imm"]),
    "slti": Inst(IClass=SLTI, Fields=["rd", "rs1", "imm"]),
    "sltiu": Inst(IClass=SLTIU, Fields=["rd", "rs1", "imm"]),
    "xori": Inst(IClass=XORI, Fields=["rd", "rs1", "imm"]),
    "ori": Inst(IClass=ORI, Fields=["rd", "rs1", "imm"]),
    "andi": Inst(IClass=ANDI, Fields=["rd", "rs1", "imm"]),
    "ecall": Inst(IClass=ECALL, Fields=["rd", "rs1", "imm"]),
    "ebreak": Inst(IClass=EBREAK, Fields=["rd", "rs1", "imm"]),
    "slli": Inst(IClass=SLLI, Fields=["rd", "rs1", "shamt"]),
    "srli": Inst(IClass=SRLI, Fields=["rd", "rs1", "shamt"]),
    "srai": Inst(IClass=SRAI, Fields=["rd", "rs1", "shamt"]),
    "sb": Inst(IClass=SB, Fields=["rs1", "rs2", "imm"]),
    "sh": Inst(IClass=SH, Fields=["rs1", "rs2", "imm"]),
    "sw": Inst(IClass=SW, Fields=["rs1", "rs2", "imm"]),
    "beq": Inst(IClass=BEQ, Fields=["rs1", "rs2", "imm"]),
    "bne": Inst(IClass=BNE, Fields=["rs1", "rs2", "imm"]),
    "blt": Inst(IClass=BLT, Fields=["rs1", "rs2", "imm"]),
    "bge": Inst(IClass=BGE, Fields=["rs1", "rs2", "imm"]),
    "bltu": Inst(IClass=BLTU, Fields=["rs1", "rs2", "imm"]),
    "bgeu": Inst(IClass=BGEU, Fields=["rs1", "rs2", "imm"]),
    "jal": Inst(IClass=JAL, Fields=["rd", "imm"]),  # added manually
    "lui": Inst(IClass=LUI, Fields=["rd", "imm"]),  # added manually
    "auipc": Inst(IClass=AUIPC, Fields=["rd", "imm"]),  # added manually
}
