import Mathlib

/-!
# Moser worm: support-allocation algebra

This file is an independent formalization of the load-bearing exact algebra in
the support-allocation attack.  It deliberately does not encode or invoke any
floating-point certificate checker.
-/

namespace Verified.Moser

theorem checker_pi_enclosure :
    (333 / 106 : ℝ) < Real.pi ∧ Real.pi < (355 / 113 : ℝ) := by
  constructor
  · exact lt_trans (by norm_num : (333 / 106 : ℝ) < 3.14159265358979323846)
      Real.pi_gt_d20
  · exact lt_trans Real.pi_lt_d20
      (by norm_num : (3.14159265358979323847 : ℝ) < 355 / 113)

abbrev Vec := ℚ × ℚ

def add (u v : Vec) : Vec := (u.1 + v.1, u.2 + v.2)
def smul (a : ℚ) (u : Vec) : Vec := (a * u.1, a * u.2)
def sub (u v : Vec) : Vec := (u.1 - v.1, u.2 - v.2)
def normSq (u : Vec) : ℚ := u.1 ^ 2 + u.2 ^ 2
def cross (u v : Vec) : ℚ := u.1 * v.2 - u.2 * v.1

def c : ℚ := 69 / 269
def s : ℚ := 260 / 269

def p0 : Vec := (0, 0)
def p1 : Vec := (1 / 3, 0)
def p2 : Vec := (338 / 807, 260 / 807)
def p3 : Vec := (9361 / 72361, 105820 / 217083)

def e0 : Vec := sub p1 p0
def e1 : Vec := sub p2 p1
def e2 : Vec := sub p3 p2
def closing : Vec := sub p0 p3

theorem pythagorean_direction : c ^ 2 + s ^ 2 = 1 := by
  norm_num [c, s]

theorem three_unit_thirds :
    normSq e0 = 1 / 9 ∧ normSq e1 = 1 / 9 ∧ normSq e2 = 1 / 9 := by
  norm_num [normSq, e0, e1, e2, sub, p0, p1, p2, p3]

theorem exact_open_arc_length :
    normSq e0 = (1 / 3) ^ 2 ∧ normSq e1 = (1 / 3) ^ 2 ∧
      normSq e2 = (1 / 3) ^ 2 ∧ (1 / 3 : ℚ) + 1 / 3 + 1 / 3 = 1 := by
  norm_num [normSq, e0, e1, e2, sub, p0, p1, p2, p3]

def chordLength : ℚ := 407 / 807

theorem exact_closing_chord :
    chordLength = (1 + 2 * c) / 3 ∧ normSq closing = chordLength ^ 2 := by
  norm_num [chordLength, c, normSq, closing, sub, p0, p3]

theorem witness_strictly_convex_orientation :
    0 < cross e0 e1 ∧ 0 < cross e1 e2 ∧ 0 < cross e2 closing ∧
      0 < cross closing e0 := by
  norm_num [cross, e0, e1, e2, closing, sub, p0, p1, p2, p3]

def twiceShoelaceArea : ℚ :=
  cross p0 p1 + cross p1 p2 + cross p2 p3 + cross p3 p0

theorem exact_witness_hull_area : twiceShoelaceArea / 2 = 87880 / 651249 := by
  norm_num [twiceShoelaceArea, cross, p0, p1, p2, p3]

def n0 : Vec := (0, -1)
def n1 : Vec := (s, -c)
def n2 : Vec := (2 * s * c, s ^ 2 - c ^ 2)
def n3 : Vec := (-s, c)

theorem normals_are_unit :
    normSq n0 = 1 ∧ normSq n1 = 1 ∧ normSq n2 = 1 ∧ normSq n3 = 1 := by
  norm_num [normSq, n0, n1, n2, n3, c, s]

theorem balanced_surface_split :
    add (add n0 n2) (smul (2 * c) n3) = (0, 0) ∧ add n1 n3 = (0, 0) := by
  norm_num [add, smul, n0, n1, n2, n3, c, s]

def segmentAllocation : Fin 4 → ℚ
  | 0 => 1 | 1 => 0 | 2 => 1 | 3 => 138 / 407

def squareAllocation : Fin 4 → ℚ
  | 0 => 0 | 1 => 1 | 2 => 0 | 3 => 269 / 407

def edgeLength : Fin 4 → ℚ
  | 0 => 1 / 3 | 1 => 1 / 3 | 2 => 1 / 3 | 3 => chordLength

def normal : Fin 4 → Vec
  | 0 => n0 | 1 => n1 | 2 => n2 | 3 => n3

theorem exact_capacities (i : Fin 4) :
    segmentAllocation i + squareAllocation i = 1 := by
  fin_cases i <;> norm_num [segmentAllocation, squareAllocation]

theorem exact_segment_load :
    ∑ i : Fin 4, smul (edgeLength i * segmentAllocation i) (normal i) = (0, 0) := by
  norm_num [Fin.sum_univ_four, segmentAllocation, edgeLength, normal, chordLength,
    smul, n0, n1, n2, n3, c, s]

