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
