
#define USING_SPEEDCODE_INPUT_SPEC 1


#include <cilk/cilk.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <random>
#include <sys/time.h>
#include <unistd.h>
#include <vector>
#include <nanobench.h>

#include <catch2/catch_test_macros.hpp>
//#include <catch2/benchmark/catch_benchmark.hpp>
//#include <catch2/matchers/catch_matchers_floating_point.hpp>

#include <emmintrin.h>

#include "./solution.hpp"
#include "./inputschema.cpp"

namespace Driver {
#include <driver_common.h>
}

#include "./input.hpp"

namespace Driver {
#include "./get_time.h"

TEST_CASE("Custom", "[custom]") {
  auto inputs = get_custom_inputs();

  for (int i = 0; i < inputs.size(); i++) {
      ProblemInput input(std::get<0>(inputs[i]), std::get<1>(inputs[i]));
      std::optional<std::string> error_message = input.check();
      if (error_message.has_value()) {
        CAPTURE(error_message.value());
        REQUIRE(!error_message.has_value());
      } else {
        REQUIRE(!error_message.has_value());
      }
  }
}

TEST_CASE("Correctness", "[correctness]") {
  auto inputs = get_inputs();

  for (int i = 0; i < inputs.size(); i++) {
      ProblemInput input(std::get<0>(inputs[i]), std::get<1>(inputs[i]));
      std::optional<std::string> error_message = input.check();
      if (error_message.has_value()) {
        CAPTURE(error_message.value());
        REQUIRE(!error_message.has_value());
      } else {
        REQUIRE(!error_message.has_value());
      }
  }
}

TEST_CASE("Cilksan", "[cilksan]") {
  auto inputs = get_inputs();
  for (int i = 0; i < inputs.size(); i++) {
      ProblemInput input(std::get<0>(inputs[i]), std::get<1>(inputs[i]));
      std::optional<std::string> error_message = input.check();
      CAPTURE(error_message);
      REQUIRE(!error_message.has_value());
      if (error_message.has_value()) {
        CAPTURE(error_message.value());
        REQUIRE(!error_message.has_value());
      } else {
        REQUIRE(!error_message.has_value());
      }
  }
}

bool success() {
  return true;
}

TEST_CASE("Cilkscale", "[cilkscale]") {
  auto inputs = get_inputs();

  wsp_t cilkscale_sum = wsp_zero();
  for (int i = 0; i < inputs.size(); i++) {
      ProblemInput input(std::get<0>(inputs[i]), std::get<1>(inputs[i]));
      wsp_t cilkscale_start = wsp_getworkspan();
      auto ret = input.run();
      ankerl::nanobench::doNotOptimizeAway(ret);
      wsp_t cilkscale_end = wsp_getworkspan();
      wsp_t cilkscale_elapsed = wsp_sub(cilkscale_end,cilkscale_start);
      cilkscale_sum = wsp_add(cilkscale_sum, cilkscale_elapsed);
  }

  export_cilkscale_results(cilkscale_sum);
}

TEST_CASE("Benchmark", "[benchmark]") {

  _tm2.reset();
  _tm2.start();
  auto inputs = get_inputs();
  _tm2.stop();
  _tm2.reportTotal("loading the inputs");
  auto bencher = get_bencher(5,5); // Run for 10 epochs with at least 10 iterations each.
  for (int i = 0; i < inputs.size(); i++) {
     printf("%s\n", std::get<0>(inputs[i]).c_str());
     std::string inp_name = std::get<0>(inputs[i]);
     quicktype::Inputschema& inp = std::get<1>(inputs[i]);

     auto env_name = getenv("DYNAMIC_BENCHMARK_NAME");
     std::string benchmark_name;

     if (env_name == NULL) {
             benchmark_name = std::string("Error");
     } else {
             benchmark_name = std::string(getenv("DYNAMIC_BENCHMARK_NAME"));
     }

     uint64_t iter_count = 0;
     _tm.reset();
     //std::vector<uint64_t> times(1000000); 
     bencher.run(benchmark_name, [&] {
      //_tm2.reset();
      //_tm2.start();
       ProblemInput input(inp_name, inp);
       //_tm2.stop();
       //_tm2.reportTotal("ProblemInput constructor time.");
       _tm.start();
       input.run();
       _tm.stop();
       //times[iter_count] = _tm.get_total();
       iter_count += 1;
     });
     /*for (int i = 0 ; i < iter_count; i++) {
        double time_sec = (times[i]*1e-9)/(i+1);// / iter_count;
        double time_nansec = (times[i]*1.0)/(i+1);// / iter_count;

        printf("Total time %d: %f sec, %f nanoseconds\n", i, time_sec, time_nansec);
     }*/
     double time_sec = (_tm.get_total()*1e-9) / iter_count;
     double time_nansec = (_tm.get_total()*1.0) / iter_count;

     printf("Total time: %f sec, %f nanoseconds\n", time_sec, time_nansec);
  }

  export_benchmark_results(bencher);
}

} // end Driver namespace
