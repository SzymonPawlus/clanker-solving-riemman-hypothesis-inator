# 2026-08-19 — exact dijoin packing, and why #7/#31 were never really blocked

Issue #73. Attack: `problems/woodalls-conjecture/attacks/dijoin-exact-ip-search/`.

## The thing I got wrong at the start, and corrected

I assumed #7 and #31 carried the `blocked` label because someone had hit a genuine
computational wall. They had not. #7 said "blocked on the dicut/dijoin implementation" and
that implementation landed in #6 / PR #20. The label was simply stale. #31 then inherited
the block transitively.

The *real* obstruction was in the shape of the algorithm and nobody had written it down:
`woodalls-dicuts/woodall.py` decides a packing by enumerating every dijoin, i.e. iterating
all `2^|A|` arc subsets, then backtracking over that list. It is a correct and carefully
tested reference implementation — it just cannot be the engine of a census. Reading the
code rather than the labels was the highest-value ten minutes of this task.

## The reformulation

Supersets of dijoins are dijoins ⟹ leftover arcs can be dumped anywhere ⟹

> `τ` disjoint dijoins exist ⟺ the arcs can be `τ`-coloured so every dicut sees all `τ`
> colours.

Polychromatic colouring of the dicut hypergraph. `|A|` variables over `τ` values instead of
`2^|A|` subsets, and the minimum dicuts (size exactly `τ`) become AllDifferent constraints
that propagate hard. This is the whole content of the speedup.

It is *my* lemma, so §3 forbids me from resting on it — including resting on it myself.
I handled that by making every positive answer carry an explicit witness re-verified
against the full dicut family by a second code path, so "holds" never depends on the lemma
being right.

## What actually caught bugs

Two things, and neither was the maths.

1. The colouring search stops as soon as every dicut is polychromatic, which can leave arcs
   uncoloured. My witness reconstruction then did `colour[a]` and raised `KeyError`. A
   crash, so harmless — but it is exactly the shape of bug that, one refactor away, silently
   emits a bad witness.
2. A test assertion of mine was **wrong while the code was right**: for `0→1, 1→2` I claimed
   `{1→2}` is not a dicut. It is — shore `{0,1}` is closed. The independent reference said
   so first. I had written the test from the intuition "the shore is `{1}`" without checking
   the other shore. This is precisely the §0 failure mode, and the only reason I caught it
   in seconds is that I had wired in the cross-check before running anything.

Lesson I want to keep: the agreement harness against a differently-shaped implementation
earned its cost twice over, and it earned it *before* any sweep ran, not after.

## The coverage claim I nearly overstated

My first instinct was to write "no counterexample among all digraphs on ≤ 7 vertices".
That is false. I enumerate *simple* DAGs, and the condensation of a general digraph can
carry **parallel arcs** between two strong components. So simple-DAG coverage does not
imply digraph coverage. I added `sweep_multi.py` for exactly that gap and capped the
multiplicity explicitly rather than quietly hoping it did not matter.

Second near-overstatement: my enumeration is redundant, not isomorph-free. #31 wanted
counts compared against OEIS A003087. Mine cannot be — upper-triangular enumeration visits
a class once per topological order. Redundancy costs time, never coverage, but the counts
are not unlabelled counts and saying otherwise would be a fabricated number.

## Something worth someone else's time

Parallel arcs = integer capacities, so `sweep_multi.py` is literally the **capacitated**
dijoin-packing statement. The problem RULES §1 "Schrijver filter" warns that the weighted
version is false — but that filter is about **Edmonds–Giles**, which is the min-max on the
*other* side (weighted Lucchesi–Younger). It is not literally capacitated Woodall, and I
could not establish from repo contents whether capacitated Woodall is known false. Every
scholarly host 403s at the egress proxy, so I stopped rather than guess.

If capacitated Woodall *is* known false, a counterexample exists, my multi-arc sweep bounds
where it can live, and that sweep becomes a validation target with a **known answer** —
which is worth more than any further vertex count. Flagged in the attack README as a
literature task.

## Outcome

No counterexample anywhere in the covered box, with witnesses. The kill-criterion fired on
cost. Per §0 that is a success and I have reported it as one.
