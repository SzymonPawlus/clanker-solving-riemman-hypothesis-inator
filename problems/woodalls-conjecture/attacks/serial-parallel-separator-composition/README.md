# Serial and parallel separator composition for dijoin packings

**Issue:** #214. **Status:** `sketch`; non-computational closure theorem.

This develops a trace-aware replacement for naive two-separator gluing. It is
self-contained and does not modify the frozen PR #211. The theorem applies to
arbitrary finite unweighted digraph pieces already known to satisfy Woodall,
not only to source--sink-connected pieces.

**Reference status (checked 2026-09-04).** PR #211 is **open and unmerged**, so
its content is not on `main` and cannot be checked from this file. Nothing below
depends on it: #211 is named only to say which earlier line of work this attack
declines to modify.

## Definitions and elementary restriction lemma

For `U subseteq V(D)`, a nonempty dicut is `delta+(U)` where `U` is nonempty
and proper, `delta-(U)=empty`, and `delta+(U)` is nonempty. A dijoin meets
every such dicut. Write `tau(D)` for the minimum dicut cardinality.

Let `D=D1 union D2`, with disjoint arc sets, all arcs in one of the pieces,
and arbitrary vertex intersection `S`. If `U` is an incoming-closed shore in
`D`, then `Ui=U intersection V(Di)` is incoming-closed in `Di`, the two traces
on `S` agree, and

```text
delta+_D(U)=delta+_D1(U1) disjoint-union delta+_D2(U2). (1)
```

Conversely, compatible incoming-closed component shores unite to such a
global shore. This follows by inspecting the endpoints of each arc. In
particular, every nonempty global dicut has a nonempty restricted boundary in
at least one piece.

Sanity checks use the required nonempty-cut convention: a directed path has
`tau=1`; a directed cycle has no dicut; and the two-branch diamond has
`tau=2`, not zero. Empty restrictions in (1) are allowed but are not called
dicuts.

## Two composition modes

Assume `Di` has `tau_i` pairwise arc-disjoint dijoins.

### Serial (minimum) mode

If

```text
tau(D)=min(tau_1,tau_2)=k,                              (2)
```

choose any `k` members of each component packing and index them as
`J_i^1,...,J_i^k`. Then

```text
J^r=J_1^r union J_2^r,  1<=r<=k                       (3)
```

are `k` arc-disjoint global dijoins. Indeed, a global dicut has a nonempty
restricted dicut in at least one component, and the corresponding member in
(3) meets it. Arc-disjointness follows both between colors and between pieces.

Condition (2) is checkable by shore traces: it holds exactly when a minimum
dicut in a component attaining `min(tau_1,tau_2)` has a compatible shore in
the other component with zero outgoing boundary. For a one-vertex sum this is
automatic by choosing the empty or full shore. For a larger separator this
is a genuine hypothesis, not a hidden lifting assumption.

### Parallel (additive) mode

Suppose instead that

1. every nonempty global dicut has nonempty restricted boundary in **both**
   pieces; and
2. the pieces have compatible minimum-dicut shores, so their union is a
   global shore.

Equation (1) then gives

```text
tau(D)=tau_1+tau_2.                                    (4)
```

The lower bound follows because both restrictions cost at least their local
taus; compatible minimum shores give equality. More importantly, every local
dijoin in either piece, viewed as an arc set in `D`, is already a global
dijoin: every global cut restricts nontrivially to that piece. Therefore keep
all component dijoins as separate colors:

```text
J_1^1,...,J_1^tau_1,J_2^1,...,J_2^tau_2.              (5)
```

They are pairwise arc-disjoint and, by (4), their number is exactly `tau(D)`.
This is the nontrivial parallel compatibility. Unioning equal colors, as in
serial mode, would throw away the additional `tau_1+tau_2-min(tau_1,tau_2)`
packings.

Thus Woodall's packing property is preserved by either composition mode.

## Decomposition-tree theorem

Let a digraph be built from arc-disjoint leaf pieces along a rooted binary
decomposition tree. Assume every leaf satisfies Woodall. At each internal
node require either the serial hypotheses (2), certified by a zero-cost trace
lift, or the two parallel hypotheses above. Then the digraph at every node,
and hence the root, has `tau` pairwise arc-disjoint dijoins.

Proof is induction on the tree. At a serial node use (3); at a parallel node
use (5). Both constructions are explicit, so the induction returns the
actual global dijoins rather than only their number.

This is a closure class parameterized by bounded separator traces, and it can
start from any proved positive leaf classes. It is not restricted to a
single source--sink-connected root. For example, disjoint unions are serial
nodes (a minimum cut lives in one component and lifts against the empty/full
shore), so disjoint unions of positive pieces are covered although a DAG with
sources and sinks in different weak components is not source--sink connected.
Further serial or parallel adhesions may then be applied without changing the
leaf theorem.

## Two-terminal series-parallel check

A two-terminal acyclic network has terminals `s,t` and every vertex lies on a
directed `s`--`t` path. Every nontrivial incoming-closed shore contains `s`
and excludes `t`: a path from `s` to a vertex in the shore forces `s` in,
while a path from a vertex outside to `t` rules out `t` in. Its boundary is
nonempty along an `s`--`t` path.

Consequently:

- series composition at a single identified terminal is serial mode and uses
  the colorwise unions (3);
- parallel composition along `{s,t}` is parallel mode: every cut restricts
  nontrivially to every branch, minimum shores all have trace `{s}`, taus add,
  and all branch dijoins remain separate as in (5).

Induction proves Woodall for two-terminal series-parallel DAGs and explicitly
constructs the packing. This corollary is a consistency test, not a new
special case: these networks are already source--sink connected and hence
covered by the cited capacitated theorem. The decomposition-tree theorem is
the broader statement; it also accepts positive leaves and serial assemblies
outside source--sink connectivity.

## Why no unconditional arbitrary two-sum theorem is claimed

There is a third, mixed regime: some global dicuts restrict nontrivially to
one piece and others to both. Neither construction has the right count there.
The directed diamond split into its two length-two branches is the smallest
warning: local taus are `1,1` but global tau is `2`, so serial color union
produces only one dijoin; parallel separation of the two local path dijoins is
the correct construction. For a general mixed instance, trace states must
record which local dijoins hit which separator classes. The theorem above
does not conceal that unsolved compatibility problem.

## Mandatory filters

1. **Schrijver filter.** The construction is unweighted: `tau_i` and `k` are
   integer arc cardinalities, every arc has capacity one, extra members of a
   packing are discarded in serial mode, and disjoint component packings are
   concatenated in parallel mode. No weighted Edmonds--Giles statement is
   inferred. These unit-capacity color operations are the step that does not
   purport to handle arbitrary weights.
2. **Lucchesi--Younger filter.** No dicut/dijoin min-max theorem is used.
   Every constructed set is shown directly to meet an arbitrary global
   dicut via its nonempty component restriction.
3. **Easy-direction filter.** The proof establishes the existence direction:
   formulas (3) and (5) explicitly construct exactly `tau(D)` pairwise
   arc-disjoint dijoins. It does not merely observe that no larger packing can
   exist.
