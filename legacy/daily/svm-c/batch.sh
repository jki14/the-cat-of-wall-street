#! /bin/bash

python benchmark.py 5 35 benchmark.log.0 > benchmark.out.0 2>&1 &
python benchmark.py 35 65 benchmark.log.1 > benchmark.out.1 2>&1 &
