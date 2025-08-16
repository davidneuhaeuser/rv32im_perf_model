from riscvmodel.insn import InstructionSB, InstructionSH, InstructionSW
from riscvmodel.isa import InstructionSType

from perf_model.backend.utils import set_bits_in_range
from perf_model.backend.utils.reg_names_util import map_imm_arg, map_reg_name


class STypeInstruction(InstructionSType):
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

        # append both bit-sequences to imm[11:0]
        imm = (
            (unassigned_bits & imm_mask_11_5)
            >> (cls.field_imm.base[1] - cls.field_imm.size[0])
        ) | ((unassigned_bits & imm_mask_4_0) >> cls.field_imm.base[0])

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
        InstructionSType.get_fields
        return self.encode()

    def __str__(self):
        return "{} x{}, {}(x{})".format(self.mnemonic, self.rs2, self.imm, self.rs1)

    def __repr__(self):
        return "{}({}, {}, {}) ".format(
            self.__class__.__name__, self.rs1, self.rs2, self.imm
        )


class SB(InstructionSB, STypeInstruction):
    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        InstructionSB.__init__(
            self, map_reg_name(rs1), map_reg_name(rs2), map_imm_arg(imm)
        )


class SH(InstructionSH, STypeInstruction):
    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        InstructionSH.__init__(
            self, map_reg_name(rs1), map_reg_name(rs2), map_imm_arg(imm)
        )


class SW(InstructionSW, STypeInstruction):
    def __init__(self, rs1: int = None, rs2: int = None, imm: int = None):
        InstructionSW.__init__(
            self, map_reg_name(rs1), map_reg_name(rs2), map_imm_arg(imm)
        )
