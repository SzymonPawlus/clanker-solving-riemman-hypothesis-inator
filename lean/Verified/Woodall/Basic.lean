/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: claude
-/
import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Fintype.Prod
import Mathlib.Tactic

/-!
# Woodall's conjecture — definitions, statement, and the easy direction

**Claim kind: definitions plus the trivial direction.** Nothing here proves Woodall's conjecture,
and nothing here should be cited as progress on it. What is proved is the direction that is
*easy and true*: a packing of arc-disjoint dijoins is never larger than a dicut. The conjectured
direction is stated (`WoodallConjecture`) and left entirely unproved.

## What the definitions mean, in prose

`problems/woodalls-conjecture/RULES.md` §4 says the definitions are the trap, so each one is
spelled out here in words as well as in Lean. Read this list against the Lean below; if they
disagree, the Lean is what CI checks and the prose is what a human believes, and that gap is
exactly the §7 failure mode "a formal statement that does not say what you think it says".

* A **finite digraph** `D` is just a finite set of arcs `D.arcs : Finset (V × V)` on a finite
  vertex type `V`. The pair `(u, v)` is the arc **from `u` to `v`**: `u` is the tail, `v` is the
  head. Loops and the absence of arcs are both permitted; `Finset` means no parallel arcs, which
  is harmless here because a dicut and a dijoin are both *sets* of arcs.

* `D.out S` is `δ⁺(S)`, the arcs **leaving** `S`: tail in `S`, head outside `S`.

* `D.inn S` is `δ⁻(S)`, the arcs **entering** `S`: tail outside `S`, head in `S`.

* `D.IsDicutSide S` says `S` is a **nonempty proper** vertex subset with `δ⁻(S) = ∅` — no arc
  enters `S`. The condition `δ⁻(S) = ∅` is the whole content: §4 warns that requiring merely
  `δ⁺(S) ≠ ∅` is the single error that invalidates most first attempts, and
  `not_isDicutSide_sink` below is a concrete witness that the two conditions differ.

* `D.IsDicut C` says `C` is `δ⁺(S)` for some such `S`. Note this does **not** require `C` to be
  nonempty: if some nonempty proper `S` has no arcs entering *and* none leaving, then `∅` is a
  dicut. That is a deliberate convention choice (some authors require dicuts to be nonempty) and
  it is the honest one here, because such a digraph genuinely has no dijoin at all — see
  `not_isDijoin_of_isDicut_empty` — so the conjecture holds in that case with both sides `0`
  rather than being definitionally excluded.

* `D.IsDijoin J` says `J` is a set of arcs of `D` meeting **every** dicut. (The equivalent
  "contracting `J` makes `D` strongly connected" formulation is not used; the hitting-set form is
  the one the conjecture is about.)

* `D.HasPacking k` says there are `k` dijoins that are **pairwise arc-disjoint**. The packing
  number `ν(D)` is the largest such `k`; it is not defined as a number here, because every
  statement below is cleaner in the relational form and defining a maximum would drag in
  boundedness side conditions that add risk without adding content.

* `D.IsMinDicut C` says `C` is a dicut of minimum cardinality, so `C.card` **is** `τ(D)`. Again
  `τ` is not defined as a standalone number: `IsMinDicut` carries the same information and avoids
  a `sInf`-of-the-empty-set convention in the case where `D` has no dicut at all.

* `WoodallConjecture D` says: for every minimum dicut `C`, there are `C.card` pairwise
  arc-disjoint dijoins — i.e. `ν(D) ≥ τ(D)`. Together with `card_le_of_hasPacking` (proved
  below), which gives `ν(D) ≤ τ(D)`, this is exactly `ν(D) = τ(D)`, Woodall's conjecture. When
  `D` has no dicut the statement is vacuous, which is correct: there is then no constraint to
  satisfy, and indeed every arc set is vacuously a dijoin.

## What is actually proved here

* `IsDijoin.exists_mem_of_isDicut` — a dijoin meets every dicut.
* `card_le_of_hasPacking` — **the easy direction**, `ν(D) ≤ τ(D)`: `k` pairwise arc-disjoint
  dijoins each contain a distinct arc of any fixed dicut `C`, so `k ≤ |C|`.
* `woodall_of_card_le_one` — Woodall's conjecture **holds when `τ ≤ 1`**, both cases proved
  outright. This is not evidence for the conjecture; it is the degenerate range.

