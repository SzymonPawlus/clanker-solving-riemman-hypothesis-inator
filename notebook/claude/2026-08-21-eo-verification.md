# 2026-08-21 — verification pass over the day's Erdős–Oler lemmas

Role: verifier. Six claims from `eo-exhaustion`, `eo-hull-deficit`, `eo-small-cases`, none of which
had been checked by anyone while other provers were being told to build on them. Wrote my own exact
checkers in `experiments/packing-eo-verify/` (101 checks, all passing) and did not read any
author's code. Report: `attacks/eo-verification/README.md`.

## The one that matters

I nearly shipped a wrong "disagreement" as my headline finding.

I had convinced myself that `eo-hull-deficit` §9's necessary condition — *the open corner triangle
of side $j$ holds at least $T(j)$ points* — was off by one, and that the truth was $T(j)-1$. The
reasoning was: the gain $\frac{t^2+t}{2} - m$ has supremum $T(j)-m$ as $t\to j^-$, the supremum is
not attained, so to get a gain of **1** you need $m \le T(j)-2$.

The error is in "to get a gain of 1". A contradiction does not need gain $\ge 1$; it needs
gain $> \varepsilon(a)$, and $\varepsilon(a) = \Omega(a) - (\Delta(k)-1) < 1$ **strictly** for every
$a < k-1$. So the non-attained supremum is fine: the constraint "gain $\le \varepsilon$ for all
$t<j$" is a closed condition and transfers to the supremum, giving $T(j) - m \le \varepsilon < 1$,
hence $m \ge T(j)$ for integer $m$. The headline is right, exactly as written, including the choice
of the open rather than the closed triangle.

Three things about this are worth keeping.

1. **I was fluent and wrong in exactly the direction §0 warns about, while acting as the check.**
   The bad finding would have been the most consequential thing in my report, and it would have
   sent the prover working the contrapositive back to redo correct work.
2. **What caught it was writing the threshold as an exact predicate parameterised by $\varepsilon$
   and testing it, instead of writing prose.** The prose version of my error reads perfectly well.
   The predicate version has $\varepsilon$ in it and the mistake becomes a typo you can see.
3. **The lesson generalises to this whole problem: 1 is not the budget, $\varepsilon(a)$ is.**
   Every argument here lives at a supremum that is not attained, and whether that matters depends
   on whether the thing you must beat is $1$ or something strictly below $1$. `eo-hull-deficit`
   gets this right in §§4, 7, 9 and slightly wrong in §9's two "sharper" instances (which say
   "the root" where they need "strictly above the root"). Same subtlety, both directions.

I recorded the whole thing in §0.1 of the report rather than quietly deleting it, per §0.

## What actually broke

Six disagreements, of which one is doing real damage:

**"Every partition-and-count refinement of Oler is dead"** — false, and refuted by this repo's own
EO(3) proof. The `eo-exhaustion` §3 *lemma* is correct (I re-derived it; it needs two hypotheses the
write-up omits). It says that capping each piece **by Oler's bound** always loses $I+(m-1)$. It has
been read as saying that capping each piece by *anything* loses. But `eo-small-cases` §2 caps four
cells at their true capacity 1 and gets $n\le4$ where Oler gives $n\le5.9965$ — a partition beating
Oler by nearly two points. `eo-exhaustion` §1 states that same argument itself, as its "one
exception". Two routes were reportedly killed on the broad reading; they should be reopened.

The general shape of the other five: **the theorems are right and the sentences around them are
broader than the theorems.** Theorem 6 is a genuine theorem at integer side and I could not dent it
over ~10 000 exact convex cuts — but its equality family is every lattice line, not just corner
triangles; its extension below integer side is vacuous (at $a=5.9$ it permits a gain of 6.25 where
1 is needed); and "no convex-cut relaxation improves Oler at all" is true only for
worst-case-charged relaxations, which the file's own CIO is not. The exhaustion-impossibility
argument's topology is simply wrong as written ($\bigcap_{\varepsilon>0}$ of a *decreasing* family
is not the limit at $\varepsilon=0$, and under EO every member is empty), though the narrow
conclusion is true for a trivial monotonicity reason the file never gives.

That pattern — correct theorem, oversold sentence, manager quotes the sentence — is I think the
main failure mode of a fast multi-worker day, and it is not caught by checking the proofs. It is
caught by asking "what exactly does this kill?" of every kill claim.

## What held up

- **Corollary 4** (conditional EO) is sound, and sound under *both* readings of "empty" — the open
  hypothesis is the weaker one and is exactly what the proof uses, so the open/closed distinction
  the brief warned about does not bite here.
- **The Corner-Deficit Lemma** holds on 2148 random exact configurations satisfying its side
  condition, with equality on the whole one-parameter extremal family (not just the two cases the
  file reports tight). The side condition is exactly the disjointness condition for the three
  corner triangles, and it is load-bearing: 660 of 1852 violating configurations break the lemma.
- **The $k=3$ proof** is the cleanest thing produced today. $m^2$ cells verified for $m\le7$, all
  exactly equilateral of side $a/m$; covering verified two independent ways; the closed-cell
  double-counting worry is harmless in the upper-bound direction; strictness in $a<m$ correctly
  load-bearing. It is also the best Lean target in the repo — a finite covering argument with an
  exact diameter bound and no Mathlib gap I can see.

## Method note, for next time

Working in lattice coordinates $(u,v)\mapsto(u+v/2, v\sqrt3/2)$ made the whole pass cheap: squared
distances become $du^2+du\,dv+dv^2$ (rational), and Oler's $\frac2{\sqrt3}A$ term becomes exactly
the $(u,v)$-shoelace (rational). Only edge lengths leave $\mathbb Q$, and a formal
sum-of-square-roots type handles those with exact equality. Nothing needed intervals except sign
tests. If someone formalises any of this, that coordinate choice is the thing to reuse.

The other reusable trick: for each claim, build the *worst* configuration for it and check
equality, rather than sampling and checking the inequality. That is how the Corner-Deficit Lemma's
tightness family showed up, and how the boundary case $t_U+t_V=a$ got tested at all — my first
attempt at "just inside the boundary" silently constructed a configuration on the *other* side of
it, and only failed loudly because I had asserted the side condition as part of the test.

## Status

Nothing here grants status. Same model family as every author (`RULES.md` §5), so all six claims
remain `sketch` and non-assumable — including the five I confirmed. Said so at the top of the
report, in a box, because the risk is that "verified by the verifier" gets quoted.
