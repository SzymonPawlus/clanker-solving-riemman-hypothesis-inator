# Global exposed-face sweep, determinant kernel

Issue #190. Status: **sketch**, verification-critical.

This continuation starts from frozen PR #189 and does not modify it. The new
Lean module `Verified.Moser.BoundarySweep` establishes the main local-to-global
existence step for the convex-boundary sweep:

1. If a finite polygon vertex maximizes a nonzero normal, the inequalities at
   its two neighbours put that normal in the closed cone of the two adjacent
   clockwise edge normals. The proof is only two determinant signs and the
   cone-coordinate theorem from PR #189.
2. If the incoming coefficient is positive, that vertex already owns the
   half-open cone. If it is zero, nonzeroness makes the outgoing coefficient
   positive; the proof advances once across the exposed edge. Global edge
   support and the exact endpoint tie show that the next vertex is also a
   maximizer. It now has positive incoming coefficient and zero outgoing
   coefficient.
3. Finite maximization supplies the initial vertex. Therefore every nonzero
   normal has a maximizing half-open owner under strict turns and global edge
   support. Flat edge ties are resolved coherently rather than independently.

The module also proves exact exposed-edge maximizer characterization when
strict support is supplied, and uniqueness throughout an open normal cone.

## Necessary correction to weak hypotheses

Full dimensionality, closure, and positive local turns alone are insufficient.
The exact rational pentagram ledger

```text
(0,3), (-2,-3), (3,1), (-3,1), (2,-3)
```

has consecutive edge cross products

```text
22, 24, 24, 22, 24,
```

closes exactly and is full-dimensional. Nevertheless its first clockwise edge
normal gives support value `6` at the edge endpoint and `20` at vertex 3. It is
a winding star, not a convex boundary. All four facts are kernel checked as
`star_all_local_turns_positive`, `star_edges_close`,
`star_full_dimensional`, and
`star_local_turns_do_not_give_edge_support`.

Thus the corrected sweep theorem must explicitly require every directed edge
to support every listed vertex (or an already established simple convex
boundary). This agrees with PR #187, which assumes a convex containing polygon;
the counterexample does not weaken that note.

## Remaining statement

For the five cyclically ordered cut normals, apply
`exists_halfOpen_owner` separately. The remaining formal step is to prove that
their half-open owners occur in cyclic boundary order. Then the crossed edges
are consecutive by construction and their sums telescope to the endpoint
differences consumed by PR #189's `five_block_telescoping`.

No counterexample was found under strict turns plus global edge support. The
current module compiles without `sorry`, `unsafe`, custom axioms, or
`native_decide`.
