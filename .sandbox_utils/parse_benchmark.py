from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_Benchmark, PRM_BenchmarkResult, PRM_CorrectnessTests
from pydantic.json import pydantic_encoder
from pathlib import Path
import os


from sandbox_utils.context import ROOT_DIR
from sandbox_utils.parse_correctness import parse_correctness

def parse_benchmark():
    obj = json.load(open(ROOT_DIR / 'benchmark_results.json'))
    correctness_results = parse_correctness(redirect_prefix = "benchmark")

    benchmark_result_list = []
    submission_result = None
    reference_result = None
  
    for result in obj['results']:
        item = PRM_BenchmarkResult(function=result['name'],\
                benchmark_name=result['title'],\
                runtime=result['median(elapsed)'],\
                instructions=result['median(instructions)'],\
                cpucycles=result['median(cpucycles)'],\
                contextswitches=result['median(contextswitches)'],\
                pagefaults=result['median(pagefaults)'],\
                branchinstructions=result['median(branchinstructions)'],\
                branchmisses=result['median(branchmisses)'])

        if item.function.find("benchmark_submission") != -1:
            item.function = "Submission"
        if item.function.find("benchmark_reference") != -1:
            item.function = "Reference"
        if item.function != "Submission" and item.function != "Reference":
            benchmark_result_list.append(item)
        else:
            if item.function == "Submission" or item.function.strip() == "benchmark_submission":
                submission_result = item
            if item.function == "Reference" or item.function.strip() == "benchmark_reference":
                reference_result = item
 
    pkg = PRM_Benchmark(stdout=None,\
            stderr=None,\
            tests=correctness_results.dict(),\
            challenges=benchmark_result_list,\
            reference=reference_result,\
            submission=submission_result) 
    return pkg

if __name__ == '__main__':
    print(json.dumps(parse_benchmark(), default=pydantic_encoder), end="")
