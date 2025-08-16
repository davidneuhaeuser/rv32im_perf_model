import unittest

from perf_model.backend.isa.b_type import *
from perf_model.backend.isa.i_type import *
from perf_model.backend.isa.j_type import *
from perf_model.backend.isa.r_type import *
from perf_model.backend.isa.RV32M_instructions import *
from perf_model.backend.isa.s_type import *
from perf_model.backend.isa.u_type import *
from perf_model.perf_model_rv32im import *
from perf_model.utility import *


def instr_sim(instr, a, b) -> int:
    instr.rd = 10
    instr.rs1 = 1
    instr.rs2 = 2
    instructions = [instr, ECALL(0, 0, 0)]

    dut = RV32IMCachedProcessor(get_program(instructions))
    print(dut.program)
    dut.registers[1] = a
    dut.registers[2] = b
    dut.simulate()

    return dut.registers[10]


def instr_sim_i(instr, a, b) -> int:
    instr.rd = 10
    instr.rs1 = 1
    instr.imm.set(b)
    instructions = [instr, ECALL(0, 0, 0)]

    dut = RV32IMCachedProcessor(get_program(instructions))
    dut.registers[1] = a
    dut.simulate()

    return dut.registers[10]


def instr_sim_shift(instr, a, b) -> int:
    instr.rd = 10
    instr.rs1 = 1
    instr.shamt.set(b)
    instructions = [instr, ECALL(0, 0, 0)]

    dut = RV32IMCachedProcessor(get_program(instructions))
    dut.registers[1] = a
    dut.simulate()

    return dut.registers[10]


