# n16-verification-5 — independent exact check of the n = 16 upper-bound certificate

**Role: verification** (repo [`RULES.md`](../../../../RULES.md) §8 convergent lane). Nothing new
is *constructed* here. This lane re-derives, from the problem statement only, whether
[`../n16-upper-2/n16-certificate.json`](../n16-upper-2/n16-certificate.json) is what it says it is.

- Verifier: `claude`, worker **V5**, model **Opus 5**, 2026-08-22 · issue #97 · branch
  `claude/circle-packing-subagents-9yg5gt`
- Certificate under review: authored by worker **U2**, model **Fable 5** (a decorrelated
  intra-agent pairing, `RULES.md` §8 — but *not* a different model **family**, see §7 below)
- My checker: [`experiments/packing-n16-verify-5/`](../../../../experiments/packing-n16-verify-5/),
  written from `problems/circle-packing-equilateral-triangle/README.md` + `RULES.md` §2 alone.
  U2's `exact_gate.py` was **not read, imported, or adapted** (problem `RULES.md` §3.2). U2's
  prose `README.md` was read for its *claims* only, after my checker was written and run.

## Verdict in one line

**Confirmed.** The certificate is a valid exact construction certificate for
$s(16) \le 9249527159013717/10^{15} + 2\sqrt3 = 12.7136287741514715870548\ldots$, it is **not
tight** (by $3.08\times10^{-14}$, as U2 itself states), and every number U2 reports that I could
recompute, I recomputed to the digit. No correction to the certificate is required.

---

## 1. What I reimplemented, and how

Working in `fractions.Fraction` and in $\mathbb{Q}(\sqrt3)$ (pairs $a + b\sqrt3$ with an exact
sign routine). **No float decides anything**; floats and a `math.isqrt`-based decimal renderer
appear only in printed magnitudes. `numpy`/`scipy` appear only in the *side note* of §6 and decide
nothing.

Derived independently from the problem `README.md` and `RULES.md` §2, before opening any sibling
lane:

- **Reduction.** $n$ unit circles in a triangle of side $s$ $\iff$ $n$ points at pairwise distance
  $\ge \mathbf{2}$ in a triangle of side $d = s - 2\sqrt3$. Separation **two**, not one — the
  standing trap (`FINDINGS.md`); corruption 10 below is the regression test for it.
- **Placement**, fixed, no search over rigid motions: $A=(0,0)$, $B=(d,0)$,
  $C=(d/2, d\sqrt3/2)$.
- **Containment**, each edge oriented by the opposite vertex:
  $y \ge 0$; $\sqrt3\,x - y \ge 0$ (edge $AC$, oriented by $B$); $\sqrt3(d-x) - y \ge 0$
  (edge $BC$, oriented by $A$). All **non-strict**.
- **Minimal enclosing side at the fixed placement.** Only the $BC$ constraint involves $d$:
  $\sqrt3(d-x_i) \ge y_i \iff d \ge x_i + y_i/\sqrt3$. The other two constraints are $d$-free.
  Hence, given $y_i \ge 0$ and $\sqrt3 x_i \ge y_i$ for all $i$,
  $$d_{\min} \;=\; \max_i\Big(x_i + \tfrac{y_i}{3}\sqrt3\Big),$$
  and the certificate is **tight** iff $d = d_{\min}$. I derived this before reading U2's §4 and
  landed on the same expression; see §3.

### The squaring step U2 asked to be attacked

U2 flags the encoding $\sqrt3\,x \ge y \iff x \ge 0 \wedge 3x^2 \ge y^2$ as the one place a sign
slip voids the certificate. I checked the **equivalence itself** rather than assuming it:

- **($\Leftarrow$), the soundness direction — holds with no hypothesis on $y$.** If $x \ge 0$ and
  $3x^2 \ge y^2$ then $\sqrt3 x = \sqrt{3x^2} \ge \sqrt{y^2} = |y| \ge y$. So the encoding can
  never **accept** a point outside edge $AC$. (Randomised over 4000 rational points: 0 false
  accepts.)
- **($\Rightarrow$), the completeness direction — needs $y \ge 0$.** From $\sqrt3 x \ge y \ge 0$
  we get $x \ge 0$, and squaring two non-negatives preserves the order. Without the $y \ge 0$
  gate the implication fails, e.g. $x = -1, y = -5$: $\sqrt3 x \ge y$ holds but $x \ge 0$ does
  not. So a checker missing that gate is over-strict, not unsound.
- **The dangerous mutant is dropping the `x >= 0` guard**, not dropping $y \ge 0$. Corruption 13
  exhibits a point that the guardless form $3x^2 \ge y^2$ **accepts** and the exact
  $\mathbb{Q}(\sqrt3)$ test **rejects**.

