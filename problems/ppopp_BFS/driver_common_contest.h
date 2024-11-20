#include <cilk/cilkscale.h>
#include <sstream>
#include <iostream>
#include <vector>
#include <string>

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
	    //std::cout << entry.path() <<std::endl;
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

std::string get_datafile_path(std::string ref) {
  std::string path = "./data";
  if (std::getenv("SPEEDCODE_SERVER") != NULL && std::string(std::getenv("SPEEDCODE_SERVER")).compare("1") == 0) {
    path = "/sandbox/data";
  }
  return path + "/" + ref;
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

static std::vector<std::string> get_input_targets() {
  auto env_input_targets = getenv("DYNAMIC_INPUT_TARGETS");

  std::string bench_name;
  std::vector<std::string> input_targets;
  if (env_input_targets == NULL) {
	  //input_targets = "";//"benchmark_" + std::string((char*)BENCHMARK_NAME_SUBMISSION);
	  return input_targets;
  } else {
	std::string str(env_input_targets);
  	str.erase(str.find_last_not_of(' ')+1);         //suffixing spaces
  	str.erase(0, str.find_first_not_of(' '));       //prefixing spaces
  	str.erase(str.find_last_not_of('"')+1);         //suffixing quotes
  	str.erase(0, str.find_first_not_of('"'));       //prefixing quotes
  	str.erase(str.find_last_not_of('\'')+1);         //suffixing quotes
  	str.erase(0, str.find_first_not_of('\''));       //prefixing quotes


	 //std::istringstream f(env_input_targets);
	 std::istringstream f(str.c_str());
	 std::string s;
	 while (std::getline(f,s,',')) {
		std::string x(s);
		if (!x.ends_with(".json")) {
		   x = x + ".json";
		}
		if (x.find_last_of('/') != std::string::npos) {
		   x = x.substr(x.find_last_of('/')+1);
		}
		input_targets.push_back(x);
	 }
	 return input_targets;
         //bench_name = std::string(env_name);
  }

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

static std::string export_benchmark_input_results(ankerl::nanobench::Bench& bencher, std::string inp_name, uint64_t time_nanoseconds) {
  auto env_name = getenv("DYNAMIC_BENCHMARK_NAME");
  std::string bench_name;
  if (env_name == NULL) {
	  bench_name = "Error";//"benchmark_" + std::string((char*)BENCHMARK_NAME_SUBMISSION);
  } else {
         bench_name = std::string(env_name);
  }

  std::string dynamic_benchmark(bench_name);
  std::string filename = dynamic_benchmark+"_"+inp_name+".json"; 
  //std::string filename{BENCHMARK_RESULTS_FILE};
  std::fstream s{filename, s.trunc | s.in | s.out};
  ankerl::nanobench::render(ankerl::nanobench::templates::json(), bencher, s);
  return filename;
}
