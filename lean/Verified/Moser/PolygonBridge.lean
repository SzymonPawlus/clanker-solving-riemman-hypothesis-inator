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

/-- Four-sector algebraic key for a nonzero oriented ray, cut at the positive
horizontal ray. The rational coordinate increases from zero to one inside each
closed quadrant. -/
noncomputable def rayKey (v : RVec) : Fin 4 × ℝ :=
  if 0 ≤ v.1 ∧ 0 ≤ v.2 then
    (⟨0, by norm_num⟩, v.2 / (v.1 + v.2))
  else if v.1 ≤ 0 ∧ 0 ≤ v.2 then
    (⟨1, by norm_num⟩, (-v.1) / (v.2 - v.1))
  else if v.1 ≤ 0 ∧ v.2 ≤ 0 then
    (⟨2, by norm_num⟩, (-v.2) / (-v.1 - v.2))
  else
    (⟨3, by norm_num⟩, v.1 / (v.1 - v.2))

/-- Lexicographically ordered form of `rayKey`, used by `fanMerge`. -/
noncomputable def rayOrderKey (v : RVec) : Lex (Fin 4 × ℝ) := toLex (rayKey v)

/-- Intrinsic rational worm normals, coerced to real vectors. -/
def wormN0 : RVec := (0, -1)
noncomputable def wormN1 : RVec := (260 / 269, -(69 / 269))
noncomputable def wormN2 : RVec :=
  (2 * (260 / 269) * (69 / 269), (260 / 269) ^ 2 - (69 / 269) ^ 2)
noncomputable def wormN3 : RVec := (-(260 / 269), 69 / 269)

/-- Exact rational worm hull vertices in cyclic order. -/
noncomputable def wormVertex (i : ZMod 4) : RVec :=
  if i = 0 then (0, 0)
  else if i = 1 then (1 / 3, 0)
  else if i = 2 then (338 / 807, 260 / 807)
  else (9361 / 72361, 105820 / 217083)

/-- Moving to a later quadrant strictly increases the ordered ray key. -/
theorem rayOrderKey_lt_of_sector_lt (u v : RVec)
    (h : (rayKey u).1 < (rayKey v).1) : rayOrderKey u < rayOrderKey v := by
  change Prod.Lex (· < ·) (· < ·) (rayKey u) (rayKey v)
  exact (Prod.lex_def.mpr (Or.inl h))

/-- Inside one sector, ordering the rational coordinate orders the ray key. -/
theorem rayOrderKey_le_of_sector_eq_of_coordinate_le (u v : RVec)
    (hsector : (rayKey u).1 = (rayKey v).1)
    (hcoordinate : (rayKey u).2 ≤ (rayKey v).2) :
    rayOrderKey u ≤ rayOrderKey v := by
  change Prod.Lex (· < ·) (· ≤ ·) (rayKey u) (rayKey v)
  exact Prod.lex_def.mpr (Or.inr ⟨hsector, hcoordinate⟩)

/-- Exact ray keys of the rational worm normals. They occur in cyclic order
`n₂,n₃,n₀,n₁` after the positive-horizontal cut. -/
theorem worm_normal_rayKeys :
    rayKey (((2 * (260 / 269 : ℚ) * (69 / 269 : ℚ) : ℚ),
      ((260 / 269 : ℚ) ^ 2 - (69 / 269 : ℚ) ^ 2 : ℚ)) : RVec) =
        (⟨0, by norm_num⟩, (62839 / 98719 : ℝ)) ∧
    rayKey (((-(260 / 269 : ℚ) : ℚ), (69 / 269 : ℚ)) : RVec) =
        (⟨1, by norm_num⟩, (260 / 329 : ℝ)) ∧
    rayKey (((0 : ℚ), (-1 : ℚ)) : RVec) =
        (⟨2, by norm_num⟩, (1 : ℝ)) ∧
    rayKey ((((260 / 269 : ℚ) : ℚ), (-(69 / 269 : ℚ) : ℚ)) : RVec) =
        (⟨3, by norm_num⟩, (260 / 329 : ℝ)) := by
  norm_num [rayKey]

/-- The exact worm normal ledger is strictly sorted after its cyclic cut. -/
theorem worm_normal_rayOrder :
    rayOrderKey wormN2 < rayOrderKey wormN3 ∧
      rayOrderKey wormN3 < rayOrderKey wormN0 ∧
      rayOrderKey wormN0 < rayOrderKey wormN1 := by
  constructor
  · apply rayOrderKey_lt_of_sector_lt
    norm_num [rayKey, wormN2, wormN3]
  constructor
  · apply rayOrderKey_lt_of_sector_lt
    norm_num [rayKey, wormN3, wormN0]
    decide
  · apply rayOrderKey_lt_of_sector_lt
    norm_num [rayKey, wormN0, wormN1]

