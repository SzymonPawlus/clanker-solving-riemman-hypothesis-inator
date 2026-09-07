# Square Peg #120: the vanishing critical 2-variation class

Status: `sketch`.

This note proves a self-contained implication, modulo the explicitly cited
primary theorems below:

> Every planar Jordan parametrization of vanishing 2-variation admits a
> continuous Legendrian lift in the sense of Asano--Ike and therefore
> inscribes a rectangle of every prescribed diagonal angle.  In particular,
> it inscribes a square.

The winding estimate used here is proved again below.  PRs #115, #118, and
#119 are frozen sketches and are neither premises nor dependencies of this
note.

## 1. Exact critical-variation hypothesis

Identify `S^1` with `R/Z`, and write a Jordan parametrization as a continuous
map

```text
c : R -> R^2,       c(t+1)=c(t),
```

which is injective on `[0,1)`.  For a path `x` on an interval `I=[a,b]`, set

```text
||x||_(2-var;I)^2
  = sup_P sum_i |x(t_(i+1))-x(t_i)|^2,                       (1)
```

where the supremum is over all finite ordered partitions of `I`.  For a
partition `D={0=t_0<...<t_m=1}`, write

```text
mesh(D)=max_i(t_(i+1)-t_i)
```

and define the fine-mesh functional

```text
w_2(c,delta)^2
 = sup {sum_i |c(t_(i+1))-c(t_i)|^2 : mesh(D)<=delta}.       (2)
```

The hypothesis `c in C^(0,2-var)` means precisely

```text
w_2(c,delta) -> 0 as delta -> 0.                             (3)
```

This is the Wiener/Yang definition of **vanishing 2-variation**, not merely
finite 2-variation.

A useful consequence will be needed repeatedly.  If `I` is any lifted
interval of length at most `delta<=1/2`, then

```text
||c||_(2-var;I) <= sqrt(2) w_2(c,delta).                     (4)
```

For an interval not crossing an integer, take any partition of `I` and extend
it on the complementary parameter arc to a partition of the full period
having mesh at most `delta`; this even gives the bound without `sqrt(2)`.  If
`I` crosses an integer, insert that seam into its partition.  The insertion
may split one increment `u+v`, and
`|u+v|^2<=2(|u|^2+|v|^2)`; all other increments are unchanged.  After reducing
modulo one, extend the two seam pieces together to a full-period partition of
mesh at most `delta`.  Its squared-increment sum is at most
`w_2(c,delta)^2`, so the original sum is at most twice that quantity.  Taking
the supremum proves (4).  Thus the fixed-base mesh definition supplies the
uniform local lifted-interval modulus, with the harmless seam constant shown
explicitly.

## 2. Simple polygonal interpolation in 2-variation

For a partition `D`, let `c^D` be the parametrized piecewise-linear
interpolant that agrees with `c` at every point of `D` and is affine on every
partition interval.

