#include "solution.hpp"
#include <cilk/cilk.h>
#include <cmath>
#include <queue>
#include <vector>
#include <tuple>
#include <map>
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
		data_pointer = (void*)col;
        }

        void SSSP(vidType source, weight_type *distances) {

	  #if 0
	  std::map<std::tuple<int,int>, float> edges;
          for (int i = 0; i < N; i++) {
            for (int j = rowptr[i]; j < rowptr[i+1]; j++) {
		edges[std::make_tuple(i,col[j])] = weights[j]; 
            }
          }
          for (int i = 0; i < N; i++) {
            for (int j = rowptr[i]; j < rowptr[i+1]; j++) {
		//edges[std::make_tuple(i,col[j])] = weights[j]; 
		if (edges.find(std::make_tuple(col[j],i)) == edges.end()) {
			printf("SOL Error the graph is not symmetric!\n");
		} else if (edges[std::make_tuple(col[j],i)] != weights[j]) {
			printf("SOL Error the graph weights are not symmetric %f, %f\n", edges[std::make_tuple(col[j],i)], weights[j]);
		}
            }
          }
	  #endif

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
