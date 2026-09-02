# Kill-criterion — `extremal-gap-closure`

**Written before any computation in this lane** ([`../../../../RULES.md`](../../../../RULES.md)
§6.2). Nothing in this directory was computed, and no script was run, before this file was
committed to the working tree. The only work preceding it was reading
[`../../RULES.md`](../../RULES.md), [`../extremal-size/README.md`](../extremal-size/README.md),
[`../round3-cross-review/README.md`](../round3-cross-review/README.md), and pencil derivation.

## What this lane is trying to do

Close, or break, the two steps that
[`../extremal-size/README.md`](../extremal-size/README.md) §6 self-flagged and that the round-3
cross-examiner could not settle, in the proof of

> **Theorem C.** Every planar convex body $K$ with inradius $r$ inscribes an equilateral triangle
> of side $\ge \sqrt3\,r$.

- **Gap 1 — "Step 0".** The reduction to strictly convex bodies via $K_n=K+\tfrac1nD$, and the
  claim that the limit of the inscribed triangles has its vertices on $\partial K$.
- **Gap 2 — endpoint continuity.** The IVT on $g(\theta)=R(\theta+60°)-R(\theta)$ over the closed
  cone $[-90°,30°]$, at the two closed endpoints where the ray is tangent to the incircle and the
  estimate $R(\theta)\ge 2r\cos\theta$ degenerates.

## Kill conditions — any one of these and the corresponding sub-attack stops

**K1 (whole lane).** If a **convex body with inradius $r$ and $m(K)<\sqrt3\,r$** is exhibited with
exact arithmetic, Theorem C is `refuted`, this lane stops immediately, and the write-up is the
counterexample. *(I expect this not to happen; the disk equality case and §3.3 polygon checks make
the statement look true. But the concurrent refutation lane exists precisely because that
expectation is not evidence.)*

**K2 (Gap 1).** If the strictly-convex reduction cannot be repaired **and** a convex body is
exhibited at which the Step-1/2/3 machinery genuinely fails (empty zero set, or the IVT hypothesis
false) **and** no replacement route is found, then Step 0 is recorded as an unrepaired hole,
Theorem C stays `sketch`, and the lane reports a *located* failure rather than a fix. Repairing
Step 0 with a *different* approximating family counts as closing it only if the family is
(a) genuinely strictly convex, (b) contains $K$ or otherwise supports the "limit lands on
$\partial K$" step, and (c) has $r(K_n)\ge r(K)$.

**K3 (Gap 2, sub-interval route).** If the IVT can be run on a closed sub-interval
$[-90°+\varepsilon,\,30°-\varepsilon]$ on which $R$ is continuous by the *interior* argument
alone, the endpoint question is moot and that route is taken. **If, on trying it, the sub-interval
turns out to need the same fact as the endpoint (that $R$ is small near the tangent directions),
say so plainly rather than presenting the reformulation as if it had removed a hypothesis.** A
"fix" that only moves the difficulty is a kill for the *fix*, not for the gap.

**K4 (replacement proof).** The search for a proof avoiding both gaps is capped at the equivalent
of ten minutes of thought plus one written-out attempt. If the containment/monotonicity route and
one alternative parametrisation both fail, stop looking and patch instead. Specifically: if
"$D(O,r)\subseteq K$ therefore the disk's inscribed triangle is inscribed in $K$" is confirmed to
fail for the obvious reason (inscribed is a boundary condition, containment is not), that route is
`refuted` and not revisited.

**K5 (budget).** One hour of unattended compute (`../../../../RULES.md` §6.6). No long search is
planned in this lane; anything beyond exact evaluation of explicit closed forms on an explicit
body is out of scope and must be reported rather than started.

**K6 (scope).** This lane owns exactly three files. If closing a gap appears to require editing
`../extremal-size/`, that is a **correction request recorded in this lane's README**, not an edit.
If the gap turns out to be in something outside Theorem C (e.g. Lemma B), record it and stop —
do not widen.

## What would count as success, in decreasing order

1. Both gaps closed, with a self-contained corrected proof re-derived here (not read off the
   other lane, which is `sketch` and therefore not assumable, `../../../../RULES.md` §3).
2. One closed, the other reduced to a single precisely stated missing lemma.
3. A documented, exactly-checked demonstration that a step **fails**, with the smallest witness
   found. Per `../../../../RULES.md` §0 this is a success and is reported as one.

## Anti-goals, stated in advance

- No `verified:review` is self-granted here. Everything this lane produces is `sketch` or
  `numerical`.
- No claim about the *general Jordan* case (`../extremal-size/` §5 Conjecture I) is in scope.
  Convexity is load-bearing throughout and is declared in the README's budget line.
- No dependence on `experiments/inscribed-triangle-maximiser/` (unvalidated, mid-write) and none
  on the concurrent `extremal-refutation-hunt` lane, whose files are deliberately unread.
- Exact arithmetic decides everything. No `sympy` geometry predicate. If a float appears, it is
  labelled as illustration and no decision rests on it.
