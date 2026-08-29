# Kill-criterion — the spiral-tip exceptional point (idea I2)

Author `claude` (Claude Opus 5), 2026-08-29, branch
`claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.

## Provenance — written before any computation, and what "before" means here

Repo [`../../../../RULES.md`](../../../../RULES.md) §6.2 requires the kill-criterion **before**
the work. **This file was written before a single line of code was run in this lane**, and before
[`README.md`](./README.md) existed. That is the honest and useful sense of "before": every
criterion below is a forward bet against machine evidence that did not yet exist.

It is *not* true that this file precedes all thought. The lane brief already contains a
construction sketch (a log-spiral arm closed into a Jordan curve), and I spent the reading pass
working out on paper what the closing arc would have to look like. So the criteria below are the
bets of someone who already believes the construction is likely to close — and a reader should
discount K1 and K2 accordingly, while K3–K7 remain genuine, because they are the ways a
construction that "obviously works" on paper actually dies.

Recording this distinction rather than smoothing it over is the point of the rule
([`../../../../RULES.md`](../../../../RULES.md) §0).

---

## What is being attacked

**Claim under construction (call it W).** *There is a Jordan curve $J$ and a point $O \in J$ such
that (a) $O$ is exceptional — no equilateral triangle inscribed in $J$ has $O$ as a vertex — and
(b) the set of directions from $O$ achieved by $J$ inside every ball $B(O,\varepsilon)$ is all of
$S^1$, so the wedge obstruction ([`../../RULES.md`](../../RULES.md) §3.1) does not apply at $O$;
and ideally (c) $J$ is rectifiable.*

Why it is worth doing: every exceptional point this repo can currently exhibit is wedge-type
(the $30$–$30$–$120$ triangle, [`../rotation-continuity/README.md`](../rotation-continuity/README.md)
§3, and [`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md) Thm A).
If W holds, the wedge obstruction is **not** the whole story of the exceptional set. If W fails
for a *reason*, that reason is evidence that it **is**, which is equally worth writing down.

**Success criterion.** Either (i) an explicit $J$, an explicit $O$, and a proof of exceptionality
that a cross-examiner can check line by line without trusting any computation of mine, with a
regularity budget; or (ii) a documented refutation naming the exact pairing that cannot be made
disjoint. Both are first-class outcomes ([`../../../README.md`](../../../README.md)); neither is
promotable past `sketch` by me.

**What is *not* a success:** anything that reads as progress on the general theorem. The planar
equilateral question is settled ([`../README.md`](../README.md)); this lane produces a *witness*,
not a theorem about all curves.

---

## Kill-criteria — stop, mark `refuted`, and write up why

Abandon the construction if **any** of K1–K7 is observed. "Abandon" means: write the refutation,
do not re-scope the construction to survive its own falsification
([`../../../../RULES.md`](../../../../RULES.md) §6.3).

### K1 — the criterion itself is wrong

