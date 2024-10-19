from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_Cilksan, PRM_Cilksan_DistinctRace, PRM_Cilksan_DistinctRace_MemoryAccess
from pydantic.json import pydantic_encoder
from pathlib import Path
import os

from sandbox_utils.context import ROOT_DIR
from sandbox_utils.parse_correctness import parse_correctness

# A helper function that parses the text for a single reported race by Cilksan into schema.
def parse_cilksan_race_item(race_lines):
    mem_access_types = ["Read", "Write", "Free", "Realloc"]


    # First divide into three sections:
    #   (a) Races
    #   (b) Common calling context
    #   (c) Allocation context.

    race_section = []
    calling_section = []
    allocation_section = []

    # get race section
    start = False
    for l in race_lines:
        if l.find('Race detected on location') != -1:
            start = True
            continue
        if l.find('Common calling context') != -1:
            break
        if start:
            race_section.append(l)

    # get calling context section
    start = False
    for l in race_lines:
        if l.find('Common calling context') != -1:
            start = True
            continue
        if l.find('Allocation context') != -1:
            break
        if start:
            calling_section.append(l)

    # get allocation context section
    start = False
    for l in race_lines:
        if l.find('Allocation context') != -1:
            start = True
            continue
        if l.strip() == "":
            break
        if start:
            allocation_section.append(l)


    # Now parse out the two memory accesses in race_section
    current_mem_access = None
    distinct_race_list = []
    mem_access_list = []
    for idx, l in enumerate(race_section):
        for t in mem_access_types:
            if l.find(f"{t} ") != -1:
                if current_mem_access != None:
                    mem_access_list.append(current_mem_access)
                current_mem_access = []

                # NOTE(TFK): We can't simply do the below line because the function name might have spaces in it.
                info = l[l.find(f'{t}'):].split(' ')
                # NOTE(TFK): So instead we're going to deal with the function separately.

                # First one is reliable.
                memory_access_type = info[0]
                # We skip info[1].
                full_path = info[-1]
                function = l[l.find(f'{t}'):].replace(info[0], '').replace(info[1], '').replace(full_path, '')
                function = function.strip()
                file_name = full_path.split(':')[0].split('/')[-1]

                line_num = full_path.split(':')[1]
                col_num = full_path.split(':')[2]

                if file_name.strip() != "solution.cpp":
                    # lets see if we can find a call.
                    for k in range(idx+1, len(race_section)):
                        l = race_section[k]
                        stop = False
                        for t in mem_access_types:
                            if l.find(f'{t} ') != -1:
                                stop = True
                                break 
                        if stop:
                            break 
                        if l.find('Call ') == -1:
                            continue
                        # NOTE(TFK): We can't simply do the below line because the function name might have spaces in it.
                        info2 = l[l.find(f'Call '):].split(' ')
                        # NOTE(TFK): So instead we're going to deal with the function separately.

                        # First one is reliable.
                        memory_access_type2 = info2[0]
                        # We skip info[1].
                        full_path2 = info2[-1]
                        function2 = l[l.find(f'Call '):].replace(info2[0], '').replace(info2[1], '').replace(full_path2, '')
                        function2 = function2.strip()
                        file_name2 = full_path2.split(':')[0].split('/')[-1]

                        line_num2 = full_path2.split(':')[1]
                        col_num2 = full_path2.split(':')[2]
                        if file_name2.strip() == "solution.cpp":
                            memory_access_type = memory_access_type2
                            full_path = full_path2
                            function = function2
                            file_name = file_name2
                            line_num = line_num2
                            col_num = col_num2
                            break
    
                mem_access_list.append(PRM_Cilksan_DistinctRace_MemoryAccess(\
                        access_type=memory_access_type, function=function, full_path=full_path,\
                        file_name=file_name, line_num=int(line_num.strip()), col_num=int(col_num.strip())))
                current_mem_access = None
                #print(result)
                #print()
                #print(f"memory_access_type: {memory_access_type}")
                #print(f"function: {function}")
                #print(f"full_path: {full_path}")
                #print(f"file_name: {file_name}")
                #print(f"line_num: {line_num}")
                #print(f"col_num: {col_num}")
                #print()
    return PRM_Cilksan_DistinctRace(memory_accesses=mem_access_list)

def detailed_parse_cilksan(report):
    race_details_list = []
    race_details = None
    for l in report.splitlines():
        if l.strip() == "":
            if race_details != None:
                race_details_list.append(race_details)
            race_details = None
        if l.find("Race detected on location") != -1:
            race_details = []
        if race_details != None:
            race_details.append(l)
    distinct_race_list = []
    for x in race_details_list:
        distinct_race_list.append(parse_cilksan_race_item(x))
    return distinct_race_list

def parse_cilksan():
    report = open(ROOT_DIR/'cilksan-report.err').read()
    full_report = report.strip()
    distinct_races = None
    for l in report.splitlines():
        l = l.strip()
        if len(l) == 0:
            continue
        if l.startswith('Cilksan detected') and l.endswith('distinct races.'):
            l = l.replace('Cilksan detected', '').replace('distinct races.', '').strip()
            distinct_races = int(l)

    distinct_race_list = None
    if distinct_races != None and distinct_races > 0:
        distinct_race_list = detailed_parse_cilksan(report)
    result = PRM_Cilksan(distinct_races = distinct_races, full_report = full_report, distinct_race_list = distinct_race_list)
    return result

if __name__ == '__main__':
    print(json.dumps(parse_cilksan(), default=pydantic_encoder), end="")
