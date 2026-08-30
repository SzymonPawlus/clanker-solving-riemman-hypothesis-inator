/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: codex
-/
import Mathlib.Analysis.Complex.Basic
import Mathlib.Data.ENNReal.Basic
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Topology.Order.OrderClosed

/-!
# Vanishing critical 2-variation: verified elementary core

This module formalizes only algebraic and finite-sum components of the proposed
`C^{0,2-var}` Square Peg argument. It does not assert the Square Peg theorem.
The independently source-verified analytic approximation criterion and its
four-distinct/off-diagonal conclusion are kept as separate proposition
parameters in `conditional_positive_square`: this module checks the logical
composition but does not formalize those external analytic theorems.
-/

namespace Verified.SquarePeg.C02Var

/-- Squared increment sum of a finite sampled path. This is the finite object
whose supremum defines 2-variation. -/
def sqIncrementSum {E : Type*} [SeminormedAddCommGroup E] {n : ℕ}
    (x : Fin (n + 1) → E) : ℝ :=
  ∑ i : Fin n, ‖x i.succ - x i.castSucc‖ ^ 2

/-- Every finite squared increment sum is nonnegative. -/
lemma sqIncrementSum_nonneg {E : Type*} [SeminormedAddCommGroup E] {n : ℕ}
    (x : Fin (n + 1) → E) : 0 ≤ sqIncrementSum x := by
  exact Finset.sum_nonneg fun _ _ ↦ sq_nonneg _

/-- A finite ordered partition of `[a,b]`, including both endpoints. -/
structure OrderedPartition (a b : ℝ) (n : ℕ) where
  points : Fin (n + 1) → ℝ
  strictMono : StrictMono points
  left : points 0 = a
  right : points (Fin.last n) = b

/-- Every gap of the partition is at most `δ`. This predicate avoids choosing
a junk value for the maximum of an empty family. -/
def OrderedPartition.IsMeshLE {a b : ℝ} {n : ℕ}
    (P : OrderedPartition a b n) (δ : ℝ) : Prop :=
  ∀ i : Fin n, P.points i.succ - P.points i.castSucc ≤ δ

/-- Squared increment energy of a path sampled on an ordered partition. -/
def partitionEnergy {E : Type*} [SeminormedAddCommGroup E]
    (x : ℝ → E) {a b : ℝ} {n : ℕ} (P : OrderedPartition a b n) : ENNReal :=
  ENNReal.ofReal (sqIncrementSum fun i ↦ x (P.points i))

/-- Fine-mesh squared 2-variation as the supremum over all finite ordered
partitions whose gaps are at most `δ`. This is the square of the paper's
`w₂`; the codomain records possible infinity. -/
noncomputable def fineEVariationSq {E : Type*} [SeminormedAddCommGroup E]
    (x : ℝ → E) (a b δ : ℝ) : ENNReal :=
  ⨆ (n : ℕ) (P : OrderedPartition a b n) (_h : P.IsMeshLE δ), partitionEnergy x P

/-- Every admissible partition energy is bounded by the fine squared
variation at the same mesh scale. -/
lemma partitionEnergy_le_fineEVariationSq {E : Type*} [SeminormedAddCommGroup E]
    (x : ℝ → E) {a b δ : ℝ} {n : ℕ} (P : OrderedPartition a b n)
    (hP : P.IsMeshLE δ) :
    partitionEnergy x P ≤ fineEVariationSq x a b δ := by
  unfold fineEVariationSq
  exact le_iSup_of_le n <| le_iSup_of_le P <| le_iSup_of_le hP le_rfl

/-- Allowing a larger mesh can only increase the fine squared variation. -/
lemma fineEVariationSq_mono_mesh {E : Type*} [SeminormedAddCommGroup E]
    (x : ℝ → E) (a b : ℝ) : Monotone (fineEVariationSq x a b) := by
  intro δ ε hδε
  unfold fineEVariationSq
  refine iSup_le fun n ↦ iSup_le fun P ↦ iSup_le fun hP ↦ ?_
  have hPε : P.IsMeshLE ε := fun i ↦ (hP i).trans hδε
  exact le_iSup_of_le n <| le_iSup_of_le P <| le_iSup_of_le hPε le_rfl

