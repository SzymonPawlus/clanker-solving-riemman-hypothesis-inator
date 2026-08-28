# Square Peg #128: algebraic winding does not imply convex-excursion control

Status: `sketch`.

This note constructs a sequence of smooth Jordan parametrizations converging
uniformly to a fixed Jordan curve for which every short chord-closed subarc
has uniformly vanishing algebraic winding integral, while a sequence of
shrinking subarcs has convex-excursion area bounded below.  Thus the exact
algebraic winding condition `AW` is strictly weaker than the sufficient
absolute condition `CH` defined below.

The proof is self-contained.  Frozen PRs #115, #118, #119, #122, #123, #126,
and #127 are neither premises nor dependencies.

## 1. The two local conditions

For a smooth embedded arc `a:[s,t]->R^2`, close it by the oriented chord from
`a(t)` to `a(s)` and call the resulting loop `L(a;s,t)`.  Put

```text
lambda_0=(x dy-y dx)/2,
W(a;s,t)=integral_(L(a;s,t)) lambda_0.
```

By the classical Green formula,

```text
W(a;s,t)=integral_R2 Ind(L(a;s,t),z) dz.                    (1)
```

A uniformly convergent sequence of smooth period-one Jordan maps `a_n`
satisfies `AW` when

```text
lim_(delta->0) sup_n sup_(0<=t-s<=delta)|W(a_n;s,t)|=0.     (AW)
```

For `CH`, let `S=[a(s),a(t)]`.  The open set
`{u in (s,t):a(u) notin S}` is a countable union of intervals
`(alpha_j,beta_j)`.  Close each corresponding excursion by its subsegment of
`S` and denote the closed curve by `E_j`.  Define

```text
H(a;s,t)=sum_j area(conv(E_j)).
```

The family satisfies `CH` if the same uniform local limit with `H` in place
of `|W|` is zero.  We construct `a_n` satisfying `AW` but not `CH`.

For polygonal paths, the integral of `lambda_0` on an oriented edge from `p`
to `q` is `det(p,q)/2`.  Closing by a chord therefore gives

```text
W(a;s,t)=F(t)-F(s)+det(a(t),a(s))/2,                        (2)
```

where `F` is any primitive of `a^*lambda_0`.  Closed action is translation
invariant.  In particular, if an arc lies in a disk of radius `R`, its chord
term after translating the center to zero is at most `R^2/2`.

## 2. The alternating inward coil

Let `N>=2` be even and set

```text
r=N^(-1/2),       Delta=r/(2N),       rho_k=r-k Delta
                                              (0<=k<=N).    (3)
```

Let `M` be the least even integer with `M>=100N^2`.  For `0<=k<N` put
`sigma_k=(-1)^k`.  The `k`-th polygonal turn has vertices

```text
v_(k,l)=rho_(k,l)(cos theta_(k,l),sin theta_(k,l)),
rho_(k,l)=rho_k-l Delta/M,
theta_(k,l)=sigma_k 2 pi l/M,             0<=l<=M.          (4)
```

Thus `v_(k,M)=v_(k+1,0)=(rho_(k+1),0)`.  Concatenate the
turns from `v_(0,0)=(r,0)` to `v_(N,0)=(r/2,0)`.

This polygonal coil is injective.  To see the radial assertion exactly,
rotate one edge so its endpoints are `A=R` and
`B=(R-d)exp(i alpha)`, where `d=Delta/M` and `alpha=2pi/M`.  For
`z(u)=(1-u)A+uB`,

```text
|z(u)|^2-(R-d)^2
 =(1-u)[R^2-(R-d)^2-u|A-B|^2].                             (4a)
```

Moreover,

```text
|A-B|^2<=d^2+R(R-d)alpha^2,
R^2-(R-d)^2=2(R-d)d+d^2.
```

Here `R>=r/2`, `d=r/(2NM)`, and `M>=100N^2`, so
`2(R-d)d>=R(R-d)alpha^2`.  The bracket in (4a) is nonnegative.
Consequently the norm on each edge is minimized at its inner endpoint, and
the open edges of turn `k` lie in
`{rho_(k+1)<|z|<rho_k}`.  Distinct turns occupy disjoint open annuli; within
one turn the polar angle is strictly monotone through one revolution and
nonadjacent angular sectors are disjoint.  Adjacent edges meet only at their
common vertex.

