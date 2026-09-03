/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: claude
-/

/-!
# Woodall's conjecture — basic definitions and the trivial direction

**Nothing in this file is progress on Woodall's conjecture.** The only nontrivial-looking
theorem here, `length_le_card_deltaOut`, is the *easy* inequality, and
`problems/woodalls-conjecture/README.md` says it outright: "any 'proof' that only establishes
the easy inequality has proved nothing." See the warning block above
`length_le_card_deltaOut` before citing anything from this file.

## What is defined

Following `problems/woodalls-conjecture/README.md`, for a digraph `D = (V, A)` and
`U ⊆ V`:

* `deltaOut D U` — the arcs leaving `U`;
* `deltaIn D U` — the arcs entering `U`;
* `IsDicutShore D U` — `U` is a shore of a **dicut**: `δ⁻(U) = ∅` and `δ⁺(U) ≠ ∅`.
  The `δ⁻(U) = ∅` half is the one that is routinely dropped by mistake; problem `RULES.md` §4
  names exactly that error ("Confirm your code's notion of dicut requires `δ⁻(U) = ∅`, not
  merely `δ⁺(U) ≠ ∅`"). The `δ⁺(U) ≠ ∅` half was an addition to the README's text when this
  file was written (audit finding F1 on issue #151); the README was amended on 2026-09-02 to
  require it, so prose and code now agree and `IsDicutShoreAllowingEmpty` records the reading
  that was dropped.
* `IsDijoin D J` — `J` meets **every** dicut;
* `IsMinDicutSize D t` — `t` is `τ`, the minimum size of a dicut.

## Design decisions an audit should check

**Arcs are an indexed family, not a set of pairs.** A digraph is `tail, head : Fin m → Fin n`,
so an arc *is* its index `a : Fin m`. Two arcs with the same endpoints are different elements of
`Fin m`, i.e. **parallel arcs stay distinct**, and arc sets `Fin m → Bool` can contain one
parallel arc without the other. Modelling `A` as a set of pairs `Fin n × Fin n` would silently
identify parallel arcs and change the problem.

**Vertex subsets are `Fin n → Bool`, arc subsets `Fin m → Bool`**, both quantified over
unrestrictedly — `∀ U : Fin n → Bool` really is "for every subset of `V`". The `Decidable`
instances below are what make the concrete instances in `Verified/Woodall/Instances.lean`
`decide`-checkable; they are *proved* equivalent to the quantified statements
(`decidable_of_iff` against `mem_allVertexSets`), so `decide` checks the real statement and not
an enumeration that might be incomplete.

**`IsDicutShore` also records that `U` is nonempty and proper.** Those two conditions are in
the README's definition and are implied by `δ⁺(U) ≠ ∅` (`nonempty_and_proper_of_isDicutShore`),
so stating them costs nothing and removes a reading in which they were quietly dropped.

**`τ` is `Option`-valued when phrased computably** (`tau?`): a digraph with no dicut at all —
the directed cycle, or any strongly connected digraph — has no minimum dicut size, and then
*every* arc set is vacuously a dijoin and no bound on disjoint dijoins exists. `IsMinDicutSize`
carries the existence of a dicut as a hypothesis for exactly this reason. The two are **proved
equal** by `tau?_eq_some_iff` and `tau?_eq_none_iff` below; before those existed, a fact about
`tau?` was a fact about `min?` of a filtered enumeration and said nothing about `τ`.

This file deliberately depends on Lean core only (no `Mathlib` import): the definitions need
nothing beyond `List`, `Fin` and `Bool`, and keeping the import empty keeps kernel reduction
cheap enough for `decide` on the concrete instances.
-/

namespace Verified.Woodall

/-! ## Finite enumerations

Everything is finite, so each quantifier below is backed by a list that provably contains every
element of the type being quantified over. These lists are the only reason `decide` works. -/

/-- Every index of `Fin m`, used to enumerate arcs. -/
def allArcs (m : Nat) : List (Fin m) := List.finRange m

@[simp] theorem mem_allArcs {m : Nat} (a : Fin m) : a ∈ allArcs m := by
  simp [allArcs]

@[simp] theorem length_allArcs (m : Nat) : (allArcs m).length = m := by
  simp [allArcs]

/-- Prepend a membership bit: `consB b U` is the subset of `Fin (n+1)` containing `0` iff `b`,
and containing `i.succ` iff `U i`. Written by hand rather than via `Fin.cons` so that the
kernel reduces it cheaply during `decide`. -/
def consB {n : Nat} (b : Bool) (U : Fin n → Bool) : Fin (n + 1) → Bool :=
  fun i => if h : i.val = 0 then b else U ⟨i.val - 1, by omega⟩

/-- Every subset of `Fin n`, as a list of `Fin n → Bool`. Has length `2 ^ n`. -/
def allVertexSets : (n : Nat) → List (Fin n → Bool)
  | 0 => [fun i => i.elim0]
  | n + 1 => (allVertexSets n).flatMap fun U => [consB false U, consB true U]

/-- The enumeration of subsets is complete: this is what lets `decide` on
`∀ U : Fin n → Bool, _` be a proof of the honest, unrestricted statement. -/
theorem mem_allVertexSets : ∀ {n : Nat} (U : Fin n → Bool), U ∈ allVertexSets n
  | 0, U => by
      have : U = fun i => i.elim0 := funext fun i => i.elim0
      simp [allVertexSets, this]
  | n + 1, U => by
      have hsplit : U = consB (U 0) (fun i => U i.succ) := by
        funext i
        by_cases h : i.val = 0
        · have : i = 0 := Fin.ext (by simpa using h)
          simp [consB, this]
        · have : (⟨i.val - 1, by omega⟩ : Fin n).succ = i := Fin.ext (by simp; omega)
          simp [consB, h, this]
      have hmem := mem_allVertexSets (fun i => U i.succ)
      rw [hsplit]
      simp only [allVertexSets, List.mem_flatMap]
      exact ⟨_, hmem, by cases U 0 <;> simp⟩

instance decidableForallVertexSet {n : Nat} (p : (Fin n → Bool) → Prop) [DecidablePred p] :
    Decidable (∀ U : Fin n → Bool, p U) :=
  decidable_of_iff (∀ U ∈ allVertexSets n, p U)
    ⟨fun h U => h U (mem_allVertexSets U), fun h U _ => h U⟩

instance decidableExistsVertexSet {n : Nat} (p : (Fin n → Bool) → Prop) [DecidablePred p] :
    Decidable (∃ U : Fin n → Bool, p U) :=
  decidable_of_iff (∃ U ∈ allVertexSets n, p U)
    ⟨fun ⟨U, _, hU⟩ => ⟨U, hU⟩, fun ⟨U, hU⟩ => ⟨U, mem_allVertexSets U, hU⟩⟩

instance decidableExistsFin {m : Nat} (p : Fin m → Prop) [DecidablePred p] :
    Decidable (∃ a : Fin m, p a) :=
  decidable_of_iff (∃ a ∈ allArcs m, p a)
    ⟨fun ⟨a, _, ha⟩ => ⟨a, ha⟩, fun ⟨a, ha⟩ => ⟨a, mem_allArcs a, ha⟩⟩

/-! ## Digraphs -/

/-- A finite digraph on the vertex set `Fin n` with arcs indexed by `Fin m`.

An arc *is* its index, so `tail` and `head` may agree on two different indices: **parallel arcs
are distinct arcs**, which is essential — Woodall's conjecture partitions the arc *family* `A`,
and a digraph with two parallel arcs is not the same instance as the one with a single arc. -/
structure Digraph (n m : Nat) where
  /-- The vertex an arc leaves. -/
  tail : Fin m → Fin n
  /-- The vertex an arc enters. -/
  head : Fin m → Fin n

/-- Build a digraph from a **list** of arcs, indexed by position in the list. Listing the same
pair twice therefore gives two genuinely distinct parallel arcs. -/
def Digraph.ofArcList {n : Nat} (arcs : List (Fin n × Fin n)) : Digraph n arcs.length where
  tail := fun a => (arcs.get a).1
  head := fun a => (arcs.get a).2

/-- A set of vertices. -/
abbrev VertexSet (n : Nat) := Fin n → Bool

/-- A set of arcs. -/
abbrev ArcSet (m : Nat) := Fin m → Bool

variable {n m : Nat}

/-- `δ⁺(U)`: the arcs leaving `U` — tail inside `U`, head outside. -/
def deltaOut (D : Digraph n m) (U : VertexSet n) : ArcSet m :=
  fun a => U (D.tail a) && !U (D.head a)

/-- `δ⁻(U)`: the arcs entering `U` — tail outside `U`, head inside. -/
def deltaIn (D : Digraph n m) (U : VertexSet n) : ArcSet m :=
  fun a => !U (D.tail a) && U (D.head a)

/-- `U` is a **shore of a dicut**: no arc enters `U`, and at least one arc leaves it. The dicut
itself is the arc set `deltaOut D U`.

The `∀ a, deltaIn D U a = false` conjunct is the whole content of the word *di*cut and is the
condition problem `RULES.md` §4 warns is routinely omitted. The nonemptiness and properness of
`U` are recorded explicitly even though they follow from `δ⁺(U) ≠ ∅`
(`nonempty_and_proper_of_isDicutShore`). -/
def IsDicutShore (D : Digraph n m) (U : VertexSet n) : Prop :=
  (∀ a, deltaIn D U a = false) ∧ (∃ a, deltaOut D U a = true)

instance (D : Digraph n m) (U : VertexSet n) : Decidable (IsDicutShore D U) := by
  unfold IsDicutShore; infer_instance

/-- A dicut shore is a nonempty proper subset of the vertices, so no degenerate `U = ∅` or
`U = V` sneaks in. Stated to show the extra conditions in the README's definition are not
missing from `IsDicutShore`, merely implied. -/
theorem nonempty_and_proper_of_isDicutShore {D : Digraph n m} {U : VertexSet n}
    (h : IsDicutShore D U) : (∃ v, U v = true) ∧ (∃ v, U v = false) := by
  obtain ⟨_, a, ha⟩ := h
  simp only [deltaOut, Bool.and_eq_true, Bool.not_eq_true'] at ha
  exact ⟨⟨D.tail a, ha.1⟩, ⟨D.head a, ha.2⟩⟩

/-- `J` meets the arc set `S`. -/
def Meets (S J : ArcSet m) : Prop := ∃ a, S a = true ∧ J a = true

instance (S J : ArcSet m) : Decidable (Meets S J) := by unfold Meets; infer_instance

/-- A **dijoin**: a set of arcs meeting every dicut at least once.

Note the quantifier is over *all* `U : VertexSet n`, filtered by `IsDicutShore`; there is no
enumeration or restriction hiding here. In a digraph with no dicut every arc set is vacuously a
dijoin, which is the correct reading of the definition. -/
def IsDijoin (D : Digraph n m) (J : ArcSet m) : Prop :=
  ∀ U : VertexSet n, IsDicutShore D U → Meets (deltaOut D U) J

instance (D : Digraph n m) (J : ArcSet m) : Decidable (IsDijoin D J) := by
  unfold IsDijoin; infer_instance

/-- Two arc sets share no arc. -/
def ArcDisjoint (J K : ArcSet m) : Prop := ∀ a, ¬(J a = true ∧ K a = true)

instance (J K : ArcSet m) : Decidable (ArcDisjoint J K) := by
  unfold ArcDisjoint; infer_instance

/-- The number of arcs in an arc set. -/
def card (S : ArcSet m) : Nat := (allArcs m).countP S

/-- `t` is `τ(D)`: the minimum size of a dicut of `D`. The first conjunct says the minimum is
attained (in particular `D` *has* a dicut); the second says it is a lower bound. -/
def IsMinDicutSize (D : Digraph n m) (t : Nat) : Prop :=
  (∃ U : VertexSet n, IsDicutShore D U ∧ card (deltaOut D U) = t) ∧
    (∀ U : VertexSet n, IsDicutShore D U → t ≤ card (deltaOut D U))

instance (D : Digraph n m) (t : Nat) : Decidable (IsMinDicutSize D t) := by
  unfold IsMinDicutSize; infer_instance

/-- The shores of the dicuts of `D`, as a list. -/
def dicutShores (D : Digraph n m) : List (VertexSet n) :=
  (allVertexSets n).filter fun U => decide (IsDicutShore D U)

/-- The sizes of the dicuts of `D`. -/
def dicutSizes (D : Digraph n m) : List Nat :=
  (dicutShores D).map fun U => card (deltaOut D U)

/-- `τ(D)` computed: `none` exactly when `D` has no dicut. -/
def tau? (D : Digraph n m) : Option Nat := (dicutSizes D).min?

/-- The arc set given by a list of arc indices. -/
def arcSetOf {m : Nat} (l : List Nat) : ArcSet m := fun a => l.contains a.val

/-! ## Bridging the two definitions of `τ`

`IsMinDicutSize` (relational) and `tau?` (computed) are two separate definitions of the same
quantity, and until the theorems below existed nothing was entitled to read `tau?` as `τ`: a
`decide`-checked fact about `tau?` said something about `min?` of a filtered enumeration, not
about the minimum dicut size. `tau?_eq_some_iff` closes that gap, so the two may be used
interchangeably from here on.

The bridge is an `↔` at `some t`, not an equation between a `Nat` and a `Nat`, because `tau?` is
`Option`-valued: `none` is the honest value for a digraph with no dicut, and `IsMinDicutSize`
holds of no `t` there. `tau?_eq_none_iff` is the matching statement for that case, so the two
definitions are related on the whole of their domains and not merely where both are defined. -/

/-- The enumeration `dicutShores` lists exactly the dicut shores — no shore is missed and
nothing else is included. This is where the completeness of `allVertexSets` enters. -/
@[simp] theorem mem_dicutShores {D : Digraph n m} {U : VertexSet n} :
    U ∈ dicutShores D ↔ IsDicutShore D U := by
  simp [dicutShores, List.mem_filter, mem_allVertexSets]

/-- Hence `dicutSizes` lists exactly the sizes of dicuts. -/
theorem mem_dicutSizes {D : Digraph n m} {t : Nat} :
    t ∈ dicutSizes D ↔ ∃ U : VertexSet n, IsDicutShore D U ∧ card (deltaOut D U) = t := by
  simp [dicutSizes, List.mem_map, mem_dicutShores]

/-- **The bridge: the computed `τ` is the relational `τ`.** `tau? D = some t` holds for exactly
the `t` that `IsMinDicutSize D t` holds of.

Both halves of `IsMinDicutSize` are needed and both are supplied by `min?`: membership of the
minimum in the list gives the attaining shore, and its minimality gives the lower bound over
*all* shores, which is a genuine quantification over every `U : VertexSet n` because
`mem_allVertexSets` says the enumeration is complete. -/
theorem tau?_eq_some_iff {D : Digraph n m} {t : Nat} :
    tau? D = some t ↔ IsMinDicutSize D t := by
  rw [tau?, List.min?_eq_some_iff]
  constructor
  · rintro ⟨hmem, hle⟩
    exact ⟨mem_dicutSizes.1 hmem, fun U hU => hle _ (mem_dicutSizes.2 ⟨U, hU, rfl⟩)⟩
  · rintro ⟨hex, hle⟩
    refine ⟨mem_dicutSizes.2 hex, ?_⟩
    rintro b hb
    obtain ⟨U, hU, rfl⟩ := mem_dicutSizes.1 hb
    exact hle U hU

/-- The other half of the bridge: `tau?` is `none` exactly when the digraph has no dicut at all,
which is exactly when no `t` satisfies `IsMinDicutSize`. -/
theorem tau?_eq_none_iff {D : Digraph n m} :
    tau? D = none ↔ ∀ U : VertexSet n, ¬ IsDicutShore D U := by
  rw [tau?, List.min?_eq_none_iff]
  constructor
  · intro h U hU
    have hmem : card (deltaOut D U) ∈ dicutSizes D := mem_dicutSizes.2 ⟨U, hU, rfl⟩
    rw [h] at hmem
    exact absurd hmem (by simp)
  · intro h
    rw [List.eq_nil_iff_forall_not_mem]
    intro t ht
    obtain ⟨U, hU, -⟩ := mem_dicutSizes.1 ht
    exact h U hU

/-- A digraph with no dicut has no minimum dicut size, for **every** natural number — the
unbounded statement, with no `decide`-imposed range restriction. -/
theorem not_isMinDicutSize_of_no_dicut {D : Digraph n m}
    (h : ∀ U : VertexSet n, ¬ IsDicutShore D U) (t : Nat) : ¬ IsMinDicutSize D t := by
  rintro ⟨⟨U, hU, -⟩, -⟩
  exact h U hU

/-- Consequently `tau? D = none` is equivalent to `τ` being undefined, stated directly on
`IsMinDicutSize` rather than on the shores. -/
theorem tau?_eq_none_iff_not_exists {D : Digraph n m} :
    tau? D = none ↔ ¬ ∃ t : Nat, IsMinDicutSize D t := by
  constructor
  · rintro h ⟨t, ht⟩
    have := tau?_eq_some_iff.2 ht
    rw [h] at this
    exact absurd this (by simp)
  · intro h
    cases hd : tau? D with
    | none => rfl
    | some t => exact absurd ⟨t, tau?_eq_some_iff.1 hd⟩ h

/-! ## Counting

Two elementary list lemmas; nothing here is specific to digraphs. -/

/-- Erasing an element that is present and counted drops the count by exactly one. -/
theorem countP_erase_of_mem {α : Type _} [DecidableEq α] (S : α → Bool) :
    ∀ (l : List α) (a : α), a ∈ l → S a = true → l.countP S = (l.erase a).countP S + 1
  | [], a, ha, _ => absurd ha (by simp)
  | b :: t, a, ha, hSa => by
      by_cases hba : b = a
      · subst hba
        simp [hSa]
      · have hat : a ∈ t := by
          rcases List.mem_cons.1 ha with h | h
          · exact absurd h.symm hba
          · exact h
        have hne : ¬ (b == a) = true := by simpa using hba
        rw [List.erase_cons_tail (by simpa using hne)]
        rw [List.countP_cons, List.countP_cons, countP_erase_of_mem S t a hat hSa]
        omega

/-- **The counting core of the easy direction.** Pairwise disjoint sets that each meet `S`
somewhere inside `l` cannot outnumber the elements of `l` that `S` contains.

The proof is the obvious one: the head of `Js` grabs an element `a` of `S ∩ l`; disjointness
forces every later member to meet `S ∩ (l.erase a)`; induct. -/
theorem length_le_countP {α : Type _} [DecidableEq α] (S : α → Bool) :
    ∀ (Js : List (α → Bool)) (l : List α),
      (∀ J ∈ Js, ∃ a, a ∈ l ∧ S a = true ∧ J a = true) →
      Js.Pairwise (fun J K => ∀ a, ¬(J a = true ∧ K a = true)) →
      Js.length ≤ l.countP S
  | [], _, _, _ => Nat.zero_le _
  | J :: rest, l, hmeet, hdisj => by
      obtain ⟨a, hal, hSa, hJa⟩ := hmeet J (List.mem_cons_self ..)
      obtain ⟨hhead, htail⟩ := List.pairwise_cons.1 hdisj
      have hrest : ∀ K ∈ rest, ∃ b, b ∈ l.erase a ∧ S b = true ∧ K b = true := by
        intro K hK
        obtain ⟨b, hbl, hSb, hKb⟩ := hmeet K (List.mem_cons_of_mem _ hK)
        have hba : b ≠ a := by
          rintro rfl
          exact hhead K hK b ⟨hJa, hKb⟩
        exact ⟨b, (List.mem_erase_of_ne hba).2 hbl, hSb, hKb⟩
      have ih := length_le_countP S rest (l.erase a) hrest htail
      rw [countP_erase_of_mem S l a hal hSa]
      simpa using Nat.succ_le_succ ih

/-! ## The easy direction

Read the warning. -/

/--
**THE TRIVIAL HALF OF WOODALL'S CONJECTURE. THIS IS NOT PROGRESS ON WOODALL.**

Any family of pairwise arc-disjoint dijoins has at most `card (deltaOut D U)` members, for every
dicut `δ⁺(U)`. Each dijoin must use up an arc of that dicut and they use different arcs, so
there are at most as many dijoins as dicut arcs. That is the entire argument; it was already
stated in one line of `problems/woodalls-conjecture/README.md`.

Woodall's conjecture is the **existence** direction: that `A` can be *partitioned into `τ`
dijoins*. That statement is not proved, not stated, and not assumed anywhere in this
development. `problems/woodalls-conjecture/README.md`: "The conjecture is the existence
direction, and any 'proof' that only establishes the easy inequality has proved nothing."
-/
theorem length_le_card_deltaOut (D : Digraph n m) (Js : List (ArcSet m))
    (hJ : ∀ J ∈ Js, IsDijoin D J) (hd : Js.Pairwise ArcDisjoint)
    (U : VertexSet n) (hU : IsDicutShore D U) :
    Js.length ≤ card (deltaOut D U) := by
  refine length_le_countP (deltaOut D U) Js (allArcs m) ?_ hd
  intro J hJmem
  obtain ⟨a, ha, hJa⟩ := hJ J hJmem U hU
  exact ⟨a, mem_allArcs a, ha, hJa⟩

/--
**Still the trivial half.** At most `τ` pairwise arc-disjoint dijoins. Woodall asserts that `τ`
of them exist and partition `A`; that is untouched here.
-/
theorem length_le_tau (D : Digraph n m) (t : Nat) (ht : IsMinDicutSize D t)
    (Js : List (ArcSet m)) (hJ : ∀ J ∈ Js, IsDijoin D J) (hd : Js.Pairwise ArcDisjoint) :
    Js.length ≤ t := by
  obtain ⟨⟨U, hU, hUcard⟩, _⟩ := ht
  have := length_le_card_deltaOut D Js hJ hd U hU
  omega

/-! ## The conjecture itself, and the degenerate range `τ ≤ 1`

Stated, never assumed and never proved. -/

/-- The arc sets `Js` **partition** the arcs of the digraph: every arc lies in exactly one
member. This is the literal reading of `problems/woodalls-conjecture/README.md` ("the arc set
`A` can be partitioned into `τ` disjoint dijoins"), and it is strictly more than a *packing* of
pairwise-disjoint dijoins, which need not cover `A`. The two forms are equivalent because a
superset of a dijoin is again a dijoin (`IsDijoin.mono`), so leftover arcs can be handed to any
member; that equivalence is proved, not assumed. -/
def IsArcPartition {m : Nat} (Js : List (ArcSet m)) : Prop :=
  ∀ a : Fin m, (Js.countP fun J => J a) = 1

/-- A superset of a dijoin is a dijoin. -/
theorem IsDijoin.mono {D : Digraph n m} {J K : ArcSet m} (hJ : IsDijoin D J)
    (hJK : ∀ a, J a = true → K a = true) : IsDijoin D K := by
  intro U hU
  obtain ⟨a, ha, hJa⟩ := hJ U hU
  exact ⟨a, ha, hJK a hJa⟩

/--
**WOODALL'S CONJECTURE.** For every `t` that is the minimum dicut size `τ(D)`, the arcs of `D`
can be partitioned into `t` dijoins.

This is a `Prop`. **It is not proved anywhere in this development, and nothing here may assume
it.** The only theorem about it below covers `τ ≤ 1`, which is degenerate.

Faithfulness notes for an audit:

* The quantifier is over *all* digraphs when the statement is applied — `Digraph n m` ranges
  over every finite digraph, with arcs an indexed family so **parallel arcs are distinct**.
* `IsArcPartition` demands a genuine partition of `A`, matching the README, not merely a
  disjoint family.
* A digraph with no dicut satisfies this vacuously, which is correct: there is then no `t` with
  `IsMinDicutSize D t`, and indeed arbitrarily many disjoint dijoins exist.
-/
def WoodallConjecture (D : Digraph n m) : Prop :=
  ∀ t : Nat, IsMinDicutSize D t →
    ∃ Js : List (ArcSet m), Js.length = t ∧ (∀ J ∈ Js, IsDijoin D J) ∧ IsArcPartition Js

/-- A dicut has at least one arc, because `IsDicutShore` requires `δ⁺(U) ≠ ∅`. -/
theorem one_le_card_deltaOut {D : Digraph n m} {U : VertexSet n} (hU : IsDicutShore D U) :
    1 ≤ card (deltaOut D U) := by
  obtain ⟨-, a, ha⟩ := hU
  have : 0 < (allArcs m).countP (deltaOut D U) :=
    List.countP_pos_iff.2 ⟨a, mem_allArcs a, ha⟩
  simpa [card] using this

/-- Hence `τ = 0` is impossible under this file's convention. Under the alternative convention
that admits the empty set as a dicut (see `IsDicutShoreAllowingEmpty`) it is possible, and then
the digraph has no dijoin at all — the two conventions genuinely disagree, which is why the
choice is stated rather than assumed. -/
theorem not_isMinDicutSize_zero (D : Digraph n m) : ¬ IsMinDicutSize D 0 := by
  rintro ⟨⟨U, hU, hcard⟩, -⟩
  have := one_le_card_deltaOut hU
  omega

/-- `τ` is well defined: at most one number is the minimum dicut size. -/
theorem isMinDicutSize_unique {D : Digraph n m} {s t : Nat}
    (hs : IsMinDicutSize D s) (ht : IsMinDicutSize D t) : s = t := by
  obtain ⟨⟨U, hU, hUc⟩, hsle⟩ := hs
  obtain ⟨⟨W, hW, hWc⟩, htle⟩ := ht
  have h1 := hsle W hW
  have h2 := htle U hU
  omega

/-- The full arc set is a dijoin, since every dicut is nonempty by convention. -/
theorem isDijoin_all (D : Digraph n m) : IsDijoin D (fun _ => true) := by
  intro U hU
  obtain ⟨-, a, ha⟩ := hU
  exact ⟨a, ha, rfl⟩

/--
**Woodall's conjecture holds when `τ(D) = 1`** — put every arc in the single dijoin `A`.

This is degenerate and is *not* progress: it is the `τ = 1` corner, not the `τ = 2` folklore
theorem and certainly not the conjecture. It is recorded only so the conjecture statement is
exercised on a case where it is provable, which guards against `WoodallConjecture` being
accidentally unsatisfiable.
-/
theorem woodall_of_isMinDicutSize_one {D : Digraph n m} (h : IsMinDicutSize D 1) :
    WoodallConjecture D := by
  intro t ht
  have hts : t = 1 := isMinDicutSize_unique ht h
  subst hts
  refine ⟨[fun _ => true], rfl, ?_, ?_⟩
  · intro J hJ
    rcases List.mem_cons.1 hJ with rfl | hJ
    · exact isDijoin_all D
    · exact absurd hJ (by simp)
  · intro a; simp

/-- **Woodall's conjecture holds whenever `τ(D) ≤ 1`.** `τ = 0` cannot occur here, so this is
just the `τ = 1` case. Still degenerate; still not progress. -/
theorem woodall_of_isMinDicutSize_le_one {D : Digraph n m} {t : Nat} (h : IsMinDicutSize D t)
    (ht : t ≤ 1) : WoodallConjecture D := by
  match t, ht with
  | 0, _ => exact absurd h (not_isMinDicutSize_zero D)
  | 1, _ => exact woodall_of_isMinDicutSize_one h

/-! ## The rejected alternative convention

Recorded so that the divergence from the earlier, superseded branch
`origin/claude/76-lean-woodall` is visible rather than silent. -/

/-- The alternative reading of "dicut" used on the superseded branch: `U` nonempty and proper
with `δ⁻(U) = ∅`, but `δ⁺(U)` allowed to be **empty**. On a weakly connected digraph the two
readings coincide; on a disconnected one they do not, and
`Verified/Woodall/Instances.lean` exhibits a digraph where they disagree. -/
def IsDicutShoreAllowingEmpty (D : Digraph n m) (U : VertexSet n) : Prop :=
  (∃ v, U v = true) ∧ (∃ v, U v = false) ∧ (∀ a, deltaIn D U a = false)

instance (D : Digraph n m) (U : VertexSet n) : Decidable (IsDicutShoreAllowingEmpty D U) := by
  unfold IsDicutShoreAllowingEmpty; infer_instance

/-- This file's convention is the stronger one: every dicut shore is one under the permissive
reading too. -/
theorem isDicutShoreAllowingEmpty_of_isDicutShore {D : Digraph n m} {U : VertexSet n}
    (h : IsDicutShore D U) : IsDicutShoreAllowingEmpty D U := by
  obtain ⟨hne, hprop⟩ := nonempty_and_proper_of_isDicutShore h
  exact ⟨hne, hprop, h.1⟩

end Verified.Woodall
