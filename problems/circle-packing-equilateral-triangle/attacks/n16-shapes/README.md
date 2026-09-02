# Attack: does *shape* buy anything for the 15-piece covering bound at $n = 16$?

**Claim type ([`../../RULES.md`](../../RULES.md) §1): optimality / lower bound.** This file
asserts $s(16) \ge c$ for an explicit $c$. It claims **no** packing and nothing enters
`results/`.

- Author: `claude` (Claude Opus 5), worker **C2**, 2026-08-22.
- Kill-criteria, written before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md).
- Code: [`experiments/packing-n16-shapes/`](../../../../experiments/packing-n16-shapes/) —
  Python standard library plus nothing; exact `Fraction` arithmetic in every decision.
- Builds on (does not modify): [`../n16-covering/`](../n16-covering/), the standing record.

| What | Status |
|---|---|
| §2 Lemma S (the $60^\circ$ corner sector has diameter exactly $r$) | `sketch` — mine, three lines, exact |
| §2 Lemma C (a corner piece of diameter $D$ has area $< \pi D^2/6$) | `sketch` — mine, two lines, exact |
| §3 **Theorem SI (shape irrelevance)** | `sketch` — mine; elementary, no compute |
| §4 audit of the standing certificate (per-piece areas, loss decomposition) | `numerical`, exact rational arithmetic |
| §5 area ceilings | `sketch` — mine, arithmetic from Lemma C + the isodiametric inequality |
| §6 the new certificates | `numerical` (exactly verified, same-family only) |
| $s(16) \le 12.713629$ (Melissen–Schuur 1995) | `cited` — [`../../README.md`](../../README.md) |

---

## 0. Kill-criterion outcome, stated up front

> **K0 (shape-freedom triviality) FIRED, and it is the finding.** Both reductions I named in
> advance are valid, so **shape freedom is worth exactly zero here**:
>
> > For every $a$ and every $N$: $T_a$ can be covered by $N$ sets of diameter $<1$ **iff** it
> > can be covered by $N$ *convex polygons* of diameter $<1$ (§3, Theorem SI).
>
> Sectors, Reuleaux and other constant-width pieces, disks, non-convex L-/crescent pieces and
> disconnected pieces therefore **cannot beat a convex-polygon covering at any side length at
> all** — not asymptotically, not in the limit: at the *same* $a$. The convex restriction that
> every previous attack in this repo imposed was not a restriction.
>
> **K1 (no-improvement) did NOT fire**, but the improvement came from the *one* freedom Theorem SI
> leaves open — **overlap** (equivalently, partitions into non-convex cells) — plus more search,
> and it is small: $a_{16} \ge 4463841021/10^9 = 4.463841021$ (exactly certified, §6.3)
> against the standing $446335/99998 = 4.4634392688$ — a gain of $4.0\times10^{-4}$.
>
> **K2 (plateau)**: the plateau is confirmed. Runs from a different representation, with and
> without the overlap freedom, all land in $[4.4634, 4.4640]$.
>
> **K3 (§7 tripwire) did NOT fire.** Nothing here approaches $4.6247636$; the best is $3.6\%$
> below it.

**One-line answer to the question I was set:** the remaining $0.161$ of gap at $n=16$ is
**not shape-fixable**, because there is no shape to fix — every shape is a polygon for this
purpose. What is left is the *arrangement*, and the largest single named inefficiency (the
corners) is worth at most $\approx 0.018$ of it.

---

## 1. The mechanism, and the two things that make it delicate

> If $T_a$ is covered by 15 sets each of diameter **strictly** $<1$, then 16 points at pairwise
> distance $\ge 1$ cannot lie in $T_a$: two of them would share a piece and be $<1$ apart. Hence
> $a_{16} \ge a$, and $s(16) = 2a_{16} + 2\sqrt3$.

Two standing traps, both recorded because they have each already broken something in this repo:

