# Circle packing in an equilateral triangle

**Status:** open for most $n$. Optimal packings are proven for only a handful of small cases;
everything else is best-known-construction.

Shared conventions: [`../README.md`](../README.md). Repo-wide protocol:
[`../../RULES.md`](../../RULES.md). **Problem-specific rules: [`RULES.md`](./RULES.md) — read
before working on this problem.**

## Statement

Pack $n$ unit circles into the smallest possible equilateral triangle. Write $s(n)$ for the
minimal side length.

Only $s(n)$ for $n \le 15$-ish is settled; see the table below. There is no known closed form
for general $n$.

## The reduction that makes this tractable

A unit circle inside the triangle has its centre at distance $\ge 1$ from each side. The set of
valid centres is therefore a concentric equilateral triangle of side $s - 2\sqrt{3}$.

> Packing $n$ unit circles in an equilateral triangle of side $s$ is **equivalent** to placing
> $n$ points with pairwise distances $\ge 2$ in an equilateral triangle of side $s - 2\sqrt{3}$.

So $s(n) = 2\sqrt{3} + d(n)$, where $d(n)$ is the smallest side of an equilateral triangle
admitting $n$ points at mutual distance $\ge 2$. Work in the point formulation — the constraints
become finitely many pairwise inequalities plus three half-plane containments, all of which are
cheap to check exactly. `RULES.md` §2 requires certificates in this form.

## Known results

Two kinds of statement, and conflating them is the main way to overclaim here:

- **Construction / upper bound.** An explicit packing witnessing $s(n) \le c$. Self-certifying —
  hand over the coordinates and anyone can check them.
- **Optimality / lower bound.** A proof that no packing does better, $s(n) \ge c$. Far harder;
  needs exhaustive case analysis or rigorous global optimisation.

### Proven optimal

| $n$ | $s(n)$ | Credited to |
|---|---|---|
| 1, 2, 3 | trivial | — |
| 4 | $4\sqrt{3} \approx 6.928$ | Melissen (1987, per Friedman's "Milano") |
| 5 | $4 + 2\sqrt{3} \approx 7.464$ | as above |
| 6 | $4 + 2\sqrt{3} \approx 7.464$ | Oler / Groemer (1961) |
| 9 | $6 + 2\sqrt{3} \approx 9.464$ | Melissen (1993) |
| 10 | $6 + 2\sqrt{3} \approx 9.464$ | Oler / Groemer (1961) |
| 12 | $4 + 4\sqrt{3} \approx 10.928$ | Melissen (1994) |
| 15 | $8 + 2\sqrt{3} \approx 11.464$ | Erdős / Groemer (1961) |

### Best known only (optimality *not* established)

| $n$ | best known $s(n)$ | Credited to |
|---|---|---|
| 7 | $2 + 4\sqrt{3} \approx 8.928$ | Melissen (1993) |
| 8 | $2 + 2\sqrt{3} + \tfrac{2\sqrt{33}}{3} \approx 9.293$ | Melissen (1993) |
| 11 | $4 + 2\sqrt{3} + \tfrac{4\sqrt{6}}{3} \approx 10.730$ | Melissen (1993) |
| 13 | $4 + \tfrac{2\sqrt{6}}{3} + \tfrac{10\sqrt{3}}{3} \approx 11.406$ | Melissen (1993) |
| 14 | $8 + 2\sqrt{3} \approx 11.464$ | Erdős / Oler (1961) |
| 16–34 | various | Graham & Lubachevsky (1995) |

### ⚠️ Sources disagree — resolve this before relying on the table

Wikipedia states optimal packings are **proven for all $n \le 15$**. Erich Friedman's packing
pages mark $n = 7, 8, 11, 13, 14$ as best-known only. These cannot both be right.

Likely explanations: Friedman's pages predate later proofs, or "proven" is being used loosely
for one of the two. **This is the natural first issue for this problem** — resolve it against
the primary literature (Melissen's 1997 thesis is the place to look) and correct this file.
Until then, treat the split above as `numerical`, not `cited`.

### The Erdős–Oler conjecture

For a triangular number $T_k = k(k+1)/2$, removing one circle from an optimal $T_k$-packing
still gives an optimal packing: $s(T_k - 1) = s(T_k)$. Proven for $n \le 15$. Note rows $n=15/14$
and $n=10/9$ above exhibit exactly this.

Graham and Lubachevsky conjectured seven further infinite families of optimal packings, covering
cases including $n = 37, 40, 42, 43, 46, 49$.

## Sources

Primary references, roughly in order of usefulness for getting started:

- [Circle packing in an equilateral triangle — Wikipedia](https://en.wikipedia.org/wiki/Circle_packing_in_an_equilateral_triangle) — overview and table.
- [Erich Friedman, Packing Center — circles in triangles](https://erich-friedman.github.io/packing/cirintri/) — per-$n$ diagrams, exact side lengths, and proven/best-known status.
- [Erich's Packing Center (index)](https://erich-friedman.github.io/packing/) — the sibling problems.
- Graham & Lubachevsky, *Dense packings of equal disks in an equilateral triangle: from 22 to 34 and beyond*, Electronic J. Combinatorics 2 (1995), #A1 — **open access**, and the source of the 22–34 records plus the infinite families. Also describes the billiard-simulation method worth reusing.
- Melissen, *Packing and covering with circles*, PhD thesis, Utrecht University (1997) — the most complete account of the small-$n$ optimality proofs.
- Melissen, *Densest packings of congruent circles in an equilateral triangle*, Amer. Math. Monthly 100 (1993) 916–925.
- Oler, *A finite packing problem*, Canad. Math. Bull. 4 (1961) — the Oler inequality, the main lower-bound tool.
- [Packomania](http://www.packomania.com/) — maintained record tables for related packing problems; check before claiming any record.

## Layout

- `RULES.md` — how work on this problem must be done. Certificates, not screenshots.
- `attacks/` — one directory per approach.
- `results/` — verified constructions and optimality results.
