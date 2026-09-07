# Woodall basics in Lean — machine-checked statements

Issues #150 (the formalisation), #267 (this promotion). Sources:
[`lean/Verified/Woodall/Basic.lean`](../../../lean/Verified/Woodall/Basic.lean),
[`lean/Verified/Woodall/Instances.lean`](../../../lean/Verified/Woodall/Instances.lean).
Design notes and convention choices:
[`../attacks/lean-foundations/README.md`](../attacks/lean-foundations/README.md).

## The headline, first

**The easy direction is not Woodall's conjecture.** `problems/woodalls-conjecture/README.md`
says it without hedging: "One direction is trivial — `τ` disjoint dijoins each consume an arc of
the minimum dicut, so there can never be more than `τ`. **The conjecture is the existence
direction**, and any 'proof' that only establishes the easy inequality has proved nothing."

`length_le_card_deltaOut` and `length_le_tau` below are exactly that trivial inequality.
`WoodallConjecture` is *stated* and is *not proved*: it remains **open**. Nothing in this
development may be cited as progress on Woodall's conjecture, because there is none. Everything
here is definitional scaffolding plus five small fixtures.

## Verification evidence

The earlier revision of this file recorded every row as "not verified", because its author could
not reach the Mathlib cache host and CI had not run on their branch. That caveat is now **stale**
and has been discharged. What was checked, on 2026-09-04:

**1. Lean CI on `main` is green and covers these files.**

| | |
|---|---|
| Workflow run | `33804022050` (`Lean`), event `push`, branch `main` |
| Conclusion | `success`, 2026-09-03T20:44:35Z |
| Head SHA | `a9cd3c619f80111b607a3ed0fbe3ece802ddcb68` |
| Commit that added the two modules | `ad78d86`, confirmed an **ancestor** of `a9cd3c6` |
| `git diff a9cd3c6 origin/main -- lean/` | **empty** — the `lean/` tree is unchanged since that run |

Both modules are imported from `lean/Verified.lean`, which is the `defaultTargets` of
`lean/lakefile.toml`, so `lake build` genuinely reaches them. (An unimported module is never
checked, however green the build; that was verified explicitly rather than assumed.)

**2. The build was reproduced locally on the pinned toolchain**, not taken on trust from CI:

```
$ lean --version   # inside lean/, i.e. the version elan selects from lean-toolchain
Lean (version 4.33.0, x86_64-unknown-linux-gnu, commit d8b18978322de05a8f3dba51ef03cf5461676c17)
$ lake exe cache get && lake build --wfail
...
✔ [3575/3580] Built Verified.Woodall.Basic (402ms)
✔ [3576/3580] Built Verified.Woodall.Instances (429ms)
Build completed successfully (3580 jobs).
```

Exit code 0 under `--wfail`, the flag CI uses, so the Mathlib style linters are clean too.
Mathlib pinned at `v4.33.0` per `lake-manifest.json`.

**3. No `sorry`, no added `axiom`, no `native_decide`.** CI's exact grep pattern, run locally
against `Verified/` and `Verified.lean`, matches nothing:

```
$ grep -rnE '\b(sorry|native_decide)\b|^[[:space:]]*axiom\b' Verified/ Verified.lean
$ echo $?
1
```

**4. `#print axioms` on every declaration below.** Each reports a subset of
`{propext, Classical.choice, Quot.sound}` — the three standard Lean axioms — and in particular
**`sorryAx` appears nowhere**. Several are stronger than required: `IsDijoin.mono`,
`isDijoin_all`, `diamond_disjoint` and `diamond_partition` depend on **no axioms at all**.

**5. Every row was `#check`ed individually.** Each named declaration was confirmed to exist and
its full elaborated signature was read against the prose in the table. This turned up three
defects, recorded in *Faithfulness defects found* below; the table has been corrected to say
what the Lean actually proves.

**6. The instance values were cross-checked by independent reimplementation.** `dicut`, `dijoin`
and `τ` were reimplemented from scratch in Python against the definitions in
`problems/woodalls-conjecture/README.md` — *not* by reading the Lean — and used to recompute
every fixture: `cycle3` has no dicut shore and no `τ`; `path3` has shores exactly `{0}` and
`{0,1}` with `τ = 1`; `diamond` has `τ = 2`; `nearMiss` has `τ = 1` with shore `{0}`;
`twoArcs` has `τ = 1` and `{0,1}` is a permissive-convention shore but not a strict one; and the
two diamond paths are disjoint dijoins partitioning `A`. All 21 checks agree with the Lean. A
sweep over every digraph with `n ≤ 4`, `m ≤ 3` found no `τ = 0`, agreeing with
`not_isMinDicutSize_zero`. Script: `experiments/`-style but not a `results/` numeric; it is
reproduced in the PR for #267 and in the notebook entry, and it is corroboration of the
*definitions*, not an independent proof of anything.

