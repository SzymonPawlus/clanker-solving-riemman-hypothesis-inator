# Groemer's Satz and Oler's inequality — the equality characterisation, from the primary source

**Issue:** #96. **Outcome: confirmed, with two corrections to what #96 itself asserted.**

Two separable things live in this file, and they carry *different* statuses. Read the status
labels, not the prose.

| Thing | Status | Why |
|---|---|---|
| Groemer's Satz and its equality clause, as printed on p. 285 | `cited` | Primary source **read in full**, all 10 pages, from the GDZ scan. Verbatim German below. |
| The derivation Groemer's Satz $\Rightarrow$ Oler's inequality for $\pi = \mathrm{conv}(E)$ | `sketch` | Redone here independently and checked symbolically, but it is an agent derivation and no examiner has granted `verified:review`. **Not assumable** (`RULES.md` §3), including by me. |
| "Groemer's equality clause *is* (R2) of issue #44" | `sketch` | One inference beyond the printed clause is mine; §4.3 isolates it. |

---

## 1. The source, and exactly how it was reached

H. Groemer, *Über die Einlagerung von Kreisen in einen konvexen Bereich*, Math. Z. **73** (1960)
285–294. Received 12 June 1959; author's address on p. 294 is Oregon State College, Corvallis.

**Read in full — all ten pages, 285 through 294.** Locators actually used, so the next worker does
not have to rediscover them:

| Locator | Reached? |
|---|---|
| `https://gdz.sub.uni-goettingen.de/id/PPN266833020_0073` (Math. Z. vol. 73 on GDZ) | **yes**, HTTP 200 |
| IIIF manifest `https://gdz.sub.uni-goettingen.de/iiif/presentation/PPN266833020_0073/manifest` | **yes**, 729 KB of JSON |
| Logical range `LOG_0047` in that manifest — *Über die Einlagerung von Kreisen…*, 10 canvases | **yes** |
| Page images `https://images.sub.uni-goettingen.de/iiif/image/gdz:PPN266833020_0073:000003NN/full/1800,/0/default.jpg` for `NN = 299…308` | **yes**, all ten, 1800×2947 px |
| Legacy resolver `http://gdz.sub.uni-goettingen.de/dms/resolveppn/?PPN=GDZPPN002389444` | reachable but **useless** — it lands on the journal's search portal, not the article |
| `https://gdz.sub.uni-goettingen.de/id/GDZPPN002389444` | **404** |
| `https://gdz.sub.uni-goettingen.de/mets/PPN266833020_0073` | **404** |

Canvas *labels* in the manifest are the printed page numbers, so image `00000299` ↔ p. 285 …
image `00000308` ↔ p. 294. That mapping is the manifest's own, not an assumption of mine.

**Note for the provenance table in `../../README.md`:** the old entry recorded pp. 286–293 as
unread and the resolver PPN `GDZPPN002389444` as the route. That resolver PPN no longer resolves to
the article; the working route is the volume PPN plus the IIIF manifest, recorded above.

## 2. What p. 285 actually prints — `cited`

Verbatim, including the equality clause, which is printed as running italic text immediately after
the displayed inequality (transcribed from the scan, German original; `ϰ` is Groemer's kappa):

> **Satz.** *Sind in einem konvexen Bereich vom Flächeninhalt $F$ und Umfang $U$ $n$ Einheitskreise
> eingelagert, so ist*
>
> $$(2) \qquad n\cdot\sqrt{12} \le F - \varkappa U + \lambda$$
>
> *mit*
> $$\varkappa = \frac{2-\sqrt3}{2} = 0{,}1339\ldots, \qquad \lambda = \sqrt{12} - \pi(\sqrt3-1) = 1{,}1642\ldots$$
>
> *Das Gleichheitszeichen steht in* (2) *genau dann, wenn $B$ die konvexe Hülle aller eingelagerten
> Kreise ist und, wenn die konvexe Hülle $H$ aller Kreismittelpunkte eine der folgenden Bedingungen
> erfüllt:*
>
> *a) $H$ kann in gleichseitige Dreiecke der Seitenlänge 2 zerlegt werden und jeder Eckpunkt dieser
> Dreiecke ist Mittelpunkt eines Kreises.*
>
> *b) $H$ kann in geradlinige Strecken der Länge 2 zerlegt werden, und jeder Endpunkt dieser Strecken
> ist Mittelpunkt eines Kreises.*
>
> *c) $H$ ist ein Punkt.*
>
> Die Ungleichung (2) ist auch für $n=1$ richtig und für $n>1$, mit Rücksicht auf
> $U \ge 2\pi + 4 > \lambda/\varkappa = 8{,}7\ldots$, tatsächlich schärfer als (1).
>
> — Groemer, Math. Z. 73 (1960), p. 285.