Per `problems/woodalls-conjecture/RULES.md` §1 the "easy-direction filter": `card_le_of_hasPacking`
is deliberately and only the trivial bound, and is labelled as such so that it can never be
mistaken for the existence direction.

## Sanity checks

The final section instantiates the definitions on digraphs whose answers are known by hand: a
single arc (exactly one dicut, of size 1) and a directed 2-cycle (**no** dicuts, the check §4
explicitly asks for). These are `theorem`s, not comments, so CI checks them.
-/

namespace Verified.Woodall

variable {V : Type*} [DecidableEq V] [Fintype V]

/-- A finite digraph on the vertex type `V`, given by its set of arcs. The arc `(u, v)` points
**from `u` to `v`**. -/
structure FinDigraph (V : Type*) where
  /-- The arcs of the digraph; `(u, v)` is the arc from `u` to `v`. -/
  arcs : Finset (V × V)

namespace FinDigraph

/-- `δ⁺(S)`: the arcs of `D` **leaving** `S` — tail in `S`, head outside `S`. -/
def out (D : FinDigraph V) (S : Finset V) : Finset (V × V) :=
  D.arcs.filter fun a => a.1 ∈ S ∧ a.2 ∉ S

/-- `δ⁻(S)`: the arcs of `D` **entering** `S` — tail outside `S`, head in `S`. -/
def inn (D : FinDigraph V) (S : Finset V) : Finset (V × V) :=
  D.arcs.filter fun a => a.1 ∉ S ∧ a.2 ∈ S

theorem out_subset_arcs (D : FinDigraph V) (S : Finset V) : D.out S ⊆ D.arcs :=
  Finset.filter_subset _ _

theorem inn_subset_arcs (D : FinDigraph V) (S : Finset V) : D.inn S ⊆ D.arcs :=
  Finset.filter_subset _ _

/-- `S` is the source side of a dicut: a nonempty proper vertex subset that **no arc enters**.

The condition `D.inn S = ∅` is the one that matters. Weakening it to `D.out S ≠ ∅` is the error
`problems/woodalls-conjecture/RULES.md` §4 warns about. -/
def IsDicutSide (D : FinDigraph V) (S : Finset V) : Prop :=
  S ≠ ∅ ∧ S ≠ Finset.univ ∧ D.inn S = ∅

/-- `C` is a **dicut** of `D`: the set of arcs leaving some nonempty proper vertex set that no arc
enters. Not required to be nonempty — see the module docstring. -/
def IsDicut (D : FinDigraph V) (C : Finset (V × V)) : Prop :=
  ∃ S : Finset V, D.IsDicutSide S ∧ C = D.out S

/-- A **dijoin** of `D`: a set of arcs of `D` meeting every dicut. -/
def IsDijoin (D : FinDigraph V) (J : Finset (V × V)) : Prop :=
  J ⊆ D.arcs ∧ ∀ C, D.IsDicut C → (J ∩ C).Nonempty

/-- `D` has a packing of `k` **pairwise arc-disjoint** dijoins. The packing number `ν(D)` is the
largest such `k`. -/
def HasPacking (D : FinDigraph V) (k : ℕ) : Prop :=
  ∃ J : Fin k → Finset (V × V),
    (∀ i, D.IsDijoin (J i)) ∧ ∀ i j, i ≠ j → Disjoint (J i) (J j)

/-- `C` is a dicut of minimum size; equivalently `C.card = τ(D)`. -/
def IsMinDicut (D : FinDigraph V) (C : Finset (V × V)) : Prop :=
  D.IsDicut C ∧ ∀ C', D.IsDicut C' → C.card ≤ C'.card

/-- **Woodall's conjecture** for `D`: for every minimum dicut `C` there are `C.card` pairwise
arc-disjoint dijoins, i.e. `ν(D) ≥ τ(D)`.

Combined with `card_le_of_hasPacking`, which proves `ν(D) ≤ τ(D)` unconditionally, this says
exactly `ν(D) = τ(D)`. **This is not proved anywhere in this file and must not be assumed.** -/
def WoodallConjecture (D : FinDigraph V) : Prop :=
  ∀ C, D.IsMinDicut C → D.HasPacking C.card

theorem IsDicut.subset_arcs {D : FinDigraph V} {C : Finset (V × V)} (hC : D.IsDicut C) :
    C ⊆ D.arcs := by
  obtain ⟨S, -, rfl⟩ := hC
  exact D.out_subset_arcs S

