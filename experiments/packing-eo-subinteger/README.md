# `packing-eo-subinteger` — sub-integer corner-coordinate relaxation for Erdős–Oler

Companion code for
[`problems/circle-packing-equilateral-triangle/attacks/eo-subinteger-relaxation/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-subinteger-relaxation/).
Python standard library only; exact rational arithmetic (`fractions.Fraction`) in every decision.
Floats appear only inside the LP *search*; every conclusion is re-derived exactly.

**Normalisation: separation 1, triangle side $a$ (Oler).** The repo's certificates use separation 2
and side $d = 2a$; `controls.py` halves them on load.

## One command each

```bash
python3 controls.py                # K3: capacities vs certificates and lattices; Lemma P
python3 proof_k4.py                # the k=4 certificate, re-checked outside the LP pipeline
python3 scan.py 4 3,4,6            # LP bound at k=4 on the a/M grids
python3 astar.py 5 6               # how far up in a the relaxation still certifies
python3 run.py 3 4                 # integer vs sub-integer thresholds, both deltas, to out/report.txt
```

Nothing is seeded or random; every run is deterministic.

## Files

| file | what |
|---|---|
| `geom.py` | corner coordinates, exact polygons, and the capacity toolkit: diameter, Lemma D (circumradius), star cover, subdivision/independent-set, Oler, segment |
| `lp.py` | fractional-cover LP (two-phase simplex, perturbed RHS) plus exact verification of a cover |
| `run.py` | cells, boxes, capacity cache by congruence class, dominance pruning, per-level driver |
| `scan.py`, `astar.py` | threshold-grid scan; bisection for the largest $a$ still certified |
| `controls.py` | kill-criterion K3, and the independent re-verification of Lemma P |
| `proof_k4.py` | standalone re-check of the $k=4$ four-piece cover, uniform in $a$ |
| `out/` | transcripts |

## Two things a reader should check first

1. **No $d(n)$ value enters any capacity.** The literature table appears once, in the validation
   row of the attack's §3, where it checks the tool from outside. This is the guard that
   `FINDINGS.md` (2026-08-21) exists for.
2. **Capacities are upper bounds and are falsifiable.** `controls.py` counts real separated
   configurations against every box; that is how the segment bug in `capacity` was found.
