# Woodall basics in Lean — status of each statement

Issue #150. Sources: [`lean/Verified/Woodall/Basic.lean`](../../../lean/Verified/Woodall/Basic.lean),
[`lean/Verified/Woodall/Instances.lean`](../../../lean/Verified/Woodall/Instances.lean).
Design notes and convention choices:
[`../attacks/lean-foundations/README.md`](../attacks/lean-foundations/README.md).

## The headline, first

**The easy direction is not Woodall's conjecture.** `problems/woodalls-conjecture/README.md`
says it without hedging: "One direction is trivial — `τ` disjoint dijoins each consume an arc of
the minimum dicut, so there can never be more than `τ`. **The conjecture is the existence
direction**, and any 'proof' that only establishes the easy inequality has proved nothing."

`length_le_card_deltaOut` and `length_le_tau` below are exactly that trivial inequality.
`WoodallConjecture` is *stated* and is *not proved*. Nothing in this development may be cited as
progress on Woodall's conjecture, because there is none.

## Status of every claim

**No statement in this note is `verified:lean`.** CI has not run on this branch, and I could not
run the repo's own `lake build` locally (§ "What the toolchain actually did"). `verified:lean`
is granted by a green CI build on the pinned toolchain, and I do not have one. The statuses
below are therefore the *maximum* each statement can reach once CI is green, together with what
I actually observed.

| Lean declaration | Statement | Observed locally | Status now |
|---|---|---|---|
| `length_le_card_deltaOut` | pairwise arc-disjoint dijoins number ≤ \|δ⁺(U)\| for any dicut | compiles, clean axioms | not verified |
| `length_le_tau` | …hence ≤ τ — **the trivial half** | compiles, clean axioms | not verified |
| `length_le_countP` | list-counting core of the above | compiles, clean axioms | not verified |
| `countP_erase_of_mem` | elementary `List` lemma | compiles, clean axioms | not verified |
| `mem_allVertexSets` | the subset enumeration is complete | compiles, clean axioms | not verified |
| `nonempty_and_proper_of_isDicutShore` | a dicut shore is nonempty and proper | compiles, clean axioms | not verified |
| `one_le_card_deltaOut` | a dicut has ≥ 1 arc | compiles, clean axioms | not verified |
| `not_isMinDicutSize_zero` | τ = 0 impossible under this convention | compiles, clean axioms | not verified |
| `isMinDicutSize_unique` | τ is single-valued | compiles, clean axioms | not verified |
| `IsDijoin.mono` | a superset of a dijoin is a dijoin | compiles, clean axioms | not verified |
| `isDijoin_all` | `A` is a dijoin | compiles, clean axioms | not verified |
| `woodall_of_isMinDicutSize_one` | **conjecture for τ = 1** (degenerate) | compiles, clean axioms | not verified |
| `woodall_of_isMinDicutSize_le_one` | **conjecture for τ ≤ 1** (degenerate) | compiles, clean axioms | not verified |
| `isDicutShoreAllowingEmpty_of_isDicutShore` | this file's dicut notion is the stronger one | compiles, clean axioms | not verified |
| `cycle3_no_dicut` | the directed 3-cycle has **no** dicut | `decide`, clean axioms | not verified |
| `cycle3_no_min_dicut_size`, `cycle3_tau` | hence no τ; `tau? = none` | `decide`, clean axioms | not verified |
| `cycle3_empty_isDijoin` | every arc set is vacuously a dijoin there | `decide`, clean axioms | not verified |
| `cycle3_trap` | `{0}` has δ⁺ ≠ ∅ yet is **not** a dicut shore | `decide`, clean axioms | not verified |
| `path3_dicutShores` | the path's dicuts are exactly its two prefix cuts | `decide`, clean axioms | not verified |
| `path3_tau`, `path3_tau?` | τ = 1 for the path | `decide`, clean axioms | not verified |
| `diamond_tau`, `diamond_tau?` | **τ = 2 for the diamond** | `decide`, clean axioms | not verified |
| `diamondJ₁_isDijoin`, `diamondJ₂_isDijoin` | the two `s`–`t` paths are dijoins | `decide`, clean axioms | not verified |
| `diamond_disjoint`, `diamond_partition` | they are disjoint and partition `A` | `decide`, clean axioms | not verified |
| `diamond_two_le_tau` | the easy bound, instantiated | compiles, clean axioms | not verified |
| `nearMiss_tau`, `nearMiss_tau?`, `nearMiss_shore` | τ = 1 for `s₁→t₁, s₂→t₁, s₂→t₂` | `decide`, clean axioms | not verified |
| `nearMiss_all_isDijoin`, `nearMiss_two_sources` | `A` is a dijoin; two sources | `decide`, clean axioms | not verified |
| `twoArcs_conventions_disagree` | the two dicut conventions differ on a disconnected digraph | `decide`, clean axioms | not verified |
| `twoArcs_tau`, `twoArcs_woodall`, `path3_woodall`, `nearMiss_woodall` | τ = 1 instances of the conjecture | compiles, clean axioms | not verified |
| `WoodallConjecture` | **the conjecture** | *a definition; not proved* | **open** |

