# Fixed-trace dicuts have the full packing property

**Issue:** #237. **Status:** `sketch`, targeting `verified:review`.

This removes every residual branch-bit and terminal-clamping obstruction for
a single optional separator trace.  For any fixed trace whose local
boundaries are all nonempty, an auxiliary integral max-flow packs exactly as
many pairwise arc-disjoint trace covers as the smallest trace boundary has
arcs.

The theorem is noncomputational.  It closes the full `tau=3` two-piece regime
with one relevant optional trace and no relevant forced traces, without any
clamping, source--sink connectivity, or bound on the number of residual SCC
membership bits.

## Definitions and sanity checks

For a finite digraph `D=(V,A)`, a **dicut** is a nonempty outgoing boundary
`delta+(U)` with `delta-(U)=empty`.  A **dijoin** meets every dicut.

Fix a vertex set `S` and a proper nonempty trace `T subset S`.  Let
`B_D(T)` be the boundaries `delta+(U)` of all incoming-closed shores satisfying

```text
U intersection S = T.                                   (1)
```

Assume at least one such shore exists and every such boundary is nonempty.
This is exactly the local “optional trace” situation: there is no empty
realization.  Define

```text
mu_D(T) = min{|B| : B in B_D(T)}.
```

A **T-cover** is an arc set meeting every boundary in `B_D(T)`.

The no-entering condition is essential.  On a directed path the dicut shores
are prefixes; a directed cycle has no dicut; and
`s1->t1, s2->t1, s2->t2` has singleton-source dicuts even though `s1` cannot
reach `t2`.  No arbitrary directed cut is substituted below.

## The auxiliary network

Let `M=|A|+1`.  Construct a capacitated network `N_T` with new source `sigma`
and sink `omega`:

1. for each original arc `a:u->v`, add a **forward** copy `u->v` of capacity
   one and a **reverse guard** `v->u` of capacity `M`;
2. for each `x in T`, add `sigma->x` with capacity `M`;
3. for each `y in S-T`, add `y->omega` with capacity `M`.

Parallel copies are kept distinct.  Capacity `M` plays the role of infinity,
but remains an ordinary integer.

**Lemma 1 (exact cut correspondence).**  The `sigma`--`omega` cuts of
capacity less than `M` are in bijection with the shores in (1), and their
capacities are the corresponding boundary cardinalities.  Consequently the
minimum network-cut value is `mu_D(T)`.

**Proof.**  Let `R` be the source side of a network cut of capacity below
`M`, and put `U=R intersection V`.  No terminal arc of capacity `M` crosses,
so `T subseteq U` and `U intersection (S-T)=empty`, proving (1).  No reverse
guard `v->u` crosses from `R` to its complement.  Hence an original arc
`u->v` can never have `u` outside `U` and `v` inside: `U` is incoming-closed.
The only crossing network arcs are therefore the unit forward copies, exactly
those corresponding to `delta+_D(U)`.  Cut capacity equals boundary size.

Conversely, take a shore satisfying (1).  The source side
`{sigma} union U` crosses no terminal capacity-`M` arc and no reverse guard,
because the shore is incoming-closed.  Its crossing arcs are precisely the
unit forward copies of its outgoing boundary.

Such a shore exists and its boundary has at most `|A|=M-1` arcs, so the
minimum network cut is below `M`.  The two directions above show that its
value is exactly `mu_D(T)`.  QED

## Full fixed-trace packing theorem

**Theorem 2.**  There exist `mu_D(T)` pairwise arc-disjoint `T`-covers.

**Proof.**  All capacities in `N_T` are integral.  Integral max-flow/min-cut
and Lemma 1 give an integral `sigma`--`omega` flow of value `mu_D(T)`.  Remove
flow cycles and decompose the remaining integral flow into
`mu_D(T)` unit source--sink paths `P_1,...,P_mu`.

For each `j`, let `X_j` be the original arcs whose unit forward copies occur
on `P_j`.  A forward copy has capacity one, so no such arc occurs in two
different sets `X_j`; the sets are pairwise arc-disjoint.  Reverse guards and
terminal arcs may be shared by paths up to their capacity, but they are not
placed in any `X_j`.

Fix any trace shore `U`.  By Lemma 1 its auxiliary cut has capacity below
`M`, and no guard or terminal arc crosses it.  Every source--sink path must
leave its source side, so `P_j` crosses it on a unit forward arc belonging to
`delta+_D(U)`.  Therefore `X_j` meets that boundary.  This holds for every
trace shore and every `j`; all `X_j` are `T`-covers.  QED

Every path necessarily contains a unit forward copy: otherwise it could not
cross any finite cut from Lemma 1.  Thus no empty artifact is counted as a
cover.

