# SPE4IC'25 Problem 1: BFS

This is one of the test problems for the SPE4IC track of the FastCode Programming Challenge at PPoPP’25. The goal is to leverage parallelism to improve the performance for breadth-first search. This is not an easy task - achieving high parallelism in BFS is highly challenging due to the irregular computation. Good luck!

You can find more details about the competition on our website here:

https://fastcode.org/events/fastcode-challenge/

Description about the test dataset, background overview, and scoring on the competition website here:

https://fastcode.org/events/fastcode-challenge/spe4ic/


## Problem statement

Given a graph $$G=(V,E)$$, and a source vertex $$s\in V$$, your task is to compute the number of hops needed from $$s$$ to all vertices in $$G$$. In this problem, all graphs are undirected. 

## Input

The input graph is given in the standard *Compressed Sparse Row (CSR)* format. We use `N` to denote the number of vertices, and `M` the number of edges. Each vertex id is an integer from `0` to `N-1`, and each edge id are from `0` to `M-1`. A graph is initialized from the input data, represented by three arrays:

`eidType* rowptr`: the “offset” array in CSR. Each index is a vertex id. Each element is an edge id in range `[0, M-1]`, which is a pointer to a location in the col array. `rowprt[N]` is always set to `M`.

`vidType* col`: the “edges” array in CSR. Each index is an edge id. Each element is a vertex id in range [0, N-1]. 

In particular, for vertex `v`, `rowptr[v]` specifies the starting location of its neighbor list in the edge list array `col`. All its neighbors are stored from `col[rowptr[v]..(rowptr[v+1]-1)]`. 

The graphs are all undirected. An edge `(u,v)` will appear twice in the CSR: `u` will appear in the neighborlist of `v` and `v` will also appear in the neighbor list of `u`.

The source is given as `vidType source`.

## Output

The output is an array `weight_type* distances`. For each vertex id `v` (from `0` to `N-1`), `distance[v]` is the hop distance from `source` to `v`.

## Example

### Input:
`rowptr: [0, 2, 5, 7, 10, 12]`

`col: [1, 4, 0, 2, 3, 1, 3, 1, 2, 4, 0, 3]`

`source: 0` 

![Example image](/images/SPE4IC25/bfs.png)


### Output: 

`distances: [0, 1, 2, 2, 1]`

## Constraints

The sizes of the tested graphs are given below:

| Graph Name    | `\|V\|` | `\|E\|` | Notes |
| ------- | ------- | ------- | ------- |
| Social Network  |  4.9M   | 85.8M | Small diameter |
| Web Graph | 6.6M     | 300M | Small diameter |
| Collaboration Network    | 1.1M    | 113M | Small diameter|
| Synthetic Dense | 10M | 1B | Small diameter | 
| Road Network 1 | 22.1M | 30.0M | Large diameter |
| Road Network 2 | 87.0M | 112.9M | Large diameter |
| kNN Graph | 24.9M | 158M | Large diameter |
| Synthetic Sparse | 10M | 40M | Large diameter |

The synthetic dense graph is generated from Erdos-Renyi model. The synthetic sparse graph is a mesh-like planar graph. 

`|V|` = number of vertices

`|E|` = number of edges

All graphs are undirected. 

In the final test, the tested graphs are mostly the same as the graphs used in this problem, but with 1% of the edges changed (insertion/deletion). The vertices will be re-ordered. This is to avoid specific optimizations overfit to these test graphs. 

The final tests will also use a different set of sources from this problem. 

We have special awards for outstanding solutions to specific graph types. In particular, we consider the four graphs with small diameters as one test set, and the other four large-diameter graphs as another test set. The best submission for each test set will get honorable mention awards. 


## Function Signature

Function `initialize_graph` will set the input graph. You can use this function to perform simple preprocessing of the graph. The preprocessing time is limited to `max(2*time_ref, 10 milliseconds)`, where `time_ref` is the running time of the reference code. This time will not be counted as your score.

Function `void BFS(vidType source, weight_type *distances)` takes the source vertex id `source` and an array `distance`. Your output will be stored and returned in the `distance` array.

## Hints for Optimization:

You can find more details about the competition, including the test dataset, background overview, possible algorithms and optimizations, and scoring on the competition website here:

https://fastcode.org/events/fastcode-challenge/spe4ic/


## Update Log

* 12/15/2024: Updates to OpenMP support. Including OpenMP header `#include <omp.h>` will cause solutions to be compiled with proper flags to link to the OpenMP runtime. 
* 12/18/2024: Graph data has been updated to correct the weight distributions on certain graphs.


