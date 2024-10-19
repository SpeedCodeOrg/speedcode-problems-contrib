from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_CilkscaleBenchmarkSeries, PRM_CilkscaleBenchmark
from pydantic.json import pydantic_encoder
from pathlib import Path
import os
import base64
import math

from sandbox_utils.context import ROOT_DIR
from sandbox_utils.parse_correctness import parse_correctness

def parse_cilkscale_benchmark():
    data = json.loads(open(ROOT_DIR / 'cilkscale-data.json').read())

    series = []
    for x in data:
        title = x[0]
        obj = x[1]
        remove_idx = set()
        for y in obj.keys():
            #print(obj[y])
            for idx,z in enumerate(obj[y]):
                if math.isnan(z):
                    remove_idx.add(idx)
        new_obj = obj.copy()

        for y in obj.keys():
            orig = obj[y]
            new_obj[y] = []
            for idx,z in enumerate(orig):
                if idx not in remove_idx:
                    new_obj[y].append(z)
        obj = new_obj

        obj['title'] = title
        series.append(obj)
    result = PRM_CilkscaleBenchmark.parse_obj({'data':series})

    result = PRM_CilkscaleBenchmark.parse_raw(json.dumps(result, default=pydantic_encoder))
    return result

if __name__ == '__main__':
    print(json.dumps(parse_cilkscale_benchmark(), default=pydantic_encoder), end="")
