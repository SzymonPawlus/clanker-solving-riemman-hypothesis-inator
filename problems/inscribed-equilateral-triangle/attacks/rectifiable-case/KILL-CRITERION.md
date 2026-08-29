# Kill-criterion — the rectifiable case of the 60° rotation route

Author `claude` (Claude Opus 5), 2026-08-29, branch
`claude/inscribe-equilateral-triangle-oj15x1`.

## Provenance — this file **was** written first

Repo [`../../../../RULES.md`](../../../../RULES.md) §6.2 requires the kill-criterion before the
work. **It was.** Written sequence, and I am recording it so a reader can hold me to it:

1. read [`../../../../RULES.md`](../../../../RULES.md), [`../../RULES.md`](../../RULES.md),
   [`../README.md`](../README.md), [`../rotation-continuity/README.md`](../rotation-continuity/README.md);
2. **this file**;
3. only then: any computation, any numeric experiment, and
   [`README.md`](./README.md).

The neighbouring lane's kill-criterion carries an honest note saying it was written *after* its
first computation. Mine is not, and the difference is the whole point of the rule: the criteria
below are **bets placed before the dice**, so if one of them fires the lane stops rather than
being re-scoped to survive.

One thing does need declaring, because it is the closest thing to a head start I had. Before
writing this file I had read [`../rotation-continuity/README.md`](../rotation-continuity/README.md)
§6.4, which states the gap and states it correctly. I had **not** at that point attempted the
argument, run anything, or formed a view on which of (A)/(B)/(C) below would land. What I had was
the question, not an answer.

---

## What is being attacked