/-- The algebraic ray key is invariant under positive rescaling. -/
theorem rayKey_pos_smul (a : ℝ) (v : RVec) (ha : 0 < a) :
    rayKey (a * v.1, a * v.2) = rayKey v := by
  simp only [rayKey]
  simp only [mul_nonneg_iff_of_pos_left ha]
  have hnonpos (x : ℝ) : a * x ≤ 0 ↔ x ≤ 0 := by
    constructor
    · intro h
      exact le_of_mul_le_mul_left (by simpa using h) ha
    · exact fun h ↦ mul_nonpos_of_nonneg_of_nonpos ha.le h
  simp only [hnonpos]
  split_ifs
  · congr 1
    convert mul_div_mul_left v.2 (v.1 + v.2) ha.ne' using 1
    all_goals ring
  · congr 1
    convert mul_div_mul_left (-v.1) (v.2 - v.1) ha.ne' using 1
    all_goals ring
  · congr 1
    convert mul_div_mul_left (-v.2) (-v.1 - v.2) ha.ne' using 1
    all_goals ring
  · congr 1
    convert mul_div_mul_left v.1 (v.1 - v.2) ha.ne' using 1
    all_goals ring

/-- The ordered ray key is invariant under positive rescaling. -/
theorem rayOrderKey_pos_smul (a : ℝ) (v : RVec) (ha : 0 < a) :
    rayOrderKey (a * v.1, a * v.2) = rayOrderKey v := by
  exact congrArg toLex (rayKey_pos_smul a v ha)

/-- Within the first quadrant, ordering by the algebraic key is exactly
counterclockwise determinant order. -/
theorem rayKey_quadrant0_le_iff (u v : RVec)
    (hu : 0 ≤ u.1 ∧ 0 ≤ u.2) (hv : 0 ≤ v.1 ∧ 0 ≤ v.2)
    (hu0 : 0 < u.1 + u.2) (hv0 : 0 < v.1 + v.2) :
    (rayKey u).2 ≤ (rayKey v).2 ↔ 0 ≤ u.1 * v.2 - u.2 * v.1 := by
  simp only [rayKey, if_pos hu, if_pos hv]
  rw [div_le_div_iff₀ hu0 hv0]
  constructor <;> intro h <;> linarith

/-- Within the second quadrant, key order is determinant order. -/
theorem rayKey_quadrant1_le_iff (u v : RVec)
    (hu : u.1 < 0 ∧ 0 ≤ u.2) (hv : v.1 < 0 ∧ 0 ≤ v.2) :
    (rayKey u).2 ≤ (rayKey v).2 ↔ 0 ≤ u.1 * v.2 - u.2 * v.1 := by
  have hu1 : ¬(0 ≤ u.1 ∧ 0 ≤ u.2) := fun h ↦ (not_le_of_gt hu.1) h.1
  have hv1 : ¬(0 ≤ v.1 ∧ 0 ≤ v.2) := fun h ↦ (not_le_of_gt hv.1) h.1
  have hu2 : u.1 ≤ 0 ∧ 0 ≤ u.2 := ⟨hu.1.le, hu.2⟩
  have hv2 : v.1 ≤ 0 ∧ 0 ≤ v.2 := ⟨hv.1.le, hv.2⟩
  have hdu : 0 < u.2 - u.1 := by linarith
  have hdv : 0 < v.2 - v.1 := by linarith
  simp only [rayKey, if_neg hu1, if_neg hv1, if_pos hu2, if_pos hv2]
  rw [div_le_div_iff₀ hdu hdv]
  constructor <;> intro h <;> linarith

/-- Within the third quadrant, key order is determinant order. -/
theorem rayKey_quadrant2_le_iff (u v : RVec)
    (hu : u.1 ≤ 0 ∧ u.2 < 0) (hv : v.1 ≤ 0 ∧ v.2 < 0) :
    (rayKey u).2 ≤ (rayKey v).2 ↔ 0 ≤ u.1 * v.2 - u.2 * v.1 := by
  have hu1 : ¬(0 ≤ u.1 ∧ 0 ≤ u.2) := fun h ↦ (not_le_of_gt hu.2) h.2
  have hv1 : ¬(0 ≤ v.1 ∧ 0 ≤ v.2) := fun h ↦ (not_le_of_gt hv.2) h.2
  have hu2 : ¬(u.1 ≤ 0 ∧ 0 ≤ u.2) := fun h ↦ (not_le_of_gt hu.2) h.2
  have hv2 : ¬(v.1 ≤ 0 ∧ 0 ≤ v.2) := fun h ↦ (not_le_of_gt hv.2) h.2
  have hu3 : u.1 ≤ 0 ∧ u.2 ≤ 0 := ⟨hu.1, hu.2.le⟩
  have hv3 : v.1 ≤ 0 ∧ v.2 ≤ 0 := ⟨hv.1, hv.2.le⟩
  have hdu : 0 < -u.1 - u.2 := by linarith
  have hdv : 0 < -v.1 - v.2 := by linarith
  simp only [rayKey, if_neg hu1, if_neg hv1, if_neg hu2, if_neg hv2,
    if_pos hu3, if_pos hv3]
  rw [div_le_div_iff₀ hdu hdv]
  constructor <;> intro h <;> linarith

