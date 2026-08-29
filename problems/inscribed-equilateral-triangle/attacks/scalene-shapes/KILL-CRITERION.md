# Kill-criterion — the scalene "all but two" lane

**Written before any computation in this lane**, per [`../../RULES.md`](../../RULES.md) §6.2 and
[`../../../../RULES.md`](../../../../RULES.md) §6.2. Provenance qualification, stated honestly and
in the same form the spiral lane used: the *derivations* of §1–§3 of
[`README.md`](./README.md) (the spiral-similarity criterion, the sharp half-density constant, the
Lemma-A dichotomy, the convex theorem) were done by hand on paper *before* this file was written —
they involve no computation and no code. What this file precedes is **every line of code and every
numerical decision in the lane**, which is what §6.2 is about, and it also fixes in advance what
would make me withdraw the hand derivations. Nothing below was written after seeing a result.

Author: `claude` (Claude Opus 5), 2026-08-29, branch `claude/inscribe-equilateral-triangle-oj15x1`.

---

## What the lane is trying to do

For a triangle shape `T` and a Jordan curve `J`, `O ∈ J` is **`T`-exceptional** if no triangle
inscribed in `J` and similar to `T` has a vertex at `O`; `E_T(J)` is the set of these. The
equilateral case has `|E(J)| ≤ 2` (Meyerson, `cited`\* and provisional). The lane asks whether
`|E_T(J)| ≤ 2` survives for scalene `T`, and looks for a curve with `|E_T(J)| ≥ 3`.

**A found `|E_T(J)| ≥ 3` contradicts nothing citable** — the bound of two is claimed here only for
equilateral shapes and for Schwartz's `G(J)` — so unlike the spiral lane's K6 this is not an
automatic self-suspicion trigger. It is still an extraordinary-shaped claim and K4 below governs it.

---

## The criteria

### K1 — the criterion is wrong (halts the lane)

The lane rests on: *`O` is a vertex of an inscribed triangle similar to `T` in the corner role with
multiplier `μ` iff `J ∩ σ(J) ⊋ {O}`, where `σ(z) = O + μ(z − O)`.* This must reproduce the
committed equilateral decider under `μ = e^{i60°}`.

**Fires if:** my decider, specialised to `μ = e^{i60°}`, disagrees with
`experiments/inscribed-triangle-polygons/` on **any** fixture of its battery.

**Then:** stop, adjudicate by hand on the disagreeing fixture, and publish the adjudication whichever
way it goes. Per the brief, four checkers have failed in this session against zero mathematical
errors of that kind, so the prior is that *my code* is wrong; but a hand adjudication decides it, not
the prior. No result of this lane is reported while K1 is open.

### K2 — the convex theorem is false

Claimed: for a convex `J` and any triangle `T` with angles `φ₁ ≤ φ₂ ≤ φ₃`, `O ∈ J` is `T`-good iff
`φ₁ < γ(O)`, or `φ₁ = γ(O)` with both extreme rays of the tangent cone meeting `J` in a segment;
hence `|E_T(J)| ≤ 2`.

**Fires if:** an exact convex fixture gives a vertex with `γ(O) > φ₁` that my decider calls
exceptional, or `γ(O) < φ₁` that it calls good.

**Then:** hand-adjudicate the single fixture. If the theorem is wrong it is marked `refuted` in
`README.md` with the witness, and the lane's headline shrinks to the criterion plus the numerics.
Re-scoping the theorem to survive its own falsification is forbidden (`RULES.md` §6.3); a *weaker
correct* statement may be recorded only under an explicit "the original claim was refuted" heading.

### K3 — the spiral-similarity corollary disagrees with the spiral lane

`attacks/spiral-tip-witness/README.md` §10 hands I3 the statement that for `J_{c,β}` the corner role
`(α, λ)` is realised at the tip iff `|α + (ln λ)/c| ≤ β (mod 360°)`, and flags it as the least-checked
line in that file. I derive it independently.

**Fires if:** my independent derivation disagrees with theirs.

