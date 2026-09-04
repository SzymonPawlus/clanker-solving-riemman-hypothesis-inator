# `packing-eo-covering-bound` — lower bounds on the diameter-<1 covering number of T_a

Companion code for
[`problems/circle-packing-equilateral-triangle/attacks/eo-covering-bound/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-covering-bound/).

Reproduce every decision with

```
sh experiments/packing-eo-covering-bound/run.sh
```

Python standard library only; no seeds are needed for any *decision* (the float searches that
propose configurations do pin their seeds, and their output is checked in under `out/`).

| file | role | arithmetic |
|---|---|---|
| `exactlib.py` | triangular coordinates; containment + distance as rational comparisons | exact |
| `bound_area.py` | Theorem 1, the corner-refined isodiametric floor | exact (certified `pi`, `sqrt 3` enclosures) |
| `verify.py` | snaps float hypotheses to rationals and certifies the separated sets | exact |
| `recheck.py` | re-checks the same certificates through cartesian coordinates | exact + 60-digit decimals |
| `gap.py` | the chi-vs-alpha tool — the only method here that could reach 27 | exact |
| `optimize.py`, `feas.py`, `shrink.py`, `hop.py`, `pairs.py`, `cornerscreen.py`, `seed26.py` | float search; **hypothesis generators, nothing more** | float |

`out/certificates.json` holds the certified separated sets as exact rationals.
