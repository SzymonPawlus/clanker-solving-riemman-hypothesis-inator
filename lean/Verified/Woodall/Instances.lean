/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: claude
-/
import Verified.Woodall.Basic

/-!
# Woodall's conjecture — small instances, checked by `decide`

Sanity fixtures for the definitions in `Verified/Woodall/Basic.lean`, of exactly the kind
`problems/woodalls-conjecture/RULES.md` §4 demands ("Sanity-check them on a small example — a
directed path, a directed cycle (which has *no* dicuts), a DAG with two sources", and "Test any
implementation against the `τ = 2` case").

Every theorem here is closed by `decide`, i.e. by kernel evaluation of the `Decidable` instances
in `Basic.lean`, which are themselves *proved* to agree with the quantified statements. The
kernel checks these, not the compiler: no compiler-trusting evaluation tactic is used anywhere.

**None of this is evidence for Woodall's conjecture.** A conjecture quantified over all digraphs
is not supported by any finite number of instances (problem `RULES.md` §0). These fixtures test
the *definitions*.
-/

namespace Verified.Woodall

/-! ## The directed cycle has no dicut

Every vertex of a directed cycle has an entering arc reachable from outside any proper nonempty
`U`, so `δ⁻(U) = ∅` never holds together with `δ⁺(U) ≠ ∅`. This is the first thing a wrong
implementation gets wrong: dropping the `δ⁻(U) = ∅` requirement makes `{0}` a "dicut" here. -/

/-- The directed 3-cycle `0 → 1 → 2 → 0`. -/
def cycle3 : Digraph 3 3 := Digraph.ofArcList [(0, 1), (1, 2), (2, 0)]

/-- **The directed cycle has no dicut at all.** -/
theorem cycle3_no_dicut : ∀ U : VertexSet 3, ¬ IsDicutShore cycle3 U := by decide

/-- Consequently `τ` is undefined for it: no natural number is the minimum dicut size. -/
theorem cycle3_no_min_dicut_size : ∀ t : Nat, t ≤ 3 → ¬ IsMinDicutSize cycle3 t := by decide

/-- The computed `τ` agrees: `none`, meaning "no dicut". -/
theorem cycle3_tau : tau? cycle3 = none := by decide

/-- Every arc set — including the empty one — is vacuously a dijoin of the directed cycle. -/
theorem cycle3_empty_isDijoin : IsDijoin cycle3 (fun _ => false) := by decide

/-! ## The directed path and its dicuts -/

/-- The directed path `0 → 1 → 2`, with arc `0` being `0 → 1` and arc `1` being `1 → 2`. -/
def path3 : Digraph 3 2 := Digraph.ofArcList [(0, 1), (1, 2)]

/-- **The dicuts of the directed path are exactly the two "prefix" cuts** `{0}` and `{0, 1}`.
Stated as a pointwise characterisation of the shores, so no set-equality decidability is
needed. -/
theorem path3_dicutShores (U : VertexSet 3) :
    IsDicutShore path3 U ↔
      ((U 0 = true ∧ U 1 = false ∧ U 2 = false) ∨ (U 0 = true ∧ U 1 = true ∧ U 2 = false)) := by
  revert U; decide

/-- Both dicuts of the path are single arcs, so `τ = 1`. -/
theorem path3_tau : IsMinDicutSize path3 1 := by decide

/-- And the computed `τ` agrees. -/
theorem path3_tau? : tau? path3 = some 1 := by decide

/-! ## The diamond: `τ = 2` and two disjoint dijoins

The fixture from `problems/woodalls-conjecture/README.md`: `s → x, s → y, x → t, y → t`, which
is source–sink connected. `τ = 2` is the case problem `RULES.md` §4 says to test against, and
the two `s`–`t` paths are the two disjoint dijoins. -/

/-- The diamond `s → x`, `s → y`, `x → t`, `y → t` with `s = 0, x = 1, y = 2, t = 3`. -/
def diamond : Digraph 4 4 := Digraph.ofArcList [(0, 1), (0, 2), (1, 3), (2, 3)]

/-- **`τ = 2` for the diamond.** -/
theorem diamond_tau : IsMinDicutSize diamond 2 := by decide

/-- And the computed `τ` agrees. -/
theorem diamond_tau? : tau? diamond = some 2 := by decide

/-- The path `s → x → t`, as an arc set. -/
def diamondJ₁ : ArcSet 4 := arcSetOf [0, 2]

/-- The path `s → y → t`, as an arc set. -/
def diamondJ₂ : ArcSet 4 := arcSetOf [1, 3]

theorem diamondJ₁_isDijoin : IsDijoin diamond diamondJ₁ := by decide

theorem diamondJ₂_isDijoin : IsDijoin diamond diamondJ₂ := by decide

theorem diamond_disjoint : ArcDisjoint diamondJ₁ diamondJ₂ := by decide

/-- The two dijoins **partition** the arc set: every arc lies in exactly one of them. Together
with `diamond_tau` this is the conclusion Woodall's conjecture predicts for this one digraph —
verified here for this digraph only, by enumeration. -/
theorem diamond_partition (a : Fin 4) :
    (diamondJ₁ a = true ∧ diamondJ₂ a = false) ∨ (diamondJ₁ a = false ∧ diamondJ₂ a = true) := by
  revert a; decide

/-- The easy direction, instantiated: these two dijoins already meet the `≤ τ` bound, so no
third arc-disjoint dijoin can be added. -/
theorem diamond_two_le_tau :
    [diamondJ₁, diamondJ₂].length ≤ 2 :=
  length_le_tau diamond 2 diamond_tau [diamondJ₁, diamondJ₂]
    (by intro J hJ; rcases List.mem_cons.1 hJ with rfl | hJ
        · exact diamondJ₁_isDijoin
        · rcases List.mem_cons.1 hJ with rfl | hJ
          · exact diamondJ₂_isDijoin
          · exact absurd hJ (by simp))
    (by simp [ArcDisjoint]; decide)

/-! ## The near-miss DAG

`s₁ → t₁, s₂ → t₁, s₂ → t₂` from `problems/woodalls-conjecture/README.md`: two sources, `s₁` a
source and `t₂` a sink with no directed `s₁`–`t₂` path, so the source–sink-connected theorem
says nothing about it. It is **not** a counterexample, and the facts below are not claimed to
be evidence either way. -/

/-- `s₁ → t₁, s₂ → t₁, s₂ → t₂` with `s₁ = 0, t₁ = 1, s₂ = 2, t₂ = 3`. -/
def nearMiss : Digraph 4 3 := Digraph.ofArcList [(0, 1), (2, 1), (2, 3)]

/-- `τ = 1`: the single arc `s₁ → t₁` is a dicut, since nothing enters `{s₁}`. -/
theorem nearMiss_tau : IsMinDicutSize nearMiss 1 := by decide

/-- And the computed `τ` agrees. -/
theorem nearMiss_tau? : tau? nearMiss = some 1 := by decide

/-- `{s₁}` is the shore realising it. -/
theorem nearMiss_shore : IsDicutShore nearMiss (fun v => v == 0) := by decide

/-- With `τ = 1`, one dijoin suffices, and the whole arc set is one — so the conjecture's
prediction holds here trivially. Not a counterexample. -/
theorem nearMiss_all_isDijoin : IsDijoin nearMiss (fun _ => true) := by decide

/-- It has two sources (`s₁` and `s₂`), the configuration problem `RULES.md` §4 asks to test. -/
theorem nearMiss_two_sources :
    (∀ a : Fin 3, nearMiss.head a ≠ 0) ∧ (∀ a : Fin 3, nearMiss.head a ≠ 2) := by decide

/-! ## The §4 trap, exhibited

`problems/woodalls-conjecture/RULES.md` §4: "Confirm your code's notion of dicut requires
`δ⁻(U) = ∅`, not merely `δ⁺(U) ≠ ∅`." Here is a witness that this file's definition does
require it. -/

/-- On the directed 3-cycle, `{0}` has an arc leaving it, so a definition that only asked for
`δ⁺(U) ≠ ∅` would call it a dicut shore. It is not one, because `2 → 0` enters it. -/
theorem cycle3_trap :
    (∃ a, deltaOut cycle3 (fun v => v == 0) a = true) ∧
      ¬ IsDicutShore cycle3 (fun v => v == 0) := by decide

/-! ## Where the two dicut conventions disagree

The superseded branch `origin/claude/76-lean-woodall` admitted the empty set as a dicut; this
file requires `δ⁺(U) ≠ ∅`. On weakly connected digraphs the readings agree. They disagree on
disconnected ones, and pretending otherwise would be exactly the silent-weakening failure this
development is meant to avoid, so the disagreement is exhibited. -/

/-- Two disjoint arcs `0 → 1` and `2 → 3`: a disconnected digraph. -/
def twoArcs : Digraph 4 2 := Digraph.ofArcList [(0, 1), (2, 3)]

/-- `{0, 1}` is a dicut shore under the permissive convention (nothing enters it) but **not**
under this file's convention (nothing leaves it either, so `δ⁺ = ∅`). The two conventions
therefore give different sets of dicuts, and different values of `τ`. -/
theorem twoArcs_conventions_disagree :
    IsDicutShoreAllowingEmpty twoArcs (fun v => v == 0 || v == 1) ∧
      ¬ IsDicutShore twoArcs (fun v => v == 0 || v == 1) := by decide

/-- Under this file's convention `τ = 1` for it, realised by the shore `{0}`. Under the
permissive convention the empty dicut would force `τ = 0` and no dijoin would exist. -/
theorem twoArcs_tau : IsMinDicutSize twoArcs 1 := by decide

/-- So Woodall's conjecture holds for this digraph, by the degenerate `τ = 1` case. -/
theorem twoArcs_woodall : WoodallConjecture twoArcs :=
  woodall_of_isMinDicutSize_one twoArcs_tau

/-- Likewise for the directed path and the near-miss DAG, both of which have `τ = 1`. Degenerate
corner of the conjecture, not progress on it. -/
theorem path3_woodall : WoodallConjecture path3 :=
  woodall_of_isMinDicutSize_one path3_tau

theorem nearMiss_woodall : WoodallConjecture nearMiss :=
  woodall_of_isMinDicutSize_one nearMiss_tau

end Verified.Woodall