The whole lane rests on: *$O$ is a vertex of an inscribed equilateral triangle iff there are
$r > 0$ and $\theta$ with $O + re^{i\theta} \in J$ and $O + re^{i(\theta + 60°)} \in J$.* I must
re-derive this from scratch before using it, **not** import it from
[`../rotation-continuity/README.md`](../rotation-continuity/README.md) §2 or
[`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md) Prop. R, both of
which are `sketch` and therefore unassumable including by me
([`../../../../RULES.md`](../../../../RULES.md) §3).

**Kill:** if my own derivation fails, or produces a *different* statement from the two lanes above,
everything stops until the discrepancy is resolved. A three-line argument that three sources state
three different ways is a warning, not a convenience.

### K2 — arm-versus-arm is not actually clean

**Kill:** if the spiral arm alone contains two points at the same distance from $O$ subtending
exactly $60°$. (Expected not to happen — strict radial monotonicity should make it immediate —
but if the strictness is only *weak* monotonicity anywhere along the arm, the construction is
dead at the first step.)

### K3 — global disjointness cannot be closed *(the one that matters)*

The arm has to close up, and the closing arc is part of $J$. **Kill:** if I cannot rule out, by
an argument I can write down in full, *every* pair $(P,Q)$ of points of $J$ with $|OP| = |OQ|$
and $\angle POQ = 60°$ — arm vs arm, arm vs closing arc, and closing arc vs itself. Specifically:

- **K3a** if the closing arc is forced to meet a radius already used by the arm at a $60°$ offset,
  and re-truncating/re-routing the closing arc merely moves the collision rather than removing it;
- **K3b** if I find myself arguing "the closing arc can be chosen far away" without exhibiting the
  choice and checking it — this lane's ideation entry flagged global disjointness as **unproved**,
  and hand-waving it is precisely the failure the lane exists to avoid;
- **K3c** if the closing arc cannot reach $O$ at all without crossing the arm. Note this is a real
  possibility, not a formality: the arm accumulates on $O$, so the closing arc must approach $O$
  through whatever is left of a neighbourhood of $O$, and if that complement is disconnected in
  the wrong way the construction is dead. **This is the criterion I most expect to bite.**

A serious attempt that fails for a stateable reason counts as a kill and is written up as one.

### K4 — it is not a Jordan curve

**Kill:** if the closed curve self-intersects. A spiral is exactly where embeddedness hides.
Required evidence before any claim: (i) an exact injectivity argument for the true curve, and
(ii) an independent brute-force all-pairs non-adjacent segment-intersection check on a
discretisation. If (i) and (ii) disagree, (i) is not automatically right — I stop and find out
which is wrong. **Sympy geometry predicates are banned here**: `Segment2D.intersection` was
wrong on 3 of 176 boundary cases in this very problem today, with witnesses off the segments by
$\sim 10^{-16}$. Predicates get reimplemented from sign tests.

### K5 — a float decides something

**Kill (of the claim, not necessarily the lane):** if the exceptionality of $O$ ends up resting on
any floating-point comparison. A logarithmic spiral is transcendental, so I must say for each step
whether it is exact algebra, interval arithmetic, or float, and the *decision* steps must be
exact. Floats are for search, pictures, and cross-checks only ([`../RULES.md`](../RULES.md) §5).
If the argument cannot be made exact, the claim is downgraded to `numerical` and stated as such.

### K6 — three or more exceptional points appear

Meyerson's theorem ([`../README.md`](../README.md) row 2, `cited` but provisional, P2, no source
text read) says $|E(J)| \le 2$. **Kill / freeze:** if the construction appears to give $J$ three or
more exceptional points, I do **not** announce a counterexample to the literature. Per
[`../../../../RULES.md`](../../../../RULES.md) §7 the likeliest explanations, in order, are:
(1) an error in my construction, (2) a misreading of the criterion, (3) a wrong provisional
citation. I write "this appears to show", check it to destruction, and flag it. The same applies
if the construction seems to prove anything about **squares** ([`../RULES.md`](../RULES.md) §3.2).

### K7 — it is already someone else's example

**Kill (rescope, not refute):** if a reachable source shows the spiral tip is Meyerson's or
Schwartz's own second mechanism. The lane then becomes reconstruction and citation, not
construction. Note the network restriction recorded in [`../README.md`](../README.md) makes this
unlikely to be *settled* here; "not found" is not evidence of novelty
([`../RULES.md`](../RULES.md) §6.1), and the write-up must say so.

---

## What does **not** count as a kill

- **The witness is not rectifiable.** That weakens the result (it would no longer bear on the
  rectifiable lane) but a non-rectifiable non-wedge exceptional point is still new information
  here. Rectifiability is a *bonus target*, not a requirement, and must be computed rather than
  assumed — the arm's length is an integral, not a picture.
- **The mechanism turns out to be a known folklore example.** Recording it precisely, in-repo and
  checkable, still has value; the status just cannot be `cited` without a source.
- **The construction only produces one exceptional point.** One non-wedge exceptional point is the
  entire claim. Getting three is K6, i.e. a red flag, not a better result.
- **The polygon enumerator has nothing to say.** A spiral tip is not a polygon feature, and
  ([`../RULES.md`](../RULES.md) §3.3) agreement with polygons would be weak evidence anyway. If
  the §3.3 control is inapplicable I say so explicitly rather than faking a check.

---

## Budget

One hour of unattended compute ([`../../../../RULES.md`](../../../../RULES.md) §6.6). The
computations foreseen are all small: a discretisation of a curve with a few thousand vertices, an
$O(n^2)$ segment-intersection check on it, and a scan for a second intersection of $J$ with its
rotate. None should exceed a minute. If anything looks like it will, that is a sign I am computing
the wrong thing, and I stop and re-derive instead.
