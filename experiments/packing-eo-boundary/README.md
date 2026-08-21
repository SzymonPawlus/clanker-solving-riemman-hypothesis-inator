# packing-eo-boundary — the Erdős–Oler boundary count, exactly

Companion code for
[`problems/circle-packing-equilateral-triangle/attacks/eo-boundary-counting/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-boundary-counting/).
Read that README first; this file only says how to run the code and what it does and does not
decide.

## Run

```
python3 experiments/packing-eo-boundary/run.py
```

One command, no arguments, no configuration, **Python standard library only** (tested on 3.11).
Nothing is downloaded and nothing outside this directory is read. Output goes to stdout and to
[`out/report.txt`](out/report.txt); the run takes a couple of minutes, almost all of it in the two
float searches.

## Files

| File | What it is |
|---|---|
| `q3.py` | exact arithmetic in $\mathbb{Q}(\sqrt3)$ plus exact planar predicates (orientation, containment, convex hull, hull-boundary count, polygon area). Written for this experiment and **deliberately independent** of `experiments/packing-oler-slack/exact.py` — two checkers that share a number type share its bugs. |
| `run.py` | the six sections of the attack, in order. |
| `out/report.txt` | the transcript, regenerated on every run. |

## What is exact and what is not

**Exact — every decision.** Signs, containments, separations, hull incidences, areas and every
comparison that produces a conclusion are computed in $\mathbb{Q}$ or $\mathbb{Q}(\sqrt3)$ with
`fractions.Fraction`. An element $p + q\sqrt3$ is zero iff $p = q = 0$, so sign tests terminate
exactly. The arguments were arranged so that **no edge length is ever compared to anything** —
only squared distances, areas, and perimeters that happen to be rational (the triangular lattice's
hull perimeter is exactly $3(k-1)$) — which removes any need for interval arithmetic.

Assertions in `run.py` are part of the check, not decoration: separations, containments and the
hull-boundary counts are asserted, so a wrong configuration aborts the run rather than printing a
plausible table.

**Float — two searches, no decisions.** Section 3 samples corner clearances looking for a
counterexample to Lemma P1; section 3b is a multistart local search for $a_{\mathrm{conv}}(b)$.
Both are labelled `numerical` in the write-up, both are *searches for counterexamples*, and
nothing downstream depends on either. Seeds are fixed in the source (`seed=20260821` and
`seed=1`), so both are reproducible.

## Sections

1. the exact Oler window for $k = 7$, and the per-$k$ table showing that the required gain is one
   point for every $k$ (and what the window becomes if the integrality of $n$ is not used)
2. an exact family attaining $3\lfloor a\rfloor$ points on $\partial T$, for nine values of $a$
3. float probe: can more than $3\lfloor a\rfloor$ points sit on $\partial T$? (no)
3b. float probe of the hull reading, $a_{\mathrm{conv}}(b)$ for $b = 3,\dots,10$
4. exact witnesses: hypothesis H fails at the triangular lattice itself, $k = 3,\dots,7$
5. exact witnesses for Theorem T1 (no count-based boundary term exists), plus two independent
   corroborations in the opposite regime
6. the corner-clearance lemma: the exact thresholds $t_7 = \frac{-3+\sqrt{33}}{6}$ and the
   $k$-independent Corollary C1

## Normalisation

Separation **1**, triangle side **$a$** (Oler's normalisation). The repo's certificates use
separation 2 and side $d = 2a$; this experiment does not read them, so there is nothing to
convert and no opportunity for the standing normalisation trap on this problem.