## Status of every claim

Every row below is **`verified:lean`** except the last, which is **open**.

| Lean declaration | What the Lean statement actually says | Status |
|---|---|---|
| `length_le_card_deltaOut` | pairwise arc-disjoint dijoins number ≤ \|δ⁺(U)\| for any dicut shore `U` | `verified:lean` |
| `length_le_tau` | …hence ≤ τ — **the trivial half** | `verified:lean` |
| `length_le_countP` | list-counting core of the above | `verified:lean` |
| `countP_erase_of_mem` | elementary `List` lemma | `verified:lean` |
| `mem_allVertexSets` | the subset enumeration is complete, for every `n` | `verified:lean` |
| `nonempty_and_proper_of_isDicutShore` | a dicut shore is nonempty and proper | `verified:lean` |
| `one_le_card_deltaOut` | a dicut has ≥ 1 arc | `verified:lean` |
| `not_isMinDicutSize_zero` | τ = 0 impossible under this convention, for every digraph | `verified:lean` |
| `isMinDicutSize_unique` | τ is single-valued | `verified:lean` |
| `IsDijoin.mono` | a superset of a dijoin is a dijoin | `verified:lean` |
| `isDijoin_all` | `A` is a dijoin | `verified:lean` |
| `woodall_of_isMinDicutSize_one` | **conjecture for τ = 1** (degenerate) | `verified:lean` |
| `woodall_of_isMinDicutSize_le_one` | **conjecture for τ ≤ 1** (degenerate) | `verified:lean` |
| `isDicutShoreAllowingEmpty_of_isDicutShore` | this file's dicut notion is the stronger one | `verified:lean` |
| `cycle3_no_dicut` | the directed 3-cycle has **no** dicut, over all `U : VertexSet 3` | `verified:lean` |
| `cycle3_no_min_dicut_size` | ⚠ **only** that no `t ≤ 3` is its minimum dicut size — see D1 | `verified:lean` |
| `cycle3_tau` | `tau? cycle3 = none` (this *is* the unbounded statement, via `tau?_eq_none_iff_not_exists`) | `verified:lean` |
| `cycle3_empty_isDijoin` | ⚠ **only** that the *empty* arc set is a dijoin there — see D2 | `verified:lean` |
| `cycle3_trap` | `{0}` has δ⁺ ≠ ∅ yet is **not** a dicut shore | `verified:lean` |
| `path3_dicutShores` | the path's dicut shores are exactly `{0}` and `{0,1}` (an `↔`, all `U`) | `verified:lean` |
| `path3_tau`, `path3_tau?` | τ = 1 for the path, relationally and computably | `verified:lean` |
| `diamond_tau`, `diamond_tau?` | **τ = 2 for the diamond** | `verified:lean` |
| `diamondJ₁_isDijoin`, `diamondJ₂_isDijoin` | the two `s`–`t` paths are dijoins | `verified:lean` |
| `diamond_disjoint`, `diamond_partition` | they are disjoint and every arc lies in exactly one | `verified:lean` |
| `diamond_two_le_tau` | ⚠ as *stated* this is `2 ≤ 2` and carries no digraph content — see D3 | `verified:lean` |
| `nearMiss_tau`, `nearMiss_tau?`, `nearMiss_shore` | τ = 1 for `s₁→t₁, s₂→t₁, s₂→t₂`, shore `{s₁}` | `verified:lean` |
| `nearMiss_all_isDijoin`, `nearMiss_two_sources` | `A` is a dijoin; vertices `0` and `2` have in-degree 0 | `verified:lean` |
| `twoArcs_conventions_disagree` | the two dicut conventions differ on a disconnected digraph | `verified:lean` |
| `twoArcs_tau`, `twoArcs_woodall`, `path3_woodall`, `nearMiss_woodall` | τ = 1 instances of the conjecture | `verified:lean` |
| `WoodallConjecture` | **the conjecture** — a `Prop`, *stated, never proved, never assumed* | **open** |

Supporting bridge lemmas, also `verified:lean` and load-bearing for any reading of `tau?` as τ:
`tau?_eq_some_iff`, `tau?_eq_none_iff`, `tau?_eq_none_iff_not_exists`,
`not_isMinDicutSize_of_no_dicut`, `mem_dicutShores`, `mem_dicutSizes`.

### Dependencies

