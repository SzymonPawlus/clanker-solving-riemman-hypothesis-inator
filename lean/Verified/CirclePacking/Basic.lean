/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: claude
-/
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Convex.Combination

/-!
# Circle packing in an equilateral triangle — feasibility of explicit configurations

**Claim kind: construction / upper bound** (`problems/circle-packing-equilateral-triangle/RULES.md`
§1). Nothing here says any configuration is optimal, and nothing here should be cited as an
optimality or lower-bound result.

We work in the point formulation of the problem README: packing `n` unit circles into an
equilateral triangle of side `s` is equivalent to placing `n` points at pairwise distance `≥ 2`
inside a concentric equilateral triangle of side `d = s - 2 * √3`.

The triangle of admissible centres is placed with vertices `(0, 0)`, `(d, 0)`, `(d / 2, √3 * d / 2)`
and described by its three closed half-planes (`InTriangle`). Half-planes are used rather than a
distance-to-side formulation because every containment check then becomes a linear inequality in
the coordinates, which `nlinarith` closes given only `√3 ^ 2 = 3` and `0 ≤ √3`.
`inTriangle_iff_mem_convexHull` proves that this really is the closed triangular hull of the three
vertices, so the predicate is not accidentally larger (or smaller) than the intended region.
-/

namespace Verified.CirclePacking

open Real

/-- The Euclidean plane, with the genuine Euclidean distance (not the sup metric that `ℝ × ℝ`
carries). -/
abbrev Plane := EuclideanSpace ℝ (Fin 2)

/-- The point of the plane with coordinates `(x, y)`. -/
def pt (x y : ℝ) : Plane := !₂[x, y]

@[simp] lemma pt_zero (x y : ℝ) : pt x y 0 = x := rfl

@[simp] lemma pt_one (x y : ℝ) : pt x y 1 = y := rfl

lemma dist_pt (x₁ y₁ x₂ y₂ : ℝ) :
    dist (pt x₁ y₁) (pt x₂ y₂) = √((x₁ - x₂) ^ 2 + (y₁ - y₂) ^ 2) := by
  rw [EuclideanSpace.dist_eq]
  congr 1
  simp [Fin.sum_univ_two, Real.dist_eq, sq_abs]

/-- The distance between two explicitly given points is at least `2` as soon as the squared
distance is at least `4`. This is the bridge from the algebra to the metric statement. -/
lemma two_le_dist_pt {x₁ y₁ x₂ y₂ : ℝ}
    (h : 4 ≤ (x₁ - x₂) ^ 2 + (y₁ - y₂) ^ 2) : 2 ≤ dist (pt x₁ y₁) (pt x₂ y₂) := by
  rw [dist_pt]
  have h4 : (2 : ℝ) = √4 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  rw [h4]
  exact Real.sqrt_le_sqrt h

/-- `√3 ^ 2 = 3`, packaged for `nlinarith`. -/
lemma sq_sqrt_three : √3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)

/-- `0 ≤ √3`, packaged for `nlinarith`. -/
lemma sqrt_three_nonneg : (0 : ℝ) ≤ √3 := Real.sqrt_nonneg 3

/-- `p` lies in the closed equilateral triangle with vertices `(0, 0)`, `(d, 0)` and
`(d / 2, √3 * d / 2)`, described as the intersection of its three closed half-planes: above the
base, right of the left edge, left of the right edge. -/
def InTriangle (d : ℝ) (p : Plane) : Prop :=
  0 ≤ p 1 ∧ p 1 ≤ √3 * p 0 ∧ √3 * p 0 + p 1 ≤ √3 * d

/-- `p : Fin n → Plane` is a feasible packing of `n` points in the triangle of side `d`: every
point lies in the triangle and every two distinct points are at distance at least `2`. By the
reduction in the problem README this is exactly a packing of `n` unit circles in an equilateral
triangle of side `d + 2 * √3`. -/
def IsFeasible {n : ℕ} (d : ℝ) (p : Fin n → Plane) : Prop :=
  (∀ i, InTriangle d (p i)) ∧ ∀ i j, i ≠ j → 2 ≤ dist (p i) (p j)

/-- A side length `d` is admissible for `n` points when some configuration of `n` points is
feasible in the triangle of side `d`. -/
def Admissible (n : ℕ) (d : ℝ) : Prop := ∃ p : Fin n → Plane, IsFeasible d p

/-- `d n`, the least side length of an equilateral triangle admitting `n` points at mutual
distance at least `2`. -/
noncomputable def minPointSide (n : ℕ) : ℝ := sInf {d | Admissible n d}

/-- `s n`, the least side length of an equilateral triangle admitting a packing by `n` unit
circles, via `s n = 2 * √3 + d n` (the reduction in the problem README). -/
noncomputable def minCircleSide (n : ℕ) : ℝ := 2 * √3 + minPointSide n

/-!
## Bounding the infimum

`minPointSide` is an `sInf`, so an upper bound on it needs the set of admissible sides to be
bounded below; otherwise `sInf` is junk-valued `0` and `minPointSide n ≤ c` would be vacuous
rather than meaningful.
-/

/-- Only nonnegative side lengths are admissible once there is at least one point to place. -/
lemma nonneg_of_admissible {n : ℕ} (hn : 0 < n) {d : ℝ} (hd : Admissible n d) : 0 ≤ d := by
  obtain ⟨p, hin, -⟩ := hd
  obtain ⟨h0, h1, h2⟩ := hin ⟨0, hn⟩
  have h3 : (0 : ℝ) < √3 := Real.sqrt_pos.mpr (by norm_num)
  nlinarith [h0, h1, h2, h3]