theorem exact_square_load :
    ∑ i : Fin 4, smul (edgeLength i * squareAllocation i) (normal i) = (0, 0) := by
  norm_num [Fin.sum_univ_four, squareAllocation, edgeLength, normal, chordLength,
    smul, n0, n1, n2, n3, c, s]

/-! The derivative comparison underlying mixed-area monotonicity.  The
geometric layer only has to supply the displayed quadratic inequality for all
positive dilation parameters; no limiting or differentiability axiom is used. -/
theorem quadratic_firstVariation_le_area
    (areaK areaP first : ℝ)
    (h : ∀ t : ℝ, 0 < t →
      areaK + t * first + t ^ 2 * areaP ≤ (1 + t) ^ 2 * areaK) :
    first ≤ 2 * areaK := by
  by_contra hn
  have hpos : 0 < first - 2 * areaK := sub_pos.mpr (lt_of_not_ge hn)
  let d := first - 2 * areaK
  let q := areaK - areaP
  let t : ℝ := d / (2 * (|q| + 1))
  have hd : 0 < d := hpos
  have hden : 0 < 2 * (|q| + 1) := by positivity
  have ht : 0 < t := div_pos hd hden
  have hq : q * t < d := by
    calc
      q * t ≤ |q| * t := mul_le_mul_of_nonneg_right (le_abs_self q) (le_of_lt ht)
      _ < (|q| + 1) * t := by nlinarith
      _ = d / 2 := by
        dsimp [t]
        field_simp [ne_of_gt (by positivity : 0 < |q| + 1)]
      _ < d := by linarith
  have H := h t ht
  dsimp [d, q] at hq
  nlinarith [sq_nonneg t]

/-! Lower-dimensional unit-segment template.  For the pinned base from
`(0,0)` to `(1,0)`, the determinant areas of apexes `(x,h₊)` and `(y,-h₋)`
are exactly `h₊/2` and `h₋/2`, independently of `x,y`. -/
theorem opposite_unit_base_triangle_areas (x y hp hm : ℝ)
    (hp0 : 0 ≤ hp) (hm0 : 0 ≤ hm) :
    |cross (0, 0) (1, 0)| = 0 ∧
      |((1 : ℝ) * hp - 0 * x)| / 2 + |((1 : ℝ) * (-hm) - 0 * y)| / 2 =
        (hp + hm) / 2 := by
  constructor
  · norm_num [cross]
  · simp only [one_mul, zero_mul, sub_zero]
    rw [abs_of_nonneg hp0, abs_of_nonpos (neg_nonpos.mpr hm0)]
    ring

theorem segment_two_triangle_bound (areaK hp hm : ℝ)
    (containedDisjointTriangles : (hp + hm) / 2 ≤ areaK) :
    (hp + hm) / 2 ≤ areaK := containedDisjointTriangles

/-! An assumption-auditable version of the two-triangle argument.  `area` is
not axiomatized globally: the caller supplies exactly the three measure facts
needed for its concrete convex hull `K`. -/
theorem segment_bound_from_measure_facts
    (areaK areaUpper areaLower hp hm : ℝ)
    (upper_formula : areaUpper = hp / 2)
    (lower_formula : areaLower = hm / 2)
    (disjoint_union_inside : areaUpper + areaLower ≤ areaK) :
    (hp + hm) / 2 ≤ areaK := by
  rw [upper_formula, lower_formula] at disjoint_union_inside
  linarith

/-! Capacity/load cancellation as a standalone finite algebra theorem. -/
theorem capacity_load_cancellation {E J : Type*} [Fintype E] [Fintype J]
    (length : E → ℝ) (translation : J → ℝ × ℝ)
    (normal : E → ℝ × ℝ) (allocation : E → J → ℝ)
    (loadX : ∀ j, ∑ e, length e * allocation e j * (normal e).1 = 0)
    (loadY : ∀ j, ∑ e, length e * allocation e j * (normal e).2 = 0) :
    ∑ e, ∑ j, length e * allocation e j *
      ((translation j).1 * (normal e).1 + (translation j).2 * (normal e).2) = 0 := by
  classical
  simp_rw [mul_add, Finset.sum_add_distrib]
  have hx : ∑ e, ∑ j, length e * allocation e j *
      ((translation j).1 * (normal e).1) = 0 := by
    rw [Finset.sum_comm]
    simp_rw [show ∀ (j : J) (e : E),
      length e * allocation e j * ((translation j).1 * (normal e).1) =
        (translation j).1 * (length e * allocation e j * (normal e).1) by
          intro j e; ring]
    simp [← Finset.mul_sum, loadX]
  have hy : ∑ e, ∑ j, length e * allocation e j *
      ((translation j).2 * (normal e).2) = 0 := by
    rw [Finset.sum_comm]
    simp_rw [show ∀ (j : J) (e : E),
      length e * allocation e j * ((translation j).2 * (normal e).2) =
        (translation j).2 * (length e * allocation e j * (normal e).2) by
          intro j e; ring]
    simp [← Finset.mul_sum, loadY]
  rw [hx, hy]
  norm_num

