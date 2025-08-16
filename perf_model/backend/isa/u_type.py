from riscvmodel.insn import InstructionAUIPC, InstructionLUI
from riscvmodel.isa import InstructionUType

from perf_model.backend.utils.reg_names_util import map_imm_arg, map_reg_name

from ..utils import set_bits_in_range


class UTypeInstruction(InstructionUType):
    @classmethod
    def from_no_type_mapping(cls, no_type_mapping):
        unassigned_bits = no_type_mapping["unassigned"]
        unassigned_bits = unassigned_bits << cls.field_opcode.size

        rd_mask = set_bits_in_range(
            cls.field_rd.base, cls.field_rd.base + cls.field_rd.size - 1
        )

        imm_mask = set_bits_in_range(
            cls.field_imm.base, cls.field_imm.base + cls.field_imm.size - 1
        )

        rd = (unassigned_bits & rd_mask) >> cls.field_rd.base
        imm = (unassigned_bits & imm_mask) >> cls.field_imm.base

        return cls(rd=rd, imm=imm)

    @classmethod
    def from_u_type_mapping(cls, r_type_mapping):
        return cls(
            rd=r_type_mapping["rd"],
            imm=r_type_mapping["imm"],
        )

    def __init__(self, rd: int = None, imm: int = None):
        super().__init__(rd, imm)

    @property
    def no_type_mapping(self):
        int_value = self.value
        unsigned_values = int_value >> self.field_opcode.size
        return {"opcode": self.field_opcode.value, "unassigned": unsigned_values}

    @property
    def u_type_mapping(self):
        mapping_dict = {
            "opcode": self.field_opcode.value,
            "rd": self.rd,
            "imm": self.field_imm.value,
        }

        return mapping_dict

    @property
    def value(self):
        return self.encode()

    def __str__(self):
        return "{} x{}, {}".format(self.mnemonic, self.rd, self.imm)

    def __repr__(self):
        return "{}({}, {}) ".format(self.__class__.__name__, self.rd, self.imm)


class LUI(InstructionLUI, UTypeInstruction):
    def __init__(self, rd: int = None, imm: int = None):
        InstructionLUI.__init__(self, map_reg_name(rd), map_imm_arg(imm))


class AUIPC(InstructionAUIPC, UTypeInstruction):
    def __init__(self, rd: int = None, imm: int = None):
        InstructionAUIPC.__init__(self, map_reg_name(rd), map_imm_arg(imm))
