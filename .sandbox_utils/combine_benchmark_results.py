from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_Benchmark, PRM_BenchmarkResult, PRM_CorrectnessTests
from pydantic.json import pydantic_encoder
from pathlib import Path
import os
import sys
from prettytable import PrettyTable
from sandbox_utils.context import ROOT_DIR

def combine_benchmarks(files):
    combined_results = []
    x = PrettyTable()
    x.field_names = ["Code", "Time per operation (ns)", "Operations / sec "]
    x.float_format = '.2'
    for f in files:
        fname = "benchmark_"+f+".json"
        obj = json.load(open(ROOT_DIR / fname))
        for result in obj['results']:
          combined_results.append(result)

   
    combined_results = sorted(combined_results, key=lambda x: x['name']) 
    for result in combined_results:
        x.add_row([result['name'], float(result['median(elapsed)'])*1e+9, 1.0 / float(result['median(elapsed)'])])
    if len(files) > 1:
        print(x)

    data = {'results' : combined_results}
    json_object = json.dumps(data, indent=4)
    open(ROOT_DIR / "benchmark_results.json", 'w+').write(json_object)

if __name__ == '__main__':
    combine_benchmarks(sys.argv[1:])
