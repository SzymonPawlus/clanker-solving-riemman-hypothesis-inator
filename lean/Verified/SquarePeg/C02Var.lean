/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: codex
-/
import Mathlib.Analysis.Complex.Basic
import Mathlib.Data.ENNReal.Basic
import Mathlib.Topology.Order.OrderClosed

/-!
# Vanishing critical 2-variation: verified elementary core

This module formalizes only algebraic and finite-sum components of the proposed
`C^{0,2-var}` Square Peg argument. It does not assert the Square Peg theorem.
The analytic approximation criterion and its nondegeneracy conclusion are kept
as separate proposition parameters in `conditional_positive_square`.
-/

namespace Verified.SquarePeg.C02Var

/-- Abstract fine-mesh squared-variation data. The extended nonnegative reals
make possible infinite variation explicit rather than silently coercing it to a
real number. `finiteScale` records the finiteness witness needed before real
square-root estimates can be used. -/
structure VanishingVariationData where
  w2sq : ℝ → ENNReal
  finiteScale : ∃ δ : ℝ, 0 < δ ∧ w2sq δ ≠ ⊤
  vanishes : Filter.Tendsto w2sq (nhdsWithin 0 (Set.Ioi 0)) (nhds 0)

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

/-- Purely conditional dependency interface. `analyticCriterion` represents
the exact Asano--Ike approximation theorem only after its primary statement is
verified. `nondegeneracy` is deliberately separate: no four-distinct-vertices
or positive-square conclusion follows from the analytic criterion alone. -/
theorem conditional_positive_square
    {AnalyticData RectangleConclusion PositiveSquare : Prop}
    (data : AnalyticData)
    (analyticCriterion : AnalyticData → RectangleConclusion)
    (nondegeneracy : RectangleConclusion → PositiveSquare) :
    PositiveSquare :=
  nondegeneracy (analyticCriterion data)

end Verified.SquarePeg.C02Var
