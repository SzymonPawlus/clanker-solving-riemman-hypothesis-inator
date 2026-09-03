# Analytic equioscillation for asymmetric four-edge witnesses

**Issue:** #185.  **Status:** `sketch`; analytic reduction, not a universal-
cover lower-bound claim.  This directory is separate from the frozen Issue
#178 certificate and the Issue #182 candidate-specific analytic proof.

## 1. Setup and direct-motion domain

Let a convex four-edge open arc have traversed hull-edge tangent directions
`theta_0 < ... < theta_3 < theta_0+pi` and positive lengths
`l_0,...,l_3` summing to one.  Its traversal vertices are

\[
 p_0=0,\qquad p_{k+1}=p_k+l_k(\cos\theta_k,\sin\theta_k).
\]

Assume the closing vector `-p_4` is a fifth strict hull edge.  Write its
length and tangent direction as `l_4,theta_4`.  The five surface vectors are
the clockwise rotations of `l_i(cos theta_i,sin theta_i)` and sum to zero.
The closing edge is a hull edge only, not part of the worm, so the worm length
is exactly `sum_{i<4} l_i=1`.

Pin the unit segment horizontally.  Its half-turn symmetry gives the complete
direct-rotation domain `phi in [0,pi]`.  No reflection of the asymmetric worm
is identified.  The equilateral triangle has its independent direct-rotation
period `2pi/3`.

## 2. Positive circuits give all atomic balanced loads

For tangent unit vectors `u_i`, a load `x=(x_i)` is balanced when

\[
 x_i\ge0,\qquad \sum_i x_i u_i=0. \tag{1}
\]

The extreme rays of this cone have support at most three.  Indeed, on a
support of size at least four the `2 x k` direction matrix has a kernel of
dimension at least two; a sufficiently small signed kernel perturbation
splits the load into two nonproportional nonnegative balanced loads.  A
one-point support cannot balance.  A two-point support occurs only for an
antipodal pair.  In the generic no-antipodes case every extreme ray is
therefore a positive three-direction circuit.

For a cyclic triple `(i,j,k)` containing the origin in its direction triangle,
the ray is explicit:

\[
 (r_i,r_j,r_k)=
 (|\sin(\theta_k-\theta_j)|,
  |\sin(\theta_i-\theta_k)|,
  |\sin(\theta_j-\theta_i)|). \tag{2}
\]

The maximal circuit allocation under surface capacities is

\[
 x_s=\kappa r_s,\qquad
 \kappa=\min_{s\in\{i,j,k\}}{l_s\over r_s}. \tag{3}
\]

Equations (2)--(3) prove balance and capacity without solving an LP.  Every
balanced nonnegative load is a conic sum of these circuits (and antipodal
pairs when present).  Capacity can couple several rays, so this statement
does not assert that the maximal single circuits are every vertex of the
capacity polytope; it asserts exactly that they are a complete atomic menu of
legal analytic support allocations.

## 3. Triangle constants are finite algebraic minima

Fix any balanced allocation `x`.  If `n_i` are its outward normals, define

\[
 \tau(x)=\min_{\psi\in[0,2\pi/3]}
 {1\over2}\sum_i x_i h_T(R_{-\psi}n_i), \tag{4}
\]

where `T` is the equilateral triangle of side `1/2`.  Between crossings of a
loaded normal with one of the three triangle fan walls, (4)'s summand is one
positive sinusoid.  It is concave, so its minimum occurs at a fan crossing.
Rotational symmetry makes the three crossings belonging to a fixed loaded
normal equivalent.  Thus an allocation supported on `k` normals needs only
`k` candidate evaluations, not an angular search.  Explicitly, align each
loaded `n_i` in turn with the downward triangle normal and evaluate

\[
 {1\over2}\sum_jx_j\max\left{0,{q_{ij,x}\over2},
 {q_{ij,x}+\sqrt3q_{ij,y}\over4}\right}, \tag{5}
\]

