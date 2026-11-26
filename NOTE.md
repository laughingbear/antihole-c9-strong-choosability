# The odd antihole complement(C₉) is strongly 5-chromatic-choosable

**Summary.** We verify the case ℓ = 5 of Conjecture 9 of Fiujlaali and McDonald [FM]: for every assignment of 4-element lists to the vertices of complement(C₉), the graph is list-colourable unless all nine lists are identical. By [FM, Theorem 10] this settles their Conjecture 3 whenever Δ = k + 1. The proof reduces the statement to a finite SAT instance via Hall's theorem; the instance is unsatisfiable, and its refutation proofs are checked by drat-trim.

## 1. Statement

Write G = complement(C_N) with vertices 0, …, N−1 taken mod N, where i and j are adjacent in G iff they are not consecutive on the cycle. A graph is *strongly ℓ-chromatic-choosable* [KM] if χ(G) = ℓ and every (ℓ−1)-assignment L for which G is not L-colourable has all lists equal.

**Conjecture 9 [FM].** For every ℓ ≥ 3, complement(C_{2ℓ−1}) is strongly ℓ-chromatic-choosable.

The case ℓ = 3 is the classical fact about odd cycles with 2-lists. [FM, Theorem 8] proves the conjecture when all lists are subsets of one common ℓ-set.

**Theorem.** complement(C₉) is strongly 5-chromatic-choosable.

**Corollary.** [FM, Theorem 10] shows that Conjecture 9 for ℓ implies [FM, Conjecture 3] for every pair (k, Δ) with Δ − k = ℓ − 4. Hence: *if G is an odd-hole-free k-critical graph with maximum degree Δ = k + 1 that contains an odd antihole of length 9, then G = complement(C₉).* [FM, Theorem 4] had established this for k ≤ 6, so the corollary is new for every k ≥ 7, including the case (k, Δ) = (7, 8) singled out in [FM].

## 2. Reduction to a finite statement

Let N = 9, G = complement(C₉), and let L assign a 4-set to each vertex. We have χ(G) = 5: a colour class is an independent set of G, so by Lemma 1 it has at most 2 vertices, which forces at least 5 classes, and 5 suffice.

**Lemma 1 (colour classes).** The independent sets of G are exactly the cliques of C₉: ∅, singletons, and consecutive pairs {i, i+1}.

So an L-colouring of G is the same as a matching M of C₉ (the colour classes of size 2) together with an injective choice of colours for the *blocks* of M, namely the matched pairs and the unmatched vertices. The allowed colours are L(v) for an unmatched v, and L(i) ∩ L(i+1) for a matched pair {i, i+1}. Distinct blocks must get distinct colours, since any two vertices in different blocks are either adjacent in G or would merge into a larger class.

**Lemma 2 (Hall).** G is not L-colourable if and only if, for each of the 76 matchings M of C₉, there is a nonempty set X of blocks of M such that the union of the allowed colours over X has fewer than |X| elements.

*Proof.* Combine Lemma 1 with Hall's theorem for systems of distinct representatives. ∎

**Lemma 3 (palette bound).** If G is not L-colourable, then |⋃_v L(v)| ≤ 20.

*Proof.* Apply Lemma 2 with M = ∅, where every block is a single vertex. This gives a set X of vertices with |L(X)| ≤ |X| − 1, so |X| ≥ 5 because every list has 4 colours. The remaining 9 − |X| vertices contribute at most 4 colours each, so the palette has at most (|X| − 1) + 4(9 − |X|) = 35 − 3|X| ≤ 20 colours. ∎

Independently of Lemma 3, a palette can never exceed 9 · 4 = 36 colours. We solve both p = 20 and p = 36.

## 3. SAT encoding (`src/skcc.py`)

- **Variables:** x[v, c] means "c ∈ L(v)", for v < 9 and c < p.
- **List size:** exactly 4 colours per vertex, via a sequential-counter cardinality encoding.
- **Hall violators:** for each matching M, selectors y_B for its blocks and indicators z_c for colours, with clauses (y_B ∧ ⋀_{v∈B} x[v, c]) → z_c and the cardinality constraint Σ y_B + Σ ¬z_c ≥ p + 1, i.e. |X| ≥ |colours(X)| + 1.
- **Symmetry breaking**, valid because colours can be renamed:
  - L(0) = {0, 1, 2, 3};
  - colours ≥ 4 are numbered in order of first appearance along vertices 0..8. The constraint: if colour c + 1 occurs on some vertex ≤ v, then so does colour c.

  Every assignment can be relabelled to satisfy both.
- **Non-identical lists:** given L(0) = {0, 1, 2, 3}, "not all lists equal" is equivalent to "some vertex v ≥ 1 has a colour ≥ 4".

A satisfying assignment would therefore be exactly a counterexample to the Theorem. Both instances are **unsatisfiable**.

## 4. Verification

| Check | Result |
|---|---|
| p = 20 instance (`cnf/l5p20.cnf`, 12,290 vars, 31,551 clauses) | UNSAT (CaDiCaL 1.5.3 in 50 s; Glucose 4 in 25 s) |
| p = 36 instance (`cnf/l5p36.cnf`, 21,650 vars, 56,975 clauses) | UNSAT (CaDiCaL 53 s; Glucose 25 s) |
| DRUP proofs from Glucose, checked by **drat-trim** (commit 2e3b2dc) | p = 20: **s VERIFIED** (208,691 of 731,977 lemmas in core, 22 s). p = 36: **s VERIFIED** (223,344 of 753,052 lemmas, 25 s) |
| Same proofs, checked by an independent forward RUP checker (`src/rupcheck.c`) | VERIFIED. The checker accepts a genuine ℓ = 4 proof and rejects a bare empty clause, a truncated proof, and a proof against a satisfiable variant |
| Encoding vs. an independent backtracking list-colourer, with lists fixed by solver assumptions | 9,000 random assignments (ℓ = 4, 5; palettes 4–9): 0 disagreements (2,036 non-colourable cases) |
| Positive controls | Allowing identical lists gives SAT (identical, non-colourable). Lists of size ℓ − 2 give SAT with non-identical non-colourable counterexamples, confirmed by brute force |
| ℓ = 3, 4 | UNSAT |
| Symmetry breaking removed, ℓ = 5, p = 6, 7 | UNSAT |

The instances were generated independently on two machines with identical SHA-256 hashes; see `cnf/SHA256SUMS` and `results/VERIFY.txt`. To reproduce everything, run `scripts/verify.sh` (about 2 minutes).

## 5. Remarks

- **ℓ = 6** would settle Δ = k + 2. The same reduction applies (palette ≤ 17, using that every colour must lie in ≥ 2 lists, by Noel–Reed–Wu). Palettes up to 9 colours are UNSAT, but run time grows roughly tenfold per added colour, and we did not complete the general case.
- **AI assistance.** The reduction, encoding and verification code were developed with the assistance of Claude (Anthropic). All claims were checked as described above.

## References

- [FM] A. Fiujlaali and J. McDonald, *Restricting odd antiholes in critical graphs via list coloring*, arXiv:2610.14241 (2026).
- [KM] H. Kaul and J. A. Mudrock, *Criticality, the list color function, and list coloring the Cartesian product of graphs*, arXiv:1805.02147.
- [NRW] J. A. Noel, B. A. Reed and H. Wu, *A proof of a conjecture of Ohba*, J. Graph Theory (2015), doi:10.1002/jgt.21819; arXiv:1211.1999.
- M. J. H. Heule, *drat-trim*, https://github.com/marijnheule/drat-trim.
