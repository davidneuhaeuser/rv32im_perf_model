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


### Step 1
Download [GCC for RISC-V](https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases/tag/v14.2.0-3) from the link for you system and extract it.
Change the first two lines of `perf_model/compilation/Makefile`, so they point towards the given binaries.

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

If you want to use *pyenv* execute the following commands from this projects root:
```
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage
**1. Configure the performance estimation to your liking via `perf_model/perf_model_config.py`**

**2. Compile the desired c project**

1. Paste your project according to the given structure into `perf_model/compilation`
2. Add the following lines at the top of your `main` or equivalent (replace names accordingly), right below any includes:
```
int main();

__asm("__start: la sp, stack; jal main; ecall");
```
3. Add each executables path to `OUT` and add a rule for each file by replacing `EXENAME` with the desired name of the executable and `FILE` with the name of the C source file:
```
$(BUILD_DIR)/EXENAME: $(SRC_DIR)/FILE.c $(LIB)
	$(CC) $(CFLAGS) -I$(INC_DIR) $(DEFS) $(SRC_DIR)/FILE.c $(LDFLAGS) -o $@
```
4. `cd` to `perf_model/compilation` and run `make`

5. **(Optional)** Use `make clean` when done.

**3. Run the performance estimation**

Run `perf_model/run.py` with your python interpreter, along with flags (see `-h` for help) and a path to either a file or a folder to execute the file or all the executables contained within that folder.
```
<path/to/pypy>/bin/python perf_model/run.py --asm perf_model/compilation/build  # will run all executables in the build folder that result from the compilation and generate an asm file of the program
```


## Performance Error

The table below shows the measured performance estimation error as compared to an HDL implementation of an RV32IM processor with the same specifications (without a cache) for programs of respective categories. Considering the results, it is therefore recommended to **assume an error of ±15%.**

| Cached   | DNNs          | DNN related   | Sorting Algorithms |
| -------- | ------------- | ------------- | ------------------ |
| Yes      | <2%           | <6%           | <12%               |
| No       | 0%            | 0%            |  0%                |


## More

The `backend` folder contains files from a different project, which are necessary for parsing the generated binaries.

## Licences

Licences for third party dependencies are listed in the respective folder: `backend/LICENCE`.
