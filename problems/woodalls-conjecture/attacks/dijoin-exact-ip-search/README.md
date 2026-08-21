# Exact polychromatic-colouring counterexample search

Status: **numerical** (the sweeps) plus one **sketch** (the reformulation lemma below).
Nothing here is assumable. Nothing here is a proof of Woodall's conjecture, and by
`../../RULES.md` §2 no exhaustive search ever could be.

Issue: #73. Supersedes the search design that left #7 and #31 blocked.

## Definitions used (per `../../RULES.md` §4)

Let `D = (V, A)` with `A` a *sequence* of ordered pairs, so parallel arcs stay distinct.
For nonempty proper `U ⊊ V`:

- `δ⁻(U)` = arcs `(x,y)` with `x ∉ U`, `y ∈ U`;
- `δ⁺(U)` = arcs `(x,y)` with `x ∈ U`, `y ∉ U`;
- **dicut** = `δ⁺(U)` for a nonempty proper `U` with **`δ⁻(U) = ∅`**. The emptiness of
  `δ⁻(U)` is the entire content; requiring only `δ⁺(U) ≠ ∅` is the standard fatal
  misreading and is explicitly regression-tested against.
- **dijoin** = an arc set meeting every dicut. `τ` = minimum dicut cardinality.

Woodall: `τ` pairwise arc-disjoint dijoins always exist.

Sanity fixtures, all in the test suite: a directed cycle has **no** dicut; a directed
path has `τ = 1`; the diamond `s→x, s→y, x→t, y→t` has `τ = 2`.

## Why the previous search design stalled

`experiments/woodalls-dicuts/woodall.py` is a correct reference implementation, but it
decides a packing by first enumerating **every** dijoin — that is, iterating all `2^|A|`
arc subsets — and then backtracking over that list. On a 7-vertex DAG with 21 arcs that is
2,097,152 subsets *per graph*, and #31 wanted 243,668 graphs. The blocker recorded on #7
("blocked on the dicut/dijoin implementation") was stale — #6/PR #20 delivered the
primitives. The live blocker was the **algorithm**, and re-running that design is the dead
end this attack avoids.

## The reformulation (status: `sketch` — my own, therefore not assumable, including by me)

A superset of a dijoin is a dijoin, so leftover arcs can always be dumped into an existing
part. Hence for `τ ≥ 1`:

> `τ` pairwise disjoint dijoins exist **iff** the arcs admit a colouring with `τ` colours
> in which **every dicut receives all `τ` colours**.

*(⇒)* Given disjoint dijoins `J₁..J_τ`, colour `a` by `i` if `a ∈ J_i`, else `0`. Each
dicut meets each `J_i`, so every colour occurs in it.
*(⇐)* Colour class `i` meets every dicut, hence is a dijoin; classes of a colouring are
disjoint. ∎

This is a **polychromatic colouring** of the dicut hypergraph: a CSP on `|A|` variables
over `τ` values, rather than a search over `2^|A|` subsets. Only inclusion-minimal dicuts
need constraining. Dicuts of size exactly `τ` become AllDifferent constraints and
propagate very hard.

The lemma is elementary but it is *mine*, so per `../../RULES.md` §3 the sweeps are not
allowed to rest on it alone. They do not: every emitted packing is re-verified arc-by-arc
against the **full** dicut family and for pairwise disjointness, and on all
small instances the whole pipeline is checked against the independent
`woodalls-dicuts` implementation. An answer of "holds" is therefore backed by an
explicit witness that a different code path accepts, not by the lemma.

The genuinely one-sided direction is a **negative** answer. There the search's completeness
is what carries the weight — see "What a negative answer rests on" below.

## Exactness

All arithmetic is Python integers used as bitmasks. **No LP relaxation, no floating point,
no rounding, no external solver.** The packing decision is complete backtracking with
propagation and a colour-permutation symmetry break (the constraint is invariant under
permuting colours, so only one fresh colour is ever opened). A `None` return is therefore a
finished exhaustive search, not a solver's opinion.

## The three mandatory filters (`../../RULES.md` §1)

1. **Schrijver filter.** This attack proves nothing, so it cannot accidentally prove the
   weighted version. It is worth recording that the multi-arc sweep *is* the
   integer-capacitated statement (parallel arcs = capacities), so it probes exactly the
   territory the filter warns about — see the open question below.
2. **Lucchesi–Younger filter.** Not used, in either direction. The code never computes a
   packing of *dicuts* and never computes a minimum dijoin; it computes minimum **dicut**
   size and packs **dijoins**. No role swap occurs.
3. **Easy-direction filter.** The easy bound `≤ τ` is not what is tested. The solver is
   asked for exactly `τ` disjoint dijoins and returns them or proves none exist; a
   regression test confirms it correctly reports `τ+1` as infeasible on the diamond.

## Coverage

**Simple DAGs, all `τ`, complete:** `n ≤ 6`.
**Simple DAGs, `τ ≥ 2`, complete:** `n = 7` (see `experiments/woodall-dijoin-exact-ip/results/`
for the exact per-run counts).

`τ ≤ 1` is excluded from the `n = 7` run and needs no search: if `τ = 0` some dicut is
empty and zero dijoins are required; if `τ = 1` every dicut is nonempty so `A` itself is a
dijoin. Both are two-line arguments, not appeals to anyone's authority.

**DAGs with parallel arcs, `τ ≥ 2`, complete:** `n = 3` with multiplicity ≤ 5, `n = 4` with
multiplicity ≤ 4, `n = 5` with multiplicity ≤ 2.

### Restricting to DAGs