where `q_ij` is `n_j` expressed in that aligned triangle frame.  The least of
these values is `tau(x)`.  Rational directions and loads put every candidate
in `Q(sqrt(3))`.

There is no hidden rotation operation in (5).  If the corresponding tangent
angles are `theta_i,theta_j`, direct dot/cross calculation gives

\[
 q_{ij}=(\sin(\theta_j-\theta_i),
         -\cos(\theta_j-\theta_i)). \tag{5a}
\]

Thus (2), (3), and (5a) are a fully symbolic recipe in pairwise sines and
cosines, including for an asymmetric circuit.

### Closed form for a symmetric three-ray circuit

One useful specialization has tangent directions `-theta,+theta,pi` and
balanced loads `1,1,2cos(theta)`, with `0<=theta<=pi/2`.  Put
`t=tan(theta/2)` and let `rho` be the unique root in `(7/10,71/100)` of

\[
 y^3-33y^2+27y-3=0. \tag{6}
\]

Direct substitution in (5) gives two distinct fan values (the two outer
normals agree).  Their formulas on the two support regimes are

\[
\begin{array}{c|cc}
 &t^2\le1/3&t^2\ge1/3\\ \hline
\text{outer-normal alignment}&
 {sc\over4}+{\sqrt3c^2\over4}&
 {sc\over4}+{\sqrt3(s^2-c^2)\over8}\\[1mm]
\text{closing-normal alignment}&{\sqrt3c\over4}&{s\over4},
\end{array}
\]

where `c=cos(theta),s=sin(theta)`.  The fan maxima change at `theta=pi/3`,
which is `t^2=1/3`; the formulas agree there.  In the first regime, subtracting
the closing value from the outer value gives
`c(s-sqrt(3)(1-c))/4 >= 0`, since
`s/(1-c)=cot(theta/2)>=sqrt(3)`.  Comparing the two second-regime values gives
the cubic threshold below.  Therefore the exact triangle floor is

\[
 f(\theta)=
 \begin{cases}
 {\sqrt3\cos\theta\over4},&0\le t^2\le1/3,\\[2mm]
 {\sin\theta\over4},&1/3\le t^2\le\rho,\\[2mm]
 {\sin\theta\cos\theta\over4}
 +{\sqrt3(\sin^2\theta-\cos^2\theta)\over8},
 &\rho\le t^2\le1.
 \end{cases} \tag{7}
\]

The first switch is `tan(theta)=sqrt(3)`.  Squaring the equality of the last
two displayed branches gives

\[
 3y^4-100y^3+114y^2-36y+3
 =(3y-1)(y^3-33y^2+27y-3),
\]

and the unsquared signs select the root (6).  The cubic derivative is negative
on `(7/10,71/100)`, and rational endpoint substitution gives opposite signs,
so `rho` is isolated uniquely.  Formula (7) explains the two very different
triangle constants in the frozen symmetric witness: its narrow-angle circuit
lies in the first regime, while its wide-angle circuit lies in the middle
regime.

## 4. Finite equioscillation theorem

Choose any finite family of balanced allocations `x^(r)`, including the zero
allocation.  Allocate `x^(r)` to the triangle and the residual surface to the
unit segment.  Replacing the actual triangle contribution by (4) gives

\[
 g_r(\phi)=\tau_r+{1\over4}\sum_i(l_i-x_i^{(r)})
 |\sin(\theta_i-\phi)|,\qquad
 G(\phi)=\max_r g_r(\phi). \tag{8}
\]

Cut `[0,pi]` at every `theta_i mod pi`.  On one resulting sign cell,

\[
 g_r(\phi)=\tau_r+A_r\sin\phi+B_r\cos\phi. \tag{9}
\]

Moreover `g_r''=-(g_r-tau_r)<=0`.  If an interior minimum of `G` has a unique
active index, it is locally a concave function and can be moved to a cell
endpoint without increasing its value (the constant case is harmless).  If
it has multiple active indices, some pair equioscillates.  Therefore the
global minimum of (8) occurs among:

