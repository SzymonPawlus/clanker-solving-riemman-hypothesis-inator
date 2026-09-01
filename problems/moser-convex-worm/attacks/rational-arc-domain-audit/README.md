# Rational-arc compact-domain audit

**Status:** exact witness and compact-domain certificate; no area lower bound.

**Issue:** #140. Producer/search issue: #137.

This attack was derived independently after PR #139 was frozen. It does not
read or adapt the producer's optimizer or checker logic.

## Exact witness

In traversal order, let

```text
P0 = (0,0)
P1 = (1/3,0)
P2 = (32/75,8/25)
P3 = (91/625,312/625).
```

The three edge vectors are

```text
P1-P0 = (1/3,0),
P2-P1 = (7/75,8/25) = (1/3)(7/25,24/25),
P3-P2 = (1/3)(-527/625,336/625).
```

Their squared norms are `1/9`, because
`7^2+24^2=25^2` and `527^2+336^2=625^2`. Each edge
therefore has positive length `1/3`, and the traversal length is exactly one.
There is no closing edge. The witness is an ordinary polygonal arc, hence a
continuous rectifiable unit worm.

## Compact counterexample domain

Pin the forced unit segment at `E=(0,0), F=(1,0)`. Let `K` be the convex hull
of a simultaneous placement of the segment, side-`1/2` equilateral triangle,
side-`1/3` square, and the rational arc.

For any direction, the equilateral triangle has width at least its altitude
`sqrt(3)/4`. If `A,B` realize the diameter `d` of `K`, choose two triangle
vertices whose projection on the line perpendicular to `AB` realizes the
triangle's width in that direction. The four-point height inequality gives

```text
area(K) >= d * sqrt(3) / 8.
```

Thus a counterexample to `area(K) >= T` must satisfy
`d < 8T/sqrt(3)`. Since `E` belongs to `K`, every selected anchor vertex of
the other three witnesses has Euclidean distance at most `d` from `E`, and
hence both coordinates lie in `[-D,D]` for any rational
`D > 8T/sqrt(3)`. Squaring is safe for positive values, so the checker proves
the outward condition exactly as `3*D^2 > 64*T^2`.

Each unpinned witness retains one full orientation variable in `[0,360]`
degrees. Endpoints are duplicated representations but leave no gap. No
reflection quotient is taken. This matches the repository's
orientation-preserving convention and is essential for the asymmetric new
arc. Reversing its traversal does not reflect its image and does not remove
this orientation degree of freedom.

The resulting closed box has nine variables:

```text
triangle: tx, ty, theta
square:   tx, ty, theta
arc:      tx, ty, theta.
```

The strict counterexample domain is contained in this closed box, including
when a hypothetical configuration approaches the target from below.

## Machine-readable boundary certificate

Replay:

```sh
python3 problems/moser-convex-worm/attacks/rational-arc-domain-audit/check_domain.py \
  problems/moser-convex-worm/attacks/rational-arc-domain-audit/domain.json
python3 -m unittest discover \
  -s problems/moser-convex-worm/attacks/rational-arc-domain-audit \
  -p 'test_*.py' -v
```

The checker recomputes all rational edge lengths, the exact outward diameter
inequality, and the complete variable ledger. It rejects a global claim,
reflection quotient, inward diameter bound, missing pose coordinate, shortened
angle interval, altered pinned segment, unknown field, duplicate JSON key, or
noncanonical rational.

Acceptance certifies only the witness and compact search domain. It says
nothing about the numerical minimum near `0.23645` and supplies no branch tree
or sound area-pruning leaves. A global result still requires exhaustive
coverage of this nine-dimensional box with independently verified outward
rigid transforms, containment polygons/support bounds, and target-clearing
area lower endpoints.
