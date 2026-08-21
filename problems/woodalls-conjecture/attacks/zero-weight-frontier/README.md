# The zero-weight frontier: how small can an Edmonds–Giles counterexample be?

```
status: sketch (all prose arguments) + numerical (the census) — nothing here is assumable
author: claude (Fable 5, ideation slot per RULES.md §8/§9.2), 2026-08-19
issue:  #72
code:   experiments/woodall-zeroweight-census/
```

**Read this first.** This file records an ideation round (three candidate attacks generated and
killed before compute, with the reasons) and one executed attack: an exhaustive census of small
`{0,1}`-weighted Edmonds–Giles instances. No claim here is assumable, including by its author.
The census is `numerical` and lives outside `results/`. A stated limitation throughout: **every
primary-source host was unreachable from this session** (network egress blocked; only search-result
snippets were available), so all literature attributions below are from memory or snippets and are
flagged for the cross-reviewer to verify against the actual papers.

---

## 0. Definitions (restated per problem RULES §4)

Let `D = (V, A)` be a digraph. For nonempty proper `U ⊊ V`, `delta+(U)` is the set of arcs with
tail in `U` and head outside, `delta-(U)` those with head in `U` and tail outside. A **dicut** is
`delta+(U)` with `delta-(U) = ∅` and `delta+(U) ≠ ∅`. A **dijoin** is an arc set meeting every
dicut. `tau(D)` is the minimum dicut size.

Weighted version (Edmonds–Giles). Give each arc a weight `w(a) ∈ Z≥0`, let
`tau_w = min over dicuts B of w(B)`, and call `J_1, …, J_k` a **w-packing** if each `J_i` is a
dijoin and every arc `a` lies in at most `w(a)` of them. The Edmonds–Giles conjecture asserted a
w-packing of size `tau_w` always exists; **Schrijver (1980) refuted it** with a `{0,1}`-weighted
instance (`cited` in the problem README). Woodall's conjecture is the `w ≡ 1` case and is open.

Sanity fixtures (all executable in the code's test suite): a directed path has its prefix
singleton dicuts; a directed cycle has no dicut; the near-miss DAG `s1→t1, s2→t1, s2→t2` has the
singleton dicut `delta+({s1})`; the two-path diamond has `tau = 2` and packs. The dicut test is
`delta-(U) = ∅`, not merely `delta+(U) ≠ ∅` — the test suite checks this on the RULES §4 example.

## 1. The ideation round: four angles, three killed before compute

The board's Woodall attacks to date (`tau2-robbins`, `tau-saturation`,
`tau3-saturated-source-sink`, `balanced-dicut-hypergraph`, `rho4-strong-base-orderability`) are
all **unweighted**; issues #7/#31 (blocked) plan unweighted counterexample censuses. Nothing on
the board touches the weighted side computationally. Angles generated this round:

### A. Search for a fractional packing gap — killed: the search space is provably empty

The idea was to hunt small digraphs where even the *fractional* dijoin-packing LP falls short of
`tau`. It dies before compute, by this argument (`sketch`; every ingredient is standard but the
citations are from memory — reviewer, please check):

1. The Lucchesi–Younger theorem in its weighted form (Lucchesi–Younger 1978; also via the
   Edmonds–Giles submodular-flow framework, 1977) makes the dicut-covering LP
   `{z ≥ 0 : z(B) ≥ 1 for all dicuts B}` integral for every nonnegative weight vector — i.e. the
   clutter of minimal dicuts is **ideal**.
2. Lehman's width–length theorem: the blocker of an ideal clutter is ideal. The blocker of the
   minimal-dicut clutter is the minimal-dijoin clutter (dijoins are exactly the transversals of
   dicuts).
3. So the dijoin-covering LP `{y ≥ 0 : y(J) ≥ 1 for all dijoins J}` is integral; with unit
   objective its optimum is the minimum *integral* transversal of dijoins, which is `tau`
   (blocker of the blocker is the original clutter). By LP duality, the maximum fractional
   packing of dijoins equals `tau` in **every** digraph.

So "fractional Woodall" holds always, and no instance exhibits a gap; the open content of
Woodall is purely the integrality of the packing (consistent with the recent literature moving
to *dyadic* packings — "Dyadic Packing of Dijoins", SIAM J. Discrete Math., found as a title in
search results). Note the failure mode this avoids: had this argument been wrong, the cost was
only that a search would have run and found empty; the argument is used to *refuse* compute,
never to assert anything downstream.

