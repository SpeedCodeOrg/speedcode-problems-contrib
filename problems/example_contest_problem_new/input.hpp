#include "solution.hpp"
#include <optional>
#include <string>
#include <nanobench.h>
#include <sstream>
#include <memory>
#include <vector>
#include "solution_ref.hpp"

class ProblemInput {
    std::string inp_name;
    quicktype::Inputschema input;
    uint64_t N;
    uint64_t M;
    eidType* rowptr;
    vidType* col;
    weight_type* weights;

    std::vector<vidType> queries;
    std::vector<std::vector<weight_type>> distances;
    BaseGraph* graph;
public:
    ProblemInput(std::string inp_name, quicktype::Inputschema& _input, decltype(initialize_graph) init = initialize_graph) {
        inp_name = inp_name;
        input = _input;
        // convert COO form to CSR format.
        N = input.row[0];
        for (int64_t i = input.row.size(); --i >= 0;) {
            if (input.row[i] > N) {
                N = input.row[i];
            }
        }
        M = input.col.size();
        assert(input.col.size() == input.row.size() && "In COO format col and row must have the same lengths");
        assert(input.col.size() == input.weight.size() && "In COO format col, row, weights must have the same lengths");
        rowptr = new eidType[N+1]();
        col = new vidType[M]();
        weights = new weight_type[M]();

        for (size_t i = 0; i < input.row.size(); i++) {
            vidType src = input.row[i];
            vidType dst = input.col[i]; 
            col[i] = dst;
            rowptr[src] += 1;
            weights[i] = input.weight[i];
        }
        for (size_t i = 1; i < N+1; i++) {
            rowptr[i] += rowptr[i-1];
        }
        graph = init(rowptr, col, weights, N, M);
        
        for (int i = 0; i < 10; i++) {
            queries.push_back(i);
            distances.emplace_back(N, std::numeric_limits<weight_type>::max());
        }
    }

    ~ProblemInput() {
        delete[] rowptr;
        delete[] col;
        delete[] weights;
        delete graph;
    }

    auto run() {
        for (int i = 0; i < queries.size(); i++) {
            graph->SSSP(queries[i], distances[i].data());
        }
        return true;
    }

    //bool approximatelyEqual(weight_type a, weight_type a_ref, double absError = 1e-7, double relError = 1e-9) {
    bool approximatelyEqual(weight_type a, weight_type a_ref, double absError = 1e-7, double relError = 1e-9) {
        if (fabs(a-a_ref) <= absError || fabs(a-a_ref) <= a_ref*relError) return true;
        return false;
    }
    std::optional<std::string> check() {
        run();
        ProblemInput reference = ProblemInput(inp_name, input, reference::initialize_graph);
        reference.run();
        for (int64_t i = 0; i < distances.size(); i++) {
            if (distances[i].size() != reference.distances[i].size()) return "Incorrect # queries in distance array";
            for (int64_t j = 0; j < distances[i].size(); j++) {
                if (!approximatelyEqual(distances[i][j], reference.distances[i][j])) {
                    return "Incorrect value, expected distance " + std::to_string(reference.distances[i][j]) + ", but got " + std::to_string(distances[i][j]);
                }
            }
        }
        return std::nullopt;
    }
};
