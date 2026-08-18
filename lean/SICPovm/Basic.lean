/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Flow-25
-/
import Mathlib

/-!
# Explicit SIC-POVMs in dimensions two and three

This module mirrors the coordinate content of
`FormalConjectures.OpenQuantumProblems.23` without importing that external package.  Its
`StateVector d` is `EuclideanSpace ℂ (Fin d)`; its norm-one condition is equivalent (by
squaring the nonnegative Euclidean norm) to the sum of coordinate `Complex.normSq`s below being
one. Its `overlapSq` is definitionally the same conjugate coordinate sum followed by
`Complex.normSq`. Thus
`HasSICPOVM` below is the coordinate-level equivalent of the external predicate: it asks for
`d ^ 2` normalized complex vectors with every distinct squared overlap equal to `(d + 1)⁻¹`.
-/

namespace Verified.SICPovm

/-- A state vector represented by its complex coordinates. -/
abbrev StateVector (d : ℕ) := Fin d → ℂ

/-- Coordinate form of unit `L²` norm. -/
def IsNormalized {d : ℕ} (ψ : StateVector d) : Prop :=
  ∑ i, Complex.normSq (ψ i) = 1

/-- Squared magnitude of the usual complex inner product. -/
def overlapSq {d : ℕ} (φ ψ : StateVector d) : ℝ :=
  Complex.normSq (∑ i, star (φ i) * ψ i)

/-- The squared overlap required of a SIC in dimension `d`. -/
noncomputable def sicOverlapSq (d : ℕ) : ℝ := (d + 1 : ℝ)⁻¹

/-- A coordinate SIC family: `d²` normalized vectors with the prescribed distinct overlaps. -/
def IsSICFamily (d : ℕ) (Φ : Fin (d ^ 2) → StateVector d) : Prop :=
  (∀ i, IsNormalized (Φ i)) ∧
    ∀ i j, i ≠ j → overlapSq (Φ i) (Φ j) = sicOverlapSq d

/-- Existence of a coordinate SIC family. -/
def HasSICPOVM (d : ℕ) : Prop := ∃ Φ, IsSICFamily d Φ

private noncomputable def a : ℝ := Real.sqrt (1 / 3)
private noncomputable def b : ℝ := Real.sqrt (2 / 3)
private noncomputable def ω : ℂ := (-1 / 2 : ℝ) + (Real.sqrt 3 / 2) * Complex.I

/-- The four tetrahedral qubit states. -/
noncomputable def qubitFamily : Fin 4 → StateVector 2
  | 0 => ![1, 0]
  | 1 => ![a, b]
  | 2 => ![a, b * ω]
  | 3 => ![a, b * ω ^ 2]

private lemma sqrt_three_sq : (Real.sqrt 3) ^ 2 = 3 := by norm_num
private lemma sqrt_three_four : (Real.sqrt 3) ^ 4 = 9 := by
  rw [show (Real.sqrt 3) ^ 4 = ((Real.sqrt 3) ^ 2) ^ 2 by ring, sqrt_three_sq]
  norm_num
private lemma sqrt_three_cube : (Real.sqrt 3) ^ 3 = 3 * Real.sqrt 3 := by
  calc
    (Real.sqrt 3) ^ 3 = (Real.sqrt 3) ^ 2 * Real.sqrt 3 := by ring
    _ = 3 * Real.sqrt 3 := by rw [sqrt_three_sq]
private lemma a_sq : a ^ 2 = 1 / 3 := by
  simp only [a]
  rw [Real.sq_sqrt]
  norm_num
private lemma b_sq : b ^ 2 = 2 / 3 := by
  simp only [b]
  rw [Real.sq_sqrt]
  norm_num

private lemma a_mul_self : a * a = 1 / 3 := by simpa [pow_two] using a_sq
private lemma b_mul_self : b * b = 2 / 3 := by simpa [pow_two] using b_sq
private lemma b_four : b ^ 4 = 4 / 9 := by rw [show b ^ 4 = (b ^ 2) ^ 2 by ring, b_sq]; norm_num
private lemma omega_re : ω.re = -1 / 2 := by simp [ω]
private lemma omega_im : ω.im = Real.sqrt 3 / 2 := by simp [ω]
private lemma omega_sq_re : (ω ^ 2).re = -1 / 2 := by
  simp [ω, pow_two]
  nlinarith [sqrt_three_sq]
private lemma omega_sq_im : (ω ^ 2).im = -(Real.sqrt 3 / 2) := by
  simp [ω, pow_two]
  ring
private lemma star_omega : star ω = ω ^ 2 := by
  apply Complex.ext <;> simp [omega_re, omega_im, omega_sq_re, omega_sq_im]
private lemma star_omega_sq : star (ω ^ 2) = ω := by
  calc
    star (ω ^ 2) = star ω ^ 2 := map_pow (starRingEnd ℂ) ω 2
    _ = (ω ^ 2) ^ 2 := by rw [star_omega]
    _ = ω := by
      apply Complex.ext <;>
        simp [pow_two, omega_re, omega_im] <;>
        ring_nf <;> nlinarith [sqrt_three_sq, sqrt_three_cube]