def instr_sim_ld(instr, data, offset):
    instr.rd = 10
    instr.rs1 = 1
    instr.imm.set(offset)

    instructions = [instr, ECALL(0, 0, 0)]

    dut = RV32IMCachedProcessor(program=get_program(instructions), dmem_offset=0)
    dut.registers[1] = 40
    dut.mem[40 // 4] = data
    dut.simulate()

    return dut.registers[10]


def instr_sim_str(instr, data, offset):
    instr.rs1 = 1
    instr.rs2 = 2
    instr.imm.set(offset)

    instructions = [instr, ECALL(0, 0, 0)]

    dut = RV32IMCachedProcessor(program=get_program(instructions), dmem_offset=0)
    # print(dut.program)
    dut.registers[1] = 40
    dut.registers[2] = data
    dut.mem[40 // 4] = 0x33333333
    dut.simulate()

    return dut.mem[40 // 4]


class TestInstructions(unittest.TestCase):
    def test_r_types(self):
        self.assertEqual(instr_sim(ADD(), 42, -13), 29)
        self.assertEqual(instr_sim(SUB(), 42, -13), 55)
        self.assertEqual(instr_sim(XOR(), 0b1100, 0b0110), 0b1010)
        self.assertEqual(instr_sim(OR(), 0b1010, 0b0100), 0b1110)
        self.assertEqual(instr_sim(AND(), 0b0110, 0b0101), 0b0100)
        self.assertEqual(instr_sim(SLL(), 0b0001, 2), 0b0100)
        self.assertEqual(instr_sim(SRL(), 0b1000, 2), 0b0010)
        self.assertEqual(instr_sim(SRA(), 0b1000, 2), 0b0010)
        self.assertEqual(instr_sim(SRA(), -8, 2), -2)
        self.assertEqual(instr_sim(SLT(), 3, 4), 1)
        self.assertEqual(instr_sim(SLT(), 4, 3), 0)
        self.assertEqual(instr_sim(SLTU(), -4, 3), 0)
        self.assertEqual(instr_sim(SLTU(), 3, 4), 1)

    def test_i_types_arlog(self):
        self.assertEqual(instr_sim_i(ADDI(0, 0, 0), 42, -13), 29)
        self.assertEqual(instr_sim_i(XORI(0, 0, 0), 0b1100, 0b0110), 0b1010)
        self.assertEqual(instr_sim_i(ORI(0, 0, 0), 0b1010, 0b0100), 0b1110)
        self.assertEqual(instr_sim_i(ANDI(0, 0, 0), 0b0110, 0b0101), 0b0100)
        self.assertEqual(instr_sim_i(SLTI(0, 0, 0), 3, 4), 1)
        self.assertEqual(instr_sim_i(SLTI(0, 0, 0), 4, 3), 0)
        self.assertEqual(instr_sim_i(SLTIU(0, 0, 0), -4, 3), 0)

    def test_i_types_shift(self):
        self.assertEqual(instr_sim_shift(SLLI(0, 0, 0), 0b0001, 2), 0b0100)
        self.assertEqual(instr_sim_shift(SRLI(0, 0, 0), 0b1000, 2), 0b0010)
        self.assertEqual(instr_sim_shift(SRAI(0, 0, 0), 0b1000, 2), 0b0010)
        self.assertEqual(instr_sim_shift(SRAI(0, 0, 0), -8, 2), -2)

    def test_loads(self):
        self.assertEqual(instr_sim_ld(LW(0, 0, 0), 0x12345678, 0), 0x12345678)
        self.assertEqual(instr_sim_ld(LBU(0, 0, 0), 0x12345678, 0), 0x78)
        self.assertEqual(instr_sim_ld(LHU(0, 0, 0), 0x12345678, 0), 0x5678)
        self.assertEqual(instr_sim_ld(LB(0, 0, 0), 0x12345678, 0), 0x78)
        self.assertEqual(instr_sim_ld(LB(0, 0, 0), 0x12345678, 1), 0x56)
        self.assertEqual(instr_sim_ld(LB(0, 0, 0), 0x12345678, 2), 0x34)
        self.assertEqual(instr_sim_ld(LB(0, 0, 0), 0x12345678, 3), 0x12)
        self.assertEqual(instr_sim_ld(LB(0, 0, 0), 0x80, 0), -0x80)
        self.assertEqual(instr_sim_ld(LH(0, 0, 0), 0x12345678, 0), 0x5678)
        self.assertEqual(instr_sim_ld(LH(0, 0, 0), 0x12345678, 1), 0x3456)
        self.assertEqual(instr_sim_ld(LH(0, 0, 0), 0x12345678, 2), 0x1234)
        self.assertEqual(instr_sim_ld(LH(0, 0, 0), 0x12345678, 3), 0x12)
        self.assertEqual(instr_sim_ld(LH(0, 0, 0), 0x8000, 0), -0x8000)

    def test_store(self):
        self.assertEqual(instr_sim_str(SW(0, 0, 0), 0x12345678, 0), 0x12345678)
        self.assertEqual(instr_sim_str(SH(0, 0, 0), 0x12345678, 0), 0x33335678)
        self.assertEqual(instr_sim_str(SH(0, 0, 0), 0x12345678, 3), 0x78333333)
        self.assertEqual(instr_sim_str(SB(0, 0, 0), 0x12345678, 0), 0x33333378)
        self.assertEqual(instr_sim_str(SB(0, 0, 0), 0x12345678, 1), 0x33337833)

    def test_jal(self):

        instructions = [
            ADD(0, 0, 0),
            JAL(1, 8),
            ADDI(1, 1, 3),
            ADDI(1, 1, 1),
            ECALL(0, 0, 0),
        ]

        dut = RV32IMCachedProcessor(get_program(instructions))
        dut.simulate()
        # print(dut.program)

        self.assertEqual(dut.registers[1], 9)

    def test_jalr(self):

        instructions = [
            ADDI(1, 0, 42),
            JALR(1, 1, -30),
            ADDI(1, 1, 3),
            ADDI(1, 1, 1),
            ECALL(0, 0, 0),
        ]

        dut = RV32IMCachedProcessor(get_program(instructions))
        dut.simulate()
        # print(dut.program)

        self.assertEqual(dut.registers[1], 9)

    def test_branch(self):

        instructions = [
            ADDI(1, 0, 42),
            ADDI(2, 0, -13),
            BLT(2, 1, 8),
            ADDI(1, 1, 3),
            BLT(1, 2, 8),
            ADDI(1, 1, 7),
            ECALL(0, 0, 0),
        ]

        dut = RV32IMCachedProcessor(get_program(instructions))
        dut.simulate()
        print(dut.program)

        self.assertEqual(dut.registers[1], 49)

    def test_lui_auipc(self):

        instructions = [LUI(1, 23), AUIPC(2, 23), ECALL(0, 0, 0)]

        dut = RV32IMCachedProcessor(get_program(instructions))
        dut.simulate()
        # print(dut.program)

        self.assertEqual(dut.registers[1], 23 << 12)
        self.assertEqual(dut.registers[2], (23 << 12) + 4)

    def test_sign_consitency(self):

        instructions = [
            ADDI(1, 0, 42),
            ADDI(2, 0, -13),
            ADDI(3, 0, 0b1100),
            SLLI(3, 3, 12),
            SW(0, 1, 4),
            SW(0, 2, 8),
            SW(0, 3, 12),
            LW(4, 0, 4),
            LW(5, 0, 8),
            LH(6, 0, 8),
            LB(7, 0, 8),
            LH(8, 0, 12),
            SRLI(3, 3, 8),
            SW(0, 3, 12),
            LB(9, 0, 12),
            ECALL(0, 0, 0),
        ]

        dut = RV32IMCachedProcessor(program=get_program(instructions), dmem_offset=0)
        dut.simulate()
        print(dut.program)

        self.assertEqual(dut.registers[4], 42)
        self.assertEqual(dut.registers[5], -13)
        self.assertEqual(dut.registers[6], -13)
        self.assertEqual(dut.registers[7], -13)
        self.assertEqual(dut.registers[8], -16384)
        self.assertEqual(dut.registers[9], -64)

    def test_mul_instruction(self):
        self.assertEqual(instr_sim(MUL(), 42, -13), -546)
        self.assertEqual(instr_sim(MUL(), -13, -13), 169)
        self.assertEqual(instr_sim(MULH(), 1 << 31, 2), 1)
        self.assertEqual(instr_sim(MULHU(), -1, -1), -2)
        self.assertEqual(instr_sim(MULHSU(), -1, -1), -1)
        self.assertEqual(instr_sim(DIV(), -13, -13), 1)
        self.assertEqual(instr_sim(DIV(), -13, 9), -1)
        self.assertEqual(instr_sim(DIV(), 13, -9), -1)
        self.assertEqual(instr_sim(DIV(), 13, 9), 1)
        self.assertEqual(instr_sim(DIV(), 13, 0), -1)
        self.assertEqual(instr_sim(DIVU(), -1, 1 << 30), 3)
        self.assertEqual(instr_sim(DIVU(), 42, 0), -1)
        self.assertEqual(instr_sim(REM(), 13, 9), 4)
        self.assertEqual(instr_sim(REM(), 13, -9), 4)
        self.assertEqual(instr_sim(REM(), -13, 9), -4)
        self.assertEqual(instr_sim(REM(), -13, -9), -4)
        self.assertEqual(instr_sim(REM(), 42, 0), 42)
        self.assertEqual(instr_sim(REMU(), -1, 2), 1)
        self.assertEqual(instr_sim(REMU(), -1, 4), 3)
        self.assertEqual(instr_sim(REMU(), -1, -1), 0)
        self.assertEqual(instr_sim(REMU(), -42, 0), -42)

    def test_cache_q(self):

        instructions = [
            SW(0, 0, 0),
            SW(0, 0, 32),
            SW(0, 0, 64),
            SW(0, 0, 96),
            LW(0, 0, 128),
            ECALL(0, 0, 0),
        ]

        dut = RV32IMCachedProcessor(
            program=get_program(instructions),
            dmem_offset=0,
            sets=4,
            ways=4,
            blsz=2,
        )

        dut.simulate()
        dut.print_runtime_info()
        self.assertEqual(0, 1)

    def test_cache(self):

        for sets in range(1, 9):
            for ways in range(1, 9):
                for blszs in range(1, 9):

                    instructions = [
                        ADDI(2, 0, sets * ways * blszs),  # ctr
                        SW(3, 1, 0),  # store(idx)
                        ADDI(2, 2, -1),  # ctr -= 1
                        ADDI(3, 3, 4),  # idx += 4
                        BNE(2, 0, -12),  # loop
                        ECALL(0, 0, 0),
                    ]

                    dut = RV32IMCachedProcessor(
                        program=get_program(instructions),
                        dmem_offset=0,
                        sets=sets,
                        ways=ways,
                        blsz=blszs,
                    )
                    print(dut.cache)
                    dut.simulate()

                    for set in range(dut.sets):
                        for way in range(dut.ways):
                            self.assertEqual(
                                dut.cache[set][way][0], way * dut.sets + set
                            )
