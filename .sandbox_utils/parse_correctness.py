from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_CorrectnessTests, PRM_CorrectnessTestCase
from pydantic.json import pydantic_encoder
from pathlib import Path
import os

from sandbox_utils.context import ROOT_DIR

def parse_correctness(redirect_prefix : str = "correctness"):
    obj = parse(ROOT_DIR / 'result.xml')
    
    test_case_list = []
    for x in obj.getroot().iter('TestCase'):
        test_case = dict()
        test_case['name'] = x.attrib['name']
    
        for y in x.iter('OverallResult'):
            test_case['success'] = y.attrib['success']
    
        EXPRESSIONS = []
        INFO = []
        for y in x.iter('Expression'):
            orig = None
            expanded = None
            for z in y.iter("Original"):
                orig = z.text
            for z in y.iter("Expanded"):
                expanded = z.text
            EXPRESSIONS.append(orig.strip() + "(" + expanded.strip() + ")")
        for z in x.iter('Info'):
            INFO.append(z.text.strip())
        test_case['info'] = INFO
        test_case['expressions'] = EXPRESSIONS
        # Below conversion from dict and to dict is redundant.
        #   It is done to aid debugging by making validation fail early on blameworthy testcase.
        test_case_list.append(PRM_CorrectnessTestCase.parse_obj(test_case).dict())
    
    correctness_tests = dict()
    correctness_tests['test_cases'] = test_case_list
    
    for x in obj.getroot().iter('OverallResults'):
        correctness_tests['checks_passed'] = x.attrib['successes']
        correctness_tests['checks_failed'] = x.attrib['failures']
    
    for x in obj.getroot().iter('OverallResultsCases'):
        correctness_tests['cases_passed'] = x.attrib['successes']
        correctness_tests['cases_failed'] = x.attrib['failures']
    
    # Stdout and stderr will be obtained from a file from previous runs.
    correctness_tests['stdout'] = None
    correctness_tests['stderr'] = None
    if Path(ROOT_DIR/'correctness.stdout').exists():
        correctness_tests['stdout'] = open(ROOT_DIR/f'{redirect_prefix}.stdout').read()
        correctness_tests['stderr'] = open(ROOT_DIR/f'{redirect_prefix}.stderr').read()
    
    test_case_output = PRM_CorrectnessTests.parse_obj(correctness_tests)
    return test_case_output

if __name__ ==  '__main__':
    print(json.dumps(parse_correctness(), default=pydantic_encoder), end="")
