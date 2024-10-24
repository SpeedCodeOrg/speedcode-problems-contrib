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
public:
    ProblemInput(std::string inp_name, quicktype::Inputschema& input) {
        strings = input.strings;
    }

    auto run(decltype(solution_entry) F = solution_entry) {
        std::vector<std::string>& input = this->strings;
        auto Out = F(input);
        ankerl::nanobench::doNotOptimizeAway(Out);
        return input;
    }

    std::optional<std::string> check() {
        auto result = run();
        auto result_ref = run(reference_solution);
        if (result.size() != result_ref.size()) return "Error: result of incorrect size";

        for (size_t i = 0; i < result.size(); i++) {
            if (result[i] != result_ref[i]) {
                return "Incorrect value at index " + std::to_string(i) + 
                       ". Expected: " + result_ref[i] + 
                       ", Actual: " + result[i];
            }
        }
        return std::nullopt;
    }
};