/-- The admissible sides for `n ≥ 1` points are bounded below, so `sInf` is the genuine
infimum. -/
lemma bddBelow_admissible {n : ℕ} (hn : 0 < n) : BddBelow {d : ℝ | Admissible n d} :=
  ⟨0, fun _ hd => nonneg_of_admissible hn hd⟩

/-- Any admissible side bounds `minPointSide` from above. This is the only route by which an
explicit configuration turns into an upper bound. -/
lemma minPointSide_le {n : ℕ} (hn : 0 < n) {d : ℝ} (hd : Admissible n d) :
    minPointSide n ≤ d :=
  csInf_le (bddBelow_admissible hn) hd

/-- Any admissible side bounds `minCircleSide` from above. -/
lemma minCircleSide_le {n : ℕ} (hn : 0 < n) {d : ℝ} (hd : Admissible n d) :
    minCircleSide n ≤ 2 * √3 + d := by
  have := minPointSide_le hn hd
  simpa [minCircleSide] using this

/-- Reduce a pairwise condition to the pairs with `i < j`, halving the case split. -/
lemma pairwise_of_lt {n : ℕ} {p : Fin n → Plane}
    (h : ∀ i j : Fin n, i < j → 2 ≤ dist (p i) (p j)) :
    ∀ i j : Fin n, i ≠ j → 2 ≤ dist (p i) (p j) := by
  intro i j hij
  rcases lt_or_gt_of_ne hij with h' | h'
  · exact h i j h'
  · rw [dist_comm]; exact h j i h'

/-!
## `n = 3`

Three points at the corners of a triangle of side `2`, pairwise distance exactly `2`.
Gives `s 3 ≤ 2 + 2 * √3`.
-/

/-- The three corners of an equilateral triangle of side `2`. -/
noncomputable def config3 : Fin 3 → Plane := ![pt 0 0, pt 2 0, pt 1 √3]

/-- **Construction, not optimality.** The three corners of a side-`2` triangle are a feasible
placement of `3` points. -/
theorem isFeasible_config3 : IsFeasible (n := 3) 2 config3 := by
  refine ⟨?_, pairwise_of_lt ?_⟩
  · intro i
    fin_cases i <;>
      refine ⟨?_, ?_, ?_⟩ <;>
      simp only [config3, Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk, Matrix.cons_val_zero,
        Matrix.cons_val_one, Matrix.cons_val, pt_zero, pt_one] <;>
      nlinarith [sqrt_three_nonneg, sq_sqrt_three]
  · intro i j hij
    fin_cases i <;> fin_cases j <;>
      simp only [config3, Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk, Matrix.cons_val_zero,
        Matrix.cons_val_one, Matrix.cons_val] <;>
      first
        | exact absurd hij (by decide)
        | (apply two_le_dist_pt; nlinarith [sqrt_three_nonneg, sq_sqrt_three])

/-- `d 3 ≤ 2`: three points at mutual distance `≥ 2` fit in an equilateral triangle of side `2`.
Upper bound only. -/
theorem minPointSide_three_le : minPointSide 3 ≤ 2 :=
  minPointSide_le (by norm_num) ⟨config3, isFeasible_config3⟩

/-- `s 3 ≤ 2 + 2 * √3`: three unit circles pack into an equilateral triangle of side
`2 + 2 * √3`. **Upper bound / construction only** — this does not claim optimality. -/
theorem minCircleSide_three_le : minCircleSide 3 ≤ 2 + 2 * √3 := by
  have := minCircleSide_le (n := 3) (by norm_num) ⟨config3, isFeasible_config3⟩
  linarith

/-!
## `n = 6`

The triangular-lattice arrangement `T₃`: the three corners of a triangle of side `4` together
with the three edge midpoints. Gives `s 6 ≤ 4 + 2 * √3`, matching the value recorded in the
problem README for `n = 6`.
-/

/-- The six points of the triangular lattice `T₃` in a triangle of side `4`. -/
noncomputable def config6 : Fin 6 → Plane :=
  ![pt 0 0, pt 2 0, pt 4 0, pt 1 √3, pt 3 √3, pt 2 (2 * √3)]

/-- **Construction, not optimality.** The `T₃` lattice arrangement is a feasible placement of `6`
points in a triangle of side `4`. -/
theorem isFeasible_config6 : IsFeasible (n := 6) 4 config6 := by
  refine ⟨?_, pairwise_of_lt ?_⟩
  · intro i
    fin_cases i <;>
      refine ⟨?_, ?_, ?_⟩ <;>
      simp only [config6, Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk, Matrix.cons_val_zero,
        Matrix.cons_val_one, Matrix.cons_val, pt_zero, pt_one] <;>
      nlinarith [sqrt_three_nonneg, sq_sqrt_three]
  · intro i j hij
    fin_cases i <;> fin_cases j <;>
      simp only [config6, Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk, Matrix.cons_val_zero,
        Matrix.cons_val_one, Matrix.cons_val] <;>
      first
        | exact absurd hij (by decide)
        | (apply two_le_dist_pt; nlinarith [sqrt_three_nonneg, sq_sqrt_three])

/-- `d 6 ≤ 4`. Upper bound only. -/
theorem minPointSide_six_le : minPointSide 6 ≤ 4 :=
  minPointSide_le (by norm_num) ⟨config6, isFeasible_config6⟩

/-- `s 6 ≤ 4 + 2 * √3`: six unit circles pack into an equilateral triangle of side `4 + 2 * √3`.
**Upper bound / construction only** — this does not claim optimality, though the value matches the
one credited to Oler/Groemer in the problem README. -/
theorem minCircleSide_six_le : minCircleSide 6 ≤ 4 + 2 * √3 := by
  have := minCircleSide_le (n := 6) (by norm_num) ⟨config6, isFeasible_config6⟩
  linarith

end Verified.CirclePacking
