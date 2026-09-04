# Boolean intervals of traces have the full packing property

**Issue:** #240. **Status:** `sketch`, targeting `verified:review`.

This extends the fixed-trace max-flow theorem of PR #239 to several traces at
once.  Whenever the required traces form an interval of the Boolean lattice,
they are exactly one coarsely pinned shore family.  A single auxiliary
max-flow then packs as many pairwise arc-disjoint simultaneous covers as the
smallest boundary over the entire interval.

In particular, two adjacent optional traces always admit this full local
packing theorem.  A sharp four-arc `tau=3` example identifies the remaining
crossed-bottleneck phenomenon: the two pieces can attain their minima at
opposite traces, so global `tau=3` alone does not force three *simultaneous*
local covers.  The example still has three explicit global dijoins and shows
exactly where a genuinely two-trace compatibility argument must improve on
the one-flow sufficient condition.

## Definitions and conventions

For a finite digraph `D=(V,A)`, a **dicut** is a nonempty outgoing boundary
`delta+(W)` with no arc entering `W`.  A **dijoin** meets every dicut.

Fix a separator set `S`.  For `L subseteq U subseteq S`, write

```text
[L,U] = {T subseteq S : L subseteq T subseteq U}.
```

Let `B_D[L,U]` be the outgoing boundaries of all incoming-closed shores `W`
whose trace lies in this interval:

```text
L subseteq W intersection S subseteq U.                  (1)
```

Assume `L` and `S-U` are nonempty, at least one such shore exists, and every
such boundary is nonempty.  Put

```text
mu_D[L,U] = min{|delta+(W)| : W satisfies (1)}.
```

An **interval cover** meets every boundary in `B_D[L,U]`.

The no-entering condition is used throughout.  A directed path has prefix
dicuts; a directed cycle has no dicut; and the DAG
`s1->t1, s2->t1, s2->t2` has singleton-source dicuts although it is not
source--sink connected.  Arbitrary cuts with arcs in both directions are not
included.

## Coarse pins are exactly trace intervals

Define the coarsened separator

```text
S_0 = L union (S-U).
```

Condition (1) is equivalent to the single fixed coarse trace

```text
W intersection S_0 = L.                                 (2)
```

Indeed, (2) forces every vertex of `L` in and every vertex of `S-U` out,
while placing no restriction on the coordinates in `U-L`.  Their arbitrary
choices produce exactly the Boolean interval `[L,U]`.

This observation is the reason an interval is single-commodity.  A
non-convex collection of traces cannot in general be represented by one set
of terminal pins without adding the missing traces in its Boolean hull.

## Interval max-flow theorem

Let `M=|A|+1`.  Construct a network with source `sigma`, sink `omega`, and:

- a capacity-one forward copy `u->v` and capacity-`M` reverse guard `v->u`
  for every original arc `u->v`;
- a capacity-`M` arc `sigma->x` for every `x in L`;
- a capacity-`M` arc `y->omega` for every `y in S-U`.

**Theorem 1.**  The family `B_D[L,U]` has
`mu_D[L,U]` pairwise arc-disjoint interval covers.

**Proof.**  A network cut of capacity below `M` crosses no terminal pin, so
its original-vertex source side `W` contains `L` and excludes `S-U`, exactly
(1).  It crosses no reverse guard, so no original arc enters `W`.  Its only
crossing arcs are the unit forward copies of `delta+_D(W)`, and its capacity
is that boundary's cardinality.

Conversely, every shore satisfying (1) gives precisely such a finite network
cut.  One exists with capacity at most `|A|`, so the minimum network cut is
below `M` and equals `mu_D[L,U]`.

Integral max-flow/min-cut gives an integral flow of that value.  Delete flow
cycles and decompose it into unit source--sink paths.  For each path retain
the original arcs whose unit forward copies it uses.  Capacity one makes
these retained sets pairwise arc-disjoint.  Every path crosses every finite
network cut, and guards cannot cross one, so it crosses on a retained forward
arc of the corresponding original boundary.  Each retained set therefore
meets every member of `B_D[L,U]` and is an interval cover.  QED

No enumeration of the `2^|U-L|` traces or their residual SCC membership bits
is needed.

## Two adjacent traces

If traces `T_0,T_1` differ in exactly one separator vertex, they are
comparable; write `T_1=T_0 union {z}` after swapping their names.  Their
Boolean interval contains exactly those two traces:

```text
[T_0,T_1]={T_0,T_1}.
```

Provided both local families are nonempty and have no empty boundary,
Theorem 1 gives

```text
min(mu_D(T_0),mu_D(T_1))
```

pairwise arc-disjoint sets, every one of which covers **both** traces.  Thus
two adjacent traces have the full simultaneous packing property.  This is a
strict extension of packing either trace separately.

