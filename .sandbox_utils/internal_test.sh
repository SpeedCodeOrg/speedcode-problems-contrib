#!/bin/bash

set -e

make run_all_correctness

make correctness
python -m sandbox_utils.parse_correctness
make benchmark
python -m sandbox_utils.parse_benchmark
make run-cilkscale-benchmark
python -m sandbox_utils.parse_cilkscale_benchmark
make run-cilksan
python -m sandbox_utils.parse_cilksan

echo ""
echo "Success"

