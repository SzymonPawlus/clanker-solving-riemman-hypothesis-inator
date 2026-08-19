# 2026-08-19 — Lean foundations for Woodall (issue #76, PR #79)

## The environment result, which may matter more than the maths

**There is no Lean toolchain in the worker image, and it cannot be installed from here.** The
egress proxy returns `403` policy denials for `elan.lean-lang.org`, `release.lean-lang.org`, and
`lakecache.blob.core.windows.net`. The first two block the compiler; the third blocks
`lake exe cache get`, and without that Lean compiles Mathlib from source for hours, so the third
denial alone kills a local build even if the compiler were obtainable.

`github.com` and `objects.githubusercontent.com` *are* reachable, so the elan/Lean release
tarballs could in principle be pulled from GitHub instead. I did not do that: `/root/.ccr/README.md`
says to report denied hosts rather than route around them, and it would not have helped anyway,
because the Mathlib olean cache has no GitHub mirror I can use.

Practical consequence for future Lean workers in this environment: **you cannot iterate against a
compiler.** Either the image gains a warm `.lake` and toolchain, or Lean work has to be written
blind and validated by repo CI. That changes the cost of Lean work here by a lot and should be
factored into any dispatch decision. Worth raising with a human.

## What I did instead

Wrote the file carefully, minimised the Mathlib API surface deliberately (only `Finset`,
`Fintype`, `Finset.card`, `Finset.card_le_card_of_injOn`), pushed, and used the repo's own Lean CI
as the first machine check. That is honest — the PR says plainly that I never ran `lake build` —
but it burns a CI round-trip per typo, which is exactly the loop the missing toolchain would have
made cheap.

## Design decisions I want to be able to revisit

1. **Relational `τ` and `ν` instead of `sInf`/`sSup`.** `IsMinDicut C` says `C.card = τ`;
   `HasPacking k` says `k ≤ ν`. This avoids picking a convention for a digraph with *no* dicut
   (strongly connected ⇒ no dicuts ⇒ `sInf ∅ = 0` would make `τ = 0`, which is arguably wrong;
   morally `τ = ∞`). Price: `WoodallConjecture` is vacuously true for such digraphs. I believe
   that is correct rather than a dodge — there is genuinely no constraint, since every arc set is
   vacuously a dijoin — but it is the single step I would most want a reviewer to attack, and I
   said so in the PR.

2. **`∅` allowed as a dicut.** Deliberate. It makes `τ = 0` a real case with real content (no
   dijoin exists at all), which I could then *prove*, rather than excluding it by fiat.

3. **`FinDigraph`, not Mathlib's `Digraph`.** Mathlib's is `Adj : V → V → Prop`; the conjecture
   counts arcs, so I need `Finset (V × V)` and its `card`. Converting at every step would have
   been pure overhead.

4. **`S ≠ ∅` rather than `S.Nonempty`** in `IsDicutSide` — purely so the `decide` sanity checks
   get their `Decidable` instances from `DecidableEq` without needing `Finset.decidableNonempty`.
   A small hedge against writing blind. Mathematically identical.

## The trap I was most worried about

`problems/woodalls-conjecture/RULES.md` §4: dicut requires `δ⁻(S) = ∅`, not `δ⁺(S) ≠ ∅`. I turned
that warning into a theorem rather than a comment — `not_isDicutSide_sink` shows the sink `{1}` of
the one-arc digraph is not a dicut side. Under the wrong definition it would be, `∅` would be a
dicut, and `τ` would come out `0` instead of `1`. If someone later "generalises" the definitions
and that theorem stops holding, they broke it.

## Scope discipline

Did not attempt the conjecture (§7). What is proved is `ν ≤ τ` (the *easy* direction, labelled as
such in its own docstring so it cannot be misread) and the conjecture for `τ ≤ 1`, which is the
degenerate range and evidence for nothing. The first case with content is `τ = 2`, and Mathlib has
none of the machinery — no dicuts, no dijoins, no Lucchesi–Younger — so that is a real project,
not a follow-up ticket.
