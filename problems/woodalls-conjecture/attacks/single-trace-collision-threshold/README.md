# The sharp single-trace threshold at `tau=3`

**Issue:** #225. **Status:** `sketch`, targeting `verified:review`.

This rules out both Hall-obstruction shapes from PR #224 when a separator has
one optional trace and the local triples realize their elementary trace cut
capacities.  The threshold is sharp: the compatibility graph is a complete
bipartite graph with one rectangular block deleted, and it has a perfect
matching exactly when the two sides supply at least three covering slots in
total.

The result is noncomputational and applies, in particular, to two-vertex
interfaces and to any at-most-five-arc interface whose realizable mixed state
has a single optional trace.

## Definitions and restriction identity

For a finite digraph `D`, a **dicut** is a nonempty outgoing boundary
`delta+(U)` with no arc entering `U`.  A **dijoin** meets every dicut, and
`tau(D)` is the minimum dicut cardinality.

Let `D=D1 union D2`, with disjoint arc sets, common vertex separator `S`, and
no other overlap.  An incoming-closed global shore restricts to
incoming-closed local shores with the same trace `T subseteq S`, and

```text
delta+_D(U) = delta+_D1(U intersection V(D1))
              disjoint-union
              delta+_D2(U intersection V(D2)).                 (1)
```

Conversely, two incoming-closed local shores with equal trace unite to a
global incoming-closed shore and satisfy (1).  This is checked arc by arc,
using that every arc belongs to exactly one piece.

For each piece and trace, let `B_i(T)` be the family of all corresponding
local boundaries, retaining the empty boundary.  A local arc set **covers
T** if it meets every nonempty boundary in `B_i(T)`.  A trace is **relevant**
when both local families are nonempty and some pair of their boundaries has
nonempty union.  A relevant trace is **optional** when neither `B_1(T)` nor `B_2(T)`
contains the empty boundary.  If piece 2 admits an empty boundary at `T` and
piece 1 has a nonempty boundary, then `T` is **forced onto piece 1**, because
pairing those realizations gives a global dicut which only piece 1 can hit.
Define the symmetric forced condition likewise.  A trace for which one local
family is empty is unrealizable globally and imposes no condition.

The usual checks fix the convention: a directed path has singleton prefix
dicuts, a directed cycle has no dicut, and
`s1->t1, s2->t1, s2->t2` has singleton-source dicuts even though it is not
source--sink connected.  A boundary with arcs in both directions is never
called a dicut.

## One optional trace

Fix three pairwise arc-disjoint slots `X_i^1,X_i^2,X_i^3` in each piece;
empty slots are allowed.  Assume every slot covers every trace forced onto
its piece.  Suppose there is exactly one optional trace, denoted `T`.

Let

```text
g_i = number of piece-i slots which cover T,
b_i = 3-g_i.
```

For any pair of slots, all forced traces are already handled.  By (1), their
union fails to be a global dijoin exactly when both slots fail `T`: missed
nonempty boundaries on the two sides unite to a missed global dicut.
Therefore the compatibility graph is exactly

```text
Gamma = K_3,3 minus K_(b_1,b_2),                         (2)
```

where the deleted rectangle joins the noncovering slots on the two sides.

## Sharp matching theorem

**Theorem 1.**  Under the hypotheses above, the six slots can be paired into
three global pairwise arc-disjoint dijoins if and only if

```text
g_1 + g_2 >= 3.                                         (3)
```

**Proof.**  In any compatible pairing, a noncovering piece-1 slot must be
paired with a covering piece-2 slot.  Hence `b_1<=g_2`; equivalently,
`g_1+g_2>=3`.  This proves necessity.

Conversely, (3) gives `b_1<=g_2` and symmetrically `b_2<=g_1`.  Match every
noncovering piece-1 slot injectively to a covering piece-2 slot.  Match every
still-unmatched noncovering piece-2 slot to an unused covering piece-1 slot;
the symmetric inequality supplies enough.  Pair any remaining covering
slots arbitrarily.  No pair has two noncovering endpoints, so every pair is
an edge of (2).  The restriction identity proves each union is a global
dijoin, and local plus inter-piece disjointness makes the three unions
arc-disjoint.  QED

Equivalently, the deleted rectangle in (2) causes an isolated vertex or a
`2 x 2` collision Hall obstruction exactly when `b_1+b_2>3`.  Thus the two
obstruction families collapse to one sharp integer threshold in the
single-optional-trace regime.

## How `tau=3` removes the rectangle

