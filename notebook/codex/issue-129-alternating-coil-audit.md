# Independent audit: alternating-coil separation of AW from CH

Status: **independent audit / sketch**, not a premise and not a verification status.
Frozen Square Peg pull requests and the prover worktree were not used as premises.

## 1. The packet

Let `N` be even and large, put

```text
r=N^(-1/2),  Delta=r/(2N),  rho_k=r-k Delta  (0<=k<=N).
```

Choose an even `M>=100N^2`, set `d=Delta/M`, `delta=2pi/M`, and define turn
`k` by the vertices

```text
v_(k,l)=(rho_k-l d)(cos(sigma_k l delta),sin(sigma_k l delta)),
sigma_k=(-1)^k,  0<=l<=M.
```

Thus `v_(k,M)=v_(k+1,0)`.  Concatenate the turns from radius `r` to radius
`r/2`.

## 2. Injectivity, without a sagitta shortcut

Consider one edge from `a=R(cos theta,sin theta)` to
`b=(R-d)(cos(theta+sigma delta),sin(theta+sigma delta))`.  Along its affine
parametrization `q(s)`, the derivative of `|q(s)|^2` is affine increasing in
`s`, so it is enough to check it at `s=1`.  There

```text
(1/2) d/ds |q(s)|^2 = b dot (b-a)
                         =(R-d)((R-d)-R cos delta)<0,
```

because

```text
d= r/(2NM) > r(1-cos delta) >= R(1-cos delta)
```

for `M>=100N^2` and large `N`.  Hence radius decreases strictly along every
open edge.  Each edge also stays in its angular sector of width `delta<pi`.
Distinct nonadjacent sectors of one turn do not meet, and distinct turns lie
in disjoint open radial annuli.  Adjacent turns share only their prescribed
endpoint.  The inward coil is therefore a simple polygonal arc.

At a shared endpoint on the positive ray, the last edge of turn `k-1` and
first edge of turn `k` both lie in the half-plane whose `y`-sign is `sigma_k`:
the former has terminal angle
`sigma_(k-1)(2pi-delta)=sigma_k delta` modulo `2pi`, and the latter has angle
`sigma_k delta`.  The opposite side of the ray is locally free.  This is the
topological fact needed by a radial escape.

## 3. Every-subarc algebraic action

For `lambda=(x dy-y dx)/2`, the action of turn `k` is exactly

```text
B_k=(sigma_k/2) sin(delta)
       sum_(l=0)^(M-1) (rho_k-l d)(rho_k-(l+1)d).
```

Write `a_k=|B_k|`.  The sequence `a_k` is decreasing, `a_k<=C r^2`, and

```text
0<=a_k-a_(k+1)<=C r Delta=C r^2/N.
```

Every consecutive alternating sum of complete turns is bounded by its first
term (or by pairing adjacent terms), hence by `C r^2`.  Every partial-turn
action has one sign and magnitude at most `a_k<=C r^2`.  An arbitrary coil
subarc consists of at most two partial turns and a consecutive block of whole
turns, so its action is `O(r^2)`.  The straight closing chord between two
points of the radius-`r` ball has action
`det(q,p)/2`, also `O(r^2)`.  Thus every chord-closed subarc has algebraic
winding/action `O(r^2)=O(1/N)`, not merely the full coil.

This is cancellation of signed action.  It does not assert small absolute
winding mass.

## 4. CH lower bound

The positive radial chord from `v_(0,0)` to `v_(N,0)` meets the inward coil
exactly at the `N+1` turn boundaries.  Its excursions are the individual
turns.  For any unit vector `u`, some turn vertex has angular distance at most
`pi/M` from `u` and radius at least `rho_(k+1)`.  Therefore the support
function of the convex hull of turn `k` is at least

```text
rho_(k+1) cos(pi/M) >= (r/2) cos(pi/M)
```

in every direction.  The hull contains the disk of that radius, and

```text
sum_(k=0)^(N-1) area(conv(turn k)) >= c N r^2 = c.
```

The selected inward-coil interval can be assigned parameter length at most
`r`, which tends to zero.  Hence CH fails on shrinking subintervals while AW
there tends to zero.

## 5. Escape and global Jordan insertion

The raw last inward edge followed immediately by an outward radial segment
reverses tangent direction at the inner endpoint.  A mere pinned corner
rounding cannot turn this into a regular smooth embedding.  Instead, after
reaching the exact inner endpoint, continue with a tiny embedded hairpin on
the locally free side.  Its initial tangent matches the last coil edge, and it
turns inside a clearance ball to join the positive ray slightly farther out
with outward tangent.  The chosen CH subarc still ends at the exact inner
point.  Give the cap diameter `eta_N` arbitrarily smaller than all local
clearances; its action is `O(r eta_N+eta_N^2)`.

Then travel outward on the positive ray.  At each turn
boundary replace a small ray neighborhood by a semicircle on the locally free
side identified in Section 2.  Since the polygon is finite, choose each radius
`epsilon_k` below one tenth of every relevant nonincident-edge clearance,
below `r/(10M)`, and below `r/N^3`; choose the semicircles pairwise disjoint.
The escape then meets the inward coil only at its initial endpoint.