/-- The partition of `[a,b]` into `k` equal parameter intervals. -/
noncomputable def equispacedPartition {a b : ℝ} (hab : a < b) (k : ℕ)
    (hk : 0 < k) : OrderedPartition a b k where
  points i := a + ((i : ℝ) / k) * (b - a)
  strictMono := by
    intro i j hij
    have hijR : (i : ℝ) < (j : ℝ) := by exact_mod_cast hij
    have hkR : (0 : ℝ) < k := by exact_mod_cast hk
    simpa [add_comm] using add_lt_add_left
      (mul_lt_mul_of_pos_right (div_lt_div_of_pos_right hijR hkR) (sub_pos.mpr hab)) a
  left := by simp
  right := by
    simp only [Fin.last, Fin.val_mk]
    have hkR : (k : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt hk)
    field_simp
    ring

/-- Every gap of the equispaced partition is exactly `(b-a)/k`. -/
lemma equispacedPartition_gap {a b : ℝ} (hab : a < b) (k : ℕ) (hk : 0 < k)
    (i : Fin k) :
    (equispacedPartition hab k hk).points i.succ -
      (equispacedPartition hab k hk).points i.castSucc = (b - a) / k := by
  simp only [equispacedPartition, Fin.val_succ, Fin.val_castSucc]
  push_cast
  have hkR : (k : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt hk)
  field_simp
  ring

/-- Every nondegenerate real interval has an equispaced finite partition with
mesh at most any prescribed positive `δ`. -/
lemma exists_equispacedPartition_mesh_le {a b δ : ℝ} (hab : a < b) (hδ : 0 < δ) :
    ∃ (k : ℕ) (_hk : 0 < k) (P : OrderedPartition a b k), P.IsMeshLE δ := by
  obtain ⟨k, hkBig⟩ := exists_nat_gt ((b - a) / δ)
  have hratio : 0 < (b - a) / δ := div_pos (sub_pos.mpr hab) hδ
  have hkR : (0 : ℝ) < k := hratio.trans hkBig
  have hk : 0 < k := by exact_mod_cast hkR
  refine ⟨k, hk, equispacedPartition hab k hk, ?_⟩
  intro i
  rw [equispacedPartition_gap]
  have hmul : b - a < (k : ℝ) * δ := (div_lt_iff₀ hδ).mp hkBig
  exact le_of_lt ((div_lt_iff₀ hkR).2 (by nlinarith))

/-- The unique one-point partition of a degenerate interval. -/
def singletonPartition (a : ℝ) : OrderedPartition a a 0 where
  points _ := a
  strictMono := by intro i j hij; omega
  left := rfl
  right := rfl

/-- Every nonempty interval admits a finite partition at every positive mesh
scale, including the degenerate singleton case. -/
lemma exists_partition_mesh_le {a b δ : ℝ} (hab : a ≤ b) (hδ : 0 < δ) :
    ∃ (n : ℕ) (P : OrderedPartition a b n), P.IsMeshLE δ := by
  rcases hab.eq_or_lt with rfl | hablt
  · exact ⟨0, singletonPartition a, fun i ↦ Fin.elim0 i⟩
  · obtain ⟨k, _hk, P, hP⟩ := exists_equispacedPartition_mesh_le hablt hδ
    exact ⟨k, P, hP⟩

/-- Point array obtained by concatenating two partitions and dropping the
second copy of their common endpoint. -/
def concatPoints {a b c : ℝ} {m n : ℕ}
    (P : OrderedPartition a b m) (Q : OrderedPartition b c n) :
    Fin (m + n + 1) → ℝ :=
  (Fin.append P.points (fun i : Fin n ↦ Q.points i.succ)) ∘ Fin.cast (by omega)

