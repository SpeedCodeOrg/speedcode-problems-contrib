from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_Tiers, PRM_CorrectnessTests, PRM_Error
from pydantic.json import pydantic_encoder
from pathlib import Path
import os
import sys

from sandbox_utils.context import ROOT_DIR
from sandbox_utils.parse_correctness import parse_correctness


def parse_error():
    name = sys.argv[1].strip()
    stdout = None
    stderr = None
    details = ""
    try:
        stdout = open(ROOT_DIR / (name+".stdout")).read()
    except:
        stdout = "Failed to find stdout"
    try:
        stderr = open(ROOT_DIR / (name+".stderr")).read()
    except:
        stderr = "Failed to find stderr"

    result = PRM_Error(error=True, stdout=stdout, stderr=stderr, details=details)
    return result


if __name__ == '__main__':
    print(json.dumps(parse_error(), default=pydantic_encoder), end="")
