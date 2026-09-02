# Issue #176 — coherent fan faces and triangle measure

Date: 2026-09-02

This continuation starts from the frozen Issue #170 commit `765cee5` and does
not modify that branch.

## Kernel-checked progress

- The exact four-edge rational-worm outward ledger is proved, including the
  positive multipliers relating each edge vector to `wormN0` through `wormN3`.
- `exposedVertices` retains the complete maximizing vertex face at a normal.
  It is nonempty, invariant under positive ray rescaling, and contains both
  endpoints of every supporting polygon edge.
- A unit-square counterexample proves that independent active-vertex choice is
  insufficient: at normal `(1,0)`, both `(1,0)` and `(1,1)` maximize support,
  although their difference is the nonzero vector `(0,1)`.  A common-fan proof
  must therefore preserve exposed faces or use coherent cyclic tie-breaking.
- The closed standard triangle is proved equal to the convex hull of
  `(0,0),(1,0),(0,1)`.  Its product Lebesgue measure is computed from
  `regionBetween` and an interval integral as `1/2`, then identified with its
  determinant/shoelace area.
- An invertible linear equivalence on `Fin 2 -> R` is proved to scale volume of
  every measurable image by the absolute determinant.  This is the analytic
  transport needed for arbitrary nondegenerate triangles.
- The two opposite base-apex triangles' additive measure is proved at most the
  measure of every convex set containing their four vertices.

`lake build` succeeds.  Searches find no `sorry`, `unsafe`, custom `axiom`, or
`native_decide`.  `#print axioms` for all new principal theorems reports only
`[propext, Classical.choice, Quot.sound]`.

## Remaining work

1. Conjugate the `Fin 2 -> R` determinant-scaling theorem through the
   volume-preserving `finTwoArrow` equivalence and identify the image of the
   standard triangle with the arbitrary base-apex convex hull.  Degenerate
   height zero is then the existing null-line case.
2. Combine those two triangle formulas with the proved union containment to
   discharge `segment_bound_from_measure_facts` using actual product volume.
3. For fan coherence, show adjacent normal cones of each concrete polygon
   share the correct exposed endpoint.  Duplicate merged rays must retain the
   same endpoint; parallel edges require the full exposed-face representation.
4. Connect the containing polygon's product volume with its cyclic shoelace
   expression, then feed the completed geometric facts into
   `allocation_chain_commonFan` / `support_certificate_chain`.
