# Low-degree signatures in an atomic `tau=3` obstruction

**Status:** `sketch`; independent review required.

Definitions use nonempty dicuts: $\delta^+(U)\ne\varnothing$ and
$\delta^-(U)=\varnothing$. A dijoin meets every such dicut.

## Theorem

Let $D$ be a lexicographically minimal counterexample at $\tau(D)=3$: first
minimize vertices, then arcs. Contract SCCs and take a counterexample weak
component, so $D$ is a weakly connected DAG. Then:

1. every arc satisfies the following **cut-or-gate dichotomy**: it belongs to
   a minimum (three-arc) dicut, or there is a shore $U$ for which it is the
   unique entering arc and $1\le|\delta^+(U)|\le2$.

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

This proves the stated dichotomy. QED.

An earlier draft continued by claiming that $\tau(D)=3$ makes the underlying
multigraph 3-edge-connected. That is false: contracting the components of an
undirected cut in a DAG can create a directed 2-cycle in the quotient. For
example, take two disjoint all-left-to-right orientations of $K_{3,3}$ and
add one arc from a left vertex of each block to a right vertex of the other.
The result is still a DAG with $\tau=3$, but the underlying cut between the
blocks has size two. Consequently no degree-deficit or exact-two-exit-gate
claim is built on that discarded step.

## Filters

- **Schrijver:** unit deletion and the exact cardinalities three/four are the
  unweighted step; zero weights destroy it.
- **Lucchesi--Younger:** unused.
- **Easy direction:** the argument invokes existence from minimality and does
  not infer it from the trivial packing upper bound.

Sanity checks: a directed path exposes a one-arc dicut and cannot have
$\tau=3$; a directed cycle has no dicut; in a two-source DAG only
incoming-closed shores are counted.

## Exact degree-three source/sink reduction

### Directed minimum-cut composition

The following reduction works for every positive integer $k$.

**Composition theorem.** Let $C=\delta_D^+(U)$ have size $k$, put
$W=V(D)\setminus U$, and retain parallel arc copies under contraction. Let
$L=D/W$ and $R=D/U$, deleting the contraction loops (which lie in no
dicut). Here the class is finite loopless directed multigraphs, so parallel
copies remain distinct. If both $L$ and $R$ have $k$ pairwise disjoint
dijoins, then so does $D$.

Every quotient dicut lifts cardinality-preservingly to $D$. When
$\tau(D)=|C|=k$, the two contractions therefore also have dicut number $k$,
since $C$ survives in each. Each $k$-packing hits the $k$ individual copies
of $C$ bijectively. Relabel the two packings so colour $i$ contains the same
arc $c_i$ on both sides, and combine their internal colour-$i$ arcs with
$c_i$.

To check the combined colour, take a dicut shore $X$ of $D$ and write
$A=X\cap U$, $B=X\cap W$. If $A\ne\varnothing$ and $B\ne W$, then $A$ is a
quotient dicut shore in $L$, while $\{u\}\cup B$ is one in $R$. If either
colour-$i$ witness is internal, that arc leaves $X$. Otherwise the left
colour-$i$ witness is its unique matched $c_i$, saying that the tail of
$c_i$ lies in $A$, and the right witness is that same $c_i$, saying that its
head lies outside $B$; hence $c_i$ leaves $X$. These quotient shores have
nonempty boundaries: they are nonempty proper ideals in weakly connected
quotients.

If $A=\varnothing$, incoming-closedness forces $B$ to contain no head of
$C$, and the shore $B$ excluding the contracted source in $R$ has boundary
exactly $\delta_D^+(X)$. If $B=W$, it forces no tail of $C$ to lie in
$U\setminus A$, and the shore $A$ together with the contracted sink in $L$
has boundary exactly $\delta_D^+(X)$. Weak connectivity makes these
boundaries nonempty; the empty and full choices of $X$ are excluded. Thus
the combined sets are disjoint dijoins.

**Atomic consequence.** In a vertex-minimal counterexample with
$\tau(D)=3$, a minimum dicut cannot have both shores of size at least two:
the two strictly smaller contractions would pack by minimality and the
composition theorem would glue them. Hence every minimum dicut isolates a
singleton source of outdegree three or a singleton sink of indegree three.
In particular a degree-three source or sink exists, without using the
conditional bound $m\le3n-4$.

