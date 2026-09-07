# 2026-09-07 — Woodall Lean: closing the two docstring overclaims (issue #270)

Issue #270, found while promoting `problems/woodalls-conjecture/results/woodall-lean-basics.md`
to `verified:lean` (#267 / PR #269). Two docstrings in `lean/Verified/Woodall/Instances.lean`
promised more than the theorem below them delivered. Neither was a false statement; both were
the RULES §4 shape where a later reader cites a weak theorem for a strong fact.

The issue offered two fixes and argued for strengthening the statements rather than weakening
the prose. I checked that argument rather than taking it, and in both cases it held, so both
statements were strengthened. Nothing was fixed by editing prose down.

## D1 — `cycle3_no_min_dicut_size`

Was `∀ t : Nat, t ≤ 3 → ¬ IsMinDicutSize cycle3 t`, closed by `decide`; docstring said "no
natural number". `decide` cannot close the unbounded form — the quantifier ranges over an
infinite type and there is no `Decidable` instance to evaluate — so the bound was there to make
the tactic work, and the prose then quietly ignored it.

The unbounded form does not need enumeration at all. `IsMinDicutSize D t` has as its first
conjunct `∃ U, IsDicutShore D U ∧ card (deltaOut D U) = t`, i.e. it *asserts a dicut exists*. On
a digraph with no dicut that conjunct is unsatisfiable for every `t` at once, uniformly in `t` —
which is exactly `not_isMinDicutSize_of_no_dicut` in `Basic.lean`, written for this purpose
after audit finding F3 (`attacks/lean-foundations-audit/README.md` line 180). So:

```lean
theorem cycle3_no_min_dicut_size : ∀ t : Nat, ¬ IsMinDicutSize cycle3 t :=
  not_isMinDicutSize_of_no_dicut cycle3_no_dicut
```

One term, no `decide`, and the `t ≤ 3` version is now a one-line corollary of it (checked as an
`example` before deleting it).

## D2 — `cycle3_empty_isDijoin` → `cycle3_all_isDijoin`

Was `IsDijoin cycle3 (fun _ => false)`; docstring said "every arc set". Before proving the
strong form I checked whether it is actually true under this repo's `IsDijoin`, since the
instruction was explicitly to correct the docstring instead if it is not:

```lean
def IsDijoin (D : Digraph n m) (J : ArcSet m) : Prop :=
  ∀ U : VertexSet n, IsDicutShore D U → Meets (deltaOut D U) J
```

`J` occurs only in the conclusion of that implication, and the hypothesis is refuted for every
`U` by `cycle3_no_dicut`. The vacuity is therefore genuinely uniform in `J` — nothing about the
empty arc set was load-bearing:

```lean
theorem cycle3_all_isDijoin : ∀ J : ArcSet 3, IsDijoin cycle3 J :=
  fun _ U hU => absurd hU (cycle3_no_dicut U)
```

Renamed, because `cycle3_empty_isDijoin` naming a statement about all arc sets would have been a
new (milder) instance of the same defect. The weak form `IsDijoin cycle3 (fun _ => false)` is
`cycle3_all_isDijoin _`, checked before deletion.

Worth noting what this does *not* say: it is a statement about a digraph with no dicut, so it is
a fact about the definition being vacuous in the right place, not about dijoins being easy. That
is why `Basic.lean` makes `τ` `Option`-valued.

## Third prose fix, unprompted

The module docstring opened with "Every theorem here is closed by `decide`". After this change
two are not, so that line would itself have become an overclaim about the file's method. Amended
to name the two exceptions and say why they cannot be `decide`d.

## Checks

`lake build --wfail` green over the whole library (8712 jobs). `#print axioms` on everything
touched and its dependency:

```
'Verified.Woodall.cycle3_no_dicut' depends on axioms: [propext, Quot.sound]
'Verified.Woodall.cycle3_no_min_dicut_size' depends on axioms: [propext, Quot.sound]
'Verified.Woodall.cycle3_tau' depends on axioms: [propext, Quot.sound]
'Verified.Woodall.cycle3_all_isDijoin' depends on axioms: [propext, Quot.sound]
'Verified.Woodall.not_isMinDicutSize_of_no_dicut' does not depend on any axioms
```

No `sorryAx`, no `Lean.ofReduceBool`, no new `axiom`, no `native_decide`. (Recorded elsewhere and
worth repeating: CI's grep does not in fact catch `axiom`, and a `results/`-only PR runs no Lean
job at all, so `#print axioms` by hand is the real gate, not the workflow.)

## Left for someone else

`problems/woodalls-conjecture/results/woodall-lean-basics.md` rows 44-45 describe these two
theorems and carry the D1/D2 defect notes. PR #269 is rewriting that file right now, so I did not
touch it — file ownership, RULES §2. Reported the exact name and statement changes on issue #270
and on PR #269 so #269's author can reconcile after both land.

Not touched, and still open from #270: `diamond_two_le_tau` is literally `2 ≤ 2` and names no
digraph in its statement. Honestly labelled as content-free in the results file; making it carry
content means bounding `Js.length` for any pairwise-disjoint family of dijoins of `diamond`, which
is a different task.
