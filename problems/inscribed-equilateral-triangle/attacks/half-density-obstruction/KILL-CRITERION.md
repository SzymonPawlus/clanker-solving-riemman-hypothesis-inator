# Kill-criterion — the half-density obstruction (idea I1)

**Provenance, stated plainly.** This file was written **before any computation was run** in this
lane, as [`../../../../RULES.md`](../../../../RULES.md) §6.2 and the lane brief require, and before the
polygon witness of [`README.md`](./README.md) §6 existed. It was **not** written before the
*derivation*: by the time I wrote it I had already done the measure-theoretic core (§3 of the
README) and the Lemma A re-derivation (§4) on paper. So it is honest as a pre-registration of the
**computational** predictions in §5–§7 below, and it is *not* a pre-registration of the algebra.
I record the distinction because the rotation lane's kill-criterion file carries the same
qualification and the repo is better served by the two being comparable than by mine looking
stronger than it is.

Predictions §5–§7 were written down with their expected outcomes *before* the corresponding
script existed, so each is falsifiable in the only sense that matters here: an outcome table
disagreeing with them would have forced the verdicts in §8.

---

## 1. What the lane claims

Let `J` be a Jordan curve, `Ω` its bounded complementary component, `O ∈ J`, and `ρ` the rotation
by `60°` about `O`. `O` is **exceptional** if no inscribed equilateral triangle has a vertex at
`O`.

> **Speculative Lemma (half-density), as briefed.** `O` exceptional ⟹
> `λ(Ω ∩ B(O,R)) ≤ ½ λ(B(O,R))` for every `R > 0`.

> **Criterion (contrapositive).** If `Ω` fills more than half of a single ball centred at `O`,
> then `O` is a vertex of an inscribed equilateral triangle.

The lane also owns a **topology-free core**: `U ∩ ρ(U) = ∅` ⟹ `U` has density `≤ ½` in every
ball centred at `O`, with no topology in the statement at all.

## 2. Kill conditions — meeting any one of these ends the lane as briefed

- **K1 (core broken).** A gap in the core measure inequality, or in the passage from
  "`Ω ∩ ρΩ = ∅`" to a density bound, that I cannot repair. *Outcome if met:* the lane is
  `refuted`; write up where it broke.
- **K2 (Lemma A broken).** My independent re-derivation of "`J ∩ ρ(J) = {O}` ⟹ `Ω ∩ ρ(Ω) = ∅`"
  fails, or produces a different conclusion from the rotation lane's. *Outcome if met:* the whole
  chain is `refuted` **and** the rotation lane's §4 needs a correction notice on its own issue.
- **K3 (outright refutation).** An exact example of an exceptional point with interior density
  `> ½` in some ball. This refutes the lemma *and* Lemma A simultaneously. *Outcome if met:*
  `refuted`, loudly, and the polygon lane inherits a bug report.
- **K4 (pinwheel fails).** The "pinwheel" separation witness — a point where the density
  criterion fires and the sector criterion cannot — fails on exact computation. *Outcome if met:*
  the lemma may still be true, but it is demoted to "true and never adds coverage beyond the
  sector criterion", which is not worth a lane. Say so; that is a successful outcome, not a
  failed one.

## 3. What does **not** count as a kill

- The lemma turning out to be easy. A two-line proof of a true statement is a better outcome than
  a long proof, not a worse one.
- The constant coming out `½` rather than the stronger `1/6` the brief floats. `1/6` is a
  conjecture in the brief, not a requirement of the lane.
- The result being known to the literature. Per [`../../RULES.md`](../../RULES.md) §6.1 this
  directory's job includes second, self-contained, checkable proofs; no scholarly host is
  reachable from this session anyway.
- The criterion being *incomparable* to the sector criterion rather than *stronger*. That is a
  finding about I1's triage line, not a kill — as long as the pinwheel (K4) survives, the lane
  covers points the sector criterion cannot.

## 4. Compute budget

Well under the one hour of [`../../../../RULES.md`](../../../../RULES.md) §6, item 6. Everything here
is exact rational / `ℚ(√3)` arithmetic on polygons of at most a few hundred vertices, plus a
seeded random hunt sized so it finishes in a couple of minutes. Nothing is compute-bound and no
background job is started. Estimated total: **< 5 minutes** of wall clock.

---

## 5. Pre-registered prediction A — the pinwheel witness

I will build an explicit simple polygon `P` with rational vertices, `O` a vertex of `P`, such that

1. the interior angle of `P` at `O` is exactly-testably `< 60°` (so the sector criterion of the
   rotation lane's Lemma B is silent at `O`, at every radius);
2. `P ⊆ B̄(O,1)` with every vertex at exact rational distance `≤ 1` from `O`;
3. `area(P) > π/2` (so the density criterion fires at `R = 1`), decided by comparing an exact
   rational area against `π/2` using only `3.1415 < π < 3.1416`.

**Predicted outcome:** all three hold, and the repo's committed exact decider
`experiments/inscribed-triangle-polygons/` independently reports `O` **good**, with an exhibited
inscribed equilateral triangle whose three squared side lengths are exactly equal in `ℚ(√3)`.

**Falsifier:** the decider reports `O` **not good** while (3) holds. That is K3 and K2 together.

## 6. Pre-registered prediction B — direct test of Lemma A on exceptional points

For a seeded family of random non-convex simple polygons, for every vertex `O` the decider calls
**not good**, I will sample interior points `x` and test exactly whether `ρ^{-1}(x)` is also
interior — i.e. whether `Ω ∩ ρ(Ω) = ∅` as Lemma A asserts.

**Predicted outcome:** zero hits, over every exceptional vertex found.

**Falsifier:** a single exact hit `x ∈ Ω`, `ρ^{-1}(x) ∈ Ω` at a vertex the decider calls not good.
That is K2/K3, and it is the single most valuable thing this lane could produce.

## 7. Pre-registered prediction C — the criterion never fires on a convex curve

Every convex body lies in a supporting half-plane at each boundary point, so I predict the density
criterion is **vacuous** on convex curves: density `≤ ½` at every boundary point and every radius,
never `>`. Checked against the convex fixtures of the polygon experiment.

**Falsifier:** a convex polygon vertex with ball density `> ½`. Would mean my supporting-line
argument is wrong.

## 8. Verdict rule, fixed in advance

| Outcome | Verdict recorded in `README.md` |
|---|---|
| K1 or K2 met | lane `refuted`; the rotation lane's Lemma A gets a correction notice |
| K3 met | lane `refuted`, and an extraordinary-claim-grade bug report on the chain |
| K4 met, K1–K3 not | lemma stands as `sketch`, lane **demoted**: "true, never stronger than the sector criterion" |
| none met | lemma stands as `sketch`, lane keeps its criterion, with the honest comparison to the sector criterion stated either way |

Nothing in this lane may be promoted above `sketch` by me; `verified:review` requires a
different model family ([`../../../../RULES.md`](../../../../RULES.md) §5).
