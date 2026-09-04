# Translation-free support reduction for the \(t=10/13\) witness

**Status:** sketch pending independent review. This is an analytic reduction,
not a numerical lower-bound certificate. It was derived without reading the
Issue #137/#140 checker implementations.

## Witness and motion convention

Let \(W\) be the polygonal arc with traversal vertices

\[
p_0=(0,0),\quad p_1=(1/3,0),\quad
p_2=(338/807,260/807),\quad
p_3=(9361/72361,105820/217083).
\]

Put

\[
c=\frac{69}{269},\qquad s=\frac{260}{269},\qquad
z=c+is,\qquad \phi=\arg z.
\]

Then \(c^2+s^2=1\), and the three edge vectors are
\(1/3,z/3,z^2/3\). Thus the traversal length is exactly one. Its convex hull
is an isosceles trapezoid of area

\[
A_W=\frac{87880}{651249}.
\]

This hull replacement loses no lower-bound information: the placed arc
contains its four traversal vertices, and every convex set containing the arc
therefore contains their convex hull. The same observation applies to every
other polygonal witness arc.

Every placement is a translation followed by a rotation. Pin the unit segment
horizontally by an orientation-preserving motion. Write \(\alpha\) for the raw
square-edge angle, \(\beta\) for the raw triangle-edge angle, and \(\gamma\)
for the first-edge angle of \(W\). Intrinsic rotations give the compact
quotient represented by

\[
0\leq\alpha\leq\pi/2,\qquad
0\leq\beta\leq2\pi/3,\qquad
0\leq\gamma\leq2\pi,
\]

with opposite faces identified. Retaining both representatives of every
identified boundary is harmless. The reduction uses no reflection gauge.

## Support-area functional

For a counterclockwise convex polygon \(P\), with edge lengths \(\ell_e\) and
outward unit normals \(n_e\), define

\[
\mathcal S_P(K)=\frac12\sum_e\ell_eh_K(n_e).
\]

If compact convex \(K\) contains \(P\), then

\[
\operatorname{area}(K)\geq\mathcal S_P(K). \tag{SA}
\]

Indeed, \(P\subseteq K\) implies
\(K+tP\subseteq K+tK=(1+t)K\) for \(t\geq0\). The polygonal mixed-area identity
is

\[
\operatorname{area}(K+tP)=\operatorname{area}(K)
+t\sum_e\ell_eh_K(n_e)+t^2\operatorname{area}(P).
\]

Comparison with \((1+t)^2\operatorname{area}(K)\), division by positive \(t\),
and \(t\downarrow0\) proves (SA). We apply it only to the compact hull of
finitely many placed witness vertices.

The containment premise \(P\subseteq K\) is essential. Arbitrary balanced
normals and weights do not define a lower-area functional for an unrelated
small \(K\). In this application \(P\) is literally one of the placed witness
hulls inside \(K\); omitting that checked premise is a kill condition. The
first-variation sum may equivalently be written using the edges of \(K\) and
supports of \(P\); equality of the two forms is the symmetry of planar mixed
area.

## Balanced-support elimination theorem

Let the already-rotated intrinsic witness hulls be \(Q_j\), let their
translations be arbitrary vectors \(t_j\), and set

\[
K=\operatorname{conv}\bigcup_j(Q_j+t_j).
\]

For polygonal \(Q_j\), every value \(h_{Q_j}(n)\) is attained at a listed
vertex. That vertex is a point of the placed witness hull and hence belongs to
\(K\) after adding \(t_j\); no hypothetical support point is introduced.

Choose one placed witness hull as the polygon \(P\subseteq K\). Choose
\(\lambda_{ej}\geq0\) satisfying

\[
\sum_j\lambda_{ej}=1\quad\text{for every }e, \tag{capacity}
\]

and, separately for every independently translated witness,

\[
\sum_e\ell_e\lambda_{ej}n_e=0. \tag{balance}
\]

Then

\[
\operatorname{area}(K)\geq
\frac12\sum_{e,j}\ell_e\lambda_{ej}h_{Q_j}(n_e). \tag{BS}
\]

For each edge,

\[
h_K(n_e)\geq
\sum_j\lambda_{ej}\bigl(h_{Q_j}(n_e)+t_j\cdot n_e\bigr),
\]

because every summand before averaging is at most \(h_K(n_e)\), and capacity
makes the right side a convex average. After multiplication by \(\ell_e\) and
summation, the coefficient of the arbitrary vector \(t_j\) is precisely
\(\sum_e\ell_e\lambda_{ej}n_e\). Balance cancels it separately for every
\(j\). Formula (SA) completes the proof.

Conversely, if one load vector is nonzero, translating just that witness
changes the proposed right side linearly: that substitution has not eliminated
the translation. Hence one support contact can never cancel a planar
translation, and two contacts can do so only when their normals are
antiparallel. The reported five-cycle with only one strict fourth-witness
vertex cannot alone become a translation-free support certificate.