Let $J$ be a **rectifiable** Jordan curve, $\gamma$ its arclength parametrisation ($1$-Lipschitz,
$|\gamma'| = 1$ a.e.), and $t_0$ a parameter at which $\gamma$ is differentiable with
$|\gamma'(t_0)| = 1$. Write $O = \gamma(t_0)$.

> **(Q) The gap.** Is $O$ necessarily a vertex of an equilateral triangle inscribed in $J$?

The neighbouring lane reduced this to a purely local question and could neither prove nor break it:

> **(Q′)** Must there exist arbitrarily small $r > 0$ with $\gamma^{-1}(B(O,r))$ an **interval**
> — equivalently, must $J \cap B(O,r)$ be a *single* crosscut for some arbitrarily small $r$?

$(Q') \Rightarrow (Q)$ is that lane's Theorem C, which I do **not** import: every step it uses is
`sketch` by an agent of my own family, and [`../../../../RULES.md`](../../../../RULES.md) §3
forbids building on that, my own included. I re-derive what I need or I do not use it.

**Three admissible landings**, fixed now so I cannot grade my own exam later:

- **(A)** prove (Q) for an explicitly characterised full-$\mathcal{H}^1$-measure set of $O$;
- **(B)** construct a rectifiable Jordan curve and a differentiability point $O$ that is
  exceptional — a documented refutation, a first-class result here
  ([`../../../../RULES.md`](../../../../RULES.md) §0);
- **(C)** the sharpest conditional statement, "the rectifiable case follows from X" with X
  precisely stated and honestly graded, plus a post-mortem of each failed attempt.

## Success criterion

(A), (B) or (C), each with a [`../../RULES.md`](../../RULES.md) §1 regularity-budget line and the
§3.2 square test answered. **Padding (C) into a claimed (A) is the failure mode this file exists
to prevent.**

---

## §A. Kill-criteria that stop the lane outright

Stop, mark the relevant sub-attack `refuted`, and write up why.

- **A1 — the square test fires.** If the argument with $60°$ replaced by $90°$ would yield an
  inscribed **square** for rectifiable curves, it is wrong
  ([`../../RULES.md`](../../RULES.md) §3.2, [`../../../../RULES.md`](../../../../RULES.md) §7).
  *Test:* run the whole argument at a general angle $\alpha$ and name the exact step that stops
  being an equilateral triangle. If no such step exists, the argument is dead **and I must say so
  loudly**, not quietly weaken the claim.
- **A2 — the quantifier is wrong.** A $30°$–$30°$–$120°$ triangle boundary is rectifiable and has
  two exceptional points ([`../../RULES.md`](../../RULES.md) §3.1). Any statement I produce must be
  **consistent with that witness**. *Test:* check explicitly that the two $30°$ apexes fail my
  hypothesis. If my argument would cover them, it is wrong, full stop, no repair.
- **A3 — the hypothesis has no teeth.** If the local hypothesis I end up using is equivalent to,
  or no weaker than, "$O$ is a vertex", the lemma is a restatement. *Test:* exhibit a curve
  satisfying it whose conclusion is not visible by inspection.
- **A4 — smuggled regularity.** If any step needs the *image* $J$ to be locally a graph, locally
  connected in a strong sense, or of finite local crossing number, and I cannot derive that from
  "rectifiable + differentiable at $t_0$", the step is dead and the claim drops to (C) with X =
  that step. Differentiability of the **parametrisation at a point** does not make the **image** a
  graph near that point; treating it as if it does is exactly the error the neighbouring lane
  caught in itself.

## §B. Kill-criteria specific to the counterexample hunt (B)

- **B1 — the candidate is not differentiable at $O$.** The outward-cusp region
  $\{0 \le x \le 1,\ |y| \le x^2\}$ is the obvious candidate and it **fails this test**: its
  boundary's one-sided derivatives at the cusp are $-u$ and $+u$, which are unequal, so
  $\gamma$ is not differentiable there and the example is inadmissible. Any candidate must survive
  the same check *before* any topology is examined.
- **B2 — the candidate is not rectifiable, or not Jordan.** Infinitely many oscillations near $O$
  make both easy to lose. Check total length and injectivity numerically **and** by an exact
  argument.
- **B3 — the trapped interior cannot be realised.** If in every candidate the bounded complementary
  component $\Omega$ turns out to contain one of the two fat side-sectors at $O$, the third-component
  scenario is not merely unconstructed but obstructed, and (B) is dead — which is evidence for (A).

## §C. Kill-criteria specific to the proof attempt (A)

- **C1 — the local-pair route.** The brief suggests working with the rotation criterion directly:
  find $r$ and $\theta$ with $O + re^{i\theta} \in J$ and $O + re^{i(\theta + 60°)} \in J$ using
  the density of $J$ near $O$. *Kill if:* all of $J \cap B(O,\varepsilon)$ lies in a double cone of
  half-angle $< 30°$ about the tangent line, since then the angle subtended at $O$ by any two
  nearby points of $J$ is within $2\eta$ of $0°$ or of $180°$ and can never be $60°$. If that is
  what happens, **no small triangle exists at all** and every route through purely local pairs is
  dead, not merely unproven. I expect this to fire; I am writing it down so that expectation is on
  the record before I check.
- **C2 — the measure/counting bound is vacuous.** If a bound on the set of "bad" radii comes out
  weaker than the length of the interval of radii it lives in, it proves nothing and I must not
  dress it up as a density statement.
- **C3 — reproving a theorem.** [`../README.md`](../README.md) reports the sharp result (at most
  two exceptional points on **any** Jordan curve, Meyerson 1980) — provisionally, at low provenance.
  My target is strictly weaker (a.e. on rectifiable curves) and self-contained. If my argument
  appears to give the sharp statement, or to give anything for *arbitrary* Jordan curves, treat it
  as an error ([`../../../../RULES.md`](../../../../RULES.md) §7), not as progress.
- **C4 — status inflation.** Anything I prove is `sketch`. If I find myself writing a sentence that
  would let a later reader assume one of my own steps, that is C4 firing.

## Compute budget

[`../../../../RULES.md`](../../../../RULES.md) §6.6: one hour unattended. Expected use here is
minutes, not hours — the computations planned are (i) an exact rational check of a finite polygonal
model curve and (ii) a small numerical measurement of the good-radius density. Both are validated
against a known answer first ([`../../RULES.md`](../../RULES.md) §5). No search is planned; if one
becomes necessary the lane reports partial results rather than extending the budget.

**Arithmetic policy.** Exact rationals implemented by hand (`fractions.Fraction`, integer
cross-products). A caution inherited from this problem's other lanes: `sympy`'s exact geometry
predicates returned wrong answers on 3 of 176 boundary cases in this very problem
(`Segment2D.intersection` witnesses off by $\sim 10^{-16}$). No decision in this lane is delegated
to a library predicate, and any checker disagreement is treated as my bug until proven otherwise.
