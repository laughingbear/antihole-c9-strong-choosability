#!/usr/bin/env bash
# Reproduce the main result end to end (Linux / WSL / macOS; needs python3, pip, git, gcc, make).
# 1. regenerate both SAT instances from src/skcc.py and check they match cnf/SHA256SUMS
# 2. solve them with Glucose 4 (python-sat), emitting DRUP proofs
# 3. check both proofs with drat-trim (pinned commit)
# Takes about 2 minutes; the proofs are ~130 MB each (written to build/).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -c "import pysat" 2>/dev/null || python3 -m pip install python-sat
mkdir -p build
for P in 20 36; do python3 src/proof.py "$P" build; done
( cd build && sha256sum -c ../cnf/SHA256SUMS )
if [ ! -x build/drat-trim/drat-trim ]; then
  git clone -q https://github.com/marijnheule/drat-trim.git build/drat-trim
  git -C build/drat-trim checkout -q 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
  make -C build/drat-trim drat-trim
fi
status=0
for P in 20 36; do
  echo "== drat-trim l5p$P"
  build/drat-trim/drat-trim "build/l5p$P.cnf" "build/l5p$P.drup" | tr -d '\r' > "build/drat-trim-l5p$P.log" || true
  grep -E "^s |verification time" "build/drat-trim-l5p$P.log"
  grep -qx "s VERIFIED" "build/drat-trim-l5p$P.log" || status=1
done
[ $status -eq 0 ] && echo "ALL PROOFS VERIFIED" || { echo "VERIFICATION FAILED"; exit 1; }