/-- Within the fourth quadrant, key order is determinant order. -/
theorem rayKey_quadrant3_le_iff (u v : RVec)
    (hu : 0 < u.1 ∧ u.2 < 0) (hv : 0 < v.1 ∧ v.2 < 0) :
    (rayKey u).2 ≤ (rayKey v).2 ↔ 0 ≤ u.1 * v.2 - u.2 * v.1 := by
  have hu1 : ¬(0 ≤ u.1 ∧ 0 ≤ u.2) := fun h ↦ (not_le_of_gt hu.2) h.2
  have hv1 : ¬(0 ≤ v.1 ∧ 0 ≤ v.2) := fun h ↦ (not_le_of_gt hv.2) h.2
  have hu2 : ¬(u.1 ≤ 0 ∧ 0 ≤ u.2) := fun h ↦ (not_le_of_gt hu.1) h.1
  have hv2 : ¬(v.1 ≤ 0 ∧ 0 ≤ v.2) := fun h ↦ (not_le_of_gt hv.1) h.1
  have hu3 : ¬(u.1 ≤ 0 ∧ u.2 ≤ 0) := fun h ↦ (not_le_of_gt hu.1) h.1
  have hv3 : ¬(v.1 ≤ 0 ∧ v.2 ≤ 0) := fun h ↦ (not_le_of_gt hv.1) h.1
  have hdu : 0 < u.1 - u.2 := by linarith
  have hdv : 0 < v.1 - v.2 := by linarith
  simp only [rayKey, if_neg hu1, if_neg hv1, if_neg hu2, if_neg hv2,
    if_neg hu3, if_neg hv3]
  rw [div_le_div_iff₀ hdu hdv]
  constructor <;> intro h <;> linarith

/-- Vector subtraction. -/
def vsub (u v : RVec) : RVec := (u.1 - v.1, u.2 - v.2)

/-- The oriented planar determinant. -/
def det (u v : RVec) : ℝ := u.1 * v.2 - u.2 * v.1

/-- Dot product on the chosen pair representation. -/
def dot (u v : RVec) : ℝ := u.1 * v.1 + u.2 * v.2

/-- Clockwise rotation by a right angle. -/
def cw (u : RVec) : RVec := (u.2, -u.1)

/-- Algebraic planar rotation with cosine/sine parameters. -/
def rotate (c s : ℝ) (u : RVec) : RVec :=
  (c * u.1 - s * u.2, s * u.1 + c * u.2)

/-- Unit algebraic rotations preserve oriented determinants. -/
theorem det_rotate (c s : ℝ) (hunit : c ^ 2 + s ^ 2 = 1) (u v : RVec) :
    det (rotate c s u) (rotate c s v) = det u v := by
  calc
    det (rotate c s u) (rotate c s v) = (c ^ 2 + s ^ 2) * det u v := by
      simp only [det, rotate]
      ring
    _ = det u v := by rw [hunit]; ring

/-- Clockwise right-angle rotation commutes with every planar rotation. -/
theorem cw_rotate (c s : ℝ) (u : RVec) : cw (rotate c s u) = rotate c s (cw u) := by
  apply Prod.ext <;> simp [cw, rotate] <;> ring

/-- Unnormalised outward normal of a counterclockwise directed edge. -/
def outward (u v : RVec) : RVec := cw (vsub v u)

/-- Consequently outward edge vectors rotate equivariantly. -/
theorem outward_rotate (c s : ℝ) (u v : RVec) :
    outward (rotate c s u) (rotate c s v) = rotate c s (outward u v) := by
  simp [outward, cw, rotate, vsub]
  constructor <;> ring

/-- The edge/support pairing equals the corresponding determinant. -/
theorem dot_outward (x u v : RVec) : dot x (outward u v) = det x (vsub v u) := by
  simp [dot, outward, cw, det, vsub]
  ring

/-- Both endpoints of an edge have the same support value in its outward direction. -/
theorem edge_endpoint_support_eq (u v : RVec) :
    dot u (outward u v) = dot v (outward u v) := by
  simp [dot, outward, cw, vsub]
  ring

/-- Finite support formulation of counterclockwise polygon convexity: the
initial endpoint of every directed edge maximizes its outward functional. -/
def EdgeSupportsAll {n : ℕ} [NeZero n] (vertex : ZMod n → RVec) : Prop :=
  ∀ i j, dot (vertex j) (outward (vertex i) (vertex (i + 1))) ≤
    dot (vertex i) (outward (vertex i) (vertex (i + 1)))

/-- Under `EdgeSupportsAll`, both endpoints are active on their edge ray. -/
theorem edge_endpoints_active {n : ℕ} [NeZero n] (vertex : ZMod n → RVec)
    (hconvex : EdgeSupportsAll vertex) (i j : ZMod n) :
    dot (vertex j) (outward (vertex i) (vertex (i + 1))) ≤
      dot (vertex (i + 1)) (outward (vertex i) (vertex (i + 1))) := by
  rw [← edge_endpoint_support_eq (vertex i) (vertex (i + 1))]
  exact hconvex i j

/-! ## The concrete four-edge witness ledger

The common-fan existence problem has two logically distinct sides.  The
following exact lemmas close the source-polygon side for the rational worm:
its four outward edge vectors are positive multiples of the four advertised
unit normals, and every directed edge is genuinely supporting.  Thus an
active vertex can be advanced from `i` to `i+1` precisely at that edge ray;
no arbitrary choice among the two tied endpoints is used.
-/

