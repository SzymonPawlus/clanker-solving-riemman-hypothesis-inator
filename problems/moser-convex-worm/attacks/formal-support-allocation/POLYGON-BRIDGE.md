# Finite-polygon mixed-area bridge

The finite algebra is implemented in `Verified.Moser.PolygonBridge`. Mathlib
4.33 has no planar convex-polygon volume/Minkowski API, so this development uses
cyclic shoelace sums instead. No axiom or opaque definition named “mixed area
monotonicity” is introduced.

## Implemented theorem signature

For nonempty counterclockwise convex polygons `P` and `K`, represented by
cyclic vertex lists with duplicate consecutive vertices removed, define

```text
edge(v,i)       = v[i+1] - v[i]
outward(e)      = (e.y,-e.x)
support(v,n)    = max_i dot(v[i],n)
twiceArea(v)    = sum_i cross(v[i],v[i+1])
surface(v,K)    = sum_i support(K,outward(edge(v,i)))
```

Using the unnormalised outward vector is intentional: it already equals edge
length times outward unit normal. The mathematical core is:

```text
theorem polygon_surface_symmetry
  (hP : StrictCCWConvex P) (hK : StrictCCWConvex K) :
  surface P K = surface K P

theorem polygon_self_surface
  (hK : StrictCCWConvex K) :
  surface K K = twiceArea K

theorem polygon_support_mono
  (hK : StrictCCWConvex K) (hPK : every vertex of P lies in K) :
  forall edge of K,
    support(P,outward(edge)) <= support(K,outward(edge))
```

It is implemented as `surface_symmetry_commonFan`,
`self_surface_eq_twiceArea`, `support_le_of_convexCoordinates`, and
`surface_le_twiceArea_of_commonFan`. The first two are unconditional cyclic
identities. `allocation_chain_commonFan` connects the finite surface inequality
to the previous allocation theorem and an exact slab premise.

`exists_active_vertex` and `exists_active_vertices_on_fan` prove that a
maximizing source vertex can be selected on every ray of any already-given
finite fan. `commonFan_support_of_coordinates` then derives the pointwise
containment inequality from explicit convex coordinates and those active
maximality facts.

For fan construction, the original `fanMerge` sorts the concatenation as a
multiset. The theorem `fanMerge_shared_ray_is_duplicated` records the exact
counterexample to treating it as a set union. The surface ledger instead uses
`fanMergeDedup`; its membership, sortedness, `Nodup`, one-shared-ray, and
duplicate-free input sublist properties are kernel checked. Cyclic reindexing
invariance of both shoelace area and mixed surface is also formalized.

These three imply, by a finite sum inequality only,

```text
surface P K = surface K P <= surface K K = twiceArea K,
```

which is exactly

```text
(1/2) sum_e length_e(P) h_K(unitNormal_e(P)) <= area(K).
```

It covers the actual application because `P` is one placed witness hull and
all its listed vertices belong to the joint convex hull `K`.

## Proof blueprint

1. Merge the two cyclic lists of outward edge directions, preserving repeated
   parallel directions only once.  Insert zero-length edges so both polygons
   use this common cyclic fan.  This operation preserves support, surface, and
   shoelace area.
2. On every open normal cone, record the active support vertex of each polygon.
   Across a fan ray that vertex changes by exactly the corresponding edge.
3. Expand `surface P K` as dot products between active vertices of `K` and
   clockwise rotations of edge increments of `P`.  Discrete summation by parts
   on the cyclic fan moves the increment from `P` to `K`; `dot(x,Rcw y) =
   dot(y,Rcw x)` with the cyclic sign change gives `surface K P`.
4. Taking both polygons equal reduces the same sum to the shoelace formula,
   proving self-surface without limits or measure theory.
5. Vertex containment implies every linear functional is bounded by `K`'s
   support.  Multiply by the nonnegative edge lengths of `K` and sum.

An alternative Minkowski proof can expand the common-fan edge list of `K+tP`;
its shoelace polynomial has linear coefficient `surface P K`.  The symmetry
route above is shorter and avoids separately formalising area monotonicity.

## Lower-dimensional segment

The segment must remain separate because it has no strictly convex cyclic
edge list.  Pin its endpoints at `(0,0),(1,0)`.  Compact polygon `K` attains
maximum and minimum `y` at vertices `(x+,h+)` and `(x-,-h-)`. Convexity puts
both base-apex triangles in `K`; their interiors lie in opposite open
half-planes and their determinant areas are `h+/2` and `h-/2`. Lean now proves
the arbitrary unit-base triangle product-Lebesgue measure formula, including
the degenerate case, by transporting the standard triangle through an exact
determinant linear equivalence. Null overlap and convex containment therefore
give the complete two-cap measure bound, including its finite real `toReal`
form. The repeated-vertex common-fan theorem also permits a degenerate-polygon
treatment without a limiting argument.

## Kill criterion

The cyclic summation-by-parts identity, repeated-vertex insertion invariance,
convex-coordinate support inequality, surface inequality, triangle containment,
and allocation chain compile without `sorry`, `unsafe`, or custom axioms.

The remaining kill criterion is the **existence layer**: do not call the global
bridge complete until arbitrary concrete finite convex polygons are proved to
admit a cyclic common-fan representation whose active vertices satisfy the
support hypotheses and whose repeated-vertex shoelace sum is the original
polygon's. The deduplicated abstract sorted merge and exposed-face representation
are complete;
the concrete four-quadrant algebraic ray key is now defined and proved
rescaling-invariant, and its within-sector order is proved equivalent to
counterclockwise determinant order. The exact worm ledger is strictly ordered
as `n₂,n₃,n₀,n₁` after the positive-horizontal cut. The remaining fan step is
proving that coherently selected exposed-face endpoints across successive
merged rays reproduce exactly the original polygon edges. The direct segment
route's measure-theoretic triangle and union interfaces are fully discharged;
connecting an arbitrary containing polygon's product volume to its cyclic
shoelace expression remains part of the polygon existence layer.
