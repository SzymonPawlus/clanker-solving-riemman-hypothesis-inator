# Analytic angular proof of a `0.2350682` support floor

**Status:** `sketch`. This note replaces the 70-leaf angular subdivision in
the frozen
[`verify_four_edge.py`](../four-edge-support/verify_four_edge.py) artifact
from Issue #178 (frozen producer commit `2fd399b`) by four concavity arguments;
it does not modify that artifact.  The passage from the support inequalities
to an area bound still depends on the finite-polygon
mixed-area/common-fan bridge under review in Issues #170 and #176.  PR #175
is only a same-family red-team of part of that bridge and grants no
verification status.

**Angular proposition.** For every relative direct-rotation angle of the
four-edge hull, at least one of the five legal balanced support choices below
(the all-segment choice and four triangle allocations) has value at least

\[
 {1175341\over5000000}=0.2350682.
\]

This proposition is the bridge-independent content of the note, still at
status `sketch`.  Turning it into a convex-area statement uses the explicitly
identified bridge dependency.
The proof first verifies the hull and balanced loads, then reduces the free
triangle orientation to nine support-cell boundaries.  Four elementary
sinusoids cover the remaining half-turn by concavity, and an exact index
involution supplies the second half without reflecting the worm.

## 1. Exact hull data

Put

\[
 \alpha=2\arctan(1/72),\qquad \beta=2\arctan(4/5).
\]

The four traversed unit directions and the closing direction are

\[
\begin{aligned}
 v_0&=(9/41,-40/41),&v_1&=(5183/5185,-144/5185),\\
 v_2&=(5183/5185,144/5185),&v_3&=(9/41,40/41),\\
 v_4&=(-1,0).
\end{aligned}
\]

Their hull-edge lengths are

\[
 (L_0,L_1,L_2,L_3,L_4)
 =\left({163\over480},{77\over480},{77\over480},{163\over480},
 {11984563\over25510200}\right).
\]

Only the first four edges belong to the worm, and their lengths sum to one.
The fifth edge closes the polygonal chain; the turn check below proves that
this closed chain is its convex hull boundary.  Direct calculation gives

\[
 L_4=2{163\over480}{9\over41}
       +2{77\over480}{5183\over5185}
       ={11984563\over25510200},\qquad
 \sum_{i=0}^4 L_i v_i=0,
\]

and consecutive cross products are strictly positive, including the last-to-
first product.  In order, their exact values are

\[
 {206024\over212585},\quad {1492704\over26884225},\quad
 {206024\over212585},\quad {40\over41},\quad {40\over41}.
\]

Local left turns alone would not rule out a winding-two star, so we also note
the unwrapped direction order

\[
 -\beta<-\alpha<\alpha<\beta<\pi<2\pi-\beta.
\]

The five turns are

\[
 \beta-\alpha,\quad 2\alpha,\quad \beta-\alpha,\quad
 \pi-\beta,\quad \pi-\beta,
\]

each strictly between zero and \(\pi\), and their sum is \(2\pi\).  Together with
closure and positive edge lengths, this proves that the edge list is the
strict counterclockwise boundary of its convex hull, rather than merely a
locally left-turning closed walk.

The unit-vector checks are just the Pythagorean identities
\(9^2+40^2=41^2\) and \(5183^2+144^2=5185^2\), while
\(2(163+77)/480=1\) proves the open-chain length exactly.

## 2. Four first-half support bounds

Pin the centred unit segment horizontally.  In the fixed hull frame let
\(e_\phi=(\cos\phi,\sin\phi)\) be the segment direction; equivalently, after
pinning the segment this \(\phi\) is the negative of the hull's physical
rotation angle.  The sign convention does not change the full orientation
domain.  If an edge load \(r_i\) is assigned to the segment, its contribution
to the mixed-area lower bound is

\[
 {r_i\over4}\,|\det(v_i,(\cos\phi,\sin\phi))|.
\]

On the first half-domain we use the all-segment allocation `S` and three of
the balanced triangle allocations from the exact hull:

\[
 x^S=(0,0,0,0,0),\qquad
 A=(0,2,4),\qquad B=(0,3,4),\qquad C=(1,2,4).
\]

The fourth triangle allocation

\[
 D=(1,3,4)
\]

is the index mirror of `A`; it is needed only when transporting the support
formula to the second half-domain in Section 4.  Explicitly,

\[
 x^D=\left(0,{77\over480},0,{9471\over2074000},
                    {2007929\over12444000}\right).
\]

In the edge order \(0,1,2,3,4\), their exact triangle loads are

\[
\begin{aligned}
 x^A&=\left({9471\over2074000},0,{77\over480},0,
                    {2007929\over12444000}\right),\\
 x^B&=\left({163\over480},0,0,{163\over480},{489\over3280}\right),\\
 x^C&=\left(0,{77\over480},{77\over480},0,
                    {399091\over1244400}\right).
\end{aligned}
\]

