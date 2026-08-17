/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: claude, codex
-/
import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.LSeries.ZetaZeros

/-!
# Riemann Hypothesis — orientation

Landing module for RH formalisation. It contains no results yet; its job is to record the
Mathlib entry points so nobody has to rediscover them, and to serve as a worked example of the
file conventions described in `lean/README.md`.

## Mathlib entry points

Confirmed present in Mathlib `v4.33.0`:

* `riemannZeta : ℂ → ℂ` — `Mathlib/NumberTheory/LSeries/RiemannZeta.lean`
* `RiemannHypothesis : Prop` — same file, the official statement
* `riemannZetaZeros : Set ℂ` — `Mathlib/NumberTheory/LSeries/ZetaZeros.lean`
* `riemannZeta_one_sub` — the functional equation
* `riemannZeta_ne_zero_of_one_le_re` — no zeros in `1 ≤ re s`

Do not guess Mathlib names. Confirm each one with `exact?`, `#check`, or by grepping
`.lake/packages/mathlib/Mathlib/` before relying on it.
-/

namespace Verified.RiemannHypothesis

open Complex

/-- Mathlib's statement of RH, re-exported under our namespace so everything downstream refers
to one canonical `Prop` rather than a locally re-stated variant. Re-stating the target yourself
is a classic route to proving something subtly weaker than you think. -/
abbrev RH : Prop := _root_.RiemannHypothesis

/-- Sanity check that the alias really is Mathlib's statement, unfolded. This is not progress on
anything; it exists so that a broken build fails loudly and early. -/
example : RH ↔
    ∀ (s : ℂ) (_ : riemannZeta s = 0) (_ : ¬∃ n : ℕ, s = -2 * (n + 1)) (_ : s ≠ 1),
      s.re = 1 / 2 :=
  Iff.rfl

end Verified.RiemannHypothesis
