/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Codex
-/
import Verified.Moser.SupportAllocation

/-!
# Finite polygon bridge for the Moser support argument

This module proves the algebraic common-normal-fan identities without measure
theory.  Geometric compatibility with a concrete cyclic fan remains visible in
the hypotheses of the final theorem.
-/

namespace Verified.Moser.PolygonBridge

/-- A real planar vector, represented without introducing additional geometry APIs. -/
abbrev RVec := ℝ × ℝ

/-- Vector subtraction. -/
def vsub (u v : RVec) : RVec := (u.1 - v.1, u.2 - v.2)

/-- The oriented planar determinant. -/
def det (u v : RVec) : ℝ := u.1 * v.2 - u.2 * v.1

/-- Dot product on the chosen pair representation. -/
def dot (u v : RVec) : ℝ := u.1 * v.1 + u.2 * v.2

/-- Clockwise rotation by a right angle. -/
def cw (u : RVec) : RVec := (u.2, -u.1)

/-- Unnormalised outward normal of a counterclockwise directed edge. -/
def outward (u v : RVec) : RVec := cw (vsub v u)

/-- The edge/support pairing equals the corresponding determinant. -/
theorem dot_outward (x u v : RVec) : dot x (outward u v) = det x (vsub v u) := by
  simp [dot, outward, cw, det, vsub]
  ring

/-- Scalar cyclic integration by parts. -/
theorem cyclic_mul_sub {n : ℕ} [NeZero n] (a b : ZMod n → ℝ) :
    ∑ i, a i * (b (i + 1) - b i) = ∑ i, b i * (a (i - 1) - a i) := by
  have shift := Equiv.sum_comp (Equiv.addRight (-1 : ZMod n))
    (fun i ↦ a i * b (i + 1))
  have shift' : ∑ i, a i * b (i + 1) = ∑ i, a (i - 1) * b i := by
    calc
      _ = ∑ i, a ((Equiv.addRight (-1 : ZMod n)) i) *
          b ((Equiv.addRight (-1 : ZMod n)) i + 1) := shift.symm
      _ = _ := by
        apply Finset.sum_congr rfl
        intro i _
        congr 2 <;> simp [Equiv.addRight, sub_eq_add_neg]
  simp_rw [mul_sub, Finset.sum_sub_distrib]
  rw [shift']
  congr 1 <;> apply Finset.sum_congr rfl <;> intro i _ <;> ring

/-- Discrete cyclic integration by parts on a common fan. -/
theorem cyclic_summation_by_parts {n : ℕ} [NeZero n]
    (p k : ZMod n → RVec) :
    ∑ i, det (k i) (vsub (p (i + 1)) (p i)) =
      ∑ i, det (p i) (vsub (k i) (k (i - 1))) := by
  simp_rw [det, vsub, Finset.sum_sub_distrib]
  rw [cyclic_mul_sub (fun i ↦ (k i).1) (fun i ↦ (p i).2)]
  rw [cyclic_mul_sub (fun i ↦ (k i).2) (fun i ↦ (p i).1)]
  have hx : ∑ i, (p i).2 * ((k (i - 1)).1 - (k i).1) =
      -(∑ i, (p i).2 * ((k i).1 - (k (i - 1)).1)) := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro i _
    ring
  have hy : ∑ i, (p i).1 * ((k (i - 1)).2 - (k i).2) =
      -(∑ i, (p i).1 * ((k i).2 - (k (i - 1)).2)) := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hx, hy]
  ring

/-- Shoelace twice-area for cyclic vertices. -/
def twiceArea {n : ℕ} [NeZero n] (p : ZMod n → RVec) : ℝ :=
  ∑ i, det (p i) (p (i + 1))

/-- Self-pairing with outward edge vectors is exactly the shoelace sum. -/
theorem self_surface_eq_twiceArea {n : ℕ} [NeZero n] (p : ZMod n → RVec) :
    ∑ i, dot (p i) (outward (p i) (p (i + 1))) = twiceArea p := by
  simp_rw [dot_outward]
  simp only [twiceArea, det, vsub]
  simp_rw [mul_sub, Finset.sum_sub_distrib]
  have diagonal : ∑ i, (p i).1 * (p i).2 = ∑ i, (p i).2 * (p i).1 := by
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [diagonal]
  ring

/-- Mixed surface sum using the support vertex of `k` selected on each edge of `p`. -/
def surface {n : ℕ} [NeZero n] (p k : ZMod n → RVec) : ℝ :=
  ∑ i, dot (k i) (outward (p i) (p (i + 1)))

