#include "solution.hpp"
#include <algorithm>

std::vector<std::string> solution_entry(std::vector<std::string> input) {
    std::sort(input.begin(), input.end());
    return input;
}
