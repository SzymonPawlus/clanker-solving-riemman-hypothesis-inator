# Kill-criterion — `exceptional-set-polygons`

**Written before any computation in this lane** (`../../RULES.md` §6.2, repo `RULES.md` §6.2).
At the moment of writing, this lane has run **no** script, imported **no** module from
`experiments/`, and produced **no** number. What *had* already happened, and it would be
dishonest to pretend otherwise: the five briefed attack READMEs and the problem rules had been
read, and the candidate witness of §K3 below had been **designed by hand on paper** — its radii,
its rotation matrix and the reason it should work were fixed before this file was written. So
this file pre-registers the *verdicts*, not the *idea*. That is the same qualification the
`half-density-obstruction` and `spiral-tip-witness` lanes made, and it is made here for the same
reason: a kill-criterion written after the answer is known is decoration.

Lane target: **prove $|E(P)| \le 2$ for every simple polygon $P$, or find what actually happens.**

---

## K1 — criterion sanity (fires: abandon everything downstream)

The whole lane rests on one three-line equivalence, re-derived from scratch:

> $O$ is a vertex of a nondegenerate inscribed equilateral triangle $\iff$ there are $r>0$ and
> $\theta$ with $O + re^{i\theta} \in J$ **and** $O + re^{i(\theta+60°)} \in J$.

**Kill if:** my re-derivation disagrees with the committed exact decider
(`experiments/inscribed-triangle-polygons/`, read-only) on any of the three controls — the
equilateral triangle (all three vertices good), the $30$–$30$–$120$ triangle (both $30°$ apexes
exceptional, the $120°$ vertex good), the unit square (all four corners good).
**Verdict rule:** any disagreement ⇒ my criterion is wrong ⇒ stop, and report the criterion as
the finding. It is not permitted to "fix" the criterion after seeing which way the disagreement
went.

## K2 — the reduction $E(P) \subseteq \mathrm{vertices}(P)$

**Kill if:** an exceptional **non-vertex** boundary point of a simple polygon is exhibited
(exactly, not numerically). Then the reduction is false and *that* is this lane's result; the
count question is not re-scoped to survive it.

**Also kill if** the reduction can only be proved by importing a `sketch` from another lane. The
reduction must be re-derived here, from the definitions, or it does not count
(`RULES.md` §3). If the re-derivation needs the Jordan curve theorem, that must be stated as a
dependency in the regularity budget, not smuggled.

## K3 — the "exceptional ⟹ wedge-type" sub-question

Sub-question, pre-registered as the cleanest available result: *is every exceptional point of a
simple polygon wedge-type* (i.e. is the whole polygon contained in a closed cone of opening
$<60°$ at that point)?

The candidate witness is a **polygonal spiral channel**: a simple polygon whose interior is a
channel of constant angular width $w<60°$ about a tip $O$, wound through more than $60°$ of
total turning, so that the directions from $O$ to points of $J$ fill an arc far wider than $60°$
while every circle centred at $O$ still meets the polygon in an arc of width $w$.

**Kill the witness if any one of these holds:**

- **K3a** the polygon is **not simple** (exact `is_simple` test), or
- **K3b** the committed exact decider reports $O$ **good**, or
- **K3c** the polygon does after all lie in a closed cone of opening $<60°$ at $O$, i.e. the
  witness is wedge-type and proves nothing, or
- **K3d** the hand proof that $\overline{\Omega}$ meets every circle about $O$ in an arc of
  width $\le w$ has a gap I cannot close, **even if the decider agrees** — a decider agreeing
  with an unproved claim is `numerical` evidence, not a proof, and this lane may not promote it.

If K3 fires the honest report is "every exceptional point of a polygon may well be wedge-type;
here is the construction that failed and why", and the wedge-type route to the count stays open.

## K4 — the count $|E(P)| \le 2$

**Kill the *proof attempt* if** the argument at any point requires one of:

- treating a `sketch` (mine or another lane's, including Theorem T, Lemma A, Lemma B,
  Observation R, Proposition R) as an assumable premise;
- the convex-case angle-sum count applied to points that are **not** shown to be wedge-type —
  that count consumes "the whole body lies in the tangent cone at $O$", which is exactly what a
  non-convex polygon does not supply;
