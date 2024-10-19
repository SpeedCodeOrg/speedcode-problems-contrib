

ifeq ($(SPEEDCODE_SERVER), 1)
	SANDBOX_CXXFLAGS = `/bin/python3 ${UTILS_DIR}/get_copts.py3` -I$(UTILS_DIR)/include -DPARLAY_OPENCILK 
	OUTPUT_PREFIX = /box
	SANDBOX_PREFIX = /sandbox
else
	UTILS_DIR=../.sandbox_utils
	SANDBOX_CXXFLAGS = -O3 -I$(UTILS_DIR)/include -DPARLAY_OPENCILK
	OUTPUT_PREFIX = .
	SANDBOX_PREFIX = .
endif



compile_all_benchmarks:
	$(MAKE) -j 8 -f ${UTILS_DIR}/Makefile.common compile_all_benchmarks

benchmark: compile_all_benchmarks
	$(MAKE)  -f ${UTILS_DIR}/Makefile.common $@
#export EXTRA_ARGUMENTS=${EXTRA_ARGUMENTS}
%:
	$(MAKE)  -f ${UTILS_DIR}/Makefile.common $@

default:
	$(MAKE)  -f ${UTILS_DIR}/Makefile.common
############################################################################
## Compilation and linking flags
#
#COMMON_CXXFLAGS=-fopencilk -O3 -Rpass='(loop-vectorize)' -march=native -g -gdwarf-4 `pkg-config --cflags catch2-with-main` -I${CONDA_PREFIX}/include
#
#ifeq ($(SPEEDCODE_SERVER), 1)
#	SANDBOX_CXXFLAGS = `/bin/python3 ${UTILS_DIR}/get_copts.py3` -I$(UTILS_DIR)/include
#	OUTPUT_PREFIX = /box
#	SANDBOX_PREFIX = /sandbox
#else
#	UTILS_DIR=../.sandbox_utils
#	SANDBOX_CXXFLAGS = -O3 -I$(UTILS_DIR)/include
#	OUTPUT_PREFIX = .
#	SANDBOX_PREFIX = .
#endif
#
#CXX=${OPENCILK_COMPILER_DIR}/bin/clang++
#CXXFLAGS=$(COMMON_CXXFLAGS) $(SANDBOX_CXXFLAGS)
#LDFLAGS=-fopencilk `pkg-config --libs catch2-with-main`
#
#CILKSAN_CXXFLAGS=-fsanitize=cilk
#CILKSAN_LDFLAGS=-fsanitize=cilk
#CILKSCALE_CXXFLAGS=-fcilktool=cilkscale-instructions
#CILKSCALE_LDFLAGS=-fcilktool=cilkscale-instructions
#
#%.cilksan : CXXFLAGS+=$(CILKSAN_CXXFLAGS)
#%.cilksan : LDFLAGS+=$(CILKSAN_LDFLAGS)
#%.cilkscale : CXXFLAGS+=$(CILKSCALE_CXXFLAGS)
#%.cilkscale : LDFLAGS+=$(CILKSCALE_LDFLAGS)
#
#.PHONY : all clean run tiers correctness run-cilksan run-cilkscale
#
#all: tmp
#
############################################################################
## Rules for building object files from sources
#
## To avoid rebuilding common library, we assume its prebuilt in a directory sandbox has read access to.
#$(UTILS_DIR)/lib/nanobench.o : $(UTILS_DIR)/include/nanobench.cpp
#	@mkdir -p $(@D)
#	$(CXX) $(SANDBOX_CXXFLAGS) -g -gdwarf-4 -c $^ -o $@
#
#$(OUTPUT_PREFIX)/%.o : $(SANDBOX_PREFIX)/%.cpp
#	$(CXX) $^ -c $(CXXFLAGS) -o $@
#
#$(OUTPUT_PREFIX)/%.o.cilksan : $(SANDBOX_PREFIX)/%.cpp
#	$(CXX) $^ -c $(CXXFLAGS) -o $@
#
#$(OUTPUT_PREFIX)/%.o.cilkscale : $(SANDBOX_PREFIX)/%.cpp
#	$(CXX) $^ -c $(CXXFLAGS) -o $@
#
############################################################################
## Rules for builing executables from object files
#
#$(OUTPUT_PREFIX)/tmp : $(OUTPUT_PREFIX)/driver.o $(OUTPUT_PREFIX)/solution.o $(UTILS_DIR)/lib/nanobench.o
#	$(CXX) $^ $(LDFLAGS) -o $@
#
#$(OUTPUT_PREFIX)/tmp% : $(OUTPUT_PREFIX)/driver.o% $(OUTPUT_PREFIX)/solution.o% $(UTILS_DIR)/lib/nanobench.o
#	$(CXX) $^ $(LDFLAGS) -o $@
#
############################################################################
## Phony rules for running different tests
#
#run : $(OUTPUT_PREFIX)/tmp
#	LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CONDA_PREFIX}/lib:${OPENCILK_COMPILER_DIR}/lib $(OUTPUT_PREFIX)/tmp ${EXTRA_ARGUMENTS}
#
#tiers : $(OUTPUT_PREFIX)/tmp
#	LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CONDA_PREFIX}/lib:${OPENCILK_COMPILER_DIR}/lib $(OUTPUT_PREFIX)/tmp `python ${UTILS_DIR}/get_tier_benchmarks.py` --reporter XML::out=${OUTPUT_PREFIX}/result.xml --reporter TAP::out=${OUTPUT_PREFIX}/result.tap --reporter console
#
#
#benchmark: $(OUTPUT_PREFIX)/tmp
#	LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CONDA_PREFIX}/lib:${OPENCILK_COMPILER_DIR}/lib $(OUTPUT_PREFIX)/tmp [benchmark] --reporter XML::out=${OUTPUT_PREFIX}/result.xml --reporter TAP::out=${OUTPUT_PREFIX}/result.tap --reporter console
#
#correctness : $(OUTPUT_PREFIX)/tmp
#	LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CONDA_PREFIX}/lib:${OPENCILK_COMPILER_DIR}/lib $(OUTPUT_PREFIX)/tmp [correctness] --reporter XML::out=${OUTPUT_PREFIX}/result.xml --reporter TAP::out=${OUTPUT_PREFIX}/result.tap --reporter console
#
#
#
#run-cilksan : $(OUTPUT_PREFIX)/tmp.cilksan
#	LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CONDA_PREFIX}/lib:${OPENCILK_COMPILER_DIR}/lib $(OUTPUT_PREFIX)/tmp.cilksan [correctness] ${EXTRA_ARGUMENTS}
#
#run-cilkscale : $(OUTPUT_PREFIX)/tmp.cilkscale
#	LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CONDA_PREFIX}/lib:${OPENCILK_COMPILER_DIR}/lib $(OUTPUT_PREFIX)/tmp.cilkscale [cilkscale] #${EXTRA_ARGUMENTS}
#
#
#
#clean :
#	rm -f $(OUTPUT_PREFIX)/%.o $(OUTPUT_PREFIX)/*.o* $(OUTPUT_PREFIX)/tmp $(OUTPUT_PREFIX)/tmp.* ${OUTPUT_PREFIX}/result.tap  ${OUTPUT_PREFIX}/result.xml ${OUTPUT_PREFIX}/tier*.json *~