Boedihardjo--Geng, *Simple Piecewise Geodesic Interpolation of Simple and
Jordan Curves with Applications*,
[arXiv:1309.1576v2](https://arxiv.org/abs/1309.1576), Theorem 2.2, proves that
for every `epsilon>0` there is a partition `D_epsilon` with
`mesh(D_epsilon)<epsilon` whose interpolant is a simple polygonal Jordan
curve.  The theorem respects the given parametrization; it is not merely a
Hausdorff approximation of images.

Yang, *Notes on area operator, geometric 2-rough paths and Young integral
when p^(-1)+q^(-1)=1*,
[arXiv:1204.0112v1](https://arxiv.org/abs/1204.0112), Notation 9 and equation
(5), records Wiener's characterization: for `1<p<infinity`, a path is in
`C^(0,p-var)` exactly when its piecewise-linear interpolants converge to it in
`p`-variation as the partition mesh tends to zero.

Choose the Boedihardjo--Geng partitions with mesh tending to zero and write
`P_n=c^(D_n)`.  The two cited results give simultaneously

```text
P_n is a parametrized polygonal Jordan curve,
||P_n-c||_(2-var;[0,1]) -> 0.                               (5)
```

The variation seminorm alone ignores a constant translation, but the
interpolants agree with `c` at `0`; hence (5) also gives uniform convergence.

## 3. Smoothing without losing simplicity or 2-variation convergence

We use the following elementary rounding lemma.

**Corner-rounding lemma.**  If `P:S^1->R^2` is a parametrized simple polygon
and `epsilon>0`, there is a smooth Jordan embedding `Q:S^1->R^2`, with the
same orientation, such that

```text
||Q-P||_(1-var;[0,1]) < epsilon.                            (6)
```

To prove it, choose around each of the finitely many vertices a closed ball
which is disjoint from all other vertex balls and all nonincident edges.
Shrink the balls so that the sum of the lengths of incident edge pieces
inside them is as small as desired.  Within each ball replace the two radial
edge pieces by a smooth embedded rounding lying in the local sector occupied
by the polygonal arc, choosing the appropriate sector also at a reflex
vertex, and matching the unchanged straight pieces to all orders at the exit
points.  Such a rounding is obtained by smoothing the two-ray corner with a
compactly supported bump in sector-adapted coordinates.  The replacements
stay in disjoint balls and meet the old polygon only at their two exit
points, so the result remains a Jordan embedding.

Parametrize each replacement on the parameter interval occupied by the
removed edge pieces and leave `P` unchanged elsewhere.  On one such interval,
the variation of the pointwise difference is at most the sum of the lengths
of the old and new pieces.  The new piece can be chosen with length bounded
by a fixed multiple of the removed length.  Summing over the finite disjoint
balls proves (6).  The same construction at the parameter seam makes the
periodic map smooth there.

Apply the lemma to `P_n`, choosing the error `epsilon_n->0`, and call the
result `c_n`.  Since `||x||_(2-var)<=||x||_(1-var)`, Minkowski's inequality
and (5)--(6) give

```text
||c_n-c||_(2-var;[0,1]) -> 0,                              (7)
c_n -> c uniformly.                                        (8)
```

If the rounding moves the parameter basepoint, its displacement is bounded
by the same local rounding scale; alternatively one may prescribe a point in
the interior of an unchanged edge as basepoint.  Thus the seminorm statement
in (7) genuinely implies (8), with no hidden translation.

## 4. One uniform local 2-variation modulus

Define

```text
nu(delta)
 = sup_n sup {||c_n||_(2-var;[s,t]) : 0<=t-s<=delta},       (9)
```

where intervals are taken on the lifted periodic parameter and
`delta<=1/2`.  Then

```text
nu(delta) -> 0 as delta -> 0.                               (10)
```

Here is the quantifier proof.  Put
`e_n=||c_n-c||_(2-var;[0,1])`.  For every short interval `I`, restriction and
Minkowski give

```text
||c_n||_(2-var;I)
 <= ||c||_(2-var;I)+||c_n-c||_(2-var;I)
 <= sqrt(2)(w_2(c,|I|)+e_n).                               (11)
```

For a seam-crossing interval the restriction of the periodic difference
`c_n-c` costs the same `sqrt(2)` insertion factor as in (4), which explains
the second term in (11).  Given `epsilon>0`, first choose `N` so that
`e_n<epsilon/(2sqrt(2))` for every `n>=N`,
and then choose `delta` so that
`w_2(c,delta)<epsilon/(2sqrt(2))`.  This controls the tail.  Each of the
finitely many smooth maps `c_1,...,c_(N-1)` is Lipschitz,
say with constant `L_j`, and for an interval of length `delta`,

```text
sum_i |Delta c_j|^2
 <= (max_i |Delta c_j|) sum_i |Delta c_j|
 <= L_j^2 delta^2.
```

Their finite maximum therefore also tends to zero.  This proves (10).

## 5. Embedded arcs: absolute winding mass at critical variation

The next lemma is included in full so that no frozen PR is a premise.

**Embedded-arc lemma.**  Let `a:[u,v]->R^2` be an injective rectifiable arc.
Let `S=[a(u),a(v)]`, oriented from `a(v)` back to `a(u)`, and let `L=a+S` be
the resulting closed rectifiable loop.  Then

```text
integral_R2 |Ind(L,z)| dz
 <= (pi/4) ||a||_(2-var;[u,v])^2.                           (12)
```

**Proof.**  The open set

```text
U={tau in (u,v): a(tau) notin S}
```

is the disjoint union of countably many intervals `(alpha_j,beta_j)`.  The
two endpoint images lie on `S` and are distinct by injectivity.  The open
excursion avoids the entire chord, so the excursion followed by the chord
segment from `a(beta_j)` to `a(alpha_j)` is an oriented Jordan loop `E_j`.
No transversality is required; the excursion may cross the line supporting
`S` outside the finite chord.

Regard rectifiable paths as integral one-currents.  The excursion currents
are absolutely summable in mass because

```text
Mass(E_j)
 <= length(a|_[alpha_j,beta_j])+|a(beta_j)-a(alpha_j)|
 <= 2 length(a|_[alpha_j,beta_j]),
```

and the parameter intervals are disjoint.  The residual
`L-sum_j E_j` is a compact one-cycle supported on the line containing `S`.
It is zero: the restriction of every smooth one-form to that line has a
one-dimensional primitive, on which a cycle vanishes.  Therefore

```text
L=sum_j E_j                                                     (13)
```

as currents.  This also accounts for intervals or Cantor subsets on which
the original arc lies in `S`.

Let `Omega_j` be the bounded Jordan domain of `E_j`.  Adding the excursion's
chord does not enlarge its convex hull, so

```text
diam(E_j)=diam(a([alpha_j,beta_j])).
```

For any finite family of excursions, choose two ordered points in each
parameter interval whose image distance approaches that excursion diameter.
Combining all chosen points in their parameter order into one partition of
`[u,v]` proves, and monotone passage to the countable family gives,

```text
sum_j diam(E_j)^2 <= ||a||_(2-var;[u,v])^2.                 (14)
```

The planar isodiametric inequality now yields

```text
sum_j area(Omega_j)
 <= (pi/4) sum_j diam(E_j)^2
 <= (pi/4)||a||_(2-var;[u,v])^2.                            (15)
```

Thus the signed Jordan fillings
`sum_j sign(E_j)[Omega_j]` converge in mass and have boundary `L` by (13).
The compactly supported planar two-current with boundary `L` is unique: the
difference of two such fillings is a compactly supported two-cycle in
`R^2`, hence vanishes by the constancy theorem.  Its multiplicity is the
usual winding function, so almost everywhere

```text
Ind(L,.)=sum_j sign(E_j) 1_(Omega_j).
```

Taking absolute values, integrating, and using (15) proves (12).  Nested or
overlapping lobe interiors cause no problem because the current identity is
signed while the estimate uses the triangle inequality.  QED.

## 6. Compact Liouville primitives

Use the symmetric Liouville form

```text
lambda_0=(x dy-y dx)/2,       d lambda_0=dx wedge dy.
```

On the lifted parameter define

```text
F_n(0)=0,
F_n(t)-F_n(s)=integral_[s,t] c_n^*lambda_0.                 (16)
```

Uniform convergence makes the images lie in one ball `B(0,R)`.  For
`0<=t-s<=delta<=1/2`, close the injective subarc from `s` to `t` by the chord
from `q=c_n(t)` to `p=c_n(s)`.  The generalized Green formula for arbitrary
closed rectifiable planar curves gives

```text
integral_L lambda_0=integral_R2 Ind(L,z) dz.                (17)
```

For a primary source at this regularity, see Cufí--Verdera, *A general form
of Green Formula and Cauchy Integral Theorem*,
[arXiv:1306.6832](https://arxiv.org/abs/1306.6832), main theorem.  Taking
`f(z)=conjugate(z)` in their formula gives (17), since
`partial_bar f=1` and `integral conjugate(z) dz=2i integral lambda_0` on a
closed curve.

The embedded-arc lemma and (9) bound the closed-loop action by

```text
|integral_L lambda_0| <= (pi/4)nu(delta)^2.                 (18)
```

Direct parametrization of the chord gives

```text
integral_[q,p] lambda_0=det(q,p)/2=det(q,p-q)/2,
|integral_[q,p] lambda_0| <= (R/2)|p-q| <= (R/2)nu(delta).  (19)
```

Equations (16)--(19) give the common modulus

```text
|F_n(t)-F_n(s)|
 <= (pi/4)nu(delta)^2+(R/2)nu(delta).                       (20)
```

Covering `[0,1]` by finitely many short intervals bounds `F_n` uniformly
there.  Arzelà--Ascoli supplies a subsequence converging uniformly on
`[0,1]` to a continuous `F`.  In particular the period actions
`A_n=F_n(1)` converge to `A=F(1)`.  Since

```text
F_n(k+r)=k A_n+F_n(r),       k in Z, 0<=r<1,                (21)
```

the convergence is locally uniform on all of `R`, with the analogous period
identity for `F`.  Relabel this subsequence.  It is still a sequence of smooth
Jordan embeddings converging uniformly to `c`.

## 7. Exact match to Asano--Ike and the rectangle conclusion

Asano--Ike, *The rectifiable rectangular peg problem*,
[arXiv:2412.21057v3](https://arxiv.org/abs/2412.21057), Theorem 1.1, states:
if a Jordan curve is the parametrized `C^0` limit of smooth Jordan curves and
the primitives of the pulled-back Liouville form along their lifted
parametrizations converge locally uniformly on `R`, then the limiting curve
inscribes a `theta`-rectangle for every `theta in (0,pi)`.

Their circle is written `R/(2 pi Z)` rather than `R/Z`; composing our maps
with `t -> t/(2 pi)` is an orientation-preserving linear reparametrization and
preserves all convergence statements.

Their cotangent-coordinate Liouville form is `lambda_AI=y dx`.  It differs
from the form used above only by a sign and an exact term:

```text
y dx=-lambda_0+d(xy/2).                                    (22)
```

If `G_n` denotes the primitive normalized at zero for `y dx`, then

```text
G_n(t)=-F_n(t)
       +(x_n(t)y_n(t)-x_n(0)y_n(0))/2.                      (23)
```

The first term converges locally uniformly by Section 6, and the endpoint
term does so by uniform convergence `c_n->c` and periodicity.  Hence the
exact primitive hypothesis of Asano--Ike Theorem 1.1 is satisfied.  The
theorem supplies an inscribed rectangle of every diagonal angle, with four
distinct boundary vertices (equivalently, the intersection is off the
diagonal rather than a degenerate rectangle).  At `theta=pi/2` its diagonals
are perpendicular, so this is a classical positive-size inscribed square.

## 8. Dependency and scope audit

The chain depends on the following cited results:

1. Boedihardjo--Geng Theorem 2.2: mesh-fine simple parametrized polygonal
   interpolation of a Jordan curve;
2. Yang equation (5): Wiener characterization by convergence of polygonal
   interpolants in 2-variation;
3. Cufí--Verdera's generalized Green formula for closed rectifiable curves;
4. Asano--Ike Theorem 1.1: continuous-Legendrian-lift criterion for all
   prescribed rectangle angles.

The corner smoothing, common local modulus, embedded-arc estimate, primitive
compactness, and exact-form conversion are proved within this note.  The
overall status remains `sketch` pending the repository's required independent
verification.  In particular, this note must not be used as an assumable
claim merely because its external dependencies are cited.

The result covers the precise Wiener/Yang class `C^(0,2-var)`.  It does not
claim that every path of finite 2-variation has vanishing 2-variation, nor
that an arbitrary uniformly convergent smooth approximation has the common
modulus (10).  The latter is false for critical shrinking spiral bubbles.
