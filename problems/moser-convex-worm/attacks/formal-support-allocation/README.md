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

Replay:

```sh
cd lean && lake build Verified.Moser.SupportAllocation
cd .. && python3 problems/moser-convex-worm/attacks/formal-support-allocation/check_slabs.py
```

Remaining geometric boundary: the Lean first-variation lemma takes the
quadratic Minkowski containment inequality as a premise.  A fully
`verified:lean` geometric interpretation still needs a formal polygon area and
Minkowski-sum identity, plus the lower-dimensional segment's direct
two-triangle area argument.  Until then this remains a substantial exact audit,
not a verified global Moser improvement; the Issue #136 baseline gate also
remains unresolved.
