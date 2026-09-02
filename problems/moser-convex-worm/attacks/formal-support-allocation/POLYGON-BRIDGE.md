# Finite-polygon mixed-area bridge: exact missing theorem

This is the deliberately unhidden boundary of the current Lean development.
Mathlib 4.33 has no planar convex-polygon volume/Minkowski API from which this
can be discharged by a short import.  Adding a premise named “mixed area
monotonicity” would merely rename the claim, so no such axiom or opaque
definition is used.

## Sufficient theorem signature

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
length times outward unit normal.  The precise missing Lean theorem is:

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
maximum and minimum `y` at vertices `(x+,h+)` and `(x-,-h-)`.  Convexity puts
both base-apex triangles in `K`; their interiors lie in opposite open
half-planes and their determinant areas are `h+/2` and `h-/2`.  A finite
polygon proof may triangulate `K` along the base line and show the two triangle
shoelace areas sum to at most `area(K)`.  Lean already proves the determinant
identity and the final implication from that finite additivity fact.

## Kill criterion

Do not mark the bridge complete unless the common-fan insertion invariants,
cyclic summation-by-parts identity, and vertex-containment support inequality
all compile without `sorry`, `unsafe`, custom axioms, or an assumed theorem
equivalent to `polygon_surface_symmetry`.  For the segment, assuming the sum of
the two triangle areas is at most `area(K)` is still an exposed interface, not
a completed geometric proof.
