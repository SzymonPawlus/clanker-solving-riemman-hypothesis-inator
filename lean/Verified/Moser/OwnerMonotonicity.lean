/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Codex
-/
import Verified.Moser.BoundarySweep

/-!
# Monotonicity of half-open normal-cone owners

After cutting and unwrapping a cyclic strict-convex boundary, its outward edge
rays form a strictly increasing linear ledger.  This file proves that half-open
owner indices are monotone with the cut normals and packages the five-cut case.
-/

namespace Verified.Moser.OwnerMonotonicity

/-- A cut lies in the half-open interval owned by index `i`. The incoming
boundary is included and the outgoing boundary is excluded, matching the
last-exposed-endpoint convention of `BoundarySweep`. -/
def OwnsInterval {α : Type*} [LinearOrder α]
    (ray : ℕ → α) (cut : α) (i : ℕ) : Prop :=
  ray i ≤ cut ∧ cut < ray (i + 1)

/-- Half-open interval owners in a strictly increasing ray ledger are unique. -/
theorem owner_unique {α : Type*} [LinearOrder α]
    (ray : ℕ → α) (hray : StrictMono ray) (cut : α) {i j : ℕ}
    (hi : OwnsInterval ray cut i) (hj : OwnsInterval ray cut j) : i = j := by
  apply le_antisymm
  · by_contra hji
    have hsucc : j + 1 ≤ i := Nat.succ_le_iff.mpr (Nat.lt_of_not_ge hji)
    have hrle : ray (j + 1) ≤ ray i := hray.monotone hsucc
    exact (not_lt_of_ge (hrle.trans hi.1)) hj.2
  · by_contra hij
    have hsucc : i + 1 ≤ j := Nat.succ_le_iff.mpr (Nat.lt_of_not_ge hij)
    have hrle : ray (i + 1) ≤ ray j := hray.monotone hsucc
    exact (not_lt_of_ge (hrle.trans hj.1)) hi.2

/-- Ordered cuts have ordered half-open owners. This is the linearized form of
the global exposed-face sweep lemma. -/
theorem owner_mono_of_cut_le {α : Type*} [LinearOrder α]
    (ray : ℕ → α) (hray : StrictMono ray) {c d : α} {i j : ℕ}
    (hcd : c ≤ d) (hi : OwnsInterval ray c i) (hj : OwnsInterval ray d j) :
    i ≤ j := by
  by_contra h
  have hsucc : j + 1 ≤ i := Nat.succ_le_iff.mpr (Nat.lt_of_not_ge h)
  have hrle : ray (j + 1) ≤ ray i := hray.monotone hsucc
  have : ray (j + 1) ≤ d := hrle.trans (hi.1.trans hcd)
  exact (not_lt_of_ge this) hj.2

/-- Strictly ordered cuts can share an owner, but can never reverse owner
order. They have distinct owners precisely when a boundary ray separates them. -/
theorem owner_mono_of_cut_lt {α : Type*} [LinearOrder α]
    (ray : ℕ → α) (hray : StrictMono ray) {c d : α} {i j : ℕ}
    (hcd : c < d) (hi : OwnsInterval ray c i) (hj : OwnsInterval ray d j) :
    i ≤ j :=
  owner_mono_of_cut_le ray hray hcd.le hi hj

/-- The exact five-cut consequence used by the Moser bridge after one cyclic
cut unwraps both normal ledgers. -/
theorem five_owners_monotone {α : Type*} [LinearOrder α]
    (ray : ℕ → α) (hray : StrictMono ray)
    (c0 c1 c2 c3 c4 : α) (t0 t1 t2 t3 t4 : ℕ)
    (hcuts : c0 ≤ c1 ∧ c1 ≤ c2 ∧ c2 ≤ c3 ∧ c3 ≤ c4)
    (h0 : OwnsInterval ray c0 t0) (h1 : OwnsInterval ray c1 t1)
    (h2 : OwnsInterval ray c2 t2) (h3 : OwnsInterval ray c3 t3)
    (h4 : OwnsInterval ray c4 t4) :
    t0 ≤ t1 ∧ t1 ≤ t2 ∧ t2 ≤ t3 ∧ t3 ≤ t4 := by
  exact ⟨owner_mono_of_cut_le ray hray hcuts.1 h0 h1,
    owner_mono_of_cut_le ray hray hcuts.2.1 h1 h2,
    owner_mono_of_cut_le ray hray hcuts.2.2.1 h2 h3,
    owner_mono_of_cut_le ray hray hcuts.2.2.2 h3 h4⟩

/-! ## Consecutive boundary blocks -/

open Verified.Moser.FiveSectorOrder (RVec)
open Verified.Moser.BoundarySweep (vsub)

/-- Endpoint reached after the first `t` vectors of a linearly unwrapped
boundary ledger. -/
def prefixEndpoint (base : RVec) (edges : List RVec) (t : ℕ) : RVec :=
  base + (edges.take t).sum

/-- The consecutive edge block after prefix `a` and through prefix `b`. -/
def edgeBlock (edges : List RVec) (a b : ℕ) : List RVec :=
  (edges.drop a).take (b - a)

