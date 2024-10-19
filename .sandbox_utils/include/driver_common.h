#include <cilk/cilkscale.h>

static const char* BENCHMARK_NAME_REFERENCE = "Reference";
static const char* BENCHMARK_NAME_SUBMISSION = "Submission";
static const char* BENCHMARK_RESULTS_FILE = "benchmark_results.json";

#ifdef USING_SPEEDCODE_INPUT_SPEC
std::vector<std::tuple<std::string, quicktype::Inputschema>> get_inputs() {
  std::vector<std::tuple<std::string, quicktype::Inputschema>> inputs;

  std::string path = "./inputs";
  if (std::getenv("SPEEDCODE_SERVER") != NULL && std::string(std::getenv("SPEEDCODE_SERVER")).compare("1") == 0) {
    path = "/sandbox/inputs";
  }
  for (const auto& entry : std::filesystem::directory_iterator(path)) {
    if (entry.path().has_extension() && entry.path().extension() == ".json") {
	    std::cout << entry.path() <<std::endl;
	    if (entry.path().stem() == "user_input") continue;
      std::ifstream in(entry.path());
      nlohmann::json j;
      in >> j;
      quicktype::Inputschema data;
      quicktype::from_json(j, data);
      inputs.push_back(std::make_tuple(entry.path().stem(), std::move(data)));
    }
  }
  return std::move(inputs);
}

std::vector<std::tuple<std::string, quicktype::Inputschema>> get_custom_inputs() {
  std::vector<std::tuple<std::string, quicktype::Inputschema>> inputs;

  std::string path = "./inputs";
  if (std::getenv("SPEEDCODE_SERVER") != NULL && std::string(std::getenv("SPEEDCODE_SERVER")).compare("1") == 0) {
    path = "/box/inputs";
  }
  for (const auto& entry : std::filesystem::directory_iterator(path)) {
    if (entry.path().has_extension() && entry.path().extension() == ".json") {
	    if (entry.path().stem() != "user_input") continue;
	    std::cout << entry.path() <<std::endl;
      std::ifstream in(entry.path());
      nlohmann::json j;
      in >> j;
      quicktype::Inputschema data;
      quicktype::from_json(j, data);
      inputs.push_back(std::make_tuple(entry.path().stem(), std::move(data)));
    }
  }
  return std::move(inputs);
}

#endif



static void export_cilkscale_results(wsp_t cilkscale_sum) {
  freopen("output.txt", "w", stdout);
  wsp_dump(cilkscale_sum, "Cilkscale");
  freopen("/dev/tty", "w", stdout);
}

static void __export_cilksan_output() {
}
static void export_cilksan_output() {
  freopen("cilksan-output.txt", "w", stdout);
}

auto get_bencher(int epochs = 5, int min_epoch_iterations = 4) {
  return ankerl::nanobench::Bench()
	  .epochs(epochs).minEpochIterations(min_epoch_iterations)
	  .performanceCounters(true).relative(true)
	  .minEpochTime(std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::milliseconds(200)));
}


static void export_benchmark_results(ankerl::nanobench::Bench& bencher) {
  auto env_name = getenv("DYNAMIC_BENCHMARK_NAME");
  std::string bench_name;
  if (env_name == NULL) {
	  bench_name = "Error";//"benchmark_" + std::string((char*)BENCHMARK_NAME_SUBMISSION);
  } else {
         bench_name = std::string(env_name);
  }

  std::string dynamic_benchmark(bench_name);
  std::string filename = dynamic_benchmark+".json"; 
  //std::string filename{BENCHMARK_RESULTS_FILE};
  std::fstream s{filename, s.trunc | s.in | s.out};
  ankerl::nanobench::render(ankerl::nanobench::templates::json(), bencher, s);
}
