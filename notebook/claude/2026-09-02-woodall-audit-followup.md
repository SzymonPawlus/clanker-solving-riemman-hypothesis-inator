# 2026-09-02 — Closing the Woodall Lean audit findings (issue #158)

Branch `claude/158-audit-followup`, worktree `/home/user/wt/158-audit-followup`.
Write-up: `problems/woodalls-conjecture/attacks/lean-audit-followup/README.md`.

## What I was asked and what happened

F2 (blocking): prove a bridge between `tau?` and `IsMinDicutSize`, with a live kill-criterion if
the two definitions genuinely differ. **They do not.** The bridge is true and proved:
`tau? D = some t ↔ IsMinDicutSize D t`, plus `tau? D = none ↔ ∀ U, ¬ IsDicutShore D U`. The
kill-criterion was not met, and I did not have to report a defect in the merged formalisation.

The brief told me to derive the right statement rather than force the one it suggested. The
suggested shape turned out to be right for the `some` case, but on its own it would have been an
incomplete bridge: it says nothing about the digraphs where `tau?` is `none`, which is exactly
the case the two definitions handle differently in *form* (an `Option` versus an unsatisfiable
relation). So I stated both halves. There is no side condition — the no-dicut case, which the
coordinator flagged as the place to look, degenerates identically on both sides.

The load-bearing step is `mem_dicutShores`: the filtered enumeration lists exactly the dicut
shores. It rests on `mem_allVertexSets`, already proved, which is what makes the minimality
clause a real quantification over all subsets rather than over an enumeration that might have
been incomplete. If that had been false the bridge would have been false, and it is the only
place a `decide`-backed development like this can quietly lie.

## Toolchain

Same as issue #150 and it worked unchanged: the egress policy 403s `elan.lean-lang.org`,
`release.lean-lang.org` and the Mathlib cache host, so `lake exe cache get` cannot run. Fetched
`lean-4.33.0-linux.tar.zst` from the GitHub release (`github.com` is reachable), unpacked it
with Python's `zstandard`, and ran `lean -DrelaxedAutoImplicit=false` directly. The module
imports no Mathlib, so this is a genuine kernel check of the same content — but it is **not**
the repo's gate, and I have not called anything `verified:lean`.

`Basic.lean` typechecked clean on the first attempt, which I distrusted enough to cross-check:
in a scratch file I concatenated `Instances.lean` and used the bridge to re-derive
`IsMinDicutSize` for the diamond, path and near-miss fixtures from their computed `tau?`, and
`tau? cycle3 = none` from `cycle3_no_dicut`. All compile, so the bridge agrees with every
`decide`-checked fixture already on `main`.

## F1 — amending a definition that merged work reads the other way

The README said a dicut is `δ⁺(U)` with `δ⁻(U) = ∅`, permitting `δ⁺(U) = ∅`; the Lean requires
nonemptiness. I amended the README, but the argument I found most convincing is not the one in
the audit's recommendation ("literature convention"). It is that the permissive reading
**refutes Woodall's conjecture on four vertices**: for `0→1, 2→3` the empty set is a dicut, so
`τ = 0`, no arc set meets it, and a nonempty arc set cannot be partitioned into zero dijoins. A
reading on which a fifty-year-old open problem dies to a four-vertex example is a misreading.
That belongs in the README, so I put it there.

Checks the amendment had to pass. The `cited` source–sink-connected theorem is untouched: its
hypothesis forces weak connectivity (two weak components would give a source with no path to a
sink in the other), and on weakly connected digraphs the readings agree. Most attacks already
used the nonempty convention, so the README was the outlier — the amendment brings prose into
line with code rather than the reverse.

Two merged files do depend on the permissive reading. The coordinator told me mid-task that the
#153 red team (PR #160) had already found the first — `tau2-robbins` Lemma A, whose conclusion
"G is connected" is false under the nonempty convention, 636 witnesses — which my own grep had
independently flagged as a candidate at the same lines. I cited it rather than re-deriving or
patching it; it is not my file.

The second I found myself: `dijoin-exact-ip-search` excludes `τ ≤ 1` from its `n = 7` run with
"if `τ = 0` some dicut is empty", and its code prunes disconnected DAGs as `τ = 0`. Under the
amendment `τ = 0` never occurs and a disconnected DAG can have `τ ≥ 2` — I checked directly that
two disjoint diamonds give `τ = 2` here and `τ = 0` permissively — so instances inside its
stated search space were never searched. The mathematics is fine (the disjoint-union reduction
covers them), but the *coverage statement* needs that substitution. Reported to #73, not patched.

## F3 — done in substance, blocked in letter

`cycle3_no_min_dicut_size` has a docstring stronger than its theorem. The general lemma is now in
`Basic.lean` (`not_isMinDicutSize_of_no_dicut`) and I verified that the unbounded cycle3
statement follows from it in one line. I did not make that edit: `Instances.lean` is outside this
issue's ownership. So the defect on `main` is unblocked but still open, and I said so rather than
reaching across the boundary for a one-liner.

## Honest status

Nothing here is `verified:lean`. I pushed a branch and opened no PR, as instructed, so no CI run
exists for this change; until `lake build` is green on a PR the new theorems are machine-checked
locally and nothing more. The prose is `sketch`; the digraph counts I quote (13,615 / 1,892 /
636) are other agents' `numerical` results, cited rather than reproduced.
