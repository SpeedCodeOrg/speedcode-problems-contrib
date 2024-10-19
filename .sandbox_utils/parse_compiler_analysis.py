from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_CompilerAnalysis
from pydantic.json import pydantic_encoder
from pathlib import Path
import os

from sandbox_utils.context import ROOT_DIR
#from sandbox_utils.parse_correctness import parse_correctness

def parse_compiler_analysis():
    assembly = open(ROOT_DIR/'solution_analysis.assembly').read()
    vector_report = open(ROOT_DIR/'solution_analysis.report_vector').read()

    result = PRM_CompilerAnalysis(vectorization_report = vector_report, assembly = assembly)
    return result

if __name__ == '__main__':
    print(json.dumps(parse_compiler_analysis(), default=pydantic_encoder), end="")
