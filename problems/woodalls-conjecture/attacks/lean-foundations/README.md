# Lean foundations for Woodall's conjecture

**Status: scaffolding. Claims nothing.** The only mathematical content is the *easy* direction
`ν ≤ τ` and the degenerate range `τ ≤ 1`. Neither is progress on the conjecture, and this
directory must not be cited as if it were.

Lean source: [`lean/Verified/Woodall/Basic.lean`](../../../../lean/Verified/Woodall/Basic.lean).

This file exists so that the definitions are legible without a Lean toolchain, and so that a
reviewer can check the *prose meaning* against the *formal statement* independently — per
`RULES.md` §7, "a formal statement that does not say what you think it says" is the failure mode
this whole exercise is exposed to.

## The definitions, in words

A **finite digraph** `D` is a finite arc set `arcs ⊆ V × V` over a finite vertex type `V`. The
pair `(u, v)` is the arc **from `u` to `v`**.

| Notion | Meaning | Lean |
|---|---|---|
| `δ⁺(S)` | arcs **leaving** `S`: tail in `S`, head outside | `FinDigraph.out` |
| `δ⁻(S)` | arcs **entering** `S`: tail outside, head in `S` | `FinDigraph.inn` |
| dicut side | `S` nonempty, proper, and `δ⁻(S) = ∅` | `FinDigraph.IsDicutSide` |
| dicut | `δ⁺(S)` for some dicut side `S` | `FinDigraph.IsDicut` |
| dijoin | arc set `J ⊆ arcs` meeting **every** dicut | `FinDigraph.IsDijoin` |
| packing of size `k` | `k` **pairwise arc-disjoint** dijoins | `FinDigraph.HasPacking` |
| `τ(D)` | size of a minimum dicut | `FinDigraph.IsMinDicut` |
| `ν(D)` | largest `k` with a packing of size `k` | (relational; see below) |

**Woodall's conjecture**, as stated formally: *for every minimum dicut `C`, there is a packing of
size `C.card`* — that is, `ν(D) ≥ τ(D)`. Since `ν(D) ≤ τ(D)` is proved in the same file, the
formal statement is equivalent to `ν(D) = τ(D)`, which is the conjecture.

### Two convention choices, stated openly

1. **`τ` and `ν` are not defined as standalone numbers.** `IsMinDicut C` carries exactly the
   information "`C.card = τ`", and `HasPacking k` carries "`k ≤ ν`". Defining `τ` as an `sInf`
   would force a convention for the digraph with no dicut at all (a strongly connected digraph
   has none), and defining `ν` as an `sSup` would drag in a boundedness side condition. The
   relational form has neither problem and states the same mathematics. The cost is that the
   formal statement quantifies over minimum dicuts rather than mentioning `τ` by name.

2. **The empty set is allowed to be a dicut.** If some nonempty proper `S` has no arcs entering
   *and* no arcs leaving, then `δ⁺(S) = ∅` is a dicut under this definition. Some authors
   exclude this by requiring dicuts to be nonempty. Allowing it is the honest choice here,
   because such a digraph really does have **no dijoin at all** (nothing can meet the empty
   dicut), so `ν = τ = 0` and the conjecture holds in that case as a genuine, if trivial,
   instance rather than by definitional exclusion. This is proved:
   `not_isDijoin_of_isDicut_empty`.

## What is proved, completely

- `IsDijoin.exists_mem_of_isDicut` — a dijoin contains an arc of every dicut.
- `card_le_of_hasPacking` — **`ν(D) ≤ τ(D)`.** Given `k` pairwise arc-disjoint dijoins and any
  dicut `C`, choose from each dijoin an arc of `C`. Arc-disjointness makes that choice injective,
  so `C` contains `k` distinct arcs and `k ≤ |C|`.
- `woodall_of_card_le_one` — **the conjecture for `τ ≤ 1`.** Two cases. If `τ = 0` the minimum
  dicut is empty, no dijoin exists, and `ν = 0 = τ`. If `τ = 1` then minimality makes every dicut
  nonempty, so the entire arc set is a dijoin and `ν = 1 = τ` by the bound above.

