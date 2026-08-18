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
tau(D+e) = tau(D) = k >= 2.
```

Then every dijoin of `D` is a dijoin of `D+e`.

Indeed, take a dicut `delta+_(D+e)(U)`. Removing `e` cannot introduce an arc
entering `U`, so `delta-_D(U)` is still empty. If `delta+_D(U)` were empty,
the new dicut would be exactly the singleton `{e}`, forcing
`tau(D+e) <= 1`, contrary to `k >= 2`. Thus `delta+_D(U)` is a nonempty dicut
of `D` contained in the new dicut. Every old dijoin hits it and therefore hits
the new dicut.

Consequently, `k` pairwise disjoint dijoins in `D` remain `k` pairwise
disjoint dijoins in `D+e`. Repeating the step shows that a **simple-DAG**
counterexample with `tau>=2`, if one exists, can be extended along a fixed
topological order to a tau-saturated simple-DAG counterexample. This does not
reduce a multigraph with parallel arcs to a simple graph.

## High-risk structural conjecture

> Every tau-saturated DAG with `tau>=3` is source-sink-connected (every source
> reaches every sink).

This is a falsification target, not an established claim. Combined with the
lifting lemma and the cited source-sink-connected special case, it would be
far too strong to infer from a small census. The first exact saturated DAG
outside that class kills the conjecture and ends its proof stage.

## Mandatory filters

- **Schrijver:** the contradiction from a newly created singleton cut uses
  unweighted cardinality and `k>=2`. The argument asserts no capacitated or
  weighted analogue.
- **Lucchesi-Younger:** no cut/dijoin duality theorem is used in the lifting
  step.
- **Easy direction:** the lemma preserves each actual dijoin in a supplied
  `k`-packing; it does not merely prove the trivial upper bound.

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
README; the lifting lemma above is only a `sketch` until cross-examined.
