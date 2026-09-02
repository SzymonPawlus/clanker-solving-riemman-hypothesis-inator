# Kill-criterion — exceptional-pair rigidity (idea I5)

Author `claude` (Claude Opus 5), 2026-08-29, branch
`claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.

## Provenance — written before any computation in this lane

Repo [`../../../../RULES.md`](../../../../RULES.md) §6.2 requires the kill-criterion **before**
the work, and this problem's brief repeats the requirement. **No line of code had been run in
this lane when this file was written**, and [`README.md`](./README.md) did not yet exist.

What *had* happened before it: a reading pass over
[`../../RULES.md`](../../RULES.md), [`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md),
[`../ideation-round-1/README.md`](../ideation-round-1/README.md) §I5,
[`../spiral-tip-witness/README.md`](../spiral-tip-witness/README.md) §10, and the two experiment
READMEs — and, on paper, a re-derivation of the convex tangent-cone criterion and a first attempt
at the pair statement. So the criteria below are the bets of someone who already suspects the
convex answer is "the pair is the diameter". A reader should discount **K1** accordingly and
treat **K2–K7** as the genuine forward bets: they are the ways a statement that looks clean on
paper actually dies.

Recording that distinction rather than smoothing it over is the point of the rule
([`../../../../RULES.md`](../../../../RULES.md) §0).

---

## What is being attacked

**Question (I5).** $E(J)$ is the set of points of the Jordan curve $J$ that are a vertex of no
inscribed equilateral triangle. When $|E(J)| = 2$, what does that force about $J$ and about the
relationship between the two points? And can $|E(J)| = 1$?

**Claims under construction.**

- **R-convex.** For $K$ compact convex with nonempty interior and $J = \partial K$: if
  $E(J) = \{O_1, O_2\}$ then $|O_1O_2| = \operatorname{diam}(K)$, and $\{O_1,O_2\}$ is the only
  pair realising it.
- **R-single.** Every exceptional point of a convex $J$ is an endpoint of a diameter of $K$.
- **R-general.** Some version of R-convex survives for non-convex $J$ — or it does not, and the
  census says which.
- **Parity.** $|E(J)| = 1$ is or is not possible.

**What is *not* a success.** Anything that reads as progress on the existence theorem, which is
settled ([`../../README.md`](../../README.md)); anything that treats the provisional Meyerson
bound $|E| \le 2$ as a premise rather than as an after-the-fact consistency check; and any
promotion of my own `sketch` beyond `sketch`.

---

## Kill-criteria — stop, mark `refuted`, write up why

Abandon the corresponding claim if any of K1–K7 is observed. "Abandon" means write the refutation
and do **not** re-scope the claim to survive its own falsification
([`../../../../RULES.md`](../../../../RULES.md) §6.3).

### K1 — the convex pair statement is false

An exact convex witness (rational or $\mathbb{Q}(\sqrt3)$ coordinates) with two exceptional
boundary points $O_1, O_2$ and a pair $X,Y$ of boundary points with $|XY| > |O_1O_2|$ kills
R-convex outright. **Test:** exact census over convex polygons — compare $|O_1O_2|^2$ against
$\max_{i<j}|V_iV_j|^2$ in exact arithmetic, never in floating point.

### K2 — my re-derivation of the convex criterion disagrees with the existing lane

The pair statement needs "exceptional $\Rightarrow \alpha(O) \le 60°$", i.e. the contrapositive
of $\alpha > 60° \Rightarrow$ good. I must re-derive that myself
([`../../../../RULES.md`](../../../../RULES.md) §3: `../convex-vertex-criterion/` is `sketch` and
not assumable, including its Theorem B). If my re-derivation and the existing lane's disagree on
any exact convex fixture, I stop and adjudicate **by hand, exactly**. An unresolved disagreement
kills every claim downstream of it. If the disagreement turns out to be in *my* argument, that is
the outcome to report.

### K3 — no metric rigidity in the non-convex census (I5's own kill line)

If the exact polygon census turns up pairs with $|O_1O_2|/\operatorname{diam}$ scattered across
$(0,1]$ with no floor, then no metric rigidity exists for general Jordan curves and the lane's
output is the **negative census** — which is a success under
[`../../../../RULES.md`](../../../../RULES.md) §0, and must be written up as one rather than
weakened into "rigidity holds under extra hypotheses I chose after seeing the data".

### K4 — the parity question resolves trivially

If a single exact witness with $|E(J)| = 1$ appears, "$|E(J)| = 1$ is impossible" is dead on the
spot and no further effort goes into it. (I expect this to fire; a triangle with exactly one
angle below $60°$ is the obvious candidate and I will check it first.) The converse — no
$|E| = 1$ anywhere in the census — would be a reason to look for a parity argument, but absence
in a finite sample is never a proof and must not be written as one.

### K5 — three exceptional points appear

A polygon with three exceptional boundary points would contradict the provisional
`cited`\* row 2 of [`../../README.md`](../../README.md). Per
[`../../../../RULES.md`](../../../../RULES.md) §7 and this problem's
[`RULES.md`](../../RULES.md) §5, the response is: **suspect my own decider first**, re-decide the
fixture by a second route and by hand in exact arithmetic, and if it survives, report it as "this
appears to show", flag it, and do not announce it. Five checkers have failed in this session
against zero mathematical errors of this kind; the prior is overwhelmingly that the code is
wrong.

### K6 — the rigidity statement is already refuted by a curve in this repo

[`../spiral-tip-witness/README.md`](../spiral-tip-witness/README.md) §10 reports, as unasserted
`numerical` evidence, a curve whose exceptional set appears to be a **mixed** pair (a spiral tip
and a wedge corner). If the diameter statement fails on that curve, R-general is dead and must be
reported dead — not narrowed to "convex only" *after* the fact. (Narrowing is legitimate only if
the convex statement was stated as the convex statement from the start, which it is: R-convex
above carries the convexity hypothesis in its own name.)

### K7 — budget

One hour of unattended compute ([`../../../../RULES.md`](../../../../RULES.md) §6.6). Every stage
checkpoints to disk. If the census is not finished by then, the partial census is the reported
result and the shortfall is stated.

---

## What would count as the lane succeeding

1. A convex rigidity statement, proved from re-derived ingredients, with an honest regularity
   budget and the §3.2 square test answered.
2. An exact census that either supports or refutes the non-convex version, reported either way.
3. A definite answer on $|E(J)| = 1$, with an exact witness or an argument.
4. Everything at `sketch`/`numerical`, nothing promoted, and the Meyerson row used only as an
   after-the-fact consistency check.
