/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Codex
-/
import Verified.Moser.FiveSectorOrder

/-!
# Determinant-only convex-boundary sweep lemmas

Local lemmas characterizing which normal cone contains a normal maximized at a
given strict-CCW polygon vertex.  These are the geometric core of the global
last-exposed-endpoint sweep.
-/

namespace Verified.Moser.BoundarySweep

open FiveSectorOrder

def vsub (u v : RVec) : RVec := (u.1 - v.1, u.2 - v.2)

theorem det_cw_cw (u v : RVec) : det (cw u) (cw v) = det u v := by
  simp [det, cw]
  ring

theorem det_cw_left (u n : RVec) : det (cw u) n = dot u n := by
  simp [det, cw, dot]
  ring

theorem det_right_cw (n u : RVec) : det n (cw u) = -dot n u := by
  simp [det, cw, dot]
  ring

theorem dot_vsub_left (x y n : RVec) :
    dot (vsub x y) n = dot x n - dot y n := by
  simp [vsub, dot]
  ring

/-- A normal maximized at the common vertex of two successive edges lies in
the closed positive cone spanned by their clockwise outward normals.  No
angle or topology is used: the two neighboring support inequalities become
the two determinant signs defining cone membership. -/
theorem maximizer_normal_in_corner_cone
    (qPrev q qNext n : RVec)
    (hturn : 0 < det (vsub q qPrev) (vsub qNext q))
    (hPrev : dot qPrev n ≤ dot q n)
    (hNext : dot qNext n ≤ dot q n) :
    ∃ a b : ℝ, 0 ≤ a ∧ 0 ≤ b ∧
      n =
        (a * (cw (vsub q qPrev)).1 + b * (cw (vsub qNext q)).1,
         a * (cw (vsub q qPrev)).2 + b * (cw (vsub qNext q)).2) := by
  apply exists_nonnegative_cone_coefficients
  · simpa [det_cw_cw] using hturn
  · rw [det_cw_left, dot_vsub_left]
    linarith
  · rw [det_right_cw]
    have : dot n (vsub qNext q) = dot (vsub qNext q) n := by
      simp [dot]
      ring
    rw [this, dot_vsub_left]
    linarith

/-- Family form consumed by a finite polygon: global maximality immediately
supplies the two neighboring inequalities. -/
theorem global_maximizer_normal_in_corner_cone {ι : Type*}
    (vertex : ι → RVec) (iPrev i iNext : ι) (n : RVec)
    (hturn : 0 < det (vsub (vertex i) (vertex iPrev))
      (vsub (vertex iNext) (vertex i)))
    (hmax : ∀ j, dot (vertex j) n ≤ dot (vertex i) n) :
    ∃ a b : ℝ, 0 ≤ a ∧ 0 ≤ b ∧
      n =
        (a * (cw (vsub (vertex i) (vertex iPrev))).1 +
            b * (cw (vsub (vertex iNext) (vertex i))).1,
         a * (cw (vsub (vertex i) (vertex iPrev))).2 +
            b * (cw (vsub (vertex iNext) (vertex i))).2) := by
  exact maximizer_normal_in_corner_cone _ _ _ _ hturn (hmax iPrev) (hmax iNext)

/-- If a point is strictly below at at least one of two bounding normals, it
is strictly below throughout every positive combination using both normals. -/
theorem strict_support_in_open_normal_cone
    (x p n₀ n₁ : RVec) (a b : ℝ) (ha : 0 < a) (hb : 0 < b)
    (h₀ : dot x n₀ ≤ dot p n₀) (h₁ : dot x n₁ ≤ dot p n₁)
    (hstrict : dot x n₀ < dot p n₀ ∨ dot x n₁ < dot p n₁) :
    dot x (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) <
      dot p (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) := by
  rcases hstrict with hs | hs
  · have hsa := mul_lt_mul_of_pos_left hs ha
    have hwb := mul_le_mul_of_nonneg_left h₁ (le_of_lt hb)
    calc
      dot x (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) =
          a * dot x n₀ + b * dot x n₁ := by simp [dot]; ring
      _ < a * dot p n₀ + b * dot p n₁ := add_lt_add_of_lt_of_le hsa hwb
      _ = dot p (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) := by
        simp [dot]
        ring
  · have hwa := mul_le_mul_of_nonneg_left h₀ (le_of_lt ha)
    have hsb := mul_lt_mul_of_pos_left hs hb
    calc
      dot x (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) =
          a * dot x n₀ + b * dot x n₁ := by simp [dot]; ring
      _ < a * dot p n₀ + b * dot p n₁ := add_lt_add_of_le_of_lt hwa hsb
      _ = dot p (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) := by
        simp [dot]
        ring

