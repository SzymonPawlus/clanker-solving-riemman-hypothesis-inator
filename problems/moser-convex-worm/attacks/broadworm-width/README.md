# Directional-width proof for the exact broadworm

**Status:** sketch. This independently reconstructs the load-bearing width
lemma from Adhikari--Pitman; it requires cross-review before it can discharge
the broadworm dependency of the `0.232239` benchmark.

## Claim actually needed

Let \(\Gamma\) be the unit-width calliper arc from Adhikari--Pitman Section 2,
and let \(L\) be its length. For every unit normal \(n\),

\[
 \max_{x\in\Gamma}n\cdot x-\min_{x\in\Gamma}n\cdot x\geq1. \tag{W1}
\]

After scaling by \(1/L\), the resulting unit-length rectifiable arc has width
at least \(b_0=1/L>0.438925\) in every direction. This—not global optimality
among all unit arcs—is the only broadworm fact used in the repaired Moser area
argument.

## Exact geometry

Take \(1<d<2/\sqrt3\),

\[
 A=(0,0),\quad B=(d,0),\quad F=(d/2,1),
\]

and define tangency points on the unit circle about \(B\):

\[
 C=\left(d-d^{-1},{\sqrt{d^2-1}\over d}\right),
\quad
 D=\left(d-{d\over1+d^2/4},{1-d^2/4\over1+d^2/4}\right).
\]

Traverse \(AC\), the minor circle arc \(CD\) centered at \(B\), and \(DF\),
then reflect this half in \(x=d/2\) and traverse the reflected half to \(B\).
The algebraic checks behind the construction are

\[
 |B-C|=|B-D|=1,quad (A-C)\cdot(B-C)=0,
 \quad(F-D)\cdot(B-D)=0. \tag{T}
\]

Thus the line pieces meet the circle tangentially. The reflection supplies the
corresponding identities about the unit circle centered at \(A\). Tangent
directions turn monotonically along the traversal, so \(\Gamma\cup BA\) is
the boundary of a compact convex set lying above \(AB\).

## Disk criterion

For completeness, the Adhikari--Pitman Section 2 lemma can be stated without
any optimization:

> Let a convex arc from \(A=(0,0)\) to \(B=(d,0)\), \(d>1\), lie above
> \(AB\). If it meets the line \(y=1\) at \(F\), its subarc \(A\to F\)
> avoids the open unit disk centered at \(B\), and its subarc \(F\to B\)
> avoids the open unit disk centered at \(A\), then its width in every
> direction is at least one.

The calliper satisfies these conditions exactly. It contains \(F=(d/2,1)\).
The first half is the shortest obstacle-avoiding path made of a tangent,
boundary arc, and tangent around the open disk centered at \(B\), hence never
enters that disk. Reflection gives the other half and disk.

## Support-direction proof of the criterion

Write \(K=\operatorname{conv}(\Gamma)\). Since the arc is convex,
\(\partial K=\Gamma\cup AB\). It suffices to consider unoriented normals
through angles \([0,\pi]\).

1. For the horizontal normal, \(A,B\in K\) give width \(d>1\).
2. For the vertical normal, \(AB\subset\{y=0\}\) and \(F\in\{y=1\}\), so
   the width is at least one.
3. Let \(n=(\cos\theta,\sin\theta)\), \(0<\theta<\pi/2\). The line
   \(n\cdot x=1\) is tangent to the open unit disk about \(A\), while
   \(n\cdot x=0\) passes through \(A\). The subarc \(F\to B\) is connected,
   lies outside that disk, begins above \(y=1\), and ends at \(B\) on the
   other side of the tangent direction. Convexity forces it to meet or lie
   beyond the tangent support line. Hence \(h_K(n)\geq1\) and
   \(h_K(-n)\geq0\), giving width at least one.
4. For \(\pi/2<\theta<\pi\), reflect the preceding argument: use the unit
   disk about \(B\), the subarc \(A\to F\), and the tangent line at distance
   one from the parallel through \(B\).

These four cases cover the closed projective circle of directions, including
all boundaries. They are exactly the horizontal, vertical, down-sloping, and
up-sloping parallel cases in the primary proof.

An alternative compact formulation uses separation: if the relevant subarc
did not reach the unit tangent line, convexity would put it strictly inside the
corresponding open tangent half-plane; together with its endpoint and the line
\(y=1\), this would force an intersection with the forbidden open disk. This
is the contrapositive drawn in Adhikari--Pitman's Figures 5--6.

## Scaling and the Moser height predicate

For \(\widetilde\Gamma=L^{-1}\Gamma\), rectifiable length and every support
value scale by \(L^{-1}\). Therefore

\[
 \operatorname{length}(\widetilde\Gamma)=1,qquad
 w_{\widetilde\Gamma}(n)\geq L^{-1}=b_0>0.438925
\]

for every direction \(n\). Compactness ensures the maximum and minimum support
values are attained at two actual points of the arc. Those two points are the
pair \(S,T\) used in the rectangle-width lower bound in the `0.232239` proof.

## Orientation and reflection

The unlabelled calliper set is fixed by reflection in \(x=d/2\), with traversal
reversed. If \(R\) is any planar reflection and \(S\) is this intrinsic
symmetry, \(R\circ S\) is orientation-preserving and
\(R(\Gamma)=(R\circ S)(\Gamma)\). Hence allowing only translations followed
by rotations loses no reflected placement of this witness. Support width is
itself invariant under traversal reversal, translation, rotation, and
reflection.

## Audit boundary

The disk criterion is primary-source cited, and its four support cases are
reconstructed above. The most delicate sentence is the convexity/separation
step in cases 3--4; an independent reviewer should reproduce that step from
the source figures or formalize it as a half-plane lemma. No sampled-angle or
floating-point check is being offered as a substitute.
