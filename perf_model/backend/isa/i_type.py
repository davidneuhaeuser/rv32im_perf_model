from riscvmodel.insn import (
    InstructionADDI,
    InstructionANDI,
    InstructionEBREAK,
    InstructionECALL,
    InstructionJALR,
    InstructionLB,
    InstructionLBU,
    InstructionLH,
    InstructionLHU,
    InstructionLW,
    InstructionORI,
    InstructionSLLI,
    InstructionSLTI,
    InstructionSLTIU,
    InstructionSRAI,
    InstructionSRLI,
    InstructionXORI,
)
from riscvmodel.isa import InstructionILType, InstructionISType, InstructionIType

from perf_model.backend.utils.reg_names_util import map_imm_arg, map_reg_name
from perf_model.backend.utils.utils import set_bits_in_range


class ITypeInstruction(InstructionIType):
    @classmethod
    def from_no_type_mapping(cls, no_type_mapping):
        unassigned_bits = no_type_mapping["unassigned"]
        unassigned_bits = unassigned_bits << cls.field_opcode.size

        # fmt: off
        rd_mask = set_bits_in_range(cls.field_rd.base, cls.field_rd.base + cls.field_rd.size - 1)
        rs1_mask = set_bits_in_range(cls.field_rs1.base, cls.field_rs1.base + cls.field_rs1.size - 1)
        imm_mask = set_bits_in_range(cls.field_imm.base, cls.field_imm.base + cls.field_imm.size - 1)
        # fmt: on

        rd = (unassigned_bits & rd_mask) >> cls.field_rd.base
        rs1 = (unassigned_bits & rs1_mask) >> cls.field_rs1.base
        imm = (unassigned_bits & imm_mask) >> cls.field_imm.base

        return cls(rd=rd, rs1=rs1, imm=imm)

    @classmethod
    def from_i_type_mapping(cls, i_type_mapping):
        return cls(
            rd=i_type_mapping["rd"],
            rs1=i_type_mapping["rs1"],
            imm=i_type_mapping["imm"],
        )

    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        super().__init__(rd, rs1, imm)

    @property
    def no_type_mapping(self):
        int_value = self.value
        unsigned_values = int_value >> self.field_opcode.size
        return {"opcode": self.field_opcode.value, "unassigned": unsigned_values}

    @property
    def i_type_mapping(self):
        mapping_dict = {
            "opcode": self.field_opcode.value,
            "rd": self.rd,
            "funct3": self.field_funct3.value,
            "rs1": self.rs1,
            "imm": self.imm,
        }

        return mapping_dict

    @property
    def value(self):
        return self.encode()

    def __str__(self) -> str:
        return "{} x{}, x{}, {}".format(self.mnemonic, self.rd, self.rs1, self.imm)

    def __repr__(self) -> str:
        return "{}({}, {}, {}) ".format(
            self.__class__.__name__, self.rd, self.rs1, self.imm
        )


class ILTypeInstruction(InstructionILType, ITypeInstruction):
    # for load instructions
    pass


class ISTypeInstruction(InstructionISType):
    # for shift instructions
    @classmethod
    def from_no_type_mapping(cls, no_type_mapping):
        unassigned_bits = no_type_mapping["unassigned"]
        unassigned_bits = unassigned_bits << cls.field_opcode.size

        # fmt: off
        rd_mask = set_bits_in_range(cls.field_rd.base, cls.field_rd.base + cls.field_rd.size - 1)
        rs1_mask = set_bits_in_range(cls.field_rs1.base, cls.field_rs1.base + cls.field_rs1.size - 1)
        shamt_mask = set_bits_in_range(cls.field_shamt.base, cls.field_shamt.base + cls.field_shamt.size - 1)
        # fmt: on

        rd = (unassigned_bits & rd_mask) >> cls.field_rd.base
        rs1 = (unassigned_bits & rs1_mask) >> cls.field_rs1.base
        imm = (unassigned_bits & shamt_mask) >> cls.field_shamt.base

        return cls(rd=rd, rs1=rs1, imm=imm)

    @classmethod
    def from_i_type_mapping(cls, i_type_mapping):
        return cls(
            rd=i_type_mapping["rd"],
            rs1=i_type_mapping["rs1"],
            shamt=i_type_mapping["shamt"],
        )

    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        super().__init__(rd, rs1, imm)

    @property
    def no_type_mapping(self):
        int_value = self.value
        unsigned_values = int_value >> self.field_opcode.size
        return {"opcode": self.field_opcode.value, "unassigned": unsigned_values}

    @property
    def i_type_mapping(self):
        mapping_dict = {
            "opcode": self.field_opcode.value,
            "rd": self.rd,
            "funct3": self.field_funct3.value,
            "rs1": self.rs1,
            "shamt": self.shamt,
        }

        return mapping_dict

    @property
    def value(self):
        return self.encode()

    def __str__(self):
        return "{} x{}, x{}, 0x{:02x}".format(
            self.mnemonic, self.rd, self.rs1, self.shamt
        )

    def __repr__(self):
        return "{}({}, {}, {}) ".format(
            self.__class__.__name__, self.rd, self.rs1, self.shamt
        )


class ADDI(InstructionADDI, ITypeInstruction):
    def __init__(self, rd=None, rs1=None, imm=None):
        InstructionADDI.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class XORI(InstructionXORI, ITypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionXORI.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class ORI(InstructionORI, ITypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionORI.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class ANDI(InstructionANDI, ITypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionANDI.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class SLLI(InstructionSLLI, ISTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionSLLI.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class SRLI(InstructionSRLI, ISTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionSRLI.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class SRAI(InstructionSRAI, ISTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionSRAI.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class SLTI(InstructionSLTI, ITypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionSLTI.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class SLTIU(InstructionSLTIU, ITypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionSLTIU.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class LB(InstructionLB, ILTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionLB.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class LH(InstructionLH, ILTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionLH.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class LW(InstructionLW, ILTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionLW.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class LBU(InstructionLBU, ILTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionLBU.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class LHU(InstructionLHU, ILTypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionLHU.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class JALR(InstructionJALR, ITypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionJALR.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


# Unused: ECALL and EBREAK
class ECALL(InstructionECALL, ITypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionECALL.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )


class EBREAK(InstructionEBREAK, ITypeInstruction):
    def __init__(self, rd: int = None, rs1: int = None, imm: int = None):
        InstructionEBREAK.__init__(
            self, map_reg_name(rd), map_reg_name(rs1), map_imm_arg(imm)
        )