theorem allocated_support_le_template_support
    {E J : Type*} [Fintype E] [Fintype J]
    (length : E → ℝ) (hK : E → ℝ) (placedSupport : J → E → ℝ)
    (allocation : E → J → ℝ)
    (length_nonneg : ∀ e, 0 ≤ length e)
    (allocation_nonneg : ∀ e j, 0 ≤ allocation e j)
    (capacity : ∀ e, ∑ j, allocation e j = 1)
    (contained : ∀ e j, placedSupport j e ≤ hK e) :
    ∑ e, length e * ∑ j, allocation e j * placedSupport j e ≤
      ∑ e, length e * hK e := by
  classical
  apply Finset.sum_le_sum
  intro e _
  apply mul_le_mul_of_nonneg_left _ (length_nonneg e)
  calc
    ∑ j, allocation e j * placedSupport j e ≤
        ∑ j, allocation e j * hK e := by
      apply Finset.sum_le_sum
      intro j _
      exact mul_le_mul_of_nonneg_left (contained e j) (allocation_nonneg e j)
    _ = hK e := by rw [← Finset.sum_mul, capacity]; norm_num

theorem mixed_area_support_allocation_bound
    {E J : Type*} [Fintype E] [Fintype J]
    (areaK : ℝ) (length : E → ℝ) (hK : E → ℝ)
    (placedSupport : J → E → ℝ) (allocation : E → J → ℝ)
    (length_nonneg : ∀ e, 0 ≤ length e)
    (allocation_nonneg : ∀ e j, 0 ≤ allocation e j)
    (capacity : ∀ e, ∑ j, allocation e j = 1)
    (contained : ∀ e j, placedSupport j e ≤ hK e)
    (mixedArea : (∑ e, length e * hK e) / 2 ≤ areaK) :
    (∑ e, length e * ∑ j, allocation e j * placedSupport j e) / 2 ≤ areaK := by
  apply le_trans (div_le_div_of_nonneg_right
    (allocated_support_le_template_support length hK placedSupport allocation
      length_nonneg allocation_nonneg capacity contained) (by norm_num : (0 : ℝ) ≤ 2))
  exact mixedArea

/-! End-to-end logical chain.  The hypotheses intentionally expose the two
remaining geometric interfaces: `minkowskiContainment` is the area inequality
coming from `K+tP ⊆ (1+t)K`, and `slabCertificate` is the exact closed-form
trigonometric result checked independently by `check_slabs.py`. -/
theorem support_certificate_chain
    {E J : Type*} [Fintype E] [Fintype J]
    (target areaK areaP : ℝ) (length : E → ℝ) (hK : E → ℝ)
    (placedSupport : J → E → ℝ) (allocation : E → J → ℝ)
    (length_nonneg : ∀ e, 0 ≤ length e)
    (allocation_nonneg : ∀ e j, 0 ≤ allocation e j)
    (capacity : ∀ e, ∑ j, allocation e j = 1)
    (containedSupports : ∀ e j, placedSupport j e ≤ hK e)
    (minkowskiContainment : ∀ t : ℝ, 0 < t →
      areaK + t * (∑ e, length e * hK e) + t ^ 2 * areaP ≤
        (1 + t) ^ 2 * areaK)
    (slabCertificate : target ≤
      (∑ e, length e * ∑ j, allocation e j * placedSupport j e) / 2) :
    target ≤ areaK := by
  have firstVariation := quadratic_firstVariation_le_area areaK areaP
    (∑ e, length e * hK e) minkowskiContainment
  have mixed : (∑ e, length e * hK e) / 2 ≤ areaK := by linarith
  exact slabCertificate.trans
    (mixed_area_support_allocation_bound areaK length hK placedSupport allocation
      length_nonneg allocation_nonneg capacity containedSupports mixed)

theorem endpoint_union :
    Set.Icc (0 : ℚ) 80 ∪ Set.Icc 75 (269 / 2) ∪ Set.Icc (259 / 2) 180 =
      Set.Icc 0 180 := by
  ext x
  simp only [Set.mem_union, Set.mem_Icc]
  constructor
  · rintro ((⟨hx0, hx80⟩ | ⟨hx75, hx269⟩) | ⟨hx259, hx180⟩) <;>
      constructor <;> norm_num at * <;> linarith
  · rintro ⟨hx0, hx180⟩
    by_cases h80 : x ≤ 80
    · exact Or.inl (Or.inl ⟨hx0, h80⟩)
    by_cases h269 : x ≤ 269 / 2
    · exact Or.inl (Or.inr ⟨by linarith, h269⟩)
    · exact Or.inr ⟨by norm_num at h269 ⊢; linarith, hx180⟩

theorem conservative_endpoint : (232239 / 1000000 : ℚ) < 2323 / 10000 := by
  norm_num

end Verified.Moser