Rather than rely on the equivalence at all, my checker runs **both** encodings on every point and
gates on their agreement (G3.1/G3.2). They agreed on all 16 points and on 4000 random rational
points.

---

## 2. Item-by-item verdicts

### 2.1 Pairwise separation

```
checked:      all C(16,2) = 120 squared distances recomputed in exact Fraction arithmetic from
              the certificate's rational coordinates; each compared against 4 (separation 2).
              Exact minimum, at pair (4,11):
                 4000000000000720532000000032447897689 / 10^36  =  4 + 7.205320e-13.
not-checked:  nothing.
verdict:      confirmed.  Matches U2's reported "4 + 7.2e-13" exactly.
```

### 2.2 Containment in the closed triangle

```
checked:      all 16 points against the three closed half-planes at the FIXED placement, twice:
              (a) exact Q(sqrt3) sign arithmetic, (b) the squared encoding, with the equivalence
              proved and randomised-tested rather than assumed (see s1).  Both encodings agree
              on all 16 points; 0 violations.  The tightest wall residual is 5.34e-14 (three
              points sitting at the triangle's vertices, 5.34e-14 inside).
not-checked:  nothing.
verdict:      confirmed.  The encoding U2 flagged is sound; the guard that matters is `x >= 0`.
```

### 2.3 `side_length` is a genuine upper bound, and tightness

```
checked:      d = s - 2*sqrt(3) parsed exactly and shown rational.  Exact minimal enclosing side
              at the fixed placement, derived independently (s1):
                 d_min = 125533377979040259/(2*10^16) + (5149141550127628529/(3*10^18))*sqrt(3)
                       = 9.2495271590136861685589...   (attained at point 0)
                 d     = 9249527159013717/10^15
                       = 9.2495271590137170000000
                 d - d_min = 3.0831e-14  > 0
              s_min = d_min + 2*sqrt(3) = 12.7136287741514407556138...
not-checked:  the minimal enclosing equilateral triangle over RIGID MOTIONS.  RULES.md s2 forbids
              that search, so "minimal enclosing" here means minimal at the fixed placement; a
              rotated/translated triangle could in principle be smaller and would not count.
verdict:      confirmed.  d >= d_min, so s is a valid upper bound.
              TIGHTNESS: NOT TIGHT, by 3.08e-14 in d (= in s).  This is an honest upper bound,
              exactly as U2 claims it (its "~3.1e-14" is my 3.0831e-14, and its printed d_min
              expression is character-for-character the one I derived).  No record is claimed and
              none could be: RULES.md s4 requires tightness for a record claim.
```

### 2.4 Encoding hygiene

```
checked:      every coordinate string parsed under a strict grammar accepting ONLY
              [+-]?digits(/digits)? -- no decimal point, no exponent, no radical.  All 32 strings
              pass, so `coordinate_type: "rational"` matches the actual encoding.  side_length
              parsed under a grammar accepting only sums of <rational> and <rational>*sqrt(3):
              "9249527159013717/1000000000000000 + 2*sqrt(3)" is exact, not a decimal string.
              n == len(coordinates) == 16; claim == "construction".
not-checked:  `verified_by`, `status`, `beats_record`, `side_length_note` are prose/metadata and
              are not load-bearing (U2 says the same).  I did confirm side_length_note's decimal
              12.71362877415147158705 is correct to all 20 printed places -- a Python float
              cannot render it, so a naive check would flag a false discrepancy at the 14th digit.
verdict:      confirmed.
```

### 2.5 Placement convention

```
checked:      the certificate is checked at A=(0,0), B=(d,0), C=(d/2, d*sqrt3/2) with NO search
              over rigid motions; corruption 12 confirms my checker rejects a translated copy of
              the same packing rather than re-fitting the triangle to it.
not-checked:  nothing.
verdict:      confirmed.
```

---

## 3. Corruption-rejection table

Full machine output in
[`experiments/packing-n16-verify-5/verify.log`](../../../../experiments/packing-n16-verify-5/verify.log)
(section 2). Every defect is injected into the real certificate and re-run through my checker.

