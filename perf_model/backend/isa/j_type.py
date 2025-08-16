from riscvmodel.insn import InstructionJAL
from riscvmodel.isa import InstructionJType

from perf_model.backend.utils.reg_names_util import map_imm_arg, map_reg_name

from ..utils import set_bits_in_range


class JTypeInstruction(InstructionJType):
    @classmethod
    def from_no_type_mapping(cls, no_type_mapping):
        unassigned_bits = no_type_mapping["unassigned"]
        unassigned_bits <<= cls.field_opcode.size

        rd_mask = set_bits_in_range(
            cls.field_rd.base, cls.field_rd.base + cls.field_rd.size - 1
        )

        imm_mask = [0] * 4

        for i in range(4):
            imm_mask[i] = set_bits_in_range(
                cls.field_imm.base[i], cls.field_imm.base[i] + cls.field_imm.size[i] - 1
            )

        rd = (unassigned_bits & rd_mask) >> cls.field_rd.base

        imm = (
            ((unassigned_bits & imm_mask[3]) >> 11)  # >> 11
            | (unassigned_bits & imm_mask[2])  # >> 0
            | ((unassigned_bits & imm_mask[1]) >> 9)  # >> 9
            | ((unassigned_bits & imm_mask[0]) >> 20)  # >> 20
        )

        return cls(rd=rd, imm=imm)

    def __init__(self, rd: int = None, imm: int = None):
        super().__init__(rd, imm)

    @property
    def no_type_mapping(self):
        int_value = self.value
        unsigned_values = int_value >> self.field_opcode.size
        return {"opcode": self.field_opcode.value, "unassigned": unsigned_values}

    @property
    def value(self):
        return self.encode()

    def __str__(self):
        return "{} x{}, .{:+}".format(self.mnemonic, self.rd, self.imm)

    def __repr__(self):
        return "{}({}, {}) ".format(self.__class__.__name__, self.rd, self.imm)


class JAL(InstructionJAL, JTypeInstruction):
    def __init__(self, rd: int = None, imm: int = None):
        InstructionJAL.__init__(self, map_reg_name(rd), map_imm_arg(imm))