/-- Evaluation of concatenated points on the left partition. -/
@[simp] lemma concatPoints_left {a b c : ℝ} {m n : ℕ}
    (P : OrderedPartition a b m) (Q : OrderedPartition b c n) (i : Fin (m + 1)) :
    concatPoints P Q (Fin.castLE (by omega) i) = P.points i := by
  simp [concatPoints, Function.comp_apply]

/-- Evaluation of concatenated points on the right partition after its
repeated initial endpoint has been removed. -/
@[simp] lemma concatPoints_right {a b c : ℝ} {m n : ℕ}
    (P : OrderedPartition a b m) (Q : OrderedPartition b c n) (i : Fin n) :
    concatPoints P Q ⟨m + 1 + i, by omega⟩ = Q.points i.succ := by
  simp [concatPoints, Function.comp_apply, Fin.append, Fin.addCases]
  omega

/-- Concatenated points are strictly increasing. -/
lemma concatPoints_strictMono {a b c : ℝ} {m n : ℕ}
    (P : OrderedPartition a b m) (Q : OrderedPartition b c n) :
    StrictMono (concatPoints P Q) := by
  rw [Fin.strictMono_iff_lt_succ]
  intro i
  by_cases hleft : i.val < m
  · let pi : Fin (m + 1) := ⟨i.val, by omega⟩
    let pj : Fin (m + 1) := ⟨i.val + 1, by omega⟩
    rw [show i.castSucc = Fin.castLE (by omega) pi by ext; simp [pi],
      show i.succ = Fin.castLE (by omega) pj by ext; simp [pj]]
    simpa using P.strictMono (show pi < pj by simp [pi, pj])
  · by_cases hjoint : i.val = m
    · have hn : 0 < n := by omega
      let q0 : Fin n := ⟨0, hn⟩
      let pm : Fin (m + 1) := Fin.last m
      rw [show i.castSucc = Fin.castLE (by omega) pm by ext; simp [pm, hjoint],
        show i.succ = ⟨m + 1 + q0.val, by omega⟩ by ext; simp [q0, hjoint]]
      rw [concatPoints_left, concatPoints_right, P.right]
      calc
        b = Q.points 0 := Q.left.symm
        _ < Q.points q0.succ :=
          Q.strictMono (by simpa [q0] using q0.castSucc_lt_succ)
    · have hright : m < i.val := by omega
      let qi : Fin n := ⟨i.val - (m + 1), by omega⟩
      let qj : Fin n := ⟨i.val + 1 - (m + 1), by omega⟩
      rw [show i.castSucc = ⟨m + 1 + qi.val, by omega⟩ by ext; simp [qi]; omega,
        show i.succ = ⟨m + 1 + qj.val, by omega⟩ by ext; simp [qj]; omega]
      rw [concatPoints_right, concatPoints_right]
      exact Q.strictMono (show qi.succ < qj.succ by simp [qi, qj]; omega)

/-- Concatenation of ordered partitions, with the repeated joint retained only
once. -/
def OrderedPartition.concat {a b c : ℝ} {m n : ℕ}
    (P : OrderedPartition a b m) (Q : OrderedPartition b c n) :
    OrderedPartition a c (m + n) where
  points := concatPoints P Q
  strictMono := concatPoints_strictMono P Q
  left := by
    exact (concatPoints_left P Q (0 : Fin (m + 1))).trans P.left
  right := by
    cases n with
    | zero =>
        have hbc : b = c := Q.left.symm.trans Q.right
        calc
          concatPoints P Q (Fin.last (m + 0)) = P.points (Fin.last m) := by
            rw [show Fin.last (m + 0) = Fin.castLE (by omega) (Fin.last m) by ext; simp]
            exact concatPoints_left P Q (Fin.last m)
          _ = b := P.right
          _ = c := hbc
    | succ n =>
        calc
          concatPoints P Q (Fin.last (m + (n + 1))) = Q.points (Fin.last n).succ := by
            rw [show Fin.last (m + (n + 1)) = ⟨m + 1 + (Fin.last n).val, by omega⟩ by
              ext; simp; omega]
            exact concatPoints_right P Q (Fin.last n)
          _ = c := Q.right