/-- A dijoin contains an arc of every dicut. This is the defining property, restated in the form
the counting argument uses. -/
theorem IsDijoin.exists_mem_of_isDicut {D : FinDigraph V} {J C : Finset (V × V)}
    (hJ : D.IsDijoin J) (hC : D.IsDicut C) : ∃ a, a ∈ J ∧ a ∈ C := by
  obtain ⟨a, ha⟩ := hJ.2 C hC
  exact ⟨a, (Finset.mem_inter.mp ha).1, (Finset.mem_inter.mp ha).2⟩

/-- **The easy direction of Woodall's conjecture: `ν(D) ≤ τ(D)`.**

If `D` has `k` pairwise arc-disjoint dijoins then `k ≤ |C|` for *every* dicut `C`, in particular
for a minimum one. Proof: each dijoin meets `C`, pick one such arc from each; arc-disjointness
makes the choice injective, so the `k` chosen arcs are distinct elements of `C`.

`problems/woodalls-conjecture/RULES.md` §1, easy-direction filter: this is the trivial bound and
nothing more. The conjecture is the *other* inequality. -/
theorem card_le_of_hasPacking {D : FinDigraph V} {k : ℕ} {C : Finset (V × V)}
    (hk : D.HasPacking k) (hC : D.IsDicut C) : k ≤ C.card := by
  obtain ⟨J, hJ, hdisj⟩ := hk
  choose f hfJ hfC using fun i => (hJ i).exists_mem_of_isDicut hC
  have hinj : ∀ i j : Fin k, f i = f j → i = j := by
    intro i j hij
    by_contra hne
    have hmem : f i ∈ J j := by rw [hij]; exact hfJ j
    exact (Finset.disjoint_left.mp (hdisj i j hne) (hfJ i)) hmem
  have hcard : (Finset.univ : Finset (Fin k)).card ≤ C.card :=
    Finset.card_le_card_of_injOn f (fun i _ => hfC i) (fun i _ j _ h => hinj i j h)
  simpa using hcard

/-- Corollary of the easy direction: a packing is no larger than the minimum dicut, `ν ≤ τ`. -/
theorem card_le_of_hasPacking_of_isMinDicut {D : FinDigraph V} {k : ℕ} {C : Finset (V × V)}
    (hk : D.HasPacking k) (hC : D.IsMinDicut C) : k ≤ C.card :=
  card_le_of_hasPacking hk hC.1

/-- If `∅` is a dicut then `D` has **no** dijoin at all: there is no arc to meet the empty dicut
with. This is why the empty dicut is allowed by `IsDicut` rather than excluded by fiat. -/
theorem not_isDijoin_of_isDicut_empty {D : FinDigraph V} {J : Finset (V × V)}
    (hC : D.IsDicut ∅) : ¬D.IsDijoin J := by
  intro hJ
  obtain ⟨a, -, ha⟩ := hJ.exists_mem_of_isDicut hC
  exact absurd ha (Finset.not_mem_empty a)

/-- Every digraph has the empty packing. -/
theorem hasPacking_zero (D : FinDigraph V) : D.HasPacking 0 :=
  ⟨Fin.elim0, fun i => i.elim0, fun i _ _ => i.elim0⟩

/-- If every dicut is nonempty then the full arc set is a dijoin. -/
theorem isDijoin_arcs (D : FinDigraph V) (h : ∀ C, D.IsDicut C → C.Nonempty) :
    D.IsDijoin D.arcs := by
  refine ⟨Finset.Subset.refl _, fun C hC => ?_⟩
  obtain ⟨a, ha⟩ := h C hC
  exact ⟨a, Finset.mem_inter.mpr ⟨hC.subset_arcs ha, ha⟩⟩

/-- If every dicut is nonempty then `D` has a packing of size `1`. -/
theorem hasPacking_one (D : FinDigraph V) (h : ∀ C, D.IsDicut C → C.Nonempty) :
    D.HasPacking 1 :=
  ⟨fun _ => D.arcs, fun _ => D.isDijoin_arcs h, fun i j hij => absurd (Subsingleton.elim i j) hij⟩

/-- **Woodall's conjecture holds when `τ(D) = 0`.** An empty minimum dicut means no dijoin
exists, so `ν = 0 = τ`. -/
theorem woodall_of_isMinDicut_card_zero {D : FinDigraph V} {C : Finset (V × V)}
    (_h : D.IsMinDicut C) (hcard : C.card = 0) : D.HasPacking C.card := by
  rw [hcard]
  exact D.hasPacking_zero

