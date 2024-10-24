#include "solution.hpp"
#include <cilk/cilk.h>
#include <cilk/opadd_reducer.h>
#include <algorithm>
#include <vector>

#include <cilk/cilk.h>

void Merge_ScalarTrivial(const std::string *aArr, int aCnt, const std::string *bArr, int bCnt, std::string *dst) {
    std::merge(aArr, aArr+aCnt, bArr, bArr+bCnt, dst);
}


#define MERGE_CUTOFF 2000
int Merge_Parallel(const std::string *aArr, int aCnt, const std::string *bArr, int bCnt, std::string *dst) {
  if (aCnt + bCnt <= MERGE_CUTOFF) {
    Merge_ScalarTrivial(aArr, aCnt, bArr, bCnt, dst);
    //Merge_ScalarBranchless_3(aArr, aCnt, bArr, bCnt, dst);
    //Merge_Simd_KeysOnly(aArr, aCnt, bArr, bCnt, dst);
  } else {
    const std::string *am, *bm;
    if (aCnt < bCnt) {
      bm = bArr + bCnt / 2;
      am = std::upper_bound(aArr, aArr + aCnt, *bm);
    } else {
      am = aArr + aCnt / 2;
      bm = std::lower_bound(bArr, bArr + bCnt, *am);
    }
    std::string * zm = dst + (am - aArr) + (bm - bArr);
    cilk_spawn Merge_Parallel(aArr, am - aArr, bArr, bm - bArr, dst);
    Merge_Parallel(am, aArr + aCnt - am, bm, bArr + bCnt - bm, zm);
  }
  return aCnt + bCnt;
}



// Parallel sort function
void parallelSort(std::vector<std::string> &input, int start, int end, std::vector<std::string> &temp) {
    if (end - start <= 1024) {
      std::sort(&input[start], &input[end]);
      return;	    
    }
    int mid = start + (end - start) / 2;

    cilk_spawn parallelSort(input, start, mid, temp);
    parallelSort(input, mid, end, temp);
    cilk_sync;

    Merge_Parallel(&input[start], (mid-start), &input[mid], (end-mid), &temp[start]);
    cilk_for (int i = start; i < end; i++) {
      input[i] = temp[i];
    }
}

std::vector<std::string> solution_entry(std::vector<std::string> input) {
    std::vector<std::string> temp(input.size());
    parallelSort(input, 0, input.size(), temp);
    return input;
}
