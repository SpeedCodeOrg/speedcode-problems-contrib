#pragma once
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>

using vidType = unsigned int;
using eidType = unsigned long;
using weight_type = unsigned int;
using edge_t = std::pair<vidType, weight_type>;

class BaseGraph {
public:
  virtual void BFS(vidType source, weight_type *distances) = 0;
  virtual ~BaseGraph(){};
};

BaseGraph* initialize_graph(eidType* rowptr, vidType* col, uint64_t N, uint64_t M);