| # | corruption | magnitude | checker response | outcome |
|---|---|---|---|---|
| 0 | unmodified certificate | — | **accepted**, all gates pass | control OK |
| 1 | pair $(4,11)$ pushed into overlap | $\mathrm{dist}^2 = 4 - 3.28\times10^{-12}$, i.e. distance short of 2 by $\sim10^{-12}$ | rejected by **G2.1** | OK |
| 2 | point 2 pushed below edge $AB$ | $y = -9.7\times10^{-13}$ | rejected by **G3.1, G3.2** | OK |
| 3 | point 1 pushed across the **slanted** edge $AC$ | perpendicular distance outside $\approx 10^{-12}$ | rejected by **G3.1, G3.2** (also G2.1 — the displacement needed to clear $AC$ also breaks a contact; the containment gates fire independently) | OK |
| 4 | point 6 pushed across the **slanted** edge $BC$ | perpendicular distance outside $\approx 10^{-12}$ | rejected by **G3.1, G3.2, G4.1** | OK |
| 5 | `side_length` **inflated** by $10^{-3}$ | $d \to d + 1/1000$ | **accepted as feasible** (correctly — an inflated $s$ *is* a true upper bound) but reported `tight=False, d - d_min = 0.001`. The tightness gate is what exposes it, exactly as `RULES.md` §2 intends | OK |
| 6 | `side_length` **deflated** below $d_{\min}$ | $d \to d - 10^{-12}$ | rejected by **G3.1, G3.2, G4.1** | OK |
| 7 | coordinate as a truncated decimal string | `"6.27666889895201295"` | rejected by **G0.4, G0.5** | OK |
| 8 | coordinate in scientific notation | `"4.6248e-14"` | rejected by **G0.4, G0.5** | OK |
| 9 | `side_length` as a decimal string | `"12.71362877415147"` | rejected at parse | OK |
| 10 | **separation-1/2 trap**: whole packing halved | legal at separation 1, illegal at separation 2 | rejected by **G2.1** | OK |
| 11 | `coordinate_type` lies (`"interval"`, payload rational) | — | rejected by **G0.5** | OK |
| 12 | whole packing translated by $(0.1, 0)$ | — | rejected by **G3.1, G3.2, G4.1** (no rigid-motion search) | OK |
| 13 | **discrimination test**: sign-slip mutant checker (`x >= 0` guard dropped) | point mirrored to $x<0$, outside $AC$ | mutant **accepts**; exact $\mathbb{Q}(\sqrt3)$ test **rejects** | OK — the failure mode is real and the guard is what stops it |

Corruptions 3, 4 and 13 are the ones that matter for U2's flagged risk: a containment test broken
on the slanted edges usually still catches the axis-aligned edge $AB$, so #2 alone would prove
nothing.

---

## 4. Adjudication: the rattler and the rigidity count

`attacks/n16-dual` reports: rattler $P_4$ with **one** contact; "21 contacts and 10 wall
contacts"; the other 15 points **isostatic**, 30 constraints on 30 dof.
`attacks/n16-upper-2` reports: rattler with **zero** contacts, $5.3\times10^{-3}$ cage clearance;
20 pair contacts + **13** wall incidences = 33 constraints on 30 dof; rank 30; **hyperstatic by
3**.

I recounted from the certificate coordinates. Active sets are identified with a threshold placed
inside an **exactly exhibited** spectral gap; the rigidity rank is computed by Gauss–Jordan over
the **field** $\mathbb{Q}(\sqrt3)$ — exact, no SVD, no tolerance.

