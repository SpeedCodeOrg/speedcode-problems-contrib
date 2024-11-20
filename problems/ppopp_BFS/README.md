This is one of the test problems for the SPE4IC track of the FastCode
Programming Challenge at PPoPP’25. The goal is to leverage parallelism to
improve the performance for breadth-first search. This is not an easy task -
achieving high parallelism in BFS is highly challenging due to the irregular
computation. Good luck!

You can find more details about the competition on our website here:

https://fastcode.org/events/ppopp-programming-competition/

Description about the test dataset, background overview, and scoring on the competition website here:

https://fastcode.org/events/ppopp-programming-competition/traditional/


## Problem statement

Given a weighted graph $G=(V,E)$, and a source vertex $s\in V$, your task is to
compute the shortest distance from s to all vertices in G. In this problem, all
graphs are undirected with unit weights.

## Input

The input graph is given in the standard *Compressed Sparse Row (CSR)* format.
We use `N` to denote the number of vertices, and `M` the number of edges. Each
vertex id is an integer from `0` to `N-1`, and each edge id are from `0` to
`M-1`. A graph is initialized from the input data, represented by three arrays:

`eidType* rowptr`: the “offset” array in CSR. Each index is a vertex id. Each
element is an edge id in range `[0, M-1]`, which is a pointer to a location in
the col array. `rowprt[N]` is always set to `M`.

`vidType* col`: the “edges” array in CSR. Each index is an edge id. Each
element is a vertex id in range [0, N-1]. 

In particular, for vertex `v`, `rowptr[v]` specifies the starting location of
its neighbor list in the edge list array `col`. All its neighbors are stored
from `col[rowptr[v]..(rowptr[v+1]-1)]`. 

The graphs are all undirected. An edge `(u,v)` will appear twice in the CSR:
`u` will appear in the neighborlist of `v` and `v` will also appear in the
neighbor list of `u`.

The source is given as `vidType source`.

## Output

The output is an array `weight_type* distances`. Where `weight_type` is an
`unsigned int`. It is guaranteed that all graphs will have fewer than $$2^31$$
vertices. For each vertex id `v` (from `0` to `N-1`), `distance[v]` is the
shortest distance from `source` to `v` in the graph.

## Example

### Input:
`rowptr: [0, 2, 5, 7, 10, 12]`

`col: [1, 4, 0, 2, 3, 1, 3, 1, 2, 4, 0, 3]`

`source: 0` 

(Put the image for the example graph here)


### Output: 

`distances: [0, 1, 2, 2, 1]`

## Constraints

The sizes of the tested graphs are given below:

| Graph Name    | `\|V\|` | `\|E\|` | Notes |
| ------- | ------- | ------- | ------- |
| Social Network  |  4.9M   | 85.8M | Small diameter; skewed random edge weights |
| Web Graph | 6.6M     | 300M | Small diameter; skewed random edge weights |
| Collaboration Network    | 1.1M    | 113M | Small diameter; uniform random edge weights|
| Synthetic Dense | 10M | 1B | Small diameter; uniform random edge weights | 
| Road Network 1 | 22.1M | 30.0M | Large diameter; real edge weights |
| Road Network 2 | 87.0M | 112.9M | Large diameter; real edge weights |
| kNN Graph | 24.9M | 158M | Large diameter; real edge weights |
| Synthetic Sparse | 10M | 40M | Large diameter; skewed random edge weights |

The synthetic dense graph is generated from Erdos-Renyi model.

The synthetic sparse graph is a mesh-like planar graph. 

`|V|` = number of vertices

`|E|` = number of edges

All graphs are undirected. 

In the final test, the tested graphs are mostly the same as the graphs used in
this problem, but with 1% of the edges changed (insertion/deletion/edge weight
change). This is to avoid specific optimizations overfit to these test graphs. 

The final tests will also use a different set of sources from this problem. 

## Function Signature

Function `initialize_graph` will set the input graph. You can use this function
to perform simple preprocessing of the graph. The preprocessing time is limited
to `max(2*time_ref, 10 milliseconds)`, where `time_ref` is the running time of
the reference implementation of breadth-first search. This time will not be
counted as your score.

Function `void BFS(vidType source, weight_type *distances)` takes the source
vertex id `source` and an array `distance`. Your output will be stored and
returned in the `distance` array.

## Hints for Optimization:

You can find more details about the competition, including the test dataset,
background overview, possible algorithms and optimizations, and scoring on the
competition website here:


https://fastcode.org/events/ppopp-programming-competition/traditional/