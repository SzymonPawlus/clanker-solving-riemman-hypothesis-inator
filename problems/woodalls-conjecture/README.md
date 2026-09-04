# Woodall's conjecture

**Status:** open since 1976. Notably, the natural weighted generalisation is **false**, which
constrains what any proof can look like.

Shared conventions: [`../README.md`](../README.md). Repo-wide protocol:
[`../../RULES.md`](../../RULES.md). **Problem-specific rules: [`RULES.md`](./RULES.md) — read
before working on this problem.**

## Definitions

Let $D = (V, A)$ be a digraph. For nonempty proper $U \subsetneq V$ write $\delta^+(U)$ for the
arcs leaving $U$ and $\delta^-(U)$ for those entering.

- A **dicut** is a **nonempty** set $\delta^+(U)$ where $\delta^-(U) = \emptyset$ — a cut with
  all arcs pointing the same way. Nonemptiness is part of the definition; it was added on
  2026-09-02 and it changes what earlier work in this directory says, so read *Convention:
  dicuts are nonempty* below before relying on any statement about disconnected digraphs.
- A **dijoin** is a set of arcs meeting *every* dicut at least once.
- A **$k$-dijoin** meets every dicut at least $k$ times.
- $\tau$ denotes the minimum size of a dicut.

### Convention: dicuts are nonempty

**Amended 2026-09-02, issue #158, acting on finding F1 of the independent Lean audit on issue
#151 (branch `claude/151-lean-audit`, `attacks/lean-foundations-audit/`, not yet on `main` when
this was written).** Until then
this file required only $\delta^-(U) = \emptyset$, which admits $\delta^+(U) = \emptyset$ as a
dicut. That permissive reading and this one differ on **exactly** the digraphs whose underlying
graph is disconnected, and never on a weakly connected one: if $D$ is weakly connected and $U$
is nonempty proper, some edge of the underlying graph crosses, and $\delta^-(U) = \emptyset$
forces its arc to leave $U$; conversely, in a disconnected $D$ a union of components has
$\delta^+(U) = \delta^-(U) = \emptyset$. The audit's sweep found the two readings disagreeing
on 1,892 of 13,615 digraphs, all of them disconnected.

Why the nonempty reading is the intended one (elementary, `sketch`-tier — check it, do not take
it on trust):

1. **The permissive reading refutes the conjecture on four vertices.** For $D$ with arcs
   $0\to1$ and $2\to3$, the set $U=\{0,1\}$ has $\delta^+(U)=\delta^-(U)=\emptyset$, so
   $\emptyset$ is a dicut and $\tau=0$. No arc set meets $\emptyset$, so $D$ has **no dijoin at
   all**, and $A\ne\emptyset$ cannot be partitioned into $0$ dijoins. A reading on which a
   50-year-old open problem is settled by a four-vertex example is a misreading, not a
   counterexample.
2. **It is the literature convention.** Schrijver and Feofiloff–Younger, cited below, treat a
   directed cut as a cut, i.e. as a set of arcs that exists.
3. **The disconnected case then reduces to the connected one** in the usual way rather than
   being degenerate: dicuts of a disjoint union are the dicuts of the parts, so
   $\tau(D_1\sqcup D_2)=\min(\tau(D_1),\tau(D_2))$ and a dijoin of the union is exactly a
   union of dijoins of the parts. The same reduction is stated as item 3 of
   [`attacks/zero-weight-frontier/`](./attacks/zero-weight-frontier/README.md).

**This does not change the cited source–sink-connected theorem below.** Its hypothesis implies
weak connectivity — a finite nonempty DAG has a source and a sink, so two weak components would
give a source with no directed path to a sink in the other component — and on weakly connected
digraphs the two readings agree, so $\tau(D,c)$ and the theorem's conclusion are unaffected.

**What it does change, and where that has already bitten.** Statements about disconnected
digraphs written against the permissive reading are not automatically true here:

- [`attacks/tau2-robbins/`](./attacks/tau2-robbins/README.md), **Lemma A** — the red team on
  issue #153 (PR #160) reports that the lemma mixes the two conventions and that under the
  nonempty convention its conclusion "$G$ is connected" is **false**, with 636 weakly
  disconnected $\tau\ge2$ digraphs as witnesses. Recorded here, not repaired here; that file
  belongs to #153/#160. Its main $\tau=2$ argument treats components separately and is not
  obviously affected, but that is for #160 to settle, not for this note to assert.
