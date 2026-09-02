# Square Peg #125: a finite-2-variation graph beyond the vanishing class

Status: `sketch`.

This note gives an explicit Jordan curve of finite 2-variation which is not of
vanishing 2-variation, but whose chord-closed subarcs have a uniform vanishing
absolute winding-mass modulus and whose Liouville primitive is elementary.
It isolates a genuine gap between variation-based sufficient hypotheses and
the local planar quantity needed for primitive compactness.

Frozen PRs #115, #118, #119, #122, and #123 are not premises.

## 1. The lacunary graph

On `[0,2 pi]`, put

```text
g(t)=sum_(i>=0) 2^(-i/2) sin(2^i t).                       (1)
```

The series converges uniformly.  If `h=|t-s|` and `m` is chosen so that
`2^(-m-1)<h<=2^(-m)`, then

```text
sum_(i<=m) 2^(-i/2)|sin(2^i t)-sin(2^i s)|
 <= h sum_(i<=m)2^(i/2) <= C sqrt(h),

sum_(i>m) 2^(-i/2)|sin(2^i t)-sin(2^i s)|
 <= 2 sum_(i>m)2^(-i/2) <= C sqrt(h).                     (2)
```

Thus `g` is `1/2`-Holder.  For every partition `D`,

```text
sum_D |Delta g|^2 <= C^2 sum_D Delta t = 2 pi C^2,         (3)
```

so `g` has finite 2-variation.