/-- Left-block edge endpoints of a concatenated partition. -/
lemma concat_edge_left {a b c : ℝ} {m n : ℕ}
    (P : OrderedPartition a b m) (Q : OrderedPartition b c n) (i : Fin m) :
    (P.concat Q).points (Fin.castAdd n i).castSucc = P.points i.castSucc ∧
      (P.concat Q).points (Fin.castAdd n i).succ = P.points i.succ := by
  constructor
  · rw [show (Fin.castAdd n i).castSucc = Fin.castLE (by omega) i.castSucc by ext; simp]
    exact concatPoints_left P Q i.castSucc
  · rw [show (Fin.castAdd n i).succ = Fin.castLE (by omega) i.succ by ext; simp]
    exact concatPoints_left P Q i.succ

/-- Right-block edge endpoints of a concatenated partition, including the
joint as the initial endpoint of the first right edge. -/
lemma concat_edge_right {a b c : ℝ} {m n : ℕ}
    (P : OrderedPartition a b m) (Q : OrderedPartition b c n) (i : Fin n) :
    (P.concat Q).points (Fin.natAdd m i).castSucc = Q.points i.castSucc ∧
      (P.concat Q).points (Fin.natAdd m i).succ = Q.points i.succ := by
  constructor
  · by_cases hi : i.val = 0
    · rw [show (Fin.natAdd m i).castSucc =
          Fin.castLE (by omega) (Fin.last m) by ext; simp [hi]]
      change concatPoints P Q _ = _
      rw [concatPoints_left, P.right]
      calc
        b = Q.points 0 := Q.left.symm
        _ = Q.points i.castSucc := by congr 1; ext; simpa using hi.symm
    · let j : Fin n := ⟨i.val - 1, by omega⟩
      rw [show (Fin.natAdd m i).castSucc =
          ⟨m + 1 + j.val, by omega⟩ by ext; simp [j]; omega]
      change concatPoints P Q _ = _
      rw [show i.castSucc = j.succ by ext; simp [j]; omega]
      exact concatPoints_right P Q j
  · rw [show (Fin.natAdd m i).succ = ⟨m + 1 + i.val, by omega⟩ by ext; simp; omega]
    exact concatPoints_right P Q i

/-- Concatenation preserves a common mesh upper bound. -/
lemma OrderedPartition.concat_isMeshLE {a b c δ : ℝ} {m n : ℕ}
    {P : OrderedPartition a b m} {Q : OrderedPartition b c n}
    (hP : P.IsMeshLE δ) (hQ : Q.IsMeshLE δ) : (P.concat Q).IsMeshLE δ := by
  intro i
  refine Fin.addCases (m := m) (n := n) (fun j ↦ ?_) (fun j ↦ ?_) i
  · rw [(concat_edge_left P Q j).1, (concat_edge_left P Q j).2]
    exact hP j
  · rw [(concat_edge_right P Q j).1, (concat_edge_right P Q j).2]
    exact hQ j

/-- Squared increment sums add exactly under partition concatenation. -/
lemma sqIncrementSum_concatPoints {E : Type*} [SeminormedAddCommGroup E]
    (x : ℝ → E) {a b c : ℝ} {m n : ℕ}
    (P : OrderedPartition a b m) (Q : OrderedPartition b c n) :
    sqIncrementSum (fun i ↦ x ((P.concat Q).points i)) =
      sqIncrementSum (fun i ↦ x (P.points i)) +
        sqIncrementSum (fun i ↦ x (Q.points i)) := by
  unfold sqIncrementSum
  rw [Fin.sum_univ_add]
  congr 1
  · apply Finset.sum_congr rfl
    intro i _
    simp only
    rw [(concat_edge_left P Q i).1, (concat_edge_left P Q i).2]
  · apply Finset.sum_congr rfl
    intro i _
    simp only
    rw [(concat_edge_right P Q i).1, (concat_edge_right P Q i).2]