- [`attacks/dijoin-exact-ip-search/`](./attacks/dijoin-exact-ip-search/README.md) — its
  exclusion of $\tau\le1$ from the $n=7$ run is justified by "if $\tau=0$ some dicut is empty",
  which is a permissive-reading argument, and its code prunes disconnected DAGs by computing
  $\tau=0$ for them. Under this convention $\tau=0$ never occurs, and a disconnected DAG can
  have $\tau\ge2$ (two disjoint diamonds), so those instances are inside the stated search
  space and were not searched. The gap is closable by the disjoint-union reduction in point 3
  above rather than by more computing, but the write-up's coverage statement needs that
  substitution to be made explicit. Not repaired here; that file belongs to #73.

Several attacks — [`tau-saturation`](./attacks/tau-saturation/README.md),
[`balanced-dicut-hypergraph`](./attacks/balanced-dicut-hypergraph/README.md),
[`tau3-saturated-source-sink`](./attacks/tau3-saturated-source-sink/README.md) — already state
the nonempty convention, and so does the Lean: `IsDicutShore` in
[`../../lean/Verified/Woodall/Basic.lean`](../../lean/Verified/Woodall/Basic.lean) requires
$\delta^+(U)\ne\emptyset$, with `IsDicutShoreAllowingEmpty` naming the permissive alternative
and a `decide`-checked digraph where they disagree. This amendment brings the prose into line
with the code, not the other way round.

Equivalently, a dijoin is a set of arcs whose **contraction** makes $D$ strongly connected. Arc
sets whose reversal makes $D$ strongly connected (called *strengthenings*) are dijoins, but the
converse need not hold.

## Statement

> **Woodall's conjecture (1976).** In any digraph, the arc set $A$ can be partitioned into
> $\tau$ disjoint dijoins.

Equivalently: the minimum size of a dicut equals the maximum number of pairwise disjoint dijoins.
One direction is trivial — $\tau$ disjoint dijoins each consume an arc of the minimum dicut, so
there can never be more than $\tau$. **The conjecture is the existence direction**, and any
"proof" that only establishes the easy inequality has proved nothing.

## Why this is subtle: the neighbouring statements

Getting these straight is most of the work, and mixing them up is the standard failure mode here.

| Statement | Status |
|---|---|
| **Lucchesi–Younger theorem**: min dijoin size = max number of disjoint *dicuts* | **Proven** |
| **Woodall's conjecture**: min dicut size = max number of disjoint *dijoins* | **Open** |
| **Edmonds–Giles conjecture**: weighted/fractional version | **False** — refuted by Schrijver (1980) |

Lucchesi–Younger is Woodall with the roles of dicut and dijoin exchanged. It is a theorem; Woodall
is not. They are not interchangeable, and an argument that silently swaps them is circular.

Schrijver's refutation of Edmonds–Giles matters practically: **any approach that would also prove
the weighted version is provably wrong.** If your argument never uses the fact that arcs are
unweighted, you have either refuted Schrijver or made an error. Check this before writing
anything up — it is a cheap, decisive filter that will kill most naive approaches.

## Known partial results

- **$\tau = 2$**: true, folklore.
- $A$ can always be partitioned into a dijoin and a $(\tau-1)$-dijoin. Much weaker than the
  conjecture, which wants $\tau$ *dijoins*.
- **Source–sink-connected digraphs** (`cited`): the full capacitated packing equality holds;
  the precise statement and hypotheses are recorded below.
- **Condensation**: the problem reduces to the condensation (contract strongly connected
  components), since arcs inside a strong component lie in no dicut. Use this — it shrinks
  instances a lot.
- **Approximate packing** (`cited`): Cornuéjols, Liu & Ravi prove that every digraph with
  minimum dicut size $\tau$ contains $\lfloor \tau/6\rfloor$ pairwise arc-disjoint dijoins,
  constructible in polynomial time. More generally, if the underlying undirected graph admits
  a nowhere-zero circular $k$-flow for rational $k\ge 2$, their theorem gives
  $\lfloor \tau/k\rfloor$ disjoint dijoins. For $\tau\ge2$ the underlying graph is
  2-edge-connected, so Seymour's 6-flow theorem (with Younger's algorithmic version) yields the
  unconditional $1/6$ bound. If Tutte's nowhere-zero 5-flow conjecture holds, the same theorem
  gives $\lfloor \tau/5\rfloor$. They also prove that a $6p$-edge-connected underlying graph
  guarantees $\lfloor \tau p/(2p+1)\rfloor$ disjoint dijoins for every positive integer $p$.

### The source–sink-connected theorem

For a DAG, call a vertex with no entering arcs a **source** and one with no leaving arcs a
**sink**.  Feofiloff–Younger and Schrijver call the DAG **source–sink connected** when every
source has a directed path to every sink.  Schrijver notes immediately after his introductory
formulation that acyclicity is inessential: for a general digraph, impose this condition on its
condensation.  Thus the sources and sinks in the general formulation are the initial and terminal
strong components.