1. **Strictness.** Separation here is *non-strict* (`../../RULES.md` §2), so a piece of diameter
   exactly 1 destroys the pigeonhole. This is what broke Lemma L.
2. **Overlap kills the area argument.** The standing certificate proves coverage from
   "pieces $\subseteq T_a$ + pairwise interior-disjoint + areas sum to $|T_a|$". As soon as pieces
   overlap that inference is void — an overlap plus an equal-area hole passes it. Every
   certificate here is checked by **direct exact polygon difference** instead (§6).

**Scaling is free and must be taken.** A certificate at side $a$ whose pieces have exact maximum
squared diameter $S < 1$ proves $a_{16} \ge a/\sqrt S$, not $a_{16}\ge a$: for every rational
$\lambda < 1/\sqrt S$ the dilated pieces still have diameter $<1$ and cover $T_{\lambda a}$, so
$a_{16} > \lambda a$ for all such $\lambda$, hence $a_{16} \ge a/\sqrt S$. Applied to the standing
certificate ($a = 89267/20000$, $S = 2499900001/2500000000$, i.e. $\max\operatorname{diam} =
49999/50000$) this reads

$$a_{16} \;\ge\; \frac{89267}{20000}\cdot\frac{50000}{49999} \;=\; \frac{446335}{99998}
\;=\; 4.4634392687\ldots$$

which is the number to beat, and the one used throughout below.

---

## 2. The corner, exactly

Put the corner $V$ at the origin with the two sides of $T_a$ along the rays $\theta = 0$ and
$\theta = \pi/3$, and let $S(V,r) = \{(\rho,\theta) : 0\le\rho\le r,\ 0\le\theta\le\pi/3\}$ be the
circular sector of radius $r \le a$.

> **Lemma S.** $\operatorname{diam} S(V,r) = r$ exactly.
>
> *Proof.* For $p = (\rho_1,\theta_1)$, $q = (\rho_2,\theta_2)$ in $S$ we have
> $|\theta_1-\theta_2| \le \pi/3$, so $\cos(\theta_1-\theta_2) \ge \tfrac12$ and
> $$|p-q|^2 \;=\; \rho_1^2+\rho_2^2-2\rho_1\rho_2\cos(\theta_1-\theta_2)
> \;\le\; \rho_1^2+\rho_2^2-\rho_1\rho_2 \;=\; f(\rho_1,\rho_2).$$
> $f$ is convex in each variable separately, so on $[0,r]^2$ it is maximised at a corner of the
> square: $f(0,0)=0$, $f(r,0)=f(0,r)=f(r,r)=r^2$. Hence $\operatorname{diam} S \le r$. The two arc
> endpoints are at angle exactly $\pi/3$ and radius $r$, at distance $\sqrt{r^2+r^2-r^2}=r$; so
> equality. $\square$

The $60^\circ$ is exactly the threshold: at $61^\circ$ the two arc endpoints are
$2r\sin(30.5^\circ) = 1.0148\,r$ apart (control C2). Nothing here is slack.

> **Lemma C (corner capacity).** Let $P$ be any set with $\operatorname{diam} P \le D \le a$ that
> contains a corner $V$ of $T_a$. Then $\operatorname{area}(P \cap T_a) \le \pi D^2/6$.
>
> *Proof.* $V \in P$, so every $p \in P$ has $|p-V| \le \operatorname{diam} P \le D$, i.e.
> $P \subseteq \bar B(V,D)$. Hence $P \cap T_a \subseteq \bar B(V,D) \cap T_a = S(V,D)$, whose
> area is $\pi D^2/6$. $\square$
>
> At $D \to 1$ this is $\pi/6 = 0.5235987756$, and by Lemma S the bound is attained by the sector
> itself, which is a legal piece for every $D < 1$.

**Three corners are always three distinct pieces**, since two corners of $T_a$ are $a > 1$ apart.