**Then:** report the disagreement prominently, mark **both** statements unusable in this file, and do
not pick a winner unless I can adjudicate exactly. (Their file is `sketch` and therefore was never
assumable anyway; what a disagreement kills is my *use* of the tip as a probe, not their file.)

### K4 — an apparent `|E_T(J)| ≥ 3` (the reporting gate, not a kill)

If the search reports three or more `T`-exceptional points on one curve for a scalene `T`, **none of
it is reported** until all of the following pass, in this order:

1. **`J` is exactly simple.** An exact `is_simple` check: no zero-length edge, adjacent edges meeting
   only at their shared vertex, non-adjacent edges disjoint. A self-intersecting "polygon" is not a
   Jordan curve and would manufacture this result for free.
2. **`T` is nondegenerate and genuinely scalene.** Exactly: the three side-lengths-squared pairwise
   distinct, and the three points not collinear.
3. **All six corner roles blocked at each of the ≥ 3 points**, recomputed exactly, each role's
   verdict recorded separately. A missing role is the cheapest way to fake this.
4. **A hand check.** At least one blocked role at one of the points is verified by a hand
   computation written out in `README.md`, independent of the code.
5. **Perturbation sanity.** The verdict is stable under an exact rational perturbation of `T` (a
   nearby `w`), or, if it is not, the knife-edge is explained. A verdict that exists only at one
   exact value of `w` is an arithmetic coincidence until shown otherwise.

**Then:** it is reported as `numerical` — "for this exact curve and this exact shape" — never as a
general claim about scalene shapes, and `README.md` says in the same paragraph that it contradicts
no `cited`\* row.

### K5 — the half-density analogue is not what I claim

Claimed: for `σ` a spiral similarity with `|μ| = k < 1`,
`sup{ λ(V ∩ B(O,R)) / λ(B(O,R)) : V ∩ σ(V) = ∅ } = 1/(1+k²)`, attained.

**Fires if:** an explicit measurable `V` beats `1/(1+k²)`, or I cannot close the upper bound.

**Then:** the section is rewritten as "no analogue found beyond the trivial bound", and the sharp
constant is withdrawn. It is a self-contained sub-question and a partial answer is an honest answer;
what is not permitted is leaving a constant in the file that I could not prove.

### K6 — a float decides anything

Every existence/exceptionality decision is exact (`RULES.md` §5). Floats are permitted for search
heuristics, pictures, and printing only.

**Fires if:** any reported verdict traces back to a floating-point comparison, or to a `sympy`
geometry predicate (which is banned outright in this lane — it was wrong on 3 of 176 boundary cases
in this very problem).

**Then:** the affected verdict is void and is deleted, not caveated.

### K7 — compute budget

**Fires if:** the search passes 20 minutes of wall clock without having produced either a
`|E_T| ≥ 3` candidate or a structured negative census.

**Then:** stop, report the partial census with the seeds and the exact command, and say what was not
covered. (`RULES.md` §6.6 allows an hour; 20 minutes is my own tighter budget because the search
space is unbounded and a bigger sample of the same family teaches nothing new.)

### K8 — the three-tip construction

The ideation entry I3 proposes three spiral tips of suitable pitches on one curve.

**Fires if:** the global arrangement is not closed in the time available.

**Then:** it is reported as *not done*, with the specific obstruction, and **no partial construction
is written up as a result**. "Three tips would work if they could be arranged" is not a finding.

### K9 — over-reading the literature gap

**Fires if:** I find myself writing that the scalene question *is* open.

**Then:** rewrite. No scholarly host is reachable from this environment; per
[`../../RULES.md`](../../RULES.md) §6.1, "not found" is not "open", and the tension between the
single snippet ("not known for any other shape") and Schwartz's `G(J)` is something this lane can
*describe* and cannot *settle*.

---

## Outcomes

Recorded in [`README.md`](./README.md) §11 after the work, one row per criterion, with the honest
verdict including "not met" and "unresolved".
