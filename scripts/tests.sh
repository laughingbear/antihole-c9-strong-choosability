#!/usr/bin/env bash
# Controls for the encoding (each line states the expected outcome).
set -euo pipefail
cd "$(dirname "$0")/.."
run(){ echo "== $1   [expect $2]"; python3 src/skcc.py ${@:3} | tail -3; }
run "l=3 (C5, 2-lists)"                 UNSAT 3
run "l=4 (complement C7, 3-lists)"       UNSAT 4
run "l=4, identical lists allowed"       "SAT, identical, not colourable" 4 --const-ok
run "l=4, lists too small (size 2)"      "SAT, non-identical, not colourable" 4 --s 2
run "l=5, lists too small (size 3)"      "SAT, non-identical, not colourable" 5 --s 3
run "l=5, no symmetry breaking, p=6"     UNSAT 5 --p 6 --nosym
echo "== encoding semantics vs brute force on random fixed lists   [expect 0 disagree]"
python3 src/semcheck.py
