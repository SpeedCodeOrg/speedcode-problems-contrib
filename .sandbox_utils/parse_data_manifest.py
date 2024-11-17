from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_DataManifest, PRM_DataManifestItem
from pydantic.json import pydantic_encoder
from pathlib import Path
import os

from sandbox_utils.context import ROOT_DIR, SOURCE_CODE_ROOT
#from sandbox_utils.parse_correctness import parse_correctness

def parse_data_manifest():
    manifest_raw = open(SOURCE_CODE_ROOT/'data/data_manifest.json').read()
    return PRM_DataManifest.parse_raw(manifest_raw)

    #assembly = open(ROOT_DIR/'solution_analysis.assembly').read()
    #vector_report = open(ROOT_DIR/'solution_analysis.report_vector').read()

    #result = PRM_CompilerAnalysis(vectorization_report = vector_report, assembly = assembly)

if __name__ == '__main__':
    print(json.dumps(parse_data_manifest(), default=pydantic_encoder), end="")
