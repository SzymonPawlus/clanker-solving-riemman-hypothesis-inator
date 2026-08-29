# The case of minimum dicut size two

status: sketch

target-status: verified:review

depends-on:

- `cited`: Robbins's strong-orientation theorem [1].
- `cited`: the weighted-packing formulation and its reduction to
  \(\{0,1\}\)-valued weights [2].
- `cited`: Schrijver's \(\tau=2\) counterexample to the weighted
  Edmonds--Giles conjecture [3].
- Elementary finite-graph facts proved below (so they are not external
  dependencies).

## Claim

Let \(D=(V,A)\) be a finite digraph whose minimum dicut has size
\(\tau(D)=2\).  Then \(A\) can be partitioned into two dijoins.

This is the existence direction of Woodall's conjecture for \(\tau=2\).  The
argument below is a write-up for cross-examination; it remains a `sketch` until
an agent from a different model family reconstructs it under the repository
review protocol.

## Definitions used here

For a nonempty proper set \(U\subsetneq V\), let \(\delta_D^+(U)\) be the arcs
with tail in \(U\) and head outside \(U\), and let \(\delta_D^-(U)\) be the arcs
with tail outside \(U\) and head in \(U\).  A **dicut** is
\(\delta_D^+(U)\) when \(\delta_D^-(U)=\varnothing\): every arc crossing this
vertex cut points out of \(U\).  A **dijoin** is an arc set meeting every such
dicut.  Thus a partition into two dijoins is exactly a red/blue colouring of
all arcs in which every dicut contains both colours.

The **underlying undirected multigraph** \(G\) has vertex set \(V\) and one
undirected edge for each arc of \(D\), retaining parallel copies and forgetting
direction.  Loops cross no cut and may be placed in either part at the end.
An orientation of \(G\) chooses a direction for each individual non-loop edge.

## Sanity checks on the definitions

- On the directed path \(s\to v\to t\), both \(\delta_D^+(\{s\})\) and
  \(\delta_D^+(\{s,v\})\) are one-arc dicuts.  Hence \(\tau=1\), and the
  two-colour conclusion is not expected.
- A directed cycle has no dicut: every nontrivial vertex cut which has an arc
  leaving also has an arc entering.  (Accordingly, the minimum over dicuts is
  not \(2\).)
- In the two-source DAG \(s_1\to t\leftarrow s_2\), each singleton source
  gives a one-arc dicut.  If each displayed arc is replaced by two parallel
  copies, then the minimum dicut size is \(2\), and colouring one copy of each
  pair red and the other blue gives the promised two dijoins.

These checks use the condition \(\delta_D^-(U)=\varnothing\), not merely the
condition that some arc leaves \(U\).

## Two elementary lemmas

**Lemma 1.** Every cut of \(G\) containing an edge contains at least two
edges.  Equivalently, every nontrivial connected component of \(G\) is
bridgeless.  Under the convention that an empty directed cut is a dicut, \(G\)
is connected as well and hence is 2-edge-connected.

**Proof.** Fix \(U\subseteq V\) for which an edge crosses.  If exactly one edge
crosses, its corresponding arc
either points out of \(U\), making \(\delta_D^+(U)\) a one-arc dicut, or points
into \(U\), in which case \(\delta_D^+(V\setminus U)\) is a one-arc dicut.
Both alternatives contradict \(\tau(D)=2\).  Therefore every such cut has at
least two edges.  In particular no connected component containing an edge has
a bridge.  If empty dicuts are admitted, a disconnected \(G\) would also give
an empty dicut by taking a union of components, so \(G\) is then connected.
\(\square\)

**Lemma 2.** If an orientation \(O\) of a finite undirected graph is strongly
connected, then for every nonempty proper \(U\subsetneq V\), at least one
\(O\)-arc leaves \(U\) and at least one \(O\)-arc enters \(U\).

**Proof.** Choose \(u\in U\) and \(v\notin U\).  A directed \(u\)-to-\(v\)
path has a first arc leaving \(U\), and a directed \(v\)-to-\(u\) path has a
first arc entering \(U\). \(\square\)

## Proof of the claim

By Lemma 1 and Robbins's theorem [1], every nontrivial connected component of
\(G\) has a strongly connected orientation.  Choose such an orientation in
each component and call their union \(O\).  (If empty dicuts count, \(G\) is
connected and \(O\) is simply a strongly connected orientation of \(G\).)
Partition the non-loop arcs of \(D\) as follows:

\[
  J_+ := \{a\in A : \text{the direction of }a\text{ agrees with }O\},
  \qquad
  J_- := A\setminus J_+.
\]

Here agreement is tested separately for every parallel edge of \(G\).  Assign
loops arbitrarily; they affect no dicut.  Thus \(J_+\) and \(J_-\) partition
\(A\).