/-- Partition energies add exactly under concatenation. -/
lemma partitionEnergy_concat {E : Type*} [SeminormedAddCommGroup E]
    (x : ℝ → E) {a b c : ℝ} {m n : ℕ}
    (P : OrderedPartition a b m) (Q : OrderedPartition b c n) :
    partitionEnergy x (P.concat Q) = partitionEnergy x P + partitionEnergy x Q := by
  unfold partitionEnergy
  rw [sqIncrementSum_concatPoints]
  rw [ENNReal.ofReal_add (sqIncrementSum_nonneg (fun i ↦ x (P.points i)))
    (sqIncrementSum_nonneg (fun i ↦ x (Q.points i)))]

/-- If the whole interval has length at most `δ`, every gap of any ordered
partition of that interval has length at most `δ`. -/
lemma OrderedPartition.isMeshLE_of_length_le {a b δ : ℝ} {n : ℕ}
    (P : OrderedPartition a b n) (h : b - a ≤ δ) : P.IsMeshLE δ := by
  intro i
  have hlo : a ≤ P.points i.castSucc := by
    calc
      a = P.points 0 := P.left.symm
      _ ≤ P.points i.castSucc := P.strictMono.monotone (Fin.zero_le _)
  have hhi : P.points i.succ ≤ b := by
    calc
      P.points i.succ ≤ P.points (Fin.last n) :=
        P.strictMono.monotone (Fin.le_last _)
      _ = b := P.right
  linarith

/-- Extend a partition of `[s,t]` to `[a,b]` by mesh-controlled left and
right fillers. The displayed energy equality retains both filler energies. -/
lemma exists_superinterval_extension {E : Type*} [SeminormedAddCommGroup E]
    (x : ℝ → E) {a s t b δ : ℝ} {n : ℕ} (P : OrderedPartition s t n)
    (has : a ≤ s) (_hst : s ≤ t) (htb : t ≤ b) (hδ : 0 < δ)
    (hP : P.IsMeshLE δ) :
    ∃ (l r : ℕ) (L : OrderedPartition a s l) (R : OrderedPartition t b r),
      ((L.concat P).concat R).IsMeshLE δ ∧
      partitionEnergy x ((L.concat P).concat R) =
        partitionEnergy x L + partitionEnergy x P + partitionEnergy x R := by
  obtain ⟨l, L, hL⟩ := exists_partition_mesh_le has hδ
  obtain ⟨r, R, hR⟩ := exists_partition_mesh_le htb hδ
  refine ⟨l, r, L, R,
    OrderedPartition.concat_isMeshLE (OrderedPartition.concat_isMeshLE hL hP) hR, ?_⟩
  rw [partitionEnergy_concat, partitionEnergy_concat, add_assoc]

/-- A mesh-admissible subinterval partition has energy bounded by the global
fine squared variation after extension to the containing interval. -/
lemma partitionEnergy_le_fineEVariationSq_superinterval
    {E : Type*} [SeminormedAddCommGroup E] (x : ℝ → E)
    {a s t b δ : ℝ} {n : ℕ} (P : OrderedPartition s t n)
    (has : a ≤ s) (hst : s ≤ t) (htb : t ≤ b) (hδ : 0 < δ)
    (hP : P.IsMeshLE δ) :
    partitionEnergy x P ≤ fineEVariationSq x a b δ := by
  obtain ⟨l, r, L, R, hmesh, henergy⟩ :=
    exists_superinterval_extension x P has hst htb hδ hP
  have hglobal := partitionEnergy_le_fineEVariationSq x ((L.concat P).concat R) hmesh
  rw [henergy] at hglobal
  have hdrop : partitionEnergy x P ≤
      partitionEnergy x L + partitionEnergy x P + partitionEnergy x R :=
    le_add_right (self_le_add_left _ _)
  exact hdrop.trans hglobal

