# Closing the Lean foundations audit: the `τ` bridge and the dicut convention

Issue #158. Acts on findings F1, F2, F3 of the independent audit on issue #151
(branch `claude/151-lean-audit`, `attacks/lean-foundations-audit/`) against the Woodall Lean
merged by PR #154.

**Status.** The bridge lemma of F2 is machine-checked but is **not** `verified:lean` yet: the
repo's gate is a green `lake build` in CI, and CI runs on pull requests, not on a pushed branch.
Everything else here is `sketch`-tier prose or an audit record. Nothing in this file is progress
on Woodall's conjecture.

## F2 — the bridge between the two definitions of `τ` (the blocking item)

`lean/Verified/Woodall/Basic.lean` carried two definitions of `τ`:

- `IsMinDicutSize D t` — relational: some dicut shore has `card (deltaOut D U) = t`, and every
  dicut shore has `t ≤ card (deltaOut D U)`;
- `tau? D : Option Nat` — computed: `min?` of the sizes of the dicuts found by filtering the
  enumeration `allVertexSets`.

No theorem connected them. The #151 sweep found them equal on all 13,615 digraphs it covered,
which is `numerical` evidence and, per `../../RULES.md` §3, not a proof step. So every
`decide`-checked fact about `tau?` was a fact about `min?` of a filtered list and said nothing
about the minimum dicut size.

**The bridge is true and is now proved.** The kill-criterion for this issue — that the two
definitions genuinely disagree somewhere — was **not** met.

The right statement is an `↔` at `some t` rather than an equation between naturals, because
`tau?` is `Option`-valued and `IsMinDicutSize` is a relation that no `t` satisfies when the
digraph has no dicut. Both halves of the domain are covered:

```lean
theorem tau?_eq_some_iff {D : Digraph n m} {t : Nat} :
    tau? D = some t ↔ IsMinDicutSize D t

theorem tau?_eq_none_iff {D : Digraph n m} :
    tau? D = none ↔ ∀ U : VertexSet n, ¬ IsDicutShore D U

theorem tau?_eq_none_iff_not_exists {D : Digraph n m} :
    tau? D = none ↔ ¬ ∃ t : Nat, IsMinDicutSize D t
```

with two supporting lemmas that are where the real content sits:

```lean
theorem mem_dicutShores {D : Digraph n m} {U : VertexSet n} :
    U ∈ dicutShores D ↔ IsDicutShore D U

theorem mem_dicutSizes {D : Digraph n m} {t : Nat} :
    t ∈ dicutSizes D ↔ ∃ U : VertexSet n, IsDicutShore D U ∧ card (deltaOut D U) = t
```

`mem_dicutShores` is the step that could have failed: it says the filtered enumeration lists
*exactly* the dicut shores, missing none. It holds because `mem_allVertexSets` — already proved
in `Basic.lean` — says the enumeration of `Fin n → Bool` is complete. That is why the bound in
`tau?_eq_some_iff` is a genuine quantification over every vertex subset and not over whatever
the enumeration happened to contain. The rest is Lean core's `List.min?_eq_some_iff`, which
gives membership and minimality, matched one-for-one against the two conjuncts of
`IsMinDicutSize`.

Where a side condition might have been needed, and was not: the no-dicut case. `min?` on the
empty list is `none`, and `IsMinDicutSize` requires an attaining shore, so both definitions
degenerate the same way and `tau?_eq_none_iff` states it. There is no hypothesis of
connectivity, acyclicity or nonemptiness anywhere in the bridge.

**Cross-check against the merged fixtures.** Not part of the committed Lean (the fixture file
belongs to another issue), but run locally: the bridge re-derives `IsMinDicutSize diamond 2`
from `diamond_tau?`, `IsMinDicutSize path3 1` from `path3_tau?`, and `IsMinDicutSize nearMiss 1`
from `nearMiss_tau?`, and derives `tau? cycle3 = none` from `cycle3_no_dicut`. All five compile.

## F1 — the dicut convention in `README.md`

