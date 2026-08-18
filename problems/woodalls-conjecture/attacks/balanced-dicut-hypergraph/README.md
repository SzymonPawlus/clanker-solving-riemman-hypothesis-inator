# Balanced dicut hypergraphs

Status: **refuted** (the proposed structural sufficient condition fails)

## Definitions

For a finite digraph `D=(V,A)` and `U` a proper nonempty subset of `V`, the
outgoing cut `delta+(U)` is a **dicut** when `delta-(U)` is empty and
`delta+(U)` is nonempty. A **dijoin** is an arc set meeting every dicut, and
`tau(D)` is the minimum cardinality of a dicut. A **dibond** means an
inclusion-minimal nonempty dicut as an arc set.

Let `B(D)` be the hypergraph whose vertices are the arcs of `D` and whose
hyperedges are its dibonds. Its transversals are dijoins: hitting all dibonds
is equivalent to hitting all dicuts. Its minimum hyperedge size is `tau(D)`.

## Cited engine

Theorem 4.1 of Gollin, Heuer, and Stavropoulos (2022), quoting Berge, states
that a finite balanced hypergraph has as many pairwise disjoint transversals
as the minimum size of a hyperedge. Consequently, balancedness of `B(D)` is a
sufficient condition for `D` to satisfy Woodall's conclusion.

Reference: J. Pascal Gollin, Karl Heuer, and Konstantinos Stavropoulos,
“Disjoint dijoins for classes of dicuts in finite and infinite digraphs,”
*Combinatorial Theory* 2(3), 2022,
<https://doi.org/10.5070/C62359180>.

## Concrete conjecture tested

> If `D` is a DAG and the bipartite reachability graph between its sources and
> sinks is a forest, then `B(D)` is balanced.

This conjecture is false. The kill criterion fired at five vertices, ending the
proof stage of this attack.

## Exact refutation

Take the DAG on vertices `0,1,2,3,4` with arcs

```text
0->1, 0->2, 0->3, 1->3, 1->4, 2->3, 2->4.
```

Its only source is `0` and its sinks are `3` and `4`. Thus its bipartite
source-to-sink reachability graph is the two-edge star with edges `0--3` and
`0--4`, which is a forest.

The following three dibonds and three selected arc-vertices form a proper odd
Berge cycle:

| dibond | source shore | selected arcs in the dibond |
|---|---|---|
| `{0->1, 0->3, 2->3, 2->4}` | `{0,2}` | `0->3, 2->4` |
| `{1->4, 2->4}` | `{0,1,2,3}` | `2->4, 1->4` |
| `{0->2, 0->3, 1->3, 1->4}` | `{0,1}` | `1->4, 0->3` |

Restricting the incidence matrix to these three rows (arcs) and three columns
(dibonds) gives exactly two `1`s in each row and column. Hence the dibond
hypergraph is not balanced.

This only refutes balancedness as a sufficient-condition route for the stated
forest-reachability class. The graph has a unique source and is therefore in a
known positive class for Woodall's conjecture; it is not a counterexample to
Woodall.

## Mandatory filters

- **Schrijver:** the Berge step itself can prove stronger capacitated results
  under an extra balancedness hypothesis. It therefore cannot be promoted to
  a proof for all unweighted digraphs. This route is retained only as a
  restricted-class search; an unweighted unbalanced `B(D)` is expected to
  block any general extrapolation.
- **Lucchesi–Younger:** the argument uses Berge's theorem on hypergraph
  transversals, not Lucchesi–Younger with dicuts and dijoins interchanged.
- **Easy direction:** Berge supplies `tau(D)` actual pairwise disjoint
  transversals, hence the nontrivial existence direction.

## Experiment and kill criterion

The exact code in `experiments/woodalls-balanced-dicuts/` was designed to enumerate every
subset of the `n(n-1)/2` arcs `u -> v` with `u < v`, for `1 <= n <= 6`:

`1 + 2 + 8 + 64 + 1024 + 32768 = 33867` instances.

These are fixed-topological-order labeled DAGs, not isomorphism classes; a DAG
with several topological orders can occur more than once. The code contracts
no SCCs because every enumerated graph is already acyclic. All positive census
findings remain **numerical**. Every negative balancedness finding must carry
an explicit odd Berge-cycle witness.

The kill criterion fired during `n = 5`, after all 1,099 fixed-order instances
through five vertices had been checked. The structural conjecture is therefore
marked **refuted** and was not rescoped. The induced-cycle detector agreed on
all 1,099 instances with the independent definition-level oracle that directly
enumerates odd square incidence submatrices. These exhaustive observations are
still **numerical** evidence about the implementation, not a general theorem.

The unrun `n = 6` portion is deliberately omitted: once the stated kill
criterion fired, further census work no longer served this attack.