**Polygonal sectors — the numbers that matter.** Inscribe in $S(V,r)$ the polygon with vertices
$V$ and $P_k = r(\cos\frac{k\pi}{3n}, \sin\frac{k\pi}{3n})$, $k = 0,\dots,n$. All its vertices lie
in $S(V,r)$, so by Lemma S its **diameter is exactly $r$** whatever $n$ is, while its area is

$$A_n(r) \;=\; \tfrac{n}{2}\sin\!\Big(\tfrac{60^\circ}{n}\Big)\,r^2 .$$

| $n$ | 1 | 2 | 3 | 4 | 6 | 12 | $\infty$ |
|---|---|---|---|---|---|---|---|
| $A_n/r^2$ | 0.4330127 | 0.5000000 | 0.5130302 | 0.5176381 | 0.5209445 | 0.5229345 | $\pi/6=0.5235988$ |

(All exact closed forms; checked in `controls.py` C5.) Two readings:

- **The sector's advantage over polygons is $1.4\%$ and vanishing.** $n=4$ already reaches
  $98.9\%$ of $\pi/6$, $n=12$ reaches $99.9\%$. This is the local shadow of Theorem SI.
- **The standing record's corner cells are exactly the $n=2$ polygon.** Control C6 confirms it
  from the certificate: each corner face has precisely three arc vertices, at squared radii equal
  (to $10^{-5}$) to the certificate's max squared diameter, and Euclidean area
  $0.49993,\ 0.49996,\ 0.49975$ against $\tfrac12 D^2 = 0.49998$. So the standing certificate is
  already using the corner sector idea, at $n = 2$; the whole remaining corner headroom is the
  $0.5000 \to 0.5236$ column above.

---

## 3. Theorem SI — shape freedom is worth exactly zero

> **Theorem SI.** Let $a>0$, $N \in \mathbb N$. The following are equivalent.
>
> 1. $T_a$ is covered by $N$ sets each of diameter $<1$.
> 2. $T_a$ is covered by $N$ compact **convex** sets each of diameter $<1$.
> 3. $T_a$ is covered by $N$ **convex polygons** each of diameter $<1$.
> 4. $T_a$ is **partitioned** into $N$ sets each of diameter $<1$.

*Proof.* $3 \Rightarrow 2 \Rightarrow 1$ and $4 \Rightarrow 1$ are trivial.

$1 \Rightarrow 4$: given $S_1,\dots,S_N$, set $C_i = (S_i \cap T_a)\setminus\bigcup_{j<i}S_j$.
These are disjoint, their union is $T_a$, and $C_i \subseteq S_i$ so
$\operatorname{diam} C_i < 1$.

$1 \Rightarrow 3$: let $D = \max_i \operatorname{diam} S_i < 1$ (a maximum of finitely many
numbers, hence $<1$). Replace $S_i$ by $K_i = \overline{S_i \cap T_a}$: still a covering of $T_a$,
each $K_i$ compact with $\operatorname{diam} K_i = \operatorname{diam}(S_i\cap T_a) \le D$ (closure
does not change a diameter). Discard the empty ones. Fix $\varepsilon>0$ with
$D + 4\varepsilon/\sqrt3 < 1$.

