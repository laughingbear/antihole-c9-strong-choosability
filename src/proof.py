"""Generate the SAT instance for l=5 and a DRUP refutation proof (Glucose 4 via python-sat).

Usage: python3 src/proof.py P [OUTDIR]
  P      palette size (20 covers all palettes by the bound in NOTE.md; 36 is the absolute maximum)
  OUTDIR where to write l5p{P}.cnf and l5p{P}.drup (default: build/)
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skcc import build
from pysat.solvers import Glucose4

p = int(sys.argv[1])
out = sys.argv[2] if len(sys.argv) > 2 else 'build'
os.makedirs(out, exist_ok=True)
tag = os.path.join(out, f"l5p{p}")
cnf, pool, N, s, p = build(5, p=p)
cnf.to_file(f'{tag}.cnf')
t = time.time()
with Glucose4(bootstrap_with=cnf.clauses, with_proof=True) as S:
    r = S.solve()
    print(f"l5p{p}:", 'SAT' if r else 'UNSAT', f'{time.time() - t:.1f}s', flush=True)
    if r:
        sys.exit("unexpected SAT")
    with open(f'{tag}.drup', 'w') as f:
        for line in S.get_proof():
            f.write(line + '\n')
print("wrote", f'{tag}.cnf', f'{tag}.drup')
