# Square Peg #124: a local algebraic winding condition

Status: `sketch`.

This note isolates the weakest local winding quantity needed to compactify
Liouville primitives, gives a directly checkable condition on one sequence of
simple polygonal interpolants, and shows that condition is strictly broader
than vanishing 2-variation.  It does not use PRs #115, #118, #119, #122, or
#123 as premises.

## 1. The exact local quantity

Write

```text
lambda_0=(x dy-y dx)/2.
```

Let `a_n:R->R^2` be period-one smooth Jordan parametrizations converging
uniformly to a period-one Jordan parametrization `c`.  Uniform convergence
makes the family uniformly bounded and equicontinuous.  For `s<t<s+1`, close
the embedded arc `a_n|[s,t]` by the oriented chord from `a_n(t)` back to
`a_n(s)` and call the resulting rectifiable loop `L_(n;s,t)`.  Green's formula
gives

```text
integral_(L_(n;s,t)) lambda_0
 = integral_R2 Ind(L_(n;s,t),z) dz.                         (1)
```

If `F_n(0)=0` and `dF_n=a_n^*lambda_0`, direct parametrization of the chord
gives

```text
F_n(t)-F_n(s)
 = integral_R2 Ind(L_(n;s,t),z) dz
   - det(a_n(t),a_n(s))/2.                                  (2)
```

The chord term has a common modulus because the maps are uniformly bounded
and equicontinuous.  Consequently, the exact remaining condition is

```text
lim_(delta->0) sup_n sup_(0<=t-s<=delta)
 |integral_R2 Ind(L_(n;s,t),z) dz| = 0.                     (AW)
```

Thus (AW) is sufficient for equicontinuity of the normalized primitives.
Conversely, (2) shows that primitive equicontinuity implies (AW).  In this
precise sense (AW), which controls **algebraic winding mass**, is the weakest
local winding condition for the chosen approximating sequence.  The more
familiar absolute condition

```text
sup_n sup_(t-s<=delta) integral_R2 |Ind(L_(n;s,t),z)| dz ->0 (3)
```

is sufficient but not logically necessary: oppositely oriented lobes may
cancel in (1).

