#pragma once
#include "solution.hpp"
namespace reference {
  BaseGraph* initialize_graph(eidType* rowptr, vidType* col, weight_type* weights, uint64_t N, uint64_t M);
}