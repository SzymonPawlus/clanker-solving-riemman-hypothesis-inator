# Direct five-edge mixed-area bridge

Issue #184. Status: **sketch**, verification-critical.

This note isolates an elementary finite-polygon proof sufficient for inequality
(1) in `four-edge-support-analytic/README.md`. It uses the exact five-edge hull
from frozen Issue #178 but does not modify or depend on the producer checker.
Unlike the generic Lean interface in Issues #170/#176, it never constructs a
common refined polygon or inserts repeated vertices. Instead it partitions the
boundary edges of the containing polygon into five consecutive normal sectors
and telescopes each sector directly.

## Statement needed by the certificate

Let `P` be the strict counterclockwise pentagon whose directed unit edge
directions and positive lengths are

```text
v0 = (9/41, -40/41)       L0 = 163/480
v1 = (5183/5185,-144/5185) L1 = 77/480
v2 = (5183/5185, 144/5185) L2 = 77/480
v3 = (9/41, 40/41)        L3 = 163/480
v4 = (-1,0)               L4 = 11984563/25510200.
```

Put `e_i=L_i v_i` and `n_i=cw(v_i)`. If a compact convex polygon `K`
contains `P`, then

```text
(1/2) sum_i L_i h_K(n_i) <= area(K).                 (A)
```

Because support is positively homogeneous, the left side is equivalently
`(1/2) sum_i h_K(cw(e_i))`, exactly the first term of inequality (1).
The data above are self-checking: all five squared norms are one,
`sum_i L_i v_i=(0,0)`, and the five consecutive direction cross products are

```text
206024/212585, 1492704/26884225, 206024/212585, 40/41, 40/41,
```

so the ledger closes and turns strictly counterclockwise at every vertex.

## Five-sector proof

Write the vertices of `P` as `p_i`, so `e_i=p_(i+1)-p_i`. Write a
counterclockwise boundary ledger for `K` as `q_j`, with
`d_j=q_(j+1)-q_j`. Zero edges may be deleted. Consecutive codirected edges may
either be retained or combined; neither choice changes the calculation.

The exact direction order proved in the analytic note says that the five
outward rays `n_i` occur strictly cyclically and that every successive turn is
in `(0,pi)`. They partition the outward-normal circle into the five closed
cones from `n_(i-1)` to `n_i`. Assign each outward edge normal `cw(d_j)` of
`K` to the unique half-open cone ending at `n_i`. Call the resulting index
`owner(j)=i`. Each fibre is a consecutive boundary block. A normal on a cut
ray is put in just one adjacent block; this is the only tie convention needed.

The vertex `p_i` maximizes every functional whose outward normal is in the
cone from `n_(i-1)` to `n_i`. Indeed such a normal is a nonnegative linear
combination of the two boundary normals. Every vertex `x` of `P` satisfies

```text
<x-p_i,n_(i-1)> <= 0,   <x-p_i,n_i> <= 0,
```

and the same inequalities persist under a nonnegative combination. Hence

```text
h_P(cw(d_j)) = <p_owner(j),cw(d_j)>
             = det(p_owner(j),d_j).                   (B)
```

For every cut normal `n_i`, choose the last counterclockwise vertex `q_(t_i)`
of its exposed face in `K`. The elementary support-order lemma says that the
indices `t_i` are cyclically nondecreasing, and that the `K` edges after
`t_(i-1)` through `t_i` are precisely the block with owner `i`. This follows
directly from the two supporting half-planes: while the outward normal rotates
through an angle less than `pi`, the terminal point of the exposed face cannot
move backwards around a convex boundary. Equality of adjacent `t_i` means an
empty block and causes no exceptional term.

Here is a purely polygonal proof of that order lemma. Delete zero edges and
write the remaining edge-normal rays of `K` in their boundary order. On an
open interval between two successive rays, exactly one boundary vertex
maximizes the functional: the intersection of the two adjacent supporting
half-planes. When the normal reaches an edge ray, the exposed face expands to
that edge; choosing its last counterclockwise endpoint advances the selector
across the edge. Immediately after the ray, that endpoint is the unique
maximizer. Thus a full counterclockwise sweep visits the `q_j` in order and
crosses each boundary edge exactly when its normal ray is crossed. Restricting
this sweep to the five cut intervals gives exactly the asserted five blocks.
Parallel consecutive edges merely expand one exposed face and are handled by
the same last-endpoint convention; alternatively they may first be combined.

The support of `K` at a cut is attained at `q_(t_i)`. Cyclic summation by parts
followed by block telescoping now gives

```text
sum_i h_K(cw(e_i))
 = sum_i det(q_(t_i), p_(i+1)-p_i)
 = sum_i det(p_i, q_(t_i)-q_(t_(i-1)))
 = sum_j det(p_owner(j),d_j)
 = sum_j h_P(cw(d_j)).                                (C)
```

This is mixed-surface symmetry, but proved using only five boundary blocks;
there is no merged fan data structure and no independent choice of tied
maximizers. Since `P subset K`, support monotonicity applied separately to
every `K` edge gives

```text
sum_j h_P(cw(d_j)) <= sum_j h_K(cw(d_j))
                    = sum_j det(q_j,d_j)
                    = 2 area(K).                      (D)
```

Combining (C) and (D), then dividing by two, proves (A).

The last equality in (D) is also elementary Lebesgue geometry, not a new
mixed-area assumption. Choose `q_0` as a fan vertex. Convexity makes the
triangles `(q_0,q_j,q_(j+1))`, for `1 <= j <= m-2`, cover `K`; their interiors
are pairwise disjoint, and their boundaries are finite unions of null line
segments. Their determinant areas therefore add. Expanding and telescoping
the triangle determinants gives exactly the cyclic shoelace sum. This proof
also permits collinear boundary vertices; zero-area triangles simply vanish.

## Why five arbitrary support points do not suffice

A tempting shorter proof selects one maximizer at each source normal and tries
to bound the mixed surface by the shoelace area of those selected points. That
claim is false, even with exact rational polygons.

Let `K` be the counterclockwise octagon

```text
(0,-5),(4,-4),(5,0),(4,4),(0,5),(-4,4),(-5,0),(-4,-4)
```

and let `P=[-4,4]^2`. Then `P subset K`. At the four axis normals, selecting
the cardinal maximizers `(0,-5),(5,0),(0,5),(-5,0)` produces a diamond of area
`50`. But

```text
(1/2) sum_edges(P) length(e) h_K(unit outward(e))
 = (1/2) * 4 * 8 * 5 = 80,
```

which equals the octagon's shoelace area. Thus the selected-point polygon can
miss `30` units of area. The intervening boundary blocks in (C), not merely
the five cut support points, are essential. Independent endpoint selection can
also reverse a chord at a flat exposed face, as recorded formally in PR #180.

## Remaining verification work

The algebraic identities (B)--(D) are finite. The only geometric lemma still
requiring kernel-level packaging is the support-order/block lemma for a cyclic
convex polygon. A direct Lean implementation can avoid angle functions by
requiring the five exact cone decompositions and proving each with determinant
signs. The Lebesgue/shoelace step can be built from the already proved arbitrary
triangle determinant-measure theorem in PR #180 plus finite null-overlap and
measure-union induction.

Until those two pieces are formalized or independently reviewed, this note is
not an assumable proof of the `0.2350682` area bound.
