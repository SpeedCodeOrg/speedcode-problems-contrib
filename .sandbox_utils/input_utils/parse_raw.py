from sandbox_utils.context import ROOT_DIR, SOURCE_CODE_ROOT
import importlib.util
import sys
from pathlib import Path
import json
spec = importlib.util.spec_from_file_location('input_schema.schema', SOURCE_CODE_ROOT / 'input_schema/schema.py')
schema = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schema)


Input = schema.Input

import json
from pydantic.json import pydantic_encoder
import argparse

schema = Input.schema()
parser = argparse.ArgumentParser(prog='Raw input parser')
parser.add_argument('input_filename')
parser.add_argument('output_filename')
args = parser.parse_args()
info = open(args.input_filename).read().strip()
data_dict = json.loads(info)
output_path = Path(args.output_filename).parent
output_path.mkdir(exist_ok=True)
open(args.output_filename, 'w+').write(json.dumps(Input.parse_obj(data_dict), default=pydantic_encoder))
