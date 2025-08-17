# single cycle simulation
import math

from perf_model.instructions import (
    rv32i_B_instructions,
    rv32i_I_arlog_instructions,
    rv32i_I_mem_instructions,
    rv32i_S_instructions,
    rv32im_R_instructions,
)
from perf_model.utility import btd_conversion

RD = 1
RS1 = 2
RS2 = 3
DATA = 1
IOFFS = 2
BASE = 3
IMM = 3


class RV32IMCachedProcessor:
    def __init__(
        self,
        program: list[list[str]] = [[""]],
        mem_size: int = 4096,
        mem_init: list[int] = [0],
        read_delay: int = 9,
        write_delay: int = 14,
        mult_delay: int = 4,
        ways: int = 4,
        sets: int = 4,
        blsz: int = 2,
        dmem_offset: int = 0x10000,
        cache_error_correction: float = 1.05,
        cached: bool = True,
    ):
        # TODO order these

        self.cerrc: bool = cache_error_correction
        self.cached: bool = cached

        self.program: int = program
        self.read_delay: int = read_delay
        self.write_delay: int = write_delay
        self.mult_delay: int = mult_delay
        self.ccs: int = 4
        self.jump_delay: int = 3
        self.reads: int = 0
        self.writes: int = 0
        self.stalls: int = 0
        self.exec_history: list[str] = []

        self.ways: int = ways
        self.blsz: int = blsz
        self.sets: int = sets
        self.read_hits: int = 0
        self.write_hits: int = 0
        self.read_stalls: int = 0
        self.write_stalls: int = 0

        self.cache: list[list[int]] = [
            [[-1, ways - i] for i in range(ways)] for j in range(sets)
        ]

        self.dmem_offset: int = dmem_offset // 4
        self.registers: list[int] = [0] * 32
        self.read_data: int = 0
        self.pc: int = 0
        self.instruction: list[str] = [""]
        self.rd1: int = 0
        self.rd2: int = 0
        self.rd_mask: int = 0
        self.sign: int = 0
        self.extension: int = 0
        self.signed: bool = False
        self.wb_data: int = 0
        self.imm: int = 0
        self.read: bool = False
        self.write: bool = False
        self.comp: bool = False
        self.result: int = 0
        self.rd: int = 0
        self.jump: bool = False

        self.mem: list[int] = [0] * (math.ceil(mem_size / 4))

        for i in range(math.ceil(len(mem_init) / 4)):
            byte0: int = mem_init[4 * i]
            byte1: int = 0
            byte2: int = 0
            byte3: int = 0

            if ((4 * i) + 1) in range(len(mem_init)):
                byte1: int = mem_init[4 * i + 1]
            if ((4 * i) + 2) in range(len(mem_init)):
                byte2: int = mem_init[4 * i + 2]
            if ((4 * i) + 3) in range(len(mem_init)):
                byte3: int = mem_init[4 * i + 3]

            self.mem[i] = byte0 | (byte1 << 8) | (byte2 << 16) | (byte3 << 24)

    def return_value(self) -> str:
        if self.registers[10] in range(-10000, 10000):
            return str(btd_conversion(self.registers[10]))
        else:
            return hex(btd_conversion(self.registers[10]))

    def cache_access(self, addr: int, wr_strobe: bool):

        address: int = addr // self.blsz
        hit: bool = False
        set: int = address % self.sets
        oldest: int = 0
        oldest_pos: int = 0

        for way in range(self.ways):

            self.cache[set][way][1] = self.cache[set][way][1] + 1

            if address == self.cache[set][way][0]:
                self.cache[set][way][1] = 0
                hit = True

        if hit:
            if wr_strobe:
                self.write_hits += 1
            else:
                self.read_hits += 1
        else:
            for way in range(self.ways):
                if oldest < self.cache[set][way][1]:
                    oldest = self.cache[set][way][1]
                    oldest_pos = way
                # if self.cache[set][way][1] >= self.ways:
                #     self.cache[set][way][0] = address
                #     self.cache[set][way][1] = 0

            self.cache[set][oldest_pos][0] = address
            self.cache[set][oldest_pos][1] = 0

    def simulate(self, track_exec: bool = False):
        while True:
            if track_exec:
                self.exec_history += [self.instruction[0]]

            if self.instruction[0] == "ecall":
                self.ccs -= 1  # magic correction...
                if self.cached:
                    print(self.ccs)

                    mar: int = (self.reads + self.writes) / self.ccs
                    rhr: int = self.read_hits / self.reads
                    whr: int = self.write_hits / self.writes
                    wrate: int = self.writes / self.ccs
                    rrate: int = self.reads / self.ccs
                    wrtrd: int = self.writes / self.reads
                    print("mar", mar)
                    print("rhr", rhr)
                    print("whr", whr)
                    print("rd rate:", rrate)
                    print("wr rate:", wrate)
                    print("rd/wr :", wrtrd)

                    self.read_stalls -= self.read_hits * (self.read_delay - 1)
                    self.write_stalls -= self.write_hits * (self.write_delay - 1)

                    self.read_stalls += (self.reads - self.read_hits) * (
                        self.write_delay
                    )
                    self.write_stalls += (self.writes - self.write_hits) * (
                        self.write_delay
                    )

                self.read_stalls *= self.cerrc
                self.write_stalls *= self.cerrc
                self.stalls += self.read_stalls + self.write_stalls
                self.ccs += int(self.stalls)
                return
            else:
                self.tick()
                self.ccs += 1

    def print_cache(self):
        entries: str = ""
        header: str = ""

        for way in range(self.ways):
            header += f"way {way}"

        print("\taddress\tlru" * self.ways)
        for set in range(self.sets):
            entries = ""
            for way in range(self.ways):
                entries += f"\t{self.cache[set][way][0]}\t{self.cache[set][way][1]}"
            print(f"set {set}{entries}")

    def print_runtime_info(self) -> None:
        print("mem accs:\t", self.reads + self.writes)
        print("\nreads:\t\t", self.reads)
        print("read hits:\t", self.read_hits)
        print("read misses:\t", self.reads - self.read_hits)
        print("\nwrites:\t\t", self.writes)
        print("write hits:\t", self.write_hits)
        print("write misses:\t", self.writes - self.write_hits)
        print("\nstalls:\t\t", self.stalls)
        print("\ncycles:\t\t", self.ccs)
        # print("\n", self.cache)

    def tick(self) -> None:

        self.read_data = 0
        self.rd1 = 0
        self.rd2 = 0
        self.rd_mask = 0
        self.sign = 0
        self.extension = 0
        self.signed = False
        self.wb_data = 0
        self.imm = 0
        self.read = False
        self.write = False

        # self.cache_busy -= 1

        self.fetch()
        self.decode()
        self.execute()
        self.memory()
        self.write_back()

    def fetch(self):

        if (self.pc // 4) in range(0, len(self.program) + 1):
            if self.jump:
                self.pc = self.j_dest
            self.instruction = self.program[self.pc // 4]
            self.pc += 4
        else:
            self.instruction = ["ecall"]
            print("automatically added missing ecall to program")

    def decode(self):

        rs1: int = 0
        rs2: int = 0
        self.rd = 0
        self.read = False
        self.write = False

        instr = self.instruction[0]

        if instr in rv32im_R_instructions:
            self.rd = int(self.instruction[RD], 0)
            rs1 = int(self.instruction[RS1], 0)
            rs2 = int(self.instruction[RS2], 0)
        elif instr in rv32i_I_arlog_instructions:
            self.rd = int(self.instruction[RD], 0)
            rs1 = int(self.instruction[RS1], 0)
            self.imm = int(self.instruction[IMM], 0)
        elif instr in rv32i_I_mem_instructions:
            self.reads += 1
            self.rd = int(self.instruction[RD], 0)
            self.imm = int(self.instruction[IOFFS], 0)
            rs1 = int(self.instruction[BASE], 0)
        elif instr in rv32i_S_instructions:
            self.writes += 1
            self.imm = int(self.instruction[IOFFS], 0)
            rs1 = int(self.instruction[BASE], 0)
            rs2 = int(self.instruction[DATA], 0)
        elif instr in rv32i_B_instructions:
            rs1 = int(self.instruction[1], 0)
            rs2 = int(self.instruction[2], 0)
            self.imm = int(self.instruction[3], 0)
        elif (instr == "lui") or (instr == "auipc"):
            self.rd = int(self.instruction[RD], 0)
            self.imm = int(self.instruction[2], 0)
        elif instr == "jal":
            self.rd = int(self.instruction[RD], 0)
            self.imm = int(self.instruction[2], 0)
        elif instr == "jalr":
            self.rd = int(self.instruction[RD], 0)
            rs1 = int(self.instruction[RS1], 0)
            self.imm = int(self.instruction[IMM], 0)

        self.rd1 = self.registers[rs1]
        self.rd2 = self.registers[rs2]

        if rs1 == 0:
            self.rd1 = 0

        if rs2 == 0:
            self.rd2 = 0

    def execute(self):
        rs1: int = self.rd1
        rs2: int = self.rd2
        imm: int = self.imm
        res: int = 0
        sign_bit: int = 0x80000000
        mask: int = 0xFFFFFFFF
        msb: int = sign_bit & rs1
        self.jump = False
        self.j_dest = 0

        match self.instruction[0]:
            case "addi":
                res = rs1 + imm
            case "lw":
                res = rs1 + imm
                self.rd_mask = 0xFFFFFFFF
                self.read = True
            case "add":
                res = rs1 + rs2
            case "mul":
                self.stalls += self.mult_delay
                res = rs1 * rs2
                res = res & mask
            case "bne":
                self.stalls += self.jump_delay
                self.jump = rs1 != rs2
                self.j_dest = self.pc - 4 + imm
            case "slli":
                res = rs1 << imm
            case "bgeu":
                self.stalls += self.jump_delay
                self.jump = (rs1 & mask) >= (rs2 & mask)
                self.j_dest = self.pc - 4 + imm
            case "sw":
                res = rs1 + imm
                self.wr_mask = 0xFFFFFFFF
                self.write = True
            case "beq":
                self.stalls += self.jump_delay
                self.jump = rs1 == rs2
                self.j_dest = self.pc - 4 + imm
            case "jalr":
                self.stalls += self.jump_delay
                self.j_dest = rs1 + imm
                res = self.pc
                self.jump = True
            case "blt":
                self.stalls += self.jump_delay
                self.jump = rs1 < rs2
                self.j_dest = self.pc - 4 + imm
            case "jal":
                self.stalls += self.jump_delay
                self.j_dest = self.pc - 4 + imm
                res = self.pc
                self.jump = True
            case "lui":
                res = imm << 12
            case "mulh":
                self.stalls += self.mult_delay
                res = rs1 * rs2
                res = res >> 32
            case "mulhsu":
                self.stalls += self.mult_delay
                res = rs1 * (rs2 & mask)
                res = res >> 32
            case "mulhu":
                self.stalls += self.mult_delay
                res = (rs1 & mask) * (rs2 & mask)
                res = res >> 32
            case "div":
                if rs2 != 0:
                    res = rs1 // rs2
                    if res < 0:
                        res += 1
                else:
                    res = -1
                self.stalls += len(str(res))
            case "divu":
                if rs2 != 0:
                    res = (rs1 & mask) // (rs2 & mask)
                else:
                    res = -1
                self.stalls += len(str(res))
            case "rem":
                if rs2 != 0:
                    res = abs(rs1) % abs(rs2)
                    if rs1 < 0:
                        res = res * -1
                else:
                    res = rs1
                self.stalls += len(str(res))
            case "remu":
                if rs2 != 0:
                    res = (rs1 & mask) % (rs2 & mask)
                else:
                    res = rs1 & mask
                self.stalls += len(str(res))
            case "sub":
                res = rs1 - rs2
            case "xor":
                res = rs1 ^ rs2
            case "or":
                res = rs1 | rs2
            case "and":
                res = rs1 & rs2
            case "sll":
                res = rs1 << rs2
                res = res & mask
            case "srl":
                res = rs1 >> rs2
            case "sra":
                res = rs1
                for _ in range(rs2):
                    res = msb | (res >> 1)
            case "slt":
                res = int(rs1 < rs2)
                res = res & mask
            case "sltu":
                rs1 = rs1 & mask
                rs2 = rs2 & mask
                res = int(rs1 < rs2)
            case "xori":
                res = rs1 ^ imm
            case "ori":
                res = rs1 | imm
            case "andi":
                res = rs1 & imm
            case "srli":
                res = rs1 >> imm
            case "srai":
                res = rs1
                for _ in range(imm):
                    res = msb | (res >> 1)
            case "slti":
                res = int(rs1 < imm)
            case "sltiu":
                rs1 = rs1 & mask
                rs2 = imm & mask
                res = int(rs1 < rs2)
            case "lb":
                res = rs1 + imm
                self.rd_mask = 0xFF
                self.sign = 0x80
                self.signed = True
                self.extension = 0xFFFFFF00
            case "lh":
                res = rs1 + imm
                self.rd_mask = 0xFFFF
                self.sign = 0x8000
                self.signed = True
                self.extension = 0xFFFF0000
            case "lbu":
                res = rs1 + imm
                self.rd_mask = 0xFF
                self.read = True
            case "lhu":
                res = rs1 + imm
                self.rd_mask = 0xFFFF
                self.read = True
            case "sb":
                res = rs1 + imm
                self.wr_mask = 0xFF
                self.write = True
            case "sh":
                res = rs1 + imm
                self.wr_mask = 0xFFFF
                self.write = True
            case "auipc":
                res = self.pc - 4 + (imm << 12)
            case "bge":
                self.stalls += self.jump_delay
                self.jump = rs1 >= rs2
                self.j_dest = self.pc - 4 + imm
            case "bltu":
                self.stalls += self.jump_delay
                self.jump = (rs1 & mask) < (rs2 & mask)
                self.j_dest = self.pc - 4 + imm

        self.result = res

    def memory(self):

        offset: int = (self.result % 4) * 8
        address: int = (self.result // 4) - self.dmem_offset
        self.read_data: int = 0
        mem_data: int = 0
        if address in range(len(self.mem)):
            mem_data = self.mem[address] & 0xFFFFFFFF

        self.rd_mask = (self.rd_mask << offset) & 0xFFFFFFFF
        self.sign = (self.sign << offset) & 0xFFFFFFFF

        if self.read:
            if self.cached:
                self.cache_access(address, False)
            self.read_stalls += self.read_delay
            self.read_data = (mem_data & self.rd_mask) >> offset
        elif self.signed:
            if self.cached:
                self.cache_access(address, False)
            self.read_stalls += self.read_delay
            self.read_data = (mem_data & self.rd_mask) >> offset
            if self.read_data & self.sign:
                self.read_data = self.read_data | self.extension
        elif self.write:
            if self.cached:
                self.cache_access(address, True)
            self.write_stalls += self.write_delay
            self.mem[address] = (
                (mem_data & (~(self.wr_mask << offset)))
                | ((self.rd2 & self.wr_mask) << offset)
            ) & 0xFFFFFFFF

        self.read_data = self.read_data

    def write_back(self):
        instr: str = self.instruction[0]

        if self.rd != 0:

            if (
                (instr in rv32im_R_instructions)
                or (instr in rv32i_I_arlog_instructions)
                or (instr == "lui")
                or (instr == "auipc")
                or (instr == "jal")
                or (instr == "jalr")
            ):
                self.registers[self.rd] = btd_conversion(self.result)

            elif instr in rv32i_I_mem_instructions:
                self.registers[self.rd] = btd_conversion(self.read_data)