| quantity (my exact recount, certificate coordinates) | value |
|---|---|
| pair contacts (threshold $10^{-6}$ on $\mathrm{dist}^2-4$) | **20** — largest active $7.2\times10^{-13}$, smallest inactive $0.1987$; a $10^{10}$ gap, so the count is threshold-independent |
| wall **incidences** (point, edge) | **13** — largest active residual $5.3\times10^{-14}$, smallest inactive $0.657$ |
| distinct points touching $\ge 1$ wall | **10** |
| points on two edges at once | **3**: $P_2$ at $A$, $P_7$ at $B$, $P_6$ at the apex $C$ (each within $5.4\times10^{-14}$ of the vertex, which is exactly the certificate's contraction offset) |
| rattler | **$P_{13}$, zero pair contacts, zero wall incidences**; nearest neighbours at $\mathrm{dist}^2-4 = 0.1987, 0.2154, 0.3871$, i.e. cage clearance $5.30\times10^{-3}$ in unit-triangle scale |
| rigidity, all 16 points | 33 constraints, 32 dof, **exact rank 30** → 2 flexes (the rattler's two), 3 self-stresses |
| rigidity, 15-point core | 33 constraints, 30 dof, **exact rank 30** → 0 flexes, **3-dimensional self-stress space: hyperstatic by 3** |
| the same core with each corner counted **once** | 30 constraints, 30 dof, exact rank 30 → 0 flexes, 0 self-stresses: **reads as isostatic** |

**Verdict: U2 is right, and n16-dual's numbers are explained rather than merely contradicted.**

1. **The wall count. `10` vs `13` is a count of *points* versus a count of *incidences*.** My
   recount gives both numbers, from the same active set: 13 incidences over 10 distinct points,
   the difference being exactly the 3 corner points. n16-dual's "10 wall contacts" is the
   point count. As a **constraint** count it is wrong: a point at a triangle vertex has two
   independent active edge constraints, with linearly independent normals, and dropping one of
   them is dropping a real row of the rigidity matrix.
2. **The isostatic reading is internally consistent but built on that undercount.** I built the
   "corner counted once" $30\times30$ matrix explicitly: it has exact rank 30, so it does read as
   isostatic. That is why the reading is attractive and why it is nonetheless wrong — the
   constraint set, not the rank computation, is the error.
3. **The rattler's contact count is not an invariant, and I can show it directly.** In the
   certificate's configuration the rattler $P_{13}$ has **zero** contacts and $5.30\times10^{-3}$
   of clearance. In `experiments/circle-packing-search/out/n16.json` (the float file n16-dual
   drew on) the corresponding free point has exactly **one** near-contact, at relative gap
   $1.5\times10^{-10}$ — five orders of magnitude looser than every genuine contact in that same
   file, all of which sit at $\le 1.1\times10^{-15}$ relative. So even there the "contact" is an
   optimiser artifact visible only at a loose tolerance. A point with a single contact is a
   rattler either way: one constraint leaves it 1 of its 2 dof.
4. **Both lanes agree on the substantive claim: 15 jammed points + 1 rattler.** Both are
   `numerical`. Nothing depends on either.

**Caveat I want on the record.** My rank-30 is exact *at the certificate's rational coordinates*,
which sit $\sim10^{-13}$ from the true stationary configuration. Rank is lower semicontinuous, so
rank 30 nearby does **not** prove rank 30 at the limit — it proves rank $\ge 30$ nearby and 30 is
already the column count. The structural statement about the *optimum* therefore remains
`numerical`, as both lanes label it.

---

## 5. Side finding: the certificate and the repo's stored float packing are different configurations

Not part of the mandate; recorded because it bears on §4 and on anything that later assumes "the"
$n=16$ configuration. Comparing the certificate's points (rescaled to the unit triangle) against
`experiments/circle-packing-search/out/n16.json` under all six symmetries of the equilateral
triangle and an optimal assignment: **11 of the 16 points coincide to $<10^{-5}$; four form a
rearranged sub-block** (displacements $0.091$–$0.135$, a swap of the two bottom-edge gaps
$0.35132 \leftrightarrow 0.21623$ together with three interior points), **and the rattler differs
by $9.4\times10^{-3}$ inside the same cage.** Both report a minimum pairwise distance of
$0.2162272693097817\ldots$

So these are two *distinct* configurations with the same minimum distance to 16 digits. Status
`numerical`, and deliberately weak: floats cannot distinguish "equal" from "equal to $10^{-16}$",
so this is **not** a claim of non-uniqueness of the optimum. Its use here is narrower and solid:
the two lanes' contact counts are counts of **different point sets**, which is a second reason
they need not have matched. `numpy`/`scipy` were used for this comparison and for nothing that
decides a result.

---

## 6. Literature cross-check (problem `RULES.md` §4) — provenance labelled

`WebSearch` works in this session; `WebFetch` and direct fetching are blocked at the gateway, so
nothing below was read from a page.

| statement | provenance | status |
|---|---|---|
| Graham–Lubachevsky, *Dense packings of equal disks in an equilateral triangle*, EJC **2** (1995) #A1, is open access and tabulates $d(n)$ to 15 significant digits for their packings | **search-result item** (combinatorics.org listing; also a copy at `fanchung.ucsd.edu/ron/papers/95_01_equilateral.pdf`) | `cited` (bibliographic only) |
| $d(16) = 0.216227269309782$ appears in that paper | **search-backend summary only — NOT obtained.** The backend affirmed the digit string *that I supplied in the query*, which is not independent confirmation and is exactly how a guess gets laundered into a citation. A quoted-string search for `"0.216227269309782"` returned **no** result item containing it | **not obtained** |
| $d(17) = (3-\sqrt3)/6 = 0.211324865405187$ | **search-backend summary**, volunteered *unprompted* (I did not mention $n=17$) while answering a Melissen–Schuur query | `numerical` corroboration — see below |
| Melissen & Schuur, *Packing 16, 17 or 18 circles in an equilateral triangle*, Discrete Math. **145** (1995) 333–342, PDF at `ris.utwente.nl` | **search-result item** (title + URL) | `cited` (bibliographic only) |

**The one genuinely useful triangulation.** The repo's `experiments/circle-packing-search/reference.py`
transcribes GL's table with `17: "0.211324865405187"`. The search backend independently produced
the closed form $(3-\sqrt3)/6$ for $n=17$, which evaluates to $0.21132486540518713$ — agreeing
with that transcription to all 15 printed digits, and I was not asking about $n = 17$. That
corroborates the *transcription* (`reference.py` is an in-repo artifact by an earlier worker, not
a source), and therefore raises confidence in its neighbouring $d(16)$ entry. It is **not**
confirmation of $d(16)$ itself, and I am not upgrading anything on it.

**Exact bracket check** against `cited` values in the problem `README.md`, which the certificate
must respect and does:
$$s(15) = 8+2\sqrt3 = 11.46410\ldots \;\le\; s(16) \;\le\; 12.71362877415147\ldots \;<\; s(17) \le 6+4\sqrt3 = 12.92820\ldots \;<\; s(20) = 10+2\sqrt3 = 13.46410\ldots$$
(the $s(17)$ figure via $s = 2/d(17) + 2\sqrt3$ from the $(3-\sqrt3)/6$ value, itself only
`numerical`). Monotonicity in $n$ holds. Nothing in the certificate is inconsistent with any
`cited` row.

**No citation is invented here.** The honest summary is: the *value* is corroborated by two
in-repo transcriptions and by every optimiser in this repo, and by nothing I could read from a
primary source in this session.

---

## 7. What status this can carry

- The certificate establishes a **construction / upper bound**: $s(16) \le
  9249527159013717/10^{15} + 2\sqrt3$. That is now exactly proved, twice, by two independently
  written checkers, over exact rationals and $\mathbb{Q}(\sqrt3)$.
- It establishes **nothing about optimality**. $s(16) \ge c$ is a separate claim of a different
  kind (problem `RULES.md` §1), and no amount of converging optimiser runs is evidence for it
  beyond `numerical`. The certificate is untight by $3\times10^{-14}$, so it is not even the
  tightest bound its own coordinates support.
- **I cannot grant `verified:review`.** `RULES.md` §5 requires an examiner from a **different
  model family**; U2 is Fable 5 and I am Opus 5 — both Claude. The §8 divergent/convergent split
  is real decorrelation and it is why this check is worth more than U2 re-running its own gate,
  but it is not a family boundary. **The certificate stays `numerical`** until Codex writes its
  own checker per problem `RULES.md` §3.
- What this lane *is*: an independent reimplementation satisfying problem `RULES.md` §3.2–§3.3
  and, if that route is ever needed, the "independently reconstructed or reimplemented" standard
  for the exceptional same-agent non-claim audit (`RULES.md` §5) — which still could not promote
  the claim.

## 8. Corrections

**None to the certificate.** Every load-bearing number U2 reports, I reproduced exactly:
the minimum $\mathrm{dist}^2 = 4 + 7.2\times10^{-13}$; the closed form of $d_{\min}$; the
untightness $\approx 3.1\times10^{-14}$; 20 pair contacts; 13 wall incidences; 3 corner points;
rank 30; 3 self-stresses; rattler with 0 contacts and $5.3\times10^{-3}$ clearance.

Two notes, neither a defect:

1. **`n16-dual`'s "10 wall contacts" and "isostatic" should be read as superseded**, with the
   reason recorded in §4: it is a count of points, not of constraints, and the corner points each
   carry two. I have not edited that lane's file (not mine to write).
2. **`side_length_note`'s decimal is correct and a naive checker will think it is not.** IEEE
   doubles cannot represent $12.71362877415147158705\ldots$ to the 14th decimal; a checker that
   renders $d + 2\sqrt3$ in float will disagree with the note at $\sim1.6\times10^{-13}$ and may
   report a phantom error. Mine renders via `math.isqrt` at 40 digits and confirms the note to
   all 20 printed places.

## 9. Reproduce (one command)

```sh
sh experiments/packing-n16-verify-5/verify.sh
```

CPython 3.11.15, **standard library only** for every exact gate (`fractions`, `math.isqrt`, `re`,
`json`); `numpy` 2.4.6 / `scipy` 1.17.1 are imported only by the §5 side note and decide nothing.
Deterministic — the one randomised component (the containment-equivalence sweep, G3.3/G3.4) is
seeded with `20260822`. Runtime $\approx 3$ s on one core. Exit status 0 iff every gate and every
corruption behaves as required. Stored output:
[`experiments/packing-n16-verify-5/verify.log`](../../../../experiments/packing-n16-verify-5/verify.log).