/-- Common-fan surface symmetry, with the dual support vertex indexed at the fan ray's end. -/
theorem surface_symmetry_commonFan {n : ℕ} [NeZero n]
    (p k : ZMod n → RVec) :
    surface p k = ∑ i, dot (p i) (outward (k (i - 1)) (k i)) := by
  simp_rw [surface, dot_outward]
  exact cyclic_summation_by_parts p k

/-- The backwards-indexed self surface is also the shoelace twice-area. -/
theorem self_surface_prev_eq_twiceArea {n : ℕ} [NeZero n] (k : ZMod n → RVec) :
    ∑ i, dot (k i) (outward (k (i - 1)) (k i)) = twiceArea k := by
  simp_rw [dot_outward]
  simp only [twiceArea, det, vsub]
  have shift := Equiv.sum_comp (Equiv.addRight (1 : ZMod n))
    (fun i ↦ det (k (i - 1)) (k i))
  calc
    ∑ i, det (k i) (vsub (k i) (k (i - 1))) =
        ∑ i, det (k (i - 1)) (k i) := by
      apply Finset.sum_congr rfl
      intro i _
      simp [det, vsub]
      ring
    _ = ∑ i, det (k i) (k (i + 1)) := by
      rw [← shift]
      apply Finset.sum_congr rfl
      intro i _
      congr 2
      all_goals simp [Equiv.addRight, sub_eq_add_neg]

/-- The finite mixed-area inequality once a common fan supplies the two active
support vertices and containment supplies their pointwise support comparison. -/
theorem surface_le_twiceArea_of_commonFan {n : ℕ} [NeZero n]
    (p k : ZMod n → RVec)
    (containedSupport : ∀ i,
      dot (p i) (outward (k (i - 1)) (k i)) ≤
        dot (k i) (outward (k (i - 1)) (k i))) :
    surface p k ≤ twiceArea k := by
  rw [surface_symmetry_commonFan, ← self_surface_prev_eq_twiceArea]
  apply Finset.sum_le_sum
  intro i _
  exact containedSupport i

/-- Repeating a support vertex across a newly inserted fan ray contributes a
zero edge to the polygon whose vertex was repeated. -/
theorem repeated_vertex_edge_zero (u x : RVec) :
    outward x x = (0, 0) ∧ dot u (outward x x) = 0 ∧ det x (vsub x x) = 0 := by
  simp [outward, cw, vsub, dot, det]

/-- Determinant sum along an open polygonal chain. -/
def chainDet : List RVec → ℝ
  | x :: y :: tail => det x y + chainDet (y :: tail)
  | _ => 0

/-- Inserting a repeated support vertex leaves an open-chain shoelace sum unchanged. -/
theorem chainDet_insert_duplicate (pre : List RVec) (x : RVec) (suffix : List RVec) :
    chainDet (pre ++ x :: x :: suffix) = chainDet (pre ++ x :: suffix) := by
  induction pre with
  | nil =>
      cases suffix <;> simp [chainDet, det] <;> ring
  | cons y tail ih =>
      cases tail with
      | nil => simp [chainDet, det]; ring
      | cons z zs => simpa [chainDet] using ih

/-- Closing an open chain by its first vertex gives the cyclic shoelace sum. -/
def closedChainDet : List RVec → ℝ
  | [] => 0
  | x :: xs => chainDet (x :: xs ++ [x])

/-- Repeating an interior support vertex preserves the closed shoelace sum. -/
theorem closedChainDet_insert_duplicate (first : RVec) (pre : List RVec)
    (x : RVec) (suffix : List RVec) :
    closedChainDet (first :: pre ++ x :: x :: suffix) =
      closedChainDet (first :: pre ++ x :: suffix) := by
  simp only [closedChainDet, List.cons_append]
  simpa [List.append_assoc] using
    chainDet_insert_duplicate (first :: pre) x (suffix ++ [first])

/-- Exact determinant area of a triangle on the horizontal unit base. -/
theorem unit_base_triangle_twiceArea (x h : ℝ) :
    det (0, 0) (1, 0) + det (1, 0) (x, h) + det (x, h) (0, 0) = h := by
  simp [det]

/-- Each of the two base-apex triangles lies in a convex containing set. -/
theorem opposite_base_triangles_subset_convex
    (K : Set RVec) (hK : Convex ℝ K) (a b upper lower : RVec)
    (ha : a ∈ K) (hb : b ∈ K) (hu : upper ∈ K) (hl : lower ∈ K) :
    convexHull ℝ ({a, b, upper} : Set RVec) ⊆ K ∧
      convexHull ℝ ({a, b, lower} : Set RVec) ⊆ K := by
  constructor <;> apply convexHull_min _ hK
  · intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with (rfl | rfl | rfl) <;> assumption
  · intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with (rfl | rfl | rfl) <;> assumption

