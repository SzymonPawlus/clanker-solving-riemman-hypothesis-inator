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

/-!
### Sanity: `InTriangle` really is the triangle

`InTriangle` is our own definition, so on its own it could silently describe a region larger or
smaller than intended — the classic way to "prove" a weaker statement. The following identifies it
with the convex hull of the three vertices, which is the definition nobody can argue with.
-/

/-- The three vertices of the triangle of admissible centres. -/
noncomputable def vertices (d : ℝ) : Set Plane := {pt 0 0, pt d 0, pt (d / 2) (√3 * d / 2)}

/-- Two points of the plane agree as soon as both coordinates do. -/
lemma plane_ext {u v : Plane} (h0 : u 0 = v 0) (h1 : u 1 = v 1) : u = v := by
  rw [WithLp.ext_iff]
  funext i
  fin_cases i <;> assumption

/-- A convex combination of three points lies in their convex hull. -/
lemma mem_convexHull_triple {A B C p : Plane} {a b c : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (habc : a + b + c = 1) (hp : p = a • A + b • B + c • C) :
    p ∈ convexHull ℝ ({A, B, C} : Set Plane) := by
  have hA : A ∈ convexHull ℝ ({A, B, C} : Set Plane) := subset_convexHull ℝ _ (by simp)
  have hB : B ∈ convexHull ℝ ({A, B, C} : Set Plane) := subset_convexHull ℝ _ (by simp)
  have hC : C ∈ convexHull ℝ ({A, B, C} : Set Plane) := subset_convexHull ℝ _ (by simp)
  have hconv := convex_convexHull ℝ ({A, B, C} : Set Plane)
  rcases eq_or_lt_of_le (by linarith : (0 : ℝ) ≤ a + b) with hab | hab
  · have ha0 : a = 0 := by linarith
    have hb0 : b = 0 := by linarith
    have hc1 : c = 1 := by linarith
    simpa [hp, ha0, hb0, hc1] using hC
  · have hq : (a / (a + b)) • A + (b / (a + b)) • B ∈ convexHull ℝ ({A, B, C} : Set Plane) :=
      hconv hA hB (by positivity) (by positivity) (by field_simp)
    have hmix := hconv hq hC (le_of_lt hab) hc (by linarith)
    have hrw : (a + b) • ((a / (a + b)) • A + (b / (a + b)) • B) + c • C
        = a • A + b • B + c • C := by
      rw [smul_add, smul_smul, smul_smul]
      field_simp
    rw [hp, ← hrw]
    exact hmix

/-- The triangle is convex, being an intersection of three closed half-planes. -/
lemma convex_inTriangle (d : ℝ) : Convex ℝ {q : Plane | InTriangle d q} := by
  rintro u ⟨u1, u2, u3⟩ v ⟨v1, v2, v3⟩ a b ha hb hab
  refine ⟨?_, ?_, ?_⟩ <;>
    simp only [PiLp.add_apply, PiLp.smul_apply, smul_eq_mul] <;>
    nlinarith [u1, u2, u3, v1, v2, v3, ha, hb]

/-- `InTriangle d` is exactly the closed triangle spanned by the three vertices. This is the
statement that pins the definition down: the half-plane description is neither larger nor smaller
than the convex hull of `(0, 0)`, `(d, 0)`, `(d / 2, √3 * d / 2)`. -/
theorem inTriangle_iff_mem_convexHull {d : ℝ} (hd : 0 < d) (p : Plane) :
    InTriangle d p ↔ p ∈ convexHull ℝ (vertices d) := by
  have h3 : (0 : ℝ) < √3 := Real.sqrt_pos.mpr (by norm_num)
  have hne : √3 * d ≠ 0 := by positivity
  constructor
  · rintro ⟨h1, h2, h4⟩
    refine mem_convexHull_triple (A := pt 0 0) (B := pt d 0) (C := pt (d / 2) (√3 * d / 2))
      (a := (√3 * d - √3 * p 0 - p 1) / (√3 * d)) (b := (√3 * p 0 - p 1) / (√3 * d))
      (c := 2 * p 1 / (√3 * d))
      (div_nonneg (by linarith) (by positivity)) (div_nonneg (by linarith) (by positivity))
      (div_nonneg (by linarith) (by positivity)) (by field_simp; ring) ?_
    refine plane_ext ?_ ?_ <;>
      simp only [PiLp.add_apply, PiLp.smul_apply, smul_eq_mul, pt_zero, pt_one] <;>
      field_simp <;> ring
  · intro hp
    refine convexHull_min (t := {q : Plane | InTriangle d q}) ?_ (convex_inTriangle d) hp
    rintro q hq
    simp only [vertices, Set.mem_insert_iff, Set.mem_singleton_iff] at hq
    rcases hq with rfl | rfl | rfl <;>
      refine ⟨?_, ?_, ?_⟩ <;>
      simp only [pt_zero, pt_one] <;>
      nlinarith [h3, hd]

/-- Non-vacuity guard: `InTriangle` really excludes points, so a containment proof is not
trivially true. `(5, 0)` is outside the side-`4` triangle. -/
example : ¬ InTriangle 4 (pt 5 0) := by
  rintro ⟨-, -, h⟩
  simp only [pt_zero, pt_one] at h
  nlinarith [Real.sqrt_pos.mpr (show (0 : ℝ) < 3 by norm_num)]

/-- Non-vacuity guard: the separation condition really excludes point pairs. -/
example : ¬ (2 : ℝ) ≤ dist (pt 0 0) (pt 1 0) := by
  rw [dist_pt]
  have : √((0 - 1 : ℝ) ^ 2 + (0 - 0 : ℝ) ^ 2) = 1 := by norm_num
  rw [this]
  norm_num

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
