# Oler's inequality — the lower-bound tool

**This is not an attack that can succeed.** It is a literature write-up whose main finding is a
**negative result**, recorded as required by [`../../../../RULES.md`](../../../../RULES.md) §6.3.

> **Kill-criterion (from issue #17):** *"if Oler's inequality turns out to be slack for all n where
> the optimum is unknown, then it cannot settle any open case alone."*
>
> **The kill-criterion is met.** Oler's inequality is tight **exactly** at the triangular numbers
> $n = T_k = k(k+1)/2$, and the optimum is already proven for every triangular number — by Oler
> himself, and by nothing else. On every non-triangular $n \le 15$, where the optimum is known, the
> bound is slack by $0.37$–$0.92$ in $s$ — on the order of half a circle diameter. On $n = 16,17,18$
> it falls $0.76$–$0.89$ short of the *best known construction*, so it could only settle those cases
> if every published packing there is beatable by a huge margin. **Oler alone cannot settle any open
> case.** See §5, including §5.0 on the one point where I stop short of a proof.

That does *not* make Oler useless — it is the reason the triangular numbers are solved at all, and
it is the correct scaffolding for a case analysis. §3 records what the published proofs add on top
of it. §4 says what formalising it would cost (short answer: far more than this repo has).

## Provenance of the sources — read this before trusting anything below

Per the honesty requirement in issue #17:

| Source | How I used it |
|---|---|
| **Oler, *A finite packing problem*, Canad. Math. Bull. **4** (1961) 153–155.** [doi:10.4153/CMB-1961-018-7](https://doi.org/10.4153/CMB-1961-018-7) | **Read in full, primary source.** All 3 pages, from the Cambridge Core scan. Every quotation in §1 is transcribed from that scan. |
| Oler, *An inequality in the geometry of numbers*, Acta Math. **105** (1961) 19–48. | **NOT read.** This is where the theorem is actually *proved*; the CMB note only derives a corollary from it and cites it as "[a paper] which is shortly to appear". Everything I say about *why* Oler's inequality is true is therefore reconstruction, marked `sketch`, not a report of Oler's proof. |
| Melissen & Schuur, *Packing 16, 17 or 18 circles in an equilateral triangle*, Discrete Math. **145** (1995) 333–342. | **Read in full** (open-access copy at [ris.utwente.nl](https://ris.utwente.nl/ws/files/6509759/Melissen95packing.pdf)). Source of the attribution sentence in §3 and the $t_{16},t_{17},t_{18}$ values in §2. |
| Tedeschi & Mackey, *On Packing Thirteen Points in an Equilateral Triangle*, AJUR **18**(2) (2021) 3–12. | **Read in full** ([open access](https://www.ajuronline.org/uploads/Volume_18_2/AJUR_Vol_18_Issue_2_Sept_2021p3.pdf)). **Secondary source.** It is an undergraduate-journal paper, and my account of *Melissen's, Payan's and Joós's methods* in §3 rests almost entirely on it. Treat those method descriptions as second-hand. |
| Melissen (1993 AMM), Melissen (1994 Acta Math. Hungar.), Payan (1997 Discrete Math.), Joós (2021 Aequat. Math.) | **NOT read — all paywalled.** I have their abstracts/bibliographic data only. Anything attributed to them below comes from a secondary source and is flagged. |
| Amore, *Circle packing in regular polygons*, arXiv:[2212.12287](https://arxiv.org/abs/2212.12287) (Phys. Fluids **35** 027130, 2023). | **Read the relevant sections.** Used only as an independent modern restatement of Oler's inequality, to check I had transcribed it correctly. |
| Wikipedia, [Circle packing in an equilateral triangle](https://en.wikipedia.org/wiki/Circle_packing_in_an_equilateral_triangle). | Used **only** for the sentence "Optimal solutions have been proved for $n \le 15$, and for any triangular number of circles", which I then corroborated independently against Melissen–Schuur, Payan's abstract and Tedeschi–Mackey. |

**Explicitly not used:** an item titled *"Optimal Circle Packings for Triangular Numbers: A Detailed
Mathematical Proof of the Erdős–Oler Conjecture"* circulating on Academia.edu/ResearchGate turns up
high in searches for this topic. It is not peer-reviewed, and its title claims a result (the
Erdős–Oler conjecture in general) that the peer-reviewed literature still lists as open. **Do not
cite it.** Flagged here so the next agent does not have to rediscover this.

---

## 1. The statement — `cited`

**Status:** `cited` (Oler 1961, primary source, read in full).

### 1.1 Verbatim, as Oler states it

> Let $\pi$ be a Jordan polygon and $E$ a finite set of points which together satisfy the following
> conditions.
>
> (i) The vertices of $\pi$ belong to $E$.
> (ii) The set $E$ is contained in the closed region bounded by $\pi$.
> (iii) The distance between any two points in $E$ is not less than 1.
>
> Then the following inequality holds:
>
> $$\tfrac{2}{\sqrt 3}A(\pi) + \tfrac{1}{2}M(\pi) + 1 \ \ge\ N$$
>
> where $A(\pi)$ is the area of the region bounded by $\pi$, $M(\pi)$ is the length of $\pi$ and $N$
> is the number of points in $E$.
>
> — Oler, *A finite packing problem*, Canad. Math. Bull. 4 (1961), p. 154.

### 1.2 Every symbol

| Symbol | Meaning |
|---|---|
| $\pi$ | A **Jordan polygon**: a closed, non-self-intersecting polygonal curve in $\mathbb R^2$. It bounds a well-defined interior (Jordan curve theorem). |
| $E$ | A **finite** set of points in $\mathbb R^2$. |
| $N$ | $= \lvert E\rvert$, the number of points. |
| $A(\pi)$ | The **area** enclosed by $\pi$. |
| $M(\pi)$ | The **length of the curve** $\pi$, i.e. the perimeter — $\sum_i \lvert v_{i+1} - v_i\rvert$ over the edges. |
| $1$ | The **minimum separation**, normalised. Condition (iii) fixes the scale; everything else is homogeneous in it. |

**Hypothesis (i) is load-bearing and easy to miss.** The inequality is *not* "any $N$ points in any
region $\pi$". Every vertex of the polygon must itself be one of the points. Oler's own application
satisfies it by taking $\pi = H$, the convex hull of $E$ — whose vertices are automatically points
of $E$.

Without (i) the inequality is false as stated: shrink $\pi$ to a tiny polygon far from a large point
set and $A, M \to 0$ while $N$ stays large. (ii) is what rules this out, and (i) is what makes the
boundary term $\tfrac12 M(\pi)$ the *right* correction rather than an arbitrary one.

**Note on what Oler actually proved here.** The CMB note does *not* contain a proof. It states this
as "the following corollary to our theorem on the packing of convex disks", citing Oler, *An
inequality in the geometry of numbers*, Acta Math. — a paper that had not yet appeared. **The proof
lives in the Acta paper, which I have not read.**

### 1.3 Independent restatement (consistency check)

Amore, arXiv:2212.12287, eq. (28), states it for $N$ disks of unit *diameter* in a Jordan polygon
$\Pi$ as $N \le \frac{2}{\sqrt3}A(\Pi) + \frac12 P(\Pi) + 1$. Same constants, same shape. Unit
diameter disks $\Leftrightarrow$ centres at mutual distance $\ge 1$, so the two statements agree.

### 1.4 Why it should be true — `sketch`

**Status:** `sketch` — this is *my* reconstruction of the intuition, not Oler's argument, which I
have not read. Do not build on it.

The bound is the exact point count of the triangular (hexagonal) lattice, split into a bulk term and
a boundary term.

- **Bulk.** In the densest lattice of points at mutual distance $\ge 1$ — the triangular lattice with
  spacing exactly $1$ — the fundamental cell is a rhombus of area $\frac{\sqrt3}{2}$, so there is one
  point per area $\frac{\sqrt3}{2}$, i.e. $\frac{2}{\sqrt3}$ points per unit area. That is exactly
  the coefficient of $A(\pi)$. This is the finite-region analogue of the Thue/Fejes Tóth/Rogers
  density theorems Oler cites as [1]–[3] in his introduction.
- **Boundary.** A point on the boundary "owns" only about half a cell, so the area term undercounts
  it. Along an edge, points at mutual distance $\ge 1$ occur at linear density $\le 1$ per unit
  length, and the correction is half of that: $\frac12 M(\pi)$.
- **Corner.** The single $+1$ is an Euler-characteristic-style constant: the boundary is a closed
  curve, so the "one extra point" is the same $+1$ that turns $k$ intervals into $k+1$ endpoints.

The self-consistency check that this is the *right* split, and not merely a plausible one, is that
the three terms sum to the triangular-lattice count **exactly**, with no slack — see §2.1.

**What this intuition does not explain**, and what the Acta paper presumably supplies, is why an
*arbitrary* (non-lattice) point set cannot beat the lattice locally. That is the entire difficulty,
and nothing above touches it.

---

## 2. What it gives for $s(n)$, and where it is tight

### 2.1 The specialisation to the equilateral triangle — `cited` (Oler's own derivation)

Oler carries out exactly this specialisation on p. 154 of the CMB note. Transcribed:

> We consider a set $E$ contained in or on a triangle $T$ of sides $n$ ($n$ a positive integer) with
> the property that the distance between any two points in $E$ is at least 1. Let $H$ be the convex
> hull of $E$ [...]. It is clear that it is a polygon whose vertices are in $E$ and furthermore that
> it is contained in or coincides with $T$. Hence $A(H) \le A(T)$. Further since $H$ is convex it is
> easy to prove that $M(H) \le M(T)$.

Applying the inequality to $(H, E)$ and then $A(H) \le A(T) = \frac{\sqrt3}{4}n^2$,
$M(H) \le M(T) = 3n$:

> $$N \le 1 + \tfrac{3}{2}n + \tfrac{1}{2}n^2 = \tfrac12 (n+1)(n+2).$$

and Oler notes equality is attained by the triangular-lattice subset.

Two structural points worth extracting, because they matter for any future attempt:

1. The step is a **two-stage monotonicity**: Oler applies the inequality to the *hull*, then relaxes
   to the *containing triangle*. All the slack for non-triangular $n$ enters at the second stage —
   and only there, since the inequality itself is exact on the lattice.
2. Oler states it for **integer** side $n$, but nothing in the derivation uses integrality. It holds
   verbatim for real side length.

### 2.2 Converting to $s(n)$ — `sketch` (my derivation, arithmetic only)

**Status:** `sketch`. The input (§2.1) is `cited`; the rearrangement below is mine and has not been
cross-examined. It is elementary algebra, but §3 of the repo rules says my own derivations are not
assumable until someone else checks them.

The repo's point formulation (`../../README.md`): $n$ points at pairwise distance $\ge 2$ in an
equilateral triangle of side $d$, with $s = d + 2\sqrt3$. Oler is normalised to distance $\ge 1$, so
rescale by $\tfrac12$: put $a = d/2$. Then §2.1 with side $a$ gives

$$n \ \le\ \frac{2}{\sqrt3}\cdot\frac{\sqrt3}{4}a^2 \ +\ \frac12\cdot 3a\ +\ 1 \ =\ \frac{a^2+3a+2}{2} \ =\ \frac{(a+1)(a+2)}{2}.$$

Solving $a^2 + 3a + 2 - 2n \ge 0$ for $a > 0$:

$$a \ \ge\ \frac{\sqrt{8n+1}-3}{2}, \qquad d \ \ge\ \sqrt{8n+1}-3,$$

and therefore

$$\boxed{\ s(n)\ \ge\ s_{\mathrm{Oler}}(n) \ :=\ 2\sqrt3 \;+\; \sqrt{8n+1} \;-\; 3\ }$$

**This is the form to use.** It is a clean closed form in $n$, valid for all $n \ge 1$.

**Tightness at triangular numbers, exactly.** If $n = T_k = k(k+1)/2$ then $8n+1 = (2k+1)^2$, so
$\sqrt{8n+1} = 2k+1$ and

$$s_{\mathrm{Oler}}(T_k) \ =\ 2\sqrt3 + 2(k-1),$$

which is precisely the side length of the triangular arrangement in $k$ rows (spacing 2, so
$d = 2(k-1)$). Conversely $8n+1$ is a perfect square iff $n$ is triangular, so
**$s_{\mathrm{Oler}}(n)$ equals the triangular-lattice value if and only if $n$ is triangular.**

### 2.3 The numbers — `numerical`

**Status:** `numerical`. Reproduce with `python3 oler_bound.py` (stdlib only, in this directory).
Known values from `../../README.md`, except $s(13)$ which I recomputed from Joós's separation
distance as a cross-check (agreement to 6 dp — see §2.4).

| $n$ | triangular? | $s_{\mathrm{Oler}}(n)$ | known / best-known $s(n)$ | gap | verdict |
|---:|:---:|---:|---:|---:|:---|
| 1 | **T₁** | 3.464102 | 3.464102 | 0.000000 | **tight** |
| 2 | | 4.587207 | 5.464102 | 0.876894 | slack |
| 3 | **T₂** | 5.464102 | 5.464102 | 0.000000 | **tight** |
| 4 | | 6.208664 | 6.928203 | 0.719539 | slack |
| 5 | | 6.867226 | 7.464102 | 0.596876 | slack |
| 6 | **T₃** | 7.464102 | 7.464102 | 0.000000 | **tight** |
| 7 | | 8.013936 | 8.928203 | 0.914267 | slack |
| 8 | | 8.526359 | 9.293810 | 0.767451 | slack |
| 9 | | 9.008105 | 9.464102 | 0.455996 | slack |
| 10 | **T₄** | 9.464102 | 9.464102 | 0.000000 | **tight** |
| 11 | | 9.898083 | 10.730088 | 0.832005 | slack |
| 12 | | 10.312959 | 10.928203 | 0.615244 | slack |
| 13 | | 10.711052 | 11.406496 | 0.695443 | slack |
| 14 | | 11.094247 | 11.464102 | 0.369854 | slack |
| 15 | **T₅** | 11.464102 | 11.464102 | 0.000000 | **tight** |

And for the first genuinely open cases, where the right-hand column is only an **upper** bound (best
known construction), so the row records the width of the interval in which $s(n)$ still lies:

| $n$ | $s_{\mathrm{Oler}}(n)$ (lower) | best known (upper) | interval still open |
|---:|---:|---:|---:|
| 16 | 11.821918 | 12.713629 | 0.891710 |
| 17 | 12.168802 | 12.928203 | 0.759402 |
| 18 | 12.505696 | 13.293790 | 0.788094 |
| 21 = **T₆** | 13.464102 | 13.464102 | **0 — settled by Oler** |

($t_{16}=0.216227269\ldots$, $t_{17}=(3-\sqrt3)/6$, $t_{18}=0.203465240\ldots$ from Melissen &
Schuur 1995, converted by $s = 2\sqrt3 + 2/t_n$.)

**Reading of the table.** The tight rows are exactly the triangular rows — 1, 3, 6, 10, 15, and by
§2.2 this continues for every $T_k$. Everywhere else the gap is between $0.37$ and $0.92$; a circle
has diameter $2$, so Oler is off by roughly a fifth to a half of a circle diameter. That is not a
near miss to be closed by a small extra argument; it is a gap of the same order as the whole
question.

### 2.4 Consistency checks performed

- $s_{\mathrm{Oler}}(T_k) = 2\sqrt3 + 2(k-1)$ verified numerically for $k = 1..8$.
- $s(13)$: Joós's separation distance in a **unit** triangle is
  $d_{13} = 9 - 5\sqrt3 - \tfrac72\sqrt6 + 6\sqrt2 \approx 0.251813237$ (quoted by Tedeschi & Mackey
  from Joós 2021). Then $s(13) = 2\sqrt3 + 2/d_{13} = 11.406495854\ldots$, matching the
  $\approx 11.406$ in `../../README.md`. This independently validates both the rescaling convention
  used throughout this file and that row of the repo's table.
- The Oler bound is below every known value in the table (it had better be — a violation would mean
  I had made a sign or scaling error).

---

## 3. What the published proofs actually add — `cited`, but mostly via a secondary source

**Read the provenance table first.** I could not obtain Melissen 1993/1994, Payan 1997 or Joós 2021.
The method descriptions here are from **Tedeschi & Mackey (AJUR 2021)** and from Melissen & Schuur
(1995), which I did read. Where I am reporting a secondary account of a paper's method, it says so.

### 3.1 Attribution — who proved what

Verbatim from Melissen & Schuur 1995, p. 334 (**read in full, primary for this sentence**):

> Optimal packings in an equilateral triangle were first determined by Oler [23] for the triangular
> numbers $n = k(k+1)/2$, $k = 2, 3, \ldots$, for $n \le 6$ by Milano [20], and by the first author
> for $n \le 12$ [16, 18].

with [23] = Oler 1961, [16] = Melissen, Amer. Math. Monthly **100** (1993) 916–925, [18] = Melissen,
Acta Math. Hungar. **65** (1994) 389–393.

Combining with Payan and Joós, the state of the art is:

| $n$ | proved by | reference |
|---|---|---|
| $n = T_k$, **all** $k$ | **Oler** — the inequality alone | Oler 1961 |
| $n \le 6$ | Milano (independently) | Milano, mémoire de licence, ULB 1987 |
| $4 \le n \le 12$ | Melissen | AMM 100 (1993); $n=11$ in Acta Math. Hungar. 65 (1994) |
| $n = 13$ | Joós | Aequat. Math. 95 (2021) 35–65 |
| $n = 14$ ($=T_5-1$) | Payan | Discrete Math. 165–166 (1997) 555–565 |
| $n = 20$ ($=T_6-1$) | Payan — **see caveat below** | same |
| $n \ge 16$, $n$ not triangular | **open** | — |

**Correction to the repo README (which I must not edit — it is locked by PR #10).**
`../../README.md` currently lists $n = 7, 8, 11, 13, 14$ under "best known only (optimality *not*
established)" and flags a Wikipedia/Friedman disagreement. **The disagreement resolves in
Wikipedia's favour**: all of $7, 8, 11, 13, 14$ are proven. $7, 8, 11$ are inside Melissen's $n\le12$
range (with $n=11$ the subject of its own 1994 paper); $n=13$ is Joós 2021; $n=14$ is Payan 1997.
Friedman's pages simply predate Payan and Joós. That is issue-#17-adjacent housekeeping and belongs
in whatever issue owns the README — it is noted here so the information is not lost.

**Caveat on $n = 20$.** Payan's own abstract (which I read; the full paper is paywalled) says the
$k=5$ proof *"can be extended for the case $k=6$"* — a statement of extensibility, not necessarily a
carried-out proof. Tedeschi & Mackey list $n = 20$ flatly as proven, citing Payan. I cannot tell
from outside which is right. **Treat $n=20$ as unresolved-in-this-repo** until someone reads Payan.

### 3.2 What each proof adds on top of Oler

- **Triangular $n$ — Oler alone, and nothing else.** This is the one place where the inequality is
  the complete proof. §2.2 shows why: the bound is exactly attained, so there is no slack to close.

- **Melissen, $4 \le n \le 12$ — a dissection/pigeonhole argument, essentially *not* Oler.**
  Tedeschi & Mackey (secondary) describe it as proving the optimal placements *"using only partitions
  and direct applications of Dirichlet's pigeon-hole principle."* The shape of the argument: cut the
  triangle into $n-1$ pieces each of diameter $< t_n$; then $n$ points force two into one piece,
  contradiction. The extra ingredient over Oler is therefore **a hand-designed dissection per $n$** —
  it is a bespoke combinatorial certificate, not a general principle. A load-bearing lemma of
  Melissen's, quoted by Tedeschi & Mackey: *"In an optimal configuration of $n \ge 3$ points in an
  equilateral triangle, the three vertices of the triangle must be among the selected points."*

- **Payan, $n = 14$ (and the $T_k - 1$ family) — this is the Erdős–Oler conjecture.** Oler himself
  poses it, as an open question, on the last page of the very note that proves the inequality:
  > *"Thus can one find a set of $\frac12(n+1)(n+2)-1$ points, the distance between any two being at
  > least one, in an equilateral triangle whose sides are $n - \varepsilon$ where $\varepsilon > 0$?
  > [...] this question remains open."*

  Payan's abstract states the conjecture had previously been shown only for $k \le 4$, and that he
  settles $k=5$. So $T_k - 1$ is *precisely* the family where Oler's slack has to be closed by hand,
  and 36 years of effort produced two more values of $k$. Melissen & Schuur add the relevant negative
  fact for $T_k - 2$: *"For $n = k(k+1)/2 - 2$ we could do the same and remove two circles. It was
  shown in [16], however, that this situation can always be improved slightly."* — i.e. the naive
  "keep deleting circles" pattern breaks immediately after one deletion.

- **Joós, $n = 13$ — continuous methods and heavy case analysis.** Tedeschi & Mackey (secondary):
  *"Unlike Melissen's proofs, however, Joos's proof for the optimal arrangement of thirteen points in
  an equilateral triangle requires continuous functions and calculus"*, and *"relies heavily on
  inequalities, and considers several cases."* The paper is 31 pages (Aequat. Math. 95, 35–65) for a
  **single value of $n$**. Tedeschi & Mackey's own contribution is a partial *discrete* re-proof:
  they show that fixing either of two specific points reduces $n=13$ to Melissen-style dissection,
  and identify exactly what remains (*"all that remains to be proven is that we cannot place thirteen
  points outside of $H$ and that we cannot fit twelve points outside of the union of $H$ and $P$"*).

### 3.3 The lesson for this repo

Every optimality proof beyond the triangular numbers is **one value of $n$, by hand, at a cost of
10–30 journal pages, over a span of 60 years**. There is no general method. Oler supplies the
framing and the triangular cases; the rest is a bespoke exhaustive geometric argument per $n$.

Concretely, a new optimality proof for an open $n$ would have to supply a *complete* argument in the
$\approx 0.8$-wide window §2.3 leaves — Oler contributes nothing inside that window.

---

## 4. Lean feasibility — `sketch` (an engineering assessment, not a theorem)

**Verdict: not feasible in this repo. Do not open an issue to formalise Oler's inequality.**

I inspected the Mathlib checkout at `lean/.lake/packages/mathlib` (read-only; `lean/` belongs to
another worker) rather than assuming. Findings:

| Needed | In Mathlib? |
|---|---|
| Polygons | **Partial.** `Mathlib/Geometry/Polygon/Basic.lean` exists, but it is brand new and *very* thin: a `Polygon P n` structure wrapping `Fin n → P`, edge paths, `boundary`, non-degeneracy predicates. That is all. |
| Area enclosed by a polygon | **No.** No shoelace formula; `grep` for `shoelace` returns nothing. One could define it as `volume (convexHull ℝ (Set.range verts))` in the convex case — `Mathlib/Analysis/Convex/Measure.lean` gives `Convex.addHaar_frontier` and `Convex.nullMeasurableSet`, so the object is at least well-behaved — but there is no computation lemma for it. |
| Perimeter | **No.** `grep -rli "perimeter"` over all of Mathlib returns **zero files**. It would have to be defined from scratch, and for the convex-hull application one first needs the hull's vertices in **cyclic order**, which Mathlib also does not provide. |
| Jordan curve theorem | **No.** `grep -rli "jordan curve"` returns nothing. Oler's hypothesis is stated for a Jordan polygon, so even *stating* the general theorem faithfully is blocked. (Restricting to convex $\pi$ dodges this — and suffices for the triangle application — so this is the one obstacle with a cheap workaround.) |
| Geometry of numbers | **Only Minkowski.** `Mathlib/MeasureTheory/Group/GeometryOfNumbers.lean` contains exactly three theorems, all versions of Minkowski's convex body theorem. Oler's *An inequality in the geometry of numbers* is a different and much harder result; nothing resembling it is present. |
| Delaunay triangulation / planar subdivision | **No.** No file matches `*Delaunay*` or `*Triangulation*` in the planar-geometry sense. Modern proofs of Oler/Groemer-type inequalities go through exactly this machinery. |

**Cost estimate.** The statement alone needs polygon area, polygon perimeter, cyclic hull ordering,
and (for full generality) Jordan. The proof needs a 30-page 1961 Acta Mathematica paper whose
prerequisites are themselves absent. This is a multi-person-year formalisation project of the kind
that gets its own paper, not a repo task. `../../RULES.md` §4 permits `verified:review` when there is
"a large Mathlib gap" — this is about as large a gap as the problem offers.

**What *is* cheap in Lean, and worth doing instead.** The §2.2 derivation is pure real arithmetic. A
theorem of the form

```
theorem s_lower_bound_of_oler
    (oler : ∀ (a : ℝ) (m : ℕ), 0 ≤ a → PointsAtDistanceOne m a → (m:ℝ) ≤ (a^2 + 3*a + 2)/2)
    (n : ℕ) (d : ℝ) (hd : PackingExists n d) :
    2*Real.sqrt 3 + Real.sqrt (8*n+1) - 3 ≤ 2*Real.sqrt 3 + d
```

takes Oler as an **explicit hypothesis** (not an `axiom` — CI rejects new axioms, and a hypothesis
in the statement is honest about the dependency) and discharges only the algebra. That is an
afternoon of work and would give a machine-checked *reduction*. Whether it is worth an afternoon,
given §5, is doubtful — the bound it certifies cannot settle anything open. Recorded as an option,
not a recommendation.

---

## 5. The negative result, stated plainly

**Status:** `sketch` for the derivation in §2.2 that underpins it; `cited` for the two literature
facts it combines. The conclusion is only as strong as the weaker of those — see `../../../../RULES.md`
§3 on status propagation. It should be cross-examined before anyone relies on it to *close* a
direction.

Oler's inequality settles $n$ on its own precisely when $s(n) = s_{\mathrm{Oler}}(n)$. So the
question is: for which $n$ does the bound *meet* the truth?

1. `sketch` (§2.2): $s_{\mathrm{Oler}}(n) = 2\sqrt3 + \sqrt{8n+1} - 3$ equals the triangular-lattice
   side length iff $8n+1$ is a perfect square, i.e. **iff $n$ is triangular**.
2. `cited` (Oler 1961; Melissen & Schuur 1995 p. 334; Wikipedia): for every triangular $n$ the bound
   is attained and the optimum **is already proven** — proven *by this very inequality*, and by
   nothing else.
3. `cited` + `numerical` (§2.3): for every **non-triangular $n \le 15$**, where $s(n)$ is known
   exactly, $s_{\mathrm{Oler}}(n) < s(n)$ with a gap of $0.37$ to $0.92$. Oler is strictly slack on
   every single one.

**So on the whole range where the answer is known, Oler is tight exactly on the already-solved
triangular numbers and slack everywhere else.**

### 5.0 The one place I must not overclaim

For $n \ge 16$ the optimum is *unknown*, so I cannot literally prove $s_{\mathrm{Oler}}(n) < s(n)$
there — that would require knowing $s(n)$. What is rigorous is the weaker statement, and it is
enough:

> For $n = 16, 17, 18$, the **best known construction** exceeds $s_{\mathrm{Oler}}(n)$ by
> $0.76$–$0.89$ (§2.3). Hence Oler could settle one of these $n$ **only if** the published best-known
> packing for it is beatable by roughly $0.8$ in side length — a record improvement of a size that
> three decades of Lubachevsky–Stillinger-style search (Melissen–Schuur 1995, Graham–Lubachevsky
> 1995) has not come close to producing.

That is `numerical`-grade evidence, not a proof, and it is labelled as such. But combined with
point 3 — where the pattern *is* proven, on all 10 non-triangular $n \le 15$ — the conclusion is not
in serious doubt.

**Sub-question that would make this rigorous.** Oler's CMB note says only that equality "is realized
for example" by the lattice subset; it gives **no characterisation of the equality case**. If the
Acta Math. paper characterises equality — plausibly: equality forces the point set to be a
triangular-lattice subset — then $s(n) > s_{\mathrm{Oler}}(n)$ for **all** non-triangular $n$ would
follow immediately and unconditionally, since $s_{\mathrm{Oler}}(n)$ is not a lattice-attainable side
length. Anyone with access to Acta Math. 105 (1961) 19–48 should check this; it is a cheap upgrade of
a `numerical` claim to a `cited` one.

**Consequence either way.** Oler's inequality **cannot, by itself, establish optimality for any $n$
whose optimum is currently unknown** — not unless a huge, universally-missed better packing exists.
Any real proof must close an $\approx 0.8$-wide window, and Oler contributes nothing inside it. This
matches the historical record in §3.2 exactly: no case after the triangular numbers was closed by
Oler, and the ones that were closed took a paper each.

### 5.1 Refinements I checked and which do **not** rescue it — `sketch`

**Status:** `sketch`, all of it. My own reasoning; not cross-examined; do not build on it.

- **Apply Oler to the convex hull $H$ instead of the triangle $T$.** This is strictly stronger in
  principle, and it is the first thing one reaches for. It gains **nothing** for $n \ge 3$: by
  Melissen's lemma (quoted in §3.2, `cited` via Tedeschi & Mackey) an optimal configuration contains
  all three vertices of $T$; the convex hull of a set containing the three corners of $T$ and
  contained in $T$ **is** $T$. So $A(H) = A(T)$ and $M(H) = M(T)$ on exactly the configurations that
  matter. To extract anything from the hull step one would need a *quantitative* "if a corner region
  is sparse then $A(H) \le A(T) - c$" lemma, which is a new argument, not a use of Oler.
- **Groemer's inequality instead.** Amore (arXiv:2212.12287) states Groemer's bound alongside Oler's
  and calls Oler's "tighter" for this setting. Switching to a weaker inequality does not help.
- **Integrality.** $n$ is an integer, so one may use $\lceil\cdot\rceil$. This changes nothing: the
  bound $n \le (a^2+3a+2)/2$ is already an inequality between an integer and a real, and rounding
  moves $s_{\mathrm{Oler}}$ by less than the gaps in §2.3.
- **Apply Oler to sub-regions.** This *is* live — it is how a case analysis would use it, as a
  counting bound on pieces of a dissection (essentially Melissen's method with Oler in place of
  pigeonhole). But then Oler is a subroutine inside a bespoke per-$n$ argument, which is precisely
  what §3.3 says the real cost is. It does not make Oler a lower-bound *method*.

---

## 6. Status of this attack

**`refuted` as an independent attack**, per `../../../../RULES.md` §6.3: the kill-criterion stated in
issue #17 was met, so this direction stops here rather than being re-scoped.

Retained as reference material. Anyone proposing a lower-bound / optimality direction for this
problem should read §2.2, §2.3 and §5 first — the specific thing not to do is propose "use Oler's
inequality to prove $s(n) \ge c$" for an open $n$.

### Reusable outputs

- $s(n) \ge 2\sqrt3 + \sqrt{8n+1} - 3$, valid for all $n$, equality iff $n$ triangular (`sketch`
  until cross-examined; see §2.2).
- The corrected attribution table in §3.1, including the finding that the Wikipedia/Friedman
  discrepancy flagged in `../../README.md` resolves in Wikipedia's favour.
- `oler_bound.py` — regenerates every number in §2.3 from stdlib Python, no dependencies.

### Open follow-ups this work surfaced (not claimed here)

1. Read Payan 1997 and settle whether $n = 20$ is actually proven or only sketched as extensible.
2. Read Joós 2021 and record what an optimality proof for a single $n$ costs in structure, as input
   to any future attempt at $n = 16$.
3. Correct the "best known only" table in `../../README.md` for $n = 7, 8, 11, 13, 14$ once PR #10
   lands.
4. **Cheapest of the four, and the only one that upgrades a status:** get Oler, *An inequality in the
   geometry of numbers*, Acta Math. **105** (1961) 19–48, and check whether it characterises the
   **equality case**. If it does, §5.0's `numerical` step becomes `cited` and the negative result
   becomes unconditional.
