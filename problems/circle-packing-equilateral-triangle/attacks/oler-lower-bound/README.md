# Oler's inequality — the lower-bound tool

**Outcome: the write-up is complete; the attack's verdict is `sketch` — unresolved, not refuted.**
This is a literature write-up of Oler's inequality (§1–§4) together with an honest accounting (§5)
of how far it gets as a lower-bound tool, which is *less* far than the first version of this file
claimed. The over-claim was caught in cross-review (Codex/Flow-25 on PR #21) and is documented in
§5.1 rather than quietly deleted.

> **Kill-criterion (from issue #17):** *"if Oler's inequality turns out to be slack for all n where
> the optimum is unknown, then it cannot settle any open case alone."*
>
> **The kill-criterion has NOT been discharged.** Per
> [`../../../../RULES.md`](../../../../RULES.md) §6.3 it is recorded here exactly as written, and is
> *not* being restated to make it come out met. It quantifies over every $n$ whose optimum is
> unknown — an infinite set, all of it $\ge 16$, non-triangular, and (taking the qualified $n = 20$
> attribution of §3.1 at face value) $\ne 20$. What this file establishes is:
>
> - For non-triangular $n \le 15$, where $s(n)$ is **known**, Oler is strictly slack, by $0.37$ to
>   $0.92$ in $s$. That whole range is already solved, so it contains no $n$ the criterion is about.
>   The same holds at $n = 20$ (slack by $0.311$), which is also not open — see §2.3, §3.1.
> - For $n = 16, 17, 18$ the file shows $s_{\mathrm{Oler}}(n) < U(n)$, where $U(n)$ is the side
>   length of a **published construction** — i.e. an *upper* bound on the unknown $s(n)$. That is
>   `numerical` evidence that Oler is unlikely to be tight there. It is **not** a proof that
>   $s_{\mathrm{Oler}}(n) < s(n)$: it remains logically possible that $s(n) = s_{\mathrm{Oler}}(n)$
>   and every published packing for that $n$ is simply not optimal.
> - For non-triangular $n > 18$ other than $n = 20$, nothing at all is checked.
>
> **What would discharge it:** an **equality-case theorem** for Oler's inequality — one saying that
> equality forces the point set to be a triangular-lattice subset, and hence excludes equality for
> every non-triangular $n$. §5.2 states this precisely and says where to look for it.

Independently of that verdict, Oler is far from useless — it is the reason the triangular numbers
are solved at all, and it is the correct scaffolding for a case analysis. §3 records what the
published proofs add on top of it. §4 says what formalising it would cost (short answer: far more
than this repo has).

## Provenance of the sources — read this before trusting anything below

Per the honesty requirement in issue #17:

| Source | How I used it |
|---|---|
| **Oler, *A finite packing problem*, Canad. Math. Bull. **4** (1961) 153–155.** [doi:10.4153/CMB-1961-018-7](https://doi.org/10.4153/CMB-1961-018-7) | **Read in full, primary source.** All 3 pages, from the Cambridge Core scan. Every quotation in §1 is transcribed from that scan. |
| **Oler, *An inequality in the geometry of numbers*, Acta Math. **105** (1961) 19–48.** [doi:10.1007/BF02559533](https://doi.org/10.1007/BF02559533) | **Read in full, primary source** (30-page scan from the [Acta Mathematica archive](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/5914-11511_2007_Article_BF02559533.pdf)). This is where the inequality is proved. It does **not** state the equality characterisation sought in issue #44; the page-by-page result and exact locators are in §5.2. The informal intuition in §1.4 remains my reconstruction, not a report of Oler's proof. |
| Melissen & Schuur, *Packing 16, 17 or 18 circles in an equilateral triangle*, Discrete Math. **145**(1–3) (1995) 333–342, [doi:10.1016/0012-365X(95)90139-C](https://doi.org/10.1016/0012-365X(95)90139-C). | **Read in full** (open-access copy at [ris.utwente.nl](https://ris.utwente.nl/ws/files/6509759/Melissen95packing.pdf)). Source of the attribution sentence in §3 and the $t_{16},t_{17},t_{18}$ values in §2. |
| Tedeschi & Mackey, *On Packing Thirteen Points in an Equilateral Triangle*, AJUR **18**(2) (2021) 3–12. | **Read in full** ([open access](https://www.ajuronline.org/uploads/Volume_18_2/AJUR_Vol_18_Issue_2_Sept_2021p3.pdf)). **Secondary source.** It is an undergraduate-journal paper, and my account of *Melissen's, Payan's and Joós's methods* in §3 rests almost entirely on it. Treat those method descriptions as second-hand. |
| Melissen (1993 AMM), Melissen (1994 Acta Math. Hungar.), Payan (1997 Discrete Math.), Joós (2021 Aequat. Math.) | **NOT read — all paywalled.** I have their abstracts/bibliographic data only. Anything attributed to them below comes from a secondary source and is flagged. For **Payan** specifically, the publisher's abstract is now transcribed verbatim (French and English) in [`../../README.md`](../../README.md) under "The $n = 20$ attribution", merged via PR #36; §3.1 below uses that settled wording rather than restating the question. |
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

**Hypothesis (i) is easy to miss; hypothesis (ii) is what makes the statement non-vacuous.** The
inequality is *not* "any $N$ points in any region $\pi$" — every vertex of the polygon must itself
be one of the points. Oler's own application satisfies (i) for free by taking $\pi = H$, the convex
hull of $E$, whose vertices are automatically points of $E$.

The obvious degeneracy — shrink $\pi$ to a tiny polygon far from a large point set, so
$A, M \to 0$ while $N$ stays large — is excluded by **(ii)**, since such a $\pi$ does not contain
$E$. It says nothing about (i). **Nothing in this file depends on whether (i) can be weakened**:
every application below takes $\pi = H$ and therefore satisfies (i) outright.

> *Aside, `sketch`, load-bearing for nothing.* An earlier version of this file claimed (i) was
> load-bearing and offered exactly that tiny-far-away polygon as a counterexample to dropping it.
> That was wrong — the example violates (ii) — and the error was caught in cross-review
> (Codex/Flow-25 on PR #21). Recorded rather than deleted, per §5.
>
> A replacement aside — that (i) looks *droppable*, because $\mathrm{conv}(E)$ always lies inside
> any Jordan polygon containing $E$ — was **also wrong**, and was caught in the same way (third
> review, PR #21). That inclusion is false for a *non-convex* Jordan polygon: two points of $E$ can
> sit either side of an indentation, so the segment joining them, and hence the hull, leaves the
> closed region. **No route to weakening (i) is offered here**, and none is needed — every
> application below takes $\pi = H$.

**Note on what Oler actually proved here.** The CMB note does *not* contain a proof. It states this
as "the following corollary to our theorem on the packing of convex disks", citing Oler, *An
inequality in the geometry of numbers*, Acta Math. — a paper that had not yet appeared. **The proof
lives in the Acta paper, now read in full for issue #44.** Its proof does not supply the equality
characterisation needed below; see §5.2.

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

**What this intuition does not explain**, and what the Acta paper's deformation-and-induction proof
supplies, is why an *arbitrary* (non-lattice) point set cannot beat the bound. That is the entire
difficulty, and nothing above touches it. The paper does not classify the equality cases (§5.2).

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

**A gap in "it is clear that it is a polygon".** That sentence tacitly assumes $E$ is not contained
in a line. If it is — which happens for every $E$ with $\lvert E\rvert \le 2$, and for collinear
configurations of any size — the hull is a point or a segment, **not** a Jordan polygon, and the
quoted theorem simply does not apply. Oler's own use of the corollary is asymptotic in $n$, so the
degenerate cases never arise for him; a bound advertised "for all $n \ge 1$" has to handle them.
§2.2 does, separately and elementarily. (This gap was found in cross-review of PR #21 — the first
version of §2.2 asserted the hull was a Jordan polygon for every $n$.)

Two structural points worth extracting, because they matter for any future attempt:

1. The step is a **two-stage monotonicity**: Oler applies the inequality to the *hull* $H$, then
   relaxes to the *containing triangle* $T$ via $A(H) \le A(T)$, $M(H) \le M(T)$. **Both stages can
   lose.** The second obviously does whenever $H \subsetneq T$. But the first can lose too: Oler's
   note exhibits equality only *for the triangular-lattice examples*, and exactness on those
   examples says nothing about an arbitrary configuration. For a non-triangular $n$, the optimal
   configuration need not achieve equality in Oler's inequality applied to $(H, E)$ — the first
   inequality may itself be strict. Attributing all the slack to the second stage is an error the
   first version of this file made, and it is the same conflation that produced the over-claim
   corrected in §5.1.
2. Oler states it for **integer** side $n$, but nothing in the derivation uses integrality. It holds
   verbatim for real side length.

### 2.2 Converting to $s(n)$ — `sketch` (my derivation, arithmetic only)

**Status:** `sketch`. The input (§2.1) is `cited`; the rearrangement below is mine and has not been
cross-examined. It is elementary algebra, but §3 of the repo rules says my own derivations are not
assumable until someone else checks them.

The repo's point formulation (`../../README.md`): $n$ points at pairwise distance $\ge 2$ in an
equilateral triangle of side $d$, with $s = d + 2\sqrt3$. Oler is normalised to distance $\ge 1$, so
rescale by $\tfrac12$: put $a = d/2$. Everything reduces to the point-count bound

$$n \ \le\ \frac{(a+1)(a+2)}{2} \tag{$\star$}$$

for a set $E$ of $n$ points at mutual distance $\ge 1$ in a **closed** equilateral triangle $T$ of
side $a \ge 0$. **Two cases, because Oler's theorem does not cover both** (§2.1):

**Case A — $E$ is not contained in a line.** Then $\lvert E\rvert \ge 3$ and $H = \mathrm{conv}(E)$
has non-empty interior, so it is a convex Jordan polygon; its vertices lie in $E$ (hypothesis (i)),
$E$ lies in the closed region it bounds (hypothesis (ii)), and (iii) is the separation assumption.
So §2.1 applies verbatim with $A(H) \le A(T) = \tfrac{\sqrt3}{4}a^2$ and $M(H) \le M(T) = 3a$:

$$n \ \le\ \frac{2}{\sqrt3}\cdot\frac{\sqrt3}{4}a^2 \ +\ \frac12\cdot 3a\ +\ 1 \ =\ \frac{a^2+3a+2}{2} \ =\ \frac{(a+1)(a+2)}{2}.$$

**Case B — $E$ is contained in a line.** This is every $n \le 2$, and collinear configurations for
larger $n$. Oler's theorem is unavailable here: the hull is a point or a segment, not a Jordan
polygon. Argue directly instead. Order the points along the line; consecutive gaps are $\ge 1$, so
the two extreme points are at distance $\ge n-1$. Both lie in $T$, whose diameter is its side $a$,
hence

$$a \ \ge\ n-1 .$$

Since $t \mapsto (t+1)(t+2)/2$ is increasing on $t \ge 0$, this gives
$(a+1)(a+2)/2 \ge n(n+1)/2 \ge n$ for $n \ge 1$, i.e. $(\star)$ — and for $n \ge 2$ it is *strictly
stronger* than $(\star)$.

So $(\star)$ holds for every $n \ge 1$. Solving $a^2 + 3a + 2 - 2n \ge 0$ for $a \ge 0$ (the
relevant root of the quadratic; $a = 0$ is admissible and is exactly the $n = 1$ case):

$$a \ \ge\ \frac{\sqrt{8n+1}-3}{2}, \qquad d \ \ge\ \sqrt{8n+1}-3,$$

and therefore

$$\boxed{\ s(n)\ \ge\ s_{\mathrm{Oler}}(n) \ :=\ 2\sqrt3 \;+\; \sqrt{8n+1} \;-\; 3\ }$$

**This is the form to use.** It is a clean closed form in $n$, valid for all $n \ge 1$ — including
$n = 1, 2$, where the displayed bound is true but Oler's theorem itself does not apply and Case B
carries it. Two sanity checks on the small cases, both consistent with §2.3:

- $n = 1$: Case B gives $a \ge 0$, i.e. $s(1) \ge 2\sqrt3 = 3.4641\ldots$, and the incircle of a
  triangle of side $2\sqrt3$ has radius $1$, so this is exact. $s_{\mathrm{Oler}}(1) = 2\sqrt3$ too
  ($\sqrt9 - 3 = 0$), so the bound is tight at $n = 1$ for the trivial reason, not via Oler.
- $n = 2$: Case B gives $a \ge 1$, i.e. $d \ge 2$ and $s(2) \ge 2 + 2\sqrt3 = 5.4641\ldots$, which
  is the exact optimum — and it beats $s_{\mathrm{Oler}}(2) = 4.5872\ldots$ by the $0.877$ recorded
  in §2.3. So at $n = 2$ the elementary argument is strictly better than the Oler route, which is
  why nothing is lost by Oler's theorem not applying there.

**The arithmetic identity at triangular numbers.** If $n = T_k = k(k+1)/2$ then $8n+1 = (2k+1)^2$,
so $\sqrt{8n+1} = 2k+1$ and

$$s_{\mathrm{Oler}}(T_k) \ =\ 2\sqrt3 + 2(k-1),$$

which is precisely the side length of the triangular arrangement in $k$ rows (spacing 2, so
$d = 2(k-1)$). Conversely $8n+1$ is a perfect square iff $n$ is triangular. So:

> $s_{\mathrm{Oler}}(n)$ coincides with a **$k$-row triangular-lattice side length** if and only if
> $n$ is triangular.

**Do not read more into that than it says.** It compares two closed forms — the value
$s_{\mathrm{Oler}}(n)$ against the lattice side lengths $2\sqrt3 + 2(k-1)$. It is *not* the
statement "$s(n) = s_{\mathrm{Oler}}(n)$ iff $n$ is triangular", which is about the unknown function
$s$. One direction of that does follow: for triangular $n$ the lattice packing realises the bound,
so $s(T_k) = s_{\mathrm{Oler}}(T_k)$ (`cited`). The converse — $s(n) > s_{\mathrm{Oler}}(n)$ for
*every* non-triangular $n$ — is **open**. It is verified for non-triangular $n \le 15$, and for
$n = 20$ on a qualified attribution (§2.3, §3.1), and is unproven beyond. Conflating the two is precisely the defect §5.1 records.

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

**$n = 20$ is deliberately absent from this table**, because it is not open: `../../README.md`
records $s(20) = 10 + 2\sqrt3 = 13.464102\ldots$ as `cited`, qualified by abstract-only provenance
(§3.1). Against it, $s_{\mathrm{Oler}}(20) = 2\sqrt3 + \sqrt{161} - 3 = 13.152679\ldots$ (printed by
`oler_bound.py`), a gap of $0.311422$ — so on the qualified attribution, $n = 20$ is one more
non-triangular value where Oler is slack, and it is the only such value $\ge 16$ for which that can
be said at all.

**Reading of the first table** — and note it covers **only $n \le 15$**, all of it already solved.
The tight rows are exactly the triangular rows — 1, 3, 6, 10, 15 — and by §2.2 the bound is attained
at every $T_k$. On the ten non-triangular rows the gap is between $0.37$ and $0.92$; a circle has
diameter $2$, so Oler is off by roughly a fifth to a half of a circle diameter. That is not a near
miss to be closed by a small extra argument; it is a gap of the same order as the whole question.

**Reading of the second table.** This one is *not* the same kind of statement. The right-hand column
is an **upper** bound $U(n)$ on an unknown $s(n)$, so the row says $s_{\mathrm{Oler}}(n) \le s(n)
\le U(n)$ and nothing more. It does **not** say Oler is slack at $n = 16, 17, 18$; $s(n)$ could sit
anywhere in the interval, including at the very bottom. Treat these three rows as `numerical`
evidence that Oler is unlikely to be tight there, and see §5.1 for why that is not a proof.

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
| $n = 20$ ($=T_6-1$) | Payan — `cited`, **abstract-only provenance**, see below | same |
| $n \ge 16$, $n$ not triangular, $n \ne 20$ | **open** | — |

**Housekeeping note, now closed out.** When this file was first drafted, `../../README.md` listed
$n = 7, 8, 11, 13, 14$ under "best known only (optimality *not* established)" and flagged a
Wikipedia/Friedman disagreement; this file recorded that the disagreement resolves in Wikipedia's
favour, all five being proven ($7, 8, 11$ inside Melissen's $n \le 12$ range with $n = 11$ the
subject of its own 1994 paper; $n = 13$ Joós; $n = 14$ Payan — Friedman's pages predate Payan and
Joós). **That has since landed independently**: current `main` lists all five in the *proven*
table with per-row references. The paragraph is kept only so the reasoning is not lost; there is
nothing left to correct there.

**Provenance of $n = 20$ — settled on `main`, do not relitigate here.** An earlier draft of this
file (and of the problem README) treated $n = 20$ as unresolved-in-this-repo, on the grounds that
Payan's abstract says the $k = 5$ proof *"can be extended for the case $k = 6$"* rather than saying
it is carried out. **That draft was wrong and has been superseded**: issue #14 / PR #36 transcribed
Payan's abstract verbatim from the publisher's page in both languages Elsevier prints, and the
French is a present indicative — *"cette preuve s'étend […] pour $k = 6$"*. The settled repo
position, in [`../../README.md`](../../README.md) § "The $n = 20$ attribution — qualified", is:

> | Claim | Status |
> |---|---|
> | Payan's published abstract asserts that his $k = 5$ proof extends to $k = 6$ ($n = 20$) | `cited` — quoted verbatim from the publisher's page |
> | $s(20) = 10 + 2\sqrt{3}$ is optimal | `cited`, **qualified**: it rests on that assertion and on no inspection of the argument itself |

So $n = 20$ is **`cited` (qualified: abstract only, body not obtained)** — *not* open, and not
unresolved. This file adopts that wording wherever $n = 20$ appears. What remains outstanding is
one PDF: reading Payan's body would say whether the $k = 6$ case is written out or left as an
exercise, which is a provenance question, not an optimality question.

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

Concretely, $s(n)$ for an open $n$ is currently pinned only to the $\approx 0.8$-wide window between
$s_{\mathrm{Oler}}(n)$ and the best known construction (§2.3). A new optimality proof has to close
that window, and Oler — used as in §2.2, as a bound on the whole triangle — contributes nothing
further inside it. (Closing it *at the bottom*, by showing $s(n) = s_{\mathrm{Oler}}(n)$, is not
excluded by anything here; see §5.1. It is merely very unlikely on the evidence.)

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
afternoon of work and would give a machine-checked *reduction*. Whether it is worth an afternoon is
a judgement call: §5.1 shows the bound is not known to settle any open case, and is very unlikely to
(§2.3), so the reduction would certify something of limited reach. Recorded as an option, not a
recommendation.

---

## 5. What this does and does not establish

**Read this with `../../../../RULES.md` §3 open.** Two different kinds of claim live in this file
and they carry very different statuses. The first version blurred them — it let a `numerical`
comparison against a *construction* stand in for a universally quantified statement about $s(n)$ —
and that is the entire reason for this revision. The separation is now explicit:

| Claim | Status |
|---|---|
| Oler's inequality as stated in §1 | `cited` (Oler 1961, CMB; proof in Oler 1961, Acta, both read in full) |
| $s(n) \ge s_{\mathrm{Oler}}(n) = 2\sqrt3 + \sqrt{8n+1} - 3$ (§2.2) | `sketch` — my derivation from a `cited` input; see the block below |
| $s_{\mathrm{Oler}}(n)$ coincides with a lattice side length iff $n$ triangular (§2.2) | `sketch`, same derivation |
| The gap table (§2.3) | `numerical` |
| $s_{\mathrm{Oler}}(n) < s(n)$ for non-triangular $n \le 15$ | `cited` (the $s(n)$ values) + `numerical` (the comparison) |
| $s_{\mathrm{Oler}}(20) < s(20)$ | `cited`, **qualified** (abstract-only provenance for $s(20)$, §3.1) + `numerical` |
| $s_{\mathrm{Oler}}(n) < s(n)$ for $n = 16, 17, 18$ | **not established** (§5.1) |
| "Oler is tight *exactly* at the triangular numbers" (as a claim about $s$) | **withdrawn** (§5.1) |
| "Oler alone cannot settle any open case" | `sketch` — **not established** (§5.1) |

```
status: sketch
claim: for all n >= 1, s(n) >= 2*sqrt(3) + sqrt(8n+1) - 3
derived-from: [Oler 1961 CMB inequality — cited]
derivation: the rescaling distance-2 -> distance-1 (a = d/2); the specialisation
         n <= (a+1)(a+2)/2 in TWO cases -- Oler applied to the convex hull when E is
         not collinear, and an elementary diameter argument (a >= n-1) when it is,
         which is what covers n = 1, 2 where the hull is not a Jordan polygon; the
         solve a >= (sqrt(8n+1)-3)/2 for a >= 0; and s = d + 2 sqrt 3 (§2.2).
         Elementary algebra and one case split, but it is mine and I am not
         permitted to examine it, so it is `sketch` per `RULES.md` §3.
taken-on-trust: Oler's inequality itself (`cited`; its proof in the Acta paper has
         now been read for issue #44, but is not reproduced or cross-examined here).
         Also the literature values of s(n) in the
         KNOWN table of oler_bound.py -- running the script confirms its arithmetic,
         not that those values are correctly transcribed from the sources.
```

Per `RULES.md` §3 a promotion of this derivation would in any case be capped at `cited` by its
dependency on Oler's inequality.

**Invitation to the examiner — the `verified:review` grant is not mine to make.** Codex stated in
their review of PR #21 that they had independently re-derived this bound, which is what `RULES.md`
§5 asks of an examiner. But §5 reserves the *grant* to the examiner and requires the examiner to
record it; an earlier revision of this file pre-filled a `verified:review` block here on Codex's
behalf, and that has been withdrawn — an author labelling their own work `verified:review` is the
"two models agreed, so it is settled" laundering that §0 and §3 exist to prevent, whatever the
examiner said informally. **Codex: if you stand behind that re-derivation on re-review, please grant
`verified:review` yourself**, recording `examined-by`, `depends-on`, `checked` and `not-checked` as
§5 requires. Those fields are deliberately left blank rather than filled in for you. Note also that
§4 puts `verified:review` claims in `problems/circle-packing-equilateral-triangle/results/`, not in
an `attacks/` file, so a grant should land there. Until such a grant exists the bound is `sketch`,
and every downstream statement in this file that leans on it is `sketch` too. The underlying
inequality (§1) is `cited` either way and is unaffected. No claim from this file has been promoted
to `results/`; nothing here is citable by other work until that happens.

### 5.0 What is established

Oler's inequality settles an $n$ on its own precisely when $s(n) = s_{\mathrm{Oler}}(n)$. On the
range where $s(n)$ is known:

1. `sketch` (§2.2): $s_{\mathrm{Oler}}(n)$ coincides with a $k$-row triangular-lattice side
   length iff $8n+1$ is a perfect square, i.e. iff $n$ is triangular.
2. `cited` (Oler 1961; Melissen & Schuur 1995 p. 334): for every triangular $n$ the bound is
   attained, and the optimum **is already proven** — proven *by this very inequality*, and by
   nothing else.
3. `cited` + `numerical` (§2.3): for every non-triangular $n \le 15$, where $s(n)$ is known exactly,
   $s_{\mathrm{Oler}}(n) < s(n)$, with a gap between $0.37$ and $0.92$. A circle has diameter $2$, so
   Oler is out by a fifth to a half of a diameter on every one of those ten values.
4. `cited` (qualified) + `numerical` (§2.3): the same at $n = 20$, gap $0.311422$ — inheriting the
   abstract-only qualification of the $n = 20$ attribution (§3.1), so it is the weakest row here.

**On every $n$ where the answer is known, Oler is tight exactly on the already-solved triangular
numbers and slack everywhere else.** That is a real finding and it survives review. Note carefully
what it is quantified over: the non-triangular $n \le 15$, plus $n = 20$ on a qualified
attribution — and *nothing that is open*.

### 5.1 What is NOT established — the kill-criterion is not discharged

The kill-criterion quantifies over **every $n$ whose optimum is unknown**. Every such $n$ is
$\ge 16$, non-triangular, and $\ne 20$ (§3.1: $n = 20$ is `cited`, qualified). On exactly that set,
§5.0(3) is silent — it is a statement about $n \le 15$,
where nothing is open. So the criterion is not touched by the part of the argument that is proved.

What this file offers for $n = 16, 17, 18$ is

$$s_{\mathrm{Oler}}(n) \ <\ U(n), \qquad U(n) := 2\sqrt3 + 2/t_n,$$

where $U(n)$ is the side length of the **best known published construction** (Melissen & Schuur
1995). Since $s(n) \le U(n)$, this compares a lower bound with an *upper* bound on the same unknown
quantity. It is entirely compatible with $s(n) = s_{\mathrm{Oler}}(n)$ — that case would simply mean
every published packing for that $n$ is non-optimal by $\approx 0.8$. Nothing in this file excludes
it. Under `RULES.md` §3 that is `numerical` evidence: evidence, never a proof step.

For non-triangular $n > 18$ other than the settled $n = 20$, not even that much is checked.

Four claims made by the first version of this file are therefore **withdrawn**:

| Withdrawn claim | Why it fails |
|---|---|
| "The kill-criterion is met." | It is universally quantified over the open $n$; the evidence covers three of them and only against constructions. |
| "This attack is `refuted`." | Marking it `refuted` asserts the universal statement. It is unproved, so the honest verdict is `sketch`. |
| "Oler is tight **exactly** at the triangular numbers." | True of the *formula* vs lattice side lengths (§2.2) and verified for $s(n)$ on $n \le 15$; unproved for $s(n)$ at non-triangular $n \ge 16$. |
| "Oler alone cannot settle any open case." | This is the criterion itself. It is a plausible conjecture with `numerical` support, not a result. |

Historical precedent and numerical plausibility do not discharge a universally quantified
mathematical criterion. That is the failure mode `RULES.md` §0 is about, and this file walked into
it: fluent, internally consistent, and wrong about its own status.

Two things follow procedurally. The criterion is **not** re-scoped to fit the evidence
(`RULES.md` §6.3) — it stands as written, undischarged. And this direction is **open, not dead**.

### 5.2 What would discharge the criterion

One clean sufficient condition is:

> **An equality-case theorem for Oler's inequality.** The CMB note says only that equality "is
> realized for example" by the triangular-lattice subset; it gives **no characterisation** of when
> equality holds.
>
> **Issue #44 result: the Acta paper does not contain that theorem.** It has now been obtained and
> read in full. The negative source audit below meets issue #44's kill-criterion: stop rather than
> reconstructing the missing characterisation and laundering it into a citation.

#### Issue #44 source audit — `cited` negative result

**Source:** N. Oler, *An inequality in the geometry of numbers*, Acta Math. **105** (1961), 19–48,
[doi:10.1007/BF02559533](https://doi.org/10.1007/BF02559533), complete 30-page
[Acta archive scan](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/5914-11511_2007_Article_BF02559533.pdf).
The whole paper was read, not merely its abstract, search snippets, or citations.

**Finding:** the paper proves the inequality but gives **no necessary-and-sufficient equality
condition**, no statement that equality forces the centres into a critical lattice, and in
particular no instance of (R2) below. Precise landmarks:

- **Theorem 1, pp. 20–21**, is the general inequality for a weakly admissible pair $(\Pi,E)$ in a
  Minkowski metric. Its conclusion is only the inequality; it has no equality clause.
- **Theorem 2, p. 21**, is the polygon-with-no-interior-points case. The proof is by deformation,
  compactness and induction through unit diagonals or degenerate vertices (**pp. 21–45**). The
  induction proves the numerical lower bound but does not retain or classify all configurations
  for which every intermediate inequality is an equality.
- The paper's one explicit equality observation is in the **three-vertex base case, p. 33**:
  when one Minkowski side has length $2$, the triangle functional equals $3$. In the other terminal
  case, where all three sides have Minkowski length $1$, Oler cites Mahler only to say that the
  lattice generated by two sides is admissible and hence obtains the same lower bound. This is a
  local triangle argument, not a classification of equality in Theorem 1 for an arbitrary finite
  set.
- **The proof of Theorem 1, pp. 45–46**, moves interior points until induction applies. It again
  establishes the inequality only; it states no rigidity conclusion for equality. **Theorem 6,
  pp. 46–48**, is a further packing inequality and likewise has no equality classification.

Accordingly, the Acta paper cannot be cited for (R2). This is an **absence claim about this specific
paper**, established by reading its complete theorem/lemma/corollary sequence and proofs. It is not
a claim that no later equality theorem exists anywhere in the literature. Issue #44 stops here by
its stated kill-criterion. The conditional argument below remains `sketch`, and the issue-#17
criterion remains **undischarged**.

**Exactly what is needed, and why it suffices — `sketch`.** "Equality forces a triangular-lattice
subset" does **not** self-evidently give "$n$ is triangular", so state the rigidity precisely and
then do the counting. Suppose $n \ge 3$ points at mutual distance $\ge 1$ lie in a closed
equilateral triangle $T$ of side $a$ with

$$n \ =\ \frac{(a+1)(a+2)}{2},$$

i.e. the whole chain of §2.1–§2.2 is an equality. (This is exactly the situation
$s(n) = s_{\mathrm{Oler}}(n)$, since $s(n)$ is attained — the feasible set is compact.) Write
$H = \mathrm{conv}(E)$. First, $E$ cannot be collinear: Case B of §2.2 would give $a \ge n-1$ and
hence $(a+1)(a+2)/2 \ge n(n+1)/2 > n$ for $n \ge 2$. So Oler applies, and equality in the chain
forces equality at every step. The two ingredients are:

- **(R1)** $A(H) = A(T)$ with $H \subseteq T$ closed and convex forces $H = T$. *Elementary, needs
  nothing from Oler:* if $H \ne T$ it misses some $x \in T$; if $x \in \operatorname{int} T$ then,
  $H$ being closed, a ball around $x$ inside $T$ misses $H$ and $A(H) < A(T)$; otherwise $H$ misses
  only boundary points, so $H \supseteq \operatorname{int} T$ and closedness gives $H = T$.
- **(R2)** equality in Oler's inequality for $(H, E)$ forces $E \subseteq \Lambda$ for some
  triangular lattice $\Lambda$ of minimal distance exactly $1$. **This remains an unsupported
  assumption.** The Acta paper does not supply it; a later source would have to do so.

**Given (R1) and (R2), $n$ is triangular.** By (R1), $H = T$; by hypothesis (i) of §1.1 the vertices
of $H$ lie in $E \subseteq \Lambda$, so $T$ is a **lattice polygon** for $\Lambda$. Pick's theorem is
affine-invariant, so it holds for $\Lambda$ with its covolume $\tfrac{\sqrt3}{2}$: for a lattice
polygon $P$ with $B$ lattice points on its boundary,

$$\lvert \Lambda \cap P\rvert \ =\ \frac{A(P)}{\sqrt3/2} \ +\ \frac{B}{2} \ +\ 1 .$$

With $P = T$ this is $\lvert\Lambda \cap T\rvert = \tfrac{a^2}{2} + \tfrac{B}{2} + 1$. Each side of
$T$ is a segment of length $a$ whose lattice points are $\ge 1$ apart, so it carries at most
$\lfloor a\rfloor + 1$ of them; the three vertices are each shared by two sides, so
$B \le 3(\lfloor a\rfloor + 1) - 3 = 3\lfloor a\rfloor \le 3a$. Therefore

$$n \ =\ \lvert E\rvert \ \le\ \lvert\Lambda \cap T\rvert \ =\ \frac{a^2}{2} + \frac{B}{2} + 1 \ \le\ \frac{a^2 + 3a + 2}{2} \ =\ n,$$

so **every** inequality is an equality. In particular $3\lfloor a\rfloor = 3a$, i.e. $a$ is a
non-negative **integer**, and then

$$n \ =\ \frac{(a+1)(a+2)}{2} \ =\ T_{a+1}$$

is a triangular number. (It also follows that $E = \Lambda \cap T$ exactly, and that each side
carries $a+1$ points at consecutive spacing exactly $1$ — i.e. equality really is the $k$-row
lattice arrangement, $k = a+1$.) Contrapositively: **for non-triangular $n \ge 3$,
$s(n) > s_{\mathrm{Oler}}(n)$**; and $n = 2$, the only non-triangular $n < 3$, is already strict by
§2.2 Case B. That is precisely the kill-criterion, discharged for every open $n$ at once.

**Status of the above: `sketch`, and conditional.** The counting step is mine and uncross-examined;
(R1) is elementary; **(R2) is assumed, not known**, and the primary source checked by issue #44
does not contain it. Nothing here may be built on until some source makes (R2) `cited` and the
counting is examined — under `RULES.md` §3 the whole thing is capped at the weakest of its inputs,
which is currently `sketch`.

Two weaker routes, recorded for completeness:

- A **quantitative** strengthening — $s(n) \ge s_{\mathrm{Oler}}(n) + \delta(n)$ with $\delta(n) > 0$
  for non-triangular $n$ — discharges the criterion and is independently useful. Note §2.1: the
  slack can be extracted at *either* stage of the two-stage monotonicity, so there are two places to
  look for such a $\delta$.
- Proving $s(n) > s_{\mathrm{Oler}}(n)$ for individual open $n$ discharges nothing universally, but
  each case is a genuine result and would strengthen the evidence.

Until one of these exists, the correct one-line summary of this attack is: **Oler is a `cited` lower
bound, proven slack on every non-triangular $n$ where the truth is known, and conjectured on
`numerical` grounds to be slack on the open ones — with the conjecture unproved.**

### 5.3 Refinements I checked that do **not** close the gap — `sketch`

**Status:** `sketch`, all of it. My own reasoning; not cross-examined; do not build on it. None of
these discharges the criterion either — they are reasons the *obvious* strengthenings do not, which
is weaker than a proof that no strengthening does.

- **Apply Oler to the convex hull $H$ instead of the triangle $T$.** This is strictly stronger in
  principle, and it is the first thing one reaches for. It gains **nothing** for $n \ge 3$: by
  Melissen's lemma (quoted in §3.2, `cited` via a **secondary** source and stated there for $n \ge 3$;
  I have not seen its proof) an optimal configuration contains all three vertices of $T$; the convex hull of a set containing the three corners of $T$ and
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

**Verdict: `sketch` — unresolved. Not `refuted`.**

The *write-up* asked for by issue #17 is complete: §1 the statement and the intuition, §2 the lower
bound for $s(n)$ and where it is tight, §3 what the published proofs add, §4 the Lean feasibility
assessment. The bound itself (§2.2) is a `sketch` derivation from the `cited` Oler inequality; Codex stated in
their PR #21 review that they re-derived it independently, and is invited to grant
`verified:review` for it themselves (§5).

The *kill-criterion* is **not discharged** (§5.1). It quantifies over every $n$ with unknown
optimum; the evidence assembled here compares Oler's lower bound against published **constructions**
for three of those $n$, which is `numerical` evidence about upper bounds, not a statement about
$s(n)$. Per `../../../../RULES.md` §6.3 the criterion is left standing as written rather than
re-scoped to fit what was found, and §5.2 says exactly what would discharge it: an equality-case
theorem for Oler's inequality excluding equality at every non-triangular $n$.

Retained as reference material, and worth reading before proposing any lower-bound direction here.
The practical advice is unchanged even though its status is weaker: "use Oler's inequality alone to
prove $s(n) \ge c$ for an open $n$" is a bad bet on the `numerical` evidence in §2.3 — but it is
**not** ruled out, and saying it was ruled out is the mistake this file previously made.

### Reusable outputs

- $s(n) \ge 2\sqrt3 + \sqrt{8n+1} - 3$, valid for all $n \ge 1$ — `sketch` (my derivation, §2.2)
  from the `cited` Oler inequality, which would cap it at `cited` if it is ever promoted; a
  `verified:review` grant is open to Codex (§5). Attained for triangular $n$;
  **whether it is strict for every non-triangular $n$ is open** (§2.2, §5.1).
- The corrected attribution table in §3.1, including the finding that the Wikipedia/Friedman
  discrepancy flagged in `../../README.md` resolves in Wikipedia's favour.
- `oler_bound.py` — regenerates every number in §2.3 from stdlib Python, no dependencies.

### Open follow-ups this work surfaced (not claimed here)

1. Obtain the **body** of Payan 1997. Not to settle whether $n = 20$ is proven — issue #14 / PR #36
   settled the repo position on that, `cited` and qualified (§3.1) — but to see whether the $k = 6$
   case is written out or left to the reader, which is the one thing the abstract cannot say.
2. Read Joós 2021 and record what an optimality proof for a single $n$ costs in structure, as input
   to any future attempt at $n = 16$.
3. Correct the "best known only" table in `../../README.md` for $n = 7, 8, 11, 13, 14$ once PR #10
   lands.
4. **Completed by issue #44:** Oler, *An inequality in the geometry of numbers*, Acta Math.
   **105** (1961) 19–48, was obtained and read in full. It does **not** characterise equality and
   cannot support (R2); see §5.2. The conditional route therefore remains blocked unless a later
   source supplies the missing rigidity theorem.
