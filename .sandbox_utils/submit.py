from defusedxml.ElementTree import parse
import json
from models.problem_response_models import PRM_Cilksan
from pydantic.json import pydantic_encoder
from pathlib import Path
import os
import json
import tarfile

import requests

url = "http://speedcode.org/get_presigned_url"

# File name for staging area for tarball extraction.
staging_area = ".tmp_staging_area"

# Job runner
MAX_MESSAGE_RETRY = 10
MESSAGE_RETRY_DELAY = 1

from sandbox_utils.context import ROOT_DIR
from sandbox_utils.parse_correctness import parse_correctness

if __name__ == '__main__':
        problem_info = json.loads(open('SPEC.json').read())
        required_keys = ['title', 'short_description']
        for x in required_keys:
            if x not in problem_info:
                print("Error missing required key " + str(x) + " in SPEC.json")
                quit()
        problem_info['readme'] = open('README.md').read()
        problem_info['source'] = open('solution.cpp').read()
        print(problem_info)
         


        if (Path('.submissions') / ("testsub.tar")).exists():
            os.remove(Path('.submissions') / ("testsub.tar"))
        Path('.submissions').mkdir(exist_ok=True)
        tarball_out_path =  Path(".submissions") / ("testsub" + ".tar")
        with tarfile.open(tarball_out_path, mode="w") as tarball:
            tarball.add(Path("."), arcname="")

        message = '''
###
### Go to http://localhost:3000/ide/index.html?user_submissions to obtain your API key.
###
        '''
        print (message)
        #url = "http://localhost:3000/get_presigned_url"
        presigned_url = input('Enter API Key\n > ')
        presigned_url = presigned_url.strip()
        keys = {'user_const_id' : presigned_url.split("#")[0], 'api_key' : presigned_url.split("#")[1], 'title': problem_info['title'], 'short_description': problem_info['short_description'], 'readme': problem_info['readme'], 'source' : problem_info['source']}
        print(keys)
        x = requests.post(url, json=keys) 
        response = json.loads(x.text)['response']
        if response == "Error":
            print("Error in response")
            quit()
        print("content is")
        print(response)
        response = eval(response)
        keys = response['fields']
        url = response['url']
        with open(Path('.submissions') / "testsub.tar", 'rb') as f:
            files = {'file' : ('testsub.tar', f)}
            http_response = requests.post(url, data=keys, files=files)
            print(http_response)