"clean axioms" means `#print axioms` reported only from `{propext, Classical.choice,
Quot.sound}` and in particular **never `sorryAx`**. Full output is in the notebook entry.

There is no `sorry`, no `axiom` declaration and no `native_decide` in either file; the repo's CI
grep pattern was run locally against both and reports nothing.

## What the toolchain actually did

The repo's build (`lake exe cache get` then `lake build`) **could not be completed**, because
this session's egress policy denies the two hosts it needs. Verbatim:

```
$ curl -sS -o /dev/null https://release.lean-lang.org/
curl: (56) CONNECT tunnel failed, response 403
$ curl -sS -o /dev/null https://lakecache.blob.core.windows.net/
curl: (56) CONNECT tunnel failed, response 403
```

and from the proxy's own status endpoint:

```
{"kind":"connect_rejected",
 "detail":"gateway answered 403 to CONNECT (policy denial or upstream failure)",
 "host":"lakecache.blob.core.windows.net:443"}
```

`lakecache.blob.core.windows.net` is where `lake exe cache get` fetches prebuilt Mathlib
artifacts, so the Mathlib cache is unobtainable here. Building Mathlib from source is explicitly
ruled out by `lean/README.md` and by the compute budget, and was not attempted.

What *was* possible: `github.com` is reachable, so the pinned compiler
(`leanprover/lean4:v4.33.0`, the exact toolchain in `lean/lean-toolchain`) was fetched from its
GitHub release and run directly:

```
$ lean --version
Lean (version 4.33.0, x86_64-unknown-linux-gnu, commit d8b18978322de05a8f3dba51ef03cf5461676c17, Release)
$ lean -DrelaxedAutoImplicit=false Verified/Woodall/Basic.lean
$ lean -DrelaxedAutoImplicit=false Verified/Woodall/Instances.lean
```

Both produced **no output at all** — no errors and no warnings — and both `.olean` files were
emitted. The `#print axioms` audit above was run in the same way.

### What that does and does not establish

It **does** establish that the real Lean 4.33.0 kernel accepts every declaration, that every
`decide` really does reduce in the kernel, and that no proof depends on `sorryAx`. Both modules
import nothing outside Lean core — deliberately, since the definitions need only `List`, `Fin`
and `Bool` — so the absent Mathlib is not on any proof's dependency path.

It **does not** establish that `lake build` is green. Not checked locally: the Mathlib-derived
linters enabled by `weak.linter.mathlibStandardSet` in `lean/lakefile.toml`, which CI runs with
`--wfail`, so a style warning there would fail CI even though the mathematics is unaffected; and
that the rest of the `Verified` library still builds alongside these modules (they add no
imports to it, so this should be unaffected). Both are checkable only by CI.

**Therefore: nothing here is `verified:lean`.** If CI comes back green the statements marked
"not verified" above become `verified:lean`; if it comes back red they stay where they are. Do
not upgrade any status in this table without a green build to point at.

## Faithfulness — what an audit should attack

The formal statements were written to be defensible; the places to push are:

1. **Parallel arcs.** Arcs are an indexed family `Fin m → Fin n`, so listing the same endpoint
   pair twice yields two distinct arcs. The superseded branch `origin/claude/76-lean-woodall`
   used `Finset (V × V)` and so stated Woodall *for simple digraphs only* — strictly weaker.
   That gap is the reason this development replaces it.
2. **`δ⁻(U) = ∅` is required**, per problem `RULES.md` §4. `cycle3_trap` exhibits a `U` with
   `δ⁺(U) ≠ ∅` that is correctly rejected.
3. **The conjecture is stated as a genuine partition** of `A` (`IsArcPartition`: every arc in
   exactly one member), matching `README.md`, not as the weaker "some disjoint family".
4. **Empty dicuts are excluded** — a real divergence from the superseded branch, exhibited by
   `twoArcs_conventions_disagree` rather than glossed over. See the attacks README.
5. **The `decide` proofs prove the quantified statements**, not an enumeration. The `Decidable`
   instances go through `decidable_of_iff` against `mem_allVertexSets`, which *proves* the
   subset enumeration is complete. A reviewer should check `mem_allVertexSets` specifically,
   since everything decided over `∀ U : VertexSet n` rests on it.
6. **Non-vacuity.** `IsMinDicutSize` carries the existence of a dicut, so `path3_tau`,
   `diamond_tau`, `nearMiss_tau` and `twoArcs_tau` cannot be vacuously true; `cycle3_trap` and
   `twoArcs_conventions_disagree` each assert a positive conjunct as well as a negative one.
