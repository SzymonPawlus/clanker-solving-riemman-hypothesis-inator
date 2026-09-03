# Low-degree signatures in an atomic `tau=3` obstruction

**Status:** `sketch`; independent review required.

Definitions use nonempty dicuts: $\delta^+(U)\ne\varnothing$ and
$\delta^-(U)=\varnothing$. A dijoin meets every such dicut.

## Theorem

Let $D$ be a lexicographically minimal counterexample at $\tau(D)=3$: first
minimize vertices, then arcs. Contract SCCs and take a counterexample weak
component, so $D$ is a weakly connected DAG. Assume the independently
reconstructed atomic-sparsity conclusion $m\le3n-4$. Then:

1. every arc satisfies the following **cut-or-gate dichotomy**: it belongs to
   a minimum (three-arc) dicut, or there is a shore $U$ for which it is the
   unique entering arc and $1\le|\delta^+(U)|\le2$;
2. the underlying multigraph is 3-edge-connected;
3. some vertex has total degree $3$, $4$, or $5$ (and none has degree below
   $3$);
4. a source among these has outdegree $3$, $4$, or $5$, a sink has the
   corresponding indegree, and an internal vertex has one of
   $(d^-,d^+)=(1,2),(2,1),(1,3),(2,2),(3,1),(1,4),(2,3),(3,2),(4,1)$.

### Proof

Fix an arc $a$ lying in no minimum dicut.  Some minimum dicut of $D$ avoids
$a$, and its shore remains a three-arc dicut after deletion, so
$\tau(D-a)\le3$.  If $D-a$ had no dicut of size one or two, equality would
hold.  Arc-minimality would then give three disjoint dijoins of $D-a$; every
dicut $C$ of $D$ would leave the nonempty dicut $C\setminus\{a\}$ in $D-a$
(and if $a\in C$, then $|C|\ge4$), so the same three sets would be dijoins of
$D$, a contradiction.

Hence $D-a$ has a dicut shore $U$ with $1\le|\delta^+_{D-a}(U)|\le2$.
This shore was not a dicut in $D$.  The only possible entering arc restored
when passing from $D-a$ to $D$ is $a$, so
$\delta^-_D(U)=\{a\}$.  (If $a$ instead left $U$, then $U$ would already be a
dicut shore of $D$ of size at most three, forcing a minimum dicut containing
$a$; if $a$ did not cross, the small dicut would be unchanged.)  This proves
the dichotomy in 1.

For 2, suppose fewer than three underlying edge copies disconnect the
underlying graph. Remove them and contract every resulting connected
component. The induced quotient orientation is a weakly connected DAG with at
least two vertices. A source quotient vertex has a nonempty directed cut
consisting only of removed edges, hence of size at most two. Its union of
components is a dicut shore of $D$, contradicting $\tau(D)=3$.

Therefore every vertex has total degree at least three. But
$2m\le6n-8<6n$, so some vertex has degree at most five. DAG acyclicity gives
the listed source, sink, and internal orientation signatures. QED.

The deletion lemma is therefore not unconditional arc-criticality.  Every one
of the at most five incident arcs at the forced vertex is instead certified
either by a minimum dicut or by a one- or two-arc almost-dicut behind that
unique entering gate.  The next step is to classify how these two kinds of
certificates can cross; the degree census alone does not yet yield a reduction.

## Filters

- **Schrijver:** unit deletion and the exact cardinalities three/four are the
  unweighted step; zero weights destroy it.
- **Lucchesi--Younger:** unused.
- **Easy direction:** the argument invokes existence from minimality and does
  not infer it from the trivial packing upper bound.

Sanity checks: a directed path exposes a one-arc dicut and fails item 2's
hypothesis; a directed cycle has no dicut; in a two-source DAG only
incoming-closed shores are counted.

## Exact degree-three source/sink reduction

Let $v$ be a source with precisely three outgoing arc copies $a_1,a_2,a_3$.
If $D-v$ has three disjoint dijoins $J_1,J_2,J_3$, then
$J_i\cup\{a_i\}$ are three disjoint dijoins of $D$.

Indeed, a dicut avoiding $v$ cannot contain a head of any $a_i$ and is an
unchanged dicut of $D-v$.  For a dicut shore $U$ containing $v$, put
$W=U\setminus\{v\}$.  If $\delta^+_{D-v}(W)$ is nonempty, it is a dicut of
$D-v$ and every $J_i$ hits it.  If it is empty, the cut of $U$ consists only
of those $a_i$ whose heads lie outside $W$; its size is at least three and
there are only three $a_i$, so it contains all of them.  The sink statement
follows by reversing all arcs and complementing shores.

This is an exact lifting rule, but it does not by itself eliminate the
signature under minimality *within the $\tau=3$ class*.  Deleting $v$ can
leave minimum dicut value at most two, or can raise it above three; only when
$\tau(D-v)=3$ does vertex-minimality supply the required packing.  More
precisely, every one- or two-arc dicut shore $W$ of $D-v$ must contain the
head of at least one $a_i$, since otherwise it is an unchanged small dicut of
$D$.  This is the exact small-shore certificate in the low-$\tau$ branch.

## Exact certificates at a branching `(1,2)` vertex

Let the incident arcs be $a=u\to v$, $b=v\to x$, and $c=v\to y$.  Applying
the cut-or-gate dichotomy separately gives the following exhaustive local
alternatives.

- If $a$ is not in a minimum dicut, there is a shore $W$ containing $v$ but
  not $u$, with $\delta^-(W)=\{a\}$ and
  $1\le|\delta^+(W)|\le2$.  Its outgoing boundary contains whichever of
  $b,c$ have heads outside $W$.
- If $b$ is not in a minimum dicut, there is a shore $W_b$ containing $x$
  but not $v$, with $\delta^-(W_b)=\{b\}$ and one or two outgoing arcs.
  The analogous statement holds for $c$ and $y$.
- If an incident arc has no such gate shore, it lies in a three-arc minimum
  dicut.  A minimum shore containing $b$ or $c$ must contain both $u$ and
  $v$ (otherwise $a$ enters it); a minimum shore containing $a$ contains
  $u$ and excludes $v$.

The dual list covers `(2,1)`.  These alternatives are genuinely exhaustive,
but no contradiction follows merely by uncrossing them: gate shores are not
dicut shores in $D$, so ordinary dicut submodularity cannot be applied to
them as though they were minimum shores.  Any elimination of `(1,2)` must
use this one-entering-arc defect explicitly.