## 3. Uniform algebraic action on every coil subarc

The signed action of turn `k` is exactly

```text
B_k=(sigma_k/2) sin(2 pi/M)
       sum_(l=0)^(M-1) rho_(k,l)rho_(k,l+1).                (5)
```

Since the radii in the turn differ from `rho_k` by at most `Delta`,

```text
B_k=sigma_k(pi rho_k^2+O(r^2/N+r^2/M^2)),                  (6)
||B_(k+1)|-|B_k||<=C r^2/N.                                (7)
```

Pair adjacent turns.  Their signs are opposite, so (7) gives, for every
consecutive collection of complete turns,

```text
|sum_(k=i)^j B_k|<=C r^2.                                  (8)
```

The action on a partial turn is at most `C r^2`, because every edge in that
turn has the same orientation sign in (5).  Hence the primitive along the
entire inward coil has oscillation at most `C r^2`.  By (2), every arbitrary
chord-closed coil subarc satisfies

```text
|W(coil;s,t)|<=C r^2.                                      (9)
```

This estimate includes endpoints in the interiors of angular edges and
subarcs beginning and ending in different partial turns.

## 4. A fixed lower bound for convex excursions

Close the whole inward coil by the positive radial chord from `(r/2,0)` to
`(r,0)`.  The coil meets this chord precisely at its `N+1` turn-boundary
points `(rho_k,0)`.  The excursion components are therefore the individual
turns.

For every unit vector `u`, some angular vertex of a fixed turn makes angle at
most `pi/M` with `u`, and every vertex radius is at least `r/2`.  The support
function of the convex hull is consequently at least
`(r/2)cos(pi/M)` in every direction.  Thus the convex hull of every turn
contains the disk of that radius.  For an absolute constant `c>0`,

```text
H(coil;whole inward part)
 >= sum_(k=0)^(N-1) c r^2
 =c N r^2=c.                                                (10)
```

## 5. An injective low-action escape

The positive radial ray meets the coil only at the turn-boundary vertices.
At an interior boundary vertex, the last edge of turn `k-1` and the first
edge of turn `k` lie on the same side of the ray: that side is lower when
`sigma_(k-1)=+1` and upper when `sigma_(k-1)=-1`.  The free side alternates.

Directly reversing from the last inward coil edge to the outward ray would
create a nonregular cusp.  Insert a free-side hairpin first.  Choose
`zeta_N>0` below `r/N^3` and below one tenth of all local clearances.  In
coordinates centered at `v_(N,0)=(r/2,0)`, let it follow the simple polygon

```text
(0,0)->(-zeta/4,0)->(-zeta/4,sigma_(N-1) zeta/4)
 ->(zeta/2,sigma_(N-1) zeta/4)->(zeta/2,0)->(zeta,0).        (11a)
```

The sign places it opposite the last turn.  Round its interior corners in
disjoint balls much smaller than `zeta`.  Smooth the last coil edge to arrive
at `(r/2,0)` with inward radial tangent, matching the first hairpin segment.
The last hairpin segment has outward radial tangent and joins the outward ray
at `(r/2+zeta,0)`.  This continuation is a regular embedded arc.  Its image
lies in a `C zeta` ball and its action is
`O(r zeta+zeta^2)=o(r^2)`.

Starting at `(r/2+zeta,0)`, travel outward on the positive ray.  Near every
boundary point `(rho_k,0)`, replace a short radial segment by a semicircle on
the free side.  Choose its radius `epsilon_k>0` so that

```text
epsilon_k<=r/N^3,
epsilon_k<r/(10M),
epsilon_k<(one tenth of every relevant nonincident-edge clearance). (11)
```

There are finitely many positive clearances.  The detour disks are disjoint
because their centers are separated by `Delta`, and (11) makes each detour
disjoint from every nonincident coil edge.  Its free-side choice makes it
disjoint from the two incident edges.  The hairpin-plus-escape meets the coil
only at the hairpin initial point and ends at

```text
q_N=(r+epsilon_0,0).
```