This classical lacunary function is also the explicit strict-inclusion
example recorded by Friz--Victoir, *A Note on the Notion of Geometric Rough
Paths*, [arXiv:math/0403115](https://arxiv.org/abs/math/0403115), concluding
discussion on PDF p. 22, for
`C^(0,p-var) subsetneq C^(p-var)`.  For completeness, the failure of
vanishing 2-variation is checked directly next.

## 2. A fixed fine-mesh quadratic mass

Let

```text
D_n={t_j=2 pi j/2^n: 0<=j<=2^n}.                           (4)
```

At these nodes every summand with `i>=n-1` vanishes.  For `i<n-1`, the
increment sequences of the distinct dyadic Fourier modes are orthogonal in
`R^(2^n)`.  (This is the finite geometric-series identity for the exponentials
`exp(2 pi i qj/2^n)`; taking real and imaginary parts gives the assertion.)
The `i=n-2` term alone has node values

```text
2^(-(n-2)/2) sin(pi j/2),
```

whose consecutive squared increments sum to

```text
2^n 2^(-(n-2))=4.                                         (5)
```

Orthogonality therefore gives

```text
sum_(j=0)^(2^n-1)|g(t_(j+1))-g(t_j)|^2 >=4,               (6)
```

while `mesh(D_n)=2 pi/2^n->0`.  Hence `g` is not of vanishing
2-variation.  The same calculation also proves that `g` has infinite total
variation.  Indeed, (2) gives

```text
max_j |Delta_j g| <= C mesh(D_n)^(1/2),
sum_j |Delta_j g|
 >= (sum_j |Delta_j g|^2)/(max_j |Delta_j g|)
 >= 4/(C mesh(D_n)^(1/2)) -> infinity.                    (6a)
```

Thus its graph is nonrectifiable.

Let `M>1+sum_(i>=0)2^(-i/2)`.  Close the graph

```text
G={(t,g(t)):0<=t<=2 pi}
```

by the three segments

```text
(2 pi,g(2 pi))->(2 pi,-M)->(0,-M)->(0,g(0)).               (7)
```

Since `g(0)=g(2 pi)=0`, this is a Jordan curve `C`.  The monotone first
coordinate shows that the graph is injective, and the closing arc lies below
it except at the two endpoints.  Equations (3) and (6), together with the
finite-variation closing arc, show

```text
C has finite 2-variation but C notin C^(0,2-var).           (8)
```

## 3. Exact winding mass of every chord-closed graph subarc

Fix arbitrary `0<=a<b<=2 pi`.  Let `ell_(a,b)` be the affine function whose
graph is the chord joining `(a,g(a))` to `(b,g(b))`.  Orient the graph subarc
from `a` to `b` and the chord back from `b` to `a`, obtaining a continuous
closed loop `L_(a,b)` (the chord may cross the graph).

Its winding multiplicity has the following vertical-section description:

```text
|Ind(L_(a,b),(x,y))|
 = 1 if a<x<b and y lies strictly between g(x) and ell_(a,b)(x),
 = 0 otherwise,                                             (9)
```

away from the loop.  To prove this without any rectifiability assumption,
apply the orientation-preserving affine shear
`(x,y)->(x,y-ell_(a,b)(x))`.  The chord becomes the `x`-axis.  The open set on
which `g-ell_(a,b)` is nonzero is a countable union of intervals.  On each
component the graph, followed by the corresponding axis segment, is a Jordan
loop, with orientation given by the sign of `g-ell_(a,b)`.  The original loop
is the concatenation of these lobes, with the remaining axis pieces cancelling
topologically.  Additivity and local constancy of winding number give (9).
This includes every chord crossing and does not use currents along the rough
graph.

Fubini now gives the exact identity

```text
integral_R2 |Ind(L_(a,b),z)| dz
 = integral_a^b |g(x)-ell_(a,b)(x)| dx.                    (10)
```

Because an affine interpolant stays between its endpoint values,

```text
|g(x)-ell_(a,b)(x)| <= osc(g;[a,b]) <= C(b-a)^(1/2).
```

Consequently every graph subarc, including arbitrary partial lacunary
scales, satisfies the uniform local estimate

```text
integral_R2 |Ind(L_(a,b),z)| dz <= C(b-a)^(3/2).           (11)
```

Thus local absolute winding mass vanishes even though the fine-mesh
2-variation functional stays bounded below by `2` along (4).

The same observation is more general: for the graph of any continuous
function `f`, (10) holds and its right side is at most
`(b-a) osc(f;[a,b])`.  No variation hypothesis is needed.

## 4. Liouville primitives and smooth approximation

For the cotangent Liouville form `lambda=y dx`, the graph has the explicit
primitive

```text
F(t)=integral_0^t g(x) dx.                                 (12)
```

In particular,

```text
|F(b)-F(a)| <= ||g||_infinity (b-a).                       (13)
```

On the chord-closed loop, the signed action is

```text
integral_(L_(a,b)) lambda
 = integral_a^b (g(x)-ell_(a,b)(x)) dx,                    (14)
```

whose absolute value is bounded by (11).  Equations (10)--(14) show directly
that neither signed-action compactness nor absolute winding-mass compactness
requires vanishing local 2-variation for this curve.

For an approximation statement, let `g_n` be the partial sums in (1).  Their
graphs converge uniformly to the graph of `g`, and their normalized
primitives

```text
F_n(t)=integral_0^t g_n(x) dx
```

converge uniformly to `F`.  Close the graphs by (7).  Round the finitely many
corners and graph/closure seams inside disjoint balls of total removed length
`epsilon_n->0`.  The resulting smooth Jordan curves remain uniformly close.
Moreover the primitive error caused by rounding tends uniformly to zero:
the `x`-variation of every graph-plus-rectangular closure is uniformly bounded
by `4 pi`, while the pointwise and `x`-variation errors of the rounding tend
to zero.  The elementary estimate

```text
|integral y_Q dx_Q-integral y_P dx_P|
 <= ||y_Q-y_P||_infinity Var(x_Q)
    +||y_P||_infinity Var(x_Q-x_P)                         (15)
```

applies on every initial parameter interval.  Hence this curve admits smooth
Jordan approximants with locally uniformly convergent lifted primitives,
despite (8).  Explicitly, if `H_n,H` are the primitives on one period and
`A_n=H_n(1), A=H(1)`, then `A_n->A` and

```text
H_n(k+r)=k A_n+H_n(r),       k in Z, 0<=r<1,               (15a)
```

upgrade uniform convergence on one period to local uniform convergence on
the lifted real parameter.

Therefore Asano--Ike, *The rectifiable rectangular peg problem*,
[arXiv:2412.21057v3](https://arxiv.org/abs/2412.21057v3), Theorem 1.1,
applies to this explicit curve: it inscribes a rectangle of every prescribed
diagonal angle, and in particular a positive square.  This conclusion remains
`sketch` here pending the repository's verification-critical review.

## 5. A more violent elementary stress test

There is also a completely elementary infinite-2-variation version.  On
shrinking disjoint intervals `I_k`, take nonnegative triangular waves of
amplitude `r_k->0` with `2N_k r_k^2>=1`.  The extrema partitions give one
unit of squared variation on every block and therefore infinite global
2-variation; arbitrarily fine meshes still see one full block.  Nevertheless,
for every chord-closed subarc the graph identity (10) gives

```text
integral |Ind| <= |b-a| osc(f;[a,b]) ->0                  (16)
```

uniformly by continuity, and `integral f dx` remains the primitive.  This
stress test shows why a local-2-variation hypothesis can be far stronger than
the planar winding/action condition it is used to guarantee.

## 6. Primary-literature boundary

The relevant neighboring results do not subsume the graph calculation:

1. Banchoff--Pohl, *A generalization of the isoperimetric inequality*,
   [J. Differential Geometry 6 (1971),
   175--192](https://doi.org/10.4310/JDG/1214430403), controls the `L^2`
   winding norm of a rectifiable closed curve by its length.  It does not apply
   to the nonrectifiable graph above.
2. Galvin, *An elementary proof of an isoperimetric inequality for paths with
   finite p-variation*, [arXiv:1801.00303](https://arxiv.org/abs/1801.00303),
   gives explicit `L^q` winding bounds for `p<2` and `q<2/p`.  The endpoint
   `p=2` is excluded.
3. Cufí--Verdera, *A general form of Green Formula and Cauchy Integral
   Theorem*, [arXiv:1306.6832](https://arxiv.org/abs/1306.6832), treats closed
   rectifiable curves through integrable winding.  Equation (10) instead
   computes winding topologically for this nonrectifiable graph loop.
4. Yang, *Notes on area operator, geometric 2-rough paths and Young integral
   when p^(-1)+q^(-1)=1*,
   [arXiv:1204.0112](https://arxiv.org/abs/1204.0112), proves that the area
   operator is unbounded at the critical index and gives vanishing-2-variation
   paths whose polygonal areas have arbitrary or divergent limits.  Those
   examples show that vanishing 2-variation alone does not create a canonical
   area for arbitrary planar paths; the graph identity `dx=dt` is the extra
   structure here.
5. Boedihardjo--Geng, *Simple Piecewise Geodesic Interpolation of Simple and
   Jordan Curves with Applications*,
   [arXiv:1309.1576](https://arxiv.org/abs/1309.1576), Theorem 2.2, supplies
   mesh-fine simple polygonal interpolation for every Jordan curve.  It does
   not by itself give primitive convergence outside the Wiener/Yang closure.
   For this graph, equations (12)--(15) provide that missing convergence
   directly.

Thus the proposed weaker condition is not a replacement for the abstract
continuous-Legendrian-lift hypothesis in Asano--Ike; it is a concrete
graph-specific verification mechanism for that hypothesis.

## 7. Scope

The construction does not prove a general Square Peg theorem beyond
`C^(0,2-var)`.  It proves only the explicit example, subject to review, and
supplies a boundary test and a candidate weaker
hypothesis: direct uniform control of chord-closed absolute winding mass (or,
for primitive compactness alone, direct equicontinuity of Liouville actions).
Whether that condition can be enforced by simple Jordan approximation for a
larger intrinsic class remains open here.
