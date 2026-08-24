# packing-r3-gridmis — grid-rounding independent-set refutation

**Question.** Can "no $n$ points at pairwise distance $\ge 2$ in the equilateral triangle $T_d$"
be turned into a *finite* combinatorial refutation, checkable by an external proof checker, that
is strong enough to beat Oler's floor $d(16) \ge \sqrt{129}-3 = 8.357817\ldots$?

**Answer.** The reduction works and is sound (two-sided calibration at $n=12$ passes), but it
does not reach the Oler floor at $n=16$ within an hour of compute. The write-up, the perturbation
lemma it rests on, and the quantified ceiling are in
[`../../problems/circle-packing-equilateral-triangle/attacks/r3-gridmis/README.md`](../../problems/circle-packing-equilateral-triangle/attacks/r3-gridmis/README.md).

**Status of everything here:** `numerical`, except the DRAT proofs in `out/*.drat`, which are
machine-checked refutations of the corresponding CNF — and which still depend on a `sketch`
lemma, so nothing here is assumable (`RULES.md` §3).

**This is a lower-bound (optimality-side) attack. It contains no packing and claims no
construction.**

## Method

For rational $d, g, r$ with $r \ge g/\sqrt3$ and $r<1$, build the graph $G$ whose vertices are the
points of the spacing-$g$ triangular lattice lying in the $r$-relaxed triangle
$T_d^{(r)} = T_{d+2\sqrt3 r}$, joined when their distance is $< \rho := 2-2r$. Lemma 1 of the
write-up says $\alpha(G) < n \Rightarrow d(n) > d$. Every geometric comparison is exact
(`fractions.Fraction` + integer arithmetic on squared distances); no float ever decides anything.

$\alpha(G) < n$ is then attacked three ways:

* `gridmis/mis.py` — an exhaustive branch and bound (greedy clique-partition bound). Complete,
  but its `UNSAT` is *solver output*, not a proof.
* `gridmis/satproof.py` — a ~20-line CNF encoding (one variable per vertex, one binary clause per
  edge, one `pysat` cardinality constraint $\sum_v x_v \ge n$) solved by glucose4. Its `UNSAT` is
  also solver output, **but** the DRAT proof it emits is checked by `drat-trim`, which this
  project did not write. That is the only machine-checked artifact here.
* witnesses: when an independent set of size $n$ exists it is returned and re-verified exactly.
  A witness is self-certifying and shows the method *cannot* refute that $d$.

## Layout

| file | what |
|---|---|
| `gridmis/lattice.py` | exact construction of $G(n,d,g,r)$; `covering_radius_bound` |
| `gridmis/mis.py` | exhaustive independent-set decision (branch and bound) |
| `gridmis/satproof.py` | CNF encoding, glucose4, DRAT emission, `drat-trim` invocation |
| `test_lemma.py` | randomised soundness tests (see below) |
| `sweep.py`, `sweep2.py`, `push.py`, `proofs.py` | the runs; each checkpoints JSON after every instance |
| `run.py` | **the single reproduce command** |
| `out/` | all results (`*.json`, `*.log`, `*.cnf`, `*.drat`) |

## Reproduce

```bash
cd experiments/packing-r3-gridmis
python3 run.py            # ~15 min on 4 cores; writes out/reproduce.json and prints a summary
```

`run.py` reruns, in order: the randomised soundness tests; the tiny known-answer validations;
the two-sided $n=12$ calibration; the $n=12$ and $n=16$ threshold sweeps at the grids that
finished inside the budget; and one DRAT-checked refutation end to end. It is deterministic apart
from the fixed seeds in `test_lemma.py` (1, 2, 3), which are pinned in the file.

The full sweeps as actually run (longer than `run.py`) are:

```bash
python3 sweep.py  12 90 out/sweep12.json  1/4,1/5,1/6,1/8,1/10 60/10,62/10,64/10,66/10,68/10,70/10,72/10,74/10,76/10,78/10
python3 sweep2.py 16 15 out/sweep16a.json 1/4,1/5,1/6,1/8      74/10,78/10,80/10,82/10,84/10,85/10,86/10,88/10,90/10,92/10,94/10
python3 push.py   16 1/5 out/push16_g5.json 8,81/10,82/10,83/10,84/10
python3 push.py   16 1/6 out/push16_g6.json 8,81/10,82/10,83/10,84/10
python3 proofs.py
```

## Versions

Python 3.11.15; `python-sat` 1.9.dev15 (glucose4); `drat-trim` built from
`https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c` (fetched
2026-08-23), `gcc -O2`. No numpy/scipy/sympy is used in any soundness-critical path — the
geometry is stdlib `fractions` and integers only.

To rebuild the checker:

```bash
curl -sSL -o drat-trim.c https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c
gcc -O2 -o /usr/local/bin/drat-trim drat-trim.c
```

If `drat-trim` is absent, `solve_with_proof(..., check=False)` still writes the `.drat` file and
the run reports `drat_verified: null` rather than silently claiming verification.

## Soundness tests (`python3 test_lemma.py`)

1. **containment** — the exact rational predicate is compared against a separately written float
   predicate on every candidate lattice point for four $(d,g)$ pairs; points within $10^{-9}$ of a
   boundary are skipped because only there may the two legitimately differ. 0 mismatches.
2. **covering radius** — 20 000 uniform samples of $T_d$ per case; the nearest lattice point is
   always within the rational $r$ returned by `covering_radius_bound`.
3. **the lemma end to end** — 1 199 random feasible point sets (random sequential adsorption at
   separation $\ge 2$ inside $T_d$) are snapped to the lattice, and all three conclusions of
   Lemma 1 are checked: the snapped points lie in $V$ (boundary trap), they are distinct
   (collapse trap), and no pair is an edge. 0 failures.

Test 3 is the one that matters: a bug in the relaxation constant or in $\rho$ would show up as a
snapped configuration that is *not* an independent set, which is exactly the unsoundness that
would let the method "prove" a false statement.
