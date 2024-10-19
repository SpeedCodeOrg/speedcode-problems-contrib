#!/bin/bash

set -e
make run_all_correctness
make correctness
python -m sandbox_utils.parse_correctness

make benchmark
python -m sandbox_utils.parse_benchmark

echo ""
echo "Success"

