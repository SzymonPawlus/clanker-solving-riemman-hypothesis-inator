# Tau-preserving arc saturation

Status: **sketch** (elementary lemma awaiting independent review) plus a
separate **numerical** finite census.

## Definitions

For a proper nonempty vertex set `U`, `delta+(U)` is a **dicut** when it is
nonempty and `delta-(U)` is empty. A **dijoin** meets every dicut, and `tau(D)`
is the minimum cardinality of a dicut. The experiment works with simple DAGs
whose displayed vertex order is topological.

A DAG is **tau-saturated in a fixed topological order** if adding any missing
forward arc strictly raises `tau`.

## Elementary lifting lemma (sketch)

Let `e` be a new arc and suppose

```text
tau(D+e) >= 2.
```

Then every dijoin of `D` is a dijoin of `D+e`.

Indeed, take a dicut `delta+_(D+e)(U)`. Removing `e` cannot introduce an arc
entering `U`, so `delta-_D(U)` is still empty. If `delta+_D(U)` were empty,
the new dicut would be exactly the singleton `{e}`, forcing
`tau(D+e) <= 1`, contrary to the hypothesis. Thus `delta+_D(U)` is a nonempty dicut
of `D` contained in the new dicut. Every old dijoin hits it and therefore hits
the new dicut.

Consequently, any pairwise disjoint dijoins in `D` remain dijoins in `D+e`.
This implication does **not** preserve counterexamples while adding arcs: the
new graph can have additional dijoins, so a counterexample can disappear.
The previously proposed saturation corollary is therefore **refuted**.

The supported direction is downward. If `D+e` is a counterexample with
`tau(D+e)=tau(D)=k>=2`, then `D` is also a counterexample: a `k`-packing in
`D` would lift to one in `D+e`. Repeatedly deleting an arc whenever deletion
preserves `tau` therefore reduces a hypothetical counterexample to a
**tau-preserving-deletion-minimal** one. At such an endpoint no further arc
can be deleted while preserving `tau`; this says nothing about adding missing
arcs, and it does not reduce a multigraph with parallel arcs to a simple graph.

An explicit warning about the failed upward direction: for
`D={(0,2),(0,3),(1,2),(1,3)}` and `e=(0,1)`, both tau values are 2, but adding
`e` destroys old dicuts. New disjoint dijoins need not restrict to dijoins of
`D`, exactly where the invalid converse would be needed.

## High-risk structural conjecture

> Every tau-saturated DAG with `tau>=3` is source-sink-connected (every source
> reaches every sink).

This is a standalone falsification target about the strict definition above,
not an established claim and not a counterexample reduction. It does not
follow from the lifting lemma. The first exact strictly saturated DAG outside
that class kills the conjecture and ends its proof stage.

Strict saturation differs from the endpoint of repeatedly adding
tau-preserving arcs. A missing forward arc can lower `tau`; then it is not
added by that process, but it also prevents strict saturation. For example, a
transitive tournament on vertices `0,1,2` plus isolated vertex `3` has `tau=2`
under this file's convention, no missing forward arc preserves `tau`, and
every missing arc lowers `tau` to 1. It is not strictly saturated. Thus weakly
disconnected endpoints of the add-preserving process are intentionally not
evidence for the strict census claim.

Here a dicut always has a **nonempty** outgoing boundary. Some older code under
`experiments/woodalls-dicuts` retains empty boundaries and consequently reports
`tau=0` on weakly disconnected fixtures such as the one above. That convention
is not used by this experiment; no comparison may silently mix the two.

## Mandatory filters

- **Schrijver:** the contradiction from a newly created singleton cut uses
  unweighted cardinality and `k>=2`. The argument asserts no capacitated or
  weighted analogue.
- **Lucchesi-Younger:** no cut/dijoin duality theorem is used in the lifting
  step.
- **Easy direction:** the lemma preserves each actual dijoin in a supplied
  packing; it does not merely prove the trivial upper bound. The refuted
  upward counterexample corollary is recorded rather than inferred from the
  easy direction.

## Exact experiment and kill criterion

The code under `experiments/woodalls-tau-saturation/` enumerates all 33,867
subsets of forward arcs through six vertices. These are labeled DAGs in one
fixed topological order, with duplicates across possible topological orders;
the census is not isomorphism-free. Every `tau` value through five vertices is
cross-checked using an independent predecessor-bitset oracle.

If a tau-saturated `tau>=3` DAG is not source-sink-connected, the result must
include its exact arc list, a minimum dicut, and the `tau` value after adding
every missing forward arc. Regardless of outcome, the census is **numerical**
and cannot prove the structural conjecture.

The completed census found 55 saturated instances with `tau>=3` (one for
`n=4`, eight for `n=5`, and 46 for `n=6`). Every one is
source-sink-connected. This is only bounded numerical evidence; it neither
proves the structural conjecture nor addresses parallel-arc digraphs.

Dependencies: the source-sink-connected special case is cited in the problem
README; the lifting lemma and downward corollary above remain only a `sketch`
until cross-examined. The census is `numerical` and does not depend on either.
