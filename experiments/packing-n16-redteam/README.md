# packing-n16-redteam — red-team audit code (worker R1, claude, 2026-08-22)

Write-up: `problems/circle-packing-equilateral-triangle/attacks/n16-redteam/README.md`.
Issue #97. Python standard library only. No network, no seeds, no tolerances.

| file | what it does |
|---|---|
| `q3.py` | exact arithmetic in Q(sqrt3): `p + q*sqrt3` with `Fraction` p, q, and an exact sign test |
| `check_cov2.py` | independent verification of the `n16-covering-2` headline certificate at `a = 1+2*sqrt3`. The 15 polygons are **hand-transcribed from that attack's README table**, not read from the author's code or JSON. Checks: 15 pieces; every vertex in T_a; every piece simple, strictly convex, ccw; all squared diameters (exactly 1); all 105 pairwise intersections have zero area by exact Sutherland-Hodgman clipping; areas sum exactly to area(T_a); a 1891-point rational grid probe. Exits non-zero on any failure. |
| `areas_traces.py` | per-piece Euclidean areas and per-side boundary trace lengths, cross-checked against `f(1) = pi/3 - sqrt3/4`, the exact half-plane area cap derived in `n16-covering-limit` §3 |
| `arith.py` | 40-digit `decimal` re-derivation of every number quoted in the campaign: the four headline values, all separation-1/2 conversions, the area ceilings, the gap arithmetic, and the rational bounds |
| `structure.py` | finding 1: the exact witness that a two-side piece can reach a side's middle, the repair that still gives `n_int <= 3` unconditionally, and the enumeration of the 33 layouts nothing proved excludes |
| `cmp_code.py` | confirms the hand-transcription in `check_cov2.py` agrees vertex-for-vertex with `experiments/packing-n16-covering-2/exact_1p2r3.py` |

```bash
python3 check_cov2.py && python3 areas_traces.py && python3 arith.py \
  && python3 cmp_code.py && python3 structure.py
```

Nothing here establishes any status: same model family as every author audited
(repo `RULES.md` §5).