/-- End-to-end finite-polygon chain from common-fan support containment and an
allocation slab to the shoelace area of the containing polygon.  Edge lengths
are absorbed into the unnormalised outward vectors. -/
theorem allocation_chain_commonFan {n m : ℕ} [NeZero n]
    (p k : ZMod n → RVec) (allocation : ZMod n → Fin m → ℝ)
    (placedSupport : Fin m → ZMod n → ℝ) (target : ℝ)
    (allocation_nonneg : ∀ e j, 0 ≤ allocation e j)
    (capacity : ∀ e, ∑ j, allocation e j = 1)
    (placed_contained : ∀ e j,
      placedSupport j e ≤ dot (k e) (outward (p e) (p (e + 1))))
    (commonFan_contained : ∀ i,
      dot (p i) (outward (k (i - 1)) (k i)) ≤
        dot (k i) (outward (k (i - 1)) (k i)))
    (slab : target ≤
      (∑ e, ∑ j, allocation e j * placedSupport j e) / 2) :
    target ≤ twiceArea k / 2 := by
  have mixed : (∑ e, (1 : ℝ) *
      dot (k e) (outward (p e) (p (e + 1)))) / 2 ≤ twiceArea k / 2 := by
    have hsurface := surface_le_twiceArea_of_commonFan p k commonFan_contained
    simpa [surface] using div_le_div_of_nonneg_right hsurface (by norm_num : (0 : ℝ) ≤ 2)
  have halloc := mixed_area_support_allocation_bound (twiceArea k / 2)
    (fun _ ↦ 1) (fun e ↦ dot (k e) (outward (p e) (p (e + 1))))
    placedSupport allocation (fun _ ↦ by norm_num) allocation_nonneg capacity
    placed_contained mixed
  exact slab.trans (by simpa using halloc)

/-- A finite convex combination cannot exceed a common scalar upper bound. -/
theorem convexCombination_le {ι : Type*} [Fintype ι]
    (weight value : ι → ℝ) (bound : ℝ)
    (weight_nonneg : ∀ i, 0 ≤ weight i)
    (weight_sum : ∑ i, weight i = 1)
    (value_le : ∀ i, value i ≤ bound) :
    ∑ i, weight i * value i ≤ bound := by
  calc
    ∑ i, weight i * value i ≤ ∑ i, weight i * bound := by
      apply Finset.sum_le_sum
      intro i _
      exact mul_le_mul_of_nonneg_left (value_le i) (weight_nonneg i)
    _ = bound := by rw [← Finset.sum_mul, weight_sum]; ring

/-- Dot product commutes with a finite convex combination, coordinatewise. -/
theorem dot_convexCombination {ι : Type*} [Fintype ι]
    (weight : ι → ℝ) (vertex : ι → RVec) (normal : RVec) :
    dot (∑ i, (weight i * (vertex i).1, weight i * (vertex i).2)) normal =
      ∑ i, weight i * dot (vertex i) normal := by
  simp only [dot, Prod.fst_sum, Prod.snd_sum]
  rw [Finset.sum_mul, Finset.sum_mul, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  ring

/-- Vertex containment expressed by convex coordinates implies support monotonicity. -/
theorem support_le_of_convexCoordinates {ι : Type*} [Fintype ι] [Nonempty ι]
    (weight : ι → ℝ) (vertex : ι → RVec) (point normal : RVec)
    (weight_nonneg : ∀ i, 0 ≤ weight i)
    (weight_sum : ∑ i, weight i = 1)
    (coordinates : point = ∑ i, (weight i * (vertex i).1, weight i * (vertex i).2)) :
    dot point normal ≤ Finset.max' (Finset.univ.image fun i ↦ dot (vertex i) normal)
      (Finset.image_nonempty.mpr ⟨Classical.choice inferInstance, Finset.mem_univ _⟩) := by
  classical
  subst point
  rw [dot_convexCombination]
  apply convexCombination_le weight (fun i ↦ dot (vertex i) normal) _
    weight_nonneg weight_sum
  intro i
  exact Finset.le_max' (Finset.univ.image fun i : ι ↦ dot (vertex i) normal) _
    (Finset.mem_image.mpr ⟨i, Finset.mem_univ i, rfl⟩)

end Verified.Moser.PolygonBridge