Because `T` is optional, every member of `B_i(T)` is nonempty.  Let

```text
mu_i(T) = min{|B| : B in B_i(T)}.
```

Choosing minimum local shores on both sides and applying (1) gives a global
dicut of size `mu_1(T)+mu_2(T)`.  Consequently, if `tau(D)=3`,

```text
mu_1(T) + mu_2(T) >= 3.                                 (4)
```

This is the point where the minimum-dicut hypothesis constrains the Hall
rectangle.  It does not by itself turn local cut size into disjoint local
trace covers; assuming that would simply reproduce the unresolved packing
problem.  The exact corrected local hypothesis is the following.

Call a local slot triple **T-adequate** when it has no forced-bad slot and

```text
g_i >= min(3,mu_i(T)).                                  (5)
```

**Corollary 2.**  If `tau(D)=3`, there is one optional trace, and both local
slot triples are `T`-adequate, then `D` has three pairwise arc-disjoint
dijoins.

**Proof.**  From (4),

```text
min(3,mu_1(T)) + min(3,mu_2(T)) >= 3.
```

Condition (5) therefore gives `g_1+g_2>=3`.  Theorem 1 supplies the three
dijoins.  QED

This is materially weaker than demanding three full local dijoins in both
pieces.  For example, local covering counts `(g_1,g_2)=(1,2)` or `(0,3)` are
enough.  It also handles forced traces simultaneously: every slot handles
those traces, while the scarce covering capacity is split only for the one
optional trace.

## Realizability and sharpness

The threshold is realized by elementary directed networks, so the deleted
rectangle is not an artifact of abstract profiles.  Take separator
`S={s,t}`.  In piece `i`, put `m_i` parallel arcs from `s` to `t`, use each as
one covering slot, and pad to three slots with empty sets.  For trace `{s}`,
the only local boundary is the set of all `m_i` arcs, so every singleton arc
covers the trace and every empty slot fails it.  The compatibility graph is
exactly

```text
K_3,3 minus K_(3-m_1,3-m_2).
```

The union has `m_1+m_2` parallel `s->t` arcs and minimum dicut size
`m_1+m_2`.  If `m_1+m_2=3`, the threshold is attained and the three arcs are
the three global dijoins.  If `m_1+m_2<=2`, the Hall obstruction is real, but
the union has `tau<=2`; it cannot be used as a `tau=3` obstruction.  This
shows sharply how the minimum-cut constraint eliminates the naive
single-trace rectangle once the local triples expose all `mu_i` units of
trace-covering capacity.

## Why colour matching alone is still insufficient

Permuting colour names changes neither `g_i` nor the deleted rectangle sizes
in (2).  Hence it cannot change condition (3).  At a one-way three-arc cut,
making the boundary rainbow is necessary, but contraction can create a
phantom local crossing whose endpoints lie on the same side of a global
shore.  A boundary arc can then be the sole local witness of its colour.
The `T`-adequacy requirement asks for actual trace covers and is the corrected
hypothesis; boundary-colour agreement alone is not substituted for it.

## Mandatory filters

1. **Schrijver filter: passed.**  The conclusion uses three supplied triples
   of disjoint unit-capacity arc sets, and `mu_i` is unweighted cardinality.
   Weighted minimum dicut value three does not imply (5): zero-weight arcs
   still determine incoming-closed shores but cannot be used by a packed
   dijoin.  No weighted tau-to-cover-packing implication is asserted.
2. **Lucchesi--Younger filter: passed.**  No dicut/dijoin role reversal is
   used.  Pair compatibility is verified directly against arbitrary global
   dicuts through (1); the only matching is the elementary slot pairing.
3. **Easy-direction filter: passed.**  Theorem 1 explicitly pairs slots and
   constructs three disjoint global dijoins.  Inequality (4) is only a lower
   bound on a particular global dicut family and is not presented as the
   existence argument.

## Scope and next bottleneck

The result completely settles realizable Hall rectangles when there is one
optional trace and proves a broad sufficient condition at `tau=3`.  It does
not prove that arbitrary local pieces admit `T`-adequate triples.  Failure of
adequacy is now the only obstruction in this regime: a piece of local trace
cut value `mu` fails to provide `min(3,mu)` disjoint trace-covering sets.
That is a smaller, one-trace packing problem and the precise target for an
uncrossing, path, or matroid argument.

The highest-risk points for review are the necessity direction of (3), the
use of optionality in deriving (4), and the distinction between the exact
local adequacy hypothesis and the invalid inference of adequacy from cut
size alone.