/-- Faithful critical vanishing-variation data for a path on `[a,b]`.
`finiteScale` makes real-valued square-root estimates legitimate at one scale;
`vanishes` is the right-hand limit at mesh zero. -/
structure VanishingVariationData {E : Type*} [SeminormedAddCommGroup E]
    (x : ℝ → E) (a b : ℝ) where
  interval_nonempty : a ≤ b
  finiteScale : ∃ δ : ℝ, 0 < δ ∧ fineEVariationSq x a b δ ≠ ⊤
  vanishes : Filter.Tendsto (fineEVariationSq x a b)
    (nhdsWithin 0 (Set.Ioi 0)) (nhds 0)

/-- The scalar inequality responsible for the factor `sqrt 2` when an
increment is split at a periodic seam. -/
lemma sq_add_le_two_sq (a b : ℝ) : (a + b) ^ 2 ≤ 2 * (a ^ 2 + b ^ 2) := by
  nlinarith [sq_nonneg (a - b)]

/-- Normed-space form of the seam estimate. -/
lemma norm_add_sq_le_two {E : Type*} [SeminormedAddCommGroup E]
    (u v : E) : ‖u + v‖ ^ 2 ≤ 2 * (‖u‖ ^ 2 + ‖v‖ ^ 2) := by
  have hadd := norm_add_le u v
  have hu := norm_nonneg u
  have hv := norm_nonneg v
  have huv := norm_nonneg (u + v)
  nlinarith [sq_nonneg (‖u‖ - ‖v‖)]

/-- Finite algebra used after a refinement has represented each old increment
as a sum of two endpoint pieces. Refinement semantics are not asserted here. -/
lemma sum_norm_add_sq_le_two {E ι : Type*} [SeminormedAddCommGroup E]
    [Fintype ι] (u v : ι → E) :
    (∑ i, ‖u i + v i‖ ^ 2) ≤
      2 * ((∑ i, ‖u i‖ ^ 2) + ∑ i, ‖v i‖ ^ 2) := by
  calc
    (∑ i, ‖u i + v i‖ ^ 2) ≤ ∑ i, 2 * (‖u i‖ ^ 2 + ‖v i‖ ^ 2) :=
      Finset.sum_le_sum fun i _ ↦ norm_add_sq_le_two (u i) (v i)
    _ = 2 * ((∑ i, ‖u i‖ ^ 2) + ∑ i, ‖v i‖ ^ 2) := by
      simp_rw [mul_add]
      rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum]

/-- Pointwise local bounds by twice a comparison increment give the factor
`4` after squaring and summing. -/
lemma sum_sq_le_four_sum_sq {ι : Type*} [Fintype ι] (y c : ι → ℝ)
    (hy : ∀ i, 0 ≤ y i) (hc : ∀ i, 0 ≤ c i)
    (h : ∀ i, y i ≤ 2 * c i) :
    (∑ i, y i ^ 2) ≤ 4 * ∑ i, c i ^ 2 := by
  calc
    (∑ i, y i ^ 2) ≤ ∑ i, 4 * c i ^ 2 := by
      apply Finset.sum_le_sum
      intro i _
      have htwo : 0 ≤ 2 * c i := mul_nonneg (by norm_num) (hc i)
      have hi := (sq_le_sq₀ (hy i) htwo).2 (h i)
      nlinarith
    _ = 4 * ∑ i, c i ^ 2 := by rw [Finset.mul_sum]