/-- In a strict polygon corner, a normal in the open adjacent-normal cone has
the corner as its unique maximizing vertex.  The hypothesis `separates`
states the determinant-free strict-convexity fact that every other vertex is
strictly below at least one adjacent supporting edge. -/
theorem unique_maximizer_in_open_corner {ι : Type*}
    (vertex : ι → RVec) (i : ι) (n₀ n₁ : RVec) (a b : ℝ)
    (ha : 0 < a) (hb : 0 < b)
    (support₀ : ∀ j, dot (vertex j) n₀ ≤ dot (vertex i) n₀)
    (support₁ : ∀ j, dot (vertex j) n₁ ≤ dot (vertex i) n₁)
    (separates : ∀ j, j ≠ i →
      dot (vertex j) n₀ < dot (vertex i) n₀ ∨
        dot (vertex j) n₁ < dot (vertex i) n₁) :
    ∀ j, j ≠ i →
      dot (vertex j)
          (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) <
        dot (vertex i)
          (a * n₀.1 + b * n₁.1, a * n₀.2 + b * n₁.2) := by
  intro j hj
  exact strict_support_in_open_normal_cone _ _ _ _ _ _ ha hb
    (support₀ j) (support₁ j) (separates j hj)

/-- Exact exposed-edge face under the global supporting-edge hypothesis. The
two endpoints tie and strictness excludes every other listed vertex. -/
theorem maximizers_at_strict_supporting_edge {ι : Type*}
    (vertex : ι → RVec) (iStart iEnd : ι) (n : RVec)
    (hendpoints : dot (vertex iStart) n = dot (vertex iEnd) n)
    (hsupport : ∀ j, dot (vertex j) n ≤ dot (vertex iEnd) n)
    (hstrict : ∀ j, j ≠ iStart → j ≠ iEnd →
      dot (vertex j) n < dot (vertex iEnd) n) :
    ∀ j, dot (vertex j) n = dot (vertex iEnd) n ↔
      j = iStart ∨ j = iEnd := by
  intro j
  constructor
  · intro hj
    by_cases hs : j = iStart
    · exact Or.inl hs
    by_cases he : j = iEnd
    · exact Or.inr he
    exact (ne_of_lt (hstrict j hs he) hj).elim
  · rintro (rfl | rfl)
    · exact hendpoints
    · rfl

/-- Half-open normal-sector selector. The incoming edge ray is included: at
that ray `q` is the last of the two exposed endpoints. Inside the sector, `q`
is the unique maximizer. The outgoing ray is intentionally excluded and is
owned by the next vertex. -/
theorem halfOpen_sector_support_and_uniqueness {ι : Type*}
    (vertex : ι → RVec) (i : ι) (nPrev nNext : RVec) (a b : ℝ)
    (ha : 0 < a) (hb : 0 ≤ b)
    (supportPrev : ∀ j, dot (vertex j) nPrev ≤ dot (vertex i) nPrev)
    (supportNext : ∀ j, dot (vertex j) nNext ≤ dot (vertex i) nNext)
    (separates : ∀ j, j ≠ i →
      dot (vertex j) nPrev < dot (vertex i) nPrev ∨
        dot (vertex j) nNext < dot (vertex i) nNext) :
    (∀ j, dot (vertex j)
        (a * nPrev.1 + b * nNext.1, a * nPrev.2 + b * nNext.2) ≤
      dot (vertex i)
        (a * nPrev.1 + b * nNext.1, a * nPrev.2 + b * nNext.2)) ∧
    (0 < b → ∀ j, j ≠ i →
      dot (vertex j)
          (a * nPrev.1 + b * nNext.1, a * nPrev.2 + b * nNext.2) <
        dot (vertex i)
          (a * nPrev.1 + b * nNext.1, a * nPrev.2 + b * nNext.2)) := by
  constructor
  · exact supports_nonnegative_normal_cone vertex (vertex i) nPrev nNext a b
      (le_of_lt ha) hb supportPrev supportNext
  · intro hbpos
    exact unique_maximizer_in_open_corner vertex i nPrev nNext a b ha hbpos
      supportPrev supportNext separates