Both modules **import nothing outside Lean core** — no `Mathlib` — so no promoted statement here
rests on any other claim in this repo, at any status. Under `../../RULES.md` §3 the weakest
dependency caps the claim; there are no repo-internal dependencies to cap it, and the Lean
kernel supplies the rest. The definitions were checked against
`problems/woodalls-conjecture/README.md` §Definitions and its 2026-09-02 *dicuts are nonempty*
amendment, and against problem `RULES.md` §4; `WoodallConjecture` matches the README's statement
("the arc set `A` can be partitioned into `τ` disjoint dijoins") including the partition rather
than the weaker packing.

## Faithfulness defects found

The per-row `#check` was not a formality. Three rows in the previous revision described their
declaration as saying more than it says. All three are cases where **the Lean statement is
weaker than the prose** — the failure mode `../../RULES.md` §4 exists to catch. The prose above
has been corrected; the Lean is untouched by this PR.

**D1 — `cycle3_no_min_dicut_size` is bounded, its prose was not.** The actual statement is

```lean
theorem cycle3_no_min_dicut_size : ∀ (t : Nat), t ≤ 3 → ¬IsMinDicutSize cycle3 t
```

but the previous table row read "hence no τ" and the Lean docstring reads "no natural number is
the minimum dicut size". The declaration only rules out `t ≤ 3`. The unbounded statement *is*
available — `cycle3_tau : tau? cycle3 = none` together with `tau?_eq_none_iff_not_exists` gives
`¬∃ t, IsMinDicutSize cycle3 t` for every `t : Nat` — but it is a different declaration, so the
row now says what `cycle3_no_min_dicut_size` proves and points at `cycle3_tau` for the rest.

**D2 — `cycle3_empty_isDijoin` covers one arc set, its prose claimed all of them.** The actual
statement is

```lean
theorem cycle3_empty_isDijoin : IsDijoin cycle3 fun x => false
```

The previous row read "every arc set is vacuously a dijoin there" and the Lean docstring reads
"Every arc set — including the empty one — is vacuously a dijoin". Only the empty one is stated.
The general fact is true and immediate from `cycle3_no_dicut` (with no dicut shore, `IsDijoin`
is a vacuous `∀`), and my independent reimplementation confirms it for all 8 arc sets of
`cycle3` — but it is **not** what the named theorem proves, so the row has been narrowed.

**D3 — `diamond_two_le_tau` is a tautology as stated.** The statement is

```lean
theorem diamond_two_le_tau : [diamondJ₁, diamondJ₂].length ≤ 2
```

which reduces to `2 ≤ 2` and is provable by `rfl` without mentioning `diamond` at all. Its
*proof term* does exercise `length_le_tau` against `diamond_tau` and the two dijoin proofs, which
is the point of the fixture, but a reader citing the **statement** gets nothing about the
digraph. Recorded as verified because it is verified; recorded as content-free because it is.

D1 and D2 are also defects in the **Lean docstrings**, which overstate their theorems in the same
way. This PR does not edit `lean/` — the docstring corrections and, if wanted, the strengthened
statements belong in a follow-up on the formalisation issue, not in a `results/` promotion.

## What is *not* claimed

- **Nothing here is progress on Woodall's conjecture.** `WoodallConjecture` is open. The only
  theorems about it cover `τ ≤ 1`, which is degenerate: with `τ = 1` the single dijoin is all of
  `A`. `τ = 0` cannot occur under this convention, so `τ ≤ 1` *is* `τ = 1`.
- **The fixtures are not evidence.** A conjecture quantified over all digraphs is not supported
  by five instances (problem `RULES.md` §0). They test the *definitions*.
- **`length_le_card_deltaOut` / `length_le_tau` are the easy direction** and were already one
  line of the README.
- The three problem-`RULES.md` §1 filters do not apply: this file proves no special case and
  advances no argument for the existence direction, so there is nothing for the Schrijver,
  Lucchesi–Younger or easy-direction filters to bite on. The easy-direction filter is the
  relevant one and is satisfied *in the negative* — the two inequality theorems are explicitly
  labelled as the easy direction and as not progress.

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
   since everything decided over `∀ U : VertexSet n` rests on it. The kernel, not the compiler,
   evaluates these: no `native_decide` appears anywhere.
6. **Non-vacuity.** `IsMinDicutSize` carries the existence of a dicut, so `path3_tau`,
   `diamond_tau`, `nearMiss_tau` and `twoArcs_tau` cannot be vacuously true; `cycle3_trap` and
   `twoArcs_conventions_disagree` each assert a positive conjunct as well as a negative one.
7. **The three D-defects above** are the concrete yield of one pass of this audit. A second pass
   should assume there are more, and re-read the signatures rather than the docstrings.
