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

def process_schema(schema, separator = '\n'):
    print(schema)
    elements = []
    if 'properties' in schema:
        for x in schema['properties'].keys():
            if schema['properties'][x]['type'] in ['integer', 'number', 'string']:
                elements.append(schema['properties'][x]['title'] + " : " + schema['properties'][x]['type'])
            if schema['properties'][x]['type'] in ['array']:
                elements.append(schema['properties'][x]['title'] + " : " + process_schema(schema['properties'][x], separator = ','))
    else:
        #if schema['type'] in ['array']:
        #    if separator == ',':
        #        separator = ','
        #    elements.append(process_schema(schema['items'], separator = ','))
        #elif schema['type'] in ['integer', 'number', 'string']:
        #    elements.append(schema['type'])
        if schema['items']['type'] in ['integer', 'number', 'string']:
            elements.append(schema['items']['type'])
        if schema['items']['type'] in ['array']:
            if separator == ',':
                separator = ','
            elements.append(process_schema(schema['items'], separator = ','))
        assert len(elements) == 1
        return f"List[{elements[0]}; separator='{separator}']"
    return separator.join(elements)

# First line must specify input type.
def compile_format_from_schema(schema):
      #print(schema['properties'])
      print(schema)
      if 'definitions' in schema:
          for x in schema['definitions']:
              print(x)
              print(process_schema(schema['definitions'][x]))
              print()
      else:
          print(schema)
          print(process_schema(schema))
          print()



compile_format_from_schema(Input.schema())

quit()
