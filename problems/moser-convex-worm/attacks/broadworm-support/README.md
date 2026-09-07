# Exact point-support proof for the calliper width

**Status:** sketch pending independent cross-review.  This note replaces the
convexity/separation step left open in `broadworm-width` by an explicit point
witness in every direction.  It does not use sampled angles, convexity of the
arc, or the disk criterion.

## Statement

Use the notation of `broadworm-width`: (A=(0,0)), (B=(d,0)),
(F=(d/2,1)), where

\[
 1<d<2/\sqrt3.
\]

Let \(\Gamma\) be the calliper consisting of (AC), the minor unit-circle
arc (CD) about (B), (DF), and its reflection in (x=d/2).  Then for
every unit vector (n),

\[
 \max_{x\in\Gamma}n\mathbin\cdot x-
 \min_{x\in\Gamma}n\mathbin\cdot x\geq1. \tag{W}
\]

It is enough to prove this for normals
(n_\theta=(\cos\theta,\sin\theta)), (0\leq\theta\leq\pi).
Reflection in (x=d/2) sends (n_\theta) to a translated support problem
with normal (n_{\pi-\theta}), and width is translation invariant.  Hence it
is enough to cover (0\leq\theta\leq\pi/2).

## The exact three-sector cover

Put

\[
 \gamma_C=\arctan\sqrt{d^2-1},\qquad
 \gamma_D=2\arctan(d/2).
\]

Reflection in (x=d/2) sends the circle arc (CD) about (B) to the unit
circle arc about (A) with endpoints

\[
 C'=\left(d^{-1},{\sqrt{d^2-1}\over d}\right)=n_{\gamma_C},
 \quad
 D'=\left({d\over1+d^2/4},{1-d^2/4\over1+d^2/4}\right)
     =n_{\gamma_D}.
\]

Both angles lie in ((0,\pi/2)), and \(\gamma_C<\gamma_D\).  One convenient
exact ordering proof is

\[
 \gamma_C<\pi/6
 \quad(d^2<4/3),
 \qquad
 \gamma_D>2\arctan(1/2)>\pi/6;
\]

the last inequality is equivalent to
(1/2>\tan(\pi/12)=2-\sqrt3), which follows from
(\sqrt3>3/2).  Therefore the reflected minor arc contains (n_\theta)
for every \(\theta\in[\gamma_C,\gamma_D]\).

Now the entire first quadrant is covered by three closed sectors.

1. If (0\leq\theta\leq\gamma_C), the two points (A,B\in\Gamma) give
   \[
     n_\theta\cdot(B-A)=d\cos\theta
       \geq d\cos\gamma_C=1.
   \]
2. If \(\gamma_C\leq\theta\leq\gamma_D\), the actual arc point
   (n_\theta\in\Gamma) and (A\in\Gamma) give projection difference
   exactly one.
3. If \(\gamma_D\leq\theta\leq\pi/2\), use (F,A\in\Gamma).  The function
   \(r(\theta)=(d/2)\cos\theta+\sin\theta\) is concave on this interval,
   so its minimum is at an endpoint.  At the endpoints,
   \[
   r(\pi/2)=1,
   \qquad
   r(\gamma_D)-1=
   { (2-d)(d^2+4d-4)\over 8(1+d^2/4)}>0. \tag{1}
   \]
   Here (2-d>0) and (d^2+4d-4>1) follow directly from
   (1<d<2/\sqrt3<2).

In each sector two named points of the arc have projection difference at
least one, which implies (W) without identifying either global support point.
The sector endpoints overlap, so there is no limiting-direction gap.

## Connection to the repaired `0.232239` cover

Let (L) be the exact calliper length certified in `broadworm-exact`, and
scale the arc by (L^{-1}).  Width homogeneity turns (W) into

\[
 w_{L^{-1}\Gamma}(n)\geq L^{-1}=b_0>0.438925
 \quad\text{for every }n. \tag{B}
\]

Thus, in any orientation used by the repaired angular cover, compactness
provides two actual broadworm points whose projection separation in the
required rectangle direction is at least (b_0).  Substitution into the
global rectangle-width lemma gives its broadworm branch

\[
 g(\alpha)=\frac14\left(\frac12
       \cos(\alpha-\theta_0)+b_0\right),
 \qquad \theta_0=\arctan(1/2).
\]

This is precisely the geometric support premise consumed by
`baseline-0232239/verify_repaired_cases.py`; that checker then proves the
finite closed angular cover.  The chain remains capped by the weakest
dependency status: the exact length certificate, rectangle-width lemma, and
the other witness-to-formula reductions retain their separately stated
review boundaries.

## Replay

`verify_partition.py` checks, over exact rationals, the parameter implications
and the factorisation used in the three-sector proof:

```text
python3 problems/moser-convex-worm/attacks/broadworm-support/verify_partition.py
```

The script is an algebraic replay aid, not a numerical angle sampler and not
a substitute for reviewing the proof above.