Justified by condensation: arcs inside a strong component lie in no dicut, the condensation
has the same dicut family and the same `τ`, and a dijoin of the condensation lifts back.
This is stated as known in the problem `README.md` and is additionally regression-tested.

### What the enumeration is, exactly

Every DAG has a topological order, so up to relabelling its adjacency matrix is strictly
upper triangular. The sweep enumerates **all** strictly upper triangular 0/1 matrices on
`n` labelled vertices. This meets every isomorphism class of `n`-vertex DAG **at least
once**. It is **redundant, not isomorph-free** — a class with several topological orders is
visited several times. That wastes time and never loses coverage, which is the trade taken
because nauty is not installed in this container. Consequently the run counts here are
*not* comparable to the A003087 unlabelled counts quoted in #31.

### What it does NOT cover — stated plainly

- **Parallel arcs beyond the small multiplicity caps above.** This is a real gap, not a
  formality: condensations of general digraphs *do* have parallel arcs, so "Woodall holds
  for all simple DAGs on ≤ 7 vertices" does **not** formally imply "Woodall holds for all
  digraphs on ≤ 7 vertices". Any write-up that elides this is overclaiming.
- Simple DAGs on ≥ 8 vertices.
- `n = 7` instances with `τ ≤ 1` (excluded deliberately, argued above, not searched).
- Loops, which lie in no dicut and are irrelevant; the reference implementation's
  loop-handling is nonetheless cross-checked.

## What a negative answer rests on

For every instance in the covered box the answer was **positive** — a `τ`-packing was found
*and* independently re-verified. So the sweep never had to rely on the completeness of the
UNSAT side. That materially weakens the usual "the solver said infeasible" objection: no
infeasibility conclusion is load-bearing anywhere in this result. Had one appeared, the
problem rules would require an independently reimplemented exhaustive check before it could
be believed, and it would trigger the extraordinary-claim protocol.

## Open question this raised (flagged, not answered)

Parallel arcs make the multi-arc sweep exactly the **integer-capacitated** dijoin-packing
statement. The problem `README.md` records that Schrijver's Theorem 5 / Corollary 5a prove
the capacitated form for source–sink-connected digraphs, while §1's Schrijver filter warns
that "the weighted version" (Edmonds–Giles) is false. **Edmonds–Giles is the min-max on the
other side** (weighted Lucchesi–Younger: minimum-weight dijoin versus a capacitated packing
of *dicuts*), so it is not literally the capacitated Woodall statement, and I could not
determine from repo contents whether capacitated Woodall is itself known false.

I did not resolve this and **the network blocks every scholarly host**, so I am recording it
rather than guessing. It matters practically: if capacitated Woodall is known false, then a
counterexample exists and my multi-arc sweep bounds where it can live, which turns the
multi-arc sweep into a search with a *known* answer — the single most valuable validation
target available for this tooling. That is a concrete next step for a literature task.

## Results

No counterexample anywhere. Headline figures (authoritative copies in
`../../../../experiments/woodall-dijoin-exact-ip/results/`):

| run | space | decided | `τ` range | counterexamples | wall |
|---|---|---|---|---|---|
| `n = 6`, all `τ` | 32,768 matrices | 32,767 | 0–5 | **0** | 4.5 s |
| `n = 7`, `τ ≥ 2` | 2,097,152 matrices | 1,047,613 | 2–6 | **0** | 436 s |
| `n = 4`, mult ≤ 4 | 15,625 vectors | 13,744 | 2–12 | **0** | 3.0 s |
| `n = 5`, mult ≤ 2 | 59,049 vectors | 43,693 | 2–8 | **0** | 9.5 s |

Every positive answer carries an explicit `τ`-packing that was re-verified against the full
dicut family and for pairwise disjointness. **No infeasibility conclusion occurs anywhere in
this result**, so nothing here depends on trusting an UNSAT.

## Kill-criterion and its outcome

Stated on #73 before launching: stop and report the negative if no counterexample is found
up to `n` vertices and the extrapolated cost of `n + 1` exceeds the budget.

**The kill-criterion fired at `n = 8`, on cost.** Measured: `n = 7` took 436 s. Going to
`n = 8` multiplies the matrix count by `2^28 / 2^21 = 128`, and per-instance work grows
roughly as `2^n · |A|`, i.e. by a further `(256·28)/(128·21) ≈ 2.7`. That projects
`436 · 128 · 2.7 ≈ 1.5 × 10^5` s ≈ **42 hours** single-process — against a one-hour
unattended budget on 4 CPUs shared with six other workers. Two orders of magnitude out;
no amount of constant-factor tuning closes it. Isomorph-free generation would remove the
topological-order redundancy (a real but bounded factor) and still leave `n = 8` far out of
reach on this budget.

So the search stopped at `n = 7` and reports the negative. Per `../../RULES.md` §0 and the
problem rules §2, a clean negative with a precisely stated coverage set is a **success**,
not a disappointment, and it is reported as one.

## Effect on the blocked issues

- **#7** — its stale blocker is identified and the search it asked for is delivered for
  `n ≤ 7`. Its own kill-criterion ("if the reachable vertex count plateaus, stop and write
  up the coverage achieved") is satisfied.
- **#31** — its premise needs correcting before anyone works it: it asks for the A003087
  unlabelled counts (243,668 at `n = 7`) via a pinned nauty, which is **not installed
  here**. Redundant upper-triangular enumeration reaches the same coverage without it. Its
  "validation gate" also required reproducing #7's corpus, which never existed.

## Reproduction

One command each; see `../../../../experiments/woodall-dijoin-exact-ip/README.md`.
