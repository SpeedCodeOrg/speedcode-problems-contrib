from .schema import Input
import numpy as np
import json
from pydantic.json import pydantic_encoder
import argparse

parser = argparse.ArgumentParser(prog='Generate a random input')
parser.add_argument('--seed', type=int, default=42)
parser.add_argument('--N', type=int, required=True)
parser.add_argument('--output_path', type=str, required=True)
args = parser.parse_args()

if not args.output_path.endswith('.json'):
    print("Error, the output path must end with the .json extension")
    quit()




elements = list(np.random.randint(0, 100, args.N))

pInput = Input(elements=elements)
open(args.output_path,'w+').write(json.dumps(pInput, default=pydantic_encoder))

