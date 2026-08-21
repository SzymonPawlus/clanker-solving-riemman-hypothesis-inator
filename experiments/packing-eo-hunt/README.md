# packing-eo-hunt

**Status: `numerical`.** Everything the search in this directory produces is a floating-point
*construction hypothesis*. It is not a certificate and it is never an optimality claim
(problem [`../../problems/circle-packing-equilateral-triangle/RULES.md`](../../problems/circle-packing-equilateral-triangle/RULES.md) §1).
The exception is `exact_check.py` / `verify3.py`, which are exact rational arithmetic and decide.

Writeup: [`../../problems/circle-packing-equilateral-triangle/attacks/eo-counterexample-hunt/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-counterexample-hunt/).

## Question

Erdős–Oler is open for $k \ge 7$ and the repo had only ever tried to *prove* it. This directory
tries to **break** it: find $\Delta(k)-1$ points at pairwise distance $\ge 1$ in an equilateral
triangle of side $a < k-1$, for $k = 7, 8, 9, 10$.

Normalisation: the optimiser places $n$ points in the **unit** equilateral triangle
$\mathrm{conv}\{(0,0),(1,0),(\tfrac12,\tfrac{\sqrt3}{2})\}$ maximising the minimum pairwise
distance $m$; the separation-1 side is $a = 1/m$. So

    EO(k) is false  <=>  m(Delta(k) - 1) > 1/(k-1).

The repo's certificates use separation 2 and side $d = 2a$. That factor of 2 is the likeliest
place to fool yourself; every number here is in the separation-1 $(a, m)$ normalisation.

## Layout

| file | what |
|---|---|
| `hunt.py` | search core: SLSQP local step, five seed families, basin-hopping moves, local-optimum census |
| `exact_check.py` | **the gate.** Two independent exact checkers — barycentric over $\mathbb{Q}$, and Cartesian over $\mathbb{Q}(\sqrt3)$ |
| `verify3.py` | a third from-scratch exact checker, sharing no representation with either of the above |
| `run.py` | driver: `bench`, `validate`, `hunt` |
| `control_n26.py` | the positive control — $n = 26$ genuinely fits below side 6, so the gate must say yes |
| `insert.py` | the targeted attack: take a $\Delta(k)-2$ packing below side $k-1$, insert one more point |
| `analyze.py` | collates `out/*.json` into `out/report.txt` |
| `tables.py` | emits the writeup's markdown tables from `out/*.json` — no number is hand-transcribed |

## Reproduction

```sh
uv run run.py bench                                        # cost model
uv run run.py validate                                     # PROVEN cases k=2..6; must pass first
uv run control_n26.py 300                                  # positive control + exact certificate
uv run verify3.py                                          # third checker on that certificate
uv run negative_control.py                                 # the gate must REJECT a 1e-12 near-miss
uv run run.py hunt --k 7 --seconds 1800 --seed 20260821 --tag a
uv run run.py hunt --k 7 --seconds 1800 --seed 770021  --tag b
uv run run.py hunt --k 8 --seconds 1800 --seed 20260821 --tag a
uv run run.py hunt --k 9 --seconds 900  --seed 20260821 --tag a
uv run run.py hunt --k 10 --seconds 900 --seed 20260821 --tag a
uv run insert.py 7  150 320 424242
uv run insert.py 8  180 360 515151
uv run insert.py 9  220 400 616161
uv run insert.py 10 240 420 717171
uv run analyze.py && uv run tables.py
```

Seeds are pinned; **wall-clock budgets are not reproducible** by construction (`--seconds` cuts a
run short), so re-running gives a different solve count and the same conclusion, not identical
JSON. Library versions are recorded in every checkpoint's `env` field.

## Discipline this directory tries to enforce

- The gate was written and self-tested **before** any search, not after a promising number appeared.
- Every reported $m$ is re-measured on points *projected into the triangle*, never taken from the
  solver's own variable — SLSQP is allowed to sit a hair outside the feasible set.
- Any solve exceeding $1/(k-1) + 10^{-9}$ **halts the sweep** and goes to the exact gate before
  anything else runs.
- `run.py validate` reproduces the cases the literature has settled ($k \le 6$) before any target
  run. An optimiser that beats a proven case is broken, not brilliant.
- Checkpoints are written every 20 s via atomic rename, so a killed run still produced something.

## Provenance

The SLSQP local step reuses the formulation of `experiments/circle-packing-search` (issue #9),
including its rule of re-measuring the achieved $m$ rather than trusting the solver's. The seed
families, the census, the exact gate, the positive control, the insertion attack and the analysis
are new here. Reference values for $d(n)$ are read from
`experiments/circle-packing-search/reference.py` (Graham–Lubachevsky 1995; Friedman's Packing
Center) and nothing in this directory recomputes them.
