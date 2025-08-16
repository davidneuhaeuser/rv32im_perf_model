from amaranth import unsigned
from amaranth.lib import data

from perf_model.backend.isa.constants import (
    FUNCT3_WIDTH,
    FUNCT7_WIDTH,
    INSTRUCTION_WIDTH,
    OPCODE_WIDTH,
    RD_WIDTH,
    RS1_WIDTH,
    RS2_WIDTH,
)

"""RV32I Instruction Format
            7                5           5           3           5         7
    +------------------+-----------+-----------+-----------+----------+---------+
    | 31            25 | 24     20 | 19     15 | 14     12 | 11     7 | 6     0 |
    +------------------+-----------+-----------+-----------+----------+---------+
    |      funct7      |    rs2    |    rs1    |  funct3   |    rd    | opcode  |
    +------------------+-----------+-----------+-----------+----------+---------+
    |                            unassigned                           | opcode  |
    +---------------------------------------------------------------------------+
"""

"""unassigned_layout
| 31            25 | 24     20 | 19     15 | 14     12 | 11     7 |
+------------------+-----------+-----------+-----------+----------+
|      funct7      |    rs2    |    rs1    |  funct3   |    rd    |
+------------------+-----------+-----------+-----------+----------+

note:
    the fields names here do not **have** to match what is inside of them.
    e.g. The funct7-field can also hold part of an immediate-value,
    or even funct7 + rs2 combined. The names were just chosen to make the
    usage of this layout intuitive.
"""
unassigned_layout = data.StructLayout(
    {
        "rd": RD_WIDTH,
        "funct3": FUNCT3_WIDTH,
        "rs1": RS1_WIDTH,
        "rs2": RS2_WIDTH,
        "funct7": FUNCT7_WIDTH,
    }
)

"""decode_layout
| 31                                                            7 | 6     0 |
+------------------+-----------+-----------+-----------+----------+---------+
|                            unassigned_layout                    | opcode  |
+---------------------------------------------------------------------------+
"""
decode_layout = data.StructLayout(
    {
        "opcode": OPCODE_WIDTH,
        "unassigned": unassigned_layout,
    }
)

"""no_type_mapping
| 31                                                            7 | 6     0 |
+------------------+-----------+-----------+-----------+----------+---------+
|                            unassigned                           | opcode  |
+---------------------------------------------------------------------------+
"""
no_type_mapping = data.StructLayout(
    {
        "opcode": unsigned(OPCODE_WIDTH),
        "unassigned": unsigned(INSTRUCTION_WIDTH - OPCODE_WIDTH),
    }
)