## Closed form for the fourth-witness base

Use \(P=R_\gamma\operatorname{conv}(W)\). Its four outward normals are

\[
\begin{aligned}
n_0&=R_\gamma(0,-1),\\
n_1&=R_\gamma(s,-c),\\
n_2&=R_\gamma(2sc,s^2-c^2),\\
n_3&=R_\gamma(-s,c).
\end{aligned}
\]

The edge lengths are \(1/3,1/3,1/3,L\), where

\[
L=\frac{1+2c}{3}=\frac{407}{807}.
\]

The surface measure splits into two balanced pieces:

\[
n_0+n_2+2cn_3=0,\qquad n_1+n_3=0. \tag{split}
\]

For each rotated intrinsic witness hull \(Q_j\), define

\[
C_j=\frac{h_j(n_0)+h_j(n_2)+2ch_j(n_3)}6,\qquad
D_j=\frac{h_j(n_1)+h_j(n_3)}6. \tag{CD}
\]

Assign the first piece to a witness maximizing \(C_j\), and the antipodal
piece to one maximizing \(D_j\). Formula (BS) gives

\[
\boxed{\operatorname{area}(K)\geq\max_jC_j+\max_jD_j.} \tag{W-base}
\]

This is optimal within the fully balanced allocation class. Rotate balance
back to the intrinsic frame and put
\(a_j=\lambda_{0j}=\lambda_{2j}\). Balance forces

\[
\lambda_{1j}=(1+2c)\lambda_{3j}-2ca_j.
\]

With

\[
\rho_j=\lambda_{1j},\qquad
\lambda_{3j}=\frac{2c}{1+2c}a_j+\frac1{1+2c}\rho_j,
\]

capacity becomes two independent simplices
\(\sum_ja_j=\sum_j\rho_j=1\), and the objective is
\(\sum_ja_jC_j+\sum_j\rho_jD_j\). Every LP extremum is explicit: each simplex
is maximized at a vertex. No numerical contact assumption enters this result.

For example, the structural primal allocation underlying the diagnostic
Issue #140 maximizers (segment for \(C\), square for \(D\)) is exactly

\[
\begin{array}{c|cccc}
 &e_0&e_1&e_2&e_3\\ \hline
\text{segment}&1&0&1&138/407\\
\text{square}&0&1&0&269/407
\end{array}
\]

with every omitted witness receiving zero. Every edge column sums to one.
The segment row balances by the first identity in (split), and the square row
by the second. These are exact primal weights; the decimal support evaluation
below is not part of their validity.

## Three-angle master function

The index \(j\) below runs over the unit segment, equilateral triangle,
square, and \(W\), each after rotation and before translation. Complementary
exact base bounds are

\[
B_S=\frac12\max_jw_j(e_y),
\]

\[
B_Q=\frac16\left(\max_jw_j(u)+\max_jw_j(v)\right),
\]

for the square's orthogonal axes \(u,v\), and

\[
B_T=\frac14\max_j\sum_{k=0}^2h_j(m_k),
\]

for the triangle's three outward normals. Its three-normal balance kernel is
one-dimensional, so fractional allocation reduces to this single-witness
maximum.

Thus every placement satisfies

\[
\operatorname{area}(K)\geq
B(\alpha,\beta,\gamma):=
\max\{B_S,B_Q,B_T,\max_jC_j+\max_jD_j\}. \tag{master}
\]

The outer operation is a maximum, not a sum of bounds from several templates.
Each displayed bound uses one contained template with total edge capacity one.
Adding independently normalized template bounds would be unsound (two
identical templates would already double-count area).

Every support here is the maximum of finitely many
\(x\cos\theta+y\sin\theta\), with rational \(x,y\) except for the standard
\(\sqrt3\) triangle coordinate. This removes all six translation variables
and leaves a compact three-angle finite analytic cover. It uses no translation
box, optimizer stationarity, hull ordering, or sampled contact conjecture.

## Strength checkpoint and remaining task

At the Issue #140 test orientation, (W-base) gives approximately
0.2349746497, versus reported hull area 0.2350390775. An exploratory scan and
local refinement found values of (master) near 0.23464, still above 0.232239.
These decimals are numerical diagnostics only.

The next exact task is an outward interval cover of the three-angle torus.
Failure to establish (balance) for every independently translated witness is
the kill criterion for any proposed support leaf.

No such full-domain interval cover is included here. Therefore neither the
diagnostic 0.23464 value nor a strict improvement over 0.232239 is claimed.

## Exact replay

Run:

    python3 problems/moser-convex-worm/attacks/fourth-witness-support/verify_geometry.py

The replay checks the rational witness, exact unit traversal, trapezoid area,
edge length \(L\), and both identities in (split). It does not claim that the
three-angle cover has been completed.
