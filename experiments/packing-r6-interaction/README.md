# packing-r6-interaction

Code for `problems/circle-packing-equilateral-triangle/attacks/r6-interaction/`.

Normalisation everywhere: **separation 1**, container `T(a)` of side `a`; repo `d = 2a`,
`s = d + 2√3`. Coordinates `r = 4·area(conv E)/√3`, `M = perim(conv E)`, so Oler is
`n ≤ (r + M)/2 + 1`.

## One command that reproduces the paper numbers

```
cd experiments/packing-r6-interaction && python3 shapes.py && python3 jumps.py
```

Deterministic, exact/rational where it matters, a few seconds, no network, no seeds.

- `shapes.py` — steps 1 and 2 of the assignment. (a) Oler is exactly tight at every `Δ(k)`
  (`Fraction` arithmetic). (b) candidate **C2** matches Oler exactly at every `Δ(k)`. (c) C2's gain
  over Oler at the open `n`. (d) C2 at the `Δ(k)−1` family — it does **not** reach `a = k−1`.
  (e) the Jump Lemma shortfall, `→ 1` exactly. (f) the `k = 4` corner-deleted Oler equality case.
- `jumps.py` — the jump structure of `N(a)`, computed from the `cited` `s(n)` table in the problem
  `README.md`. Every jump of size 2 sits at `a = k − 1`; all others have size 1.

## The stochastic probe (`numerical`, heuristic, upper bounds only)

```
python3 rho_probe.py <n> <starts>          # e.g.  python3 rho_probe.py 16 300
```

Multistart SLSQP minimisation of `φ(E) = max(√r, M/3)` over free `n`-point configurations with all
`C(n,2)` separations `≥ 1`. Writes `out/rho_n<n>.json` (value, argmin `(r, M)`, coordinates).

This gives an **upper** bound on `ρ(n)`, i.e. it can only lower the measured ceiling of C2, never
raise it. Every returned configuration is rescaled so its minimum separation is exactly `1` before
its value is recorded, so no reported number comes from an infeasible configuration.

Recorded runs (seed `20260826`, 4-core box shared with other lanes, so seconds are upper bounds):

| `n` | starts | `ρ ≤` | argmin `(r, M)` | seconds |
|---|---|---|---|---|
| 9 | 300 | `2.828427 = 2√2` | `(8, 8)` corner-deleted trapezoid | 28 |
| 16 | 60 | `4.242641 = 3√2` | `(18, 12)` `3×3` lattice rhombus | 19 |

Both reproduce the Oler-tight-family value of `shapes.py` (c)/(d) and never improve on it.