### B. Half-integral / uniform-capacity census — killed: instance-wise vacuous

"Check whether every small `D` admits `2·tau` dijoins with each arc in at most 2 of them."
Vacuous as a census: if `D` packs `tau` disjoint dijoins (Woodall holds for `D`), duplicating
each of them gives `2·tau` dijoins within capacity 2. So on any instance where Woodall has not
already failed, the half-integral question answers itself, and a census below the first
integral counterexample can never distinguish the two. The question is real only as a *general
theorem* target (equivalently, Woodall restricted to digraphs whose arcs all have even
multiplicity), which is not a computation.

### C. Positive-weight weighted search — killed as a separate frontier: it is multidigraphs

For `w ≥ 1` everywhere, replace each arc `a` by `w(a)` parallel copies: dicuts correspond, the
minimum dicut size becomes `tau_w`, disjoint dijoins in the expansion collapse to a w-packing,
and any w-packing lifts to disjoint dijoins on the copies. So the positive-weight version is
**exactly** the unweighted conjecture on multidigraphs — already noted in-repo
(`attacks/tau2-robbins`, quoting Cornuéjols–Liu–Ravi §1) — and multidigraph/simple censuses are
the territory of blocked issues #7/#31. Not taken, to keep off claimed ground.

### D. The zero-weight frontier — chosen

By C, weight `0` is the one genuinely weighted phenomenon: a zero-weight arc constrains the
dicut structure but can never be used. Schrijver's counterexample lives here, as (per the
snippets and memory) do all known counterexamples — solid (weight-1) arcs forming three
directed paths plus dashed (weight-0) arcs. Known structural results reported in the
literature (unverified this session): in any counterexample the weight-1 arcs form at least
three weakly connected components, and known counterexamples contain long chordless cycles.

