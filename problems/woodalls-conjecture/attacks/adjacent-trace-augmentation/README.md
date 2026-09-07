# Joint profile packing for two adjacent traces

**Issue:** #252. **Status:** `sketch`, targeting `verified:review`.

This proves the missing shared-incidence theorem for two adjacent optional
traces.  A maximum flow covering both traces can be preserved while the
differing separator vertex is exposed as one extra source or one extra sink.
Ordinary integral augmentation then extends it to a maximum flow for the
larger individual trace rank.  The resulting path decomposition jointly
realizes the optimal three-slot profile

```text
both = min(a_0,a_1),   neither = 3-max(a_0,a_1),
trace t support = a_t,
```

where `a_t=min(3,mu_t)`.  Applying this in both pieces and using the two
global `tau=3` cut inequalities gives a perfect compatibility matching.

Consequently, every two-piece separator sum with exactly two **adjacent**
optional traces, no forced trace, and `tau=3` has three arc-disjoint dijoins.
No common boundary core is required.  This closes the coreless path and
diamond examples left open by PR #249 within the adjacent-trace regime.

## Directed setup

For a finite digraph `D=(V,A)`, a **dicut** is a nonempty outgoing boundary
`delta+(X)` with `delta-(X)=empty`.  A **dijoin** meets every dicut.

Fix a separator `S` and adjacent traces

```text
R_0 = L,             R_1 = L union {z},                 (1)
```

where `L` and `O=S-R_1` are nonempty.  For `t=0,1`, let
`B_t` be the boundaries of incoming-closed shores with trace `R_t`, assume
this family is nonempty and contains no empty boundary, and put

```text
mu_t = min{|B|: B in B_t}.                              (2)
```

A local arc set **covers trace `t`** if it meets every member of `B_t`.

The no-entering condition is used throughout.  A directed path has prefix
dicuts, while a directed cycle has none.  Nothing below treats every
nonempty outgoing boundary as a dicut.

## One guarded network, three terminal choices

Let `M=|A|+1`.  Replace every original arc `u->v` by a capacity-one forward
copy and add a capacity-`M` reverse guard `v->u`.  Add terminals `alpha,beta`.
The following three networks differ only in their high-capacity terminal
arcs:

```text
N_*: alpha->x (x in L),       y->beta (y in O);
N_0: the arcs of N_*,         z->beta;
N_1: the arcs of N_*,         alpha->z.                 (3)
```

Every listed terminal arc has capacity `M`.  A cut of capacity below `M`
crosses no guard or terminal arc.  Its original-vertex source side is
incoming-closed.  In `N_0` it contains `L` and excludes `z union O`, so its
trace is `R_0`; in `N_1` it contains `L union {z}` and excludes `O`, so its
trace is `R_1`; and in `N_*` the vertex `z` is free, so its trace is either
`R_0` or `R_1`.  Conversely each corresponding shore gives exactly such a
cut, whose capacity is its boundary size.

Because a finite cut exists and has capacity at most `|A|`, max-flow/min-cut
therefore gives

```text
maxflow(N_0)=mu_0,
maxflow(N_1)=mu_1,
maxflow(N_*)=lambda=min(mu_0,mu_1).                      (4)
```

All capacities are integral.  Delete flow cycles and decompose a flow into
unit `alpha-beta` paths.  Retain from each path only the original arcs whose
unit forward copies it uses.  These retained sets are pairwise arc-disjoint.

In `N_0`, every path begins through a pin in `L`.  A path ending through
`z->beta` covers trace 0; a path ending through a vertex of `O` covers both
traces.  Indeed it crosses every finite cut of the indicated network on a
unit forward copy.  Symmetrically, in `N_1`, a path beginning through
`alpha->z` covers trace 1, while a path beginning through `L` covers both.

## Terminal-preserving augmentation

**Lemma 1.**  The two trace families admit pairwise arc-disjoint slots whose
profile counts simultaneously attain

```text
trace-0 support = mu_0,
trace-1 support = mu_1,
both support     = min(mu_0,mu_1).                       (5)
```

where counts above three may later be discarded.

**Proof.**  Begin with an integral maximum flow `f_*` of value `lambda` in
`N_*`.

Suppose first that `mu_0<=mu_1`.  Regard `f_*` as a feasible flow in `N_1`
and augment it to a maximum flow of value `mu_1`.  Augmenting paths can be
chosen simple and hence never revisit `alpha`; in particular they never use
a reverse residual arc entering `alpha`.  Therefore augmentation does not
decrease the existing total flow on the terminal arcs `alpha->x`, `x in L`.
The final flow has at least `lambda=mu_0` units beginning through `L`.

In its unit path decomposition, retain `mu_0` paths beginning through `L`.
Their original-arc sets cover both traces.  Every remaining path begins
through either `L` or `z`, so it covers trace 1.  Thus all `mu_1` paths cover
trace 1, while at least `mu_0` cover both and hence trace 0.  There cannot be
an additional trace-0-cover slot: pairwise disjoint trace-0 covers must use
distinct arcs of a minimum boundary of size `mu_0`.  Hence exactly `mu_0`
slots cover trace 0, and they are exactly the both-cover slots.

If `mu_1<=mu_0`, instead regard `f_*` as a feasible flow in `N_0` and
augment it to value `mu_0`.  Simple augmenting paths never revisit `beta`,
so they never use reverse residual arcs leaving `beta`; the old total flow
on `y->beta`, `y in O`, cannot decrease.  At least
`lambda=mu_1` final unit paths still end through `O` and cover both traces.
All `mu_0` paths cover trace 0.  A minimum trace-1 boundary similarly forbids
more than `mu_1` disjoint trace-1 covers, so exactly those `mu_1` slots cover
trace 1 and both traces; every additional slot is trace-0-only.  This again
gives (5).  Unit forward capacities make all retained original-arc sets
disjoint.  QED