Radial segments have zero `lambda_0` action.  A semicircle of radius
`epsilon` centered at distance at most `r` has absolute action at most
`C(r epsilon+epsilon^2)`.  Therefore the total variation of the primitive on
the escape is

```text
<=C sum_k(r epsilon_k+epsilon_k^2)=O(r^2/N^2).              (12)
```

Equations (9), (12), and the chord bound show that every subarc contained in
or straddling the inward coil and escape has closed action at most `C r^2`.

## 6. Explicit insertion into one fixed Jordan curve

Fix a smooth Jordan curve `C_0` which contains the horizontal segment
`[-1,1]x{0}` and whose remaining image lies in `{y<0}`.  Such a curve is
obtained by a smooth stadium with a flat top.  Translate the coil and escape
by

```text
O_N=(0,3r).
```

The packet is contained in `closed B(O_N,r+epsilon_0)`.  Its inward start and
escape end are

```text
p_N=(r,3r),       q_N=(r+epsilon_0,3r).
```

Remove the base segment from `A_N=(-3r,0)` to `B_N=(3r,0)` and add the
polygonal connectors

```text
A_N -> (-3r,5r) -> (3r,5r) -> p_N,
q_N -> (3r,r) -> B_N.                                      (13)
```

For large `N`, these connectors are injective and mutually disjoint.  Relative
to `O_N`, the inward coil has `x<=r`, with equality only at its start.  Its
first edge leaves that start toward the upper-left.  The escape detour around
the outer boundary point lies below the radial ray, whereas the last segment
of the first connector leaves `p_N` toward the upper-right; hence that
connector meets the packet only at `p_N`.  The escape ends at its rightmost
point `q_N`, and the second connector leaves it toward the lower-right in
`{x>=r+epsilon_0}`, so it meets the packet only at `q_N`.  The remaining
connector segments lie above, left, or right of the packet, and the upper and
lower connectors are disjoint from each other.  The retained base lies in
`{y<=0}` and meets the connectors only at `A_N,B_N`.  Hence the packet,
connectors, and retained base form a polygonal Jordan curve `P_N`.

All connector coordinates and lengths are `O(r)`.  Their primitive has total
variation `O(r^2)`.  Thus every subarc contained in the entire replacement
(connectors, inward coil, and escape), including every straddling subarc,
has primitive oscillation `O(r^2)` and image diameter `O(r)`.  Translating the
coil by `O_N` changes its open primitive only by the exact endpoint term
`det(O_N,z)/2`, whose oscillation is also `O(r^2)`.  By (2),

```text
|W(P_N;s,t)|<=C r^2                                        (14)
```

whenever the subarc lies in the replacement.

## 7. One simultaneous smoothing hierarchy

Let `K_N` be the finite number of packet and connector vertices, `d_N>0` the
minimum distance between nonincident polygonal pieces which must remain
separate, and `L_N` the total polygonal length.  Let `R` be one common image
bound.  Choose a rounding scale `tau_N>0` satisfying

```text
tau_N<d_N/100,
tau_N<min_k(epsilon_k)/100,
C(R K_N tau_N+tau_N L_N)<r^2/N.                            (15)
```

Round every corner in a disjoint ball of radius at most `tau_N`.  At every
turn-boundary point on the radial chord other than the inner endpoint, use a
smooth arc which passes through
that same point, is tangent to the radial line there, and stays on the side
occupied by the two incident edges.  Such a local rounding is the graph of a
smooth nonnegative (or nonpositive) bump after rotating the radial line to an
axis, with nonzero derivative in the radial coordinate.  It is therefore a
regular embedded arc.  It preserves the chord contact and creates no new one.
At the inner endpoint `v_(N,0)`, use the separate hairpin construction of
Section 5: the smoothed last turn arrives with inward radial tangent and the
hairpin leaves with the same nonzero tangent.  At all other
vertices use an ordinary embedded rounding.  The separation conditions in
(15) preserve global injectivity.

Call the resulting smooth Jordan curve `C_N`.  Parametrize corresponding old
and new local arcs on the same intervals.  The global `1`-variation of the
difference is `O(K_N tau_N)`, its uniform norm is `O(tau_N)`, and the
bilinear identity

