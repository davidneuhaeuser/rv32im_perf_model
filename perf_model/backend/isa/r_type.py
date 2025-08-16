from riscvmodel.insn import (
    InstructionADD,
    InstructionAND,
    InstructionOR,
    InstructionSLL,
    InstructionSLT,
    InstructionSLTU,
    InstructionSRA,
    InstructionSRL,
    InstructionSUB,
    InstructionXOR,
)
from riscvmodel.isa import InstructionRType

from perf_model.backend.utils.reg_names_util import map_reg_name

from ..utils import set_bits_in_range


class RTypeInstruction(InstructionRType):
    @classmethod
    def from_no_type_mapping(cls, no_type_mapping):
        unassigned_bits = no_type_mapping["unassigned"]
        unassigned_bits = unassigned_bits << cls.field_opcode.size

        # fmt: off
        rd_mask = set_bits_in_range(cls.field_rd.base, cls.field_rd.base + cls.field_rd.size - 1)
        rs1_mask = set_bits_in_range(cls.field_rs1.base, cls.field_rs1.base + cls.field_rs1.size - 1)
        rs2_mask = set_bits_in_range(cls.field_rs2.base, cls.field_rs2.base + cls.field_rs2.size - 1)
        # fmt: on

        rd = (unassigned_bits & rd_mask) >> cls.field_rd.base
        rs1 = (unassigned_bits & rs1_mask) >> cls.field_rs1.base
        rs2 = (unassigned_bits & rs2_mask) >> cls.field_rs2.base

        return cls(rd=rd, rs1=rs1, rs2=rs2)

    @classmethod
    def from_r_type_mapping(cls, r_type_mapping):
        return cls(
            rd=r_type_mapping["rd"],
            rs1=r_type_mapping["rs1"],
            rs2=r_type_mapping["rs2"],
        )

    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        super().__init__(rd, rs1, rs2)

    @property
    def no_type_mapping(self):
        int_value = self.value
        unsigned_values = int_value >> self.field_opcode.size
        return {"opcode": self.field_opcode.value, "unassigned": unsigned_values}

    @property
    def r_type_mapping(self):
        mapping_dict = {
            "opcode": self.field_opcode.value,
            "rd": self.rd,
            "funct3": self.field_funct3.value,
            "rs1": self.rs1,
            "rs2": self.rs2,
            "funct7": self.field_funct7.value,
        }

        return mapping_dict

    @property
    def value(self):
        return self.encode()

    def __str__(self):
        return "{} x{}, x{}, x{}".format(self.mnemonic, self.rd, self.rs1, self.rs2)

    def __repr__(self):
        return "{}({}, {}, {}) ".format(
            self.__class__.__name__, self.rd, self.rs1, self.rs2
        )


class ADD(InstructionADD, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionADD.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )


class SUB(InstructionSUB, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionSUB.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )


class XOR(InstructionXOR, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionXOR.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )


class OR(InstructionOR, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionOR.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )


class AND(InstructionAND, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionAND.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )


class SLL(InstructionSLL, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionSLL.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )


class SRL(InstructionSRL, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionSRL.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )


class SRA(InstructionSRA, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionSRA.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )


class SLT(InstructionSLT, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionSLT.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )


class SLTU(InstructionSLTU, RTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, rs2: int = None):
        InstructionSLTU.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
        RTypeInstruction.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_reg_name(rs2)
        )
