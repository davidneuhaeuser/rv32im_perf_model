# RV32IM Performance Model for DNNs

This tool can be used to compile C programs and estimate their performance when running on a RISC-V (32IM) CPU with a 5-stage pipeline, hazard detection and forwarding, along with multplication support.

This performance Model is currently optimized for performance analysis regarding DNNs.

If you intend to analyze any other type of program, it is recommended to change the order of the switch statement for `execute()` in `perf_model/perf_model_rv32im.py`. For this, the execution histogramm functionality (`-I`) can be very helpful.

> [!NOTE]
> This tool is designed for use on Linux.


## Setup
It is recommended to use [pypy](https://doc.pypy.org/en/latest/index.html), for better simulation times.

This setup will cover the following steps:

1.  **Download GCC for RISC-V**
2.  **Install pypy**
3.  **Set variables**
4.  **Initialise python project**


### Step 1
Download [GCC for RISC-V](https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases/tag/v14.2.0-3) from the link for you system.


### Step 2
Install *pypy* by downloading a [pre-built](https://pypy.org/download.html) version as explained [here](https://doc.pypy.org/en/latest/install.html#download-a-pre-built-pypy).
It is recommended to rename the extracted folder to something along the lines of `pypy_perf_model`.

### Step 3
Add all necessary variables by replacing the placeholders below with the according paths (these will only persist throughout a single session):
```
alias run="<path/to/pypy> perf_model/run.py"
export xpack="<path/to/xpack/bin/>"
alias mk="cd perf_model/compilation && make && cd ../.."
alias clean="cd perf_model/compilation && make clean && cd ../.."
```

For example:
```
alias run="~/Downloads/pypy_perf_model/bin/python perf_model/run.py"
export xpack="~/Downloads/xpack-riscv-none-elf-gcc-14.2.0-3-linux-x64/xpack-riscv-none-elf-gcc-14.2.0-3/bin"
alias mk="cd perf_model/compilation && make && cd ../.."
alias clean="cd perf_model/compilation && make clean && cd ../.."
```


### Step 4
Initialise the python project (installs package dependencies) depending on the python interpreter you are using.

For *pypy* use the following commands (explained [here](https://doc.pypy.org/en/latest/install.html#installing-more-modules)):

```
 ./pypy-xxx/bin/pypy -m ensurepip

 ./pypy-xxx/bin/pypy -mpip install -U pip wheel # to upgrade to the latest versions

 ./pypy-xxx/bin/pypy -mpip install -e ".[dev]" # install dependencies
```

## Usage
**1. Configure the simulation to your liking via `perf_model/perf_model_config.py`**

**2. Compile the desired c project**

1. Paste your project according to the given structure into `perf_model/compilation`
2. Add the following lines at the top of your `main` or equivalent (replace names accordingly), right below any includes:
```
int main();

__asm("__start: la sp, stack; jal main; ecall");
```
3. Add each executables path to `OUT` and adding a rule for each file by replacing `EXENAME` with the desired name of the executable and `FILE` with the name of the C source file:
```
$(BUILD_DIR)/EXENAME: $(SRC_DIR)/FILE.c $(LIB)
	$(CC) $(CFLAGS) -I$(INC_DIR) $(DEFS) $(SRC_DIR)/FILE.c $(LDFLAGS) -o $@
```
4. Run `mk`.

5. **(Optional)** If you are done, clean up your build by using `clean`.

**3. Run the simulation**

Use `run` with flags (see `-h` for help) and a path to either a file or a folder to execute all the executables contained within that folder.

> [!NOTE]
> Please note that you can execute all commands from the top level of this repository

## Results

| Cached   | DNNs          | DNN related   | Sorting Algorithms |
| -------- | ------------- | ------------- | ------------------ |
| Yes      | <2%           | <6%           | <15%               |
| No       | 0%*           | 0%*           |  0%*               |

> [!WARNING]
> Add 15% to any simulation result to cover worst case scenarios.

> [!NOTE]
> *: As compared to an [Amaranth](https://github.com/amaranth-lang/amaranth) implementation


## More

The `backend` folder contains files from a different project, which are necessary for parsing the generated binaries.

## Licences

Licences for third party dependencies are listed in the respective folder: `backend/LICENCE`.
