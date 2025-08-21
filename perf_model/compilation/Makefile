###########################################
##    REPLACE WITH PATH TO XPACK HERE    ##
###########################################

CC=$(XPACK)/bin/riscv-none-elf-gcc
AR=$(XPACK)/bin/riscv-none-elf-ar

###########################################
###########################################

BUILD_DIR=build
SRC_DIR=src
INC_DIR=include

# DO NOT CHANGE THESE UNLESS YOU KNOW WHAT YOU ARE DOING
# OPTIMIZATION SHOULD BE O2 IF MAIN ONLY EXECUTES VOID FUNCTIONS
CFLAGS=-O2 -march=rv32im -mabi=ilp32 --static -nostdlib -I include -fno-inline
LDFLAGS=-T linker_rv32.ld -lgcc -L$(BUILD_DIR)


SRCS=$(wildcard $(SRC_DIR)/*.c)
INCS=$(wildcard $(INC_DIR)/*.h)
OBJS=$(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SRCS))

####################################################################
##            ADD YOUR DESIRED EXECTUABLE NAMES HERE              ##
####################################################################

OUT=$(BUILD_DIR)/sort300 $(BUILD_DIR)/sort200 $(BUILD_DIR)/sort100

####################################################################
####################################################################

LIB=$(BUILD_DIR)/lib.a

all: $(LIB) $(OUT)

.PHONY: clean

$(BUILD_DIR):
	mkdir -p build

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c $(INCS) $(BUILD_DIR)
	$(CC) $(CFLAGS) -I$(INC_DIR) $(DEFS) -c $< -o $@

$(LIB): $(OBJS)
	$(AR) rcs $(LIB) $(OBJS)


################################################################################
##             REPLACE (/ADD) FILES BELOW WITH YOUR OWN FILES                 ##
################################################################################

$(BUILD_DIR)/sort300: $(SRC_DIR)/sort300.c $(LIB)
	$(CC) $(CFLAGS) -I$(INC_DIR) $(DEFS) $(SRC_DIR)/sort300.c $(LDFLAGS) -o $@

$(BUILD_DIR)/sort200: $(SRC_DIR)/sort200.c $(LIB)
	$(CC) $(CFLAGS) -I$(INC_DIR) $(DEFS) $(SRC_DIR)/sort200.c $(LDFLAGS) -o $@

$(BUILD_DIR)/sort100: $(SRC_DIR)/sort100.c $(LIB)
	$(CC) $(CFLAGS) -I$(INC_DIR) $(DEFS) $(SRC_DIR)/sort100.c $(LDFLAGS) -o $@

################################################################################
################################################################################

clean:
	rm -rf build