This argument is unweighted: the bijection uses three literal arc copies.
It retains parallel copies and makes no corresponding claim for a weighted
cut merely having value three.

### Deleting the forced endpoint

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

In fact put $R=D-v$. This residual is weakly connected. Every one of its
weak components must receive a source arc, or $D$ was already weakly
disconnected; if there were more than one component, adjoining $v$ to the
complement of a component receiving at most two source arcs would expose a
nonempty $D$-dicut of size at most two.

If $R$ has one vertex, $D$ has a unique source and sink and is covered by
the cited theorem. Assume below that $R$ has a nonempty dicut.

For any nonempty proper dicut shore $X$ of $R$, let
$f=|\delta_R^+(X)|$ and let $k$ count with multiplicity the arcs $a_i$ whose
heads lie in $X$. The $D$-dicut of $\{v\}\cup X$ has $f+3-k$ copies, so
$f\ge k$. If $k=0$, then $X$ itself is also a $D$-dicut, so $f\ge3$.
Thus $k=0,1,2,3$ give the respective lower bounds $3,1,2,3$ on $f$.
If $\tau(R)=3$, vertex-minimality within the $\tau=3$
class and the lifting rule contradict that $D$ is a counterexample. This
leaves
$$
\tau(D-v)\in\{1,2\}\qquad\text{or}\qquad\tau(D-v)\ge4.
$$
If the three arcs have one common head, every shore has $k\in\{0,3\}$ and
hence $f\ge3$; after excluding equality, this signature belongs entirely to
the unresolved $\tau(R)\ge4$ branch. It is **not** eliminated by the present
minimality hypothesis.

The unconditional cited Cornuéjols--Liu--Ravi bound supplies
$\lfloor\tau(R)/6\rfloor$ disjoint dijoins. Therefore $\tau(R)\ge18$ would
give three, which lift through $v$. An actual counterexample can retain only
$$
4\le\tau(R)\le17
$$
in the high branch. No stronger bound is inferred from underlying
edge-connectivity.

The high branch has a rigid directed normal form. No arc of $R$ can belong
to a minimum dicut of $D$: by composition that dicut isolates a degree-three
source or sink, and because the chosen arc lies in $R$ the same endpoint
gives a nonempty $R$-dicut of size at most three. Hence every arc of $R$
takes the gate side of the cut-or-gate dichotomy. For each $a\in A(R)$ there
is a nonempty proper $X\subset V(R)$ with
$$
\delta_R^-(X)=\{a\},\qquad |\delta_R^+(X)|\le2;
$$
the outgoing boundary is allowed to be empty.
If the gate shore supplied in $D$ contains $v$, take $X$ to be that shore
with $v$ removed. The head and tail of $a$ keep $X$ nonempty and proper;
the unique residual entrance remains $a$, and deleting $v$ can only reduce
the outgoing boundary.

Consequently $R$ has no parallel arc copies and is transitively reduced. Two
parallel copies could not separately be the unique entrance of any shore. If
an arc $a=x\to y$ had an alternate directed $x$--$y$ path, every shore
containing $y$ and excluding $x$ would receive both $a$ and the first path
arc entering the shore, again contradicting uniqueness. Thus the finite
high branch is a simple Hasse diagram with
$4\le\tau(R)\le17$, and every cover arc owns a shore with one entrance and
at most two exits.

A counterexample is not source--sink connected, by the cited theorem. A
weakly connected DAG with a unique source has that source reaching every
vertex, and dually every vertex reaches a unique sink; hence $D$ has at least
two sources and two sinks. Besides the deleted source, $R$ therefore has a
source which is not a head of any deleted source arc, and it has at least two
sinks. Each such residual source or sink has degree at least $\tau(R)\ge4$,
with distinct neighbours because $R$ is simple. Thus a genuine high residual
is a multi-source, multi-sink, all-gated poset cover graph, not the easy
one-source/one-sink spindle family.

If $\tau(R)=1$, a minimum shore has $f=k=1$. Then
$\{v\}\cup X$ is a three-arc dicut of $D$, so the composition consequence
forces $R\setminus X=\{t\}$. This is an adjacent degree-three sink receiving
two parallel arcs from $v$ and the one arc of $\delta_R^+(X)$; the third
source arc has its head in $X$. Thus this branch necessarily has source-head
multiplicity $2+1$.

