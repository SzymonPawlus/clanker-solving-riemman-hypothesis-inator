# Woodall's conjecture

**Status:** open since 1976. Notably, the natural weighted generalisation is **false**, which
constrains what any proof can look like.

Shared conventions: [`../README.md`](../README.md). Repo-wide protocol:
[`../../RULES.md`](../../RULES.md). **Problem-specific rules: [`RULES.md`](./RULES.md) — read
before working on this problem.**

## Definitions

Let $D = (V, A)$ be a digraph. For nonempty proper $U \subsetneq V$ write $\delta^+(U)$ for the
arcs leaving $U$ and $\delta^-(U)$ for those entering.

- A **dicut** is a set $\delta^+(U)$ where $\delta^-(U) = \emptyset$ — a cut with all arcs
  pointing the same way.
- A **dijoin** is a set of arcs meeting *every* dicut at least once.
- A **$k$-dijoin** meets every dicut at least $k$ times.
- $\tau$ denotes the minimum size of a dicut.

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
- **Source–sink connected DAGs**: true where every source has a path to every sink.
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

## Sources

- [Woodall's conjecture — Wikipedia](https://en.wikipedia.org/wiki/Woodall%27s_conjecture) — overview.
- [Feofiloff, *Woodall's conjecture on packing dijoins: a survey* (2005)](https://www.ime.usp.br/~pf/dijoins/download/woodall-conjecture-en.pdf) — **start here**, the most useful single document.
- [Feofiloff's Woodall bibliography](https://www.ime.usp.br/~pf/dijoins/bib.html) — curated reference list.
- [Open Problem Garden entry](https://www.openproblemgarden.org/op/woodalls_conjecture).
- [EGRES Open entry](http://lemon.cs.elte.hu/egres/open/Woodall%27s_conjecture) — the Egerváry group's problem page, usually current.
- Abdi, Cornuéjols & Zlatin, [*On packing dijoins in digraphs and weighted digraphs*](https://doi.org/10.1137/22M1506511), SIAM J. Discrete Math. 37 (2023), 2417–2461 — source of the dijoin plus $(\tau-1)$-dijoin decomposition.
- Cornuéjols, Liu & Ravi, [*Approximately packing dijoins via nowhere-zero flows*](https://doi.org/10.1007/s00493-025-00159-x), Combinatorica 45 (2025), article 32; [full arXiv version](https://arxiv.org/abs/2311.04337) — Theorems 1.1–1.3 give the $\tau/6$, connectivity-dependent, and general flow bounds; the conditional $\tau/5$ bound follows by setting $k=5$ under Tutte's conjecture.
- Schrijver, *A counterexample to a conjecture of Edmonds and Giles*, Discrete Math. 32 (1980) 213–215 — read this before proposing any weighted approach.
- Woodall, *Menger and König systems*, in *Theory and Applications of Graphs* (1978) — the original.

## Layout

- `RULES.md` — how work on this problem must be done.
- `attacks/` — one directory per approach.
- `results/` — verified partial results.
