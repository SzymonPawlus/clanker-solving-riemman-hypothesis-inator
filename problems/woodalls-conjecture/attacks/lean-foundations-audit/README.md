# Lean foundations — adversarial faithfulness audit

**Status: audit record** (`sketch`-tier prose plus `numerical` cross-checks; establishes no
mathematical claim). Issue #151, adversary side of pair B; companion to issue #150 (B1).
Code: [`experiments/woodall-lean-crosscheck/`](../../../../experiments/woodall-lean-crosscheck/).
Pre-registered hypotheses, committed before any Lean was read: [`hypotheses.md`](./hypotheses.md).

## The question

A green Lean build proves the *stated* theorem. This audit asks only whether the stated
definitions and theorems say what `problems/woodalls-conjecture/README.md` says — the trap
named in `problems/riemann-hypothesis/RULES.md` §4 ("a locally restated variant that looks
equivalent") and `lean/README.md` §6. Soundness (no `sorry`/`axiom`/`native_decide`) is CI's
job and is only confirmed here, not re-derived.

## Method

1. **Prose model.** `prose_model.py` implements dicut, dijoin, τ, max number of pairwise
   arc-disjoint dijoins, and "τ disjoint dijoins exist", from README.md alone. Arcs are a
   *list* (parallel arcs distinct, loops allowed); `U` ranges over nonempty proper subsets;
   a dicut is `δ⁺(U)` with `δ⁻(U) = ∅`. Two readings of one prose ambiguity are exposed
   (`allow_empty`): whether `∅` counts as a dicut when `δ⁺(U) = δ⁻(U) = ∅`.
   Fixtures (`test_prose_model.py`): path `0→1→2` τ=1; 3-cycle has no dicut; diamond τ=2
   with the two `s`–`t` paths as disjoint dijoins; near-miss DAG `s1→t1, s2→t1, s2→t2` τ=1;
   `0→1, 0→1` τ=2 with two disjoint dijoins.
2. **Pre-registered drift list** (`hypotheses.md`, H1–H20), written before any Lean was
   read, each with the small digraph that would expose it.
3. **Literal Lean model.** Every Lean definition transcribed one-for-one into Python,
   deliberately including anything that looks wrong, then swept against the prose model.
4. **Sweep space, stated exactly.** All labelled digraphs with `1 ≤ n ≤ 4` vertices, at most
   6 arcs, each ordered pair (no loops) with multiplicity 0–2: **13,615 digraphs**, not up
   to isomorphism (small enough that reduction is unnecessary). Includes arcless, disconnected,
   strongly connected (no dicut), and multigraph instances. Compared fields: the set of
   dicuts, τ, the maximum number of pairwise arc-disjoint dijoins, and whether τ disjoint
   dijoins exist. Runtime: under a minute per model, CPython 3.11, stdlib only, deterministic.

Reproduce:

```bash
cd experiments/woodall-lean-crosscheck
python3 -m unittest test_prose_model -v
python3 sweep76.py            # branch-76 Lean vs prose
python3 crosscheck.py         # B1 (issue #150) Lean vs prose, once lean_model.py exists
```

## Findings against the prose itself (README.md)

- **P1 — `∅` as a dicut is unspecified.** For a disconnected digraph, `U` = one component has
  `δ⁺(U) = δ⁻(U) = ∅`. Literal README: `∅` is a dicut, τ=0, and *no* dijoin exists.
  Survey/literature convention: dicuts are nonempty. In the sweep the two readings differ on
  exactly the 273 simple digraphs whose underlying graph is disconnected, and on no
  weakly-connected digraph. Any Lean development has to choose; the README should say which.
- **P2 — τ undefined without a dicut.** Strongly connected digraphs (and `n = 1`) have no
  dicut. The README's easy-direction argument ("each consumes an arc of the minimum dicut")
  silently assumes one exists. A Lean `τ : ℕ` must either add an existence hypothesis or avoid
  defining τ as a number.
- **P3 — "partition into τ dijoins" vs "τ pairwise disjoint dijoins exist"** are equated only
  via "a superset of a dijoin is a dijoin", stated later in the file. Fine, but a Lean
  statement may legitimately take either form; they are not syntactically the same Prop.

## Audit of the pre-existing Lean: branch `claude/76-lean-woodall` @ 561af29 (PR #79, closed)

This is the only Woodall Lean that existed on the remote when the audit began. It is not on
`main` (`lean/Verified.lean` on `main` does not import it). Literal model: `lean_model_76.py`.

Definitions translated back to prose in my words:

| Lean | My reading | vs README |
|---|---|---|
| `FinDigraph V := { arcs : Finset (V × V) }` | a **set** of ordered pairs on a finite type; loops allowed | **narrower**: parallel arcs collapse (H5) |
| `out D S` / `inn D S` | arcs with tail in `S`, head out / tail out, head in; loops never qualify | same |
| `IsDicutSide D S := S ≠ ∅ ∧ S ≠ univ ∧ inn S = ∅` | nonempty proper shore that no arc enters | same (H1, H3, H4 do **not** fire) |
| `IsDicut D C := ∃ S, IsDicutSide S ∧ C = out S` | `δ⁺(S)` of such a shore, **possibly empty** | literal README, not survey (P1 / H2; documented as deliberate) |
| `IsDijoin D J := J ⊆ arcs ∧ ∀ C, IsDicut C → (J ∩ C).Nonempty` | subset of arcs meeting every dicut | same (H13 does not fire) |
| `HasPacking D k := ∃ J : Fin k → _, (∀ i, IsDijoin (J i)) ∧ ∀ i j, i ≠ j → Disjoint (J i) (J j)` | `k` pairwise **arc-disjoint** dijoins | same (H9, H10 do not fire) |
| `IsMinDicut D C` | dicut of minimum card; τ never defined as a number | avoids P2 honestly |
| `WoodallConjecture D := ∀ C, IsMinDicut C → HasPacking C.card` | for every min dicut, that many disjoint dijoins | same up to P3; vacuous with no dicut, which is right |
| `card_le_of_hasPacking : HasPacking k → IsDicut C → k ≤ C.card` | easy direction against **every** dicut | stronger-and-correct form (H12 resolved the good way) |

Sweep, `python3 sweep76.py`, 13,615 digraphs:

| Comparison | Disagreements | Smallest witness |
|---|---|---|
| dicut sets, simple digraphs, literal reading | **0** | — |
| τ, simple digraphs, literal reading | **0** | — |
| max disjoint dijoins, simple digraphs, literal | **0** | — |
| τ, simple digraphs, survey reading | 273 | `n=2`, no arcs: prose τ undefined, Lean τ=0 (P1) |
| τ, multigraphs | 2,086 | `0→1, 0→1`: prose τ=2, Lean τ=1 (H5) |
| "τ disjoint dijoins exist", multigraphs, both τ defined (10,419 cases) | **0** | — |

So the branch-76 Lean is faithful to the literal README on simple digraphs, and its one real
gap is the one Codex's review of #79 named: `Finset (V × V)` silently restricts the
conjecture to simple digraphs while the module docstring calls that "harmless". In this sweep
the restriction changes τ on 15% of instances but never the truth value of the conjecture —
which is what one expects from subdividing parallel arcs — but the definitions are still not
the README's definitions, and issue #150 explicitly requires a multiset/list of arcs.

## Audit of B1's Lean: branch `claude/150-lean-foundations` @ `ad78d86` (issue #150)

Files read from that ref (not from B1's worktree; nothing under `lean/` was edited):
`lean/Verified/Woodall/Basic.lean` (430 lines), `lean/Verified/Woodall/Instances.lean`
(185 lines), `lean/Verified.lean`. Literal model: `lean_model.py`, verified to reproduce every
`decide`-checked fact in `Instances.lean` before the sweep was run.

### Mechanical checks (done myself, not taken from B1)

- `grep -nE 'sorry|axiom|native_decide|admit|unsafe|implemented_by|extern|opaque'` over both
  modules at `ad78d86`: **no hits** other than the English words "admits/admitted" inside doc
  comments (not the `admit` tactic). The CI pattern
  `\b(sorry|native_decide)\b|^[[:space:]]*axiom\b` also matches nothing.
- `lean/Verified.lean` at `ad78d86` imports **both** `Verified.Woodall.Basic` and
  `Verified.Woodall.Instances`, so CI reaches them.
- `Basic.lean` has **no imports at all** (Lean core only); `Instances.lean` imports only
  `Verified.Woodall.Basic`. Mathlib is on no dependency path.
- **Not checked, and not checkable here:** the actual CI build. B1's `results/` note states
  plainly that `lake build` never ran (Mathlib cache host 403-blocked), that the modules were
  typechecked with a directly-fetched Lean 4.33.0 binary, and that **nothing is
  `verified:lean`**. That is the honest statement. What remains open is whether the
  Mathlib-standard linters under `--wfail` produce a style warning. The `#print axioms` output
  is quoted in B1's notebook; I take it on trust that it was produced as described.

### Definitions translated back into prose, in my words, and diffed against README.md

| Lean | My reading | vs README |
|---|---|---|
| `Digraph n m := { tail head : Fin m → Fin n }` | `n` vertices, `m` arcs; an arc **is** its index; `ofArcList` indexes a list by position | same as prose (arcs as a list). Parallel arcs distinct; loops allowed. H5 does not fire. |
| `VertexSet n := Fin n → Bool` | **all** subsets, `∅` and `V` included | wider than "nonempty proper", but see `IsDicutShore` |
| `deltaOut D U a := U (tail a) && !U (head a)`; `deltaIn` mirrored | per-arc, by index; a loop is never in either | same; multiplicity respected (H6 does not fire) |
| `IsDicutShore D U := (∀ a, deltaIn D U a = false) ∧ (∃ a, deltaOut D U a = true)` | `δ⁻(U) = ∅` **and** `δ⁺(U) ≠ ∅` | H1 does not fire. `∅`/`V` are excluded because `δ⁺ ≠ ∅` forces a tail in `U` and a head outside (`nonempty_and_proper_of_isDicutShore`), so H3/H4 do not fire. **`δ⁺(U) ≠ ∅` is an addition to the README text** — see F1. |
| there is no `IsDicut C`; a dicut is `deltaOut D U` for a shore | the dicut as an arc set is never first-class | equivalent, since dijoin/τ only ever consume `deltaOut D U` over shores |
| `IsDijoin D J := ∀ U, IsDicutShore D U → Meets (deltaOut D U) J` | `J : Fin m → Bool` meets every dicut | same; `J ⊆ A` is automatic (H13 does not fire); no `δ⁻` filter dropped (H14 does not fire) |
| `ArcDisjoint J K := ∀ a, ¬(J a ∧ K a)` | share no arc index | same (H9 does not fire) |
| `card S := (allArcs m).countP S` | number of indices in `S` | counts parallel arcs separately; no deduplication anywhere downstream |
| `IsMinDicutSize D t := (∃ U shore, card (deltaOut D U) = t) ∧ (∀ U shore, t ≤ card (deltaOut D U))` | `t = τ`, **and a dicut exists** | same; P2 handled by making existence a hypothesis. `isMinDicutSize_unique` proved. |
| `tau? D := ((allVertexSets n).filter IsDicutShore).map card ∘ deltaOut).min?` | computed τ, `none` if no dicut | matches, empirically — see F2 |
| `length_le_card_deltaOut : (∀ J ∈ Js, IsDijoin D J) → Js.Pairwise ArcDisjoint → IsDicutShore D U → Js.length ≤ card (deltaOut D U)` | a list of pairwise arc-disjoint dijoins is no longer than **any** dicut | the stronger, correct form of the easy direction (H12). `List.Pairwise` relates distinct positions only, so H10 (self-disjointness making it vacuous) does not fire; `diamond_two_le_tau` instantiates it with a 2-element family, which is a non-vacuity witness. |
| `length_le_tau` | … hence `≤ τ` | same |
| `IsArcPartition Js := ∀ a, (Js.countP fun J => J a) = 1` | every arc in **exactly one** member | covering + pairwise disjoint; members that are dijoins are nonempty (a dicut exists), so no empty padding block is possible |
| `WoodallConjecture D := ∀ t, IsMinDicutSize D t → ∃ Js, Js.length = t ∧ (∀ J ∈ Js, IsDijoin D J) ∧ IsArcPartition Js` | `A` partitions into exactly `τ` dijoins | the README's partition wording (P3), not the packing form; `IsDijoin.mono` is proved so the two are interchangeable. Vacuous when no dicut exists — same as prose. Not a weakened restatement (H19 does not fire). |
| `IsDicutShoreAllowingEmpty` | branch-76 convention, named, never used in a theorem's hypothesis | good: the alternative is nameable, and `twoArcs_conventions_disagree` is a real witness (my model agrees) |

### Sweep: literal model of B1's Lean vs prose model — `python3 crosscheck.py`

Space: all 13,615 labelled digraphs with `n ≤ 4`, `≤ 6` arcs, multiplicity `≤ 2`, no loops
(1,892 of them have a disconnected underlying graph; 10,419 are multigraphs). Runtime 214 s.

| Comparison | Disagreements |
|---|---|
| dicut sets, prose **survey** reading vs Lean | **0** |
| τ, prose survey reading vs Lean `tau?` | **0** |
| Lean `tau?` vs Lean `IsMinDicutSize` witness (the unbridged pair, F2) | **0** |
| max number of pairwise arc-disjoint dijoins, prose survey vs Lean list families | **0** |
| "τ disjoint dijoins exist" (prose, survey) vs `WoodallConjecture` (Lean, brute-force partition) | **0** |
| easy direction, prose vs `length_le_tau` | **0** |
| dicut sets, prose **literal** reading vs Lean | **1,892** — exactly the disconnected digraphs, and no others |
| τ, prose literal reading vs Lean `tau?` | **1,892** — the same digraphs |

Smallest witness of the literal-vs-Lean gap: `n = 2`, no arcs — literal README: `∅` is a dicut,
τ = 0, no dijoin exists; Lean: no dicut, τ undefined, every arc set is a dijoin. Smallest
witness with arcs: `0→1, 2→3` (B1's own `twoArcs`) — literal τ = 0, Lean τ = 1.

### Findings

- **F1 (P1, convention — the only place the Lean says something other than the README text).**
  `IsDicutShore` requires `δ⁺(U) ≠ ∅`. README.md's definition ("a dicut is a set `δ⁺(U)`
  where `δ⁻(U) = ∅`") does not, so on every disconnected digraph the Lean's dicuts, τ, and
  dijoins differ from the literal README (1,892 of 13,615 in the sweep; never on a connected
  digraph). The Lean follows the literature convention (nonempty dicuts) and issue #150's
  "nonemptiness". B1 documents the choice, names the alternative, and exhibits a witness; this
  is the right way to diverge. But the divergence is real, and it is the README that should
  change: it should say dicuts are nonempty (equivalently, that the digraph is taken weakly
  connected). I cannot edit README.md under this issue's file ownership; recommend a
  follow-up.
- **F2 (H16-adjacent, minor).** `tau?` and `IsMinDicutSize` are two definitions of τ with **no
  Lean theorem connecting them** (`tau? D = some t ↔ IsMinDicutSize D t` is not stated).
  `Instances.lean` checks both separately on each fixture. The sweep finds them equal on all
  13,615 digraphs, so this is not a faithfulness gap in any *stated* theorem — but nothing
  downstream may treat `tau?` as τ until the bridge is proved, and the docstring "`τ(D)`
  computed" reads as if it were established.
- **F3 (cosmetic).** `cycle3_no_min_dicut_size` is stated for `t ≤ 3` only, to keep `decide`
  finite. The unbounded `∀ t, ¬IsMinDicutSize cycle3 t` follows from `cycle3_no_dicut` in one
  line and would be the honest statement; as written it is weaker than its docstring
  ("no natural number is the minimum dicut size").
- **F4 (observation).** `WoodallConjecture` is a predicate on one digraph; there is no single
  `Prop` "`∀ n m (D : Digraph n m), WoodallConjecture D`". That is fine (nothing assumes it),
  but "the conjecture" as a Lean object does not exist yet; anyone citing it should say so.
- **F5 (observation).** `diamond_two_le_tau` proves `2 ≤ 2`. Its value is only as a
  satisfiability witness for the hypotheses of `length_le_tau`; it should not be read as an
  instance-level check of the bound.

### Hypotheses that did not fire, with the reason

H1 (`δ⁻` dropped): present at `IsDicutShore` line 163. H3/H4 (`∅`, `V`): excluded by `δ⁺ ≠ ∅`.
H5 (parallel collapse): arcs are indices; `card`, `ArcDisjoint`, `deltaOut` all index-wise;
the 10,419 multigraphs agree with prose on every field. H6 (loops): loops fail both `deltaOut`
and `deltaIn`; loop batch below. H7/H8 (τ over all cuts / τ = 0 default): τ only over shores,
existence carried as hypothesis. H9/H10 (distinct vs disjoint / vacuous self-disjointness):
`ArcDisjoint` + `List.Pairwise`. H12: stated against every dicut. H13/H14: see table. H16:
one definition each, `Decidable` instances proved from `mem_allVertexSets`; only `tau?` is a
parallel definition (F2). H18: imported. H19: partition form, not weakened. H20: one
convention (`deltaOut` of a shore no arc enters) used throughout.

### Taken on trust / could not follow

- That Lean 4.33.0 accepted both files and that `#print axioms` was clean — B1's report; no
  Lean toolchain here either. Everything above is about what the *text* says.
- `mem_allVertexSets` (the completeness of the subset enumeration, on which every `decide` over
  `∀ U : VertexSet n` rests): I read the proof and it is the standard cons/split induction; I
  did not re-derive the `Fin` arithmetic in `consB` by hand. If it were wrong the `decide`
  theorems would fail to *typecheck* rather than prove something false, so this is a
  soundness-of-B1's-claim item, not a faithfulness item.
- `length_le_countP` / `countP_erase_of_mem`: read, argument is the obvious injection; not
  re-derived line by line.

### Loop batch

`n ≤ 3`, `≤ 4` arcs, multiplicity `≤ 2`, **loops allowed**: 678 digraphs
(`results/loop_batch.txt`). Same picture: 0 disagreements under the survey reading on every
field; 251 under the literal reading, which is exactly the number of disconnected digraphs in
that batch. Loops never enter `deltaOut`/`deltaIn` on either side (H6 does not fire).

## Summary for the issue

- **One genuine divergence between B1's Lean and README.md's text: F1**, the nonempty-dicut
  clause, affecting exactly the disconnected digraphs. It is the literature convention,
  documented and witnessed in the Lean; the README should be amended to match, not the Lean.
- Every other pre-registered drift (H1, H3–H10, H12–H14, H16, H18–H20) is absent, with the
  line of source that rules it out named above, and the 13,615 + 678-digraph cross-sweep
  finds no instance where the Lean and the survey-convention prose disagree on dicuts, τ,
  packing number, the partition form of the conjecture, or the easy direction.
- Minor: F2 (`tau?` unbridged), F3 (bounded `t ≤ 3`), F4 (no global conjecture Prop), F5
  (`2 ≤ 2`).
- Nothing is `verified:lean`; B1 says so. A green CI build is still required, and this audit
  does not substitute for it.
