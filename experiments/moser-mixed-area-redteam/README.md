# Independent finite-polygon mixed-area bridge red-team

Issue #174.  This directory was derived without consulting the Issue #170 Lean
implementation or adapting code from PR #168.

## Frozen derivation

Let `P` be a convex polygon contained in a convex polygon `K`.  Traverse `P`
counterclockwise.  For each directed edge `e` let `d_e` be its displacement,
`l_e=|d_e|`, and let `n_e=rot_cw(d_e)/l_e` be its outward unit normal.  The exact
polygonal Minkowski expansion is

```
area(K + t P)
  = area(K) + t sum_e l_e h_K(n_e) + t^2 area(P).       (1)
```

Here is the common-fan calculation in detail, including nongeneric cases.
Delete zero edges and combine every consecutive run of codirected collinear
edges.  This does not change either polygon or the claimed sum: support is
constant along the run's common normal and the edge lengths add.  Merge the
two resulting finite cyclic lists of outward-normal rays.  At a ray absent
from one polygon give that polygon an edge of length zero.  Shared rays occur
once, with both lengths potentially positive.  Thus there are no distinct or
generic-position assumptions.

Write the common rays in counterclockwise cyclic order.  Put
`tau_i=rot_ccw(n_i)`, and write the corresponding boundary edges as
`k_i=alpha_i tau_i` and `p_i=beta_i tau_i`, where `alpha_i,beta_i >= 0`.
Choose cyclic vertices so that `k_i=x_(i+1)-x_i` and
`p_i=y_(i+1)-y_i`.  A zero edge means the active vertex is repeated.  Both
endpoints of a nonzero edge maximize its outward functional, hence

```
det(x_i,p_i) = beta_i h_K(n_i),
det(y_i,k_i) = alpha_i h_P(n_i).                         (3)
```

Discrete cyclic summation by parts, followed only by using the other endpoint
of the same support edge, gives mixed-surface symmetry:

```
sum_i det(x_i,p_i)
 = sum_i det(y_i,k_(i-1))
 = sum_i det(y_i,k_i).                                  (4)
```

For clarity, the first equality follows by expanding
`p_i=y_(i+1)-y_i` and cyclically reindexing.  In the second, reindex and use
`det(y_(i+1),k_i)=det(y_i,k_i)`, since their difference is `p_i`, parallel
to `k_i` whenever both are nonzero (and the assertion is trivial if either is
zero).  Equations (3)--(4) say exactly

```
sum_edges(P) l_P h_K(n_P) = sum_edges(K) l_K h_P(n_K).  (5)
```

The Minkowski boundary has common-fan edge `k_i+t p_i`, and support is
`h_K+t h_P`.  Applying the exact identity
`2 area(Q)=sum_edges(Q) l_Q h_Q(n_Q)` and then (5) gives

```
2 area(K+tP)
 = sum_i (alpha_i+t beta_i)(h_K(n_i)+t h_P(n_i))
 = 2 area(K) + 2t sum_edges(P) l_P h_K(n_P)
     + 2t^2 area(P),
```

which is (1), with exactly the displayed coefficient and no hidden factor.
The area identity itself is just shoelace term by term:
`l_e h_Q(n_e)=h_Q(rot_cw(d_e))=det(q_e,d_e)`.

Containment gives, for every `t >= 0`,

```
K + tP  subset  K + tK = (1+t)K.
```

The equality on the right does not assume that the origin lies in `K`:
`(x+t y)/(1+t)` is a convex combination of `x,y in K`.  Dilation is about the
chosen origin and multiplies area by `(1+t)^2`; translating the origin merely
translates the dilate.  Compare areas, substitute (1), subtract `area(K)`,
divide by positive `t`, and let `t` tend to zero.  (Equivalently choose an
explicit sufficiently small rational `t` if the inequality failed.)  This
proves

```
(1/2) sum_e l_e h_K(n_e) <= area(K).                    (2)
```

The factor `1/2` is necessary: `P=K` makes the unhalved sum equal to
`2 area(K)`.

Translation causes no hidden origin assumption.  Translating `K` by `a` adds
`a . rot_cw(d_e)` to the edge term, and the total addition vanishes because
`sum_e d_e=0`.  Translating `P` leaves all edge vectors unchanged.

For a nondegenerate segment `[a,b]`, use its two oriented boundary edges
`d=b-a` and `-d`.  The sum in (1) is

```
h_K(rot_cw(d)) + h_K(-rot_cw(d)),
```

namely segment length times the perpendicular width of `K`.  This is also the
linear coefficient obtained by extruding `K` by the segment, so the same
containment argument proves (2).  A point follows by a zero limit and has sum
zero.

More explicitly, `K+t[a,b]` is a translate of `K+[0,t(b-a)]`.  Each section
on a line parallel to `b-a` extends by `t|b-a|`; integrating over the
perpendicular projection gives that the
added area is exactly `t|b-a|` times the perpendicular width of `K`; no
quadratic term occurs.  This is precisely the two-oriented-edge support sum
above and avoids any appeal to a full-dimensional approximation.

## Exact checker

`mixed_area.py` uses `fractions.Fraction`.  It avoids unit normals and square
roots using

```
l_e h_K(n_e) = h_K(rot_cw(d_e)).
```

It deliberately rejects clockwise, duplicate, and collinear boundary data
rather than silently changing certificate semantics.  Tests cover equality,
the missing `1/2`, segments, two independent translations, noncontainment,
wrong normals, a missing edge, and 1,000 seeded exact rational instances.

## Post-freeze comparison with Issue #170 and PR #168

This derivation and checker were committed as `5a7534d` before those interfaces
were read.  The comparison found algebraic agreement:

- both use clockwise rotation of a CCW edge as the unnormalized outward
  normal, so edge length is already absorbed;
- Issue #170's `twiceArea`, `self_surface_eq_twiceArea`, cyclic summation by
  parts, and final division by two have the same sign and factor conventions;
- its `support_certificate_chain` asks the caller for exactly the quadratic
  Minkowski inequality produced by (1) and containment above;
- its separate two-triangle segment interface computes the same two-sided
  width divided by two.

There is no numerical or sign mismatch.  The important scope distinction also
agrees: Issue #170 explicitly leaves the geometric common-fan existence layer
unfinished in Lean.  This note supplies an independent paper proof and exact
computational red-team, not a kernel-checked discharge of that remaining
interface; it therefore remains `sketch` pending independent review.

Run:

```
python -m unittest discover -s experiments/moser-mixed-area-redteam -v
```
