import argparse
from typing import List, Union, Optional
from pydantic import BaseModel
import json
import sys
import random
import numpy as np

class COOFormat(BaseModel):
    coo_format : bool = True
    row: List[int]
    col: List[int]
    weight: List[float]

class DataFileFormat(BaseModel):
    data_file_format : bool = True
    filename: str
    file_format: str

class RandomGeneratedGraph(BaseModel):
    random_generated_graph : bool = True
    num_vertices : int
    num_edges_per_vertex : int

class MetaInfo(BaseModel):
    save_to_binary : bool
    save_filename : str
    short_description : str
    tags : List[str]

class Input(BaseModel):
    graph : Union[COOFormat, RandomGeneratedGraph, DataFileFormat]
    sources : Optional[List[int]]
    meta_info : Optional[MetaInfo] 

def coo_format_gen(_num_vertices, _num_edges_per_vertex, meta_info = None):
    #return Input(graph=DataFileFormat(filename="tmptest.bin", file_format="binary")).json()
    num_vertices = _num_vertices;
    num_edges = num_vertices*_num_edges_per_vertex;
    edges = []
    random_edges = np.random.randint(0, num_vertices, size=(num_edges,2))
    random_weights = np.random.uniform(0,10.0, size=(num_edges))
    #np.random.randint(0,10, size=(10,2))
    for i in range(num_edges):
        src = random_edges[i][0]
        dst = random_edges[i][1]
        weight = random_weights[i]
        #src = random.randint(0,num_vertices)
        #dst = random.randint(0,num_vertices)
        #weight = random.uniform(0,10.0);
        if src == dst:
            continue
        edges.append((src, dst, i))
        edges.append((dst, src, i))
    #quit()
    edges.sort()
    #quit()
    edges.append((num_vertices+1, num_vertices+1, 0)) # add sentinel
    filtered_edges = []
    for i in range(0, len(edges)-1):
        if edges[i][0:2] != edges[i+1][0:2]:
            filtered_edges.append(edges[i])
    #filtered_edges = edges
    row = []
    col = []
    weights = []
    for i in range(len(filtered_edges)):
       row.append(filtered_edges[i][0]) 
       col.append(filtered_edges[i][1]) 
       weights.append(random_weights[filtered_edges[i][2]]) 
    return Input(graph=COOFormat(row=row, col=col, weight=weights), meta_info=meta_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file", type=str, required=True)
    parser.add_argument("--format", choices=['coo_format', 'random_generated_graph', 'data_file_format'])
    parser.add_argument("--num_vertices", type=int, required=False, default=0)
    parser.add_argument("--num_edges_per_vertex", type=int, required=False, default=0)
    parser.add_argument("--filename", type=str, required=False, default=None)
    parser.add_argument("--file_format", choices=['binary'], required=False, default='binary')
    parser.add_argument("--save_to_binary", type=bool, required=False, default=False)
    parser.add_argument("--save_filename", type=str, required=False, default=None)
    parser.add_argument("--short_description", type=str, required=False, default="")
    parser.add_argument("--tags", type=str, required=False, nargs="*", default=[])

    args = parser.parse_args()

    if args.save_to_binary:
        assert(args.save_filename != None)

    if args.format == 'data_file_format':
        assert(args.filename != None)

    if args.format == 'coo_format' or args.format == 'random_generated_graph':
        assert(args.num_vertices != 0 and args.num_edges_per_vertex != 0)
        
    meta_info = None
    if args.save_to_binary:
        meta_info = MetaInfo(save_to_binary=args.save_to_binary, save_filename=args.save_filename)
    else:
        meta_info = MetaInfo(save_to_binary=False, save_filename="", short_description=args.short_description, tags=args.tags)

    if args.format == 'data_file_format':
        open(args.output_file,'w+').write(Input(graph=DataFileFormat(filename=args.filename, file_format=args.file_format), meta_info=meta_info).json())
        quit()
    if args.format == 'coo_format':
        open(args.output_file,'w+').write(coo_format_gen(args.num_vertices, args.num_edges_per_vertex, meta_info=meta_info).json())
        quit()
    if args.format == 'random_generated_graph':
        open(args.output_file, 'w+')(Input(graph=RandomGeneratedGraph(num_vertices=args.num_vertices, num_edges_per_vertex=args.num_edges_per_vertex), meta_info=meta_info).json())
        quit() 

    #print(args)
    #quit()
    #N = int(sys.argv[1])
    #print(main(N))
