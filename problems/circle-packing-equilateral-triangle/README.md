# Circle packing in an equilateral triangle

**Status:** open for most $n$. Optimality is proven for **all $n \le 15$**, for every triangular
number $n = k(k+1)/2$, and — with the qualification below — for $n = 20$; everything else is
best-known-construction.

> **Qualification, 2026-08.** The $n = 20$ row is kept, but its provenance is now on the record.
> Payan's abstract states that his $k = 5$ ($n = 14$) proof *extends* to $k = 6$ ($n = 20$); this
> project has read that abstract and **not** the paper's body, so it has not seen how the extension
> is carried out. See [The $n = 20$ attribution](#the-n--20-attribution--qualified).

Shared conventions: [`../README.md`](../README.md). Repo-wide protocol:
[`../../RULES.md`](../../RULES.md). **Problem-specific rules: [`RULES.md`](./RULES.md) — read
before working on this problem.**

## Statement

Pack $n$ unit circles into the smallest possible equilateral triangle. Write $s(n)$ for the
minimal side length.

$s(n)$ is settled for $n \le 15$, for all triangular $n$, and — on Payan's abstract, see below —
for $n = 20$; see the table below. There is no known closed form for general $n$.

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

### Proven optimal, $n \le 15$ — status `cited`

Every row below is **proven optimal**. The former split of this table into "proven" and
"best known" was wrong; see [Resolution of the source conflict](#resolution-of-the-source-conflict).

Two rows carry a note. **$n = 14$** is the strongest of the Payan attributions: his abstract says
outright "in this paper, we give a proof for $k = 5$ (arrangement for 14 disks)", and Tedeschi &
Mackey and Wikipedia agree. **$n = 4,5,7,8,9,12$** are attributed to the 1993 Monthly paper on the
strength of zbMATH's review of it, not of its body; see
[The Melissen split](#the-melissen-split--resolved).

| $n$ | $s(n)$ | Optimality proved by | Reference |
|---|---|---|---|
| 1 | $2\sqrt{3} \approx 3.464$ | trivial | — |
| 2 | $2 + 2\sqrt{3} \approx 5.464$ | trivial | — |
| 3 | $2 + 2\sqrt{3} \approx 5.464$ | trivial ($n = \Delta(2)$) | Oler (1961) |
| 4 | $4\sqrt{3} \approx 6.928$ | Milano (1987); Melissen (1993) | Amer. Math. Monthly **100**, 916–925 |
| 5 | $4 + 2\sqrt{3} \approx 7.464$ | Milano (1987); Melissen (1993) | Amer. Math. Monthly **100**, 916–925 |
| 6 | $4 + 2\sqrt{3} \approx 7.464$ | Oler (1961), $n = \Delta(3)$ | Canad. Math. Bull. **4**, 153–155 |
| 7 | $2 + 4\sqrt{3} \approx 8.928$ | Melissen (1993) | Amer. Math. Monthly **100**, 916–925 |
| 8 | $2 + 2\sqrt{3} + \tfrac{2\sqrt{33}}{3} \approx 9.294$ | Melissen (1993) | Amer. Math. Monthly **100**, 916–925 |
| 9 | $6 + 2\sqrt{3} \approx 9.464$ | Melissen (1993) | Amer. Math. Monthly **100**, 916–925 |
| 10 | $6 + 2\sqrt{3} \approx 9.464$ | Oler (1961), $n = \Delta(4)$ | Canad. Math. Bull. **4**, 153–155 |
| 11 | $4 + 2\sqrt{3} + \tfrac{4\sqrt{6}}{3} \approx 10.730$ | Melissen (**1994**) | Acta Math. Hungar. **65**, 389–393 |
| 12 | $4 + 4\sqrt{3} \approx 10.928$ | Melissen (**1993**) | Amer. Math. Monthly **100**, 916–925 |
| 13 | $4 + \tfrac{2\sqrt{6}}{3} + \tfrac{10\sqrt{3}}{3} \approx 11.406$ | **Joós (2020)** | Aequat. Math. **95**, 35–65 |
| 14 | $8 + 2\sqrt{3} \approx 11.464$ | **Payan (1997)** | Discrete Math. **165–166**, 555–565 |
| 15 | $8 + 2\sqrt{3} \approx 11.464$ | Oler (1961), $n = \Delta(5)$ | Canad. Math. Bull. **4**, 153–155 |

Also proven, outside the $n \le 15$ range:

| $n$ | $s(n)$ | Optimality proved by | Reference | Provenance |
|---|---|---|---|---|
| $\Delta(k) = \tfrac{k(k+1)}{2}$ | $2(k-1) + 2\sqrt{3}$ | Oler (1961) | Canad. Math. Bull. **4**, 153–155 | primary read in full |
| 20 $= \Delta(6) - 1$ | $10 + 2\sqrt{3} \approx 13.464$ | Payan (1997) | Discrete Math. **165–166**, 555–565 | **abstract only — body not read**, see [below](#the-n--20-attribution--qualified) |

### Best known only (optimality *not* established) — status `numerical`

| $n$ | best known $s(n)$ | Construction due to |
|---|---|---|
| 16, 17, 18 | various | Melissen & Schuur (1995), Discrete Math. **145**, 333–342 |
| 19 | — | pre-1995 literature; see Graham & Lubachevsky (1995), which reproduces it |
| 22–34 | various | Graham & Lubachevsky (1995), Electron. J. Combin. **2**, #A1 |

($n = 20$ and $n = 21 = \Delta(6)$ are *proven in the literature*, not best-known — see the table
above; $n = 20$ carries the qualification recorded in the next section.)

### The $n = 20$ attribution — qualified

**What changed:** nothing about *who* proved $n = 20$. What changed is that the provenance is now
written down. `main` asserted "$n = 20$ is proven optimal (Payan 1997)" flatly, on the strength of
Tedeschi & Mackey (AJUR 2021) — a secondary source — with no record of what had actually been read.
The attribution stands; the unstated warrant does not.

Payan's abstract, from the publisher's own page for the paper (**primary source, abstract only —
the body was not obtained**), reads in full, in both languages Elsevier prints:

> Les empilements optimaux de $n$ cercles égaux dans un triangle équilatéral ne sont connus que
> pour les première valeurs de $n$ ($n \le 12$) et pour les nombres triangulaires […] Cette
> conjecture n'est montrée que pour $k \le 4$. **Nous donnons une preuve pour $k = 5$ (empilement
> de 14 cercles). Cette preuve s'étend de manière un peu plus laborieuse pour $k = 6$ (empilement
> de 20 cercles)** et devrait permettre une approche de la conjecture générale.

> […] Its validity is known for $k \le 4$. **In this paper, we give a proof for $k = 5$
> (arrangement for 14 disks). This proof can be extended for the case $k = 6$ (arrangement for 20
> disks)** and should allow an approach of the general conjecture.

**What the abstract establishes.** The French is a present indicative — *"cette preuve s'étend
[…] pour $k = 6$"*, this proof extends to $k = 6$ — and the English that Elsevier prints alongside
it says the proof "can be extended" to that case. Both are the author asserting, in his own paper's
abstract, that the method **applies** to $k = 6$ ($n = 20$). That is a positive attribution, and it
is the direct evidence this project holds for the $n = 20$ row.

**What the abstract does not establish.** Whether the $k = 6$ case is written out in the body, or
its details are left to the reader. The body was not obtained, so we cannot tell those two apart —
and the distinction is worth naming, because a case carried out in full has been through refereeing
and reading in a way an exercise left to the reader has not. But **it is not a reason to call the
result unproved.** A published proof that discharges its last case briskly is still a published
proof; only the paper can settle which of the two this is.

**Status, stated precisely** (`RULES.md` §3), because the difference between these two rows is the
whole point of this section:

| Claim | Status |
|---|---|
| Payan's published abstract asserts that his $k = 5$ proof extends to $k = 6$ ($n = 20$) | `cited` — quoted verbatim from the publisher's page, above |
| $s(20) = 10 + 2\sqrt{3}$ is optimal | `cited`, **qualified**: it rests on that assertion and on no inspection of the argument itself |

The second is not stronger than the first, and nothing in this repo should treat it as if it were.
What would settle it is one PDF; see [Remaining gaps](#remaining-gaps-honest-accounting).

**What is *not* evidence — recorded because an earlier draft of this section offered it as such.**
That draft concluded $n = 20$ is unproven and moved it to the best-known table. It should not have:

- **Tedeschi & Mackey does not contradict itself.** Its introduction states $n = 20$ as proven and
  cites Payan for it. Its abstract, describing how Payan ($n = 14$) and Joós ($n = 13$) completed
  the cases through $n = 15$, simply does not mention the separate $n = 20$ result. Omission is not
  denial.
- **Wikipedia's "$n \le 15$" is the same omission.** It cites Payan, summarises the contiguous
  range, and says nothing either way about $n = 20$.
- **zbMATH's review** of Payan (Zbl 0897.52003, J. M. Wills) says only that the author "considers
  optimal packings of equal circles in equilateral triangles for some particular values" —
  uninformative in both directions.

A source that does not repeat a claim has not denied it. Reading those silences as refutation was
the same error, inverted, as reading a survey's summary as a primary source — which is what put the
unqualified claim on `main` to begin with. Both come from not saying exactly what a source says.

$n = 14$ is unaffected throughout, and is better sourced than before: the abstract states that
proof outright, in the paper.

### Resolution of the source conflict

The `⚠️` block that used to sit here said Wikipedia and Friedman disagree about $n \le 15$. Both
halves of that framing were wrong, and it is worth recording why.

1. **Friedman was misread.** His page marks $n = 7, 8, 11$ as *"Proved by Melissen in 1993"*, not
   best-known. Only $n = 13$ (*"Found by Melissen in 1993"*) and $n = 14$ (*"Found by
   Erdős/Oler in 1961"*) carry his best-known wording. So the real disagreement was over two
   values of $n$, not five.
2. **Friedman's page is simply out of date on those two.** As of Graham & Lubachevsky (1995),
   $n = 13$ and $n = 14$ genuinely were open — their introduction states that the only known
   optima are the triangular numbers plus $n = 2, 4, 5, 7, 8, 9, 11, 12$. The two gaps closed
   later:
   - $n = 14$: **C. Payan (1997)**, proving the Erdős–Oler conjecture for $k = 5$. (His abstract
     also states that the proof extends to $k = 6$, i.e. $n = 20$; for what we have and have not
     checked there, see [The $n = 20$ attribution](#the-n--20-attribution--qualified).)
   - $n = 13$: **A. Joós**, published online 2 September 2020, Aequat. Math. **95** (2021) 35–65,
     confirming Melissen's 1993 conjecture and a Graham–Lubachevsky conjecture.

   Together these complete $n \le 15$, which is exactly what Wikipedia asserts.
3. **The old table also had $n = 11$ and $n = 12$ swapped** (following Friedman). Melissen's
   *1994* Acta Math. Hungar. paper is titled "Optimal packings of **eleven** equal circles in an
   equilateral triangle"; $n = 12$ is in the *1993* Monthly paper.
4. **"Milano (1987)"** in Friedman's table is R. Milano, *Configurations optimales de disques dans
   un polygone régulier*, mémoire de licence, Université Libre de Bruxelles (1987) — an
   unpublished thesis covering $n \le 6$. Melissen's 1993 Monthly paper covers those cases too, so
   the table above cites the published source. Friedman's "Groemer" co-credits for $n = 6, 10, 15$
   are **checked and rejected** — see [Groemer](#groemer-1960--co-credit-rejected) below.

Consistency check on $n = 13$: Joós states the maximum separation of 13 points in a unit-side
triangle as $t_{13} = 9 - 5\sqrt{3} - \tfrac{7\sqrt{6}}{2} + 6\sqrt{2} \approx 0.2518132$. Via
$s = 2\sqrt{3} + 2/t_{13}$ this gives $11.40649585375161$, against
$4 + \tfrac{2\sqrt{6}}{3} + \tfrac{10\sqrt{3}}{3} = 11.40649585375171$ — agreement to $10^{-13}$,
confirming Joós proved optimality of exactly the value tabulated above.

### The Melissen split — resolved

The per-$n$ split of $\{4,5,7,8,9,12\}$ into the 1993 Monthly paper used to be marked *inferred*.
It is now confirmed, and it was right. zbMATH's review of that paper (Zbl 0814.52006, reviewing
Amer. Math. Monthly **100** (1993) 916–925, doi:10.2307/2324212) says:

> Given an equilateral triangle $T$ in the Euclidean plane put $n$ points in $T$ such that the
> minimal distance between any two points of this arrangement is maximal. The author lists such
> configurations for $n = 2,3,4,\dots,10,12$ and for $n = k(k+1)/2$, $k \ge 2$, **together with
> proofs of the optimality and the uniqueness** (whenever the configuration is unique). **The case
> $n = 11$ is announced.**

So the 1993 Monthly paper proves $n = 2,\dots,10$ and $n = 12$, plus the triangular numbers, and
*announces* $n = 11$ — which is then settled in the 1994 Acta Math. Hungar. paper whose title says
so. That is exactly the split the table above uses, including the 11/12 ordering that Friedman has
backwards.

**Provenance:** this is a **review of the primary source**, written by a mathematician who read the
paper — not the paper's own text. It is a stronger warrant than a survey's passing summary, and
weaker than the body. Neither Melissen paper's body was obtained (JSTOR and Springer, both
paywalled).

### Groemer (1960) — co-credit rejected

Friedman co-credits "Oler/Groemer" for $n = 6, 10$ and "Erdős/Groemer" for $n = 15$. This is now
checked against the paper itself and the co-credit does **not** stand.

Groemer, *Über die Einlagerung von Kreisen in einen konvexen Bereich*, Math. Z. **73** (1960)
285–294, is freely readable as a scan via GDZ Göttingen. **All ten pages, 285–294, have now been
read directly from that scan** (issue #96; the working locators are recorded in
[`attacks/groemer-oler-equivalence/`](attacks/groemer-oler-equivalence/README.md) §1 — the old
`GDZPPN002389444` resolver no longer reaches the article, the route is the volume PPN
`PPN266833020_0073` plus its IIIF manifest). The paper contains exactly one theorem, a sharpening
of Fejes Tóth's $n\sqrt{12} \le F$:

> **Satz.** Sind in einem konvexen Bereich vom Flächeninhalt $F$ und Umfang $U$ $n$ Einheitskreise
> eingelagert, so ist
> $$n \cdot \sqrt{12} \le F - \varkappa U + \lambda$$
> mit $\varkappa = \tfrac{2-\sqrt3}{2} = 0{,}1339\ldots$, $\lambda = \sqrt{12} - \pi(\sqrt3 - 1) =
> 1{,}1642\ldots$
>
> — Groemer, Math. Z. 73 (1960), p. 285.

The equality clause is printed on the same page, immediately below, and is transcribed here in full
because an earlier one-sentence paraphrase of it was loose (see the correction note below):

> *Das Gleichheitszeichen steht in* (2) *genau dann, wenn $B$ die konvexe Hülle aller eingelagerten
> Kreise ist und, wenn die konvexe Hülle $H$ aller Kreismittelpunkte eine der folgenden Bedingungen
> erfüllt:*
>
> *a) $H$ kann in gleichseitige Dreiecke der Seitenlänge 2 zerlegt werden und jeder Eckpunkt dieser
> Dreiecke ist Mittelpunkt eines Kreises.*
> *b) $H$ kann in geradlinige Strecken der Länge 2 zerlegt werden, und jeder Endpunkt dieser
> Strecken ist Mittelpunkt eines Kreises.*
> *c) $H$ ist ein Punkt.*
>
> — Groemer, Math. Z. 73 (1960), p. 285.

That is: equality iff the region is the convex hull of the circles *and* the hull $H$ of the centres
either decomposes into equilateral triangles of side 2 all of whose vertices are centres, or
decomposes into segments of length 2 all of whose endpoints are centres, or is a single point.

> **Correction (issue #96).** This section previously paraphrased case b) as "$H$ degenerates to a
> segment". That is **weaker than what Groemer prints**: a segment hull is not by itself an equality
> case — the centres must also be spaced exactly 2 apart along it (centres at $0, 2, 5$ give strict
> inequality). Case a) was transcribed faithfully, so nothing built on it is affected.

Page 294 ends "Dies ergibt Teil a) des Satzes", followed immediately by a two-item bibliography.
**"Teil a)" is case a) of that equality clause, not an unread part of the paper** — cases b) and c)
are settled in the preceding sentences. The whole body is the proof of that one inequality, together
with its equality analysis. Now that every page has been read: **there is no application to the
equilateral triangle and no statement about any particular $n$** — previously inferred from the
first and last pages, now confirmed outright.

