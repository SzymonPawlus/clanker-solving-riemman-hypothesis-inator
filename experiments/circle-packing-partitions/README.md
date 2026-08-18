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

`generate_graham6.py` reconstructs the symmetric topology in Graham's Figure 7. In a unit outer
triangle its ideal parameters are

\[
  \delta=\frac{1}{1+\sqrt3},\qquad r=\frac{\delta}{\sqrt3}.
\]

The source gives the diagram and `delta`; the two-parameter coordinate reconstruction is ours and
therefore remains `sketch`. The committed artifact uses rational approximations to both parameters
and the rational target `d=683/125=5.464`. The exact checker obtains maximum squared cell diameter

\[
  \frac{6249769587629311467}{1562500000000000000}
  = 4-\frac{230412370688533}{1562500000000000000}<4,
\]

so the artifact supports `s(7)>683/125+2*sqrt(3)`, within about `0.000102` of the known exact
point-triangle optimum `2+2*sqrt(3)`. This is the first calibration here whose topology is not a
simple regular grid.

`search_graham6.py` is the first bounded fixed-topology search. It knows only the six-cell planar
complex and minimizes its maximum squared diameter over the two free rationalization parameters;
it does not hard-code the algebraic optimum. From the generic start `(delta,r)=(0.35,0.20)`, the
deterministic pattern search rediscovers Graham's values to six decimal places. This is a pipeline
calibration, not a new result, and its floating-point output is never accepted directly: only the
rationalized JSON above is checked.

Run:

```bash
python3 partitioncheck.py certificates/n003-d1999-over-1000.json
python3 partitioncheck.py certificates/n004-d433-over-125.json
python3 partitioncheck.py certificates/n005-d3999-over-1000.json
python3 partitioncheck.py certificates/n006-d3999-over-1000.json
python3 partitioncheck.py certificates/n007-graham6-rationalized.json
python3 search_graham6.py
python3 generate_open_baselines.py 17
python3 -m unittest discover -s tests -v
```

`generate_grid.py m --epsilon 1/1000` emits the regular `m^2`-triangle partition for
`n=m^2+1` at target side `2m-epsilon`. Its output can be saved as JSON and passed directly to the
checker. The tests independently feed frequencies `m=1,...,6` through the verifier. This family
recovers the exact limiting lower bounds for `n=2,5,10,...`; at the first open member `n=17`, its
limit `d>=8` is weaker than Oler's published bound, so the regular grid is a calibration topology,
not a competitive open-case result.

`generate_open_baselines.py` forces the regular-grid topology through the requested first open
cases. For `n=16` it merges two triangles into a rhombus; for `n=17,18,19` it uses the 4-by-4 grid
and zero, one, or two median refinements. All four outputs pass the exact verifier, but they are
decisively noncompetitive:

| `n` | exact target `d` certified by this topology | comparison |
|---:|---:|---|
| 16 | `2309/500 = 4.618` | Graham 1967 already gives the cited limiting bound `d >= 2+4*sqrt(3) ~ 8.928` |
| 17 | `7999/1000 = 7.999` | Oler gives `sqrt(137)-3 ~ 8.705` |
| 18 | `7999/1000 = 7.999` | Oler gives `sqrt(145)-3 ~ 9.042` |
| 19 | `7999/1000 = 7.999` | Oler gives `sqrt(153)-3 ~ 9.369` |

Thus the regular-grid topology meets its local kill criterion and is abandoned for the open
cases. This is a useful negative calibration: exact checking is not the bottleneck; choosing a
hexagon-like planar complex is.

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

Reconstruct Graham's 15-cell Figure 21 topology, which already supplies the strongest partition
baseline for `n=16`, and then perturb that planar complex for `n=17,18,19`. Search output remains
`numerical`; only the exact verifier's accepted rational artifact is retained.