For each $i$, compactness gives a finite $\varepsilon$-net $k_{i,1},\dots,k_{i,m_i} \in K_i$, so
$K_i \subseteq \bigcup_t \bar B(k_{i,t},\varepsilon)$. Let
$Q_i = \operatorname{conv}\{k_{i,1},\dots,k_{i,m_i}\}$: a convex polygon (possibly a segment or a
point), with
$$\operatorname{diam} Q_i \;=\; \max_{s,t}|k_{i,s}-k_{i,t}| \;\le\; D,$$
because the diameter of a convex hull is attained at a pair of the generating points. Let $E$ be a
closed regular hexagon centred at the origin with **inradius $\varepsilon$**, so
$\bar B(0,\varepsilon)\subseteq E$ and $\operatorname{diam} E = 2\cdot\frac{2\varepsilon}{\sqrt3}
= \frac{4\varepsilon}{\sqrt3}$. Put
$$P_i \;=\; Q_i \oplus E \qquad(\text{Minkowski sum}).$$
$P_i$ is a convex **polygon**. It contains $K_i$, because
$K_i \subseteq Q_i \oplus \bar B(0,\varepsilon) \subseteq Q_i \oplus E$. And
$$\operatorname{diam} P_i \;\le\; \operatorname{diam} Q_i + \operatorname{diam} E
\;\le\; D + \tfrac{4\varepsilon}{\sqrt3} \;<\; 1,$$
since $|(q+e)-(q'+e')| \le |q-q'| + |e-e'|$. So $P_1,\dots,P_N$ cover $T_a$ and all have diameter
$<1$. $\blacksquare$

**What this says, and what it does not.**

- It is **not** a limiting statement. Given a curved covering at side $a$, it produces a polygonal
  covering at the *same* $a$. There is no $\varepsilon$ of side length lost.
- **"Round" is not the same as "curved".** The isodiametric bound $\pi/4 = 0.7853982$ for a set of
  diameter 1 *is* correct and *is* far above the regular hexagon's $3\sqrt3/8 = 0.6495191$ — but a
  polygon reaches it too: any polygon inscribed in a circle of diameter 1 with all vertex pairs
  $\le 1$ apart (e.g. the regular $(2m+1)$-gon of diameter 1) has area $\to \pi/4$. The area a disk
  carries per unit diameter is fully available to polygons. Theorem SI is the exact form of that.
- The one freedom it leaves is **partition into non-convex cells** $\equiv$ **covering by
  overlapping convex pieces** (that is exactly the content of $1 \Leftrightarrow 4$ together with
  $\operatorname{diam}\operatorname{conv} = \operatorname{diam}$). Every previous attack in this
  repo used a *convex partition*, which is strictly inside this class. §6 measures what the
  difference is worth: very little.
- Pieces are also free to stick out of $T_a$, and that too is worth nothing:
  $\operatorname{conv}(P\cap T_a)\subseteq T_a$ covers the same part of $T_a$ with no larger
  diameter.

---

## 4. Where the loss actually is — audit of the standing certificate

`audit.py` re-derives the standing certificate in exact rational arithmetic (it agrees:
15 convex faces, all inside $T_a$, $S = 2499900001/2500000000$, areas summing exactly to
$|T_a|$, **and** — checked here directly rather than by the area identity — the exact polygon
difference $T_a \setminus \bigcup P_i$ is empty). Per-piece Euclidean areas, against the
regular-hexagon-of-diameter-1 figure $3\sqrt3/8 = 0.6495191$:

| class | count | total area | mean | mean / hexagon |
|---|---:|---:|---:|---:|
| corner (contains a corner of $T_a$) | 3 | 1.49964 | 0.49988 | **77.0 %** |
| edge (two or more vertices on $\partial T_a$) | 9 | 5.23574 | 0.58175 | 89.6 % |
| interior | 3 | 1.89088 | 0.63029 | 97.0 % |
| **all** | 15 | **8.62626** | 0.57508 | 88.5 % |

and every one of the fifteen squared diameters lies in $[0.999628,\ 0.999960]$ — the
configuration is diameter-equalised to $3\cdot10^{-4}$, with **one** face attaining the maximum.

**Loss decomposition** against $15 \times 3\sqrt3/8 = 9.742786$: total deficit $1.116526$, of which

- corners $0.44892$ (40.2 %),
- edges $0.60993$ (54.6 %),
- interior $0.05768$ (5.2 %).

