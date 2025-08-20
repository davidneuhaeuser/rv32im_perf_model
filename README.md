# RV32IM Performance Model for DNNs

This tool can be used to compile C programs and estimate their performance when running on a RISC-V (32IM) CPU with a 5-stage pipeline, hazard detection and forwarding, along with multplication support.

This performance Model is currently optimized for performance analysis regarding DNNs.

If you indent to analyze any other type of program, it is recommended to change the order of the switch statement for `execute()` in `perf_model/perf_model_rv32im.py`. For this, the execution histogramm functionality (`-I`) can be very helpful.

> [!NOTE]
> This tool is designed for use on Linux.


## Setup
It is recommended to use [pypy](https://doc.pypy.org/en/latest/install.html), for better simulation times. The link guides you through all necessary steps to download pypy and install necessary modules.

This setup will cover the following steps:

1.  **Download [GCC for RISC-V](https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases/tag/v14.2.0-3)**
2.  **Install pypy**
3.  **Set variables**
4.  **Initialise python project**


### Step 1
Download GCC for RISC-V from the link for you system.


### Step 2
Install pypy by downloading a pre-compiled version as explained [here](https://doc.pypy.org/en/latest/install.html).


### Step 3
Add all necessary variables (these will only persist thoughout one session):
```
alias run="<path/to/pypy> perf_model/run.py"
export xpack="<path/to/xpack/bin/>"
```

For example:
```
alias run="~/Downloads/pypy3.11/bin/python perf_model/run.py"
export xpack="~/Downloads/xpack-riscv-none-elf-gcc-14.2.0-3-linux-x64/xpack-riscv-none-elf-gcc-14.2.0-3/bin"
```


### Step 4
Initialise the python project (installs package dependencies).

## Usage
**Configure the simulation to your liking via `perf_model/perf_model_config.py`**

**Compile the desired c project**

1. by pasting your project according to the given structure in `perf_model/compilation`
2. running `make`

**Run the simulation**
1. Use `run` with flags (see `-h` for help) and a path to either a file or a folder to execute all the executables contained within that folder.

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