Write the parallel arcs as $e_1,e_2:v\to t$, the third as $a:v\to q$, the
residual in-arc as $b:u\to t$, and put $H=D-\{v,t\}$. Then $H$ is weakly
connected: every component must contain $q$ or $u$, and if those lay in
different components then $\{v\}$ together with the $q$-component would have
only $e_1,e_2$ leaving. If it is a single vertex, $D$ has a unique source and sink and the
cited source--sink-connected theorem applies directly. Otherwise
$\tau(H)\ge2$. If $q\ne u$, the four membership patterns of $(q,u)$ give
lower bounds $3,2,2,3$, in the order $(0,0),(0,1),(1,0),(1,1)$, on
$|\delta_H^+(Y)|$. The only pattern whose raw cut inequalities permit one
arc is $q\in Y,u\notin Y$; but then
$\{v\}\cup Y$ is a three-arc $D$-dicut with at least two vertices on both
shores, contradicting the composition consequence. If $q=u$, only the
diagonal patterns occur and both have lower bound three. The recorded
partition into a dijoin and a $(\tau(H)-1)$-dijoin therefore supplies two
disjoint $H$-dijoins. Adjoining $e_1,e_2$ one to each gives two $D$-dijoins.
This is a sufficient starting pair, but may consume arcs needed by the third
colour; the exact augmentation must choose the first two transversals and the
residual one simultaneously.

The two minimum dicuts $\delta_D^+(\{v\})=\{e_1,e_2,a\}$ and
$\delta_D^+(V\setminus\{t\})=\{e_1,e_2,b\}$ force the normalization: after
relabeling, $e_1,e_2$ have colours one and two, while both $a,b$ have colour
three. Precisely, for $H$-ideal shores define
$$
\mathcal A=\{\delta_H^+(Y):q\notin Y\ \text{or}\ u\in Y\},\qquad
\mathcal B=\{\delta_H^+(Y):q\in Y\ \text{or}\ u\notin Y\}.
$$
With $e_1,e_2$ assigned colours one and two and $a,b$ assigned colour three,
a packing of $D$ is equivalent to two disjoint $\mathcal A$-transversals and
a disjoint $\mathcal B$-transversal in $H$. For signatures
$(q,u)=00,01,10,11$, respectively, the requirements are
$$
\begin{array}{c|cccc}
 &00&01&10&11\\ \hline
\text{colours }1,2&\checkmark&\checkmark&&\checkmark\\
\text{colour }3&\checkmark&&\checkmark&\checkmark
\end{array}
$$
and the boundary lower bounds are $3,2,2,3$. Thus the overlap of the two
clutters is exactly the two diagonal signatures, where capacity three is
available.

If every vertex of $H$ is reachable from $q$ and can reach $u$, then any
directed $q$--$u$ path meets every $\mathcal B$-cut. Moreover such a path
meets **no** $\mathcal A$-boundary: it cannot visit a headless ideal, cannot
leave an all-head ideal and later return to $u$, and the $u$-only signature
is impossible when $q$ reaches $u$. Remove the path arcs from any two
disjoint $H$-dijoins; they remain $\mathcal A$-transversals, while the path
is a disjoint $\mathcal B$-transversal. This closes the cited
source--sink-connected subcase. For a general $q$--$u$ path the remaining
obstruction consists exactly of headless and proper all-head ideals, which
the path misses.

A broader sufficient condition is available. Assume every source of $H$
reaches at least one of $q,u$, that $q$ reaches $u$, and that every sink of
$H$ is reachable from at least one of $q,u$. Choose one witnessing path for
each condition and let $P$ be their arc union. Then $P$ is a
$\mathcal B$-transversal: a nonempty $00$ ideal contains a global source and
its chosen path must leave; the chosen $q$--$u$ path leaves every $10$ ideal;
and the complement of a proper $11$ ideal contains a global sink, so its
chosen path must leave. If $P$ can be chosen so that $H-P$ is weakly
connected with minimum dicut size at least two, the known two-packing result
gives two disjoint dijoins of $H-P$. They are $\mathcal A$-transversals in
$H$, disjoint from $P$, and close the branch. The open point is the existence
of such a thin path union; reachability alone does not control the new cuts
created by deleting $P$.

