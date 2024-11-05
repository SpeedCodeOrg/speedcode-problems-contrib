from typing import List
from pydantic import BaseModel
import json
import sys
import random

class Input(BaseModel):
    row: List[int]
    col: List[int]
    weight: List[float]

def main(N):
    num_vertices = 100000;
    num_edges = num_vertices*10;
    edges = []
    for i in range(num_edges):
        src = random.randint(0,num_vertices)
        dst = random.randint(0,num_vertices)
        weight = random.uniform(0,10.0);
        if src == dst:
            continue
        edges.append((src, dst, weight))
        edges.append((dst, src, weight))
    edges.sort()
    edges.append((num_vertices+1, num_vertices+1)) # add sentinel
    filtered_edges = []
    for i in range(0, len(edges)-1):
        if edges[i][0:2] != edges[i+1][0:2]:
            filtered_edges.append(edges[i])
    row = []
    col = []
    weights = []
    for i in range(len(filtered_edges)):
       row.append(filtered_edges[i][0]) 
       col.append(filtered_edges[i][1]) 
       weights.append(filtered_edges[i][2]) 
    return Input(row=row, col=col, weight=weights).json()

    
        

    #print(example_input.json())

if __name__ == "__main__":
    N = int(sys.argv[1])
    print(main(N))
