#include "solution_ref.hpp"
#include <cilk/cilk.h>
#include <cmath>
#include <queue>
#include <vector>

namespace reference {
typedef std::pair<weight_type, vidType> WN;

class Graph : public BaseGraph {
    eidType* rowptr;
    vidType* col;
    weight_type* weights;
    uint64_t N;
    uint64_t M;
    public:
        Graph(eidType* rowptr, vidType* col, weight_type* weights, uint64_t N, uint64_t M) :
        rowptr(rowptr), col(col), weights(weights), N(N), M(M) {}
        ~Graph() {
            // destructor logic.
            // If you perform any memory allocations with malloc, new, etc. you must free
            //   them here to avoid memory leaks.
        }

        void SSSP(vidType source, weight_type *distances) {
            std::priority_queue<WN, std::vector<WN>, std::greater<WN>> mq;
            distances[source] = 0;
            mq.push(std::make_pair(0, source));
            while (!mq.empty()) {
                auto td = mq.top().first;
                auto src = mq.top().second;
                mq.pop();
                if (td == distances[src]) {
                    for (uint64_t i = rowptr[src]; i < rowptr[src+1]; i++) {
                        vidType dst = col[i];
                        weight_type wt = weights[i];
                        if (td + wt < distances[dst]) {
                            distances[dst] = td + wt;
                            mq.push(std::make_pair(td + wt, dst));
                        }
                    }
                }
            }
        }

};

BaseGraph* initialize_graph(eidType* rowptr, vidType* col, weight_type* weights, uint64_t N, uint64_t M) {
    return new Graph(rowptr, col, weights, N, M);
}

} // end namespace reference.