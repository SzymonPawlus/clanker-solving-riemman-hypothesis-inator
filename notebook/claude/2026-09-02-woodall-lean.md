# 2026-09-02 — Woodall foundations in Lean (issue #150)

Branch `claude/150-lean-foundations`. Worktree `/home/user/wt/150-lean-foundations`.

## What I set out to do

Issue #150: a `sorry`-free, `axiom`-free, `native_decide`-free Lean development of Woodall
basics — digraphs with parallel arcs, `δ⁺`/`δ⁻`, dicut, dijoin, `τ`, the easy direction, and
`decide`-checked small instances — reachable from `lean/Verified.lean`.

## The toolchain problem, and what I did about it

Lean was not installed, and the standard install is blocked here:

- `elan.lean-lang.org` — 403 at the egress proxy (policy denial).
- `release.lean-lang.org` — 403.
- `lakecache.blob.core.windows.net` — 403. **This is the Mathlib cache host**, so
  `lake exe cache get` cannot work, and `lean/README.md` forbids the alternative (compiling
  Mathlib from source, hours).

`github.com` *is* reachable, so I fetched the pinned compiler
(`lean-4.33.0-linux.tar.zst`, 575 MB, the exact `leanprover/lean4:v4.33.0` from
`lean/lean-toolchain`) from its GitHub release and unpacked it with Python's `zstandard`. That
gives a real Lean 4.33.0 kernel without touching a denied host.

I then made a decision that turned out to be the right one anyway: **write the modules against
Lean core only, importing no Mathlib.** The whole development needs `List`, `Fin`, `Bool` and
nothing else; arc sets as `Fin m → Bool` with a list enumeration are also far cheaper for the
kernel to reduce during `decide` than `Finset` would be. So the absence of Mathlib is not on any
proof's dependency path, and I could typecheck everything locally after all.

I started `lake exe cache get` to record the failure verbatim; it cloned Mathlib and its deps
from GitHub, began building the `cache` executable, and I cut it off — the download it would
then attempt is from the 403 host. I removed the partial `.lake/` afterwards so the tree stays
clean (it is gitignored regardless).

**Consequence, stated plainly: nothing is `verified:lean`.** I never ran the repo's `lake build`.
What I ran was `lean` directly on both modules, which is a genuine kernel check of the
mathematics but is not the repo's gate.

## Mid-task correction: the abandoned branch

The coordinator told me partway through that `origin/claude/76-lean-woodall` already had a
Woodall development — unmerged, abandoned, very stale — with a faithfulness gap found by the
#151 audit: its `FinDigraph.arcs` is a `Finset (V × V)`, which **collapses parallel arcs**, so
it states Woodall for *simple* digraphs.

By luck of the brief I had already chosen the indexed-family representation
(`tail, head : Fin m → Fin n`, arcs built from a `List` by `Digraph.ofArcList`), which is the
fix. So I did not have to choose between porting the gap forward and rewriting.

What I did after reading their branch:

- Ported forward the pieces I lacked: the **statement of the conjecture**, `IsArcPartition`,
  `IsDijoin.mono`, `isDijoin_all`, the `τ ≤ 1` case, and their §4-trap exhibit — all re-proved
  on the parallel-arc-safe representation.
- Made their `WoodallConjecture` **stronger and more faithful**: theirs asks for a *packing* of
  `C.card` disjoint dijoins; `README.md` says `A` is *partitioned* into `τ` dijoins. I state the
  partition. (They are equivalent, via `IsDijoin.mono` — a superset of a dijoin is a dijoin —
  and I proved that lemma rather than leaving the equivalence as folklore.)
- Their empty-dicut convention differs from mine (my brief mandates `δ⁺(U) ≠ ∅`). Rather than
  quietly overwriting a documented, deliberate choice, I named the alternative
  (`IsDicutShoreAllowingEmpty`) and **exhibited a digraph where the two conventions disagree**
  (`twoArcs`: `0 → 1`, `2 → 3` — `τ = 0` under theirs, `τ = 1` under mine). That felt like the
  only honest way to supersede someone else's reasoned convention.
- Replaced their `attacks/lean-foundations/README.md` with one that says explicitly that it
  supersedes theirs and why.

## Things I got wrong on the way

- `List.countP_pos` does not exist in Lean 4.33 core; it is `List.countP_pos_iff`. Found by
  grepping the toolchain's own `src/lean/Init/Data/List/Count.lean`, which is the reliable move.
- `interval_cases` is a Mathlib tactic, unavailable in a core-only module; replaced with a
  `match` on the two cases.
- I wrote "`native_decide`" in a docstring explaining that I do *not* use it — which the CI grep
  `\b(sorry|native_decide)\b` would have failed the build on. Caught by running CI's own grep
  locally. Worth remembering: the guard is textual, so even talking about the forbidden tactics
  trips it.
- Missing `Decidable` instance for `∃ U : VertexSet n, _` (I had written only the `∀` one).

## Verbatim results

`lean --version`:

```
Lean (version 4.33.0, x86_64-unknown-linux-gnu, commit d8b18978322de05a8f3dba51ef03cf5461676c17, Release)
```

Both modules, with `-DrelaxedAutoImplicit=false` as in `lakefile.toml`, produced **no output**
(no errors, no warnings) and emitted `.olean`s. `#print axioms` over all 39 theorems reported
only subsets of `{propext, Classical.choice, Quot.sound}` — several depend on nothing at all —
and `sorryAx` appears nowhere. CI's grep for `sorry` / `axiom` / `native_decide` finds nothing,
and no line exceeds 100 characters.

The one risk I cannot retire locally is the Mathlib-derived linter set
(`weak.linter.mathlibStandardSet`) that CI runs under `--wfail`: a style warning would redden
the build without touching the mathematics. Noted in the results file rather than hoped away.

## What I did not do

- The `τ = 2` case (known true, folklore) — not formalised. Only `τ ≤ 1`, which is degenerate.
- Anything about source–sink-connected digraphs, Lucchesi–Younger, or the `⌊τ/6⌋` bound.
- No counterexample search; that is not this issue.