/-- Every ordered boundary block sums to the difference of its prefix
endpoints. This statement is independent of geometry and tolerates empty
blocks when two cuts have the same owner. -/
theorem edgeBlock_sum_eq_endpoint_vsub (base : RVec) (edges : List RVec)
    {a b : ℕ} (hab : a ≤ b) :
    (edgeBlock edges a b).sum =
      vsub (prefixEndpoint base edges b) (prefixEndpoint base edges a) := by
  have hb : b = a + (b - a) := (Nat.add_sub_of_le hab).symm
  have htake : (edges.take b).sum =
      (edges.take a).sum + ((edges.drop a).take (b - a)).sum := by
    rw [hb, List.take_add, List.sum_append]
    simp
  rw [edgeBlock, prefixEndpoint, prefixEndpoint, vsub]
  have hx := congrArg Prod.fst htake
  have hy := congrArg Prod.snd htake
  apply Prod.ext <;> simp only
  · simp only [Prod.fst_add] at hx ⊢
    linarith
  · simp only [Prod.snd_add] at hy ⊢
    linarith

/-- Five monotone lifted owners produce the five consecutive blocks required
by PR #189. `t5` is the next-cycle lift of `t0`; `hcycle` identifies their
prefix endpoints after one closed boundary traversal. -/
theorem five_blocks_from_monotone_owners
    (base : RVec) (edges : List RVec)
    (t0 t1 t2 t3 t4 t5 : ℕ)
    (hmono : t0 ≤ t1 ∧ t1 ≤ t2 ∧ t2 ≤ t3 ∧ t3 ≤ t4 ∧ t4 ≤ t5)
    (hcycle : prefixEndpoint base edges t5 = prefixEndpoint base edges t0) :
    let k0 := prefixEndpoint base edges t0
    let k1 := prefixEndpoint base edges t1
    let k2 := prefixEndpoint base edges t2
    let k3 := prefixEndpoint base edges t3
    let k4 := prefixEndpoint base edges t4
    (edgeBlock edges t4 t5).sum = vsub k0 k4 ∧
      (edgeBlock edges t0 t1).sum = vsub k1 k0 ∧
      (edgeBlock edges t1 t2).sum = vsub k2 k1 ∧
      (edgeBlock edges t2 t3).sum = vsub k3 k2 ∧
      (edgeBlock edges t3 t4).sum = vsub k4 k3 := by
  dsimp only
  constructor
  · rw [edgeBlock_sum_eq_endpoint_vsub base edges hmono.2.2.2.2, hcycle]
  constructor
  · exact edgeBlock_sum_eq_endpoint_vsub base edges hmono.1
  constructor
  · exact edgeBlock_sum_eq_endpoint_vsub base edges hmono.2.1
  constructor
  · exact edgeBlock_sum_eq_endpoint_vsub base edges hmono.2.2.1
  · exact edgeBlock_sum_eq_endpoint_vsub base edges hmono.2.2.2.1

/-- Combined five-cut sweep theorem. The geometric layer from PR #197 supplies
the half-open owners; a simple strict-convex boundary supplies the unwrapped
strict ray ledger. This theorem returns both cyclic owner order and every block
sum needed by PR #189, including the next-cycle wrap block. -/
theorem five_cut_sweep_blocks {α : Type*} [LinearOrder α]
    (ray : ℕ → α) (hray : StrictMono ray)
    (c0 c1 c2 c3 c4 : α) (t0 t1 t2 t3 t4 t5 : ℕ)
    (hcuts : c0 ≤ c1 ∧ c1 ≤ c2 ∧ c2 ≤ c3 ∧ c3 ≤ c4)
    (h0 : OwnsInterval ray c0 t0) (h1 : OwnsInterval ray c1 t1)
    (h2 : OwnsInterval ray c2 t2) (h3 : OwnsInterval ray c3 t3)
    (h4 : OwnsInterval ray c4 t4) (ht5 : t4 ≤ t5)
    (base : RVec) (edges : List RVec)
    (hcycle : prefixEndpoint base edges t5 = prefixEndpoint base edges t0) :
    let k0 := prefixEndpoint base edges t0
    let k1 := prefixEndpoint base edges t1
    let k2 := prefixEndpoint base edges t2
    let k3 := prefixEndpoint base edges t3
    let k4 := prefixEndpoint base edges t4
    (t0 ≤ t1 ∧ t1 ≤ t2 ∧ t2 ≤ t3 ∧ t3 ≤ t4) ∧
      (edgeBlock edges t4 t5).sum = vsub k0 k4 ∧
      (edgeBlock edges t0 t1).sum = vsub k1 k0 ∧
      (edgeBlock edges t1 t2).sum = vsub k2 k1 ∧
      (edgeBlock edges t2 t3).sum = vsub k3 k2 ∧
      (edgeBlock edges t3 t4).sum = vsub k4 k3 := by
  dsimp only
  have hm := five_owners_monotone ray hray c0 c1 c2 c3 c4
    t0 t1 t2 t3 t4 hcuts h0 h1 h2 h3 h4
  refine ⟨hm, ?_⟩
  exact five_blocks_from_monotone_owners base edges t0 t1 t2 t3 t4 t5
    ⟨hm.1, hm.2.1, hm.2.2.1, hm.2.2.2, ht5⟩ hcycle

end Verified.Moser.OwnerMonotonicity