Let \(C=\delta_D^+(U)\) be any nonempty dicut, so
\(\delta_D^-(U)=\varnothing\).  Every underlying edge crossing between \(U\)
and \(V\setminus U\) therefore comes from a \(D\)-arc directed out of \(U\).
Because \(C\ne\varnothing\), some connected component \(H\) meets both \(U\)
and its complement.  Apply Lemma 2 inside \(H\) to \(U\cap V(H)\).  Some
crossing edge is directed out of \(U\) by \(O\); its
corresponding \(D\)-arc agrees with \(O\), and hence lies in \(C\cap J_+\).
Lemma 2 also gives a crossing edge directed into \(U\) by \(O\).  Its
corresponding \(D\)-arc still points out of \(U\), so it disagrees with \(O\)
and lies in \(C\cap J_-\).  Consequently every dicut meets both \(J_+\) and
\(J_-\).  They are two disjoint dijoins whose union is \(A\). \(\square\)

## Mandatory filters

1. **Schrijver filter: passes, at the colouring-to-packing step (not in
   Lemma 1).**  For the weighted Edmonds--Giles problem, integer weights may be
   reduced to \(w\in\{0,1\}^A\): replace an arc of weight \(k>1\) by \(k\)
   parallel weight-one copies, while retaining weight-zero arcs because they
   still determine which cuts are dicuts [2].  After this reduction Lemma 1
   remains valid.  Indeed, a bridge would itself form a dicut in one of its two
   directions, of weight at most one, contradicting minimum weighted dicut
   value two.  In particular, the former explanation involving a single
   weight-two bridge was wrong: that arc becomes two parallel edges.

   Unweightedness is instead used when the agreement/disagreement colouring is
   declared to be a packing.  A weighted packing \(J_+,J_-\) must satisfy
   \(\chi^{J_+}+\chi^{J_-}\leq w\), so neither dijoin may contain a weight-zero
   arc.  The construction colours every arc, and Lemma 2 only guarantees one
   crossing arc of each colour in a dicut; either witness may have weight zero.
   Deleting those arcs is not legitimate, because their directions can prevent
   other cuts from being dicuts.  Thus the argument gives no packing respecting
   \(w\).  This is the necessary failure: Schrijver's counterexample has
   \(w\in\{0,1\}^A\), minimum weighted dicut value two, and no packing of two
   dijoins [3].
2. **Lucchesi--Younger filter: passes.**  The proof never invokes the
   Lucchesi--Younger min-dijoin/max-disjoint-dicuts theorem, nor interchanges
   dicuts and dijoins.  Its only non-elementary input is Robbins's theorem on
   strongly connected orientations of undirected graphs.
3. **Easy-direction filter: passes.**  The constructed sets \(J_+\) and
   \(J_-\) are exhibited and each is proved to meet every dicut.  This proves
   existence of two disjoint dijoins, rather than only the trivial upper bound.

## Kill criterion and outcome

The attack was to be stopped and recorded as `refuted` if either (a) minimum
dicut cardinality two failed to force the underlying multigraph to be
2-edge-connected, or (b) the agreement/disagreement partition arising from a
Robbins orientation failed to put both colours in an arbitrary dicut.  Lemma 1
settles (a), and the two opposite crossing arcs supplied by Lemma 2 settle (b),
so the kill criterion was not met.

## Weakest steps for cross-examination

The proof's load-bearing external step is Robbins's theorem, including its
standard extension to multigraphs with parallel edges.  The most important
internal step to attack is the second half of the arbitrary-dicut argument:
the edge which \(O\) directs *into* \(U\) corresponds to an arc of \(D\) which
points *out* of \(U\) only because \(C\) is a dicut.  This is precisely where
confusing an arbitrary directed cut with a dicut would break the proof.

## Sources

1. H. E. Robbins, “A theorem on graphs, with an application to a problem of
   traffic control,” *American Mathematical Monthly* **46** (1939), 281--283.
   Robbins's theorem states that a finite connected undirected graph has a
   strongly connected orientation if and only if it has no bridge.
2. G. Cornuéjols, S. Liu, and R. Ravi, “Approximately Packing Dijoins via
   Nowhere-Zero Flows,” *Combinatorica* **45** (2025), article 32,
   <https://doi.org/10.1007/s00493-025-00159-x>.  Corollary 2 records the same
   \(\tau=2\) conclusion via Robbins's theorem; Proposition 1 contains the
   agreement/disagreement construction in the more general language of
   cut-balanced orientations.  The introductory discussion of the weighted
   Edmonds--Giles conjecture explicitly says that weight-zero arcs cannot be
   removed because they help determine which cuts are dicuts.  More
   specifically, Lemma 2 and the proof of Theorem 10 work with
   \(w\in\{0,1\}^A\), retain weight-zero arcs in the digraph, and require the
   packed dijoins to respect the weights.  (Theorem 9 itself is instead a
   cited, unproved reformulation of Woodall's conjecture in terms of
   strengthenings.)
3. A. Schrijver, “A counterexample to a conjecture of Edmonds and Giles,”
   *Discrete Mathematics* **32** (1980), 213--214,
   <https://ir.cwi.nl/pub/9906/9906D.pdf>.  The example is for \(k=2\): its
   distinguished arc set meets every dicut at least twice but cannot be split
   into two dijoins (called coverings there).  Equivalently, giving those arcs
   weight one and all other arcs weight zero yields minimum weighted dicut two
   with no packing of two dijoins.

## Cross-examination record

Not yet examined.  On successful independent reconstruction by the other
model family, move this claim to `results/` and replace this section with the
required `examined-by` / `depends-on` / `checked` / `not-checked` block.
