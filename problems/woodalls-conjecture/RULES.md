# Rules — Woodall's conjecture

Problem-specific. The repo-wide protocol in [`../../RULES.md`](../../RULES.md) still applies in
full; this file adds what is particular to a *discrete combinatorial* problem where the objects
are finite and enumerable but the claims are universally quantified.

---

## 0. What makes this problem different

The opposite of the circle-packing directory. There, a result is a finite object anyone can
check. Here, the conjecture quantifies over **all digraphs**, so no amount of successful
checking proves it — while a single counterexample would settle it instantly and be verifiable
in seconds.

That asymmetry sets the strategy. Two honest modes of work:

- **Falsification** — search for a counterexample. Cheap, decisive, fully machine-checkable, and
  a negative result is still a real contribution (see §3).
- **Special cases** — prove the conjecture for a restricted class of digraphs. This is where
  essentially all published progress lives, and it is the realistic route to a partial result.

Both are welcome. What is not welcome is a general proof sketch that does not survive §2.

---

## 1. Mandatory filters before writing anything up

Three cheap checks that kill most wrong approaches. Run all three, and **state in the PR that you
did**, with the outcome.

1. **The Schrijver filter.** Edmonds–Giles — the weighted version — is *false*. If your argument
   never uses that arcs are unweighted, it would prove the weighted version too, so it is wrong.
   Find the step that needs unweightedness. If there isn't one, stop.
2. **The Lucchesi–Younger filter.** That theorem swaps the roles of dicut and dijoin. Confirm you
   have not silently used it in the direction you are trying to prove — the two statements read
   almost identically and substituting one for the other is circular.
3. **The easy-direction filter.** $\le \tau$ disjoint dijoins is trivial. Confirm you are proving
   the existence direction, not restating the bound.

An approach that fails any of these is `refuted`. Record it in `attacks/` with which filter
killed it — that record has real value, because the same idea will occur again.

## 2. Computational search

Counterexample hunting is encouraged and must be reproducible.

**State the search space exactly.** "All digraphs up to 8 vertices" is a claim about a specific
finite set; say how you enumerated it, whether up to isomorphism, and how many instances you
covered. A search whose space is not precisely stated proves nothing, positive or negative.

**Reduce first.** Contract strongly connected components — arcs inside them lie in no dicut, so
the condensation is the real instance. Searching un-reduced digraphs wastes most of your budget
on trivially equivalent copies. Restricting to DAGs is justified by this reduction; say so
explicitly when you do it.

**Verify a counterexample in two independent ways** before believing it. A claimed counterexample
needs:

- the digraph as an explicit arc list,
- $\tau$, with the minimum dicut exhibited,
- a proof that $\tau$ disjoint dijoins do **not** exist.

That last item is the hard one. It is a co-NP-style claim — exhaustive over partitions — so state
the exhaustive procedure and its cost. "My solver returned infeasible" is not sufficient unless
the encoding is given and independently reimplemented per `../../RULES.md` §5. Encoding bugs are
the overwhelmingly likely explanation for an apparent counterexample to a 50-year-old conjecture.

**Negative results get written up.** "No counterexample among all digraphs on $\le n$ vertices,
here is the reproducible search" is a genuine contribution and belongs in `results/` as
`numerical`. Do not discard it because it wasn't the exciting outcome.

## 3. Status mapping for this problem

- A **special case proved** in Lean → `verified:lean`. Realistically this needs a digraph library
  Mathlib may not have; scope a small case first and check what exists before committing.
- A **special case proved** in prose, cross-examined per `../../RULES.md` §5 → `verified:review`.
- An **exhaustive computational search** → `numerical`, always. It constrains where a
  counterexample can live; it never proves the conjecture.
- A **counterexample** → `extraordinary-claim`. Label the PR, do not merge, request both humans.
  This would resolve a 50-year-old open problem, so the prior on an encoding bug vastly exceeds
  the prior on a genuine discovery.

## 4. Definitions are the trap

Dicut, dijoin, $k$-dijoin, and directed cut are easy to confuse, and the conjecture is false-ish
under several plausible misreadings. Before any argument:

- Restate the definitions you are using, in your own words, at the top of the file.
- Sanity-check them on a small example — a directed path, a directed cycle (which has *no*
  dicuts), a DAG with two sources.
- Confirm your code's notion of dicut requires $\delta^-(U) = \emptyset$, not merely
  $\delta^+(U) \ne \emptyset$. This single error invalidates most first attempts.

Test any implementation against the $\tau = 2$ case, which is known true, before trusting it on
anything larger.

## 5. Realistic targets

Partial results count. In rough order of achievability:

1. Implement and test dicut/dijoin/$\tau$ computation, validated against $\tau = 2$ and the
   source–sink-connected DAG case. Everything else depends on this being right.
2. Exhaustive counterexample search over small digraphs, with the space precisely stated.
3. Pin the $\lfloor \tau/6 \rfloor$ bound and its attribution to a primary source, and fix
   `README.md`.
4. Reproduce a known special case (e.g. $\tau = 2$) as a careful written proof, cross-examined.
5. Prove the conjecture for a new restricted class — the genuine research target.

Read the Feofiloff survey before proposing anything. Most natural ideas here are fifty years old
and already in it.
