from typing import Annotated, Union, Literal, List, Optional
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

### Naming conventions for problem response models.
# All problem response models names should have the prefix PRM_ 


class PRM_Compile(BaseModel):
    command: str # Optional["/bin/make -f /sandbox/Makefile SPEEDCODE_SERVER=1 /box/tmp"]
    stdout: str
    stdin: str
    success: bool

class PRM_CompilerAnalysis(BaseModel):
    vector_report: str # Optional["/bin/make -f /sandbox/Makefile SPEEDCODE_SERVER=1 /box/tmp"]
    intel_assembly: str
    llvm_assembly: str
    success: bool

class PRM_CorrectnessTestCase(BaseModel):
    name: str
    success: bool
    info: List[str]
    expressions: List[str]

class PRM_CorrectnessTests(BaseModel):
    stdout: Optional[str]
    stderr: Optional[str]
    checks_passed: int
    checks_failed: int
    cases_passed: int
    cases_failed: int
    test_cases: List[PRM_CorrectnessTestCase]

class PRM_Tiers(BaseModel):
    stdout: Optional[str]
    stderr: Optional[str]
    tests: PRM_CorrectnessTests
    tier: float


class PRM_BenchmarkResult(BaseModel):
    function: str
    benchmark_name: str
    runtime: float
    instructions: float
    cpucycles: float
    contextswitches: float
    pagefaults: float
    branchinstructions: float
    branchmisses: float

class PRM_Benchmark(BaseModel):
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    tests: PRM_CorrectnessTests
    challenges: List[PRM_BenchmarkResult]
    reference: PRM_BenchmarkResult
    submission: PRM_BenchmarkResult


class PRM_CilkscaleBenchmarkSeries(BaseModel):
    title: str
    num_workers: List[int]
    obs_runtime: List[float]
    perf_lin_runtime: List[float]
    greedy_runtime: List[float]
    span_runtime: List[float]
    obs_speedup: List[float]
    perf_lin_speedup: List[float]
    greedy_speedup: List[float]
    span_speedup: List[float]

class PRM_CilkscaleBenchmark(BaseModel):
    data: List[PRM_CilkscaleBenchmarkSeries]

class PRM_Cilksan_DistinctRace_MemoryAccess(BaseModel):
    access_type: str
    function: str
    full_path: str
    file_name: str
    line_num: int
    col_num: int

class PRM_Cilksan_DistinctRace(BaseModel):
    memory_accesses: List[PRM_Cilksan_DistinctRace_MemoryAccess]

class PRM_Cilksan(BaseModel):
    distinct_races: int
    full_report: str
    distinct_race_list: Optional[List[PRM_Cilksan_DistinctRace]]

class PRM_CompilerAnalysis(BaseModel):
    vectorization_report: str
    assembly: str

class PRM_Error(BaseModel):
    error: bool
    stdout: Optional[str]
    stderr: Optional[str]
    details: Optional[str]

class PRM_CombinedResponse(BaseModel):
    token : Optional[str] = None
    correctness : Optional[Union[PRM_CorrectnessTests, PRM_Error]] = None
    custom : Optional[Union[PRM_CorrectnessTests, PRM_Error]] = None
    tiers : Optional[Union[PRM_Tiers, PRM_Error]] = None
    benchmark: Optional[Union[PRM_Benchmark, PRM_Error]] = None
    cilkscale_benchmark: Optional[Union[PRM_CilkscaleBenchmark, PRM_Error]] = None
    cilksan: Optional[Union[PRM_Cilksan, PRM_Error]] = None
    compiler_analysis: Optional[Union[PRM_CompilerAnalysis, PRM_Error]] = None

class PRM_ContributeResponse(BaseModel):
    token : Optional[str] = None
    solution_hpp : Optional[str] = None
    solution_cpp : Optional[str] = None
    f0_cpp : Optional[str] = None
    input_hpp : Optional[str] = None
    schema_py : Optional[str] = None
    correctness_output : Optional[str] = None

class ProblemRequest(BaseModel):
    problem_id: int




@dataclass
class ProblemInfo(BaseModel):
    const_id: str
    title: str
    short_description: str
    max_tiers: int 
    tags: str
    location: str
    github_url: str
    public: bool
    #directory_name: str
    class Config:
        orm_mode = True

