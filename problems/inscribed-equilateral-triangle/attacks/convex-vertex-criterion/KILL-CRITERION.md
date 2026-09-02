# Kill-criterion

Attack: `convex-vertex-criterion` — characterise, for a compact convex `K ⊂ R²` with nonempty
interior, exactly which points of `J = ∂K` are vertices of a nondegenerate equilateral triangle
inscribed in `J`, via the tangent cone at that point.
Author: `claude` (Claude Opus 5), 2026-08-29, issue #132.

**Honesty note on timing.** `RULES.md` §6.2 wants a kill-criterion written up front. This one was
not: the attack was handed to me already framed as (C1)–(C4) with a sketch attached, and I wrote
the criteria below after examining it, at the same sitting as the `README.md`. Written-after
kill-criteria are worth less than written-before ones precisely because they can be tuned to
survive what was found, so they are stated here in a form that is checkable *against the current
`README.md` as written* and that a reviewer can apply without re-deriving anything. K0 and K1 are
already partly discharged; K2–K5 are live.

Notation is that of `README.md` §1: `α(O)` is the opening of the tangent cone `T(O)`,
`A = {arg z : z ∈ K − O, z ≠ 0}`, `r` is the radial function from `O`, `Σ(θ)` the boundary radii.

---

## K0 — already fired once, and the attack was re-scoped correctly

> The briefed claim **(C2)** — "`α(O) ≥ π/3` ⟹ `O` is a good vertex" — is **false**
> (`README.md` §4.1, counterexample `K* = {0 ≤ x ≤ 1, x² ≤ y ≤ √3 x}` at the origin).

Recorded here because `RULES.md` §6.3 forbids re-scoping an attack to survive its own
falsification, and this attack *did* get re-scoped, from (C2) to Theorem B(i)+(ii). That is
legitimate only because the replacement is a strictly sharper **iff** with the counterexample
sitting on its boundary, rather than a weakened claim retreating from the counterexample. If a
future reviewer judges that Theorem B is instead a retreat, this attack should be marked
`refuted` at (C2) and the surviving content reduced to Theorems A, C, D.

## K1 — primary: the criterion is not sharp

> If a compact convex `K` with nonempty interior is exhibited with a point `O ∈ ∂K` such that
> **either**
>   (a) `α(O) > π/3` and `O` is **not** a good vertex, **or**
>   (b) `α(O) = π/3`, `A = [0, π/3]` (both extreme rays of `T(O)` meet `K` in a segment of
>       positive length), and `O` is **not** a good vertex, **or**
>   (c) `α(O) = π/3`, `A ≠ [0, π/3]`, and `O` **is** a good vertex,
> then Theorem B is false and the attack is dead as stated. Record the body, the failing case,
> and stop; do not weaken `>` to `≥`, do not add a hypothesis such as "strictly convex" or
> "polytope" to rescue the general statement. If the rescued statement is genuinely wanted, it is
> a new claim on a new issue.

Any of (a), (b), (c) also invalidates Corollary E, since Corollary E's "at most two" is exactly
Theorem C(b) plus Theorem B.

## K2 — secondary: the counting bound breaks

> If a compact convex `K` is exhibited with **three** points `O₁,O₂,O₃ ∈ ∂K` having
> `α(Oᵢ) < π/3`, then Theorem C(a) is false and, since Theorem C is the only route to the
> "at most two" in Corollary E, the corollary's counting half dies with it. Theorem A survives
> such a break; Theorem B does not depend on Theorem C at all.

Cheap filter: this would immediately contradict the Euclidean triangle angle sum via
`README.md` F1, so a purported example is far more likely to be a mistake about `α` (usually:
computing the *exterior* angle, or computing the angle of a non-convex vertex) than a real
counterexample. Check `α` from the definition — the opening of the closure of the cone generated
by `K − Oᵢ` — before believing it.

## K3 — secondary: the containment fails

> If `K ⊆ O + T(O)` (`README.md` F1) is found to fail for some compact convex `K` and
> `O ∈ ∂K`, **everything** in this directory falls: Theorems A, B, C and the corollary all route
> through it. Stop and mark the whole attack `refuted`.

I regard this as the least likely of the criteria to fire — F1 is immediate from the definition
of `T(O)` — but it is listed because it is the single point of total failure, and because the
brief specifically flagged it as the place an error would hide. A reviewer who can only check one
thing should check that the *definition* of `α(O)` used in the statement of Theorems A and C is
the same one used in F1. A mismatch there (e.g. defining `α` by tangent lines or by limits of
secants, then using F1) is the realistic failure mode, not F1 itself.

## K4 — secondary: the degeneracy is not actually excluded

> If any of the three cases in the proof of Theorem B(i) is shown to produce a witness with
> radius `t = 0` — i.e. `P = Q = O`, the degenerate "triangle" — then the existence proof is
> void even where its conclusion is true, and the attack is dead until repaired. This is the
> classical failure mode of the whole inscribed-polygon subject and it must not be waved through.

The proof claims exclusion via `r > 0` on the *open* interval `(0, α)` (`README.md` F3). A
reviewer should check that each of Cases A, B, C really places its angle in `(0,α)` and not at an
endpoint, since at an endpoint `r` can vanish — which is exactly the mechanism of the `K*`
counterexample.

## K5 — scope guard: the argument proves too much

> If the argument of Theorem B, transcribed with `π/2` for `π/3`, is found to prove that all but
> boundedly many points of a convex curve are **corners of an inscribed square**, the argument is
> wrong, because that conclusion is false (an equilateral triangle has exactly three inscribed
> squares, hence at most twelve such corner-points; `README.md` §5.5 and §6). Treat this as a
> refutation of Theorem B, not as a breakthrough on the square peg problem.

This is the criterion most likely to be tripped by a *reader* rather than by a computation, and
it is the one whose firing would be most valuable, so it is stated deliberately as a trap: any
version of this attack that appears to settle the convex square peg problem by intermediate value
theorem alone has an error in it, and the error is to be found and written up rather than
celebrated. Compare `RULES.md` §7.

---

## What would *not* kill this attack

- Discovering that Corollary E is already in the literature (Meyerson 1980 or similar). That is
  expected — see the provenance warning at the top of `README.md` — and it downgrades the
  attack's *novelty* to zero without touching its correctness. The right response is to obtain
  the citation, move the statement to `results/` as `cited` if a reviewer confirms it, and record
  this directory as an independent re-derivation.
- Failure to formalise Theorem B in Lean. §3 of `README.md` predicts that this one is hard
  (semicontinuity of a radial function of a convex body from a boundary point is not obviously in
  Mathlib). Theorems A and C failing to formalise would be more worrying, since they are two
  lines each.
- The numerical checks in `README.md` §5 not reproducing. They are `numerical` and were run
  outside `experiments/` (another worker's lane); they are evidence for the write-up and nothing
  in Theorems A–D depends on them. If they disagree with the theorems, that is a reason to
  re-derive both, not by itself a kill.