Equations (1)--(2), Arzela--Ascoli, and the period identity
`F_n(k+r)=kF_n(1)+F_n(r)` show that a subsequence of `F_n` converges locally
uniformly on `R`.  Hence any Jordan curve admitting such an approximation
satisfies the primitive-compactness hypothesis in Asano--Ike,
*The rectifiable rectangular peg problem*,
[arXiv:2412.21057v3](https://arxiv.org/abs/2412.21057), Theorem 1.1, after the
elementary exact-form conversion from `lambda_0` to their `y dx`.
Explicitly, `y dx=-lambda_0+d(xy/2)`, and uniform convergence of the curves
makes the added endpoint functions converge locally uniformly.

## 2. A useful anisotropic absolute-mass condition

There is a geometric condition stronger than (AW) which does not mention
variation.  For an injective rectifiable arc `a:[s,t]->R^2`, let `S` be its
endpoint chord.  The open set `{u in (s,t):a(u) notin S}` is a countable union
of disjoint intervals `(alpha_j,beta_j)`.  Close each excursion by the
corresponding subsegment of `S`, and call that Jordan loop `E_j`.  Define the
convex-excursion area

```text
H(a;[s,t])=sum_j area(conv(E_j)).                           (4)
```

As rectifiable one-currents, the chord-closed arc is the mass-convergent sum
of the `E_j`: the residual is a compact cycle supported on a line and hence is
zero.  If `Omega_j` is the bounded Jordan domain of `E_j`, uniqueness of the
compactly supported planar filling gives

```text
Ind(L,.)=sum_j sign(E_j) 1_(Omega_j)       almost everywhere.
```

Containment `Omega_j subset conv(E_j)` therefore proves, directly,

```text
integral_R2 |Ind(L,z)| dz
 <= sum_j area(Omega_j)
 <= H(a;[s,t]).                                             (5)
```

Thus the geometric condition

```text
sup_n sup_(t-s<=delta) H(a_n;[s,t]) -> 0                    (CH)
```

implies (3), hence (AW).  It is robust against same-orientation spiral
bubbles, but it can be unnecessarily strong when many thin lobes cancel.
Unlike the coarser bound
`H<=(pi/4)sum_j diam(E_j)^2`, (CH) retains anisotropy: a thin excursion of
width `w` and height `r` costs order `wr`, not `r^2`.

## 3. A polygonal signed-area modulus on the limiting curve

For a lifted interval `I=[s,t]` of length below one and a partition
`P={s=u_0<...<u_m=t}`, define the chord-closed polygonal area

```text
A(c;P)
 = (1/2) sum_(i=0)^(m-1)
     det(c(u_i)-c(s),c(u_(i+1))-c(s)).                      (6)
```

Set

```text
alpha_c(delta)
 = sup {|A(c;P)|: 0<=t-s<=delta, P a partition of [s,t]}.
```

Our geometric hypothesis is

```text
alpha_c(delta)->0 as delta->0.                              (VA)
```

This is parametrization-invariant under orientation-preserving circle
homeomorphisms.  It controls algebraic, not absolute, area.

Choose mesh-fine simple polygonal interpolants `P_n=c^(D_n)`.  Their existence
as parametrized Jordan polygons is Boedihardjo--Geng,
*Simple Piecewise Geodesic Interpolation of Simple and Jordan Curves with
Applications*, [arXiv:1309.1576v2](https://arxiv.org/abs/1309.1576), Theorem
2.2.  Put `h_n=mesh(D_n)` and let `omega` be a modulus of continuity for `c`.

For arbitrary `s<t`, augment the polygonal subarc `P_n|[s,t]` by all nodes of
`D_n` lying between its endpoints.  Its internal vertices are values of `c`.
Replacing its two endpoint values `P_n(s),P_n(t)` by `c(s),c(t)` changes the
closed polygonal area by at most

```text
2 omega(h_n) omega(t-s+2h_n).                               (7)
```

Indeed, changing one vertex by `e` changes the shoelace sum by
`det(e,v_next-v_previous)/2`; both neighboring vertices lie in a parameter
interval of length at most `t-s+2h_n`.  The polygon after both replacements
is exactly a sample polygon of `c` on `[s,t]`.  Therefore

```text
|integral_(closed P_n|[s,t]) lambda_0|
 <= alpha_c(t-s)+2 omega(h_n)omega(t-s+2h_n).                (8)
```

Discarding finitely many `n`, (VA) makes the right side uniformly small on
short intervals.  Each discarded polygon has its own vanishing local area
modulus.  Round the finitely many corners of `P_n` inside disjoint balls,
choosing the `1`-variation error so small that the resulting smooth Jordan
curve `a_n` changes every Liouville integral by at most `1/n`; this follows
as follows.  On any subinterval, bilinearity and
`det(q,dq)-det(p,dp)=det(q-p,dq)+det(p,d(q-p))` give

```text
|integral_q lambda_0-integral_p lambda_0|
 <= (1/2)||q-p||_infinity Var_1(q)
    +(R/2)||q-p||_(1-var),                                  (9)
```

with `R` a common image bound, applied separately for each finite polygon.
The endpoint chord changes by at most a further constant times
`R||q-p||_infinity`.
The errors may be chosen after `P_n`, so no uniform length bound is needed.
Equations (8)--(9) prove (AW) for the smooth Jordan approximants.

## 4. Strictness beyond vanishing 2-variation

Here is an explicit mechanism showing that (VA) is genuinely weaker.  On
pairwise adjacent intervals

```text
I_k=[2^(-k-1),2^(-k)],   ell_k=2^(-k-1),
r_k=exp(-k^2),           N_k=ceil(1/r_k^2),                 (10)
```

let `f` be the nonnegative triangular wave with `N_k` teeth of height `r_k`
on `I_k`, zero at every tooth endpoint, and put `f=0` on `[1/2,1]` and at
zero.  Then `g(t)=(t,f(t))` is an injective continuous graph.  The extrema
partition of block `I_k` gives

```text
||g||_(2-var;I_k)^2 >= 2N_k r_k^2 >=2.                     (11)
```

Combining the extrema of the first `K` blocks in one ordered partition shows
that the full graph does not even have finite 2-variation.

Nevertheless every sample polygon of `g` over `[s,t]` is the graph of a
piecewise-linear function over the first coordinate.  Its chord-closed signed
area is the integral of that graph minus its endpoint chord, so

```text
|A(g;P)| <= (t-s) osc(f;[s,t])                              (12)
```

for every partition `P`.  Uniform continuity of `f` makes the right side
vanish uniformly with `t-s`.

Close `g` from `(1,0)` to `(0,0)` by the three segments

```text
(1,0)->(1,-1)->(0,-1)->(0,0).                              (13)
```

Parametrize the four pieces on fixed subintervals of one period.  This is a
Jordan curve.  Away from the four seams, (12) or linearity proves (VA).
Across a seam, insert the seam into the sample polygon; the extra triangle is
bounded by the product of two local oscillations and also tends to zero.
Thus the closed Jordan parametrization satisfies (VA) while having infinite
2-variation.

It also admits smooth Jordan approximants satisfying the stronger (CH).
First truncate all blocks near zero, then smooth the resulting finite
piecewise-linear function without changing the first coordinate; denote the
smooth graph functions by `f_n`, chosen so that `f_n->f` uniformly.  Close
the graphs by (13) and round the four fixed corners.  The resulting smooth
Jordan parametrizations converge uniformly, hence have one common modulus
`Omega`.

Consider arbitrary endpoints on one graph piece and its endpoint chord.
Every chord excursion projects to a disjoint open interval on the `x`-axis.
If its projected width is `d_j`, both the graph and chord lie in a vertical
range of size at most `Omega(delta)`, and hence

```text
area(conv(E_j)) <= d_j Omega(delta).
```

The projected excursion intervals are disjoint, so `sum_j d_j<=C delta`
under the fixed linear parametrization.  Consequently

```text
H(a_n;[s,t]) <= C delta Omega(delta)                         (14)
```

uniformly in `n`.  On a straight closing piece the quantity is zero.  For a
short interval crossing one of the finitely many seams, all excursions except
possibly the one containing the seam remain excursions of a single graph
piece and obey (14).  The exceptional excursion, if present, lies in the
convex hull of a set of diameter at most `2Omega(delta)`, so its convex area
is at most `pi Omega(delta)^2`.  The corner roundings can be chosen as graphs
in suitable local coordinates and their scales can tend to zero; uniform
convergence to the fixed corner parametrization supplies the same common
modulus.  This proves (CH).
Hence both (CH) and (VA) strictly extend beyond `C^(0,2-var)`.

## 5. Bubble stress tests and limitations

1. **Same-orientation spiral bubble.**  Put `N_k` turns of radius comparable
   to `rho_k` into a parameter interval shrinking to a point, with
   `N_k rho_k^2` bounded below.  A partition following the turns has
   chord-closed algebraic area comparable to `pi N_k rho_k^2`; (VA) fails.
   Uniform convergence and shrinking image diameter alone are therefore
   insufficient.

2. **Alternating action bubbles.**  If adjacent lobes have opposite
   orientations, their total signed action can vanish while
   `integral|Ind|` and the convex-excursion content (4) stay large.  Such a family
   may satisfy the exact primitive condition (AW): absolute winding control
   is sufficient, not necessary.  Condition (VA), however, takes a supremum
   over all subintervals and all sample partitions, so cancellation of a
   complete packet does not help if a partial packet retains macroscopic
   action.

3. **Dependence on parametrized order.**  (VA) is geometric under increasing
   reparametrization, but it is not a Hausdorff-image condition.  This is
   unavoidable because the primitive and winding multiplicities depend on
   traversal order.

4. **No hidden status promotion.**  The construction and implications above
   remain a `sketch` pending independent checking, especially the endpoint
   perturbation estimate (7), smoothing estimate (9), arbitrary-chord
   estimate (14), and periodic seam assembly.  No frozen Square Peg sketch
   is assumable here.
