from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_Tiers, PRM_CorrectnessTests
from pydantic.json import pydantic_encoder
from pathlib import Path
import os


from sandbox_utils.context import ROOT_DIR
from sandbox_utils.parse_correctness import parse_correctness


def parse_tiers():
    try:
        obj = json.load(open(ROOT_DIR / 'tiers_result.json'))
        max_tier = obj['max_tier']
    except:
        max_tier = 0

    correctness_results = parse_correctness(redirect_prefix = "tiers")
    result = PRM_Tiers(stdout=None, stderr=None, tests=correctness_results.dict(), tier=float(max_tier))
    return result


if __name__ == '__main__':
    print(json.dumps(parse_tiers(), default=pydantic_encoder), end="")