The preservation statement concerns terminal-arc flow, not the identities
of the original paths.  Internal residual rerouting is harmless: after the
final augmentation, a fresh integral path decomposition has the asserted
number of paths of each terminal type.

## Exact capped three-slot profile

Set

```text
a_t=min(3,mu_t).
```

**Corollary 2.**  Three pairwise arc-disjoint slots, allowing empty padding,
can be chosen so that

```text
trace-t support = a_t,
both support    = min(a_0,a_1),
neither support = 3-max(a_0,a_1).                       (6)
```

**Proof.**  If `a_0<=a_1`, use Lemma 1 to choose `a_0` both-cover slots and
`a_1-a_0` trace-1-only slots, then add `3-a_1` empty slots.  The minimum
boundary count in Lemma 1 rules out accidental trace-0 coverage by an
additional slot.  The case `a_1<=a_0` is symmetric.  QED

## Closing the adjacent two-trace separator regime at `tau=3`

Let `D=D_1 union D_2`, where the pieces have disjoint arc sets and common
vertex separator `S`.  Assume the only relevant global traces are the two
adjacent traces (1), both optional in both pieces, and there are no relevant
forced traces.  Incoming-closed local shores with the same trace unite to a
global incoming-closed shore, and their boundaries unite disjointly;
conversely every global dicut restricts this way.

Write `mu_it` and `a_it=min(3,mu_it)` for piece `i` and trace `t`.

**Theorem 3.**  If `tau(D)=3`, then `D` has three pairwise arc-disjoint
dijoins.

**Proof.**  Minimum same-trace local shores unite to a global dicut.  Hence

```text
mu_1t+mu_2t >= 3,
a_1t+a_2t >= 3,                 t=0,1.                  (7)
```

Apply Corollary 2 in both pieces.  Classify a slot as both, trace-0-only,
trace-1-only, or neither, and denote the both and neither counts by `b_i,e_i`.
Equation (6) gives

```text
b_i >= min(a_i0,a_i1),
e_i <= 3-max(a_i0,a_i1).                                (8)
```

Using (7),

```text
min(a_20,a_21)
 >= min(3-a_10,3-a_11)
  = 3-max(a_10,a_11),
```

so `e_1<=b_2`; symmetrically `e_2<=b_1`.  Equation (7) also says that at
least three slots across the two pieces cover trace 0, and at least three
cover trace 1.

Form the bipartite compatibility graph on the two local triples, joining two
slots exactly when their profiles together cover both traces.  Hall's
condition follows from the four inequalities just proved.  For completeness,
a deficient left set containing a both-slot is impossible, since such a slot
sees every right slot.  Among the remaining types, the only maximal tests are:

- neither alone, ruled out by `e_1<=b_2`;
- neither plus trace-0-only, equivalent to total trace-1 support at least 3;
- neither plus trace-1-only, equivalent to total trace-0 support at least 3;
- all non-both slots, ruled out by `e_2<=b_1`.

Thus there is a perfect matching.  For each matched pair, unite its two arc
sets.  It covers both relevant traces and therefore meets every global
dicut.  Distinct pairs are arc-disjoint because the local slots and the two
piece arc sets are disjoint.  These three unions are the required dijoins.
QED

The theorem constructs the existence direction.  The assumption `tau=3`
enters through (7), not merely through the trivial upper bound on the number
of disjoint dijoins.

## Scope and residual case

The result includes arbitrarily coreless local families.  On a pinned
directed path, the interval flow is the whole path; on the directed diamond
from PR #251, its two disjoint path covers persist during augmentation.
Neither common boundary arcs nor laminar boundary sets are needed.

Adjacency is essential to this proof.  When two traces differ in one
separator coordinate, their Boolean interval contains exactly those traces,
so the single free terminal `z` converts one auxiliary network into the two
fixed-trace networks.  For nonadjacent comparable traces, freeing all
coordinates adds intermediate traces whose smaller boundaries may reduce
the interval flow.  The residual shared-incidence problem is therefore:

```text
two nonadjacent traces with deficient intermediate hull traces.
```

This is narrower than general corelessness and identifies where a genuinely
multiterminal submodular-flow theorem, rather than ordinary augmentation, is
still required.

## Mandatory filters

1. **Schrijver filter: passed.**  Unit forward capacities encode distinct
   usable arcs, and integrality produces actual arc-disjoint slots.  The
   argument depends on unweighted unit resources when converting flow units
   to separate dijoins; it does not derive the false weighted conjecture.
2. **Lucchesi--Younger filter: passed.**  No dicut/dijoin duality is assumed.
   Each retained path is checked directly against the relevant guarded cuts,
   and the final matched unions are directly shown to meet every dicut.
3. **Easy-direction filter: passed.**  Max-flow constructs the local slots,
   Hall constructs their pairing, and the proof explicitly produces three
   disjoint global dijoins.

## Dependency, status, and review targets

The only external input is integral max-flow/min-cut and the augmenting-path
algorithm: L. R. Ford Jr. and D. R. Fulkerson, “Maximal Flow Through a
Network,” *Canadian Journal of Mathematics* **8** (1956), 399--404,
<https://doi.org/10.4153/CJM-1956-045-5>.

Everything else, including the guarded cut correspondence, terminal-flow
preservation, profile inequalities, and Hall reduction, is proved here so
the result does not assume an unreviewed earlier sketch.  It remains `sketch`
until independent review.  The highest-risk point is whether residual
augmentation can always be chosen without entering `alpha` or leaving
`beta`; simple source-to-sink augmenting paths have precisely this property.
