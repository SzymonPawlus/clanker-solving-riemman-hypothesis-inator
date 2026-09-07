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
  every measurable image by the absolute determinant. Conjugating it through
  the coordinate equivalence proves the arbitrary unit-base triangle formula,
  with the degenerate case handled by null-line containment.
- The two opposite base-apex triangles have null overlap, their exact additive
  product measure is `(hUpper + hLower) / 2`, and convex containment proves the
  full measure bound (also in finite real `toReal` form).
- The original `fanMerge` is formally shown to duplicate a shared ray. The new
  `fanMergeDedup` has exact membership, sortedness, `Nodup`, ordered sublist,
  and shared-ray-once theorems, matching the surface-ledger convention.
- A read-only audit of PR #175 found no sign/factor counterexample, but did find
  this verification-boundary mismatch: its prose assumes unique shared rays,
  while its checker does not implement the fan merge and Issue #170's original
  merge duplicated them.

`lake build` succeeds.  Searches find no `sorry`, `unsafe`, custom `axiom`, or
`native_decide`.  `#print axioms` for all new principal theorems reports only
`[propext, Classical.choice, Quot.sound]`.

## Remaining work

1. For fan coherence, show adjacent normal cones of each concrete polygon
   share the correct exposed endpoint.  Duplicate merged rays must retain the
   same endpoint; `fanMergeDedup` removes duplicate surface slots, while
   parallel edges still require the full exposed-face representation.
2. Connect the containing polygon's product volume with its cyclic shoelace
   expression, then feed the completed geometric facts into
   `allocation_chain_commonFan` / `support_certificate_chain`.