In English: for $n$ **unit-radius** circles packed (no overlapping interiors) into a convex region
$B$ of area $F$ and perimeter $U$, inequality (2) holds; equality holds **iff** $B$ is the convex
hull of the circles *and* the convex hull $H$ of the centres satisfies a), b) or c).

### 2.1 Hypotheses, checked one at a time

Everything the Satz assumes, and where it comes from:

- $B$ convex, with finite area $F$ and finite perimeter $U$ (so bounded — §1 of the paper opens
  with "*ein beschränkter konvexer Bereich*").
- The circles have **radius 1** — hence centres at mutual distance $\ge 2$. This is the scale
  convention that the rescaling in §3 has to undo, and it is the single thing in this file most
  likely to be got backwards.
- $n \ge 1$. The paper inherits Fejes Tóth's $n \ge 2$ for its (1), but states explicitly that (2)
  is also correct for $n = 1$ — and at $n = 1$ it is in fact *tight*, via case c). See the $k=1$
  row of §3.3.
- **No further hypothesis attaches to the equality clause.** This was the load-bearing question of
  #96, and answering it needed pp. 286–293, which is why the derivation alone could not settle it.

### 2.2 What the proof does, pp. 286–294 — and why that matters here

Read so that the equality clause can be trusted rather than assumed:

- **p. 286, §2.** The reduction to $B = C := \mathrm{conv}(\text{the circles})$. Groemer shows
  $\Delta F - \varkappa\,\Delta U \ge 0$, where $\Delta$ compares $B$ against $C$; hence
- **p. 287.** $\overline F - \varkappa\overline U \le F - \varkappa U$, "*dabei steht das
  Gleichheitszeichen … nur für $B = C$*". Direction check: the functional is **smallest** on the
  hull, so proving (2) for $B = C$ gives it for every $B$. This reduction is what makes §3
  legitimate, and it is also the source of the first half of the equality clause.
- **pp. 287–288.** Dirichlet cells, cell polygons, and **Hilfssatz 1**, which reduces (2) to a
  per-cell-polygon inequality (4) and — crucially — carries equality **both ways**: "*Gilt in jeder
  der Ungleichungen* (4) *Gleichheit, so auch in* (2)*; gilt in mindestens einer der Ungleichungen*
  (4) *nicht das Gleichheitszeichen, so gilt es auch in* (2) *nicht.*" Its proof uses
  $\sum r_i = U - 2\pi$, $\sum Z_i = F - \pi$, $\sum \alpha_i = 2\pi n - 2\pi$; summing (4) gives
  $\frac{\sqrt3}{\pi}(2\pi n - 2\pi) + \frac{2-\sqrt3}{2}(U - 2\pi) \le F - \pi$, which rearranges
  to (2) with exactly the printed $\lambda$ — checked in `derive.py`.
- **pp. 288–293.** Hilfssätze 2–8 (Hilfssatz 2 is Segre–Mahler's hexagon bound, cited not
  reproved). Equality is tracked explicitly throughout, e.g. p. 290: "*das Gleichheitszeichen
  durchgehend genau dann gilt, wenn $\alpha = \pi/2$, $h_1 = 1$ und $h_2 = 1$ ist*".
- **p. 294, §4.** The endgame. Hilfssätze 3, 4, 5, 7, 8 give **strict** inequality except when a
  cell quadrilateral is a unit square with a side on $\partial B$; $H$ is recovered from $B$ by
  removing those squares and the Segre–Mahler circular sectors. One- and zero-dimensional $H$ give
  cases b) and c), "*und umgekehrt gilt in diesen Fällen auch Gleichheit*". For two-dimensional
  $H$, Segre–Mahler forces every cell$\,\cap\,H$ to be a regular hexagon circumscribed about its
  circle (or the part of one cut off by two perpendicular bisectors, when the centre lies on
  $\partial H$), and then "*Verbindet man die Mittelpunkte von je zwei einander berührenden Kreisen,
  so erhält man die verlangte Zerlegung von $H$ in gleichseitige Dreiecke*". The paper ends "*Dies
  ergibt Teil a) des Satzes*".

**"Teil a) des Satzes" is case a) of the equality clause, not an unread part of the paper.** The
provenance note in `../../README.md` previously left that open; it is now settled. The equality
characterisation is genuinely *proved*, in both directions, not merely asserted.

## 3. The derivation, redone independently — `sketch`

Reproducible: `python3 derive.py` in this directory (sympy; exact symbolic arithmetic throughout —
no float is used for any assertion, only for display).

### 3.1 Setup