/-! ## Advancing a maximizer to the half-open owner cone -/

def cyclicEdge {m : ℕ} [NeZero m] (vertex : ZMod m → RVec) (i : ZMod m) : RVec :=
  vsub (vertex (i + 1)) (vertex i)

def cyclicNormal {m : ℕ} [NeZero m] (vertex : ZMod m → RVec) (i : ZMod m) : RVec :=
  cw (cyclicEdge vertex i)

theorem cyclic_edge_endpoints_tie {m : ℕ} [NeZero m]
    (vertex : ZMod m → RVec) (i : ZMod m) :
    dot (vertex (i + 1)) (cyclicNormal vertex i) =
      dot (vertex i) (cyclicNormal vertex i) := by
  simp only [cyclicNormal, cyclicEdge]
  rw [← sub_eq_zero]
  rw [← dot_vsub_left]
  simp [vsub, dot, cw]
  ring

/-- If a chosen maximizer lies on the outgoing boundary of its closed normal
cone, advance once across that exposed edge. The result owns the normal in the
half-open convention: its incoming coefficient is strictly positive and its
outgoing coefficient is nonnegative. This is the exact tie-breaking operation
needed by the global sweep. -/
theorem exists_halfOpen_owner_of_maximizer {m : ℕ} [NeZero m]
    (vertex : ZMod m → RVec) (ν : RVec) (i : ZMod m)
    (hν : ν ≠ (0, 0))
    (turn : ∀ r, 0 < det (cyclicEdge vertex r) (cyclicEdge vertex (r + 1)))
    (edgeSupport : ∀ r j,
      dot (vertex j) (cyclicNormal vertex r) ≤
        dot (vertex r) (cyclicNormal vertex r))
    (hmax : ∀ j, dot (vertex j) ν ≤ dot (vertex i) ν) :
    ∃ owner a b, 0 < a ∧ 0 ≤ b ∧
      ν =
        (a * (cyclicNormal vertex (owner - 1)).1 +
            b * (cyclicNormal vertex owner).1,
         a * (cyclicNormal vertex (owner - 1)).2 +
            b * (cyclicNormal vertex owner).2) ∧
      ∀ j, dot (vertex j) ν ≤ dot (vertex owner) ν := by
  obtain ⟨a, b, ha, hb, hab⟩ :=
    global_maximizer_normal_in_corner_cone vertex (i - 1) i (i + 1) ν
      (by simpa [cyclicEdge, sub_eq_add_neg, add_assoc] using turn (i - 1)) hmax
  by_cases hapos : 0 < a
  · exact ⟨i, a, b, hapos, hb, by simpa [cyclicNormal, cyclicEdge] using hab, hmax⟩
  · have ha0 : a = 0 := le_antisymm (le_of_not_gt hapos) ha
    have hbpos : 0 < b := by
      by_contra hbnot
      have hbzero : b = 0 := le_antisymm (le_of_not_gt hbnot) hb
      apply hν
      rw [hab, ha0, hbzero]
      simp
    have hνout : ν =
        (b * (cyclicNormal vertex i).1, b * (cyclicNormal vertex i).2) := by
      simpa [cyclicNormal, cyclicEdge, ha0] using hab
    refine ⟨i + 1, b, 0, hbpos, le_rfl, ?_, ?_⟩
    · rw [hνout]
      simp only [sub_eq_add_neg]
      congr 1 <;> simp
    · intro j
      have hj := mul_le_mul_of_nonneg_left (edgeSupport i j) hb
      have hend := cyclic_edge_endpoints_tie vertex i
      calc
        dot (vertex j) ν = b * dot (vertex j) (cyclicNormal vertex i) := by
          rw [hνout]
          simp [dot]
          ring
        _ ≤ b * dot (vertex i) (cyclicNormal vertex i) := hj
        _ = b * dot (vertex (i + 1)) (cyclicNormal vertex i) := by rw [hend]
        _ = dot (vertex (i + 1)) ν := by
          rw [hνout]
          simp [dot]
          ring

