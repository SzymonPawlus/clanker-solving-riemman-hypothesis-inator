# Exact uncrossing classification for crossing minimum 3-dicuts

**Issue:** #219. **Status:** `sketch`; non-computational structural theorem.

The result classifies every crossing pair of minimum dicut shores in a weakly
connected unweighted digraph with `tau=3`. It is stronger than a bounded
enumeration: only three quotient multiplicity patterns are possible, and the
case with at most five distinct boundary arcs is unique.

## Definitions

For `U subseteq V(D)`, write `delta+(U)` for arcs leaving `U` and `delta-(U)`
for arcs entering it. A dicut shore is a nonempty proper `U` with
`delta-(U)=empty` and `delta+(U)` nonempty. A dijoin meets every nonempty
dicut, and `tau(D)` is the minimum dicut cardinality. Two shores `X,Y` cross
when all four regions

```text
A=X intersection Y,   B=X\Y,
C=Y\X,                E=V(D)\(X union Y)
```

are nonempty. Parallel arcs are allowed and counted with multiplicity.

Sanity checks: a directed path has `tau=1`; a directed cycle has no dicut;
and a two-source DAG may have disjoint incoming-closed shores. The condition
`delta-(U)=empty`, not merely `delta+(U) != empty`, is used throughout.

## Exact modular uncrossing

Incoming-closed shores are closed under intersection and union. For two such
shores, no arc can run in either direction between `B` and `C`: `B->C` would
enter `Y`, and `C->B` would enter `X`. Directly partitioning arcs by the four
regions therefore gives the exact identity

```text
|delta+(X)|+|delta+(Y)|
  = |delta+(X intersection Y)|+|delta+(X union Y)|.    (1)
```

This is equality, not merely cut submodularity.

If `D` is weakly connected, every nonempty proper incoming-closed shore has a
nonempty outgoing boundary: an undirected edge crosses the shore, and the
incoming orientation is forbidden. Hence, when `X,Y` cross and are minimum
shores, both their intersection and union are dicut shores. At `tau=3`, (1)
and the lower bound of three on both new cuts force

```text
|delta+(A)|=|delta+(X union Y)|=3.                     (2)
```

Thus crossing minimum shores uncross to two more minimum shores.

## Five-region count classification

The only possible inter-region arc types are

```text
A->B, A->C, A->E, B->E, C->E.
```

Let their respective multiplicities be `p,q,r,s,t`. The four minimum-cut
equalities for `X,Y,A,X union Y` are

```text
q+r+s=3,   p+r+t=3,   p+q+r=3,   r+s+t=3.             (3)
```

Subtracting equations yields

```text
s=p,  t=q,  p+q+r=3.                                  (4)
```

Moreover `p,q` are positive. If `p=0`, then (4) gives `s=0`; every other arc
incident with region `B` is forbidden by incoming-closedness, so `B` is a
union of weak components, contradicting weak connectivity. The same argument
with `C` proves `q>0`.

The nonnegative integer solutions of (4) are therefore exactly

```text
(p,q,r)=(1,1,1), (1,2,0), (2,1,0),                   (5)
```

with `(s,t)=(p,q)`. No search or simplicity assumption is involved.

## Sharp consequences

The common arcs of the two minimum dicuts are exactly the `A->E` arcs, so

```text
|delta+(X) intersection delta+(Y)|=r<=1.              (6)
```

Their combined boundary contains `6-r` distinct arcs. Consequently:

- crossing minimum 3-dicuts share at most one arc;
- if they share one arc—or equivalently their combined boundary has at most
  five arcs—the quotient is forced to the unique bow-tie pattern
  `(p,q,r,s,t)=(1,1,1,1,1)`;
- if they are disjoint, the quotient is one of the two mirror six-arc patterns
  `(1,2,0,1,2)` and `(2,1,0,2,1)`.

The five-arc bound is sharp: orient the five quotient arcs
`A->B,A->C,A->E,B->E,C->E`, with each region a single vertex. Then all four
displayed shores have boundary three and cross as stated.

This also gives a laminarity test: any family of minimum 3-dicut shores in
which each pair of boundary sets shares at least two arcs must be laminar,
because (6) rules out a crossing pair.

## Consequence for minimal counterexamples

A vertex-minimal counterexample to Woodall is weakly connected. Otherwise,
each smaller weak component satisfies Woodall whenever it has a dicut. Put
`k=min tau(component)` over the cut-bearing components, retain `k` disjoint
dijoins in each of them, use empty local sets in components having no dicut,
and union equal-index sets across components. Every global dicut restricts
nontrivially to some cut-bearing component, so these are `k=tau(D)` disjoint
global dijoins; arcs in no-dicut components may be distributed arbitrarily.
This is a contradiction.

Therefore any vertex-minimal counterexample with `tau=3` obeys the
classification above. In particular its minimum-shore family is either
laminar at a given pair, or that pair exposes one of exactly three quotient
patterns; every connected combined boundary on at most five arcs is the
five-arc bow tie. This is a finite structural target for subsequent gluing or
colour-extension arguments, obtained without claiming that the bow tie itself
is a counterexample.

## Mandatory filters

1. **Schrijver filter.** The decisive step is unweighted: `p,q` are positive
   *integer arc multiplicities*, so `p+q+r=3` has only the three solutions
   (5). With arbitrary nonnegative weights, connectivity does not make the
   crossing types have positive weight, and zero-weight arcs destroy this
   classification. No weighted Edmonds--Giles theorem follows.
2. **Lucchesi--Younger filter.** No dicut/dijoin roles are swapped and no
   min-max theorem is invoked. The only dijoin construction is the explicit
   componentwise union in the minimal-counterexample reduction.
3. **Easy-direction filter.** The minimal-counterexample reduction constructs
   exactly `tau(D)` disjoint dijoins from the smaller components. The main
   theorem is the uncrossing classification, not the trivial upper bound on
   the number of dijoins.
