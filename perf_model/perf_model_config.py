#################################################
#                 DELAY CONFIG                  #
#################################################
# Select duration of memory read accesses
READ_DELAY = 9  # default: 9

# Select duration of memory write accesses
WRITE_DELAY = 14  # default: 14

# Select the duration of multplications
# (duration of divisions depends on operands)
MULT_DELAY = 4  # default: 4

# Change this value only for experimental
# purposes, since it is tied to the processors
# architecture
JUMP_DELAY = 3


#################################################
#                 CACHE CONFIG                  #
#################################################
# Configuration of a set associative cache
# using least recently used (CACHED = False
# will ignore any effects of the cache)

CACHED = True  # default: True
WAYS = 4  # default: 4
SETS = 4  # default: 4

# Select the number of words per cache block
BLOCK_SIZE = 2  # default: 2

# Select an error correction factor for the
# total number of clock cycles
CACHE_ERROR_CORRECTION = 1.0  # default 1.0


#################################################
#     CHANGE VALUES BELOW ACCORDING TO          #
#        `linker_rv32.ld` IF CHANGED            #
#################################################

# Select the same MEM_SIZE as used for
# compilation (see: `linker_rv32.ld`)
MEM_SIZE = 4 * (2**20)  # default: 4*(2**20)

# Select the size of the instruction memory used
# for compilation (see: `linker_rv32.ld`)
DMEM_OFFSET = 0x100000  # default: 0x100000
