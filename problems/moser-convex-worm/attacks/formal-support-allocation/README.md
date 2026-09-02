# Independent formal support-allocation audit

**Status:** `sketch`, verification-critical; does not promote or modify PR #168.

This attack independently checks the exact algebra behind the mixed-area
support proof.  The Lean module `Verified.Moser.SupportAllocation` contains no
`sorry`, oracle, custom axiom, `unsafe`, or floating-point evaluation.  It
proves:

- the three rational worm edges have length exactly `1/3`, hence the open
  traversal has length exactly one;
- the closing chord has length `407/807` (and is not counted in the worm);
- the hull vertices are in strict convex orientation and their exact shoelace
  area is `87880/651249`;
- all four stated normals are unit, both surface-measure splits balance, the
  two allocation columns have unit capacity, and both translation loads vanish;
- a purely ordered-field first-variation theorem deriving `first <= 2 areaK`
  from the quadratic Minkowski containment inequality;
- finite support-allocation translation cancellation;
- an explicit end-to-end implication from the Minkowski containment polynomial
  and exact slab premise to `target <= area(K)`;
- the full closed angular endpoint union and the strict rational comparison.

The separate `check_slabs.py` is an independent exact rational checker for the
two closed forms

```text
sqrt(3)/24 + (|n0.x| + |n2.x| + (138/269)|n1.x|)/12
(|n0.x| + |n2.x|)/12 + (169/807)|n1.x|.
```

It partitions the claimed intervals into half-degree cells, proves the sign of
each normal coordinate throughout each cell using a unit Lipschitz bound, and
uses exact Taylor/Lagrange enclosures only at endpoints.  Once signs are fixed,
the nonconstant expression is `A cos(gamma)+B sin(gamma)` and satisfies
`f''=-f`; positivity gives concavity, so a cell minimum occurs at an endpoint.
This is structurally different from adapting the producer's interval replay.
Before checking angles it independently re-derives every rational coefficient
in both closed forms from the actual `1/3,1/3,1/3,407/807` surface lengths,
the `138/407` allocation, centred-segment support, and the triangle-width
coefficient.

Replay:

```sh
cd lean && lake build Verified.Moser.SupportAllocation
cd .. && python3 problems/moser-convex-worm/attacks/formal-support-allocation/check_slabs.py
```

`Verified.Moser.PolygonBridge` now replaces the first-variation premise with a
finite cyclic proof: common-fan surface symmetry is discrete summation by
parts, self-surface is the shoelace sum, and containment support inequalities
give the mixed-area bound termwise. It also proves repeated-vertex insertion
invariance, convex-coordinate support monotonicity, exact unit-base triangle
area, both triangle containments in a convex set, and an allocation theorem
ending at the containing polygon's shoelace area.

The remaining geometric boundary is existence of the common cyclic fan with
the required active support vertices for arbitrary concrete convex polygons
(and, for the direct segment route, shoelace additivity across the two caps).
Until that existence layer compiles, this remains a substantial exact audit,
not a verified global Moser improvement; the Issue #136 baseline gate also
remains unresolved.

`POLYGON-BRIDGE.md` records the implemented signatures, construction blueprint,
and the exact remaining existence-layer kill criterion.