/-- Exact edge-vector ledger of the rational worm hull, including the closing
edge.  Every displayed multiplier is strictly positive. -/
theorem worm_outward_ledger :
    outward (0, 0) (1 / 3, 0) = (1 / 3 : ℝ) • wormN0 ∧
    outward (1 / 3, 0) (338 / 807, 260 / 807) = (1 / 3 : ℝ) • wormN1 ∧
    outward (338 / 807, 260 / 807) (9361 / 72361, 105820 / 217083) =
      (1 / 3 : ℝ) • wormN2 ∧
    outward (9361 / 72361, 105820 / 217083) (0, 0) =
      (407 / 807 : ℝ) • wormN3 := by
  norm_num [outward, cw, vsub, wormN0, wormN1, wormN2, wormN3]

theorem worm_outward_ledger_positive :
    (0 : ℝ) < 1 / 3 ∧ (0 : ℝ) < 407 / 807 := by
  norm_num

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

/-- Cyclic reindexing does not change shoelace twice-area. -/
theorem twiceArea_addRight {n : ℕ} [NeZero n] (p : ZMod n → RVec) (a : ZMod n) :
    twiceArea (fun i ↦ p (i + a)) = twiceArea p := by
  simp only [twiceArea]
  have shift := Equiv.sum_comp (Equiv.addRight a)
    (fun i ↦ det (p i) (p (i + 1)))
  rw [← shift]
  apply Finset.sum_congr rfl
  intro i _
  congr 2
  all_goals simp [Equiv.addRight]
  all_goals ring

/-- Mixed surface sum using the support vertex of `k` selected on each edge of `p`. -/
def surface {n : ℕ} [NeZero n] (p k : ZMod n → RVec) : ℝ :=
  ∑ i, dot (k i) (outward (p i) (p (i + 1)))

/-- Simultaneous cyclic reindexing does not change a common-fan surface sum. -/
theorem surface_addRight {n : ℕ} [NeZero n] (p k : ZMod n → RVec) (a : ZMod n) :
    surface (fun i ↦ p (i + a)) (fun i ↦ k (i + a)) = surface p k := by
  simp only [surface]
  have shift := Equiv.sum_comp (Equiv.addRight a)
    (fun i ↦ dot (k i) (outward (p i) (p (i + 1))))
  rw [← shift]
  apply Finset.sum_congr rfl
  intro i _
  congr 3
  simp [Equiv.addRight]
  ring

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

/-! A direct measure computation starts with the standard right triangle. -/

def standardTriangle : Set RVec :=
  {p | 0 ≤ p.1 ∧ 0 ≤ p.2 ∧ p.1 + p.2 ≤ 1}

theorem standardTriangle_eq_convexHull :
    standardTriangle = convexHull ℝ ({(0, 0), (1, 0), (0, 1)} : Set RVec) := by
  apply Set.Subset.antisymm
  · intro p hp
    let w : Fin 3 → ℝ := ![1 - p.1 - p.2, p.1, p.2]
    let z : Fin 3 → RVec := ![(0, 0), (1, 0), (0, 1)]
    have hw0 : ∀ i ∈ Finset.univ, 0 ≤ w i := by
      intro i _
      fin_cases i <;> simp [w] <;> linarith [hp.1, hp.2.1, hp.2.2]
    have hw1 : ∑ i ∈ Finset.univ, w i = 1 := by
      simp [w, Fin.sum_univ_three]
      ring
    have hz : ∀ i ∈ Finset.univ, z i ∈
        convexHull ℝ ({(0, 0), (1, 0), (0, 1)} : Set RVec) := by
      intro i _
      apply subset_convexHull ℝ
      fin_cases i <;> simp [z]
    have hsum := (convex_convexHull ℝ
      ({(0, 0), (1, 0), (0, 1)} : Set RVec)).sum_mem hw0 hw1 hz
    simpa [w, z, Fin.sum_univ_three] using hsum
  · apply convexHull_min
    · intro p hp
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hp
      rcases hp with (rfl | rfl | rfl) <;> norm_num [standardTriangle]
    · intro p hp q hq a b ha hb hab
      rcases hp with ⟨hp1, hp2, hp3⟩
      rcases hq with ⟨hq1, hq2, hq3⟩
      change 0 ≤ (a • p + b • q).1 ∧ 0 ≤ (a • p + b • q).2 ∧
        (a • p + b • q).1 + (a • p + b • q).2 ≤ 1
      simp only [Prod.smul_fst, Prod.smul_snd, Prod.fst_add, Prod.snd_add]
      constructor
      · exact add_nonneg (mul_nonneg ha hp1) (mul_nonneg hb hq1)
      constructor
      · exact add_nonneg (mul_nonneg ha hp2) (mul_nonneg hb hq2)
      · have hpa : a * (p.1 + p.2) ≤ a := by
          simpa using mul_le_mul_of_nonneg_left hp3 ha
        have hqb : b * (q.1 + q.2) ≤ b := by
          simpa using mul_le_mul_of_nonneg_left hq3 hb
        calc
          a • p.1 + b • q.1 + (a • p.2 + b • q.2) =
              a * (p.1 + p.2) + b * (q.1 + q.2) := by
                simp only [smul_eq_mul]
                ring
          _ ≤ a + b := add_le_add hpa hqb
          _ = 1 := hab