/-- A linear functional attains its maximum on the finite cyclic vertex
ledger. -/
theorem exists_cyclic_maximizer {m : ℕ} [NeZero m]
    (vertex : ZMod m → RVec) (ν : RVec) :
    ∃ i, ∀ j, dot (vertex j) ν ≤ dot (vertex i) ν := by
  classical
  obtain ⟨i, _, hi⟩ := Finset.exists_max_image Finset.univ
    (fun j ↦ dot (vertex j) ν) Finset.univ_nonempty
  exact ⟨i, fun j ↦ hi j (Finset.mem_univ j)⟩

/-- Global half-open owner existence. Under strict turns and the genuinely
global condition that every directed edge supports every listed vertex, each
nonzero normal is owned by some vertex's half-open adjacent-normal cone, and
that owner maximizes the normal. This is the determinant-only exposed-face
sweep existence theorem; the half-open convention advances across flat edge
ties rather than choosing their endpoints independently. -/
theorem exists_halfOpen_owner {m : ℕ} [NeZero m]
    (vertex : ZMod m → RVec) (ν : RVec) (hν : ν ≠ (0, 0))
    (turn : ∀ r, 0 < det (cyclicEdge vertex r) (cyclicEdge vertex (r + 1)))
    (edgeSupport : ∀ r j,
      dot (vertex j) (cyclicNormal vertex r) ≤
        dot (vertex r) (cyclicNormal vertex r)) :
    ∃ owner a b, 0 < a ∧ 0 ≤ b ∧
      ν =
        (a * (cyclicNormal vertex (owner - 1)).1 +
            b * (cyclicNormal vertex owner).1,
         a * (cyclicNormal vertex (owner - 1)).2 +
            b * (cyclicNormal vertex owner).2) ∧
      ∀ j, dot (vertex j) ν ≤ dot (vertex owner) ν := by
  obtain ⟨i, hi⟩ := exists_cyclic_maximizer vertex ν
  exact exists_halfOpen_owner_of_maximizer vertex ν i hν turn edgeSupport hi

/-! ## Exact failure of local-turn-only hypotheses

Positive consecutive turns and full dimensionality do not imply that a closed
ledger is a convex boundary: it may wind as a star.  The global sweep theorem
must assume edge support (or an equivalent simple convex-boundary condition). -/

def starVertex : Fin 5 → RVec :=
  ![(0, 3), (-2, -3), (3, 1), (-3, 1), (2, -3)]

def starNext : Fin 5 → Fin 5 := ![1, 2, 3, 4, 0]

def starEdge (i : Fin 5) : RVec :=
  vsub (starVertex (starNext i)) (starVertex i)

/-- The rational pentagram has a positive local turn at every vertex. -/
theorem star_all_local_turns_positive (i : Fin 5) :
    0 < det (starEdge i) (starEdge (starNext i)) := by
  fin_cases i <;> simp [starEdge, starVertex, starNext, vsub, det] <;> norm_num

/-- It is genuinely two-dimensional. -/
theorem star_full_dimensional : det (starEdge 0) (starEdge 1) ≠ 0 := by
  simp [starEdge, starVertex, starNext, vsub, det]
  norm_num

/-- Its edge vectors nevertheless close exactly. -/
theorem star_edges_close :
    starEdge 0 + starEdge 1 + starEdge 2 + starEdge 3 + starEdge 4 = (0, 0) := by
  simp [starEdge, starVertex, starNext, vsub]

/-- The first directed edge is not supporting: vertex 3 lies strictly beyond
its clockwise normal.  Thus a sweep lemma based only on closure, dimension,
and positive local turns is false. -/
theorem star_local_turns_do_not_give_edge_support :
    dot (starVertex 0) (cw (starEdge 0)) <
      dot (starVertex 3) (cw (starEdge 0)) := by
  simp [starVertex, starEdge, starNext, vsub, cw, dot]
  norm_num

end Verified.Moser.BoundarySweep
