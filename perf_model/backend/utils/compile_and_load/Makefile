TARGET := program

SRC_DIR := ./src
INCL_DIR := ./lib
BUILD_DIR := ./build

ELF := $(BUILD_DIR)/$(TARGET).elf

ARCH = rv32i
COMP_TARGET = riscv32-unknown-elf
# ------------------
CC := clang
CXX := clang

CFLAGS := --target=$(COMP_TARGET) -march=$(ARCH) -nostdlib -fno-pie -fno-pic -Wno-incompatible-pointer-types-discards-qualifiers -I $(INCL_DIR) -include "utils.c" -ffunction-sections -Wno-incompatible-library-redeclaration

LD := ld.lld
LDSCRIPT := linker_rv32.ld
LDFLAGS := -T $(LDSCRIPT) -o $(ELF) -no-pie --verbose -static --gc-sections

# ------------------

SRC := $(wildcard $(SRC_DIR)/*.c) $(wildcard $(SRC_DIR)/*.cpp)

SRC_C := $(filter $(SRC_DIR)/%.c, $(SRC))
SRC_CPP := $(filter $(SRC_DIR)%.cpp, $(SRC))

ASMS := $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.s, $(SRC_C)) $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.s, $(SRC_CPP))
OBJS := $(patsubst %.s, %.o, $(ASMS))

OBJS_C := $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.o, $(SRC_C))
OBJS_CPP := $(patsubst $(SRC_DIR)%.cpp, $(BUILD_DIR)/%.o, $(SRC_CPP))

ASMS_C := $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.s, $(SRC_C))
ASMS_CPP := $(patsubst $(SRC_DIR)%.cpp, $(BUILD_DIR)%.s, $(SRC_CPP))

# -----------------

.PHONY: all clean debug clean-intermediate asm obj

all: $(BUILD_DIR) $(ELF)

$(ELF): $(OBJS_C) $(OBJS_CPP) $(LDSCRIPT)
	$(LD) $(LDFLAGS) $(OBJS)

$(OBJS_C): $(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJS_CPP): $(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CFLAGS) -c -o $@ $<

$(ASMS_C): $(BUILD_DIR)/%.s: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -S -o $@ $<

$(ASMS_CPP): $(BUILD_DIR)/%.s: $(SRC_DIR)/%.cpp
	$(CXX) $(CFLAGS) -S -o $@ $<

$(LDSCRIPT):
	@echo "please provide a valid linkerscript named $(LDSCRIPT)"

$(BUILD_DIR):
	mkdir $(BUILD_DIR)

obj: $(OBJS_C) $(OBJS_CPP)

asm: $(ASMS_C) $(ASMS_CPP)

clean:
	rm -rf $(BUILD_DIR)

clean-intermediate:
	rm -rf $(ASMS) $(OBJS)

debug:
	@echo "src    : $(SRCS)"
	@echo "src c  : $(SRCS_C)"
	@echo "src c++: $(SRCS_CPP)"
	@echo "asm    : $(ASMS)"
	@echo "asm c  : $(ASMS_C)"
	@echo "asm c++: $(ASMS_CPP)"
	@echo "obj    : $(OBJS)"
	@echo "obj c  : $(OBJS_C)"
	@echo "obj c++: $(OBJS_CPP)"