These fractions come directly from cancelling the two vector coordinates.
For `B` and `C`, symmetry cancels the vertical coordinate and the closing
load is respectively

\[
 2{163\over480}{9\over41}={489\over3280},\qquad
 2{77\over480}{5183\over5185}={399091\over1244400}.
\]

For `A`, cancellation of the vertical coordinate first gives

\[
 x^A_0={77\over480}{144/5185\over40/41}
       ={9471\over2074000},
\]

and cancellation of the horizontal coordinate then gives

\[
 x^A_4={9\over41}x^A_0+{5183\over5185}{77\over480}
       ={2007929\over12444000}.
\]

Every coordinate lies between zero and the corresponding \(L_i\), and direct
substitution gives both \(\sum_i x_i v_i=0\) and
\(\sum_i(L_i-x_i)v_i=0\). Thus the triangle and segment translations cancel
separately in every bound: applying the fixed clockwise quarter-turn gives
the same two zero sums for the outward normals used by the support functions.

For an exact capacity check, the only nontrivial positive residuals are

\[
 L_0-x^A_0={4168949\over12444000},\quad
 L_4-x^A_4={157366171\over510204000},\quad
 L_4-x^B_4={399091\over1244400},\quad
 L_4-x^C_4={489\over3280};
\]

all remaining coordinates are visibly either zero, a full edge load, or one
of the positive listed loads.

More explicitly, if \(K\) is the joint convex hull, then the clockwise
quarter-turn
\(n_i=(v_{i,y},-v_{i,x})\) is the outward unit normal.  The conditional bridge
applies because convexity forces \(K\) to contain the whole worm hull,
including its untraversed closing edge.  Containment of the segment and
triangle then gives

\[
 \operatorname{area}K\ge {1\over2}\sum_iL_i h_K(n_i)
 \ge {1\over2}\sum_i\left(x_i h_\triangle(n_i)
                   +(L_i-x_i)h_{\rm seg}(n_i)\right). \tag{1}
\]

This is merely a partition of each nonnegative edge load; it does not invoke
a mixed-area theorem for the degenerate segment.

For each named triple, the listed load is assigned to a freely rotated
equilateral triangle of side \(1/2\); its residual is assigned to the pinned
segment.  Both are legitimate unit-worm tests: the segment has length one,
and traversing two sides of the triangle is an open polygonal curve of total
length one whose convex hull is the full triangle.  The factor \(1/4\) in the
segment term is the product of the mixed-area factor \(1/2\) and the centred
unit segment's support radius \(1/2\).  Exact force balance holds separately
for both witnesses.  Minimizing the triangle term over its orientation gives

\[
 q_X=\min_\theta {1\over2}\sum_i x_i^X
                 h_{R_\theta\triangle}(n_i),
\]

with the exact values

\[
\begin{aligned}
 q_A&={231\over414800}+{399091\sqrt3\over19910400},\\
 q_B&={163\over1968},\\
 q_C&={399091\sqrt3\over9955200},\\
 q_D&=q_A.
\end{aligned}
\]

In the reference orientation take the triangle vertices to be

\[
 (0,0),\qquad(1/2,0),\qquad(1/4,\sqrt3/4).
\]

Its support function is therefore the explicit maximum

\[
 h_\triangle(a,b)=\max\left(0,{a\over2},
                         {a\over4}+{\sqrt3 b\over4}\right). \tag{2}
\]

Rotating \((a,b)\) through the edge-normal alignments and inserting the three
nonzero loads in \((1/2)\sum_i x_i h_\triangle(n_i)\) produces the boundary
table below.

Here is a short justification that this minimization is analytic rather than
a sampled-angle claim. Between two orientations at which a loaded normal is
perpendicular to a triangle edge, the selected triangle vertices are fixed,
so the support sum is a sinusoid
\(f(\theta)=a\sin\theta+b\cos\theta\). Balanced loads make this sum
translation invariant, so we may translate the triangle to contain the
origin; every support value, and hence \(f\), is then nonnegative. Since
\(f''=-f\leq0\), it is concave on the cell and its minimum occurs at a
boundary. Up to the triangle's threefold symmetry there are only three
boundary types, obtained by
aligning one of the three loaded normals with a triangle-edge normal. Direct
substitution produces nine candidates (three loaded normals times three edge
normals), collapsing to at most three distinct values for each allocation.
The least values are exactly \(q_A,q_B,q_C\) above. The distinct boundary
values are below; `D` duplicates the `A` row by the mirror symmetry already
noted:

\[
\begin{array}{c|c|c}
 &\text{minimum}&\text{other boundary values}\\ \hline
A&q_A&{2007929\over51020400},\quad
 {6023787\over10753690000}+{10407096007\sqrt3\over516177120000}\\[2pt]
B&q_B&{489\over26896}+{247597\sqrt3\over6455040}\\[2pt]
C&q_C&{1197273\over1075369000}+{2068488653\sqrt3\over51617712000}.
\end{array}
\]

For completeness, all comparisons follow from

\[
 {265\over153}<\sqrt3<{1351\over780};
\]

indeed, \(3\cdot153^2-265^2=2\) and
\(1351^2-3\cdot780^2=1\).  In the order displayed in the table, the first and
fourth differences have negative \(\sqrt3\)-coefficient and use the upper
bound; the other two use the lower bound.  Substitution leaves, respectively,
the positive rational margins

\[
 {2598310099\over636734592000},\quad
 {2041656001\over9871887420000},\quad
 {353873\over197524224},\quad
 {21873778619\over20130907680000}.
\]

For \(\alpha\leq\phi\leq\beta\), expanding the absolute projections gives

\[
\begin{aligned}
 F_A(\phi)&=q_A+{29833549\over255102000}\sin\phi
                   +{163\over984}\cos\phi,\\
 F_S(\phi)&={40331857\over204081600}\sin\phi
                   +{163\over984}\cos\phi.
\end{aligned}
\]

There is no numerical sign decision in this expansion.  With the convention
above, an edge of direction angle \(\theta_i\) contributes
\((L_i-x_i)|\sin(\phi-\theta_i)|/4\).  On
\([\alpha,\beta]\), the signs for \(i=0,1,2,3,4\) are respectively
\(+,+,+,-,-\) before taking absolute values, where the direction angles are
\(-\beta,-\alpha,\alpha,\beta,\pi\).  Substitution of the rational sines and
cosines of \(\alpha,\beta\), followed by collecting \(\sin\phi\) and
\(\cos\phi\), gives the two displayed formulas.

For a hand check, the only angle data needed are

\[
 (\cos\alpha,\sin\alpha)=({5183\over5185},{144\over5185}),\qquad
 (\cos\beta,\sin\beta)=({9\over41},{40\over41}),
\]

together with
\(\sin(\phi+\gamma)+\sin(\gamma-\phi)=2\sin\gamma\cos\phi\)
and
\(\sin(\phi+\gamma)+\sin(\phi-\gamma)=2\cos\gamma\sin\phi\).
For example, allocation `C` exhausts edges 1 and 2.  Its two outer residuals
give

\[
 {1\over4}{163\over480}\,2\sin\beta\cos\phi
 ={163\over984}\cos\phi,
\]

while its closing residual is \(489/3280\), giving
\((489/13120)\sin\phi\).  Allocation `B` instead exhausts the two outer
edges; its two inner residuals and closing residual collect to
\((399091/2488800)\sin\phi\).  The same two identities give `A` and `S`
directly from their listed loads.

The special residuals in `C` and `B` remove the nearby sign changes, giving
the larger validity ranges

\[
\begin{aligned}
 F_C(\phi)&=q_C+{489\over13120}\sin\phi
                   +{163\over984}\cos\phi &&(0\leq\phi\leq\beta),\\
 F_B(\phi)&=q_B+{399091\over2488800}\sin\phi
                                      &&(\alpha\leq\phi\leq\pi/2).
\end{aligned}
\]

Every sine and cosine coefficient displayed here is nonnegative. Therefore
each \(F\) is concave on its stated subinterval of \([0,\pi/2]\).

## 3. Three exact cut points

The only tight switch is from `C` to `A`.  Their cosine terms cancel, so their
exact difference is

\[
 F_A(\phi)-F_C(\phi)
 ={231\over414800}-{399091\sqrt3\over19910400}
   +{1982981\over24888000}\sin\phi.
\]

It is strictly increasing on \([0,\pi/2]\), and its unique crossing in the
relevant range is therefore characterized without root finding by

\[
 \sin\phi_*=-{180\over25753}+{25915\sqrt3\over103012}.
\]

The coarse bounds \(265/153<\sqrt3<1351/780\) place this strictly between
\(\sin\alpha=144/5185\) and \(\sin\beta=40/41\): the two comparison margins
are at least
\(1927477523/4807054980\) and \(360308447/658864752\), respectively.
Thus \(\phi_*\in(\alpha,\beta)\).

Indeed, using \(\sqrt3<1351/780\), the sine at
\(\tan(\phi/2)=157/697\) exceeds \(\sin\phi_*\) by more than

\[
 {339847\over315499796976}>0.
\]

Since sine and the half-angle tangent are increasing on this interval, this
puts \(157/697\) just above \(\tan(\phi_*/2)\).  We do not need to use
the algebraic crossing itself: the nearby rational half-angle keeps every
substitution in \(\mathbb Q(\sqrt3)\) and leaves a positive exact margin.
The other two cuts have ample slack.

