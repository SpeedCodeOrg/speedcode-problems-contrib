#include "solution.hpp"
#include <cilk/cilk.h>
#include <algorithm>
#include <vector>

// Custom comparator for parallel sort
bool compareStrings(const std::string &a, const std::string &b) {
    return a < b;
}

// Parallel merge function
void parallelMerge(std::vector<std::string> &input, int start, int mid, int end, std::vector<std::string> &temp) {
    int i = start, j = mid, for_index = 0;
    while (i < mid && j < end) {
        if (compareStrings(input[i], input[j])) {
            temp[for_index++] = input[i++];
        } else {
            temp[for_index++] = input[j++];
        }
    }
    while (i < mid) {
        temp[for_index++] = input[i++];
    }
    while (j < end) {
        temp[for_index++] = input[j++];
    }
    for (int k = 0; k < for_index; k++) {
        input[start + k] = temp[k];
    }
}

// Parallel sort function
void parallelSort(std::vector<std::string> &input, int start, int end, std::vector<std::string> &temp) {
    if (end - start <= 1024) {
      std::sort(&input[start], &input[end]);
      return;	    
    }
    int mid = start + (end - start) / 2;

    parallelSort(input, start, mid, temp);
    parallelSort(input, mid, end, temp);

    parallelMerge(input, start, mid, end, temp);
}

std::vector<std::string> solution_entry(std::vector<std::string> input) {
    std::vector<std::string> temp(input.size());
    parallelSort(input, 0, input.size(), temp);
    return input;
}