1. the projection-zero cell endpoints; and
2. the pairwise equalities `g_r=g_s` lying in their stated sign cell.

Put `u=tan(phi/2)`.  For
`Delta A=A_r-A_s`, `Delta B=B_r-B_s`, and
`Delta tau=tau_r-tau_s`, every equality in item 2 is the explicit quadratic

\[
 (\Delta\tau-\Delta B)u^2+2\Delta A u
 +(\Delta B+\Delta\tau)=0. \tag{10}
\]

For rational witness data and triangle constants in `Q(sqrt(3))`, all
candidate orientations are algebraic of degree at most two over
`Q(sqrt(3))`, hence at most four over `Q`.  Their envelope values are exact
real-algebraic numbers.  This proves a branch-tree-free global angular
algorithm for asymmetric witnesses on the full direct-motion domain.  It also
gives the stationarity principle needed for optimizing witness parameters:
away from projection and triangle-fan walls, a locally best witness must
equioscillate at least two active allocation bounds at every worst angle; an
isolated one-bound worst angle cannot be a local minimum of the envelope.

For an implementation-independent exact encoding, write the left side of
(10) as `P_0(u)+sqrt(3)P_1(u)` with rational quadratics `P_0,P_1`.  Every root
is a root of the rational quartic

\[
 N(u)=P_0(u)^2-3P_1(u)^2. \tag{11}
\]

Rational isolating intervals for the real roots of `N`, followed by checking
the original signed expression and the projection-sign cell, remove the
conjugate and squaring artifacts.  This supplies minimal-polynomial-style
exact candidates without assuming a computer algebra representation.

## 5. Next parameter equations

For a symmetric four-edge arc with directions `-beta,-alpha,+alpha,+beta`,
lengths `p,q,q,p`, and closing load
`2(p cos beta+q cos alpha)`, (2)--(7) make the two same-angle circuit constants
`p f(beta)` and `q f(alpha)` explicit.  The two crossed circuits use (5), so
all five functions in (8) have symbolic coefficients.  Equating two copies of
(10) at two worst angles, together with `2p+2q=1`, produces a finite algebraic
stationarity system.  Dropping symmetry replaces the paired lengths and
angles by independent variables but changes neither theorem (5) nor (10).

This system is the appropriate source of exact asymmetric candidates.  A
floating-point optimizer may nominate a root, but a claimed improvement must
then identify its minimal polynomials and isolating intervals and compare all
finite candidates from (10).  No such improvement is claimed here yet.

More formally, fix a parameter chamber in which hull order, capacity
saturations, triangle support vertices, projection signs, and the real-root
ordering in (10) do not change.  Each surviving worst-angle value is then a
differentiable algebraic function `H_k(z)` of the witness parameters `z`, and
the certified floor is `min_k H_k(z)`.  At an interior local maximum `z_*`,

\[
 0\in\operatorname{conv}\{\nabla H_k(z_*):
                         H_k(z_*)=\min_jH_j(z_*)\}. \tag{12}
\]

Otherwise a separating direction has positive dot product with every active
gradient, increasing all active worst values for a sufficiently small move;
the inactive values remain separated by continuity, contradicting local
maximality.  Equation (12), the pair equalities from (10), capacity equations,
and total length one form a finite stationarity/equioscillation system.  In
particular, a full-dimensional asymmetric optimum cannot be justified by one
isolated worst orientation: it needs enough active algebraic candidates for
their gradients to surround the origin, or it must lie on a hull/capacity/fan
wall.

As a diagnostic only, 5,000 random local perturbations independently varied
all four directions and the first three lengths, solved the fourth length from
exact vertical-closure balance, normalized total traversal length to one, and
ranked the resulting circuit envelopes.  The best asymmetric sample was about
`0.23497624`, below the symmetric candidate's sampled value
`0.23507549`; no improving algebraic root was nominated.  This is numerical
evidence only.  The analytic deliverables are the circuit theorem, the exact
piecewise floor (7), and the finite algebraic candidate theorem (10).
