import subprocess
import os
from pathlib import Path
import argparse
import sys

output_dir = Path(sys.argv[1])
if not output_dir.is_dir():
    print("Error output directory is not a directory")
    assert(False)

PROBLEM_NAME = os.getcwd().split('/')[-1].strip()

def run_command(cmd, asyn = False):
  proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  if not asyn:
    out,err=proc.communicate()
    return out.decode('utf-8'),err.decode('utf-8')
  else:
    return ""

out,err=run_command('ls solutions/*.cpp')

print (out)
analyze_files = []
for x in out.splitlines():
    analyze_files.append(x.strip())

print(analyze_files)

out,err=run_command('ls cachegrind*')
cg_files = []
for x in out.splitlines():
    cg_files.append(x.strip())
print(cg_files)

cg_annotations = []


CMD = 'cg_annotate --show=Dr,Dw,D1mr,D1mw --threshold=0.1'
for x in cg_files:
    outfile = 'cg'+str(len(cg_annotations))+".out"
    run_command(f'cg_annotate --show=Dr,Dw,D1mr,D1mw --threshold=0.1 --context=500 {x} > {outfile}')
    cg_annotations.append(outfile)
print(cg_annotations)

analyze_pairs = []
for x in cg_annotations:
    text = open(x, 'r').read()
    for y in analyze_files:
        if text.find(y) != -1:
            analyze_pairs.append((x,y))
            print(f"Found {y} in {x}")

print(analyze_pairs)

def get_annotated_line(perf_stats, solution_line):
    loads = perf_stats[0]+perf_stats[1]
    misses = perf_stats[2]+perf_stats[3]
    ratio = "{:.2f}".format(misses/loads)
    comment = f"Average L1 misses per load is {ratio}"
    if loads > 100000:
        ann_line = f"{solution_line} // {comment}"
    else:
        ann_line = f"{solution_line}"
    return ann_line

def analyze_pair(cga_file, solution):
    lines = open(cga_file,'r').read().splitlines()
    filtered_lines = []
    found_start = True
    start_line = 0
    for i in range(0,len(lines)):
        x = lines[i]
        if x.startswith(f'-- Auto-annotated source: ') and x.find(solution) != -1:
            found_start = True
            start_line = i+4
            break
    for i in range(start_line, len(lines)):
        x = lines[i]
        if x.find('--------------------------------------------------------------------------------') != -1:
            end_line = i-3
            break

    cg_lines = lines[start_line:end_line]
    solution_lines = open(solution).read().splitlines()
    assert(len(solution_lines) == len(cg_lines))
    annotated_lines = []
    for i in range(0, len(cg_lines)):
        filtered = cg_lines[i].replace(solution_lines[i],'')
        if len(filtered.replace('.','').replace(' ', '').replace('0','')) == 0:
            annotated_lines.append(solution_lines[i])
            continue
        items = filtered.split(')')
        new_items = []
        it = 0
        while filtered.find(')') != -1:
            it += 1
            filtered = filtered.replace(filtered[filtered.find('('):filtered.find(')')+1], ' ')
            if it > 50:
                print("Error removing percentages from cg output. infinite loop. quitting.")
                assert(False)
                quit()
        perf_stats = []
        for x in filtered.split(' '):
            if len(x) > 0:
                perf_stats.append(int(x.replace(',','')))
        annotated_lines.append(get_annotated_line(perf_stats, solution_lines[i]))
    return "\n".join(annotated_lines)
            
            
training_data = output_dir
for x in analyze_pairs:
    annotated = analyze_pair(x[0], x[1])
    sol_name = x[1].split('/')[-1].replace('.cpp','')
    ann_name = sol_name + "_ann"
    open(training_data / (PROBLEM_NAME + "_" + ann_name+".cpp"),'w+').write(annotated)
    open(training_data / (PROBLEM_NAME + "_" + sol_name+".cpp"), 'w+').write(open(x[1]).read())