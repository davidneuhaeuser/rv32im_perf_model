from collections import namedtuple

from riscvmodel.insn import RV32I
from riscvmodel.isa import get_insns

from perf_model.backend.isa.b_type import *
from perf_model.backend.isa.i_type import *
from perf_model.backend.isa.j_type import *
from perf_model.backend.isa.r_type import *
from perf_model.backend.isa.s_type import *
from perf_model.backend.isa.u_type import *

Inst = namedtuple("Inst", ["IClass", "Fields"])

field_dict = {
    "R": ["rd", "rs1", "rs2"],
    "J": ["rd", "imm"],
    "I": ["rd", "rs1", "imm"],
    "IS": ["rd", "rs1", "shamt"],
    "S": ["rs1", "rs2", "imm"],
    "U": ["rd", "imm"],
    "B": ["rs1", "rs2", "imm"],
}

UNTYPED = """ "jal": Inst(IClass=JAL, Fields=["rd", "imm"]),  # added manually
    "lui": Inst(IClass=LUI, Fields=["rd", "imm"]),  # added manually
    "auipc": Inst(IClass=AUIPC, Fields=["rd", "imm"]),  # added manually."""


def create_dict():
    out = "from perf_model.backend.utils.mem_dict_gen import Inst \n"
    out += "from perf_model.backend.isa.i_type import *\n"
    out += "from perf_model.backend.isa.j_type import *\n"
    out += "from perf_model.backend.isa.r_type import *\n"
    out += "from perf_model.backend.isa.s_type import *\n"
    out += "from perf_model.backend.isa.u_type import *\n"
    out += "from perf_model.backend.isa.b_type import *\n"
    out += "mem_dict: dict[str, Inst] = {"
    template = "'{}': Inst(IClass={}, Fields={})"
    mnems = {""}
    for icls in get_insns(variant=RV32I):
        mnem: str = icls.mnemonic
        if mnem in mnems:
            continue
        mnems.add(mnem)
        try:
            eval(mnem.upper())

            instr_format = icls.isa_format_id
            out += (
                template.format(mnem, mnem.upper(), str(field_dict[instr_format]))
                + ",\n"
            )

        except:
            continue
    # Manually add the field layouts for the instructions the riscv model dosnt privide a isa format id
    out += UNTYPED
    out = out[:-1] + "\n}"
    with open("perf_model.backend/utils/memnonic_dictonary.py", "w") as f:
        f.write(out)


# Create a new memnonic dictionary by running this script directly
if __name__ == "__main__":
    create_dict()