Let $E$ be $n$ points at mutual distance $\ge 2$ and $H = \mathrm{conv}(E)$. Take

$$K \ :=\ H \oplus B_1 \ =\ \{x : \mathrm{dist}(x, H) \le 1\}.$$

$K$ is convex and bounded; the $n$ unit circles centred at $E$ lie in $K$ and do not overlap. So
Groemer's Satz applies with $B = K$. Moreover $K = \mathrm{conv}\big(\bigcup_i B(e_i,1)\big)$ — the
convex hull of a union of equal balls is the hull of the centres Minkowski-summed with the ball —
so **the first half of the equality clause is satisfied automatically**, exactly as #96 says.

Steiner, for convex $H$ and $r = 1$, with $M(H)$ the perimeter of $H$:

$$F = A(H) + M(H) + \pi, \qquad U = M(H) + 2\pi.$$

*Degenerate $H$ is not a special case here:* for a segment of length $L$, $A = 0$ and $M = 2L$ (the
boundary traversed both ways), and $K$ is a stadium of area $2L + \pi$ and perimeter $2L + 2\pi$ —
the formulas hold as written. For a point, $M = 0$, $F = \pi$, $U = 2\pi$.

### 3.2 The algebra

$$n\sqrt{12} \ \le\ \big(A + M + \pi\big) - \varkappa\big(M + 2\pi\big) + \lambda
 \ =\ A + (1-\varkappa)M + \underbrace{\pi(1-2\varkappa) + \lambda}_{\textstyle =\ \sqrt{12}}$$

because $1 - 2\varkappa = \sqrt3 - 1$ and $\lambda = \sqrt{12} - \pi(\sqrt3-1)$. **Every $\pi$
cancels** — checked symbolically as `rhs.coeff(pi) == 0`, not by inspection — and
$1-\varkappa = \sqrt3/2$. Dividing by $\sqrt{12} = 2\sqrt3$:

$$\boxed{\;n \ \le\ \tfrac{\sqrt3}{6}A(H) \ +\ \tfrac{1}{4}M(H) \ +\ 1\;}\qquad\text{(separation 2)}$$

**Rescaling — the step to check twice.** Groemer's separation is 2, Oler's is 1, so the map is a
**shrink** by $1/2$. Writing $H' = \tfrac12 H$, so that $E' = \tfrac12 E$ has separation $\ge 1$:
$A(H') = A(H)/4$ and $M(H') = M(H)/2$, i.e. $A(H) = 4A(H')$ and $M(H) = 2M(H')$. Substituting,

$$n \ \le\ \tfrac{\sqrt3}{6}\cdot 4A(H') + \tfrac14\cdot 2M(H') + 1
      \ =\ \tfrac{2}{\sqrt3}A(H') + \tfrac12 M(H') + 1,$$

which is Oler's inequality. `derive.py` also evaluates the **inverted** substitution
$A = A'/4,\ M = M'/2$ and asserts that it does *not* reproduce Oler (it gives
$\tfrac{\sqrt3}{24}A' + \tfrac18 M' + 1$), so a silent direction flip cannot pass unnoticed.

The converse is checked too: Oler at $\pi = \mathrm{conv}(E)$, rewritten at separation 2 and pushed
back through Steiner, reproduces $F - \varkappa U + \lambda$ identically. Together with Groemer's
own p. 287 reduction from general $B$ to $B = C$, the two statements are **equivalent**, not merely
one-directional.

### 3.3 Independent numeric confirmation, at Groemer's own scale

Not a rerun of the algebra — a separate check that the Satz is *tight* exactly where the equality
clause says it should be. Triangular-lattice $E$, $n = k(k+1)/2$, hull an equilateral triangle of
side $2(k-1)$, $K = H \oplus B_1$:

| $k$ | $n$ | $n\sqrt{12}$ | $F - \varkappa U + \lambda$ | $\text{RHS}-\text{LHS}$ |
|---|---|---|---|---|
| 1 | 1 | 3.4641016 | 3.4641016 | **exactly 0** (case c) |
| 2 | 3 | 10.392305 | 10.392305 | **exactly 0** |
| 3 | 6 | 20.784610 | 20.784610 | **exactly 0** |
| 4 | 10 | 34.641016 | 34.641016 | **exactly 0** |
| 5 | 15 | 51.961524 | 51.961524 | **exactly 0** |
| 6 | 21 | 72.746134 | 72.746134 | **exactly 0** |
| 7 | 28 | 96.994845 | 96.994845 | **exactly 0** |

The differences are `simplify(...) == 0` exactly, not small floats. Equality fires precisely at the
configurations of Groemer's case a) (and c) at $k = 1$) — the behaviour the clause predicts.

## 4. Corrections to issue #96's own wording