/-- **Woodall's conjecture holds when `τ(D) = 1`.** Minimality makes every dicut nonempty, so the
whole arc set is a single dijoin, and `ν = 1 = τ`. -/
theorem woodall_of_isMinDicut_card_one {D : FinDigraph V} {C : Finset (V × V)}
    (h : D.IsMinDicut C) (hcard : C.card = 1) : D.HasPacking C.card := by
  rw [hcard]
  refine D.hasPacking_one fun C' hC' => ?_
  have h1 : C.card ≤ C'.card := h.2 C' hC'
  rw [hcard] at h1
  exact Finset.card_pos.mp h1

/-- **Woodall's conjecture holds whenever `τ(D) ≤ 1`.**

This is the degenerate range and is *not* evidence for the conjecture; the first genuinely
non-trivial case is `τ = 2` (a theorem of Lee–Wakabayashi, not formalised here). -/
theorem woodall_of_card_le_one {D : FinDigraph V} {C : Finset (V × V)}
    (h : D.IsMinDicut C) (hcard : C.card ≤ 1) : D.HasPacking C.card := by
  by_cases h0 : C.card = 0
  · exact woodall_of_isMinDicut_card_zero h h0
  · exact woodall_of_isMinDicut_card_one h (by omega)

end FinDigraph

/-!
## Sanity checks on concrete digraphs

`problems/woodalls-conjecture/RULES.md` §4 requires the definitions be checked against small
examples before anything is built on them. These are `theorem`s so that CI checks them.
-/

section Examples

/-- The digraph on `Fin 2` with the single arc `0 → 1`. By hand: the only vertex set that no arc
enters and that is nonempty and proper is `{0}`, whose out-arcs are `{(0, 1)}`. So there is
exactly one dicut, of size `1`, and `τ = 1`. -/
def oneArc : FinDigraph (Fin 2) := ⟨{(0, 1)}⟩

/-- The directed `2`-cycle on `Fin 2`. By hand it has **no** dicut: each of the two nonempty
proper vertex sets has an arc entering it. This is §4's "a directed cycle has no dicuts" check. -/
def twoCycle : FinDigraph (Fin 2) := ⟨{(0, 1), (1, 0)}⟩

/-- `{0}` is the source side of a dicut of `oneArc`, and the dicut is `{(0, 1)}`. -/
theorem oneArc_isDicut : oneArc.IsDicut {(0, 1)} :=
  ⟨{0}, ⟨by decide, by decide, by decide⟩, by decide⟩

/-- **The §4 trap, exhibited.** The sink `{1}` has *no arcs leaving it* (`δ⁺({1}) = ∅`), so a
definition of "dicut" that forgot the `δ⁻(S) = ∅` requirement would hand back `∅` as a dicut of
`oneArc` and report `τ = 0`. It is not a dicut side, because the arc `(0, 1)` enters it. -/
theorem not_isDicutSide_sink : ¬oneArc.IsDicutSide {1} := by
  rintro ⟨-, -, h⟩
  exact absurd h (by decide)

/-- `{(0, 1)}` is a *minimum* dicut of `oneArc`, so `τ(oneArc) = 1`. -/
theorem oneArc_isMinDicut : oneArc.IsMinDicut {(0, 1)} := by
  refine ⟨oneArc_isDicut, ?_⟩
  rintro C ⟨S, ⟨hne, hnu, hinn⟩, rfl⟩
  revert hne hnu hinn
  revert S
  decide

/-- End-to-end check: `oneArc` satisfies Woodall's conjecture, with `ν = τ = 1`. -/
theorem oneArc_hasPacking : oneArc.HasPacking ({(0, 1)} : Finset (Fin 2 × Fin 2)).card :=
  FinDigraph.woodall_of_card_le_one oneArc_isMinDicut (by decide)

/-- The directed `2`-cycle has no dicut at all — §4's directed-cycle check. -/
theorem twoCycle_no_dicut (C : Finset (Fin 2 × Fin 2)) : ¬twoCycle.IsDicut C := by
  rintro ⟨S, ⟨hne, hnu, hinn⟩, rfl⟩
  revert hne hnu hinn
  revert S
  decide

/-- Consequently the conjecture is vacuously true for the directed `2`-cycle: it has no minimum
dicut, because it has no dicut. -/
theorem twoCycle_woodall : twoCycle.WoodallConjecture :=
  fun _ hC => absurd hC.1 (twoCycle_no_dicut _)

end Examples

end Verified.Woodall
