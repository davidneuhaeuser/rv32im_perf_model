from riscvmodel.insn import (
    InstructionBEQ,
    InstructionBGE,
    InstructionBGEU,
    InstructionBLT,
    InstructionBLTU,
    InstructionBNE,
)
from riscvmodel.isa import InstructionBType

from perf_model.backend.utils import set_bits_in_range
from perf_model.backend.utils.reg_names_util import map_imm_arg, map_reg_name


class BTypeInstruction(InstructionBType):
    @classmethod
    def from_no_type_mapping(cls, no_type_mapping):
        unassigned_bits = no_type_mapping["unassigned"]
        unassigned_bits = unassigned_bits << cls.field_opcode.size

        rs1_mask = set_bits_in_range(
            cls.field_rs1.base, cls.field_rs1.base + cls.field_rs1.size - 1
        )
        rs2_mask = set_bits_in_range(
            cls.field_rs1.base, cls.field_rs2.base + cls.field_rs2.size - 1
        )
        imm_mask_11_5 = set_bits_in_range(
            cls.field_imm.base[1], cls.field_imm.base[1] + cls.field_imm.size[1] - 1
        )
        imm_mask_4_0 = set_bits_in_range(
            cls.field_imm.base[0], cls.field_imm.base[0] + cls.field_imm.size[0] - 1
        )

        rs1 = (unassigned_bits & rs1_mask) >> cls.field_rs1.base
        rs2 = (unassigned_bits & rs2_mask) >> cls.field_rs2.base

        imm_11 = (unassigned_bits >> 7) & 0b1
        imm_4_1 = (unassigned_bits >> 8) & 0b1111
        imm_10_5 = (unassigned_bits >> 25) & 0b111111
        imm_12 = (unassigned_bits >> 31) & 0b1
        imm = (imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)

        if imm_12:  # sign bit is set
            (1 << 13)

        return cls(rs1=rs1, rs2=rs2, imm=imm)

    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        super().__init__(rs1, rs2, imm)

    @property
    def no_type_mapping(self):
        int_value = self.value
        unsigned_values = int_value >> self.field_opcode.size
        return {"opcode": self.field_opcode.value, "unassigned": unsigned_values}

    @property
    def value(self):
        InstructionBType.get_fields
        return self.encode()

    def __str__(self):
        return "{} x{}, x{}, .{:+}".format(self.mnemonic, self.rs1, self.rs2, self.imm)

    def __repr__(self):
        return "{}({}, {}, {}) ".format(
            self.__class__.__name__, self.rs1, self.rs2, self.imm
        )


class BEQ(InstructionBEQ, BTypeInstruction):
    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        InstructionBEQ.__init__(
            self, map_reg_name(rs1), map_reg_name(rs2), map_imm_arg(imm)
        )


class BNE(InstructionBNE, BTypeInstruction):
    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        InstructionBNE.__init__(
            self, map_reg_name(rs1), map_reg_name(rs2), map_imm_arg(imm)
        )


class BLT(InstructionBLT, BTypeInstruction):
    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        InstructionBLT.__init__(
            self, map_reg_name(rs1), map_reg_name(rs2), map_imm_arg(imm)
        )


class BGE(InstructionBGE, BTypeInstruction):
    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        InstructionBGE.__init__(
            self, map_reg_name(rs1), map_reg_name(rs2), map_imm_arg(imm)
        )


class BLTU(InstructionBLTU, BTypeInstruction):
    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        InstructionBLTU.__init__(
            self, map_reg_name(rs1), map_reg_name(rs2), map_imm_arg(imm)
        )


class BGEU(InstructionBGEU, BTypeInstruction):
    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        InstructionBGEU.__init__(
            self, map_reg_name(rs1), map_reg_name(rs2), map_imm_arg(imm)
        )