The conjecture itself is **not** attempted (`RULES.md` §7).

## Mandatory filters (`problems/woodalls-conjecture/RULES.md` §1)

All three were run; this file is not an attack on the conjecture, so they are recorded as
applying to the *content that exists*.

1. **Schrijver filter (weighted Edmonds–Giles is false).** Not triggered as a refutation, but it
   is worth recording *why*: the argument for `ν ≤ τ` is a counting argument over an arc set and
   would survive weighting, which is exactly the warning sign — and correctly so, because the
   `≤` direction *is* true in the weighted setting too. It is the `≥` direction that fails when
   weighted, and nothing here touches it. Any future Lean work in this namespace that proves a
   `≥` bound without using unweightedness is wrong by this filter.
2. **Lucchesi–Younger filter.** Not used, in either direction. Lucchesi–Younger is not imported,
   stated, or assumed anywhere in the Lean file; the only inputs are the definitions.
3. **Easy-direction filter.** Explicitly triggered and explicitly declared:
   `card_le_of_hasPacking` **is** the trivial `≤ τ` bound and is labelled as such in its
   docstring so it can never be mistaken for the existence direction.

## Definition sanity checks (`problems/woodalls-conjecture/RULES.md` §4)

Checked by hand first, then formalised as `theorem`s so CI rechecks them.

| Digraph | By hand | Lean |
|---|---|---|
| single arc `0 → 1` on `Fin 2` | only dicut side is `{0}`; only dicut is `{(0,1)}`; `τ = 1` | `oneArc_isDicut`, `oneArc_isMinDicut` |
| same, the sink `{1}` | `δ⁺({1}) = ∅` but `δ⁻({1}) = {(0,1)} ≠ ∅`, so **not** a dicut side | `not_isDicutSide_sink` |
| directed `2`-cycle | **no** dicuts at all | `twoCycle_no_dicut` |
| single arc, end to end | `ν = τ = 1`, conjecture holds | `oneArc_hasPacking` |

`not_isDicutSide_sink` is the important one. §4 says the single error that invalidates most first
attempts is requiring `δ⁺(S) ≠ ∅` instead of `δ⁻(S) = ∅`. Under that wrong definition the sink
`{1}` of the one-arc digraph would be a dicut side and `∅` would be a dicut, giving `τ = 0`
instead of the correct `τ = 1`. The theorem pins down that this file does not make that error.

A directed path `0 → 1 → 2` was also checked by hand (dicut sides `{0}` and `{0,1}`, dicuts
`{(0,1)}` and `{(1,2)}`, `τ = 1`, and the unique dijoin is the whole arc set, so `ν = 1`) but was
not formalised, for budget reasons.

## Environment note — no local Lean build was possible

The worker image had no Lean toolchain, and the egress proxy returns `403` policy denials for
`elan.lean-lang.org`, `release.lean-lang.org`, and `lakecache.blob.core.windows.net`. Installing
`elan` and running `lake exe cache get` were therefore both impossible, and no `lake build` was
run locally. The repository's own Lean CI is the first machine check of this file. See the PR for
the build outcome.

## Mathlib gap assessment

Small, for this fragment. Nothing beyond `Finset`, `Fintype`, `Finset.card`, and
`Finset.card_le_card_of_injOn` is used, and the digraph notions are defined from scratch in about
twenty lines. Mathlib's own `Digraph` (an `Adj : V → V → Prop` relation) was **not** used: the
conjecture counts *arcs* and needs cardinality of arc sets, so a `Finset (V × V)` representation
is the natural one and a relation-based one would have to be converted immediately.

The gap becomes real further up. Nothing in Mathlib supplies directed cuts, dijoins, strong
connectivity after contraction, or the Lucchesi–Younger theorem, so the genuinely non-trivial
target — the `τ = 2` case — would require building that theory first. That is a substantial
project, not an afternoon's work, and anyone scoping it should budget accordingly.
