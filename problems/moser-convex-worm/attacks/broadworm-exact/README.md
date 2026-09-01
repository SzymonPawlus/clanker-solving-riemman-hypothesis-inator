# Exact broadworm dependency for the Moser benchmark

**Status:** sketch with exact terminal replay. The classical geometric theorem
is `cited`; the reconstruction and its use in the `0.232239` proof still need
independent review.

## Pinned primary source

A. Adhikari and J. Pitman, *The Shortest Planar Arc of Width 1*, Berkeley
Statistics Technical Report 113 (September 1987), subsequently *American
Mathematical Monthly* **96** (1989), 309--327. The Berkeley-hosted 31-page PDF
has SHA-256
`0e147bad35d8cd046649e8860bbd41bded631e9b34b870388e2876e27c4c8031`.

Adhikari--Pitman explicitly rediscover the Zalgaller/Schaer curve, call it the
*calliper*, construct it in Section 2, and prove it is shortest among all arcs
of width one in Sections 3--4. Schaer's 1968 Calgary Research Paper 52 is not
available in the repository or through the located public archives; the 1987
report is therefore the accessible primary proof used here.

## Ordered construction

Let \(d\in(1,2/\sqrt3)\), put

\[
 A=(0,0),\quad B=(d,0),\quad F=(d/2,1),
\]

and let \(C,D\) be the successive tangency points on the unit circle centered
at \(B\):

\[
 C=\left(d-{1\over d},{\sqrt{d^2-1}\over d}\right),
\]

\[
 D=\left(d-{d\over1+d^2/4},
 {1-d^2/4\over1+d^2/4}\right).
\]

The first half of the arc traverses the segment \(A C\), the minor circular
arc \(C D\) centered at \(B\), and the segment \(D F\). Reflect this half in
the perpendicular bisector \(x=d/2\) and traverse the reflection from \(F\) to
\(B\). Thus the full ordered path is

\[
 A\to C\to(\text{circle about }B)\to D\to F\to
 \bar D\to(\text{circle about }A)\to\bar C\to B.
\]

It consists of four line segments and two circular arcs, hence is continuous
and rectifiable. Adhikari--Pitman's width lemma shows this path has minimum
width one.

The minimizing \(d=d_*\) is the unique positive root in the recorded isolating
interval of

\[
 3d^6+36d^4+16d^2-64=0.
\]

Its unit-width length is

\[
 L(d)=2\sqrt{d^2-1}+d+\pi
 -2\arctan\sqrt{d^2-1}-4\arctan(d/2).
\]

Scaling every point by \(1/L(d_*)\) produces an arc of length exactly one.
Widths scale by the same factor, so its minimum width is exactly
\(b_0=1/L(d_*)\).

## Directed constant

Replay with

```text
python3 problems/moser-convex-worm/attacks/broadworm-exact/verify_constant.py
```

The checker isolates the algebraic root by exact polynomial signs, encloses
the square root, \(\pi\), and arctangents with rational intervals, and proves

\[
 b_0>0.438925.
\]

No binary floating-point value enters an accepted predicate. This is the
directed breadth hypothesis needed by the repaired `0.232239` angular cover.

## Orientation and reflection

The ordered arc is symmetric as an unlabelled set under reflection in
\(x=d/2\); reflection merely reverses its traversal. Any reflection \(R\) of
the plane can be written as an orientation-preserving isometry composed with
this symmetry. Hence every reflected broadworm set is obtainable by a
translation and rotation of the original set. The witness is therefore
compatible with the repository convention that allowed placements use no
reflections.

For the Khandhawit--Pagonakis--Sriswasdi area argument, only the definition of
minimum width is used: in every direction there are two points of the placed
broadworm whose transverse separation is at least \(b_0\). Rotation and
translation preserve this statement. No vertex sampling, contact conjecture,
or choice of traversal direction enters the height bound.

## Remaining review boundary

- The exact interval replay checks the constant, not the full geometric proof
  that the displayed concatenation has width one or is globally shortest.
- Global optimality is unnecessary for the Moser witness: it suffices that
  this explicit rectifiable unit arc has minimum width at least `0.438925`.
- An independent reviewer should reconstruct the tangency coordinates,
  ordered arc length, and Adhikari--Pitman width lemma before the dependency is
  promoted beyond `sketch`.
