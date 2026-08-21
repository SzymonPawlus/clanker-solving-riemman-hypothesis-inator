# Kill-criteria, recorded before any computation

Attack: `eo-oler-equality` — the **equality / stability case of Oler's inequality**, the one
route [`../oler-lower-bound/`](../oler-lower-bound/) §5.2 identifies as missing after issue #44
established that Oler's Acta paper contains no equality characterisation.
Author: `claude` (Claude Opus 5 — convergent role, `RULES.md` §8), 2026-08-21.
Written before `experiments/packing-eo-equality/run.py` exists.

**Normalisation.** Separation $1$; $E$ finite with pairwise distances $\ge 1$;
$P=\operatorname{conv}(E)$; $n=|E|$; $A,M$ area and perimeter; $b=|E\cap\partial P|$;
$\operatorname{slack}(E) = \frac{2}{\sqrt3}A(P)+\frac12 M(P)+1-n \ge 0$ (Oler, `cited`).
The repo's certificates use separation $2$ and side $d=2a$; nothing here reads them.

Target, in the manager's ordering: **(A)** full equality characterisation, **(B)** quantitative
stability, **(C)** equality for the special case that the hull is the whole triangle / all three
corners occupied. I state up front that I expect to hold **(C)** at best.

## K1 — primary (correctness of the base case)

> The base case of any equality induction is the single triangle: *for every triangle with all
> three sides $\ge 1$, $\frac{2}{\sqrt3}A + \frac{p}{2} \ge 2$, with equality only for the unit
> equilateral triangle and for the degenerate triple $(2,1,1)$.* If an exactly-verified triangle
> with all sides $\ge 1$ violates that inequality, or if a third equality triple exists, the
> base case is false, every downstream statement in this attack collapses, and I stop and report
> the refutation as the result.

## K2 — scope (does the target even close $k = 7$?)

> If the equality characterisation, **granted in full**, still leaves a non-empty set of side
> lengths $a < 6$ at which 27 unit-separated points are not excluded, then target (A) is
> *insufficient* for the team hypothesis. I must record that in the first line of the write-up,
> drop to (C), and **not** present an equality theorem as a route that closes $k = 7$.
> Forbidden per `RULES.md` §6.3: re-scoping "equality" to mean "stability" after the fact and
> claiming the target was met.

## K3 — control (the candidate extremal class)

> My candidate is: $\operatorname{slack}(E)=0$ iff $E=\Lambda\cap P$ for a unit triangular
> lattice $\Lambda$, with every edge of $P=\operatorname{conv}(E)$ of length exactly $1$ between
> consecutive points of $E$. If any such $E$ has $\operatorname{slack}\ne 0$ exactly, or if some
> lattice-convex $E$ with a hull edge of length $>1$ has $\operatorname{slack}=0$ exactly, the
> statement of the characterisation is wrong and must be corrected, not patched.

## K4 — duplication (`RULES.md` §6.1)

> Anything I derive that is already recorded in `attacks/` is cited to its author and **not**
> reclaimed, however independently I reached it. In particular the refutation of face-excess
> nonnegativity (`oler-slack-analysis` §4), its lattice-perturbation strengthening
> (`eo-boundary-counting` §4, W1), the $k=7$ window $a\in[(-3+\sqrt{217})/2,\,6)$
> (`eo-boundary-counting` §2, O1), and the Barrier Theorem (`eo-hull-deficit` §6) are all
> pre-existing. If my line of attack reduces to one of them, that is a dead end, not a result.

## What counts as success short of the goal

A proved equality lemma that is *new to this repo and checkable* (even a base case), an exact
identification of the extremal class, or a precise statement of why the equality route cannot
reach the team hypothesis. All three are reportable outcomes; a hand-wave at (A) is not.
