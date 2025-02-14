from pathlib import Path
import os

from sandbox_utils.context import ROOT_DIR, SOURCE_CODE_ROOT
from sandbox_utils.parse_correctness import parse_correctness

if __name__ == '__main__':
    lines = open(SOURCE_CODE_ROOT / 'solution.cpp').readlines()
    found_omp = False
    found_opencilk = False

    cflags_list = []
    cflags_solution_list = []
    ldflags_list = []

    for l in lines:
        if l.strip().replace(' ', '').startswith("#include<omp.h>"):
            found_omp = True
            cflags_list.append('-fopenmp')
            ldflags_list.append('-fopenmp')
        if l.strip().replace(' ', '').startswith("#include<cilk/cilk.h>"):
            found_opencilk = True
            cflags_list.append('-fopencilk')
            ldflags_list.append('-fopencilk')
        if l.strip().replace(' ', '').startswith("#include\"taskflow/taskflow.hpp\"") or\
                l.strip().replace(' ', '').startswith("#include<taskflow/taskflow.hpp>"):
            cflags_solution_list.append('-std=c++17')
            cflags_solution_list.append(f"-I{SOURCE_CODE_ROOT}")

    if not found_omp and not found_opencilk:
        # if openmp is not present then compile with -fopencilk.
        cflags_list.append('-fopencilk')
        ldflags_list.append('-fopencilk')

    open(ROOT_DIR / 'extra_cflags_solution','w+').write(" ".join(cflags_solution_list)) 
    open(ROOT_DIR / 'extra_cflags','w+').write(" ".join(cflags_list)) 
    open(ROOT_DIR / 'extra_ldflags','w+').write(" ".join(ldflags_list)) 