`IsDicutShore` requires `δ⁺(U) ≠ ∅`; the problem `README.md` did not. The two readings differ on
exactly the digraphs whose underlying graph is disconnected (1,892 of the audit's 13,615), never
on a weakly connected one. `README.md` has been amended to require nonemptiness, with the
argument, the scope of the change, and its consequences recorded there under *Convention: dicuts
are nonempty*.

Three checks the amendment had to survive:

1. **The `cited` source–sink-connected theorem is unaffected.** Its hypothesis implies weak
   connectivity — a finite nonempty DAG has a source and a sink, so two weak components would
   put a source and a sink in different components with no directed path between them — and on
   weakly connected digraphs the two readings agree. `τ(D,c)` and the theorem's conclusion are
   unchanged, so no `cited` statement was altered.
2. **Every use of "dicut" under `problems/woodalls-conjecture/**` was checked.**
   `tau-saturation`, `balanced-dicut-hypergraph` and `tau3-saturated-source-sink` already state
   the nonempty convention. `zero-weight-frontier` is weighted and its `τ_w = 0` case is about
   zero weights, not empty cuts; its item 3 states the disjoint-union reduction that the
   amendment relies on. The `rho4-*` attacks state the permissive form in their definition
   preamble but work inside a structured model whose cuts are nonempty, so nothing there
   depends on it. `results/woodall-lean-basics.md`, the only file in `results/`, already
   describes the nonempty convention.
3. **Two merged files do depend on the permissive reading.** Reported, not repaired — both are
   outside this issue's ownership.

### Finding: `attacks/tau2-robbins/` Lemma A

The red team on issue #153 (PR #160) reports that Lemma A mixes the two conventions and that
under the nonempty convention its conclusion "$G$ is connected" is **false**, with 636 weakly
disconnected `τ ≥ 2` digraphs as witnesses. Recorded here because the amendment is what makes
that reading binding; the finding and its repair belong to #153/#160. Not independently
re-derived here, and deliberately not asserted either way about the rest of that file's `τ = 2`
argument, which handles components separately.

### Finding: `attacks/dijoin-exact-ip-search/` coverage statement

Its own definition section admits empty dicuts, and it excludes `τ ≤ 1` from the `n = 7` run
with the argument "if `τ = 0` some dicut is empty and zero dijoins are required". Its code does
the same: `experiments/woodall-dijoin-exact-ip/dijoin_exact.py` returns early on an empty dicut,
and `sweep.py` records that padding with isolated vertices "forces an empty dicut and tau = 0".

Under the amended convention `τ = 0` never occurs, and a disconnected DAG can have `τ ≥ 2` —
two disjoint diamonds have `τ = 2` here and `τ = 0` under the permissive reading (checked
directly). Such digraphs are inside the stated space "all simple DAGs on `n = 7` with `τ ≥ 2`"
and were pruned from it. The gap is closable by the disjoint-union reduction rather than by more
computing, but the write-up's coverage claim needs that substitution made explicit. That file
belongs to issue #73; not repaired here.

## F3 — `cycle3_no_min_dicut_size`

Its docstring claims "no natural number is the minimum dicut size" while the theorem is bounded
to `t ≤ 3`, because `decide` needs a finite range. The general lemma the audit says would fix it
is now in `Basic.lean`:

```lean
theorem not_isMinDicutSize_of_no_dicut {D : Digraph n m}
    (h : ∀ U : VertexSet n, ¬ IsDicutShore D U) (t : Nat) : ¬ IsMinDicutSize D t
```

and `not_isMinDicutSize_of_no_dicut cycle3_no_dicut : ∀ t, ¬ IsMinDicutSize cycle3 t` compiles —
verified locally. **The one-line edit itself was not made**, because `Instances.lean` is outside
this issue's file ownership and is held by concurrent work. F3 is therefore *unblocked but not
closed*: the docstring on `main` is still stronger than its theorem, and whoever owns
`Instances.lean` next should replace that theorem with the unbounded form in one line.

## Mandatory filters (`../RULES.md` §1)

Vacuously satisfied and stated for the record: nothing here argues about packing dijoins at all.
No weighted or capacitated statement appears, so the Schrijver filter has nothing to bite on; no
cut/dijoin duality is used anywhere, so no Lucchesi–Younger role swap occurs; and the easy
direction is neither used nor extended — `length_le_tau` is untouched.

## Verification status

- `tau?_eq_some_iff`, `tau?_eq_none_iff`, `tau?_eq_none_iff_not_exists`,
  `not_isMinDicutSize_of_no_dicut`, `mem_dicutShores`, `mem_dicutSizes`: typecheck with zero
  errors and zero warnings under the pinned Lean 4.33.0 (commit `d8b1897`), fetched from its
  GitHub release because the toolchain and Mathlib cache hosts are 403-blocked here.
  `#print axioms` reports only `propext`, `Classical.choice`, `Quot.sound` — and
  `not_isMinDicutSize_of_no_dicut` depends on none at all. CI's own rejection grep was run
  locally and is clean.
- **Not `verified:lean`.** The repo's gate is a green `lake build` on a pull request. This
  branch was pushed without one, so no CI run exists for it. `lake build` was not run locally
  either — `lake exe cache get` cannot reach its host — though the modules import no Mathlib, so
  the direct `lean` invocation checks the same kernel content the build would.
- The prose in this file and the justification in the amended `README.md` are `sketch`. The
  1,892- and 13,615-digraph figures are the #151 audit's `numerical` results, cited not
  reproduced; the 636-digraph figure is #160's, likewise.
