/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Codex
-/
import Mathlib

/-!
# Determinant-only support ordering for the five-sector Moser bridge

This file isolates the local normal-cone implication used by the direct
five-edge proof.  It deliberately has no angular or trigonometric hypotheses.
-/

namespace Verified.Moser.FiveSectorOrder

abbrev RVec := ℝ × ℝ

def dot (u v : RVec) : ℝ := u.1 * v.1 + u.2 * v.2

def det (u v : RVec) : ℝ := u.1 * v.2 - u.2 * v.1

def cw (v : RVec) : RVec := (v.2, -v.1)

theorem dot_cw (u v : RVec) : dot u (cw v) = det u v := by
  simp [dot, cw, det]
  ring

theorem dot_add_right (x u v : RVec) :
    dot x (u.1 + v.1, u.2 + v.2) = dot x u + dot x v := by
  simp [dot]
  ring

theorem dot_smul_right (x u : RVec) (a : ℝ) :
    dot x (a * u.1, a * u.2) = a * dot x u := by
  simp [dot]
  ring

/-- If `p` supports a finite vertex family at two normals, it supports it at
every nonnegative linear combination of those normals.  This is the precise
local fact needed to assign all containing-polygon edges in one normal sector
to the intervening source vertex. -/
theorem supports_nonnegative_normal_cone {ι : Type*}
    (vertex : ι → RVec) (p n₀ n₁ : RVec) (a b : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b)
    (h₀ : ∀ j, dot (vertex j) n₀ ≤ dot p n₀)
    (h₁ : ∀ j, dot (vertex j) n₁ ≤ dot p n₁) :
    ∀ j, dot (vertex j)
        (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) ≤
      dot p (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) := by
  intro j
  have h₀' := mul_le_mul_of_nonneg_left (h₀ j) ha
  have h₁' := mul_le_mul_of_nonneg_left (h₁ j) hb
  calc
    dot (vertex j) (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) =
        a * dot (vertex j) n₀ + b * dot (vertex j) n₁ := by
          simp only [dot]
          ring
    _ ≤ a * dot p n₀ + b * dot p n₁ := add_le_add h₀' h₁'
    _ = dot p (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) := by
      simp only [dot]
      ring

/-- Determinant form: a vertex supporting the two bounding directed edges
supports every directed edge whose clockwise normal lies in their positive
normal cone. -/
theorem supports_edge_in_determinant_sector {ι : Type*}
    (vertex : ι → RVec) (p e₀ e₁ d : RVec) (a b : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hd : cw d =
      (a * (cw e₀).1 + b * (cw e₁).1,
       a * (cw e₀).2 + b * (cw e₁).2))
    (h₀ : ∀ j, det (vertex j) e₀ ≤ det p e₀)
    (h₁ : ∀ j, det (vertex j) e₁ ≤ det p e₁) :
    ∀ j, det (vertex j) d ≤ det p d := by
  intro j
  rw [← dot_cw, ← dot_cw, hd]
  exact supports_nonnegative_normal_cone vertex p (cw e₀) (cw e₁) a b ha hb
    (by simpa [dot_cw] using h₀) (by simpa [dot_cw] using h₁) j

/-- The two coefficients in a positively oriented planar cone are recovered
by determinants.  This eliminates angle functions from sector membership. -/
theorem cone_coefficients_of_det_pos (u v w : RVec) (huv : 0 < det u v) :
    w = ((det w v / det u v) * u.1 + (det u w / det u v) * v.1,
         (det w v / det u v) * u.2 + (det u w / det u v) * v.2) := by
  apply Prod.ext <;> simp only
  all_goals
    field_simp [ne_of_gt huv]
    simp only [det]
    ring

/-- Hence the determinant inequalities `det u w >= 0` and `det w v >= 0`
are exactly sufficient for membership in the closed positive cone from `u`
to `v`, provided that cone has turn strictly below `pi`. -/
theorem exists_nonnegative_cone_coefficients (u v w : RVec)
    (huv : 0 < det u v) (huw : 0 ≤ det u w) (hwv : 0 ≤ det w v) :
    ∃ a b : ℝ, 0 ≤ a ∧ 0 ≤ b ∧
      w = (a * u.1 + b * v.1, a * u.2 + b * v.2) := by
  refine ⟨det w v / det u v, det u w / det u v,
    div_nonneg hwv (le_of_lt huv), div_nonneg huw (le_of_lt huv), ?_⟩
  exact cone_coefficients_of_det_pos u v w huv

/-- Closed-sector support in a directly checkable determinant-only form. -/
theorem supports_determinant_sector {ι : Type*}
    (vertex : ι → RVec) (p n₀ n₁ n : RVec)
    (hturn : 0 < det n₀ n₁) (hleft : 0 ≤ det n₀ n)
    (hright : 0 ≤ det n n₁)
    (h₀ : ∀ j, dot (vertex j) n₀ ≤ dot p n₀)
    (h₁ : ∀ j, dot (vertex j) n₁ ≤ dot p n₁) :
    ∀ j, dot (vertex j) n ≤ dot p n := by
  obtain ⟨a, b, ha, hb, rfl⟩ :=
    exists_nonnegative_cone_coefficients n₀ n₁ n hturn hleft hright
  exact supports_nonnegative_normal_cone vertex p n₀ n₁ a b ha hb h₀ h₁

/-! ## The five exact cut rays -/

