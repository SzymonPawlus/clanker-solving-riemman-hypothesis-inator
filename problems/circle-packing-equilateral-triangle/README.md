# Circle packing in an equilateral triangle

**Status:** open for most $n$. Optimality is proven for **all $n \le 15$**, for every triangular
number $n = k(k+1)/2$, and for $n = 20$; everything else is best-known-construction.

Shared conventions: [`../README.md`](../README.md). Repo-wide protocol:
[`../../RULES.md`](../../RULES.md). **Problem-specific rules: [`RULES.md`](./RULES.md) — read
before working on this problem.**

## Statement

Pack $n$ unit circles into the smallest possible equilateral triangle. Write $s(n)$ for the
minimal side length.

$s(n)$ is settled for $n \le 15$, for all triangular $n$, and for $n = 20$; see the table below.
There is no known closed form for general $n$.

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

| $n$ | $s(n)$ | Optimality proved by | Reference |
|---|---|---|---|
| $\Delta(k) = \tfrac{k(k+1)}{2}$ | $2(k-1) + 2\sqrt{3}$ | Oler (1961) | Canad. Math. Bull. **4**, 153–155 |
| 20 $= \Delta(6) - 1$ | $10 + 2\sqrt{3} \approx 13.464$ | Payan (1997) | Discrete Math. **165–166**, 555–565 |

### Best known only (optimality *not* established) — status `numerical`

| $n$ | best known $s(n)$ | Construction due to |
|---|---|---|
| 16, 17, 18 | various | Melissen & Schuur (1995), Discrete Math. **145**, 333–342 |
| 19 | — | pre-1995 literature; see Graham & Lubachevsky (1995), which reproduces it |
| 22–34 | various | Graham & Lubachevsky (1995), Electron. J. Combin. **2**, #A1 |

($n = 20$ and $n = 21 = \Delta(6)$ are *proven*, not best-known — see the table above.)

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
   - $n = 14$: **C. Payan (1997)**, proving the Erdős–Oler conjecture for $k = 5$ (and $k = 6$,
     giving $n = 20$).
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
   are **not** verified here (see gaps below).

Consistency check on $n = 13$: Joós states the maximum separation of 13 points in a unit-side
triangle as $t_{13} = 9 - 5\sqrt{3} - \tfrac{7\sqrt{6}}{2} + 6\sqrt{2} \approx 0.2518132$. Via
$s = 2\sqrt{3} + 2/t_{13}$ this gives $11.40649585375161$, against
$4 + \tfrac{2\sqrt{6}}{3} + \tfrac{10\sqrt{3}}{3} = 11.40649585375171$ — agreement to $10^{-13}$,
confirming Joós proved optimality of exactly the value tabulated above.

### Remaining gaps in the attribution (honest accounting)

Resolved enough to mark the table `cited`, but these specific points were **not** verified
against a full text and should not be built on:

- **Which paper contains which small case.** The per-$n$ split of $\{4,5,7,8,9,12\}$ into
  Melissen 1993 is *inferred*, not read: Melissen & Schuur (1995) says optimal packings were
  determined "for $n \le 6$ by Milano, and by the first author for $n \le 12$ [Monthly 1993, Acta
  1994]", and Graham & Lubachevsky (1995) says the known non-triangular cases are
  $n = 2,4,5,7,8,9,11,12$ citing the same two papers. Since the Acta paper's title is confined to
  $n = 11$, the rest must be in the Monthly paper. Neither paper's body was read.
- **Payan's $n = 20$ result** comes from the publisher's abstract (via search summary) and from
  Tedeschi (2021), not from the paper itself. Its $n = 14$ result is corroborated by both.
- **Groemer.** Friedman co-credits "Oler/Groemer" ($n = 6, 10$) and "Erdős/Groemer" ($n = 15$).
  Graham & Lubachevsky credit Oler alone ("It was first shown by Oler in 1961"). Groemer,
  *Über die Einlagerung von Kreisen in einen konvexen Bereich*, Math. Z. **73** (1960) 285–294,
  exists and is closely related, but its exact contribution to these cases was **not** checked.
  The tables above therefore credit Oler only.
- **Melissen's 1997 Utrecht thesis** *Packing and covering with circles*, named in the issue as the
  place to look, could **not** be obtained — no accessible full text was found. The resolution
  above rests on the journal literature instead.
- $16 \le n \le 21$ were not researched beyond confirming that the constructions are unproven;
  the "best known" table's attributions there are coarse.

### The Erdős–Oler conjecture

For a triangular number $\Delta(k) = k(k+1)/2$, removing one circle from an optimal
$\Delta(k)$-packing still gives an optimal packing: $s(\Delta(k) - 1) = s(\Delta(k))$.

Status: **proven for $k \le 6$**, i.e. for $n = 2, 5, 9, 14, 20$. Cases $k \le 4$ are in Melissen
(1993); $k = 5$ and $k = 6$ are Payan (1997). Open for $k \ge 7$. Rows $n = 15/14$ and $n = 10/9$
above exhibit exactly this. Graham & Lubachevsky (1995) attribute the conjecture to
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
  [doi:10.2307/2324212](https://doi.org/10.2307/2324212) — the non-triangular cases
  $n \le 12$ except $n = 11$; also states the $n = 13, 14, 17, 19$ conjectures.
- J. B. M. Melissen, *Optimal packings of eleven equal circles in an equilateral triangle*,
  Acta Math. Hungar. **65** (1994) 389–393.
  [doi:10.1007/BF01876040](https://doi.org/10.1007/BF01876040) — $n = 11$.
- C. Payan, *Empilement de cercles égaux dans un triangle équilatéral. À propos d'une conjecture
  d'Erdős–Oler*, Discrete Math. **165–166** (1997) 555–565.
  [doi:10.1016/S0012-365X(96)00201-4](https://doi.org/10.1016/S0012-365X\(96\)00201-4) —
  $n = 14$ and $n = 20$.
- A. Joós, *Packing 13 circles in an equilateral triangle*, Aequat. Math. **95** (2021) 35–65
  (online 2 Sept 2020). [doi:10.1007/s00010-020-00753-y](https://doi.org/10.1007/s00010-020-00753-y)
  — $n = 13$, the last open case below 16.
- R. Milano, *Configurations optimales de disques dans un polygone régulier*, mémoire de licence,
  Université Libre de Bruxelles (1987) — $n \le 6$; unpublished, not consulted.

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
- Melissen, *Packing and covering with circles*, PhD thesis, Utrecht University (1997) — the most
  complete account of the small-$n$ proofs. **No accessible full text was found** as of 2026-08.

### Tables (secondary — verify before relying on them)

- [Circle packing in an equilateral triangle — Wikipedia](https://en.wikipedia.org/wiki/Circle_packing_in_an_equilateral_triangle)
  — its "proved for $n \le 15$" claim is correct.
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
