# Determinant-only five-sector ordering kernel

Issue #188. Status: **sketch**, verification-critical.

This is an independent continuation from frozen PR #187. It does not modify
that PR. The Lean module `Verified.Moser.FiveSectorOrder` proves the algebraic
and local geometric kernel needed to formalize its five boundary blocks:

- support at two normals implies support throughout their nonnegative cone;
- a vector is in the short cone from `u` to `v` exactly via the determinant
  coefficients `det(w,v)/det(u,v)` and `det(u,w)/det(u,v)` when
  `det(u,v)>0`;
- the five exact Issue #178 normal sectors all have positive determinant and
  the five edge directions are exactly unit;
- five-term cyclic summation by parts is proved without modular-index tactics;
- endpoint differences expressed as five boundary-block sums telescope to the
  five owner-weighted edge sums.

These statements contain no angle functions, square roots, limits, or generic
common-fan object. They compile without `sorry`, `unsafe`, custom axioms, or
`native_decide`.

The remaining global lemma is deliberately exposed rather than hidden: for a
full-dimensional counterclockwise convex boundary, the last endpoint of the
exposed face advances monotonically as the normal crosses the ordered edge
rays. Consequently the edges crossed between two successive exact cut normals
form one consecutive block, and their vector sum is the difference of the cut
endpoints. This is true after deleting zero edges; codirected consecutive edges
may be retained because the last-endpoint convention crosses their whole
exposed chain at the common ray.

No counterexample was found to that exact statement under its required
hypotheses. Two weaker variants are false and must not be substituted:

1. independently choosing an arbitrary point of each exposed face can move
   backwards at a flat face (the unit-square counterexample in PR #180);
2. keeping only the finitely many cut support points can lose intervening
   boundary area (the exact area-50 versus area-80 rational octagon example in
   PR #187).

Thus a subsequent proof should represent a convex boundary as its ordered
nonzero edge rays and prove the last-exposed-endpoint sweep lemma. Once its
five block-sum equalities are produced, `five_block_telescoping` discharges the
entire combinatorial algebra, while `supports_exact_sector` supplies each
block's source support vertex.
