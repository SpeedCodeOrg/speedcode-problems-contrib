#include "solution.hpp"
#include <cilk/cilk.h>
#include <cmath>
#include <queue>
#include <vector>
namespace reference {
class Graph : public BaseGraph {
    eidType* rowptr;
    vidType* col;
    uint64_t N;
    uint64_t M;
    public:
        Graph(eidType* rowptr, vidType* col, uint64_t N, uint64_t M) :
        rowptr(rowptr), col(col), N(N), M(M) {}
        ~Graph() {
            // destructor logic.
            // If you perform any memory allocations with malloc, new, etc. you must free
            //   them here to avoid memory leaks.
        }

        void BFS(vidType source, weight_type *distances) {
            std::vector<vidType> this_frontier;
            distances[source] = 0;
            this_frontier.push_back(source);
            while (!this_frontier.empty()) {
                std::vector<vidType> next_frontier;
                for (const auto & src : this_frontier) {
                    for (uint64_t i = rowptr[src]; i < rowptr[src+1]; i++) {
                        vidType dst = col[i];
                        if (distances[src] + 1 < distances[dst]) {
                            distances[dst] = distances[src] + 1;
                            next_frontier.push_back(dst);
                        }
                    }
                }
                std::swap(this_frontier, next_frontier);
            }
        }

};

BaseGraph* initialize_graph(eidType* rowptr, vidType* col, uint64_t N, uint64_t M) {
    return new Graph(rowptr, col, N, M);
}
}