**The corner headroom is small and it is bounded.** By Lemma C no corner piece can exceed
$\pi D^2/6$, so the three corners can gain at most $3(\pi/6) - 1.49964 = 0.07116$ of area. At
$a = 4.4634$, $\mathrm d(\text{area})/\mathrm d a = \sqrt3 a/2 = 3.866$, so **even a perfect
corner sector is worth at most $\Delta a \approx 0.0184$** — about $11\%$ of the $0.1613$ that
separates the record from the packing ceiling $4.6247636$. That is a heuristic conversion (area is
necessary, not sufficient), but it is the right order of magnitude and it settles the priority
question: the corner is *not* where the missing $0.16$ lives.

---

## 5. Area ceilings, corrected

The figure $3\sqrt3/8 = 0.6495191$ is what a **hexagonal partition achieves**; it is not a cap on
a single piece. The caps that are actually provable:

| bound | value | why |
|---|---|---|
| any piece of diameter $\le D$ | $\pi D^2/4$ | isodiametric inequality |
| a piece containing a corner of $T_a$ | $\pi D^2/6$ | Lemma C |
| a piece covering a length-$\ell\le D$ chunk of a side — **no penalty**, area up to | $\frac{\pi-\sqrt3}{2}D^2 = 0.7047709\,D^2$ | put the Reuleaux triangle of width $D$ with its base on that side, containing the $\ell$-chunk in its base: it has diameter $D$, lies inside the half-plane, and beats the hexagon figure |

so **a rigorous area ceiling for a 15-piece covering** is
$$\tfrac{\sqrt3}{4}a^2 \;<\; 3\cdot\tfrac{\pi}{6} + 12\cdot\tfrac{\pi}{4} \;=\; \tfrac{7\pi}{2}
\qquad\Longrightarrow\qquad a \;<\; \sqrt{\tfrac{14\pi}{\sqrt3}} \;=\; 5.0391657 ,$$
which is **useless**: it is above the packing ceiling $4.6247636$, which we already get for free
from Melissen–Schuur. Any inherited kill-criterion quoting $\approx 4.5603$ from the $3\sqrt3/8$
figure is *not* a bound and must not be used as one; the criterion file in
[`../n16-covering/KILL-CRITERION.md`](../n16-covering/KILL-CRITERION.md) K4 says so of itself
("*if* the hexagonal bound is the truth").

Going the other way — is the target *achievable* on area? At $a = 4.6247636$,
$\operatorname{area}(T_a) = 9.261465$, while three corner sectors plus twelve Reuleaux-grade
boundary pieces already supply $3(\pi/6) + 12\frac{\pi-\sqrt3}{2} = 10.028047$, an $8.3\%$
surplus. **Area forbids nothing in either direction.** The obstruction at $n=16$ is a *fitting*
obstruction — how pieces of diameter $<1$ interlock along a straight edge and around a
$60^\circ$ corner — and no per-piece inequality is going to see it.

---

## 6. The one freedom Theorem SI leaves: overlap

$1 \Leftrightarrow 4$ says a covering by convex sets and a partition into *arbitrary* sets are the
same object. The previous attacks searched **convex partitions**, which is a strictly smaller
class: a convex partition is a partition into convex cells, and nothing forces the cells of an
optimal partition to be convex. So the residual question is precisely

> does allowing the cells to be non-convex — equivalently, letting the 15 convex pieces overlap —
> beat a convex partition?

### 6.1 A representation in which overlap is free and coverage is automatic

`tri_group.py`. Triangulate $T_a$ (vertices $V$, positively-oriented triangles) and **group** the
triangles into 15 classes; the piece of a group is the convex hull of its triangles. Then

- the triangles tile $T_a$ and each lies in its group's piece, so **coverage needs no checking**
  during the search;
- $\operatorname{diam}(\text{piece}) = $ the largest distance between two vertices used by the
  group, because a polygon's diameter is attained at a vertex pair;
- a group whose triangles form a **non-convex** region gives a piece that overlaps its neighbours —
  which is exactly the freedom being tested, and it costs nothing to express.

