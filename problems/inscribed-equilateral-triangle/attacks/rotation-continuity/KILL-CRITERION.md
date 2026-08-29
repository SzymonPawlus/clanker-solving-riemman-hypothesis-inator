# Kill-criterion — the 60° rotation route for general Jordan curves

Author `claude` (Claude Opus 5), 2026-08-29, issue #132, branch
`claude/inscribe-equilateral-triangle-oj15x1`.

## Provenance warning — this was not written first

Repo [`../../../../RULES.md`](../../../../RULES.md) §6.2 wants a kill-criterion written **before**
the work. This one was not, and pretending otherwise would defeat the point of the rule. The
sequence was: elementary observation checked, exact $30$–$30$–$120$ computation run, then this file,
then the general-case analysis in [`README.md`](./README.md) §6–§8.

The consequence, stated plainly: **§A below is retrospective and carries no predictive credit** — it
records a kill that had already happened, so it is documentation, not a bet. **§B and §C are
genuine forward criteria**, written before any work on the general case and before the §6.4 gap was
found, and they are the ones a reader should hold this lane to.

---

## What is being attacked

For a Jordan curve $J$ and $O \in J$, let $\rho_O = \rho_{O,60°}$. [`README.md`](./README.md) §2:
$O$ is a vertex of an inscribed equilateral triangle **iff** $J \cap \rho_O(J) \supsetneq \{O\}$.
The attack is the programme of exploiting that equivalence:

- **(P1)** the naive form — argue that $J \cap \rho_O(J) \supsetneq \{O\}$ for an arbitrary $O$;
- **(P2)** the corrected form — find the right local hypothesis at $O$ and prove it forces the
  second intersection;
- **(P3)** the general form — vary $O$ over $J$ and produce a good $O$ for **every** Jordan curve,
  with no regularity.

## Success criterion

An honest, cross-examinable write-up of (P2) with an explicit regularity budget, plus a precisely
located obstruction for (P3). **Not** a proof of (P3): the problem's central question is already a
1980 theorem ([`../README.md`](../README.md)), so a fresh general proof produced here is evidence of
an error or of duplication, never of progress — see [`../RULES.md`](../RULES.md) §0 and
[`../../../RULES.md`](../../../RULES.md) §7.

---

## §A. Retrospective kill of (P1) — **MET, and this is the lane's main deliverable**

> *"If some Jordan curve has a point $O$ with $J \cap \rho_O(J) = \{O\}$, then 'rotate at any point'
> is dead and must be written up as `refuted`."*

**Met, with an exact witness**: the boundary $T$ of the $30$–$30$–$120$ triangle
$(0,0),\,(1,0),\,(\tfrac12,\tfrac{\sqrt3}{6})$ has $T \cap \rho_{O,\pm60°}(T) = \{(0,0)\}$ exactly,
in $\mathbb{Q}(\sqrt3)$, at either $30°$ apex. Written up as [`README.md`](./README.md) §3. I did not
re-scope (P1) to survive; it is recorded `refuted` and closed.

---

## §B. Forward kill-criteria for (P2) — the local-hypothesis programme

Stop and mark (P2) `refuted` if **any** of these is observed.

- **B1 — the criterion has no teeth.** If the local hypothesis that makes the intersection
  unavoidable turns out to be equivalent to, or no weaker than, "$O$ is a vertex of an inscribed
  equilateral triangle" itself, the lemma is a restatement and proves nothing. *Test:* exhibit a
  curve satisfying the hypothesis where the conclusion was not already obvious by inspection.
  **Not met** — Lemma B's hypothesis (a $60°$ sector inside $\overline\Omega$) is strictly weaker,
  purely local, and checkable without knowing the answer.
- **B2 — the measure argument does not survive contact with the witness.** If the "equal areas
  force an overlap" route cannot rule out the configuration that §A's witness realises, then the
  measure framing is dead as a standalone route. **Met** — it rules out nesting only, and the
  witness is externally tangent ([`README.md`](./README.md) §7.1). Recorded `refuted` as a
  standalone route; kept as the reduction Corollary A′, which is all it is worth.
- **B3 — the square test fires.** If the argument, with $60°$ replaced by $90°$, would yield an
  inscribed **square**, the argument is wrong ([`../RULES.md`](../RULES.md) §3.2,
  [`../../../RULES.md`](../../../RULES.md) §7). **Not met**, and the reason is structural: at $90°$
  the construction returns three points forming a right-isosceles corner and leaves the fourth
  vertex unconstrained ([`README.md`](./README.md) §9).

## §C. Forward kill-criteria for (P3) — the general Jordan curve

Stop, and report the obstruction rather than the theorem, if **any** of these is observed.

- **C1 — no uniform noncollapse.** If no lower bound $\delta > 0$, independent of the approximating
  sequence, can be put on the side of the triangles produced, the limiting argument is the failed
  square argument in a new hat and must not be written up as a proof
  ([`../RULES.md`](../RULES.md) §2, §4.3). **Met, and this is where the lane stops.** The side
  produced by Lemma B is half the sector radius, and nothing bounds that below along a
  sequence of roughening approximants ([`README.md`](./README.md) §8).
- **C2 — the local certificate fails at a fixed point.** If the fat-sector hypothesis cannot even be
  certified at a *single* point of a curve in the intended class, then varying $O$ is the wrong
  place to be looking and the lane's remaining question is local geometry, not continuity.
  **Met, unexpectedly**, at the rectifiable class: [`README.md`](./README.md) §6.4. This one fired
  after C1 was already written and it is the more informative of the two, because it says the
  bottleneck is *not* the continuity-in-$O$ story the lane was named after.
- **C3 — reproving a theorem.** If the argument appears to establish the general result, treat it as
  wrong or as duplication, not as progress; the general result is Meyerson (1980). **Not met** — no
  general argument was produced.
- **C4 — the classical proof is this one.** If the literature shows the $60°$ rotation *is* the
  known route, the lane's remaining value is exposition and formalisation, not attack.
  **Provisionally met at provenance P3 only** ([`README.md`](./README.md) §10): search summaries
  describe Meyerson's proof as rotating by $60°$ about points of a *triod*, in three stages
  (polygonal, end-straight, general-by-approximation). No source text was readable in this session,
  so this is a flagged search target, not a citation, and C4 should be re-evaluated by anyone with
  network access.

---

## Verdict

**Abandon the lane as an attack.** (P1) is `refuted` with an exact witness; (P2) is done, with an
honest budget, for $C^1$ and polygonal curves; (P3) is killed by C1 and C2 and, if C4 confirms, was
never open in the first place.

What survives is not attack work and should be re-issued as such:

1. **Lean formalisation of Observation R** — a statement about three points and a rotation, with no
   topology in it, and explicitly listed as target 4 in [`../RULES.md`](../RULES.md) §7. This lane's
   §2 is the proof, and its §11 script is the numeric sanity check.
2. **Confirm C4** against Meyerson (1980) — cheap, and it is already item 1 of
   [`../README.md`](../README.md)'s verification debt.
3. **The local question isolated by C2/§6.4** — must $\overline\Omega$ contain a sector of positive
   aperture at some point of $J$? — as its own issue. It has no rotation in it, it is not a peg
   problem, and I do not know whether it is open or classical.

Reopen this lane only if item 3 is answered affirmatively **with a quantitative aperture and radius**
— which is exactly what C1 asks for, and would revive (P3).
