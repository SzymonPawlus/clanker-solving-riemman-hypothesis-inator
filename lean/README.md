# Lean — setup and workflow

The verification gate. A `sorry`-free proof here is the only way a claim reaches
`verified:lean`, the strongest status in [`../RULES.md`](../RULES.md) §3.

Package `verified`, library `Verified`, one namespace per problem
(`Verified.RiemannHypothesis`). Pinned to Lean `v4.33.0` and Mathlib `v4.33.0`.

---

## 1. One-time setup

Install `elan` (the Lean toolchain manager — it reads `lean-toolchain` and fetches the right
compiler automatically, so never install Lean by hand):

```bash
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
```

Then, from this directory, download prebuilt Mathlib artifacts and build:

```bash
cd lean
lake exe cache get     # ~5-10 min first time, downloads several GB
lake build             # ~1 min once the cache is warm
```

**`lake exe cache get` is not optional.** Skipping it makes Lean compile Mathlib from source,
which takes hours. If you ever see a build compiling thousands of `Mathlib.*` files, stop it and
run `cache get`.

Budget **~8 GB** of disk for `.lake/` (gitignored). Downloads are shared via `~/.cache/mathlib`,
so a second checkout is fast.

## 2. Daily workflow

```bash
cd lean
lake exe cache get                          # after any pull touching lean-toolchain or manifest
lake build                                  # build everything
lake build Verified.RiemannHypothesis.Basic # build one module — much faster while iterating
```

**Never run `lake update`.** It re-resolves Mathlib to a new revision, invalidates the entire
cache, and can silently break every proof in the repo. Bumping Mathlib is a human decision made
in its own PR.

Adding a module: create `Verified/<Problem>/<Name>.lean`, then add `import Verified.<Problem>.<Name>`
to `Verified.lean`. If it is not reachable from `Verified.lean`, CI never checks it — an
unimported file is not verified, however green your local build looks.

## 3. Finding Mathlib lemmas

Guessing API names is the single biggest time sink here, and a confidently invented lemma name
is worse than no attempt. In rough order of usefulness:

| Tool | Use |
|---|---|
| `exact?` | Searches for a lemma closing the current goal outright. Try this first. |
| `apply?` | Same, but allows leftover goals. |
| `rw?` | Suggests rewrites applicable at the goal. |
| `#check @Foo.bar` | Confirms a name exists and shows its exact signature. |
| `#leansearch "..."` | Natural-language search, if the service is reachable. |
| `grep -rn "pattern" .lake/packages/mathlib/Mathlib/ --include="*.lean"` | Always works, no network. |

The `grep` fallback is the reliable one for agents — the Mathlib source is on disk. Note that in
`fish`, the glob must be quoted as `--include="*.lean"` or it errors.

Naming convention: Mathlib names describe the statement, so `riemannZeta_ne_zero_of_one_le_re`
reads "ζ ≠ 0, given 1 ≤ re". Guessing *from the convention* and confirming with `#check` is a
reasonable loop; asserting a name without confirming is not.

## 4. File conventions

Mathlib's style linter is enabled and its warnings are noise you should not leave behind. Copy
the shape of `Verified/RiemannHypothesis/Basic.lean`:

```lean
/-
Copyright (c) 2026 clanker contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: <agent>
-/
import Mathlib....          -- imports come before the module docstring

/-!
# Title
Prose about the module.
-/

namespace Verified.<Problem>
...
end Verified.<Problem>
```

Every public declaration gets a `/-- ... -/` docstring saying what it means, not what it does.

## 5. What counts as verified

`sorry` is fine on a working branch and forbidden on `main`; CI rejects it. So are new `axiom`
declarations and `native_decide` — each is a way to make the checker accept something it has not
checked. If you need one, that is a discussion in the PR, not a commit.

The real check is:

```lean
#print axioms Verified.RiemannHypothesis.myTheorem
```

A genuinely verified result prints exactly `[propext, Classical.choice, Quot.sound]` — the three
standard Lean axioms. **If `sorryAx` appears, the theorem is not proved**, no matter that the
file builds and the linter is happy. `sorry` only warns; it does not fail a build. Run
`#print axioms` on anything you are about to call `verified:lean`, and paste the output in the
PR. This catches the case where a `sorry` three dependencies down quietly hollows out your
result.

## 6. Pitfalls

- **Restating the theorem.** Proving your own paraphrase instead of the canonical statement is
  the most common way to "prove" something weaker. Alias Mathlib's statement (see `RH` in
  `Basic.lean`) rather than retyping it.
- **Vacuous truth.** A hypothesis that is never satisfiable makes anything provable. If a proof
  went suspiciously smoothly, check the hypotheses are satisfiable.
- **`simp` closing a goal you did not understand.** Fine for a real proof, but do not report a
  result as understood when you cannot say why it holds.
- **Deprecation warnings** after a Mathlib bump mean the name moved; grep for the new one.

## 7. CI

`.github/workflows/lean.yml` runs `lake exe cache get && lake build` on every PR touching
`lean/`, and fails on `sorry`, `axiom`, or `native_decide` in `Verified/`. It uses
`leanprover/lean-action`, which handles elan setup and caching.

A red Lean check means the claim is not verified. Do not merge past it, and do not "fix" it by
weakening the statement.
