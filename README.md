# RV32IM Performance Model for DNNs

This tool can be used to compile C programs and estimate their performance when running on a RISC-V (32IM) CPU with a 5-stage pipeline, hazard detection and forwarding, along with multplication support.

This performance Model is currently optimized for performance analysis regarding DNNs.

If you intend to analyze any other type of program, it is recommended to change the order of the switch statement for `execute()` in `perf_model/perf_model_rv32im.py`. For this, the execution histogramm functionality (`-I`) can be very helpful.

> [!NOTE]
> This tool is designed for use on Linux.


## Setup
It is recommended to use [pypy](https://doc.pypy.org/en/latest/index.html), for quicker performance estimation.

This setup will cover the following steps:

1.  **Download GCC for RISC-V**
2.  **Create python environment**
3.  **Initialise python project**
4.  **Configure setup file**
5.	**Setup your C project**

### Step 1
Download [GCC for RISC-V](https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases/tag/v14.2.0-3) from the link for you system and extract it.

### Step 2
Install *pypy* by downloading a [pre-built](https://pypy.org/download.html) version and extracting it as explained [here](https://doc.pypy.org/en/latest/install.html#download-a-pre-built-pypy).
For ease of access, it is recommended to rename the extracted folder to something simple along the lines of `pypy_perf_model`.

### Step 3
Initialise the python project (installs package dependencies) depending on the python interpreter you are using.

For *pypy* use the following commands (explained [here](https://doc.pypy.org/en/latest/install.html#installing-more-modules)):

```
 <path/to/pypy/folder>/pypy_perf_model/bin/pypy -m ensurepip
 <path/to/pypy/folder>/pypy_perf_model/bin/pypy -mpip install -U pip wheel
 <path/to/pypy/folder>/pypy_perf_model/bin/pypy -mpip install -e ".[dev]"
```

If you want to use *venv* execute the following commands from this projects root:
```
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Step 4
Configure the `setup` script file (if you are using *venv* you can simply skip the second step):

1.	Write the path to your xpack download to `xpackpath`
2.	Write the path to your desired python interpreter to `pypath`

### Setp 5
Prepare your C project for compilation:
1.	Copy your project into `perf_model/compilation` according to its given structure.
2.	Add the following lines at the top of your `main` or equivalent (replace names accordingly), right below any includes:
```
int main();

__asm("__start: la sp, stack; jal main; ecall");
```
3.	In the `perf_model/compilation/Makefile` add each executables path to `OUT` and add a rule for each file by replacing `<EXENAME>` with the desired name of the executable and `<FILE>` with the name of the respective C source file:
```
$(BUILD_DIR)/<EXENAME>: $(SRC_DIR)/<FILE.c> $(LIB)
	$(CC) $(CFLAGS) -I$(INC_DIR) $(DEFS) $(SRC_DIR)/<FILE.c> $(LDFLAGS) -o $@
```

## Usage
**1. Configure the performance estimation to your liking via `perf_model/perf_model_config.py`**

**2. Setup**

Please note that this setup has to be executed for each new terminal session.

Run the following command (including `.` and a space):
```
. setup
```

**3. Run**

Use `run`along with flags (see `-h` for help) and a path to either a file or a folder to execute the file or all the executables contained within that folder.
Alternativeley you can make a compact run of all files you just compiled by using `runall` (no flags supported).
```
run --asm perf_model/compilation/example  # will run 'example` and generate an asm file of the program
runall  # will run all executables from the last compilation
```

In case of errors during setup, it might help to start a fresh terminal session.

## Performance Error

The table below shows the measured performance estimation error as compared to an HDL implementation of an RV32IM processor with the same specifications (5-stage pipeline, hazard detection, forwarding, 2-way/2-set/2-words-per-block/write-back/write-allocate cache) for programs of respective categories. Considering the results, it is therefore recommended to **assume an error of ±15%.**

| Cached   | DNNs          | DNN related   | Sorting Algorithms |
| -------- | ------------- | ------------- | ------------------ |
| Yes      | <2%           | <6%           | <12%               |
| No       | 0%            | 0%            |  0%                |


## Development

....

## More

The `backend` folder contains files from a different project, which are necessary for parsing the generated binaries.

## Licences

Licences for third party dependencies are listed in the respective folder: `backend/LICENCE`.
