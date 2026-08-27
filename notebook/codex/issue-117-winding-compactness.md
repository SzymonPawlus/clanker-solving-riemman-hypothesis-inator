# Square Peg #117: winding multiplicity and primitive compactness

Status: `sketch`.  This note is self-contained and does not assume any claim
from PR #115.

## Statement

Give `S^1=R/Z` its shorter-arc metric.  Let

```text
c_n : S^1 -> R^2
```

be smooth Jordan embeddings converging uniformly, as parametrized maps, to a
continuous map `c`.  Let

```text
omega(delta)
  = sup_n sup{|c_n(u)-c_n(v)| : d_S1(u,v) <= delta}.
```

Uniform convergence makes the family `(c_n)` equicontinuous, so
`omega(delta) -> 0` as `delta -> 0`.

For lifts `s<t<=s+1/2`, let `L_n[s,t]` be the closed piecewise-smooth loop
obtained by traversing `c_n` from `s` to `t` and then traversing the straight
segment from `c_n(t)` back to `c_n(s)`.  Assume there is a fixed integer
`K>=1` such that

```text
|wind(L_n[s,t],z)| <= K
```

for every `n`, every such interval, and every point `z` outside the loop.

Use the symmetric Liouville primitive

```text
lambda_0 = (x dy - y dx)/2,       d lambda_0 = dx wedge dy,
```

and normalize the lifted primitives by

```text
F_n(0)=0,    F_n(t)-F_n(s)=integral_[s,t] c_n^* lambda_0.
```

Then `(F_n)` is locally uniformly bounded and equicontinuous on `R`.
Consequently it has a subsequence converging locally uniformly to a continuous
function `F : R -> R`.

More precisely, if

```text
R = sup_n sup_t |c_n(t)| < infinity,
```

then for `0<=t-s<=delta<=1/2`,

```text
|F_n(t)-F_n(s)|
    <= (K pi/4) omega(delta)^2 + (R/2) omega(delta).          (1)
```

The same conclusion holds for any smooth one-form `lambda` on `R^2` with
`d lambda = dx wedge dy`.  Indeed, `lambda-lambda_0=dh`; on the common compact
range, the endpoint correction `h(c_n(t))-h(c_n(s))` has a common modulus of
continuity.  A sign change in `d lambda` changes no estimate.

## Proof of the scale estimate

Fix `n,s,t`, put `p=c_n(s)`, `q=c_n(t)`, and write `A` for the oriented
subarc.  Since every two parameters in `[s,t]` are at circle distance at most
`delta`, the image of `A` has diameter at most `omega(delta)`.  Adding its
closing chord does not enlarge its convex hull, and the diameter of a convex
hull equals the diameter of the original set.

The winding number of any closed loop vanishes outside the convex hull of its
trace: a point outside that hull can be strictly separated from the loop by a
line, and the containing half-plane contracts away from the point.  The
isodiametric inequality therefore bounds the area of the support by
`(pi/4) omega(delta)^2`.

The winding-number form of Green's theorem for a piecewise `C^1` closed loop
gives

```text
integral_L lambda_0 = integral_R2 wind(L,z) dz.
```

This identity does **not** require the closing chord to meet the open arc only
finitely many times.  In current language, the loop is an integral
one-cycle and its index is the integer-valued multiplicity of the bounded
two-current that it bounds; Stokes' theorem gives the displayed identity.
Equivalently, one may approximate the loop in piecewise `C^1` norm by generic
loops having only finitely many transverse crossings, apply Green's theorem
face by face, and pass to the limit.  Thus repeated, tangential, or
accumulating chord--arc intersections do not create a missing boundary term.
The same current argument (or the half-plane contraction above) shows that
the index is zero off the convex hull.

The multiplicity hypothesis hence implies

```text
|integral_L lambda_0| <= (K pi/4) omega(delta)^2.             (2)
```

It remains to remove the closing chord.  Direct parametrization of the segment
from `q` to `p` gives

```text
integral_[q,p] lambda_0 = det(q,p)/2
                         = det(q,p-q)/2,
```

so

```text
|integral_[q,p] lambda_0|
    <= (|q|/2)|p-q| <= (R/2) omega(delta).                    (3)
```

Since the closed-loop integral is the subarc integral plus the chord integral,
(2)--(3) prove (1).

## Compactness on the universal cover

Estimate (1) applies without change to short intervals crossing an integer,
because `c_n` is extended periodically and the hypothesis was stated for all
lifts.  Thus `(F_n)` has a common local modulus.

The period increment is

```text
A_n = F_n(1)-F_n(0) = integral_c_n lambda_0.
```

Because `c_n` is a Jordan embedding contained in `B(0,R)`, Green's theorem
identifies `|A_n|` with the area of its Jordan domain, hence
`|A_n|<=pi R^2`.  Also

```text
F_n(t+m)=F_n(t)+m A_n       (0<=t<=1, m in Z).
```

The common modulus and the bound at `0` give uniform bounds on every compact
interval.  Arzela--Ascoli supplies a locally uniformly convergent subsequence.
Equivalently, first extract uniform convergence on `[0,1]`; then
`A_n=F_n(1)->A`, and extend the limit by

```text
F(t+m)=F(t)+m A.
```

The displayed period identity gives locally uniform convergence on `R`.

## Double-spiral stress test

The hypothesis is not a disguised consequence of the fact that each `c_n` is
a Jordan embedding.  A full Jordan curve has winding multiplicity one, but a
subarc closed by its endpoint chord can have arbitrarily large multiplicity.

For an explicit scale, take `N` inward turns in a disk of radius `r`, with

```text
rho(theta)=r(1-theta/(4 pi N)),    0<=theta<=2 pi N.
```

The endpoints lie on the same ray, so close the arm by the radial chord.  The
origin is not on this loop, and the spiral changes its polar angle by exactly
`2 pi N`, while the radial chord has a constant polar angle.  Hence

```text
wind(L,0)=N.                                                 (4)
```

This already proves that the required pointwise bound is at least `N`; no
informal count of annular faces is needed.  The arm can be completed to a
Jordan curve by following a sufficiently close disjoint return arm and adding
short end caps (then smoothing the caps).  It is therefore genuinely a
subarc of a smooth Jordan embedding, not merely an immersed-loop example.
Meanwhile

```text
integral_arm lambda_0
  = (1/2) integral_0^(2 pi N) rho(theta)^2 dtheta
  = (7 pi/12) N r^2.                                      (5)
```

Choosing `N` comparable to `r^(-2)` makes (5) order one while `r->0`.  A
nearby return arm, traversed in reverse and separated by
`h=r/(100N)`, makes a thin Jordan strip.  The two arm actions cancel up to

```text
(3 pi/2) N r h - pi N h^2 = O(r^2),                         (6)
```

so the full Jordan domain can have vanishing local area even though the
primitive makes an order-one excursion along one arm.

Thus the winding hypothesis correctly rejects the critical action bubble:
here `K` must grow like `N`.  Conversely, replacing the pointwise assumption
by a bound only on the signed integral of the winding function is insufficient,
because (6) exhibits cancellation between large opposite subarc actions.

## Scope and unresolved variants

The proof uses the **pointwise absolute multiplicity** bound, not merely

```text
|integral wind| <= constant
```

and not merely the global Jordan winding bound.  It also uses a common
parametrized modulus; Hausdorff convergence of images alone does not supply
one.  No claim is made here that a given rough limiting curve admits smooth
approximants satisfying the hypothesis.  Establishing such an approximation
theorem for a genuinely new curve class is a separate problem.
