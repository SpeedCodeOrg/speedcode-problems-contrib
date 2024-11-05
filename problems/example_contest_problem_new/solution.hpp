#pragma once
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>

using vidType = unsigned int;
using eidType = unsigned long;
using weight_type = float;
using edge_t = std::pair<vidType, weight_type>;

class BaseGraph {
public:
  virtual void SSSP(vidType source, weight_type *distances) = 0;
  virtual ~BaseGraph(){};
};

BaseGraph* initialize_graph(eidType* rowptr, vidType* col, weight_type* weights, uint64_t N, uint64_t M);