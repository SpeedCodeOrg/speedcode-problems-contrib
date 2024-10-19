from typing import List
from pydantic import BaseModel
import json
import sys

class Input(BaseModel):
    strings: List[str]

def main(N):
    example_input = Input(strings=[f"string_{i}" for i in range(N)])
    print(example_input.json())

if __name__ == "__main__":
    N = int(sys.argv[1])
    main(N)