## Hull condition for an arbitrary trace collection

For a nonempty collection `C` of traces, define

```text
L_C = intersection of the traces in C,
U_C = union of the traces in C.
```

Its smallest Boolean interval is `[L_C,U_C]`.  If this hull is nondegenerately
pinned and all its shores have nonempty boundary, Theorem 1 gives
`mu_D[L_C,U_C]` disjoint covers of every trace in `C`.

Consequently the exact sufficient condition delivered by one auxiliary flow
for `k` simultaneous covers is

```text
mu_D[L_C,U_C] >= k.                                      (3)
```

This is exact for the coarse-pin method because finite cuts of its auxiliary
network include every trace in the hull.  It is not claimed necessary for
`C` itself: added hull traces may create a smaller cut even when the original
non-convex collection has `k` simultaneous covers.  That distinction is the
multi-trace obstruction rather than a hidden assumption.

## A closed two-trace `tau=3` separator class

Let `D=D1 union D2` be an arc-disjoint separator sum whose only relevant
global traces are two adjacent optional traces `T_0,T_1`, with no relevant
forced traces.  Define

```text
nu_i = min(mu_Di(T_0),mu_Di(T_1)).
```

Theorem 1 supplies `g_i=min(3,nu_i)` disjoint local slots which cover both
traces.  If

```text
nu_1+nu_2 >= 3,                                          (4)
```

then `g_1+g_2>=3`.  Pad each side to three slots with empty sets and pair each
noncovering slot with a simultaneous covering slot on the other side.  Every
paired union meets every global dicut, regardless of which of the two traces
it has, and the three unions are arc-disjoint.

**Corollary 2.**  Under (4), if `tau(D)=3`, the digraph has three pairwise
arc-disjoint dijoins.

Condition (4) follows automatically when the two pieces attain their local
trace minima at the same trace: the compatible minimum shores unite to a
global dicut, whose size is at least three.  More generally (4) is a direct,
checkable local condition.  This closes a genuine two-trace regime without
demanding full local dijoins.

## Sharp crossed-bottleneck example

Global `tau=3` does not by itself imply (4).  This failure is realizable with
four arcs, not merely an abstract rank profile.

Take `S={s,z,t}`, `T_0={s}`, and `T_1={s,z}`.  Let piece 1 contain

```text
a1:s->t,  b:z->t,
```

and piece 2 contain

```text
a2:s->t,  c:s->z.
```

The parallel copies `a1,a2` remain distinct.  In piece 1 the two trace
boundary sizes are `(1,2)`; in piece 2 they are `(2,1)`.  Hence
`nu_1=nu_2=1`, so their sum is only two.

In the union, the only nonempty dicuts are

```text
delta+({s})   = {a1,a2,c},
delta+({s,z}) = {a1,a2,b}.
```

Both have size three, so `tau(D)=3`.  Three disjoint dijoins are nevertheless
explicit:

```text
{a1},  {a2},  {b,c}.
```

The third dijoin combines a piece-1 slot covering only `T_1` with a piece-2
slot covering only `T_0`.  No single interval-flow slot sees that cross-piece
complementarity.  Thus (4) is sufficient but not necessary, and the exact
remaining two-trace problem is to align trace-specific defects across pieces,
not to strengthen the max-flow theorem falsely.

The example's interface uses only the three separator vertices and four arc
copies, so a bound of five interface arcs does not eliminate crossed
bottlenecks.

## Mandatory filters

1. **Schrijver filter: passed.**  Unit forward capacities encode distinct
   usable unweighted arcs.  The interval theorem has a valid capacitated
   single-commodity analogue, but combining non-convex trace collections is
   exactly where that reduction stops.  No weighted minimum over all dicuts
   is turned into a global packing, so Schrijver's counterexample is not
   contradicted.
2. **Lucchesi--Younger filter: passed.**  No dicut/dijoin role reversal is
   used.  The proof is ordinary integral max-flow/min-cut in an explicitly
   constructed terminal network, followed by a direct check that every path
   hits every interval boundary.
3. **Easy-direction filter: passed.**  Flow paths construct the simultaneous
   covers, and Corollary 2 explicitly pairs them into three global dijoins.
   The minimum-dicut upper bound is never substituted for existence.

## Dependency, status, and review targets

The external input is integral max-flow/min-cut: L. R. Ford Jr. and D. R.
Fulkerson, “Maximal Flow Through a Network,” *Canadian Journal of
Mathematics* **8** (1956), 399--404,
<https://doi.org/10.4153/CJM-1956-045-5>.

The new interval reduction and separator corollary remain `sketch` pending
independent review.  The highest-risk points are exact equivalence between
coarse pins and the Boolean trace interval, the simultaneous-cover conclusion
for each individual flow path, and the claim that the four-arc example has no
other nonempty dicuts.
