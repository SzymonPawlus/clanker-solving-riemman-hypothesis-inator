# Drift hypotheses — written BEFORE reading any Lean from issue #150

Issue #151, step 2. This file is committed before B1's branch was fetched, so that the audit
tests a pre-registered list rather than rationalising whatever it finds. Each item names a
way a Lean formalisation of `problems/woodalls-conjecture/README.md` could type-check, build
green, and still say something other than the prose. For each: what the prose says, the
plausible Lean drift, and the concrete small digraph on which the two would disagree.

Prose (README.md "Definitions", restated in my words): `D=(V,A)`; for **nonempty proper**
`U ⊊ V`, `δ⁺(U)` = arcs leaving `U`, `δ⁻(U)` = arcs entering; a **dicut** is `δ⁺(U)` with
`δ⁻(U)=∅`; a **dijoin** meets every dicut; `τ` = min dicut size; Woodall = `A` splits into
`τ` disjoint dijoins; easy direction = never more than `τ` pairwise disjoint dijoins.

| # | Drift | Witness digraph | Prose says | Drifted Lean says |
|---|---|---|---|---|
| H1 | `IsDicut` checks `δ⁺(U) ≠ ∅` but not `δ⁻(U) = ∅` (RULES §4's named trap) | path `0→1→2` plus `2→1`? Simpler: `0→1, 1→0` (2-cycle) | no dicut, `τ` undefined | `U={0}` gives "dicut" `{0→1}`, `τ=1` |
| H2 | `IsDicut` forgets nonemptiness of the **cut** (`δ⁺(U)` may be empty) | two isolated arcs `0→1, 2→3` | `τ=1` (survey reading) / `τ=0` (literal README) — prose itself ambiguous | `∅` is a dicut, `τ=0`, no dijoin exists |
| H3 | `U` ranges over **all** subsets incl. `∅` and `V` | any digraph, e.g. single arc `0→1` | `τ=1` | `U=∅` gives `δ⁺=∅, δ⁻=∅` so `∅` is a dicut, `τ=0` |
| H4 | `U` required nonempty but not proper (or vice versa) | single arc | same as H3 | same as H3 via `U=V` |
| H5 | Arcs are a `Finset (V×V)` / `SimpleGraph`-like relation, so **parallel arcs collapse** | `0→1, 0→1` | `τ=2`, 2 disjoint dijoins | `τ=1` |
| H6 | Loops mishandled (e.g. loop counted in `δ⁺` or `δ⁻`) | `0→0, 0→1` | `τ=1`, loop irrelevant | may differ |
| H7 | `τ` minimised over all cuts `δ⁺(U)` (not just dicuts), or over all `U` incl. those with `δ⁺=∅` | 2-cycle `0→1, 1→0` | `τ` undefined | `τ=1` |
| H8 | `τ` defaults to `0` when no dicut exists (`Finset.min` / `sInf ∅ = 0`) | directed cycle | `τ` undefined; easy direction vacuous | `τ=0`; easy direction then **false** as a Prop (`{∅,{a}}` are 2 disjoint dijoins) — so it will not be provable unless a hypothesis `∃ dicut` is added or the statement is otherwise narrowed. Check what was added. |
| H9 | "disjoint dijoins" = pairwise **distinct** (`Finset (Finset Arc)` with no `Disjoint`) | diamond | max = 2 | any number of distinct dijoins, easy direction false → look for narrowing |
| H10 | Family indexed `Fin k → Finset Arc` with `∀ i j, Disjoint (f i) (f j)` **without `i ≠ j`** — forces every member empty, hypothesis unsatisfiable when a dicut exists: easy direction **vacuous** | any digraph with a dicut | bound is real | proved for free |
| H11 | Family as a `Finset` of dijoins with pairwise disjointness but statement bounds `card` of the *union* or something else | diamond | `≤ τ` on number of members | different quantity |
| H12 | Easy direction stated as `card family ≤ τ` where `τ` is min over dicuts **of the chosen dicut only**, i.e. `∀ C dicut, card family ≤ card C` — this is actually *stronger* and still true; fine. Reverse: `∃ C dicut, card family ≤ card C` — weaker, true, but says less than `≤ τ`. Check quantifier direction. | diamond vs a digraph with dicuts of sizes 1 and 3 | `≤ τ = 1` | `≤ 3` |
| H13 | `IsDijoin S` requires `S ⊆ A`? If arcs are indices `Fin m`, automatic. If arcs are pairs, `S` could contain non-arcs and "meet" a dicut spuriously. | any | dijoin ⊆ A | phantom arcs |
| H14 | `IsDijoin` meets every dicut *shore* `U` rather than every dicut *set* — same thing, since dicut is defined via `U`; but if it quantifies over `U` **without** the `δ⁻(U)=∅` filter, every arc set crossing every cut = a strengthening-like object, stronger than dijoin | path `0→1→2` with extra `2→0`? no dicuts. Use `0→1, 1→0, 1→2`: prose dicut only `{1→2}`; drifted requires meeting `{0→1}` too | `{1→2}` is a dijoin | not |
| H15 | Digraph fixed on `Fin n` with `n ≥ 1`? `n = 0` edge case: no nonempty proper `U`, no dicuts — consistent, but `Fin 0` may make `decide` instances vacuous. | `n=0` | no dicut | check |
| H16 | `decide`-checked fixtures might be checked with a *different* definition (e.g. a `Bool`-valued `dicutb`) than the one the theorem uses, with no `Decidable`-instance bridge lemma — then the fixture checks say nothing about the theorem's definitions | — | — | look for two parallel definitions |
| H17 | Easy direction proved for **one particular** min dicut passed as hypothesis, e.g. `(C : Finset Arc) (hC : IsDicut C) (hmin : C.card = τ)` — fine — versus `(hC : IsDicut C)` alone giving `card family ≤ card C`: that is the *stronger* and correct lemma. Either is OK; note which. | — | — | — |
| H18 | Namespace/`Verified.lean` reachability: module under `lean/Verified/Woodall/` but not imported | — | CI checks it | CI never sees it |
| H19 | "Woodall's conjecture" stated as a `def`/`theorem` in some locally restated form that is weaker (e.g. only for DAGs, only `τ ≤ 2`, only for digraphs with a dicut) and then *named* as the conjecture | — | full conjecture | weaker |
| H20 | Dicut defined by the *complement* convention (arcs entering a shore that nothing leaves) — equivalent per README, but if the Lean mixes conventions between `IsDicut` and `tau` or between `δ⁺` and `δ⁻` in the easy-direction proof, the objects still coincide as sets (complement shore). Check each use separately; equivalence relies on `U ↦ V∖U` being a bijection on nonempty proper subsets. | — | — | — |

## Prose ambiguities discovered while writing the model (findings against the README, not B1)

* **P1.** README does not say whether the empty arc set counts as a dicut when the underlying
  graph is disconnected (`δ⁺(U)=δ⁻(U)=∅`). Under the literal reading `τ=0` and *no* dijoin
  exists for any disconnected digraph, which makes "partition into `τ` dijoins" degenerate.
  The survey/literature convention is that dicuts are nonempty. Issue #150 asks for
  "nonemptiness" without saying of what (`U`, `V∖U`, or `δ⁺(U)`).
* **P2.** README does not define `τ` when there is no dicut (strongly connected digraphs,
  single vertex). The easy direction's prose proof ("each consumes an arc of the minimum
  dicut") assumes a minimum dicut exists.
* **P3.** The README's "partition `A` into `τ` disjoint dijoins" and "max number of pairwise
  disjoint dijoins" are equated via "a superset of a dijoin is a dijoin", which is only stated
  in the source–sink section. Fine mathematically; a Lean statement may pick either form.

## How the sweep will use this

`experiments/woodall-lean-crosscheck/` runs the prose model and a second, deliberately
literal model of B1's Lean over all 13,615 labelled digraphs with `n ≤ 4`, `≤ 6` arcs,
multiplicity `≤ 2` (plus a loop batch), and reports every digraph where `dicuts`, `τ`,
the dijoin predicate, or the easy-direction bound differ.