/-- The sum of squared nonnegative subdivision lengths is at most the square
of their total length. This is the finite core of the statement that an
affine chord has 2-variation equal to its endpoint distance. -/
lemma sum_sq_le_sq_sum {ι : Type*} [Fintype ι] (d : ι → ℝ)
    (hd : ∀ i, 0 ≤ d i) :
    (∑ i, d i ^ 2) ≤ (∑ i, d i) ^ 2 := by
  exact Finset.sum_sq_le_sq_sum_of_nonneg fun i _ ↦ hd i

/-- Normalized affine subdivision form of `sum_sq_le_sq_sum`: multiplying
nonnegative weights of total mass one by a chord length does not increase its
squared 2-variation beyond the squared chord length. -/
lemma affineChord_sqVariation_le {ι : Type*} [Fintype ι] (d : ι → ℝ) (L : ℝ)
    (hd : ∀ i, 0 ≤ d i) (hsum : ∑ i, d i = 1) :
    (∑ i, (d i * L) ^ 2) ≤ L ^ 2 := by
  have hsq : (∑ i, d i ^ 2) ≤ 1 := by
    simpa [hsum] using sum_sq_le_sq_sum d hd
  calc
    (∑ i, (d i * L) ^ 2) = L ^ 2 * ∑ i, d i ^ 2 := by
      simp only [mul_pow]
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i _
      ring
    _ ≤ L ^ 2 * 1 := mul_le_mul_of_nonneg_left hsq (sq_nonneg L)
    _ = L ^ 2 := mul_one _

/-- Squared-error bookkeeping behind the explicit `sqrt 8` polygonal
interpolation bound. The three hypotheses are precisely the analytic partition
steps which a later path-level formalization must discharge. -/
lemma pl_error_sq_le_eight (globalError localError localPath w : ℝ)
    (hglobal : globalError ^ 2 ≤ 2 * localError)
    (hlocal : localError ≤ 4 * localPath)
    (hpath : localPath ≤ w ^ 2) :
    globalError ^ 2 ≤ 8 * w ^ 2 := by
  nlinarith

/-- Unsquared form of the `sqrt 8` estimate. -/
lemma pl_error_le_sqrt_eight (globalError w : ℝ)
    (_he : 0 ≤ globalError) (hw : 0 ≤ w)
    (hsq : globalError ^ 2 ≤ 8 * w ^ 2) :
    globalError ≤ Real.sqrt 8 * w := by
  have hsqrt : 0 ≤ Real.sqrt 8 := Real.sqrt_nonneg 8
  have hsqrtSq : (Real.sqrt 8) ^ 2 = 8 := Real.sq_sqrt (by norm_num)
  have hproduct : 0 ≤ Real.sqrt 8 * w := mul_nonneg hsqrt hw
  nlinarith [sq_nonneg (globalError + Real.sqrt 8 * w)]

/-- The planar determinant, represented using complex coordinates. -/
def cross (z w : ℂ) : ℝ := z.re * w.im - z.im * w.re

/-- The Euclidean dot product, represented using complex coordinates. -/
def dot (z w : ℂ) : ℝ := z.re * w.re + z.im * w.im

/-- Subtracting the first endpoint from the second argument does not change
the determinant. This is the algebra used in the chord-action estimate. -/
lemma cross_eq_cross_sub (q p : ℂ) : cross q p = cross q (p - q) := by
  simp [cross]
  ring

/-- Exact affine-segment form of `y dx = -lambda_0 + d(xy/2)`.
It avoids importing differential forms: every term is an endpoint expression. -/
lemma liouville_segment_conversion (p q : ℂ) :
    ((p.im + q.im) / 2) * (q.re - p.re) =
      -(p.re * (q.im - p.im) - p.im * (q.re - p.re)) / 2 +
        (q.re * q.im - p.re * p.im) / 2 := by
  ring

/-- The diagonals represented by `u+v` and `u-v` are perpendicular exactly
when the squared lengths of `u` and `v` agree. -/
lemma dot_add_sub (u v : ℂ) :
    dot (u + v) (u - v) = Complex.normSq u - Complex.normSq v := by
  simp [dot, Complex.normSq_apply]
  ring

