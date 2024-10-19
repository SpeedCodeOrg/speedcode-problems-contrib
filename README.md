# Installation instructions

## Note

At present, these instructions are intended to be self-contained for folks who
want to only run code in speedcode-problems.

## 1. Install Conda

If you already have conda installed you can skip this step.

Follow instructions on the [Conda user
guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).
For example, to install Miniconda on an x86 Linux machine:

```bash
curl -Ls https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VER}-Linux-${conda_arch}.sh -o /tmp/Miniconda.sh &&\
bash Miniconda3-py38_4.10.3-Linux-x86_64.sh
```

## 2. Setup conda environment (from YAML)

The conda environment for this project is summarized in the `environment.yml` file. You can install the entire conda environment with a single command:

```bash
conda env create -n speedcode-problems --file environment.yml
```

You can activate the conda environment using the command:

```bash
conda activate speedcode-problems
```

The remainder of the instructions will assume that you are running commands with
the correct conda environment activated.

## 3. Install Quicktype and pip packages

After activating your conda environment, install quicktype using npm. Your conda environment should already have node installed, so the following npm command should work:

```bash
npm install -g quicktype
```

Also install the pip package `json-schema-codegen`

```bash
pip install json-schema-codegen prettytable
```


## 4. Install OpenCilk

Installation instructions for OpenCilk are located at https://www.opencilk.org/doc/users-guide/install/

The recommended installation, for Ubuntu 20.04 and 22.04 and Apple-Darwin is to use the shell archive.

For example, to install on Ubuntu 20.04 you should run 

```bash
wget  https://github.com/OpenCilk/opencilk-project/releases/download/opencilk/v2.0/OpenCilk-2.0.0-x86_64-Linux-Ubuntu-20.04.sh
sh OpenCilk-2.0.0-x86_64-Linux-Ubuntu-20.04.sh
```

OpenCilk will then be installed in the directory OpenCilk-2.0.0-x86_64-Linux-Ubuntu-20.04

## 5. Setup environment variable for OPENCILK_COMPILER_DIR

You need to set the environment variable `OPENCILK_COMPILER_DIR` to point to the directory where you installed OpenCilk. In order to ensure that this environment variable is correctly set whenever you are working within the `speedcode-problems` conda environment, you can run the following command:

**You must modify the path below to point to where you installed OpenCilk** 
```bash
 conda env config vars set OPENCILK_COMPILER_DIR=/path/to/OpenCilk-2.0.0-x86_64-Linux-Ubuntu-20.04
 
 # Reactivate your conda environment so that the change takes effect.
 conda activate speedcode-problems
```


## 6. Verify installation succeeded.

Enter an example problem, e.g., `cd example_problems/beta-sort-strings` and from that directory run `make internal-test`

```bash
cd example_problems/beta-sort-strings
make internal-test
```

If, at the end of the test, "Success" is printed as the last line (or second-to-last line) --- then you
have completed the installation successfully.


The command `make internal-test` verifies that the problem correctly implements all
targets, including the cilkscale and cilksan targets. For problems that do not
implement these targets, due to them being focused on sequential optimizations,
you can use the alternative command: `make internal-test-serial`, which will perform
all checks except those related to cilkscale and cilksan. 

```bash
cd example_problems/beta-sort-strings
make internal-test-serial 
```

# Problem Contribution Instructions

To design a Speedcode problem there are four key files that must be written:

```
input_schema/schema.py
solution.cpp
solution.hpp
input.hpp
```

Let us walk through the process of how one would create a simple Speedcode problem for sorting strings.

## Step 1. Define the input schema (input_schema/schema.py)

Your speedcode problem for sorting strings should accept a list of strings as input. You can specify this by modifying the `Input` Pydantic class in `input_schema/schema.py`. You should also provide some code for generating inputs that conform to your specified schema.

```python
from typing import List
from pydantic import BaseModel
import json
import sys

class Input(BaseModel):
    strings: List[str]

def main(N):
    example_input = Input(strings=[f"string_{i}" for i in range(N)])
    print(example_input.json())

if __name__ == "__main__":
    N = int(sys.argv[1])
    main(N)
```

### Generating test inputs

From your problem's directory, you can run `python input_schema.schema 1024 > inputs/small1024.json` to create an input of 1024 strings that will be used for testing correctness and benchmarking solutions to your Speedcode problem.

### Generating C/C++ interface for reading inputs

You must compile the schema you specified by running 

```bash
make schema
```

This command should generate a file in your problem directory called `inputschema.cpp` which will contain a definition of a structure "Inputschema" that contains the fields you specified in `input_schema/schema.py`. 

```cpp
    struct Inputschema {
        std::vector<std::string> strings;
    };
```