Radial pieces have zero `lambda` action, and one translated semicircle costs
at most `C(r epsilon_k+epsilon_k^2)`.  Consequently the total variation of
the escape primitive is `O(r^2/N^2)`.  In particular every escape subarc and
every coil/escape-straddling subarc has action `O(r^2)`.

For an explicit base insertion, take a smooth Jordan curve containing a flat
segment near the origin and otherwise lying below it.  Translate the packet
center to `(0,3r)`, remove the base segment from `A=(-3r,0)` to `B=(3r,0)`,
and use connectors

```text
A -> (-3r,5r) -> (3r,5r) -> p,
q -> (3r,r) -> B,
```

where `p=(r,3r)` is the coil start and `q=(r+o(r),3r)` is the escape end.
The segment entering `p` and the segment leaving `q` point strictly outward
from the packet disk; convexity shows they meet it only at their endpoints.
The remaining connector pieces lie above or to the sides, the two connector
chains are disjoint, and the retained base lies at or below `y=0`.  This is a
Jordan polygon.  All replacement coordinates and connector lengths are
`O(r)`, so every connector-subarc action is `O(r^2)`.

## 6. Seams, common parametrization, and smoothing

Parametrize the replacement on an interval `J_N` of length `r` and affinely
rescale the fixed base parameter on its complement.  The whole replacement
has diameter `O(r)`, so the resulting maps converge uniformly to the base
parametrization.  Uniform convergence to a continuous limit, plus the finite
initial prefix, gives a common modulus of continuity.

Let `F_N(t)=integral_0^t c_N^*lambda`.  On the replacement its oscillation is
`O(r^2)` by Sections 3 and 5; outside it is a small affine reparametrization of
the fixed smooth primitive.  Splitting an arbitrary short interval at the at
most two seams gives

```text
|AW_N(s,t)| <= C r_N^2 + C delta_t + C omega(delta_t)^2
```

for the tail in `N`; the joining-triangle terms are bounded by the common
spatial modulus.  First choose the tail so `r_N^2` is small, then choose
`delta_t`; finitely many earlier curves have their own smooth moduli.  This is
the required all-subarc epsilon-delta order of quantifiers.

There are `K_N=O(NM)` corners.  Let `d_N>0` be the least relevant local
clearance.  Choose a common rounding scale `tau_N` below `d_N/100`, below all
detour scales, and so small that

```text
C(R K_N tau_N + tau_N L_N) <= r_N^2/N.
```

The `1`-variation difference and the bilinear action estimate then control
the smoothing error uniformly on every subinterval by `o(r_N^2)`.  At each
internal turn boundary, use a one-sided smooth arc through the same radial point,
tangent to the radial chord.  The two incident endpoints lie on opposite
`x`-sides and the same `y`-side, so a sufficiently small parabolic template
does this without intersection.  The exact `N` chord contacts and their
excursions persist; the convex-hull support bound loses only `O(tau_N)`.
Treat the inner endpoint with the separate regular hairpin above, rather than
trying to smooth a tangent reversal at the pinned point.

## 7. Primary-literature boundary

The closest primary rough-path example located is Danyu Yang, *Notes on area
operator, geometric 2-rough paths and Young integral when
`p^(-1)+q^(-1)=1`*, arXiv:1204.0112.  Example 38 (PDF p. 16) constructs a
vanishing-2-variation Fourier path whose polygonal Riemann areas have arbitrary
limits.  Examples 41--42 (PDF p. 26) give smooth paths converging to zero in
2-variation while their areas diverge or converge to a nonzero additive area.
These are sharp signed-area cancellation/anomaly examples, but they are not
simple Jordan packets and do not formulate convex chord-excursion mass.

Boedihardjo--Geng, *Simple Piecewise Geodesic Interpolation of Simple and
Jordan Curves with Applications*, arXiv:1309.1576, Theorem 3.2 and Remarks
3.1--3.2 (PDF pp. 13--14), treats Green approximation for Jordan curves of
finite `p`-variation only for `p<2` and explicitly notes the winding
integrability obstruction for non-simple nonrectifiable curves.  It does not
give the AW-not-CH endpoint example.

The Banchoff--Pohl inequality cited there controls square-integrable winding
for rectifiable closed curves by length.  It is an absolute-mass estimate in a
different regime and does not prevent the alternating signed cancellation
above.

The current-theoretic analogue is orientation cancellation: Federer--Fleming,
*Normal and Integral Currents*, Ann. of Math. 72 (1960), pp. 458--520,
separates weak/flat convergence from mass control, while Sormani--Wenger,
*Weak Convergence of Currents and Cancellation*, Calc. Var. PDE 38 (2010),
pp. 183--206, studies conditions preventing opposing sheets from disappearing
in a weak limit.  This is conceptually the same signed-versus-absolute
distinction.  Neither source provides the one-dimensional simple-Jordan
packet, endpoint-chord excursion functional, or shrinking-parameter AW/CH
separation used here.

Thus these primary sources support the sharpness context, but no equivalent
simple-Jordan, shrinking-subinterval AW-not-CH construction was located in
this audit.  This is a bounded novelty search, not a claim of priority.

## Disposition

The independently reconstructed geometry and estimates pass the adversarial
checks above.  The result remains a verification-critical sketch until a
separate reviewer checks the exact committed claim; this audit does not
confer `verified:review`.