Two consequences, and the second is the decisive one:

1. Groemer's equality case *characterises* the triangular-lattice configurations, which is why the
   paper looks relevant. But characterising the extremal configuration of a general inequality is
   not the same as proving $s(\Delta(k))$.
2. Applied to our problem in the only direct way — take the convex region to be the containing
   equilateral triangle of side $s$, so $F = \sqrt3 s^2/4$ and $U = 3s$ — the inequality is
   **slack at every triangular $n$**, so it cannot settle those cases:

   | $n$ | Groemer's bound on $s$ | true $s(n)$ | slack |
   |---|---|---|---|
   | 3 | $\ge 5.1038$ | $5.4641$ | $0.360$ |
   | 6 | $\ge 7.2114$ | $7.4641$ | $0.253$ |
   | 10 | $\ge 9.2690$ | $9.4641$ | $0.195$ |
   | 15 | $\ge 11.3051$ | $11.4641$ | $0.159$ |
   | 21 | $\ge 13.3298$ | $13.4641$ | $0.134$ |

   (Equality in Groemer's Satz requires the region to *be* the convex hull of the circles, which a
   containing triangle never is, so strictness here is expected rather than surprising.)

   > **Which region this table evaluates — read this before citing it (issue #96).** The rows above
   > apply Groemer to the **containing equilateral triangle**. On that region he is slack, and the
   > conclusion drawn from it — that Groemer's paper credits no particular $n$ — is correct and
   > unaffected. But that is not the only region he can be applied to, and the slack is an artefact
   > of the choice. Applied instead to $K = H \oplus B_1$, the **outer-parallel body of the hull $H$
   > of the centres**, Steiner's formulas make every $\pi$ cancel and the Satz becomes
   > $n \le \tfrac{\sqrt3}{6}A(H) + \tfrac14 M(H) + 1$ — which, rescaled from Groemer's separation 2
   > to separation 1, is **exactly Oler's inequality at $\pi = \mathrm{conv}(E)$**, tight at every
   > triangular $n$. Do not read this table as saying Groemer's Satz is weaker than Oler's
   > inequality; on the right region they are equivalent. Derivation, scope and the
   > equality-characterisation consequences:
   > [`attacks/groemer-oler-equivalence/`](attacks/groemer-oler-equivalence/README.md).

   **Status of this table: `sketch`** — it is arithmetic done here, from Groemer's inequality as
   printed on p. 285, not something Groemer or anyone else states. It is offered as a consistency
   check on the rejection, not as its foundation. The foundation is simply that the paper contains
   no result about triangles. (The five rows are reproduced exactly by
   `attacks/groemer-oler-equivalence/derive.py`, which recomputes them in exact symbolic arithmetic.)

The tables above therefore continue to credit **Oler alone**, now as a checked conclusion rather
than a flagged guess. Graham & Lubachevsky ("it was first shown by Oler in 1961") agree; Friedman's
co-credit appears to be an attribution of the *underlying tool* rather than of the result.

### Provenance of every source used (per PR #21's convention)

| Source | How it was used |
|---|---|
| **Groemer, Math. Z. 73 (1960) 285–294.** | **Primary, READ IN FULL** (all ten pages, from the GDZ scan; issue #96). Supersedes the earlier partial reading of pp. 285 and 294 only. Confirms the Satz, its full three-case equality clause, and that the paper contains no application to the triangle. Locators in [`attacks/groemer-oler-equivalence/`](attacks/groemer-oler-equivalence/README.md) §1. |
| **Payan, Discrete Math. 165–166 (1997) 555–565.** | **Primary abstract only.** French *Résumé* and English *Abstract* transcribed verbatim from the publisher's own article page. **Body NOT obtained.** |
| **Melissen, Amer. Math. Monthly 100 (1993) 916–925.** | **NOT read** (JSTOR, paywalled). Contents established from the zbMATH review Zbl 0814.52006, quoted above — a review *of* the primary, i.e. still secondary. |
| **Melissen, Acta Math. Hungar. 65 (1994) 389–393.** | **NOT read** (Springer, paywalled). Its scope is taken from its title plus the 1993 review's "the case $n = 11$ is announced". |
| **Oler, Canad. Math. Bull. 4 (1961) 153–155.** | **Read in full** (open PDF at Cambridge Core); also read in full by the worker on issue #17, see `attacks/oler-lower-bound/`. |
| **Joós, Aequat. Math. 95 (2021) 35–65.** | **NOT read** (Springer, paywalled). Its $t_{13}$ value comes via Tedeschi & Mackey and is independently corroborated by the $t_{13}$ arithmetic check in §"Resolution of the source conflict". |
| Tedeschi & Mackey, AJUR 18(2) (2021) 3–12. | **Read in full**, open access. **Secondary.** Its introduction is where this file's $n = 20$ claim originally came from; its abstract omits $n = 20$ without denying it. See the $n = 20$ section. |
| Melissen & Schuur, Discrete Math. 145 (1995) 333–342. | **Read** (open copy at ris.utwente.nl). Secondary for the attribution sentence. |
| zbMATH Open (Zbl 0814.52006, Zbl 0897.52003, Zbl 0100.36601). | **Reviews and metadata**, read via the zbMATH Open API. Secondary. Also the route by which the Groemer scan was found. |
| Wikipedia; Friedman's Packing Center. | **Cross-checks only.** Neither is relied on for any status in the tables. |

### Remaining gaps (honest accounting)

- **Payan's body was not obtained**, so the $k = 6$ / $n = 20$ attribution has been checked only
  as far as the abstract, and the argument itself not at all. What was tried:
  ScienceDirect (HTTP 403 / bot challenge, direct and via a reader proxy — the article is marked
  "Open archive", so a human with a browser can very likely just download it), Unpaywall
  (`oa_status: closed`, no repository copy), Crossref (no abstract), CORE (0 hits),
  scholar.archive.org (bot-blocked), Semantic Scholar (abstract elided by publisher), HAL and a
  search for an IMAG/LSD2 technical-report preprint (nothing), Google Scholar caches, ResearchGate.
  **A single library PDF closes this gap; nothing clever is needed.**
- **Neither Melissen paper's body was obtained.** The per-$n$ split now rests on a zbMATH review
  rather than on inference from two surveys — better, still not the paper.
- **Melissen's 1997 Utrecht thesis** *Packing and covering with circles* could **not** be obtained;
  no accessible full text was found (searched again 2026-08).
- **Joós (2021) was not read.** The $n = 13$ row rests on the $t_{13}$ arithmetic cross-check in
  "Resolution of the source conflict" above, plus Tedeschi & Mackey.
- $16 \le n \le 19$ and $22 \le n \le 34$ attributions are coarse; only the proven/best-known
  boundary was checked, not the per-$n$ credit.

### The Erdős–Oler conjecture

For a triangular number $\Delta(k) = k(k+1)/2$, removing one circle from an optimal
$\Delta(k)$-packing still gives an optimal packing: $s(\Delta(k) - 1) = s(\Delta(k))$.

Status: **proven for $k \le 6$**, i.e. for $n = 2, 5, 9, 14, 20$. Cases $k \le 4$ are in Melissen
(1993); $k = 5$ is Payan (1997); **$k = 6$ ($n = 20$) is Payan's too, his abstract stating that the
same proof extends to it "de manière un peu plus laborieuse" — an attribution checked here as far
as the abstract and no further**, see
[The $n = 20$ attribution](#the-n--20-attribution--qualified). Open for $k \ge 7$. Rows $n = 15/14$
and $n = 10/9$ above exhibit exactly this. Graham & Lubachevsky (1995) attribute the conjecture to
D. J. Newman (private communication) "among others"; Melissen & Schuur (1995) attribute it to
Oler, Fejes Tóth and Newman.

Graham and Lubachevsky conjectured seven further infinite families of optimal packings, covering
cases including $n = 37, 40, 42, 43, 46, 49$.

## Sources

### Optimality proofs (the citations behind the table)

- N. Oler, *A finite packing problem*, Canad. Math. Bull. **4** (1961) 153–155.
  [doi:10.4153/CMB-1961-018-7](https://doi.org/10.4153/CMB-1961-018-7) — the Oler inequality,
  the main lower-bound tool; settles all triangular $n = \Delta(k)$.
- J. B. M. Melissen, *Densest packings of congruent circles in an equilateral triangle*,
  Amer. Math. Monthly **100** (1993) 916–925.
  [doi:10.2307/2324212](https://doi.org/10.2307/2324212) — per zbMATH Zbl 0814.52006, proves
  optimality *and uniqueness* for $n = 2,\dots,10$ and $n = 12$, plus $n = \Delta(k)$, and
  *announces* $n = 11$; also states the $n = 13, 14, 17, 19$ conjectures.
- J. B. M. Melissen, *Optimal packings of eleven equal circles in an equilateral triangle*,
  Acta Math. Hungar. **65** (1994) 389–393.
  [doi:10.1007/BF01876040](https://doi.org/10.1007/BF01876040) — $n = 11$.
- C. Payan, *Empilement de cercles égaux dans un triangle équilatéral. À propos d'une conjecture
  d'Erdős–Oler*, Discrete Math. **165–166** (1997) 555–565.
  [doi:10.1016/S0012-365X(96)00201-4](https://doi.org/10.1016/S0012-365X\(96\)00201-4) —
  **$n = 14$** ($k = 5$); its abstract also states that the proof extends to $k = 6$ ($n = 20$).
  **Cite it for $n = 20$ only with that qualification attached** — the body has not been read here,
  so how the $k = 6$ case is discharged is unknown. Marked "Open archive" on ScienceDirect, so it
  should be freely downloadable in a browser.
- A. Joós, *Packing 13 circles in an equilateral triangle*, Aequat. Math. **95** (2021) 35–65
  (online 2 Sept 2020). [doi:10.1007/s00010-020-00753-y](https://doi.org/10.1007/s00010-020-00753-y)
  — $n = 13$, the last open case below 16.
- R. Milano, *Configurations optimales de disques dans un polygone régulier*, mémoire de licence,
  Université Libre de Bruxelles (1987) — $n \le 6$; unpublished, not consulted.
- H. Groemer, *Über die Einlagerung von Kreisen in einen konvexen Bereich*, Math. Z. **73** (1960)
  285–294. [doi:10.1007/BF01159721](https://doi.org/10.1007/BF01159721);
  [**free scan at GDZ**](http://gdz.sub.uni-goettingen.de/dms/resolveppn/?PPN=GDZPPN002389444).
  A single general inequality $n\sqrt{12} \le F - \varkappa U + \lambda$ for unit circles in a
  convex region. **Does not treat the triangle and settles no particular $n$** — it is not a
  citation for any row above; see [Groemer](#groemer-1960--co-credit-rejected).

### Constructions and surveys

- Graham & Lubachevsky, *Dense packings of equal disks in an equilateral triangle: from 22 to 34
  and beyond*, Electron. J. Combin. **2** (1995) #A1 —
  [**open access**](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v2i1a1).
  Source of the 22–34 records plus the infinite families, and describes the billiard-simulation
  method worth reusing. Its introduction is the snapshot of what was proven as of 1995.
- Melissen & Schuur, *Packing 16, 17 or 18 circles in an equilateral triangle*, Discrete Math.
  **145** (1995) 333–342 —
  [PDF](https://ris.utwente.nl/ws/files/6509759/Melissen95packing.pdf). Its introduction gives the
  attribution of the small cases.
- N. Tedeschi, *On Packing Thirteen Points in an Equilateral Triangle*, Amer. J. Undergrad. Res.
  **18**(2) (2021) 3–12 —
  [PDF](https://www.ajuronline.org/uploads/Volume_18_2/AJUR_Vol_18_Issue_2_Sept_2021p3.pdf).
  Useful for its history paragraph; works towards a discrete reproof of Joós's theorem.
  **Handle its history with care** — not because it is inconsistent (it is not; its abstract omits
  $n = 20$ rather than denying it), but because it is a survey, and a survey's summary is not a
  warrant. It was this file's original, unqualified source for $n = 20$.
- zbMATH Open — [Zbl 0814.52006](https://zbmath.org/?q=an:0814.52006) (review of Melissen 1993),
  [Zbl 0897.52003](https://zbmath.org/?q=an:0897.52003) (review of Payan 1997),
  [Zbl 0100.36601](https://zbmath.org/?q=an:0100.36601) (Groemer 1960, no review text). Free, and
  its API returns review text and links to open scans. It is where the Melissen split was settled
  and where the GDZ scan of Groemer was found. Reviews are **secondary**.
- Melissen, *Packing and covering with circles*, PhD thesis, Utrecht University (1997) — the most
  complete account of the small-$n$ proofs. **No accessible full text was found** as of 2026-08.

### Tables (secondary — verify before relying on them)

- [Circle packing in an equilateral triangle — Wikipedia](https://en.wikipedia.org/wiki/Circle_packing_in_an_equilateral_triangle)
  — its "proved for $n \le 15$" claim is correct. It cites Payan, and summarises only the
  contiguous range: it neither claims nor denies $n = 20$.
- [Erich Friedman, Packing Center — circles in triangles](https://erich-friedman.github.io/packing/cirintri/)
  — per-$n$ diagrams and exact side lengths, all of which check out; but the *status* markers are
  **stale**: $n = 13$ and $n = 14$ are still shown as "Found by", and the 1993/1994 credits for
  $n = 11, 12$ are swapped.
- [Erich's Packing Center (index)](https://erich-friedman.github.io/packing/) — the sibling problems.
- [Packomania](http://www.packomania.com/) — maintained record tables for related packing problems;
  check before claiming any record.

## Layout

- `RULES.md` — how work on this problem must be done. Certificates, not screenshots.
- `attacks/` — one directory per approach.
- `results/` — verified constructions and optimality results.
