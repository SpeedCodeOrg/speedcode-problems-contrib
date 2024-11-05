#include "solution.hpp"
#include <optional>
#include <string>
#include <nanobench.h>
#include <sstream>
#include <memory>
#include <vector>

// Reference solution for correctness test.
__attribute__((weak))
std::vector<std::string> reference_solution(std::vector<std::string> input) {
    std::sort(input.begin(), input.end());
    return input;
}

class ProblemInput {
    std::vector<std::string> strings;
    ankerl::nanobench::Rng rng;

    uint64_t N;
    uint64_t M;
    eidType* rowptr;
    vidType* col;
    weight_type* weights;

    std::vector<vidType> queries;
    std::vector<std::vector<weight_type>> distances;
    BaseGraph* graph;
public:
    ProblemInput(std::string inp_name, quicktype::Inputschema& input) {
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
        graph = initialize_graph(rowptr, col, weights, N, M);
    }

    ~ProblemInput() {
        delete[] rowptr;
        delete[] col;
        delete[] weights;
        delete graph;
    }

    //auto setup(decltype(initialize_graph) init = initialize_graph) {
    //    graph = init(rowptr, col, weights, N, M);
    //    
    //    distances.clear();
    //    queries.clear();
    //    for (int i = 0; i < 10; i++) {
    //        queries.push_back(i);
    //        distances.emplace_back(N, std::numeric_limits<weight_type>::max());
    //    }
    //}

    auto run() {
        distances.clear();
        queries.clear();
        for (int i = 0; i < 10; i++) {
            queries.push_back(i);
            distances.emplace_back(N, std::numeric_limits<weight_type>::max());
        }

        for (int i = 0; i < queries.size(); i++) {
            graph->SSSP(queries[i], distances[i].data());
        }
        return true;
    }

    std::optional<std::string> check() {
        auto result = run();
        //auto result_ref = reference.run();

        //if (result.size() != result_ref.size()) return "Error: result of incorrect size";

        //for (size_t i = 0; i < result.size(); i++) {
        //    if (result[i] != result_ref[i]) {
        //        return "Incorrect value at index " + std::to_string(i) + 
        //               ". Expected: " + result_ref[i] + 
        //               ", Actual: " + result[i];
        //    }
        //}
        return std::nullopt;
    }
};
