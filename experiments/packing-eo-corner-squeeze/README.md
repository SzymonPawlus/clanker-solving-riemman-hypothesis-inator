# `packing-eo-corner-squeeze`

Exact computations for [`problems/circle-packing-equilateral-triangle/attacks/eo-corner-squeeze/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-corner-squeeze/).

**Status of everything produced here: `numerical` / `sketch`.** No bound on $s(n)$, upper or
lower, is claimed. Nothing enters `results/`.

## One command

```bash
cd experiments/packing-eo-corner-squeeze
python3 run.py             # controls + certificate validation + k = 4, 5, 6   (~3 min)
python3 run.py --with-k7   # adds k = 7                                         (longer)
```

Python standard library only. No seeds matter except `find_feasible_random`'s, which is pinned
(`seed=20260821`) and is only a shortcut: every reported witness is re-verified against every
constraint by `relax.check_solution`, and the exhaustive `relax.feasible` reaches the same verdict.
Transcript: [`out/report.txt`](out/report.txt). Its section 1b was appended by a separate
invocation (marked in the file) after `run.py` grew that section; everything else is one run.
`out/run.log` is raw stdout and may be from a partial re-run — `out/report.txt` is authoritative.

## Files

| file | what it is |
|---|---|
| `exactiv.py` | rational intervals with outward rounding, written independently of `../packing-oler-slack/exact.py`; cross-checked against its `sqrt_bounds` on 2000 rationals |
| `geom.py` | corner-coordinate geometry. Regions are intersections of half-planes in $(u_A,u_B)$; areas are **exactly rational** after Oler's $2/\sqrt3$ weighting, only edge lengths become intervals. Also the $d(n)$ table and the capacity function |
| `lemmas.py` | Lemma P (the projection bound) and the Viviani/CIO/capacity aggregate accounting, checked exactly |
| `relax.py` | builds the corner-occupancy relaxation and searches it for an integer point |
| `validate.py` | K2/K3 controls: every exact certificate in the repo tested against every computed capacity |
| `tighten.py` | how much sharper the capacities would have to be: least uniform $\tau$ making the relaxation infeasible |
| `run.py` | driver |

## Normalisation

Oler normalisation throughout: **minimum separation 1**, containing triangle of side $a$. The
repo's certificates use separation 2 and side $2a$, so `validate.py` halves every coordinate on
load. Getting this backwards is the standard way to be wrong here.

## The circularity guard — read this before trusting any verdict

`geom.EXCLUDE` removes $d(T(k)-1)$ from the cited $d$ table whenever level $k$ is under test,
because $d(T(k)-1) = k-1$ **is** the Erdős–Oler statement at level $k$. Without the guard the
whole-triangle box capacity silently imports the answer and the relaxation reports "infeasible"
at every $k$ — which is exactly what the first version of this code did. Values at levels
$< k$ are kept: using Erdős–Oler at $k-1$ to study $k$ is induction, not circularity.
