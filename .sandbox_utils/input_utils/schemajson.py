# Prints out a human readable description of how raw text should be provided, based on the specified input schema.

from sandbox_utils.context import ROOT_DIR, SOURCE_CODE_ROOT
import jsonschemacodegen.cpp as cpp
from jsonschemacodegen.resolver import SimpleResolver

import importlib.util
import sys

spec = importlib.util.spec_from_file_location('input_schema.schema', SOURCE_CODE_ROOT / 'input_schema/schema.py')
schema = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schema)


Input = schema.Input

open(SOURCE_CODE_ROOT / 'input_schema' / 'schema.json','w+').write(str(Input.schema_json()))