**What nobody seems to have recorded** (no repo trace; nothing in reachable snippets — a
limited check, flagged as such): an *exhaustive minimality census*. What is the smallest
`{0,1}`-weighted instance with `tau_w ≥ 2` and no w-packing of size `tau_w`? Both outcomes are
useful: a small counterexample would be a hand-checkable new example (and a stress test of the
reported structure theorems); an empty census is a certified size bound below which the
Schrijver phenomenon cannot occur. Unlike the unweighted census (#7), the target set here is
**known to be nonempty**, so the machinery's infeasible branch is exercised against reality.

## 2. Reductions defining the search space (each with its argument)

Everything below is elementary; proofs are two lines each and stated so the reviewer can check
rather than trust.

1. **`tau_w ≤ 1` is always feasible.** `tau_w = 0`: the empty packing. `tau_w = 1`: every dicut
   has weight ≥ 1, so `S = {a : w(a) = 1}` meets every dicut; `S` itself is a single dijoin
   using each arc once ≤ `w`.
2. **Graphs with a singleton dicut never matter.** If `{a}` is a dicut then `tau_w ≤ w(a) ≤ 1`
   for every `{0,1}` weighting, so the whole weight cube on that graph is feasible by (1). The
   census skips such graphs wholesale (this is what makes it cheap).
3. **A minimal counterexample is weakly connected.** Dicuts of a disjoint union are the dicuts
   of the parts (padded arbitrarily with full other components on the shore side, which changes
   no arc set), `tau_w = min` of the parts', and dijoins are unions of per-part dijoins; if
   every part w-packs to its own `tau_w`, truncating to the global minimum packs the union.
4. **Condensation.** Arcs inside strong components lie in no dicut and may be added freely to
   any dijoin, so the instance is its condensation with inherited weights; parallel same-
   direction arcs arising from contraction merge by adding weights (they cross exactly the same
   dicuts). Hence WLOG a **simple DAG with integer weights**.
5. **Scope limit (stated, not assumed away):** restricting to `w ∈ {0,1}` on a *simple* DAG
   does **not** cover condensations whose merged weights reach 2 or more. The census space is
   exactly: weakly connected simple DAGs on `n` vertices, all `2^|A|` weightings `w ∈ {0,1}^A`.
   Nothing is claimed outside it.
6. **Coverage without canonicalisation.** Every DAG admits a topological labeling, under which
   its arcs are upper-triangular; enumerating **all** upper-triangular arc sets therefore meets
   every isomorphism class at least once (some classes many times — a speed cost, never a
   coverage gap).

## 3. The load-bearing encoding lemma (sketch — this is what to review hardest)

**Lemma.** Let `S` be the weight-1 arcs, `tau = tau_w ≥ 2`, and let `M_1, …, M_k` be the
inclusion-minimal dicut arc sets. A w-packing of size `tau` exists **iff** there is a colouring
`c : S → {1, …, tau}` such that every `M_j` contains all `tau` colours among its `S`-arcs.

*Proof sketch.* (⇐) Set `J_i = c^{-1}(i)`. Each arc lies in exactly one `J_i` (≤ `w`, and
weight-0 arcs in none). Every dicut `B` contains some minimal dicut arc set: the family of
dicuts with arc set ⊆ `B` is nonempty (it contains `B`) and finite, and an inclusion-minimal
member `M` of that family is minimal among *all* dicuts, since any dicut properly inside `M`
would itself belong to the family. `M = M_j` has all colours, so every `J_i` meets every
dicut: each is a dijoin, and they are pairwise disjoint within `S`.
(⇒) Given dijoins `J_1, …, J_tau` with each arc in ≤ `w(a)` of them, each `J_i` avoids weight-0
arcs and the `J_i ∩ S` are pairwise disjoint; colour `a ∈ J_i ∩ S` with `i`, leftovers with 1.
Supersets of dijoins are dijoins, so this only strengthens classes; each minimal dicut is met
by every `J_i` in an `S`-arc of colour `i`. ∎

**Generalisation used by the `{0,1,2}` cube** (same proof, bookkept per copy): give each arc
`w(a)` *slots*, colour every slot, and let `J_i` be the arcs having a slot of colour `i`. An
arc then lies in at most (number of distinct colours among its slots) ≤ `w(a)` of the `J_i`,
and conversely a w-packing dedicates one slot per dijoin containing the arc — the capacity
bound is exactly what makes that dedication injective. Slots beyond `tau_w` per arc are
redundant (an arc contributes at most `tau_w` distinct colours) and the code caps them.

A consistency fact the encoding relies on: `tau_w` may be computed over inclusion-minimal
dicut arc sets only, because weights are nonnegative; and every minimal dicut then carries
≥ `tau_w` slots by definition of `tau_w`.

## 4. Validation (RULES.md §6: known answers before any long run)

All in `experiments/woodall-zeroweight-census/test_census.py` (13 tests) or asserted during the
run:

- RULES §4 fixtures: path, cycle (no dicut), two-source near-miss, diamond; the
  `delta-(U) = ∅` requirement is tested explicitly.
- **Two independent implementations** of the packing decision (pruned backtracking vs. full
  enumeration of colourings) agree on *every* weighted instance on 4 vertices, exhaustively,
  and on every infeasible instance the census flags (in-run assert).
- **`tau = 2` unweighted theorem**: all unweighted `tau ≥ 2` instances on ≤ 4 vertices pack
  (test) — and an in-run assert fires if any unweighted `tau = 2` instance is ever reported
  infeasible.
- **Source–sink-connected filter**: Schrijver's capacitated theorem (`cited` in the problem
  README) makes any "infeasible" source–sink-connected instance a certain encoding bug; the
  census asserts this on every hit.
- **Lucchesi–Younger oracle**: `min dijoin size = max disjoint dicuts` verified exactly, by two
  brute-force computations, on every census graph with `n ≤ 5` (all 771 weakly connected DAG
  labelings among the 1 094 UT graphs). Consistency check only — LY is never used as a proof
  step toward the conjecture (problem RULES §1 filter 2).
- A hand-checkable synthetic infeasible fixture (three pairwise-overlapping traces, the odd
  structure that defeats 2-colouring) exercises the infeasible branch of both solvers.

## 5. Mandatory filters (problem RULES §1)

1. **Schrijver filter: passes trivially** — this attack proves nothing; it is falsification-mode
   only, aimed at the weighted regime where Schrijver's refutation lives. There is no argument
   here that could accidentally prove the weighted version.
2. **Lucchesi–Younger filter: passes** — LY appears only as a numerical consistency oracle on
   small instances (§4), never swapped for the conjecture.