theorem standardTriangle_ae_regionBetween :
    ∀ᵐ z ∂(MeasureTheory.volume.prod MeasureTheory.volume),
      z ∈ standardTriangle ↔
        z ∈ regionBetween (fun _ : ℝ ↦ 0) (fun x ↦ 1 - x) (Set.Icc 0 1) := by
  rw [MeasureTheory.Measure.ae_prod_iff_ae_ae]
  · filter_upwards [] with x
    by_cases hx : x ∈ Set.Icc (0 : ℝ) 1
    · filter_upwards [(MeasureTheory.Ioo_ae_eq_Icc
          (μ := MeasureTheory.volume) (a := 0) (b := 1 - x))] with y hy
      change (0 ≤ x ∧ 0 ≤ y ∧ x + y ≤ 1) ↔
        (x ∈ Set.Icc (0 : ℝ) 1 ∧ y ∈ Set.Ioo 0 (1 - x))
      have hy' : y ∈ Set.Ioo (0 : ℝ) (1 - x) ↔ y ∈ Set.Icc 0 (1 - x) :=
        iff_of_eq hy
      rw [hy']
      constructor
      · intro h
        exact ⟨hx, ⟨h.2.1, by linarith [h.2.2]⟩⟩
      · rintro ⟨_, hy0, hy1⟩
        exact ⟨hx.1, hy0, by linarith⟩
    · filter_upwards [] with y
      change (0 ≤ x ∧ 0 ≤ y ∧ x + y ≤ 1) ↔
        (x ∈ Set.Icc (0 : ℝ) 1 ∧ y ∈ Set.Ioo 0 (1 - x))
      simp only [hx, false_and, iff_false]
      rintro ⟨hx0, _, hxy⟩
      apply hx
      exact ⟨hx0, by linarith⟩
  · apply MeasurableSet.iff
    · rw [standardTriangle]
      exact (isClosed_le continuous_const continuous_fst).measurableSet.inter
        ((isClosed_le continuous_const continuous_snd).measurableSet.inter
          (isClosed_le (continuous_fst.add continuous_snd) continuous_const).measurableSet)
    · exact measurableSet_regionBetween measurable_const
        (measurable_const.sub measurable_id) measurableSet_Icc

theorem standardTriangle_volume :
    (MeasureTheory.volume.prod MeasureTheory.volume) standardTriangle =
      ENNReal.ofReal (1 / 2 : ℝ) := by
  have hmeasure : (MeasureTheory.volume.prod MeasureTheory.volume) standardTriangle =
      (MeasureTheory.volume.prod MeasureTheory.volume)
        (regionBetween (fun _ : ℝ ↦ 0) (fun x ↦ 1 - x) (Set.Icc 0 1)) := by
    apply MeasureTheory.measure_congr
    filter_upwards [standardTriangle_ae_regionBetween] with z hz
    exact propext hz
  rw [hmeasure]
  rw [volume_regionBetween_eq_integral]
  · congr 1
    simp only [Pi.sub_apply, sub_zero]
    rw [MeasureTheory.integral_Icc_eq_integral_Ioc,
      ← intervalIntegral.integral_of_le (by norm_num)]
    rw [intervalIntegral.integral_sub]
    · rw [intervalIntegral.integral_const, integral_id]
      norm_num
    · exact intervalIntegrable_const
    · exact (continuous_id : Continuous (fun x : ℝ ↦ x)).intervalIntegrable
        (a := 0) (b := 1) (μ := MeasureTheory.volume)
  · exact continuous_const.integrableOn_Icc
  · exact (continuous_const.sub continuous_id).integrableOn_Icc
  · exact measurableSet_Icc
  · intro x hx
    exact sub_nonneg.mpr hx.2

/-- For the standard triangle, product Lebesgue measure is exactly one half
of its determinant/shoelace twice-area. -/
theorem standardTriangle_measure_eq_shoelace :
    (MeasureTheory.volume.prod MeasureTheory.volume)
        (convexHull ℝ ({(0, 0), (1, 0), (0, 1)} : Set RVec)) =
      ENNReal.ofReal ((det (0, 0) (1, 0) + det (1, 0) (0, 1) +
        det (0, 1) (0, 0)) / 2) := by
  rw [← standardTriangle_eq_convexHull, standardTriangle_volume]
  norm_num [det]

/-- In coordinate space, an invertible linear map scales Lebesgue volume by
the absolute determinant.  This is the transport lemma needed to pass from
the standard triangle to an arbitrary nondegenerate triangle. -/
theorem volume_image_linearEquiv_fin2 (e : (Fin 2 → ℝ) ≃ₗ[ℝ] (Fin 2 → ℝ))
    (S : Set (Fin 2 → ℝ)) (hS : MeasurableSet S) :
    MeasureTheory.volume (e '' S) =
      ENNReal.ofReal |LinearMap.det (e : (Fin 2 → ℝ) →ₗ[ℝ] (Fin 2 → ℝ))| *
        MeasureTheory.volume S := by
  have hpre : ((e.symm : (Fin 2 → ℝ) →ₗ[ℝ] (Fin 2 → ℝ)) :
      (Fin 2 → ℝ) → (Fin 2 → ℝ)) ⁻¹' S = e '' S := by
    ext x
    constructor
    · intro hx
      exact ⟨e.symm x, hx, e.apply_symm_apply x⟩
    · rintro ⟨y, hy, rfl⟩
      simpa using hy
  have hdet : LinearMap.det (e.symm : (Fin 2 → ℝ) →ₗ[ℝ] (Fin 2 → ℝ)) ≠ 0 :=
    (e.symm.isUnit_det').ne_zero
  have hmap := Real.map_linearMap_volume_pi_eq_smul_volume_pi hdet
  have happ := congrArg (fun μ : MeasureTheory.Measure (Fin 2 → ℝ) ↦ μ S) hmap
  rw [MeasureTheory.Measure.map_apply
    ((e.symm : (Fin 2 → ℝ) →ₗ[ℝ] (Fin 2 → ℝ)).continuous_on_pi.measurable) hS,
    hpre] at happ
  simpa [LinearEquiv.det_coe_symm, MeasureTheory.Measure.smul_apply] using happ

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

/-- A triangle whose three vertices have nonnegative second coordinate lies in
the closed upper half-plane. -/
theorem triangle_subset_upper_halfplane (a b c : RVec)
    (ha : 0 ≤ a.2) (hb : 0 ≤ b.2) (hc : 0 ≤ c.2) :
    convexHull ℝ ({a, b, c} : Set RVec) ⊆ {x | 0 ≤ x.2} := by
  apply convexHull_min
  · intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with (rfl | rfl | rfl) <;> assumption
  · intro x hx y hy α β hα hβ hab
    change 0 ≤ (α • x + β • y).2
    simp only [Prod.smul_snd, Prod.snd_add]
    exact add_nonneg (mul_nonneg hα hx) (mul_nonneg hβ hy)

/-- The analogous lower-half-plane containment. -/
theorem triangle_subset_lower_halfplane (a b c : RVec)
    (ha : a.2 ≤ 0) (hb : b.2 ≤ 0) (hc : c.2 ≤ 0) :
    convexHull ℝ ({a, b, c} : Set RVec) ⊆ {x | x.2 ≤ 0} := by
  apply convexHull_min
  · intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with (rfl | rfl | rfl) <;> assumption
  · intro x hx y hy α β hα hβ hab
    change (α • x + β • y).2 ≤ 0
    simp only [Prod.smul_snd, Prod.snd_add]
    exact add_nonpos (mul_nonpos_of_nonneg_of_nonpos hα hx)
      (mul_nonpos_of_nonneg_of_nonpos hβ hy)

/-- Opposite base-apex triangles meet only on the horizontal base line. -/
theorem opposite_triangles_intersection_subset_baseLine
    (xUpper xLower hUpper hLower : ℝ) (hup : 0 ≤ hUpper) (hlow : 0 ≤ hLower) :
    convexHull ℝ ({(0, 0), (1, 0), (xUpper, hUpper)} : Set RVec) ∩
        convexHull ℝ ({(0, 0), (1, 0), (xLower, -hLower)} : Set RVec) ⊆
      {x | x.2 = 0} := by
  intro x hx
  have hnonneg := triangle_subset_upper_halfplane (0, 0) (1, 0)
    (xUpper, hUpper) (by norm_num) (by norm_num) hup hx.1
  have hnonpos := triangle_subset_lower_halfplane (0, 0) (1, 0)
    (xLower, -hLower) (by norm_num) (by norm_num) (by linarith) hx.2
  exact le_antisymm hnonpos hnonneg

/-- The horizontal base line has zero product Lebesgue measure. -/
theorem baseLine_prod_volume_zero :
    (MeasureTheory.volume.prod MeasureTheory.volume) ({x : RVec | x.2 = 0}) = 0 := by
  have hset : ({x : RVec | x.2 = 0}) = Set.univ ×ˢ ({0} : Set ℝ) := by
    ext x
    simp
  rw [hset, MeasureTheory.Measure.prod_prod, Real.volume_singleton, mul_zero]

/-- Hence the two opposite triangles overlap only in a null set. -/
theorem opposite_triangles_intersection_null
    (xUpper xLower hUpper hLower : ℝ) (hup : 0 ≤ hUpper) (hlow : 0 ≤ hLower) :
    (MeasureTheory.volume.prod MeasureTheory.volume)
      (convexHull ℝ ({(0, 0), (1, 0), (xUpper, hUpper)} : Set RVec) ∩
        convexHull ℝ ({(0, 0), (1, 0), (xLower, -hLower)} : Set RVec)) = 0 := by
  exact MeasureTheory.measure_mono_null
    (opposite_triangles_intersection_subset_baseLine xUpper xLower hUpper hLower hup hlow)
    baseLine_prod_volume_zero

/-- Product Lebesgue area is additive on the union of the opposite triangles. -/
theorem opposite_triangles_union_measure
    (xUpper xLower hUpper hLower : ℝ) (hup : 0 ≤ hUpper) (hlow : 0 ≤ hLower) :
    let upper := convexHull ℝ
      ({(0, 0), (1, 0), (xUpper, hUpper)} : Set RVec)
    let lower := convexHull ℝ
      ({(0, 0), (1, 0), (xLower, -hLower)} : Set RVec)
    (MeasureTheory.volume.prod MeasureTheory.volume) (upper ∪ lower) =
      (MeasureTheory.volume.prod MeasureTheory.volume) upper +
        (MeasureTheory.volume.prod MeasureTheory.volume) lower := by
  dsimp only
  apply MeasureTheory.measure_union₀
  · have hfinite : ({(0, 0), (1, 0), (xLower, -hLower)} : Set RVec).Finite := by
      simp
    exact ((hfinite.isCompact_convexHull ℝ).isClosed.measurableSet).nullMeasurableSet
  · exact opposite_triangles_intersection_null xUpper xLower hUpper hLower hup hlow

/-- Convex containment transfers the additive two-cap union area bound to the
containing measurable set. -/
theorem opposite_triangles_measure_sum_le_containing
    (K : Set RVec) (hKconvex : Convex ℝ K)
    (xUpper xLower hUpper hLower : ℝ) (hup : 0 ≤ hUpper) (hlow : 0 ≤ hLower)
    (h0 : (0, 0) ∈ K) (h1 : (1, 0) ∈ K)
    (hu : (xUpper, hUpper) ∈ K) (hl : (xLower, -hLower) ∈ K) :
    let upper := convexHull ℝ
      ({(0, 0), (1, 0), (xUpper, hUpper)} : Set RVec)
    let lower := convexHull ℝ
      ({(0, 0), (1, 0), (xLower, -hLower)} : Set RVec)
    (MeasureTheory.volume.prod MeasureTheory.volume) upper +
        (MeasureTheory.volume.prod MeasureTheory.volume) lower ≤
      (MeasureTheory.volume.prod MeasureTheory.volume) K := by
  dsimp only
  have hsub := opposite_base_triangles_subset_convex K hKconvex
    (0, 0) (1, 0) (xUpper, hUpper) (xLower, -hLower) h0 h1 hu hl
  rw [← opposite_triangles_union_measure xUpper xLower hUpper hLower hup hlow]
  exact MeasureTheory.measure_mono (Set.union_subset hsub.1 hsub.2)

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

/-- Convex coordinates plus a named active maximizing vertex give the exact
pointwise support comparison needed by a common fan. -/
theorem dot_le_active_of_convexCoordinates {ι : Type*} [Fintype ι]
    (weight : ι → ℝ) (vertex : ι → RVec) (point active normal : RVec)
    (weight_nonneg : ∀ i, 0 ≤ weight i)
    (weight_sum : ∑ i, weight i = 1)
    (coordinates : point = ∑ i, (weight i * (vertex i).1, weight i * (vertex i).2))
    (active_max : ∀ i, dot (vertex i) normal ≤ dot active normal) :
    dot point normal ≤ dot active normal := by
  subst point
  rw [dot_convexCombination]
  exact convexCombination_le weight (fun i ↦ dot (vertex i) normal)
    (dot active normal) weight_nonneg weight_sum active_max

/-- Convex coordinates for every support point and active-maximality of the
common-fan vertex discharge the containment-support premise pointwise. -/
theorem commonFan_support_of_coordinates {n : ℕ} [NeZero n]
    (point vertex : ZMod n → RVec) (normal : ZMod n → RVec)
    (weight : ZMod n → ZMod n → ℝ)
    (weight_nonneg : ∀ i j, 0 ≤ weight i j)
    (weight_sum : ∀ i, ∑ j, weight i j = 1)
    (coordinates : ∀ i, point i =
      ∑ j, (weight i j * (vertex j).1, weight i j * (vertex j).2))
    (active_max : ∀ i j, dot (vertex j) (normal i) ≤ dot (vertex i) (normal i)) :
    ∀ i, dot (point i) (normal i) ≤ dot (vertex i) (normal i) := by
  intro i
  exact dot_le_active_of_convexCoordinates (weight i) vertex (point i) (vertex i)
    (normal i) (weight_nonneg i) (weight_sum i) (coordinates i) (active_max i)

/-- Every linear functional on a nonempty finite vertex family has an active
maximizing vertex. -/
theorem exists_active_vertex {ι : Type*} [Finite ι] [Nonempty ι]
    (vertex : ι → RVec) (normal : RVec) :
    ∃ i, ∀ j, dot (vertex j) normal ≤ dot (vertex i) normal := by
  classical
  let _ := Fintype.ofFinite ι
  obtain ⟨i, _, hi⟩ := Finset.exists_max_image Finset.univ
    (fun j ↦ dot (vertex j) normal) Finset.univ_nonempty
  exact ⟨i, fun j ↦ hi j (Finset.mem_univ j)⟩

/-- Active maximizing vertices can be selected simultaneously on a finite fan. -/
theorem exists_active_vertices_on_fan {ι : Type*} [Finite ι] [Nonempty ι]
    {n : ℕ} [NeZero n] (vertex : ι → RVec) (normal : ZMod n → RVec) :
    ∃ active : ZMod n → ι,
      ∀ i j, dot (vertex j) (normal i) ≤ dot (vertex (active i)) (normal i) := by
  classical
  choose active hactive using fun i ↦ exists_active_vertex vertex (normal i)
  exact ⟨active, hactive⟩

/-! Merely selecting a maximizer independently on every fan ray is not enough
to build the repeated-vertex refinement.  At the right normal of the unit
square, both right endpoints maximize the same functional but differ by a
nonzero vertical edge.  This exact counterexample is why the final existence
layer must impose a coherent tie-breaking rule (or construct the repeated
vertices directly), rather than invoke `exists_active_vertices_on_fan` alone.
-/

theorem independent_active_selection_counterexample :
    let square : Fin 4 → RVec := ![(0, 0), (1, 0), (1, 1), (0, 1)]
    let normal : RVec := (1, 0)
    (∀ j, dot (square j) normal ≤ dot (square 1) normal) ∧
      (∀ j, dot (square j) normal ≤ dot (square 2) normal) ∧
      vsub (square 2) (square 1) = (0, 1) ∧
      vsub (square 2) (square 1) ≠ (0, 0) := by
  dsimp
  constructor
  · intro j
    fin_cases j <;> norm_num [dot]
  constructor
  · intro j
    fin_cases j <;> norm_num [dot]
  constructor <;> norm_num [vsub]

/-- The complete exposed vertex face of a finite polygon in direction `normal`.
Keeping this set, rather than an independently chosen representative, retains
all tie information at edge normals. -/
def exposedVertices {n : ℕ} [NeZero n] (vertex : ZMod n → RVec)
    (normal : RVec) : Set (ZMod n) :=
  {i | ∀ j, dot (vertex j) normal ≤ dot (vertex i) normal}

theorem exposedVertices_nonempty {n : ℕ} [NeZero n]
    (vertex : ZMod n → RVec) (normal : RVec) :
    (exposedVertices vertex normal).Nonempty := by
  obtain ⟨i, hi⟩ := exists_active_vertex vertex normal
  exact ⟨i, hi⟩

/-- Positive rescaling of a ray preserves its entire exposed vertex face. -/
theorem exposedVertices_pos_smul {n : ℕ} [NeZero n]
    (vertex : ZMod n → RVec) (normal : RVec) (a : ℝ) (ha : 0 < a) :
    exposedVertices vertex (a * normal.1, a * normal.2) =
      exposedVertices vertex normal := by
  ext i
  simp only [exposedVertices, Set.mem_ofPred_eq, dot]
  constructor <;> intro h j
  · have := h j
    nlinarith
  · have := h j
    nlinarith

/-- For a supporting directed edge, its whole endpoint pair belongs to the
exposed face at the edge's outward ray. -/
theorem edge_endpoints_mem_exposedVertices {n : ℕ} [NeZero n]
    (vertex : ZMod n → RVec) (hconvex : EdgeSupportsAll vertex) (i : ZMod n) :
    i ∈ exposedVertices vertex (outward (vertex i) (vertex (i + 1))) ∧
      i + 1 ∈ exposedVertices vertex (outward (vertex i) (vertex (i + 1))) := by
  exact ⟨hconvex i, edge_endpoints_active vertex hconvex i⟩

/-- Merge two finite linearly ordered fan-ray ledgers into one sorted ledger. -/
def fanMerge {α : Type*} [LinearOrder α] (a b : List α) : List α :=
  (a ++ b).mergeSort fun x y ↦ decide (x ≤ y)

/-- The merged fan-ray ledger is sorted. -/
theorem fanMerge_pairwise {α : Type*} [LinearOrder α] (a b : List α) :
    (fanMerge a b).Pairwise (· ≤ ·) := by
  exact List.pairwise_mergeSort' (· ≤ ·) (a ++ b)

/-- The merged ledger contains exactly the rays from its two inputs. -/
theorem mem_fanMerge_iff {α : Type*} [LinearOrder α] (a b : List α) (x : α) :
    x ∈ fanMerge a b ↔ x ∈ a ∨ x ∈ b := by
  change x ∈ (a ++ b).mergeSort (fun x y ↦ decide (x ≤ y)) ↔ _
  rw [(List.mergeSort_perm (a ++ b) fun x y ↦ decide (x ≤ y)).mem_iff]
  exact List.mem_append

/-- A sorted input fan occurs in order inside the merged sorted fan. -/
theorem left_sublist_fanMerge {α : Type*} [LinearOrder α] (a b : List α)
    (ha : a.SortedLE) : a.Sublist (fanMerge a b) := by
  have hp0 : a.Subperm (a ++ b) := (List.sublist_append_left a b).subperm
  have hp : a.Subperm (fanMerge a b) := by
    exact ((List.mergeSort_perm (a ++ b) fun x y ↦ decide (x ≤ y)).subperm_left).2 hp0
  exact List.sublist_of_subperm_of_sortedLE hp ha (fanMerge_pairwise a b).sortedLE

/-- The other sorted input fan also occurs in order inside the merged fan. -/
theorem right_sublist_fanMerge {α : Type*} [LinearOrder α] (a b : List α)
    (hb : b.SortedLE) : b.Sublist (fanMerge a b) := by
  have hp0 : b.Subperm (a ++ b) := (List.sublist_append_right a b).subperm
  have hp : b.Subperm (fanMerge a b) := by
    exact ((List.mergeSort_perm (a ++ b) fun x y ↦ decide (x ≤ y)).subperm_left).2 hp0
  exact List.sublist_of_subperm_of_sortedLE hp hb (fanMerge_pairwise a b).sortedLE

end Verified.Moser.PolygonBridge