private lemma starMap_omega_sq_re : ((starRingEnd ℂ) ω ^ 2).re = -1 / 2 := by
  have h := congrArg Complex.re star_omega_sq
  simpa [omega_re] using h
private lemma starMap_omega_sq_im : ((starRingEnd ℂ) ω ^ 2).im = Real.sqrt 3 / 2 := by
  have h := congrArg Complex.im star_omega_sq
  simpa [omega_im] using h

/-- Every tetrahedral qubit state is exactly normalized. -/
theorem qubitFamily_normalized (i : Fin 4) : IsNormalized (qubitFamily i) := by
  fin_cases i <;>
    simp [IsNormalized, qubitFamily, Fin.sum_univ_succ, Complex.normSq,
      omega_re, omega_im, omega_sq_re, omega_sq_im, a_mul_self, b_mul_self] <;>
    ring_nf <;> simp only [sqrt_three_sq, b_sq] at * <;>
    norm_num at *

/-- Every distinct tetrahedral pair has squared overlap `1/3`. -/
theorem qubitFamily_pairwise :
    ∀ i j, i ≠ j → overlapSq (qubitFamily i) (qubitFamily j) = sicOverlapSq 2 := by
  intro i j hij
  fin_cases i <;> fin_cases j <;>
    simp_all [overlapSq, sicOverlapSq, qubitFamily, Fin.sum_univ_succ,
      Complex.normSq, omega_re, omega_im,
      omega_sq_re, omega_sq_im, starMap_omega_sq_re, starMap_omega_sq_im,
      a_mul_self] <;>
    ring_nf <;> simp only [sqrt_three_sq, sqrt_three_four, b_sq, b_four] at * <;>
    norm_num at *

/-- The tetrahedral family witnesses a SIC-POVM in dimension two. -/
theorem hasSICPOVM_two : HasSICPOVM 2 := by
  refine ⟨qubitFamily, qubitFamily_normalized, ?_⟩
  exact qubitFamily_pairwise

private noncomputable def s : ℝ := Real.sqrt (1 / 2)

/-- The nine Hesse qutrit states. -/
noncomputable def hesseFamily : Fin 9 → StateVector 3
  | 0 => ![0, s, -s]
  | 1 => ![0, s, -(s * ω)]
  | 2 => ![0, s, -(s * ω ^ 2)]
  | 3 => ![-s, 0, s]
  | 4 => ![-(s * ω), 0, s]
  | 5 => ![-(s * ω ^ 2), 0, s]
  | 6 => ![s, -s, 0]
  | 7 => ![s, -(s * ω), 0]
  | 8 => ![s, -(s * ω ^ 2), 0]

private lemma s_sq : s ^ 2 = 1 / 2 := by
  simp only [s]
  rw [Real.sq_sqrt]
  norm_num
private lemma s_mul_self : s * s = 1 / 2 := by simpa [pow_two] using s_sq
private lemma s_four : s ^ 4 = 1 / 4 := by rw [show s ^ 4 = (s ^ 2) ^ 2 by ring, s_sq]; norm_num

/-- Every Hesse qutrit state is exactly normalized. -/
theorem hesseFamily_normalized (i : Fin 9) : IsNormalized (hesseFamily i) := by
  fin_cases i <;>
    simp [IsNormalized, hesseFamily, Fin.sum_univ_succ, Complex.normSq,
      omega_re, omega_im, omega_sq_re, omega_sq_im, s_mul_self] <;>
    ring_nf <;> simp only [sqrt_three_sq, s_sq] at * <;> norm_num at *

/-- Every distinct Hesse pair has squared overlap `1/4`. -/
theorem hesseFamily_pairwise :
    ∀ i j, i ≠ j → overlapSq (hesseFamily i) (hesseFamily j) = sicOverlapSq 3 := by
  intro i j hij
  fin_cases i <;> fin_cases j <;>
    simp_all [overlapSq, sicOverlapSq, hesseFamily, Fin.sum_univ_succ,
      Complex.normSq, omega_re, omega_im,
      omega_sq_re, omega_sq_im, starMap_omega_sq_re, starMap_omega_sq_im,
      s_mul_self] <;>
    ring_nf <;> simp only [sqrt_three_sq, sqrt_three_four, s_sq, s_four] at * <;> norm_num at *

/-- The Hesse family witnesses a SIC-POVM in dimension three. -/
theorem hasSICPOVM_three : HasSICPOVM 3 := by
  refine ⟨hesseFamily, hesseFamily_normalized, ?_⟩
  exact hesseFamily_pairwise

/-- The four normalized BB84 states, used as a negative control. -/
noncomputable def bb84Family : Fin 4 → StateVector 2
  | 0 => ![1, 0]
  | 1 => ![0, 1]
  | 2 => ![s, s]
  | 3 => ![s, -s]

/-- BB84 has the right cardinality but is not a SIC family. -/
theorem bb84Family_not_isSICFamily : ¬IsSICFamily 2 bb84Family := by
  intro h
  have h01 := h.2 (0 : Fin 4) (1 : Fin 4) (by decide)
  norm_num [overlapSq, sicOverlapSq, bb84Family, Complex.normSq] at h01

#print axioms hasSICPOVM_two
#print axioms hasSICPOVM_three
#print axioms bb84Family_not_isSICFamily

end Verified.SICPovm