Choose

\[
 \tan(\phi_1/2)={157\over697},\qquad
 \tan(\phi_2/2)={1\over3},\qquad
 \tan(\phi_3/2)={3\over4}.
\]

The rational ordering

\[
 {1\over72}<{157\over697}<{1\over3}<{3\over4}<{4\over5}<1
\]

implies

\[
 \alpha<\phi_1<\phi_2<\phi_3<\beta<\pi/2.
\]

We use \(C,A,S,B\), respectively, on

\[
 [0,\phi_1],\quad[\phi_1,\phi_2],\quad
 [\phi_2,\phi_3],\quad[\phi_3,\pi/2].
\]

Concavity says that it is enough to check the endpoints.  The half-angle
identities are

\[
 \sin\phi={2u\over1+u^2},\qquad
 \cos\phi={1-u^2\over1+u^2},\qquad u=\tan(\phi/2),
\]

so every endpoint substitution is rational apart from the already displayed
linear occurrence of \(\sqrt3\).  In particular,

\[
 (\sin\phi_1,\cos\phi_1)=({109429\over255229},{230580\over255229}),
\]
\[
 (\sin\phi_2,\cos\phi_2)=({3\over5},{4\over5}),\qquad
 (\sin\phi_3,\cos\phi_3)=({24\over25},{7\over25}).
\]

A slightly sharper rational lower
approximation than the one used above is convenient:

\[
 {13775\over7953}<\sqrt3,
\]

whose square is the integer inequality \(13775^2<3\cdot7953^2\), again with
difference two. Put

\[
 T={1175341\over5000000}=0.2350682.
\]

Subtracting \(T\), the endpoint margins have the following exact lower bounds:

\[
\begin{array}{c|c|c}
\text{bound}&\text{endpoint}&F-T\\ \hline
C&0&> {16476634489\over922193730000000}\\[2pt]
C&\phi_1&> {8185416274231\over235370583514170000000}\\[2pt]
A&\phi_1&> {3607959559211\over27690656884020000000}\\[2pt]
A&\phi_2&> {5340181734103\over1844387460000000}\\[2pt]
S&\phi_2&= {638863249\over39859687500}\\[2pt]
S&\phi_3&= {660076109\over637755000000}\\[2pt]
B&\phi_3&= {1082653609\over637755000000}\\[2pt]
B&\pi/2&= {1724445453\over212585000000}.
\end{array}
\]

All entries are strictly positive; the tightest is the `C` row at \(\phi_1\),
whose displayed lower margin is still positive in exact integer arithmetic.
Hence the pointwise maximum of the legal support bounds is at least \(T\)
throughout \([0,\pi/2]\).

## 4. Complete direct-motion domain

A global half-turn about the midpoint of the pinned, unoriented segment
fixes that segment as a set and sends an admissible triangle orientation to
another admissible orientation.  It therefore reduces the new hull angle
modulo \(\pi\), or equivalently reduces the relative angle \(\phi\) modulo
\(\pi\).  Within \([0,\pi]\), write \(\mu\) for the index involution

\[
 (0,1,2,3,4)\longmapsto(3,2,1,0,4)
\]

This involution preserves the hull loads and satisfies the termwise identity

\[
 |\det(v_i,e_{\pi-\phi})|
   =|\det(v_{\mu(i)},e_\phi)|.
\]

It fixes `S`, `B`, and `C`, and swaps `A` with
`D`; the triangle floor of `D` equals \(q_A\), because the equilateral
triangle has a reflection symmetry (the two reflections compose to an
allowed rotation).  Term-by-term absolute projection identities therefore
send each bound used at \(\phi\) to a legal bound of the same value at
\(\pi-\phi\).  Thus the proof on \([0,\pi/2]\)
covers the full orientation domain.  This uses a direct global rotation and
an algebraic pairing of bounds, not reflection of the worm.

Conditional on the mixed-area bridge, every simultaneous placement of the
segment, side-\(1/2\) equilateral triangle, and this exact unit worm therefore
has convex-hull area at least

\[
 \boxed{{1175341\over5000000}=0.2350682}>{47\over200}.
\]

The improvement over the old tree target is the exact positive amount
\(341/5000000\), not a decimal-rounding artifact.

The finite-family reduction is then immediate: a universal convex cover
contains a directly congruent copy of each of these three unit arcs.  The
convex hull of those three copies lies inside the cover, so the cover's area
is no smaller than the displayed simultaneous-placement bound.

## Verification boundary

This note proves only the angular/support calculation, at status `sketch`.
It does not prove the finite-polygon mixed-area/common-fan bridge, does not
grant review status to the frozen Issue #178 checker, and is not assumable by
later claims until the required independent review has approved the complete
dependency chain.