## Step 2. Specify the solution function signature (solution.hpp)

Next, you should modify `solution.hpp` to specify the header file that should be included by all solutions to your problem. This should specify the function signature of solutions to your problem.

```cpp
#pragma once
#include <vector>
#include <string>

std::vector<std::string> solution_entry(std::vector<std::string> input);
```

## Step 3. Implement a reference solution (solution.cpp, solutions/reference.cpp)

You should implement a reference solution in `solution.cpp`. You must additionally copy this reference solution into the solutions directory `solutions/reference.cpp`. This reference solution will serve as the "starter code" for users submitting solutions to your problem.

Contents of `solution.cpp` and `solutions/reference.cpp` (both files may be identical)

```cpp
#include "solution.hpp"
#include <algorithm>

std::vector<std::string> solution_entry(std::vector<std::string> input) {
    std::sort(input.begin(), input.end());
    return input;
}
```

## Step 4. Specify how inputs should be executed. (input.hpp)

Let us look at the `input.hpp` file for the sort-strings problem.

```cpp
#include "solution.hpp"
#include <optional>
#include <string>
#include <nanobench.h>
#include <sstream>
#include <memory>
#include <vector>

// Reference solution for correctness test.
__attribute__((weak))
std::vector<std::string> reference_solution(std::vector<std::string> input) {
    std::sort(input.begin(), input.end());
    return input;
}

class ProblemInput {
    std::vector<std::string> strings;
    ankerl::nanobench::Rng rng;
public:
    ProblemInput(std::string inp_name, quicktype::Inputschema& input) {
        strings = input.strings;
    }

    auto run(decltype(solution_entry) F = solution_entry) {
        std::vector<std::string>& _input = this->strings;
        auto Out = F(input);
        ankerl::nanobench::doNotOptimizeAway(Out);
        return input;
    }

    std::optional<std::string> check() {
        auto result = run();
        auto result_ref = run(reference_solution);
        if (result.size() != result_ref.size()) return "Error: result of incorrect size";

        for (size_t i = 0; i < result.size(); i++) {
            if (result[i] != result_ref[i]) {
                return "Incorrect value at index " + std::to_string(i) + 
                       ". Expected: " + result_ref[i] + 
                       ", Actual: " + result[i];
            }
        }
        return std::nullopt;
    }
};

```

There are three main functions that must be implemented in the `ProblemInput` class. The constructor, the run() function, and the check() function. 

### ProblemInput constructor

The ProblemInput constructor must prepare the inputs to be executed by the solution code. In this particular case, the constructor is fairly trivial as the STL vector's assignment operator can be used to copy the contents into a local variable. However, sometimes there will be a need to change the data representation of the inputs prior to calling the solution function. For example, `quicktype` represents all integers and floating point numbers with 64-bit precision. Thus, if one's solution code accepts an array of `float` or `int32_t` typed elements the `Probleminput` constructor would need to coerce the input data into the proper types. It is preferable to perform this preprocessing in the constructor so that it will not impact the runtime measured when benchmarking submitted solutions.


### ProblemInput run() function

The `run()` function should execute the solution function `F` that is passed in as an argument. The `run()` function should not have side-effects. If it is possible for a solution to modify the input arguments, then it is necessary to copy them in the `run()` function. In this case, however, the function signature of the sorting-strings problem specifies that the input arguments are passed by value, not reference, so one does not need to worry about side-effects.

### ProblemInput check() function

The `check()` function should execute the submitted solution and then verify its correctness. Often, you can do this by implementing a reference code and then verifying that the outputs match. The default argument of the `run()` function is the submitted solution code (`solutionn.cpp`), but if one passes an alternate function with the same signature (e.g., the `reference_solution`) function defined at the top of `input.hpp`, then it will be used instead.

## Step 5. (optional) Create more solutions

You can add more solutions by adding files to the `solutions/` directory. For example, you might create solutions `solutions/f0.cpp`, `solutions/f1.cpp`, `solutions/f2.cpp` where each successive solution achieves better performance.


## Step 6. Write a problem description (README.md)

You should write a problem description for your Speedcode problem in the file `README.md`.

## Step 7. Specify the meta-data for your problem (SPEC.json)

You must specify a problem title, short description, and the number of challenge codes that exist for your solution.

## Step 8. (optional) Allow users to generate custom inputs for testing.

You can allow users to generate custom inputs in the web interface by generating a file `demo.json`. This file should be small so that it can be easily viewed and modified by users on the website. The Speedcode user-interface will automatically divide each field of the input schema into a separate input for the user to fill-in. 

To generate demo.json simply run:

```
python -m input_schema.schema 8 > demo.json
```

To create a default custom input consisting of 8 strings.