/-- Perpendicular diagonals force equal squared half-side lengths. This is only
an algebraic square criterion; it does not provide distinct vertices. -/
lemma normSq_eq_of_perpendicular {u v : ℂ} (h : dot (u + v) (u - v) = 0) :
    Complex.normSq u = Complex.normSq v := by
  rw [dot_add_sub] at h
  linarith

/-- A strictly positive functional on both incident edge velocities stays
positive on every convex combination. This is the finite algebraic core of
the nonvanishing-derivative argument for a mollified polygonal corner. -/
lemma dot_convexCombination_pos (n a b : ℂ) (α β : ℝ)
    (hα : 0 ≤ α) (hβ : 0 ≤ β) (hsum : α + β = 1)
    (ha : 0 < dot n a) (hb : 0 < dot n b) :
    0 < dot n (α • a + β • b) := by
  have hlinear : dot n (α • a + β • b) = α * dot n a + β * dot n b := by
    simp only [dot, Complex.add_re, Complex.add_im, Complex.smul_re, Complex.smul_im,
      smul_eq_mul]
    ring
  rw [hlinear]
  rcases eq_or_lt_of_le hα with rfl | hαpos
  · simp only [zero_add] at hsum ⊢
    simpa [hsum] using hb
  · have hleft : 0 < α * dot n a := mul_pos hαpos ha
    have hright : 0 ≤ β * dot n b := mul_nonneg hβ (le_of_lt hb)
    exact add_pos_of_pos_of_nonneg hleft hright

/-- A convex combination of two vectors in a radius-`M` ball remains in that
ball. This supplies the pointwise `‖Q'‖ ≤ M` part of the smoothing estimate. -/
lemma norm_convexCombination_le {E : Type*} [SeminormedAddCommGroup E]
    [NormedSpace ℝ E] (a b : E) (α β M : ℝ)
    (hα : 0 ≤ α) (hβ : 0 ≤ β) (hsum : α + β = 1)
    (ha : ‖a‖ ≤ M) (hb : ‖b‖ ≤ M) :
    ‖α • a + β • b‖ ≤ M := by
  calc
    ‖α • a + β • b‖ ≤ ‖α • a‖ + ‖β • b‖ := norm_add_le _ _
    _ = α * ‖a‖ + β * ‖b‖ := by rw [norm_smul, norm_smul, Real.norm_eq_abs,
      Real.norm_eq_abs, abs_of_nonneg hα, abs_of_nonneg hβ]
    _ ≤ α * M + β * M := add_le_add (mul_le_mul_of_nonneg_left ha hα)
      (mul_le_mul_of_nonneg_left hb hβ)
    _ = M := by rw [← add_mul, hsum, one_mul]

/-- Scalar bookkeeping for the quantitative smoothing bound: a set of total
parameter length at most `2*m*h` and pointwise error at most `2*M` contributes
at most `4*m*M*h`. -/
lemma smoothing_error_constant (m M h : ℝ) :
    (2 * M) * (2 * m * h) = 4 * m * M * h := by
  ring

/-- Logical composition of the two separately pinned Asano--Ike interfaces.
`analyticCriterion` represents arXiv:2412.21057v3, Theorem 1.1 (PDF p. 2),
while `nondegeneracy` represents its four-distinct/off-diagonal meaning
(PDF pp. 2–3 and Theorem 4.1 proof, p. 19). Keeping them as arguments avoids
turning an external citation into a Lean axiom. -/
theorem conditional_positive_square
    {AnalyticData RectangleConclusion PositiveSquare : Prop}
    (data : AnalyticData)
    (analyticCriterion : AnalyticData → RectangleConclusion)
    (nondegeneracy : RectangleConclusion → PositiveSquare) :
    PositiveSquare :=
  nondegeneracy (analyticCriterion data)

end Verified.SquarePeg.C02Var