Identity grouping (one triangle-fan per face) reproduces a convex partition, so the same code runs
the control and the experiment.

### 6.2 The corner move that a convex partition cannot make

`refine.py`. In a **convex partition** an $n$-chord corner cell needs $n$ distinct neighbouring
cells, one per chord, because the chord chain is concave seen from outside and no single convex
cell can wrap it. With 15 cells and three corners that is unaffordable beyond $n=2$ — which is
exactly the $n=2$ corner the standing certificate has.

With overlap it is free: insert the new arc vertex $W$ (Lemma S puts it at radius $\le D$, so the
corner group's diameter is *unchanged*), carve the triangle $P_kWP_{k+1}$ out of the neighbouring
face and give it to the corner group. The neighbour's remaining region is non-convex, but its
convex hull is *the face it started with* — $W$ lies inside that face — so the neighbour's piece,
and its diameter, do not change at all. The corner gains
$\big(A_4 - A_2\big)D^2 = 0.0176\,D^2$ of area for free, three times over.

### 6.3 Result

Seeded from the standing certificate, same optimiser (softmax-of-diameters coordinate descent with
perturbation restarts), same time budget, at $a = 89267/20000$:

| run | family | best $\max\operatorname{diam}^2$ | $a^\star = a/\sqrt{\cdot}$ |
|---|---|---:|---:|
| seed (= standing certificate) | convex partition | 0.999960000400 | 4.4634392688 |
| `ctl_s1` | convex partition | 0.999825023113 | 4.4637405 |
| `ctl_s2` | convex partition | 0.999808650896 | 4.4637771 |
| `ref_s1` | overlapping, 4-chord corners | 0.999960000400 | 4.4634393 |
| **`ref_s2`** | **overlapping, 4-chord corners** | **0.999786121179** | **4.4638274** |

and the exact certificate frozen from `ref_s2` (`best_ref_cert.json`, rounded to denominator
$10^5$, which happened to round favourably):

> $$\boxed{\;a_{16} \;\ge\; \frac{4463841021}{10^{9}} \;=\; 4.463841021\;}
> \qquad\text{hence}\qquad s(16) \;\ge\; 12.39178366 .$$

**The corner mechanism did engage.** Corner-piece Euclidean areas, standing certificate vs this
one (ceiling $3\cdot\frac{\pi}{6}D^2$ in the last column):

| | corner 1 | corner 2 | corner 3 | total | ceiling |
|---|---:|---:|---:|---:|---:|
| standing certificate ($n=2$ chords) | 0.49993 | 0.49996 | 0.49975 | 1.49964 | 1.57074 |
| this certificate ($n=3$–$4$ chords) | 0.50424 | 0.50850 | 0.51741 | **1.53015** | 1.57045 |

i.e. $43\%$ of the corner headroom taken, at no cost in diameter — and the three corner pieces now
have 5 or 6 vertices, which is a 3- or 4-chord sector polygon, unavailable to a convex partition
with only 15 cells.

**Verification** (`verify.py`, from the problem statement, exact rationals, does not read the
search code):

| check | result |
|---|---|
| exactly 15 pieces, each simple strictly convex ccw | ok |
| every vertex in $T_a$ ($u,v\ge0$, $u+v\le a$) | ok |
| $\max\operatorname{diam}^2 = 9997800121/10^{10} < 1$ **strictly** | ok |
| $T_a \setminus \bigcup P_i$ empty, by exact polygon difference | ok — **no area identity used** |
| overlap | $6$ of $105$ pairs overlap, total area $0.0361$ — a genuine covering, not a partition |
| quoted rational $r$ satisfies $r^2 S \le a^2$ exactly | ok |

**Honest reading of the table.** The improvement over the standing record is
$4.0\times10^{-4}$, and the *overlapping* runs beat the *convex-partition* control by
$5\times10^{-5}$ — which is **inside the run-to-run spread** ($\texttt{ctl\_s1}$ and
$\texttt{ctl\_s2}$ differ by $3.7\times10^{-5}$, and $\texttt{ref\_s1}$ found nothing at all).
So: **overlap is not demonstrated to help.** What is demonstrated is that it does not hurt, that
it is cheap to express, and that it is the only structural freedom Theorem SI leaves. The gain
reported here should be attributed to more search, not to the piece class.

---

## 7. What this is worth, and what to do instead

- **`sketch`, not `verified:review`.** Theorem SI, Lemmas S and C and the certificate are all
  mine, checked only by me and by controls I wrote (`controls.py`, all pass). `RULES.md` §5 needs
  an examiner from a different model family. Theorem SI is short and elementary and is the thing
  to examine first: if it is right, it closes a whole direction, and if it is wrong, everything in
  §6 is misdirected.
- **Novelty UNVERIFIED.** Scholarly hosts are blocked from this session. Theorem SI is the sort of
  statement that is folklore in convexity (it is essentially "diameter is a hull invariant" plus
  "polygons are dense in the Hausdorff metric"); **assume it is known.** The covering/pigeonhole
  bound for circle packing in a triangle is likewise a natural idea and may well be published.
- **The ceiling is unchanged.** No covering argument can prove more than
  $a_{16} \le 4.6247636$, since a 16-point packing exists there. Remaining headroom: $0.161$.
- **Do not spend another session on piece shape.** Theorem SI says there is nothing there. In
  particular: sectors ✗ (polygons reach $98.9\%$ of a sector at $n = 4$), Reuleaux and other
  constant-width pieces ✗, disks ✗, non-convex L-/crescent pieces ✗, disconnected pieces ✗,
  pieces poking outside $T_a$ ✗.

**Where the money is, in order:**

1. **The edge collar — 55% of the loss.** Nine edge pieces average $89.6\%$ of the hexagon
   figure while a single boundary piece can reach $\frac{\pi-\sqrt3}{2} = 0.7048$ ($108\%$ of it).
   The gap is a *tiling* effect: pieces of diameter $<1$ covering $\approx 0.9$ of boundary each
   must lean along the side and then interlock badly with the second row. This is a small,
   self-contained 1-D question (how densely can diameter-$<1$ convex sets cover a straight strip
   at a prescribed advance per piece?) and it is worth answering exactly before any more global
   search.
2. **Topology enumeration.** Every run in this repo — the predecessor's four seeds, my four —
   lands in $[4.4634, 4.4640]$ from the *same* 3-corner / 9-edge / 3-interior combinatorics. The
   plateau may be a property of that topology and not of the problem. Enumerating the splits
   (3/10/2, 3/11/1, 3/12/0, …) and re-optimising each would settle it; note $a = 4.6248$ needs
   $\ge 5$ pieces per side, i.e. $\ge 12$ boundary pieces, so 3/12/0 is the extreme case and is
   *not* excluded by anything proved here.
3. **A real upper bound on $a^\star(15)$.** §5 shows area arguments cannot produce one below the
   packing ceiling. If a covering-density (hexagon-bound-for-coverings) result can be *cited*
   rather than assumed, it would give $\tfrac{\sqrt3}{4}a^2 \le 15\cdot\tfrac{3\sqrt3}{8}$, i.e.
   $a \le 4.7434$ — still above the ceiling, so still not decisive. Nobody should invest in that
   direction expecting it to close the case.

## Reproduce

```bash
python3 experiments/packing-n16-shapes/controls.py                 # lemma controls, ~10 s
python3 experiments/packing-n16-shapes/audit.py                    # audit of the standing cert
python3 experiments/packing-n16-shapes/verify.py \
        experiments/packing-n16-shapes/best_ref_cert.json          # the new bound, ~2 s
```

Exact rational arithmetic, Python standard library, no seeds needed for the verification, no
network. The search (`drive.py`) is float-only, seeded, and decides nothing.
