# The forced bow-tie colouring and its exact internal obstruction

**Issue:** #223. **Status:** `sketch`; non-computational structural theorem.

This attacks the unique five-arc configuration isolated in PR #221 without
modifying or assuming that unreviewed file. The quotient colouring is forced,
and it extends immediately when dicut shores respect the four regions. In
general, however, the only remaining difficulty is a precise precolour-
extension problem inside those regions; suppressing it would be an invalid
separator lift.

## Setup and definitions

Let `X,Y` be crossing minimum dicut shores in a weakly connected unweighted
digraph with `tau=3`. Put

```text
A=X intersection Y, B=X\Y, C=Y\X, E=V\(X union Y).
```

Assume the five inter-region arcs are exactly

```text
a:A->B, b:A->C, c:A->E, d:B->E, e:C->E.              (1)
```

There are no other arcs between regions. A dicut is always nonempty and comes
from a nonempty proper shore `U` with `delta-(U)=empty`. A dijoin meets every
such dicut.

The four canonical cuts are

```text
delta+(A)       ={a,b,c},
delta+(X)       ={b,c,d},
delta+(Y)       ={a,c,e},
delta+(A∪B∪C)  ={c,d,e}.                              (2)
```

## Forced boundary-colour theorem

Suppose three pairwise arc-disjoint dijoins exist. Since every set in (2) has
three arcs, each of its arcs must belong to a different dijoin: three disjoint
sets must each hit a three-element cut.

Colour an arc by the dijoin containing it. After permuting colours, the first
cut gives

```text
colour(a)=1, colour(b)=2, colour(c)=3.
```

The second cut then forces `colour(d)=1`, and the third forces
`colour(e)=2`; the fourth is automatically rainbow. Thus every packing has
the unique boundary pattern

```text
Q1={a,d}, Q2={b,e}, Q3={c},                            (3)
```

up to permuting the three dijoins. This is a necessity theorem, not a
heuristic choice of colours.

## Exact saturated-shore extension

Call the four-region partition **shore-saturated** when every incoming-closed
shore is a union of whole regions. Then the three sets in (3) are themselves
pairwise arc-disjoint dijoins.

Proof. A nonempty proper incoming-closed union of regions is an ideal in the
four-vertex quotient of (1). Its only possibilities are

```text
A, A∪B, A∪C, A∪B∪C.
```

Their cuts are precisely (2), and every row meets each `Qi`. This explicitly
constructs three dijoins.

A useful checkable sufficient condition for shore-saturation is that every
induced region is strongly connected. If an incoming-closed shore contains
one vertex of a strongly connected region and omits another, a directed path
inside the region has a first arc entering the shore, contradiction.

Hence a bow tie whose four regions are strongly connected cannot occur in a
counterexample. More sharply, any counterexample containing (1) must have a
noncanonical dicut shore that splits at least one of `A,B,C,E`; otherwise the
explicit packing (3) settles it.

## Exact rooted demand left by a split region

For an arbitrary dicut `F`, let `F_Q=F intersection {a,b,c,d,e}`. Pattern (3)
already supplies colour `i` exactly when `F_Q intersection Qi` is nonempty.
Define the missing-colour set

```text
M(F)={i in {1,2,3}: F_Q intersection Qi=empty}.        (4)
```

Any extension of (3) to a global packing must assign, for every `i in M(F)`,
an internal arc of `F` to colour `i`. Conversely, an assignment of every
internal arc to at most one colour satisfying these demands makes
`Qi union {internal arcs of colour i}` three disjoint dijoins. This is an iff,
obtained directly from the definition of dijoin.

Thus the irreducible obstruction is exact: it is a failure of three disjoint,
colour-respecting transversals for the internal residual families

```text
H_i={F\{a,b,c,d,e}: F a dicut and i in M(F)}.          (5)
```

An empty member of some `H_i` is an immediate obstruction: it is a dicut made
entirely of quotient arcs but missing forced colour `i`. Otherwise a minimal
bow-tie counterexample must contain a split shore and a genuine disjoint-
transversal obstruction among the three rooted families (5). In the
shore-saturated case neither can occur, because the only quotient-only cuts
are the four rainbow rows (2).

This explains why a separator theorem that records only local values of
`tau` is insufficient: it forgets which of the three forced boundary colours
each split shore still demands.

## Bow tie does not force the cited source--sink class

The shortcut “the five-arc quotient is source--sink connected, so the whole
digraph is” is false. Start with (1), take singleton `A,C,E`, and replace `B`
by vertices `z,B,w`. Inside that region put three parallel arcs `z->B` and
three parallel arcs `z->w`; retain `a:A->B` and `d:B->E`.

The sources are `A,z` and the sinks are `E,w`. There is no path from `A` to
`w`, so the DAG is not source--sink connected. Nevertheless `tau=3`:

- every shore containing `A` has at least the three arcs of one canonical
  quotient cut unless it also contains `z`, in which case additional internal
  arcs can only increase the boundary;
- a shore not containing `A` is either based at `z`; if it contains neither
  `B` nor `w` its boundary has six arcs, if it contains exactly `w` it has the
  three parallel `z->B` arcs, and if it contains `B` its boundary includes
  `B->E` together with the remaining applicable arcs; direct case separation
  gives at least three;
- `delta+(A)={a,b,c}` and `delta+({z,w})` (the three parallel arcs) show
  equality.

It still has three explicit dijoins: add one parallel `z->B` arc and one
parallel `z->w` arc to each `Qi` in (3). The quotient bow tie is therefore
neither a counterexample nor a certificate that the cited theorem applies.
The split-shore demands (5), not quotient reachability, are the correct next
object.

## Mandatory filters

1. **Schrijver filter.** Unweightedness is used when a three-arc minimum cut
   forces three distinct unit-capacity colours and hence the unique pattern
   (3). With weights, three displayed arcs need not provide three available
   packing slots, and zero-weight arcs destroy the inference. No weighted
   Edmonds--Giles claim is made.
2. **Lucchesi--Younger filter.** No min-max theorem and no interchange of
   dicuts with dijoins is used. Each `Qi` is checked directly against every
   quotient dicut; (4)--(5) are just the hitting-set definition expanded.
3. **Easy-direction filter.** The saturated case proves existence by the
   explicit three sets (3), and the nonsaturated case gives a necessary and
   sufficient extension condition. Neither merely repeats the trivial upper
   bound of three.