noncomputable def exactV0 : RVec := (9 / 41, -40 / 41)
noncomputable def exactV1 : RVec := (5183 / 5185, -144 / 5185)
noncomputable def exactV2 : RVec := (5183 / 5185, 144 / 5185)
noncomputable def exactV3 : RVec := (9 / 41, 40 / 41)
noncomputable def exactV4 : RVec := (-1, 0)

noncomputable def exactDirection : Fin 5 → RVec :=
  ![exactV0, exactV1, exactV2, exactV3, exactV4]

noncomputable def exactNormal (i : Fin 5) : RVec := cw (exactDirection i)

def next5 : Fin 5 → Fin 5 := ![1, 2, 3, 4, 0]

/-- Every exact consecutive normal sector has positive determinant, so the
determinant inequalities in `supports_determinant_sector` describe the short
counterclockwise cone rather than its complement. -/
theorem exactNormal_consecutive_det_pos (i : Fin 5) :
    0 < det (exactNormal i) (exactNormal (next5 i)) := by
  fin_cases i <;>
    simp [exactNormal, exactDirection, next5, exactV0, exactV1,
      exactV2, exactV3, exactV4, cw, det] <;> norm_num

/-- Exact unit-direction checks, independent of trigonometric functions. -/
theorem exactDirection_unit (i : Fin 5) :
    (exactDirection i).1 ^ 2 + (exactDirection i).2 ^ 2 = 1 := by
  fin_cases i <;>
    norm_num [exactDirection, exactV0, exactV1, exactV2, exactV3, exactV4]

/-- Specialization of the determinant-only cone lemma to any one of the five
exact normal sectors. -/
theorem supports_exact_sector {ι : Type*}
    (vertex : ι → RVec) (p n : RVec) (i : Fin 5)
    (hleft : 0 ≤ det (exactNormal i) n)
    (hright : 0 ≤ det n (exactNormal (next5 i)))
    (h₀ : ∀ j, dot (vertex j) (exactNormal i) ≤ dot p (exactNormal i))
    (h₁ : ∀ j, dot (vertex j) (exactNormal (next5 i)) ≤
      dot p (exactNormal (next5 i))) :
    ∀ j, dot (vertex j) n ≤ dot p n := by
  exact supports_determinant_sector vertex p (exactNormal i)
    (exactNormal (next5 i)) n (exactNormal_consecutive_det_pos i)
    hleft hright h₀ h₁

/-! ## Five-block telescoping algebra -/

/-- Cyclic summation by parts written explicitly for five cuts. This form has
no modular-index normalization burden and is the algebraic core consumed by a
five-block exposed-face ledger. -/
theorem five_cyclic_summation_by_parts
    (p0 p1 p2 p3 p4 k0 k1 k2 k3 k4 : RVec) :
    det k0 (p1.1 - p0.1, p1.2 - p0.2) +
      det k1 (p2.1 - p1.1, p2.2 - p1.2) +
      det k2 (p3.1 - p2.1, p3.2 - p2.2) +
      det k3 (p4.1 - p3.1, p4.2 - p3.2) +
      det k4 (p0.1 - p4.1, p0.2 - p4.2) =
    det p0 (k0.1 - k4.1, k0.2 - k4.2) +
      det p1 (k1.1 - k0.1, k1.2 - k0.2) +
      det p2 (k2.1 - k1.1, k2.2 - k1.2) +
      det p3 (k3.1 - k2.1, k3.2 - k2.2) +
      det p4 (k4.1 - k3.1, k4.2 - k3.2) := by
  simp only [det]
  ring

/-- Determinant distributes over a finite boundary block. -/
theorem det_list_sum_right (p : RVec) (edges : List RVec) :
    det p edges.sum = (edges.map (det p)).sum := by
  induction edges with
  | nil => simp [det]
  | cons d ds ih =>
      simp only [List.sum_cons, List.map_cons]
      calc
        det p (d + ds.sum) = det p d + det p ds.sum := by
          simp only [det, Prod.fst_add, Prod.snd_add]
          ring
        _ = det p d + (ds.map (det p)).sum := by rw [ih]

/-- Once the five exposed-face endpoint differences are supplied as sums of
five consecutive boundary blocks, their cyclic determinant sum is exactly the
sum of the five owner-weighted edge ledgers.  This packages all algebra after
the support-order lemma without constructing a merged common fan. -/
theorem five_block_telescoping
    (p0 p1 p2 p3 p4 k0 k1 k2 k3 k4 : RVec)
    (b0 b1 b2 b3 b4 : List RVec)
    (h0 : b0.sum = (k0.1 - k4.1, k0.2 - k4.2))
    (h1 : b1.sum = (k1.1 - k0.1, k1.2 - k0.2))
    (h2 : b2.sum = (k2.1 - k1.1, k2.2 - k1.2))
    (h3 : b3.sum = (k3.1 - k2.1, k3.2 - k2.2))
    (h4 : b4.sum = (k4.1 - k3.1, k4.2 - k3.2)) :
    det p0 (k0.1 - k4.1, k0.2 - k4.2) +
      det p1 (k1.1 - k0.1, k1.2 - k0.2) +
      det p2 (k2.1 - k1.1, k2.2 - k1.2) +
      det p3 (k3.1 - k2.1, k3.2 - k2.2) +
      det p4 (k4.1 - k3.1, k4.2 - k3.2) =
    (b0.map (det p0)).sum + (b1.map (det p1)).sum +
      (b2.map (det p2)).sum + (b3.map (det p3)).sum +
      (b4.map (det p4)).sum := by
  rw [← h0, ← h1, ← h2, ← h3, ← h4]
  simp only [det_list_sum_right]

end Verified.Moser.FiveSectorOrder
