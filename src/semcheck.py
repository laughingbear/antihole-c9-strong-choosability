# Encoding-semantics test: with lists FIXED (unit assumptions), the Hall-violator encoding must be SAT
# exactly when the independent brute-force says "not colourable".
import sys, random, itertools
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skcc import build, colourable_bruteforce
from pysat.solvers import Cadical153
random.seed(11)
for l,p in [(4,7),(5,7),(5,9)]:
  cnf,pool,N,s,p=build(l,p=p,nonconst=False,symbreak=False)
  S=Cadical153(bootstrap_with=cnf.clauses)
  agree=dis=noncol=0
  for t in range(3000):
    pal=random.randint(s,p)   # small palettes make non-colourable lists common
    base=random.sample(range(pal),s)
    L=[]
    for v in range(N):
      if random.random()<0.6: L.append(sorted(base))
      else: L.append(sorted(random.sample(range(pal),s)))
    assum=[ (pool.id(('x',v,c)) if c in L[v] else -pool.id(('x',v,c))) for v in range(N) for c in range(p)]
    enc_noncol=S.solve(assumptions=assum)
    bf_noncol=not colourable_bruteforce(L)
    noncol+=bf_noncol
    if enc_noncol==bf_noncol: agree+=1
    else: dis+=1; print('DISAGREE',l,L,enc_noncol,bf_noncol)
  print(f"l={l} p={p}: {agree} agree, {dis} disagree; non-colourable cases among them: {noncol}")