The following capacitated form is `cited`.  Give each arc $a$ a nonnegative integer capacity
$c(a)$, let

$$
  \tau(D,c)=\min\left\{\sum_{a\in B}c(a): B\text{ is a dicut of }D\right\},
$$

and let a $c$-packing of dijoins be a family in which arc $a$ occurs in at most $c(a)$ members.
If the condensation of $D$ is source–sink connected, then $D$ has a $c$-packing of
$\tau(D,c)$ dijoins.  Schrijver's Theorem 4 gives the $0$/$1$ form directly; Theorem 5 and
Corollary 5a give the strong-connector and integer-capacity form, and Section 8 makes the
splitting polynomially constructive (including capacities encoded in binary).  Feofiloff and
Younger independently prove the source–sink-connected DAG case as their transversal-packing
theorem.  Their own proof is not directly algorithmic; their Section 7 points to a separate
polynomial construction.

The papers orient a directed cut as the arcs entering a shore that no arc leaves.  This is
exactly the convention above after taking the complementary shore: the arcs entering
$V\setminus U$ are the arcs in $\delta^+(U)$ when $\delta^-(U)=\varnothing$.  No
Lucchesi–Younger role swap is involved.

With $c\equiv1$, the theorem supplies $\tau$ pairwise arc-disjoint dijoins, hence the Woodall
existence direction for this class.  Any unused arcs can be distributed among the dijoins because
a superset of a dijoin is again a dijoin.

Two tiny fixtures make the hypothesis concrete:

- The diamond with arcs
  $s\to x,s\to y,x\to t,y\to t$ is source–sink connected.  Its minimum dicut has size
  $2$, and the two $s$--$t$ paths are disjoint dijoins.
- The weakly connected DAG with arcs
  $s_1\to t_1,s_2\to t_1,s_2\to t_2$ is a near-miss: $s_1$ is a source and $t_2$ a sink,
  but no directed $s_1$--$t_2$ path exists.  The cited theorem makes no claim about this
  instance; it is not a counterexample.

## Sources

- [Woodall's conjecture — Wikipedia](https://en.wikipedia.org/wiki/Woodall%27s_conjecture) — overview.
- [Feofiloff, *Woodall's conjecture on packing dijoins: a survey* (2005)](https://www.ime.usp.br/~pf/dijoins/download/woodall-conjecture-en.pdf) — **start here**, the most useful single document.
- [Feofiloff's Woodall bibliography](https://www.ime.usp.br/~pf/dijoins/bib.html) — curated reference list.
- [Open Problem Garden entry](https://www.openproblemgarden.org/op/woodalls_conjecture).
- [EGRES Open entry](http://lemon.cs.elte.hu/egres/open/Woodall%27s_conjecture) — the Egerváry group's problem page, usually current.
- Abdi, Cornuéjols & Zlatin, [*On packing dijoins in digraphs and weighted digraphs*](https://doi.org/10.1137/22M1506511), SIAM J. Discrete Math. 37 (2023), 2417–2461 — source of the dijoin plus $(\tau-1)$-dijoin decomposition.
- Cornuéjols, Liu & Ravi, [*Approximately packing dijoins via nowhere-zero flows*](https://doi.org/10.1007/s00493-025-00159-x), Combinatorica 45 (2025), article 32; [full arXiv version](https://arxiv.org/abs/2311.04337) — Theorems 1–3 give the $\tau/6$, connectivity-dependent, and general flow bounds; the conditional $\tau/5$ bound follows by setting $k=5$ under Tutte's conjecture.
- Schrijver, [*Min-max relations for directed graphs*](https://ir.cwi.nl/pub/10048/10048D.pdf), Annals of Discrete Mathematics 16 (1982), 261–280 — Theorem 4 proves the source–sink-connected case, Theorem 5 and Corollary 5a give the connector/capacitated form, and Section 8 gives polynomial algorithms.
- Feofiloff & Younger, [*Directed cut transversal packing for source-sink connected graphs*](https://doi.org/10.1007/BF02579302), Combinatorica 7 (1987), 255–263; [open 1984 technical-report version](https://repositorio.usp.br/directbitstream/e51c51c2-be02-47b1-b2fb-23b4085af8cf/316699.pdf) — independent transversal-packing proof for the DAG case.
- Schrijver, *A counterexample to a conjecture of Edmonds and Giles*, Discrete Math. 32 (1980) 213–215 — read this before proposing any weighted approach.
- Woodall, *Menger and König systems*, in *Theory and Applications of Graphs* (1978) — the original.

## Layout

- `RULES.md` — how work on this problem must be done.
- `attacks/` — one directory per approach.
- `results/` — verified partial results.