3. **Easy-direction filter: passes** — the code decides the *existence* of the packing by
   exhaustive search; the trivial `≤ tau` direction appears nowhere.

## 6. The census and its result

Space (exact): for each `n`, all `2^(n(n-1)/2)` upper-triangular arc sets on vertices
`0 < 1 < … < n-1`, filtered to weakly connected; for each such DAG, all `(wmax+1)^|A|`
weightings `w ∈ {0..wmax}^A`; for each instance with `tau_w ≥ 2`, the packing decision of §3.
Two cubes were run: `wmax = 1` for `n ≤ 6` and `wmax = 2` for `n ≤ 5`. Deterministic, no
seeds; pure standard-library Python 3.11.15; one command (`run.sh`); checkpointed to
`out/census-n<N>[-w2].json` during the run; ~4 minutes total on one core.

| cube | n | UT graphs | weakly conn. | `tau ≥ 2` graphs | `tau_w ≥ 2` instances | infeasible |
|---|---|---|---|---|---|---|
| `{0,1}` | 2 | 1 | 1 | 0 | 0 | 0 |
| `{0,1}` | 3 | 7 | 4 | 1 | 1 | 0 |
| `{0,1}` | 4 | 63 | 38 | 10 | 46 | 0 |
| `{0,1}` | 5 | 1 023 | 728 | 253 | 6 441 | 0 |
| `{0,1}` | 6 | 32 767 | 26 704 | 11 968 | 2 577 230 | 0 |
| `{0,1,2}` | 2–4 | 71 | 43 | 11 | 1 570 | 0 |
| `{0,1,2}` | 5 | 1 023 | 728 | 253 | 558 738 | 0 |

**Result (`numerical`).** Every one of the 3 144 026 instances with `tau_w ≥ 2` in the two
cubes admits a w-packing of `tau_w` dijoins. Both censuses ran to completion (no budget
truncation). The `{0,1}`, `n = 6` cube was additionally run twice, before and after an inner-
loop refactor (bitmask weights vs. weight tuples), with identical counts.

Interpretation, strictly within the stated space: any `{0,1}`-weighted counterexample to
Edmonds–Giles whose condensation is a simple DAG needs **at least 7 vertices**, and weights up
to 2 do not create one on ≤ 5 vertices either. Equivalently — via §1C's parallel-arc reading of
weights — the Schrijver phenomenon needs more room than 6 condensation vertices at capacity 1.
This is consistent with (and much weaker than) the reported structural facts about known
counterexamples (§1D); it neither confirms nor tests them beyond this size. The census makes
no statement about Woodall's conjecture itself beyond re-verifying its unweighted instances in
range, and none of its outputs may be cited as more than `numerical`.

## 7. Kill-criteria accounting (RULES.md §6.2–6.3, restated verbatim from issue #72)

- **K1 (encoding)** — *"if validation fails … stop; write up as tooling refutation."* Did not
  fire: all 13 tests pass; no in-run assert tripped.
- **K2 (literature)** — *"if evidence surfaces that an exhaustive minimal-counterexample census
  already exists, stop and cite."* Did not fire, with the stated caveat that primary sources
  were unreachable this session; the reviewer should treat "no prior census" as unverified and
  downgrade this write-up to a reproduction note if one exists.
- **K3 (budget)** — *"one hour compute total; census truncated at budget is reported with its
  exact covered space."* Not reached: both cubes completed in ~4 minutes total (the `n = 6`
  cube in under 2 minutes per run), well inside the cap; no truncation occurred, and the
  `complete: true` flags in the committed JSONs record it.

## 8. What would extend this (not claimed, not scheduled)

- `n = 7` at `{0,1}` is a 2-million-UT-graph space whose weight cubes sum to `3^21 ≈ 10^10`
  raw instances; the singleton-dicut skip (§2.2) plus a compiled implementation might reach
  it, this pure-Python one will not.
- Weights `{0,1,2}` at `n = 6`, or `{0,1,2,3}` at `n ≤ 5`, would push the §2.5 scope boundary
  further out.
- Reconstructing Schrijver's actual instance from the paper (unreachable this session) and
  feeding it through the checker would upgrade the infeasible-branch validation from synthetic
  to historical; the checker is ready for it. The same goes for the Cornuéjols–Guenin and
  Williams examples, whose sizes would also calibrate how far this census is from the first
  known counterexamples.
