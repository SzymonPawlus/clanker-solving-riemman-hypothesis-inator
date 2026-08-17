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

Note a dijoin is exactly a set of arcs whose reversal makes $D$ strongly connected — a useful
alternative view when writing code.

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
- **Approximate packing**: every digraph with min dicut $\tau$ contains at least
  $\lfloor \tau/6 \rfloor$ disjoint dijoins, improving to $\lfloor \tau/5 \rfloor$ if Tutte's
  nowhere-zero 5-flow conjecture holds.

<!-- The tau/6 bound and its attribution are from secondary sources and are not yet pinned to a
     primary reference. Status `numerical`/unverified until someone checks the papers below. -->

## Sources

- [Woodall's conjecture — Wikipedia](https://en.wikipedia.org/wiki/Woodall%27s_conjecture) — overview.
- [Feofiloff, *Woodall's conjecture on packing dijoins: a survey* (2005)](https://www.ime.usp.br/~pf/dijoins/download/woodall-conjecture-en.pdf) — **start here**, the most useful single document.
- [Feofiloff's Woodall bibliography](https://www.ime.usp.br/~pf/dijoins/bib.html) — curated reference list.
- [Open Problem Garden entry](https://www.openproblemgarden.org/op/woodalls_conjecture).
- [EGRES Open entry](http://lemon.cs.elte.hu/egres/open/Woodall%27s_conjecture) — the Egerváry group's problem page, usually current.
- Abdi, Cornuéjols & Zlatin, [*On packing dijoins in digraphs and weighted digraphs*, arXiv:2202.00392](https://arxiv.org/abs/2202.00392) — the main recent contribution.
- [*Approximately packing dijoins via nowhere-zero flows*, arXiv:2311.04337](https://arxiv.org/pdf/2311.04337) — source of the $\tau/6$ and conditional $\tau/5$ bounds.
- Schrijver, *A counterexample to a conjecture of Edmonds and Giles*, Discrete Math. 32 (1980) 213–215 — read this before proposing any weighted approach.
- Woodall, *Menger and König systems*, in *Theory and Applications of Graphs* (1978) — the original.

## Layout

- `RULES.md` — how work on this problem must be done.
- `attacks/` — one directory per approach.
- `results/` — verified partial results.
