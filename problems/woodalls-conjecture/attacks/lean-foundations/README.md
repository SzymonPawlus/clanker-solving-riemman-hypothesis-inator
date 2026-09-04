# Lean foundations for Woodall's conjecture

**Status: scaffolding. Claims nothing.** The only mathematical content is the *easy* direction
`ν ≤ τ` and the degenerate range `τ ≤ 1`. Neither is progress on the conjecture, and this
directory must not be cited as if it were.

**Nothing here is `verified:lean` at the time of writing** — see
[`../../results/woodall-lean-basics.md`](../../results/woodall-lean-basics.md) for exactly what
was and was not checked, and by what.

Lean sources:

- [`lean/Verified/Woodall/Basic.lean`](../../../../lean/Verified/Woodall/Basic.lean) — definitions,
  the easy direction, the conjecture statement, the `τ ≤ 1` case.
- [`lean/Verified/Woodall/Instances.lean`](../../../../lean/Verified/Woodall/Instances.lean) —
  small digraphs, every theorem closed by `decide`.

## This supersedes the earlier attempt

An earlier, unmerged and abandoned branch `origin/claude/76-lean-woodall` carried a version of
this directory and of `lean/Verified/Woodall/Basic.lean`. **That development is superseded by
this one, and its `README.md` is replaced by this file.** It was not merged, and it is very
stale (it is based on an old `main`).

The reason it is replaced rather than extended is a faithfulness gap found by the audit on
issue #151:

> its `FinDigraph.arcs` is a `Finset (V × V)`, which **collapses parallel arcs**.

Woodall's conjecture is standardly stated for digraphs in which parallel arcs are allowed and
distinct, and `problems/woodalls-conjecture/README.md` partitions the arc set `A`, not a set of
distinct endpoint pairs. `problems/woodalls-conjecture/attacks/dijoin-exact-ip-search/README.md`
already models `A` as a *sequence* of ordered pairs for exactly this reason. A `Finset (V × V)`
formalisation therefore states **Woodall for simple digraphs**, which is a strictly weaker
statement than Woodall.

This development fixes that: arcs are an **indexed family** `Fin m → Fin n` (built from a
`List` of endpoint pairs by `Digraph.ofArcList`), so an arc *is* its index and listing the same
pair twice gives two genuinely distinct parallel arcs.

What was carried forward from the superseded branch, re-proved on the new representation:
the easy direction, the statement of the conjecture, the `τ ≤ 1` case, and the §4 trap exhibit.

## The definitions, in words

A **digraph** is `tail, head : Fin m → Fin n` — `n` vertices, `m` arcs, arc `a` running from
`tail a` to `head a`. Vertex and arc subsets are `Fin n → Bool` and `Fin m → Bool`.

| Notion | Meaning | Lean |
|---|---|---|
| `δ⁺(U)` | arcs **leaving** `U`: tail in `U`, head outside | `deltaOut` |
| `δ⁻(U)` | arcs **entering** `U`: tail outside, head in `U` | `deltaIn` |
| dicut shore | `δ⁻(U) = ∅` **and** `δ⁺(U) ≠ ∅` | `IsDicutShore` |
| dicut | the arc set `δ⁺(U)` for a dicut shore `U` | `deltaOut D U` |
| dijoin | arc set meeting **every** dicut | `IsDijoin` |
| arc-disjoint | share no arc | `ArcDisjoint` |
| `τ(D)` | minimum size of a dicut | `IsMinDicutSize` (relational), `tau?` (computable) |
| partition of `A` | every arc in **exactly one** member | `IsArcPartition` |
| the conjecture | `A` partitions into `τ` dijoins | `WoodallConjecture` |

`IsDicutShore` also records that `U` is nonempty and proper. Those are implied by `δ⁺(U) ≠ ∅`
(`nonempty_and_proper_of_isDicutShore`), so stating them costs nothing and closes off a reading
in which they were quietly dropped.

### Three convention choices, stated openly

1. **Parallel arcs are distinct** (above). This is the substantive fix over the superseded
   branch.

2. **A dicut must be nonempty**, i.e. `IsDicutShore` requires `δ⁺(U) ≠ ∅`. The superseded branch
   made the opposite choice and documented it as deliberate. The two conventions **genuinely
   disagree**, and the disagreement is exhibited rather than hidden: `twoArcs` (the disconnected
   digraph `0 → 1`, `2 → 3`) has `{0, 1}` as a dicut shore under the permissive reading and not
   under this one (`twoArcs_conventions_disagree`), giving `τ = 0` there and `τ = 1` here.
   Under the permissive reading such a digraph has *no dijoin at all*. The permissive reading is
   defensible; this file takes the other one because the issue brief specifies it and because it
   keeps `τ` equal to the minimum size of an actual cut. `IsDicutShoreAllowingEmpty` is defined
   so the alternative is nameable, and `isDicutShoreAllowingEmpty_of_isDicutShore` records that
   this file's notion is the stronger one.

3. **`τ` is primarily relational.** `IsMinDicutSize D t` says "`t` is attained and is a lower
   bound"; it is proved single-valued (`isMinDicutSize_unique`). A digraph with no dicut has no
   such `t` at all, which is the correct reading — every arc set is then vacuously a dijoin and
   there is no bound on disjoint dijoins. The computable `tau? : Option Nat` returns `none`
   exactly there.

## What is proved, and what is not

**Proved (modulo the toolchain caveat in the results note):**

- `length_le_card_deltaOut` / `length_le_tau` — **the easy direction**: pairwise arc-disjoint
  dijoins number at most `τ`. `problems/woodalls-conjecture/README.md`: "any 'proof' that only
  establishes the easy inequality has proved nothing." This is that inequality. It is not
  progress.
- `woodall_of_isMinDicutSize_le_one` — the conjecture for `τ ≤ 1`, where the single dijoin is
  all of `A`. Degenerate. Not the `τ = 2` folklore theorem, which is **not** formalised here.
- Small-instance checks by `decide`: the directed cycle has no dicut; the directed path's dicuts
  are exactly its two prefix cuts; the diamond has `τ = 2` with two disjoint dijoins that
  partition `A`; the near-miss DAG has `τ = 1`.

**Not proved, not assumed, and not present in any weakened form:**

- **Woodall's conjecture.** `WoodallConjecture` is a `Prop`. Nothing derives it, and no lemma
  takes it as a hypothesis.
- The `τ = 2` case (known true, folklore).
- The source–sink-connected case, Lucchesi–Younger, or the `⌊τ/6⌋` bound.

## Mandatory filters (problem `RULES.md` §1)

All three were run on this work.

1. **Schrijver filter** — not applicable in the sense that kills approaches: no proof of the
   existence direction is attempted here, so there is no argument to check for unweightedness.
   The easy direction *does* hold in the weighted setting too, which is consistent — it is the
   direction Edmonds–Giles never contradicted. Schrijver's refutation constrains the *existence*
   direction, which is untouched.
2. **Lucchesi–Younger filter** — not used, not imported, not stated. Nothing in either file
   mentions dicut packing or dijoin minimisation, so the roles cannot have been swapped.
3. **Easy-direction filter** — this development *is* mostly the easy direction, and says so in
   the module docstring, in the theorem docstring, in this file and in the results note. It is
   labelled, not disguised as progress.
