# packing-eo-verify — independent checkers for the Erdős–Oler lemmas

Companion code for
[`problems/circle-packing-equilateral-triangle/attacks/eo-verification/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-verification/).

Everything here was written from the problem statement, as problem `RULES.md` §3 requires of a
verification pass: none of the authors' checkers was read, imported, adapted or rerun. The single
exception, permitted by the task brief, is the `sqrt_bounds` idea (rational enclosure of a square
root via `math.isqrt`) read from `experiments/packing-oler-slack/exact.py`.

## Run

```
./run.sh
```

Python standard library only. 101 checks; non-zero exit if any fails. No floats decide anything;
no seed affects any verdict (the randomised sweeps are seeded only so the counts reproduce).

## Arithmetic

`surd.py` implements `Surd`: a finite formal sum $\sum_f c_f\sqrt f$ over squarefree integers $f$
with rational coefficients. Those radicals are linearly independent over $\mathbb Q$, so **equality
is decided exactly** by comparing coefficient dictionaries; order comparisons fall back to interval
evaluation with escalating precision, which terminates because a nonzero `Surd` is bounded away
from zero.

All geometry is in **lattice coordinates** $(u,v) \mapsto (u + v/2,\ v\sqrt3/2)$. In these
coordinates:

- squared distance is $du^2 + du\,dv + dv^2$ — rational;
- Oler's area term $\frac{2}{\sqrt3}A$ is exactly the $(u,v)$-shoelace — rational;
- edge lengths are $\sqrt{\text{rational}}$ — the only irrational quantities anywhere.

So Oler's bound $B(P) = \frac2{\sqrt3}A(P) + \frac12 M(P) + 1$ is a `Surd` with no error at all,
and $T_a = \operatorname{conv}\{(0,0),(a,0),(0,a)\}$. Sanity: $B(T_a) = a^2/2 + 3a/2 + 1$, so
$B(T_6) = 28 = \Delta(7)$.

The corner "level" of a point is $(u+v,\ a-u,\ a-v)$ for the three corners; the closed corner
triangle of side $t$ at a corner is that level $\le t$.

## Files

| file | what it checks |
|---|---|
| `surd.py` | the number type, hulls, areas, perimeters, Oler's bound, the lattice |
| `shapes.py` | exact convex-polygon clipping, the $m^2$ cell subdivision, point-in-polygon, the Barrier gain |
| `check_partition.py` | Claim 1 — the partition identity, its edge cases, and the counterexample to the broad corollary |
| `check_corner_deficit.py` | Claim 3 — the Corner-Deficit Lemma, 4000 random exact configurations, the side condition's necessity and tightness |
| `check_barrier.py` | Claim 4 — Theorem 6 over ~10 000 convex cuts at $m=3..6$, the equality family, the non-convex counterexample |
| `check_cio_and_small.py` | Claims 2, 5, 6 — CIO/Corollary 4/§9's threshold, the 28 lattice deletions, Prop 5, the subdivision lemma, EO(3), the normalisation cross-check |
| `out/report.txt` | transcript of the full run |