- Meyerson's bound in any form, including as a "consistency check" that steers a step.

**And:** if the budget (§K6) runs out with the count unproved, the lane reports the count as
**not closed** and names the step where it dies. Re-scoping the lane so that it "succeeds" is
forbidden by `RULES.md` §6.3.

## K5 — three exceptional points (the dangerous outcome)

If a construction or search appears to produce a simple polygon with **three or more** exceptional
points, that contradicts the (provisional) Meyerson bound and repo `RULES.md` §7 applies in full:

1. do **not** announce it; write "this appears to show";
2. re-check with a second, independently written exact decider, and by hand at the pairwise
   distances involved;
3. name the step least trusted, in this order of prior likelihood: (i) an error in my argument,
   (ii) a misreading of the criterion, (iii) a wrong provisional citation;
4. flag for both humans rather than promoting anything.

Note the asymmetry: finding three is *evidence I made a mistake* until it survives (2).

## K6 — budget

One hour of unattended compute (repo `RULES.md` §6.6). No search is launched before the code has
reproduced the three controls of K1. Any enumeration checkpoints to disk. If a search is still
running at the budget, it is killed and the partial result reported.

## K7 — exactness

Every decision is made in exact $\mathbb{Q}$ or $\mathbb{Q}(\sqrt3)$ arithmetic
(`../../RULES.md` §5). **No `sympy` geometry predicate decides anything** — it was wrong on 3 of
176 boundary cases in this very problem. Floats are for display only. If any reported decision
turns out to have gone through a float comparison, that decision is void.

---

## Outcomes (filled in after the work — see `README.md` §11 for the narrative)

| # | Fired? | What happened |
|---|---|---|
| K1 | **no** | The re-derived criterion agrees with the committed exact decider on all three controls (equilateral: 3/3 good; $30$–$30$–$120$: both apexes exceptional, $120°$ vertex good; unit square: 4/4 good). Run **before** anything else in the lane. |
| K2 | **no** | The reduction is proved, and sharpened: $E(P) \subseteq \{$vertices of interior angle $<60°\}$ (README §5). Re-derived from the definitions; the Jordan curve theorem is declared as a dependency, not smuggled. Polygon control: 4 043 vertices of angle $\ge 60°$ and 16 749 non-vertex boundary points, 0 violations. |
| K3 | **no** | The witness survives all four sub-criteria. K3a: simple, by hand and by the exact `is_simple`. K3b: the committed decider reports $O$ **not** good, and an independently written second decider agrees. K3c: the directions from $O$ span $258°$, so no cone of opening $<60°$ contains $J$ — exhibited exactly by the pair $a_1, a_3$ with $s^2-3c^2>0$. K3d: the arc-width proof closed, and closed *without any topology* — the criterion is a statement about $J$ as a point set, so $J \subseteq$ channel suffices and $\overline\Omega \subseteq$ channel is not needed. |
| K4 | **fired, by the budget clause** | $\lvert E(P)\rvert \le 2$ is **not closed** and is not re-scoped. README §8 names the step where it dies: the angle-sum count needs $\angle O_jO_iO_k<60°$, free for a wedge-type point and false for a non-wedge one, and the criterion at $O_i$ constrains each circle separately while $O_j, O_k$ sit on different circles. No forbidden ingredient was used: no `sketch` was treated as a premise, the convex count was applied only to points *proved* wedge-type (Theorem 2), and Meyerson was not used as an input. |
| K5 | **no** | 6 026 simple polygons scanned for exceptional counts (3 218 star-shaped random with rational squashing; 2 808 thin multi-armed with 3–5 sharp tips), plus a separate 746-polygon battery used for the reduction control. Maximum number of exceptional vertices: **2**, never 3. Nothing needed escalation under repo `RULES.md` §7. |
| K6 | **no** | About six minutes of computation in total; longest single run 100 s; both hunts seeded, deterministic and checkpointed. |
| K7 | **no** | Every decision exact, in $\mathbb{Q}$ or $\mathbb{Q}(\sqrt3)$. `sympy` was not imported anywhere in this lane. Floats appear only in printed angle columns. |
