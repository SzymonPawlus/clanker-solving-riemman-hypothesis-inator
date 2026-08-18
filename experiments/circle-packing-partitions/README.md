# Exact partition certificates for circle-packing lower bounds

**Claim type: strict lower bound. Status: `numerical`.** This directory checks finite rational
partition certificates exactly. It does not prove optimality, and nothing here is assumable until
an independent checker or Lean reconstruction supplies the status required by the repository
rules.

Issue: [#27](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/27).

## The certificate implication

Use oblique coordinates

\[
  (u,v) \longmapsto u(1,0)+v(1/2,\sqrt3/2).
\]

The equilateral triangle of side `d` is then the rational simplex

\[
  T_d=\{(u,v):u\ge0,\ v\ge0,\ u+v\le d\},
\]

and squared Euclidean distance is the rational quadratic form

\[
  q(\Delta u,\Delta v)=\Delta u^2+\Delta u\Delta v+\Delta v^2.
\]

Suppose a certificate partitions `T_d` into exactly `n-1` closed convex polygons and every
polygon has diameter strictly less than 2. Any `n` points in `T_d` put two points into the same
cell, by pigeonhole, contradicting pairwise separation at least 2. Consequently

\[
  s(n)>d+2\sqrt3.
\]

This is only a lower bound. It says nothing about whether a matching packing exists.

## What the checker proves

`partitioncheck.py` accepts a certificate only after exact `fractions.Fraction` checks establish:

1. all scalars are bounded rational strings; decimal strings are rejected;
2. every cell is a simple, strictly convex, counterclockwise polygon contained in `T_d`;
3. every pair of cells has intersection area zero (shared edges and vertices are allowed);
4. the sum of cell areas equals the area of `T_d`;
5. there are exactly `n-1` cells;
6. the squared distance between every pair of vertices of each cell is strictly below 4.

For a convex polygon its diameter is attained by two vertices, so item 6 checks the whole cell.
Items 2--4 prove coverage: the finite union is a closed subset of `T_d`, its cells have disjoint
interiors, and its area equals `T_d`; a nonempty relative-open complement would have positive area.
This coverage step is load-bearing. Merely checking the area sum would be unsound because an
overlap could compensate for a hole.

The pairwise intersection-area test uses exact Sutherland--Hodgman clipping of convex polygons.
The implementation is intentionally dependency-free and uses no floating point.

## First calibrations

`certificates/n003-d1999-over-1000.json` divides `T_(1999/1000)` along the median into two
triangles. Both have squared diameter below 4, hence it certifies

\[
  s(3)>\frac{1999}{1000}+2\sqrt3.
\]

The known optimum has point-triangle side `d(3)=2`, so this is a deliberately simple certificate
within `1/1000` of the truth. It validates the representation and strict-inequality direction
before any optimiser is introduced.

`certificates/n004-d433-over-125.json` encodes Graham's three-cell centroid-to-side-midpoints
partition at the rational target `d=433/125`. Each cell has squared diameter

\[
  \frac{1}{3}\left(\frac{433}{125}\right)^2
  =\frac{187489}{46875}<4.
\]

Thus it certifies `s(4) > 433/125 + 2*sqrt(3)`, within about `0.000102` in point-triangle side of
the known exact optimum `d(4)=2*sqrt(3)`. This exercises a genuine three-cell planar complex with
a four-way mix of shared edges and a shared centroid, rather than only a single median cut.

The `n005` and `n006` fixtures use the four half-scale triangles and a refinement of one of them,
respectively, at `d=3999/1000`. They certify strict lower bounds within `1/1000` of the common
known point-triangle optimum `d(5)=d(6)=4`. Together the four fixtures reproduce Graham's simplest
box-principle calibration range using only rational coordinates.

Run:

```bash
python3 partitioncheck.py certificates/n003-d1999-over-1000.json
python3 partitioncheck.py certificates/n004-d433-over-125.json
python3 partitioncheck.py certificates/n005-d3999-over-1000.json
python3 partitioncheck.py certificates/n006-d3999-over-1000.json
python3 -m unittest discover -s tests -v
```

`generate_grid.py m --epsilon 1/1000` emits the regular `m^2`-triangle partition for
`n=m^2+1` at target side `2m-epsilon`. Its output can be saved as JSON and passed directly to the
checker. The tests independently feed frequencies `m=1,...,6` through the verifier. This family
recovers the exact limiting lower bounds for `n=2,5,10,...`; at the first open member `n=17`, its
limit `d>=8` is weaker than Oler's published bound, so the regular grid is a calibration topology,
not a competitive open-case result.

## Stage-zero literature check

R. L. Graham, *On partitions of an equilateral triangle*, Canadian Journal of Mathematics 19
(1967), 394--409, DOI
[`10.4153/CJM-1967-031-x`](https://doi.org/10.4153/CJM-1967-031-x), studies exactly the normalized
quantity "minimum possible maximum cell diameter" and determines it for many small cell counts.
In particular, the box-principle constructions give immediate calibration targets for this
pipeline. Therefore partition search itself is not novel; this issue's useful deliverable is an
exact, machine-readable certificate format, automated search within that format, and a comparison
with published lower bounds.

A 2022 paper, *Coverings of planar and three-dimensional sets with subsets of smaller diameter*,
Discrete Applied Mathematics 320 (2022), 270--281, DOI
[`10.1016/j.dam.2022.06.016`](https://doi.org/10.1016/j.dam.2022.06.016), explicitly reports an
algorithm for suboptimal small-diameter partitions of planar sets. Its abstract was checked during
stage zero; the full method has not yet been reconstructed, so no implementation claim here relies
on it.

## Next bounded step

Encode Graham's small exact partitions as rationally inward-perturbed certificates, starting with
his six-cell partition, and then search fixed planar-complex topologies. Search output remains
`numerical`; only the exact verifier's accepted rational artifact is retained.
