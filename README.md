# complement(C₉) is strongly 5-chromatic-choosable

A computer-assisted proof of the case ℓ = 5 of Conjecture 9 in

> A. Fiujlaali and J. McDonald, *Restricting odd antiholes in critical graphs via list coloring*, [arXiv:2610.14241](https://arxiv.org/abs/2610.14241) (2026).

**Theorem.** If every vertex of the odd antihole complement(C₉) gets a list of 4 colours, the graph can be properly coloured from those lists unless all nine lists are identical.

**Consequence.** By Theorem 10 of the paper, Conjecture 3 of the paper holds whenever Δ = k + 1. In other words, an odd-hole-free k-critical graph with maximum degree k + 1 that contains a 9-vertex odd antihole is that antihole. This was previously known for k ≤ 6. It is now known for all k, including the paper's first open case (k, Δ) = (7, 8).

The paper proves the case where all lists come from one common 5-set (Theorem 8). The new content is all larger palettes.

**→ Read [NOTE.md](NOTE.md)** for the mathematics: the reduction via Hall's theorem, the palette bound, the encoding, and the full verification record.

## How it works, in one paragraph

Colour classes of complement(C₉) are single vertices or adjacent pairs of the 9-cycle. So a colouring is a matching of C₉ plus distinct colours for the resulting blocks. By Hall's theorem, "not colourable" means that for every one of the 76 matchings, some set of blocks has fewer available colours than blocks. That is a purely existential condition, so the existence of a counterexample is a single SAT instance. The instance is **unsatisfiable**, and the refutation proofs are **verified by drat-trim**.

## Reproduce

Requires Linux, WSL or macOS with python3, pip, git, gcc and make. It takes about 2 minutes:

```sh
bash scripts/verify.sh   # regenerate the instances, check hashes, solve, verify proofs with drat-trim
bash scripts/tests.sh    # controls: l=3,4 UNSAT; expected counterexamples found when they should exist; brute-force agreement
```

Expected output of `verify.sh`, after the hash check reports `OK` twice:

```
== drat-trim l5p20
s VERIFIED
== drat-trim l5p36
s VERIFIED
```

## Contents

| Path | What |
|---|---|
| `NOTE.md` | Mathematical write-up and verification record |
| `src/skcc.py` | SAT encoding for complement(C_{2ℓ−1}) with (ℓ−1)-lists, any ℓ, plus a brute-force list-colouring checker |
| `src/proof.py` | Generates an instance and a DRUP proof (Glucose 4 via python-sat) |
| `src/rupcheck.c` | A small independent forward RUP proof checker, used as a second check |
| `src/semcheck.py` | Encoding vs. brute force on random fixed list assignments |
| `cnf/` | The two instances (palette 20, which covers all cases by Lemma 3; and palette 36, the absolute maximum) with SHA-256 sums |
| `results/` | drat-trim logs from the independent verification run |
| `scripts/` | `verify.sh` and `tests.sh` |

The proofs (~130 MB each) are not stored; `verify.sh` regenerates them.

## Credits

Developed with the assistance of Claude (Anthropic). All results were verified as described in NOTE.md. Thanks to A. Fiujlaali and J. McDonald for the conjecture and the reduction (their Theorem 10) that makes this case meaningful.

## License

Code: MIT (see `LICENSE`). Text (`README.md`, `NOTE.md`): CC BY 4.0.