## Exact implication/branch-bit interpretation

The construction also solves the residual binary state system explicitly.
Give each vertex a Boolean variable saying whether it belongs to the shore.
For every original arc `u->v`, incoming closure is the implication

```text
v in U  =>  u in U.
```

Pin every vertex of `T` true and every vertex of `S-T` false.  These Horn
two-variable clauses describe exactly all fixed-trace shores, including any
number of rogue source/sink membership bits.

For an arc set `X`, asking for a trace boundary disjoint from `X` adds the
reverse implication

```text
u in U  =>  v in U       for every u->v in X.
```

Equivalently, use every reverse guard and only the forward copies belonging
to `X`.  The augmented implication system is inconsistent exactly when
`omega` is reachable from `sigma`, which is exactly when `X` is a `T`-cover.
Thus the apparent 2-SAT state does not require enumerating assignments: it is
ordinary reachability, and packing its certificates is the max-flow of
Theorem 2.

In particular, the number of residual branch bits need not be bounded by a
five-arc external interface.  Their implication closure is what matters, and
the flow theorem handles arbitrarily many of them at once.

## Closing the one-optional-trace `tau=3` regime

Let `D=D1 union D2` be an arc-disjoint separator sum.  Suppose there is
exactly one relevant trace `T`, it is optional on both sides, and there are no
relevant forced traces.  Let the two local minima be `mu_1,mu_2`.

Minimum local shores have the same trace and unite to a global dicut whose
size is `mu_1+mu_2`.  Therefore `tau(D)=3` implies

```text
mu_1+mu_2 >= 3.                                          (2)
```

By Theorem 2, piece `i` supplies `g_i=min(3,mu_i)` disjoint `T`-covers.  Pad
each family to three slots with empty sets.  Inequality (2) gives
`g_1+g_2>=3`.  Pair every noncovering slot on one side with a covering slot on
the other; the elementary inequalities

```text
3-g_1 <= g_2,   3-g_2 <= g_1
```

make this possible.  Each paired union covers `T`, hence meets every global
dicut, and the three unions are arc-disjoint.  They are three global dijoins.

**Corollary 3.**  Woodall's conjecture holds for every `tau=3` two-piece
separator sum with exactly one relevant optional trace and no relevant forced
trace.

This removes the local-adequacy hypothesis of PR #227 and all clamping
hypotheses of PRs #230 and #235.  Relevant forced traces, or two or more
optional traces competing for the same unit arcs, are the remaining separator
compatibility regimes.

## Why this does not prove general Woodall

The pins in (1) are load-bearing.  They turn one fixed trace family into the
finite cuts separating one source terminal set from one sink terminal set.
For the full dicut family, different shores can have different separator
traces; there is no single pair of terminal pins and no single-commodity
flow.  Combining several traces asks the same unit arc to serve competing
terminal pairs, leading back to the Hall/multicommodity obstruction rather
than a max-flow theorem.

Thus applying this construction without fixing `T` would be invalid.  The
argument proves a substantial local packing theorem and the stated separator
class, not Woodall's conjecture in general.

## Mandatory filters

1. **Schrijver filter: passed.**  Unit forward capacities encode distinct
   unweighted arc copies and yield genuinely arc-disjoint covers.  The
   fixed-trace theorem has a valid capacitated network analogue, but the false
   weighted Edmonds--Giles conclusion would require combining all traces from
   weighted `tau`; the terminal pins explicitly prevent that inference.
   Zero-weight structural arcs in a weighted digraph would be reverse guards,
   not usable unit cover arcs.
2. **Lucchesi--Younger filter: passed.**  Lucchesi--Younger is not invoked.
   This is ordinary single-commodity max-flow/min-cut in the explicitly
   constructed auxiliary network.  Lemma 1 proves from definitions that its
   finite cuts are exactly the fixed-trace dicuts, and the path sets are
   checked directly against every such dicut.
3. **Easy-direction filter: passed.**  Theorem 2 constructs all `mu_D(T)`
   disjoint covers from flow paths.  Corollary 3 then explicitly pairs them
   into three global dijoins; neither conclusion is the trivial upper bound.

## Dependency and review targets

The only external theorem is integral max-flow/min-cut.  A primary reference
is L. R. Ford Jr. and D. R. Fulkerson, “Maximal Flow Through a Network,”
*Canadian Journal of Mathematics* **8** (1956), 399--404,
<https://doi.org/10.4153/CJM-1956-045-5>.

The new reduction and Woodall special case remain `sketch` pending
independent review.  The highest-risk points are the direction of the reverse
guards in Lemma 1, path decomposition with shared capacity-`M` guards, and
the claim that each unit path yields a cover rather than merely one hit of a
minimum boundary.
