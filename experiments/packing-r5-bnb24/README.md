# packing-r5-bnb24 — active-region interval branch and bound (round-4 proposal AI)

**Claim kind: OPTIMALITY / lower bound only.** This directory produces statements of the
form "no `n` points at pairwise distance `>= 2` lie in the closed equilateral triangle of
side `d`", for an explicit **rational** `d` — i.e. `d(n) > d`, equivalently
`s(n) > d + 2*sqrt(3)`. It produces no packing and claims no construction.

**Status: `numerical`.** The exhaustion is exact integer arithmetic with no tolerance
anywhere, but per repo `RULES.md` §3 a computational claim that has not been
independently reimplemented by the other model family is `numerical` and is not
assumable.

## Question

Does per-point **active-region propagation** — the ingredient the repo's own dyadic
interval B&B (`experiments/circle-packing-bnb`, issue #28 / PR #56) lacked — get past
the combinatorial wall that killed it? PR #56's own calibration bar is `d(12) > 6.95`.

## Method (one paragraph; the full statement is in `arbb/search.py`'s docstring)

Fix the level-`L` dyadic subdivision of `T_d` into `4^L` closed cells of side
`h = d/2^L < 2`. Any `n` points at pairwise distance `>= 2` give `n` *distinct* cells
whose **maximum** separations are all `>= 2`, i.e. an independent set of size `n` in the
conflict graph `G_L`. So `alpha(G_L) < n` implies `d(n) > d`. The search decides
`alpha(G_L) >= n` exactly, using

* **tile forcing** — a dyadic cell of side `< 2` is a clique, so it holds at most one
  point; when the number of tiles still alive equals the number of points still to
  place, every one of them is occupied;
* **active-region propagation** — for an occupied tile with active region `D`, every cell
  conflicting with *every* cell of `D` is deleted globally; run to fixpoint;
* a **hierarchical occupancy/area bound** from Oler's inequality (`cited`) applied to
  cell centroids;
* **tile-structured branching** — one tile is refined at a time down the dyadic tree, so
  the product over tiles of sub-positions is never enumerated. That product is exactly
  what PR #56 enumerated.

## Arithmetic

Every accept/reject decision is an **integer** comparison. For a lattice displacement
`a*u + b*v` with `u = (h,0)`, `v = (h/2, h*sqrt(3)/2)`, `|a*u+b*v|^2 = h^2(a^2+ab+b^2)`,
so with `d = p/q` the conflict test is `p^2 * maxQ < 4 * q^2 * 4^L` between Python
arbitrary-precision integers. The only place any irrational enters is the *capacity*
bound, where a rational **over**-estimate of `1/sqrt(3)` is used so that the capacity is
over-estimated — the sound direction. No float is consulted anywhere.

## Reproduce

```
python3 validate.py        # soundness controls (must pass before any bound is believed)
python3 crosscheck.py      # adjacency recomputed independently in Q(sqrt3)  (part B is
                           # a glucose4 re-decision; its cardinality encoding is large,
                           # see the attack README for why it was abandoned)
python3 crosscheck2.py     # verdicts re-decided by a second, independent MIS search
python3 run.py cal '[[12,71,10,5]]' 0 400     # the headline n=12 refutation, ~55 s
python3 run.py n24 '[[24,107,10,7]]' 0 400    # the n=24 push (build ~90 s, 2.2 GB)
```

`run.py <tag> <json list of [n,p,q,L]> <node_budget|0> <seconds>` checkpoints every
verdict to `out/<tag>.json` as soon as it is produced. The search is deterministic: no
randomness, no seeds; `(n, p, q, L)` fixes the node count bit for bit.

Python 3.11.15, numpy 2.4.6, python-sat (`pysat`) for the cross-check only.

## Files

| file | what |
|---|---|
| `arbb/geom.py` | dyadic cells, exact integer conflict test, dyadic ancestor maps |
| `arbb/search.py` | the branch and bound; its docstring states the relaxation lemma |
| `validate.py` | control 1 (known optima survive), control 2 (never UNSAT where feasible) |
| `crosscheck.py` | adjacency recomputed in `Q(sqrt3)` from Cartesian coordinates |
| `crosscheck2.py` | verdicts re-decided by a second, independently written MIS search |
| `run.py` | driver with per-case checkpointing |
| `out/*.json` | every verdict produced, with node and propagation counters |
