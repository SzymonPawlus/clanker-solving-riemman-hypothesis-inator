# 2026-09-04 — Woodall: restoring `results/` §4 compliance, and what the per-row check found

Issue #267. Branch `claude/267-woodall-results-s4`, worktree `agent-a652c2b522e462676`, based on
`origin/main` at `12fa645`.

## The problem

`problems/woodalls-conjecture/results/` held `.gitkeep` and `woodall-lean-basics.md`. Repo
`RULES.md` §4 admits only `cited` / `verified:lean` / `verified:review` into `results/`. Every
one of that file's 25 table rows read "not verified", and the file said so itself: "No statement
in this note is `verified:lean`. CI has not run on this branch." So the only substantive file in
`results/` was entirely below the bar.

The interesting part is *why* it was below the bar. The mathematics was fine; the author simply
could not reach `lakecache.blob.core.windows.net` from their session, so they could not run
`lake build`, so they honestly refused to claim `verified:lean` and wrote the caveat. Good
discipline — and it left a stale blocker sitting in `results/` for two days. Worth remembering:
an honest "I could not check this" ages into a rules violation if nobody comes back for it.

## Route taken: A, partial

Route A (promote), with three rows corrected rather than promoted as written.

### CI evidence I actually confirmed

I did not take the "CI is green now" claim on trust.

- `gh run view 33804022050` — workflow `Lean`, event `push`, branch `main`, conclusion
  `success`, 2026-09-03T20:44:35Z, head SHA `a9cd3c619f80111b607a3ed0fbe3ece802ddcb68`.
- `git log --diff-filter=A` puts the two Woodall modules in `ad78d86`;
  `git merge-base --is-ancestor ad78d86 a9cd3c6` → true. So the green run is downstream of the
  commit that added them, and they were present in its tree (`git ls-tree` confirms).
- `git diff a9cd3c6 origin/main -- lean/` is **empty** — nothing in `lean/` has moved since.
- Both modules are imported from `Verified.lean`, which is `defaultTargets` in `lakefile.toml`.
  I checked this explicitly because `lean/README.md` warns that an unimported module is never
  checked no matter how green the build. If they had not been imported, the green run would have
  been evidence of nothing.

That last check is the one I would have skipped if I were being lazy, and it is the one that
could have invalidated the whole route.

### Local reproduction

Not enough to read CI. `lake exe cache get && lake build --wfail` in my own worktree, on the
toolchain `lean-toolchain` pins (Lean 4.33.0, `d8b1897`), Mathlib `v4.33.0`: **exit 0**, 3580
jobs, both Woodall modules built, no linter failure under `--wfail`. The cache fetch worked here
— `~/.cache/mathlib` was already warm from the main checkout, and egress to the cache host was
open this session. (Per the memory note on egress recheck: it flips between sessions. The
previous author's failure was real; so was my success.)

CI's exact grep for `sorry` / `axiom` / `native_decide` over `Verified/` returns nothing
(exit 1). `#print axioms` on all 42 declarations: every one a subset of
`{propext, Classical.choice, Quot.sound}`, no `sorryAx` anywhere. Four depend on **no** axioms.

### Per-row `#check` — the part that mattered

I `#check`ed all 40 named declarations and read each elaborated signature against the row's
prose. This found **three** rows whose Lean statement is weaker than what the row claimed. All
three in the same direction, which is the direction §4 exists to catch.

**D1. `cycle3_no_min_dicut_size : ∀ (t : Nat), t ≤ 3 → ¬IsMinDicutSize cycle3 t`.** The row said
"hence no τ" and the Lean docstring says "no natural number is the minimum dicut size". It is
bounded by `t ≤ 3`. The unbounded fact is genuinely available from `cycle3_tau` plus
`tau?_eq_none_iff_not_exists`, so nothing is *wrong* here — but it is a different declaration,
and a reader citing `cycle3_no_min_dicut_size` for the unbounded claim would be citing something
that does not say it.

**D2. `cycle3_empty_isDijoin : IsDijoin cycle3 fun x => false`.** The row said "every arc set is
vacuously a dijoin there"; the docstring says "Every arc set — including the empty one". The
theorem covers exactly one arc set. Again the general fact is true and one line from
`cycle3_no_dicut`, and my Python check confirms it for all 8 arc sets — but it is not proved
under that name.

**D3. `diamond_two_le_tau : [diamondJ₁, diamondJ₂].length ≤ 2`.** This is `2 ≤ 2`. It is
provable by `rfl` and mentions `diamond` nowhere in its statement. The *proof term* does route
through `length_le_tau`, `diamond_tau` and both dijoin lemmas, which is presumably the intent,
but the citable statement is a tautology.

D1 and D2 are also defects in the Lean docstrings themselves. I deliberately did not touch
`lean/` — a `results/` promotion is the wrong PR to edit formal sources in, and the fix wants its
own review. Follow-up belongs on the formalisation issue.

None of the three is a case of something *false* being claimed. But "the docstring is stronger
than the theorem" is exactly how a weaker result gets cited as a stronger one three months later,
and it is the second time this repo has hit that shape (the superseded
`origin/claude/76-lean-woodall` stated Woodall for simple digraphs only, via `Finset (V × V)`).

### Independent cross-check of the fixtures

Per problem `RULES.md`, reading someone else's checker is not verification. I reimplemented
`delta^+`, `delta^-`, dicut shore, dijoin and τ in Python **from the README's definitions**,
without consulting `Basic.lean`, and recomputed every fixture:
`notebook/claude/2026-09-04-woodall-results-s4-assets/xcheck-dicut-tau.py`.

All 21 checks agree with the Lean: `cycle3` has no dicut shore and τ undefined; `path3` has
shores exactly `{0}`, `{0,1}` and τ = 1; `diamond` τ = 2 with `{0}, {0,1}, {0,2}, {0,1,2}` as
shores; `nearMiss` τ = 1; `twoArcs` τ = 1 strictly and `{0,1}` permissive-but-not-strict. A sweep
over every digraph with `n ≤ 4, m ≤ 3` found no τ = 0, matching `not_isMinDicutSize_zero`.

Writing this from the README rather than the Lean was worth it for one reason: it forced me to
re-derive the "dicuts are nonempty" convention independently, and my `permissive_shores` vs
`dicut_shores` split reproduces `twoArcs_conventions_disagree` from scratch.

## What stays open

`WoodallConjecture` is a `Prop`, stated and not proved. It stays **open**, and I want to be
plain that nothing in this promotion moves it: `length_le_card_deltaOut` and `length_le_tau` are
the trivial direction the problem README explicitly warns proves nothing, and
`woodall_of_isMinDicutSize_le_one` is the τ = 1 corner where the single dijoin is all of `A`.
Promoting 24 rows to `verified:lean` makes the *scaffolding* citable. It is not progress.

## Meta

The one-hour budget was never at risk — the Mathlib cache was warm, so `cache get` + build ran in
a few minutes. Starting the build in the background before reading the Lean sources was the right
call and I would do it again; if the cache had been cold I would have had the read-through done
by the time it finished, and could have fallen back to Route B with the row analysis already in
hand.

The thing I nearly got wrong: my first instinct was to check that the build was green and promote
all 25 rows. The three defects only surfaced because I read the elaborated `#check` output rather
than the docstrings. Docstrings are prose by the same author who wrote the prose in the results
file, so they are *correlated* with the error, not a check on it. The signature is the artifact.
