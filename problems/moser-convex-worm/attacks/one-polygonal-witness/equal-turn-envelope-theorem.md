# Exact equal-turn support-envelope theorem

**Status:** `sketch`, frozen for independent review.  This note proves the
one-dimensional minimization theorem conditional on the two support-allocation
formulae displayed below.  It is not a proof of the mixed-area bridge and does
not claim a global minimum for simultaneous placements.

## Family and envelope

Let `0 <= c <= 1`, let `s = sqrt(1-c^2)`, and take a three-edge open arc whose
edge vectors are one third of the unit vectors at angles `0, theta, 2 theta`,
where `cos(theta)=c` and `sin(theta)=s`.  If `phi` is the direction of the
middle edge relative to the pinned segment, the two support allocations give

\[
 W_c(\phi)={\sqrt3\over24}
 +{|\sin(\phi-\theta)|+|\sin(\phi+\theta)|+2c|\sin\phi|\over12},
\]
\[
 C_c(\phi)={|\sin(\phi-\theta)|+|\sin(\phi+\theta)|
 +2(1+c)|\sin\phi|\over12}.
\]

These formulae concern the support envelope only.  Their geometric
interpretation inherits the status of the support-allocation and mixed-area
lemmas on which they depend.

## Global angular minimum

Put

\[
 A_0(c)={\sqrt3\over24}+{s\over6},\qquad
 A_s(c)={s(1+2c)\over6}.
\]

Then the exact minimum over the complete orientation-preserving angular domain
is

\[
 \boxed{\min_{\phi\in\mathbb R}\max(W_c(\phi),C_c(\phi))
       =\min(A_0(c),A_s(c)).}
\]

Here is a proof that does not subdivide angles numerically.  With
`z=|sin(phi)|`,

\[
 |\sin(\phi-\theta)|+|\sin(\phi+\theta)|
 =2\max(cz,s\sqrt{1-z^2}).
\]

Also `C_c(phi)-W_c(phi)=z/6-sqrt(3)/24`.  On each of the intervals cut out by
`z=0`, `z=sqrt(3)/4`, `z=s`, and `z=1`, the resulting expression is either
linear or a positive linear combination of `z` and `sqrt(1-z^2)`, hence is
concave.  Its minimum is therefore attained at a listed endpoint.  The three
nonduplicated values are

\[
 A_0(c),\quad A_s(c),\quad
 B(c)={s\sqrt{13}+(1+c)\sqrt3\over24}.
\]

The third never lowers the other two.  To see this, define

\[
 c_*^2={4-\sqrt{13}\over8}.
\]

For `c >= c_*`, direct subtraction gives

\[
 24(B-A_0)=\sqrt3c-(4-\sqrt{13})s\ge0;
\]

the equality threshold follows by squaring the two nonnegative sides.  For
`0 <= c <= c_*`, the same squaring calculation applied to

\[
 24(B-A_s)=(1+c)\sqrt3-s(4+8c-\sqrt{13})
\]

gives `B >= A_s`, again with equality only at `c=c_*`.  Thus
`B >= min(A_0,A_s)` throughout `[0,1]`.

No reflection quotient is used.  The formula is periodic under the global
half-turn `phi -> phi+pi`, so `[0,pi]` is a complete direct-motion domain; the
half-turn merely reanchors translations about the pinned segment midpoint.

## Unique best member

The equality `A_0(c)=A_s(c)` is

\[
 cs={\sqrt3\over8}.
\]

Its first root is `c=c_*`; explicitly

\[
 c_* = \sqrt{{4-\sqrt{13}\over8}},\qquad
 s_* = \sqrt{{4+\sqrt{13}\over8}}.
\]

On `[0,c_*]`, the global floor is `A_s`.  Its derivative has the sign of
`2- c-4c^2`, which is positive there.  For `c>c_*`, the floor is at most
`A_0`, which is strictly decreasing.  Consequently `c_*` is the unique global
maximizer, and the optimal support-envelope floor is

\[
 L_*={\sqrt3\over24}+{1\over6}
       \sqrt{{4+\sqrt{13}\over8}}
     =0.2346746732371\ldots .
\]

The exact optimizer is itself an allowed algebraic unit witness.  In traversal
order its vertices are

\[
 (0,0),\quad(1/3,0),\quad((1+c_*)/3,s_*/3),
 \quad((c_*+2c_*^2)/3,s_*(1+2c_*)/3).
\]

Every consecutive difference is one third of a unit vector, so the three
edge lengths are exactly `1/3` and the open arc has length exactly one.  The
repository rules permit algebraic vertices.  A replay certificate would have
to encode the nested radicals by minimal polynomials plus isolating rational
intervals (or an exact real-algebraic type); the existing rational
`Fraction`-style certificate format cannot silently treat these coordinates
as rational.

## A stronger rational witness

A compact rational alternative uses the half-angle parameter

\[
 t={2396\over3003}>{s_*\over1+c_*}.
\]

It gives

\[
 c={3277193\over14758825},\qquad
 s={14390376\over14758825}.
\]

The inequality `c<c_*` is exact: `4-8c^2` is positive and its square is
greater than `13`.  Hence `cs<sqrt(3)/8`, so the smaller endpoint is the
rational value `A_s`.  The vertices are

```text
(0,0)
(1/3,0)
(6012006/14758825, 4796792/14758825)
(69847505896723/653468746141875,
 102235040019112/217822915380625)
```

All three squared edge lengths are exactly `1/9`.  The globally certified
support-envelope endpoint is exactly

\[
 {51117520009556\over217822915380625}
 =0.234674666438253\ldots
 >\boxed{0.2346746664}>0.232239.
\]

The boxed decimal is rounded downward.  This improves the earlier small
half-angle candidate `75/94` at the cost of larger rational coordinates.  It
still remains conditional on independent approval of the geometric bridge;
the theorem here only eliminates the angular minimization gap.
