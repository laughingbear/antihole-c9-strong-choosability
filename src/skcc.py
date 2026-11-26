"""Strong chromatic-choosability of odd antiholes  (arXiv 2610.14241, Conjecture 9).

G = complement of C_N, N = 2l-1. Claim: every s-assignment (s = l-1) for which G is not L-colourable
has all lists identical.

Encoding. Colour classes of G are cliques of C_N: single vertices or C_N-edges {i,i+1}. Hence G is
L-colourable iff for some matching M of C_N the blocks (matched pairs + unmatched vertices) have a
system of distinct representatives from their block lists (pair list = intersection). By Hall, G is
NOT L-colourable iff for EVERY matching M there is a set of blocks X_M with |union of lists| < |X_M|.
This is purely existential, so "exists a non-constant non-colourable assignment" is one SAT instance.
UNSAT  <=>  the conjecture holds for this l (for every palette size up to p; p = N*s covers all).
"""
import itertools, sys, argparse
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType

def matchings(N):
    E = [(i, (i + 1) % N) for i in range(N)]
    out = []
    for r in range(N // 2 + 1):
        for S in itertools.combinations(range(N), r):
            used = set()
            ok = True
            for e in S:
                a, b = E[e]
                if a in used or b in used: ok = False; break
                used |= {a, b}
            if ok: out.append([E[e] for e in S])
    return out

def build(l, s=None, p=None, nonconst=True, symbreak=True, enc=EncType.seqcounter):
    N = 2 * l - 1
    s = l - 1 if s is None else s
    p = N * s if p is None else p
    pool = IDPool(); cnf = CNF()
    x = lambda v, c: pool.id(('x', v, c))
    # exactly s colours per vertex
    for v in range(N):
        for cl in CardEnc.equals([x(v, c) for c in range(p)], bound=s, vpool=pool, encoding=enc).clauses:
            cnf.append(cl)
    if symbreak:
        for c in range(p):  # L(0) = {0..s-1}
            cnf.append([x(0, c)] if c < s else [-x(0, c)])
        # first-occurrence precedence for colours >= s
        occ = lambda c, v: pool.id(('occ', c, v))
        for c in range(s, p):
            for v in range(N):
                # occ(c,v) <-> x(c,v) or occ(c,v-1)
                prev = [occ(c, v - 1)] if v > 0 else []
                cnf.append([-occ(c, v), x(v, c)] + prev)
                cnf.append([occ(c, v), -x(v, c)])
                if v > 0: cnf.append([occ(c, v), -occ(c, v - 1)])
        for c in range(s, p - 1):
            for v in range(N):
                cnf.append([-occ(c + 1, v), occ(c, v)])
    if nonconst:
        if symbreak:
            cnf.append([x(v, c) for v in range(1, N) for c in range(s, p)])
        else:  # some vertex differs from vertex 0 somewhere
            d = []
            for v in range(1, N):
                for c in range(p):
                    t = pool.id(('diff', v, c)); d.append(t)
                    cnf.append([-t, x(v, c), x(0, c)]); cnf.append([-t, -x(v, c), -x(0, c)])
            cnf.append(d)
    # Hall violator for every matching
    for mi, M in enumerate(matchings(N)):
        matched = {a for e in M for a in e}
        blocks = [tuple(e) for e in M] + [(v,) for v in range(N) if v not in matched]
        ys = []
        zs = [pool.id(('z', mi, c)) for c in range(p)]
        for bi, B in enumerate(blocks):
            y = pool.id(('y', mi, bi)); ys.append(y)
            for c in range(p):
                # y and (all v in B have c) -> z_c
                cnf.append([-y] + [-x(v, c) for v in B] + [zs[c]])
        # |X| >= |Z| + 1   <=>  sum(y) + sum(not z) >= p + 1
        for cl in CardEnc.atleast(ys + [-z for z in zs], bound=p + 1, vpool=pool, encoding=enc).clauses:
            cnf.append(cl)
    return cnf, pool, N, s, p

def decode(model, pool, N, p):
    ms = set(l for l in model if l > 0)
    return [sorted(c for c in range(p) if pool.id(('x', v, c)) in ms) for v in range(N)]

def colourable_bruteforce(L):
    """Independent check: backtracking proper colouring of complement(C_N) from lists L."""
    N = len(L)
    adj = lambda u, v: u != v and (u - v) % N not in (1, N - 1)  # adjacent in complement of C_N
    col = [None] * N
    def bt(i):
        if i == N: return True
        for c in L[i]:
            if all(not (col[j] == c and adj(i, j)) for j in range(i)):
                col[i] = c
                if bt(i + 1): return True
        col[i] = None
        return False
    return bt(0)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('l', type=int); ap.add_argument('--s', type=int); ap.add_argument('--p', type=int)
    ap.add_argument('--const-ok', action='store_true'); ap.add_argument('--nosym', action='store_true')
    ap.add_argument('--dimacs')
    a = ap.parse_args()
    cnf, pool, N, s, p = build(a.l, a.s, a.p, nonconst=not a.const_ok, symbreak=not a.nosym)
    print(f"l={a.l} N={N} s={s} p={p}: vars={pool.top} clauses={len(cnf.clauses)}", flush=True)
    if a.dimacs:
        cnf.to_file(a.dimacs); print('wrote', a.dimacs); sys.exit()
    from pysat.solvers import Cadical153
    import time; t = time.time()
    with Cadical153(bootstrap_with=cnf.clauses) as S:
        r = S.solve()
        print('SAT' if r else 'UNSAT', f'{time.time() - t:.1f}s', flush=True)
        if r:
            L = decode(S.get_model(), pool, N, p)
            print('lists:', L)
            print('independent brute-force colourable?', colourable_bruteforce(L),
                  '| all identical?', all(x == L[0] for x in L))