```text
det(Q,dQ)-det(P,dP)=det(Q-P,dQ)+det(P,d(Q-P))
```

shows that the primitive error on every subinterval is bounded by the left
side of the last inequality in (15).  Consequently all estimates (10) and
(14) persist, with errors `o(r^2)`.  In (10), each smoothed turn still has the
same two radial endpoints and is uniformly `o(r)` from the polygonal turn;
its convex hull still contains a disk of radius `c r`.

## 8. Period-one parametrizations and the full AW quantifier

Choose a fixed regular period-one parametrization `c_0` of the base curve such
that a parameter neighborhood of a point `t_*` runs affinely along its flat
segment.  We now specify a compatible smooth parametrization of `C_N`, rather
than joining unrelated parametrizations at the two seams.

Let `ell` be arclength on the already smoothed geometric curve `C_N`.  Choose
a positive smooth density `w_N(ell)` such that:

1. its integral around `C_N` is one;
2. its integral over the replacement arc is exactly `r`;
3. on the retained exterior it agrees, up to a factor tending to one, with
   the density induced by `c_0`, and is bounded below there uniformly in `N`;
4. every transition lies in an arbitrarily short end collar of the
   replacement.

To construct it, first fix the exterior density, put a small positive
constant on the long coil, and join them by flat smooth cutoffs in the end
collars.  Choose the collars so their prescribed density mass is below
`r/2`, and then adjust the positive coil constant to make the replacement
mass exactly `r`; finally scale the exterior density by a factor tending to
one to make total mass one.

Define `t(ell)=integral_0^ell w_N(u)du` modulo one and let `c_N(t)` be the
inverse arclength parametrization.  Positivity makes this a smooth regular
period-one parametrization.  The single smooth density automatically matches
all jets and speeds at the replacement seams.  After a harmless rotation of
the parameter circle, property 2 makes the replacement interval

```text
J_N=[t_*-r/2,t_*+r/2],                                     (16)
```

and property 3 gives one uniform Lipschitz bound on every exterior
restriction.

The replacement image has diameter `O(r)` and replaces a base image segment
of diameter `O(r)`.  The exterior densities converge to the base density, so
the exterior parametrizations converge uniformly as well.  Hence
`c_N->c_0` uniformly.  In particular the whole family has a common modulus of
continuity `omega`.

Let `I=[s,t]` be a lifted parameter interval of length at most `delta`.  If it
does not meet `J_N`, it lies on an affinely reparametrized fixed smooth base
arc and

```text
|W(c_N;s,t)|<=C delta.                                     (17)
```

If it meets `J_N`, insert the at most two endpoints of `J_N`.  Closed action
is additive up to the oriented triangles formed by the original endpoints
and an inserted seam point.  Each such triangle has area at most
`C omega(delta)^2`.  Equations (14)--(17) give

```text
|W(c_N;s,t)|
 <=C r_N^2+C delta+C omega(delta)^2                         (18)
```

for all sufficiently large `N`; the same estimate handles an interval
crossing the period seam after one additional insertion.

Given `eta>0`, first choose `N_0` so `C r_N^2<eta/3` for `N>=N_0`, and then
choose `delta` so the remaining terms in (18) are below `2eta/3`.  The
finitely many smooth maps `c_2,c_4,...,c_(N_0-2)` have their own vanishing
local action moduli.  This proves (AW).

Finally, the inward-coil part is a subinterval of `J_N`, so its parameter
length tends to zero.  Its pinned radial chord excursions satisfy (10) after
smoothing.  Therefore

```text
limsup_(delta->0) sup_N sup_(t-s<=delta)H(c_N;s,t)>=c>0.     (19)
```

Thus `CH` fails.

## 9. Conclusion and status

The smooth Jordan maps `c_N` converge uniformly to the fixed Jordan map
`c_0`, satisfy `AW`, and fail `CH`.  Hence uniform local algebraic winding
control is strictly weaker than uniform local convex-excursion control.

This is a sharpness result about sufficient compactness conditions, not a new
Square Peg existence theorem.  It remains a verification-critical `sketch`
until independently reviewed.  No frozen sketch is made assumable by this
construction.
