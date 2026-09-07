# Two-separator shores: exact obstruction to the block argument

**Issue:** #208. **Status:** `sketch`; non-computational structural theorem
and counterexample to the naive two-separator extension of Issue #206. This
does not edit or assume the Issue #206 proof.

## Definitions

All digraphs here are finite and unweighted. For `U subseteq V(D)`, write

```text
delta+(U) = {uv in A(D): u in U, v notin U},
delta-(U) = {uv in A(D): u notin U, v in U}.
```

A **dicut shore** is a proper, nonempty `U` with `delta-(U)=empty` and
`delta+(U)` nonempty. Its dicut is `delta+(U)`. A **dijoin** meets every
nonempty dicut. The parameter `tau(D)` is the minimum cardinality of a
nonempty dicut. Empty outgoing boundaries are never dicuts.

Sanity checks: a consistently directed path has `tau=1`; a directed cycle has
no dicut; and in a DAG with two sources the union of any selection of source
components is an incoming-closed shore, but it counts only when its outgoing
boundary is nonempty.

## Shore fiber-product theorem

Let

```text
D = D1 union D2,
V(D1) intersection V(D2) = S,
A(D1) intersection A(D2) = empty,
```

and assume every arc of `D` belongs to one of the two pieces. Call a set
`X subseteq V(Di)` **closed** when `delta^-_Di(X)=empty`; unlike a dicut shore,
`X` may be empty or all of `V(Di)` and its outgoing boundary may be empty.

Then the closed shores of `D` are exactly the unions

```text
U = X1 union X2
```

of closed shores `Xi` of `Di` having the same separator trace

```text
X1 intersection S = X2 intersection S.                 (1)
```

For every such pair,

```text
delta+_D(U) = delta+_D1(X1) disjoint-union delta+_D2(X2). (2)
```

Proof. If `U` is closed in `D`, an arc entering `Xi=U intersection V(Di)`
would also enter `U`, so both restrictions are closed; they plainly have the
same trace. Conversely, under (1), membership of every endpoint is the same
whether tested in a piece or in the union. An arc entering `U` would therefore
enter one `Xi`, which is impossible. The same endpoint observation proves
(2), and arc-disjointness makes the union disjoint. This also proves that a
nonempty global dicut restricts to local closed shores, at least one of which
has nonempty outgoing boundary. Notice that a restriction need not itself be
a dicut: it may have empty boundary.

Consequently

```text
tau(D) >= min(tau(D1),tau(D2))                          (3)
```

whenever the displayed parameters exist. This is only a lower bound.

## Exact zero-cost lifting criterion

A local dicut `delta+_D1(X1)` lifts to a global dicut *with the same arc set
and cardinality* if and only if `D2` has a closed shore `X2` satisfying (1)
and

```text
delta+_D2(X2) = empty.                                  (4)
```

Necessity and sufficiency follow immediately from (2). Combining this with
(3) gives the exact criterion behind the familiar minimum formula:

> `tau(D)=min(tau(D1),tau(D2))` if and only if some minimum dicut in a
> component whose tau equals that minimum has a zero-cost compatible lift in
> the other component.

For necessity, take a global minimum cut. At least one restricted boundary is
nonempty, hence has size at least its component's tau and therefore at least
the right side of (3). Equality forces that restricted cut to be minimum and
every other restricted boundary to be empty. Sufficiency is the lifted local
minimum together with (3).

For a one-vertex separator, every trace is either empty or the whole
separator. Choosing `X2=empty` or `X2=V(D2)` supplies (4), explaining exactly
why the Issue #206 mechanism works. For `S={x,y}`, the mixed traces `{x}` and
`{y}` cannot be supplied by those two free choices. If the underlying
undirected graph of `D2` is connected, a shore with both incoming and outgoing
boundary empty is only `empty` or `V(D2)`. Thus a mixed-trace minimum dicut has
no zero-cost lift. This is the missing hypothesis in the naive extension.

## Small exact counterexample

Let

```text
D1: x -> a -> y
D2: x -> b -> y.
```

The pieces are arc-disjoint and meet exactly in `{x,y}`. Each is a directed
path, so each has `tau=1`. Their union is the directed diamond. Its nontrivial
closed shores and outgoing cuts are

```text
{x}       : {x->a, x->b}
{x,a}     : {a->y, x->b}
{x,b}     : {x->a, b->y}
{x,a,b}   : {a->y, b->y}.
```

Every nonempty dicut has size two, so

```text
tau(D)=2 > 1=min(tau(D1),tau(D2)).                      (5)
```

All minimum shores of either path have mixed trace `{x}`. The other connected
path has no zero-boundary shore with that trace, exactly as the criterion
predicts.

This example refutes the stronger claim that the one-vertex `tau=min` proof
extends unchanged to arbitrary two-vertex sums. It does **not** refute
Woodall's conjecture or even preservation of its packing property: the diamond
has the two arc-disjoint dijoins

```text
J1={x->a,a->y},  J2={x->b,b->y},
```

as direct inspection of the four cuts shows. Rather, it proves that a
two-separator reduction must carry separator-trace states and sometimes
create more global dijoins than either component can pack by itself. Merely
restricting local packings and taking colour-indexed unions cannot establish
the required global multiplicity.

## Mandatory filters

1. **Schrijver:** no weighted Woodall theorem is inferred. The positive
   packing statement is only the displayed unweighted diamond, where unit arc
   counts give `tau=2` and the two explicit arc-disjoint sets give the
   existence direction. The fiber-product identities themselves are neutral
   structural facts, not a weighted packing theorem.
2. **Lucchesi--Younger:** no min-max theorem is invoked and dicuts/dijoins are
   never interchanged. Dijoins are checked against the four listed dicuts.
3. **Easy direction:** the endpoint is not the trivial upper bound on a
   packing. The two dijoins are explicitly constructed. The main result is a
   refutation of `tau=min` plus an iff lifting theorem.

The useful next target is therefore not unrestricted componentwise gluing.
It is a trace-aware two-terminal packing theorem whose states distinguish
`empty,{x},{y},{x,y}` and whose composition accounts for the additive boundary
formula (2).