#96 got the substance right. Two things in it are nevertheless overstated, and being able to say
which is the point of having read the source.

### 4.1 "Verbatim" is too strong: Groemer gives Oler **only for $\pi = \mathrm{conv}(E)$**

Oler's CMB statement (see `../oler-lower-bound/README.md` §1.1) is for an arbitrary **Jordan
polygon** $\pi$ whose vertices belong to $E$ and which contains $E$; $\pi$ need **not** be convex.
The derivation above produces the inequality only for $\pi = H = \mathrm{conv}(E)$, because Steiner
and $K = H \oplus B_1$ both require $H$ convex. Groemer's Satz therefore yields Oler's inequality
**specialised to the convex hull**, and says nothing about non-convex $\pi$.

This costs this repository nothing — `../oler-lower-bound/README.md` §1.2 states that *every*
application in it takes $\pi = H$ — but "reduces verbatim to Oler's inequality" claims more than
the derivation delivers, and the difference should not be laundered.

### 4.2 The repo's one-sentence transcription of the equality clause was **loose**

`../../README.md` rendered the clause as

> "…the hull $H$ of the centres decomposes into equilateral triangles of side 2 whose vertices are
> all centres **(or degenerates to a segment or a point)**."

Case a) is faithful. The parenthetical is **not** a faithful rendering of b): Groemer requires $H$
to decompose into **segments of length 2 with every endpoint a circle centre**, which is strictly
stronger than "$H$ is a segment". Three centres at $0, 2, 5$ on a line have segment hull and give
strict inequality, so "$H$ degenerates to a segment" alone is *not* an equality case.

#96's premise was that the transcription might have lost a hypothesis. It did — in b), not in a).
The loss is in the direction of making the clause look *weaker* (more permissive) than it is, so
nothing previously built on case a) is affected. Corrected in `../../README.md`.

### 4.3 What this gives issue #44, and the gap that remains

Issue #44 asked whether **Oler's Acta paper** characterises the equality case. It is **closed and
its answer stands**: `../oler-lower-bound/README.md` §5.2 read that paper in full and found no such
theorem. Nothing here disturbs that finding.

What is corrected is the *generalisation* §5.2 drew from it — that the equality characterisation is
missing from the **literature**. It is not. Groemer states and proves it in 1960, a year before
Oler, and this repository has held the reference since PR #21.

**The residual gap, stated so it is not glossed over.** #44's (R2) asks that equality force
$E \subseteq \Lambda$ for a triangular lattice $\Lambda$ of minimal distance exactly 1. Groemer's
case a) gives: $H$ decomposes into unit (post-rescaling) equilateral triangles, every vertex of
which is a point of $E$. Two inferences separate that from (R2), and **both are mine, `sketch`, not
Groemer's**:

1. *Every point of $E$ is a vertex of the decomposition.* Groemer says every vertex is a centre,
   not the converse. This looks easy — the circumradius of a unit equilateral triangle is
   $1/\sqrt3 \approx 0.577 < 1$, so every point of $H$ is within $1/\sqrt3$ of some vertex, and
   separation 1 then forces it to *be* that vertex — but it is an argument I wrote, not one I read.
2. *The vertex set of such a decomposition lies in a triangular lattice.* p. 294 helps: the
   decomposition is obtained by **joining the centres of touching circles**, so its edges are
   genuine unit-distance edges of $E$ and the triangulation is edge-to-edge. I have still not
   written out the step from "edge-to-edge unit-equilateral triangulation" to "subset of a lattice".

So: **#44's question is answered, and (R2) is now within reach of a short argument from a `cited`
source rather than being absent from the literature — but (R2) is not itself `cited` yet.** Anyone
promoting it must either write out 1–2 and have them cross-examined, or find a source stating (R2)
in Oler's own normalisation. A successor issue for exactly that is the right move; this file does
not quietly do it.

## 5. What is *not* claimed here

- Not claimed: that Groemer proves anything about the equilateral triangle, or credits any
  particular $n$. He does not — the `../../README.md` rejection of Friedman's Groemer co-credit is
  **unaffected and remains correct**. The paper contains one theorem and no application, which the
  full reading now confirms rather than infers from its first and last pages.
- Not claimed: that the Erdős–Oler conjecture is settled, or that any open $n$ moves. Groemer's
  clause is about equality in *his* inequality; turning it into "$n$ must be triangular" needs (R1)
  *and* (R2) *and* the counting, and §4.3 says which of those are still open.
- Not claimed: `verified:review` for anything in §3 or §4. The derivation is short and was checked
  symbolically in both directions, which is exactly the kind of confidence `RULES.md` §0 warns
  about. It needs a cross-family examiner.