This branch is already solved by the cited theorem whenever $D$ is
source--sink connected. In particular that holds if $q$ is the unique source
of $H$ or if $u$ is the unique sink of $H$.

In the $\tau(R)=2$ branch, a minimum $R$-dicut $X$ necessarily has $k=1$ or
$2$. If $k=2$, then
$\{v\}\cup X$ is a three-arc dicut of $D$ with nonsingleton shore. The
composition consequence forces its complement to be a singleton $\{t\}$.
Thus $t$ is a degree-three sink adjacent to $v$: the unused source arc is
$v\to t$ and the other two arcs entering $t$ are exactly
$\delta_R^+(X)$. Consequently either every residual two-cut contains exactly
one source-arc head, or $D$ has this adjacent degree-three source--sink
configuration.

### The irreducible `2+1` residual

In the branch $\tau(R)=2$, suppose two arcs go from $v$ to $p$, one goes to
$q$, and the adjacent-sink alternative does not occur. Every two-arc dicut
shore of $R$ is then
$q$-only: it contains $q$, excludes $p$, and in $D$ is an exact
$1$-in/$2$-out gate with common entrance $v\to q$. These shores form a
sublattice and therefore have canonical minimal and maximal members.

The remaining colouring problem is exactly a two-clutter augmentation. Let
$\mathcal A$ contain boundaries of the headless, $p$-only, and all-head
ideals of $R$, and let $\mathcal B$ contain boundaries of the headless,
$q$-only, and all-head ideals. A lift exists exactly when there are two
disjoint $\mathcal A$-transversals $T_1,T_2$ such that
$$
B\nsubseteq T_1\cup T_2\qquad(B\in\mathcal B),
$$
because the residual arcs then form a $\mathcal B$-transversal. Equivalently,
failure is
$$
b_2(\mathcal A)\subseteq\operatorname{up}(\mathcal B),
$$
where $b_2(\mathcal A)$ consists of the inclusion-minimal unions of two
disjoint minimal $\mathcal A$-transversals.

There is strong local structure, but not yet a global augmentation theorem.
Shrink $T_1,T_2$ first to inclusion-minimal $\mathcal A$-transversals. If a
two-edge $q$-gate $Q$ is then saturated by $x\in T_1$ and $y\in T_2$, each
of $x,y$ has a private $\mathcal A$-cut for its own transversal. Uncrossing
a private cut $X$ with $Q$ proves (here $p\ne q$):

- a headless private 3-cut is a singleton degree-three source;
- an all-head private 3-cut has singleton degree-three sink complement;
- a $p$-only private cut has size at least four;
- at equality four, $Q\cap X=\{r\}$ and
  $Q\cup X=R\setminus\{t\}$ for a degree-three source $r$ and sink $t$, and
  the protected gate arc is $r\to t$.

For an essential colour-$i$ arc $x$, its private shores form a lattice. If
$P_x^-$ and $P_x^+$ are their intersection and union, respectively, an arc
can replace $x$ in one step exactly when it lies in
$$
\delta^+(P_x^-,V(R)\setminus P_x^+).
$$
A residual corridor arc gives a valid one-step exchange of the relevant
$\mathcal A$-transversal. It need not be a global augmentation: occupying it
may saturate another $\mathcal B$-cut. The resulting search is an alternating
**AND--OR** system, not an ordinary augmenting path, because repairing one
arc can require a transversal of all its private cuts. A closed alternating
cycle alone proves neither augmentation nor impossibility. One still needs a
potential or a closed-kernel exclusion showing that these exchanges improve
the global family of saturated $\mathcal B$-cuts.

## Exact certificates at a branching `(1,2)` vertex

Let the incident arcs be $a=u\to v$, $b=v\to x$, and $c=v\to y$.  Applying
the cut-or-gate dichotomy separately gives the following exhaustive local
alternatives.

- For the incoming arc $a$, the singleton shore $W=\{v\}$ itself has
  $\delta^-(W)=\{a\}$ and $\delta^+(W)=\{b,c\}$, independently of whether
  $a$ lies in a minimum dicut.
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
