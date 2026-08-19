# 2026-08-19 — exactifying triangle packings (issue #74)

Worker A3. Goal: turn float packings into exact algebraic coordinates with a machine-checkable
feasibility certificate. Upper bounds only — I kept saying that to myself because §0 says the
failure mode is fluent drift, and PR #64 got caught on exactly this overreach.

## What worked

Choosing the arithmetic before the geometry. Representing coordinates in a multiquadratic field
$\mathbb{Q}(\sqrt{p_i})$ over `Fraction` — a $\mathbb{Q}$-combination of $\sqrt{\prod S}$ over
prime sets $S$ — made equality *syntactic*: an element is zero iff every coefficient is zero,
because square roots of distinct squarefree integers are independent over $\mathbb{Q}$. That one
fact removes tolerance from the entire checker. Sign then falls out of rational bracketing that
provably halts. ~200 lines of stdlib, no sympy in anything shipped.

The payoff was that I could then stop worrying about numerics and think about triangles.

## The bit I'd have got wrong without the rules

`RULES.md` §2's "consistency of `side_length`" — containment alone certifies $s(n) \le s$ for any
inflated $s$, so a certificate that only checks feasibility is nearly vacuous. Computing the exact
minimal enclosing $d_{\min} = \max_i (x_i + y_i/\sqrt3)$ and reporting tightness is what makes the
number mean something. I wrote a negative test where an inflated $s$ *passes* feasibility but is
reported not-tight, and a second where a certificate lies about being tight and is rejected.

## $n = 8$

The only one needing real algebra, and the only one leaving $\mathbb{Q}(\sqrt3)$. Nice collapse:
for the top trio (two edge points + apex) all three contacts reduce to the *same* equation
$d - 2u = 2$, because the displacement from an edge point to the apex is parallel to an edge. Two
equations left, root $d = 2 + 2\sqrt{33}/3$ — the published value. And $\sqrt3 u = \sqrt{11}$
exactly, which I did not expect.

## $n = 7$ has a rattler

The optimiser's 7th point had zero contacts. §5 says don't "fix" rattlers, so I placed it at
$(d/2, 0)$ and certified it feasible rather than pretending it was determined. Worth remembering
that a rattler is not a convergence failure.

## What I didn't get

$n = 11, 12, 13$. The search didn't converge for $n \ge 11$ inside the budget on shared CPUs, so
I had no contact graph to exactify. The exactification method is fine — it's starved of input.
Next worker: run the search longer for those three, the closed forms to aim at are already in the
problem README.

## Note to self

I nearly wrote "confirms $s(8) = 2 + 2\sqrt3 + 2\sqrt{33}/3$". It doesn't. It confirms
$s(8) \le$ that. The equality is Melissen's, and it's `cited`, and it is not mine to restate as
though the certificate produced it.
