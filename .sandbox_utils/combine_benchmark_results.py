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

    input_targets_str = os.getenv("DYNAMIC_INPUT_TARGETS")
    if input_targets_str != None:
        #print("Dealing with input targets string")
        input_targets = [x.replace('.json','').strip() for x in input_targets_str.split(',')]
        failed = False
        #print(str(files))
        for f in files:
            if Path(ROOT_DIR / f"benchmark_{f}.json").exists():
                #print(f"Skipping {f} because benchmark_{f}.json exists")
                continue
            temp_results = []
            for target in input_targets:
                fname = f"benchmark_{f}_{target}.json"
                if not Path(ROOT_DIR / fname).exists():
                    failed = True
                    break
                obj = json.load(open(ROOT_DIR / fname))
                for result in obj['results']:
                    temp_results.append(result)

            new_data = dict()
            new_data['results'] = temp_results
            open(ROOT_DIR / f'benchmark_{f}.json','w+').write(json.dumps(new_data))

            if not failed:
                #print("Did not fail")
                new_data = dict()
                new_data['results'] = temp_results
                open(ROOT_DIR / f'benchmark_{f}.json','w+').write(json.dumps(new_data))

    combined_results = []
    x = PrettyTable()
    
    custom_score_name = None
    for f in files:
        fname = "benchmark_"+f+".json"
        obj = json.load(open(ROOT_DIR / fname))
        for result in obj['results']:
          if "custom_score_name" in result and result["custom_score_name"] != None:
              custom_score_name = result["custom_score_name"]
          combined_results.append(result)
    
    if custom_score_name != None:
        x.field_names = ["Code", "Time per operation (ns)", "Operations / sec ", custom_score_name]
    else:
        x.field_names = ["Code", "Time per operation (ns)", "Operations / sec "]

    x.float_format = '.2'
    #print(custom_score_name)
    #if custom_score_name != None:
    #    x.field_names.append(custom_score_name)

   
    combined_results = sorted(combined_results, key=lambda x: x['name']) 
    for result in combined_results:
        row_data = [result['name'], float(result['median(elapsed)'])*1e+9, 1.0 / float(result['median(elapsed)'])]
        if custom_score_name != None:
            row_data.append(result["custom_score"])
        x.add_row(row_data)
        #x.add_row([result['name'], float(result['median(elapsed)'])*1e+9, 1.0 / float(result['median(elapsed)'])])
    if len(files) > 1:
        print(x)

    data = {'results' : combined_results}
    json_object = json.dumps(data, indent=4)
    open(ROOT_DIR / "benchmark_results.json", 'w+').write(json_object)

if __name__ == '__main__':
    combine_benchmarks(sys.argv[1:])
