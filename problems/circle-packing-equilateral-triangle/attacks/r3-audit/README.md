# R3-Z — Novelty and corrections audit

```
claim type: NEITHER construction nor optimality. This file asserts no bound on s(n).
            It is a literature/provenance audit plus four arithmetic re-derivations.
status:     sketch  — every statement in this file, except where a line is explicitly
            tagged `cited`, and except the arithmetic in §5 which is `numerical`
            (reproducible, exact, but a computation and not a proof).
author:     claude (Opus 5), worker r3-audit, 2026-08-23
executes:   proposal Z of ../r3-approaches/README.md; corroborates its §0.1 and §0.2
issue:      #110 (round-3 triage); findings route to #97, #110, #13
```

**Read this first.** Nothing here may be cited or built on (`RULES.md` §3). The audit's
*negative* results — "still cannot read it" — are the deliverable, not a shortfall.

---

## 0. Evidence tiers used throughout

Every literature statement below carries exactly one tag. This is the whole point of the task:
`FINDINGS.md` records a prior failure in which this project attributed a result to a paper whose
body nobody opened.

| Tag | Meaning |
|---|---|
| **(i) read in full** | the body of the source was actually opened and read here |
| **(ii) abstract only** | a publisher-side or repository-side abstract was obtained; body not opened |
| **(iii) search-snippet** | text reached us only through a `WebSearch` result summary — a language model's rendering of an indexed page, *not* the page |
| **(iv) secondary** | a different paper/survey/review characterising the source |
| **(v) inference** | this project's own reasoning from the above |

**Nothing in this audit reaches tier (i).** Every external host that could have supplied a body
is blocked (§1). Tier (iii) is the ceiling reached today, with one item at the (ii)/(iii)
boundary. Accordingly **no claim in this file is `cited`.**

A caution about tier (iii) that the round-3 triage already flagged and this audit confirms: a
search-result summary is generated text. Three renderings agreed here (§2), which is *evidence*,
but three renderings of the same indexed page are not three independent sources.

---

## 1. The blocker, reported and not routed around

`RULES.md` and `/root/.ccr/README.md` agree: an egress 403/407 is an organization policy denial,
**"Do not retry or route around it — report the blocked host."** This audit did not.

Blocked hosts, with first-party evidence. The proxy's own status endpoint
(`curl -sS "$HTTPS_PROXY/__agentproxy/status"`, run at the top of this session) still carries the
three CONNECT denials recorded during round-3 ideation:

| Host | Proxy verdict | Recorded at |
|---|---|---|
| `www.packomania.com:443` | `connect_rejected` — "gateway answered 403 to CONNECT (policy denial or upstream failure)" | 2026-08-23T20:19:32Z |
| `pp.bme.hu:443` | `connect_rejected` — same | 2026-08-23T20:20:28Z |
| `www.math.ucsd.edu:443` | `connect_rejected` — same | 2026-08-23T20:23:52Z |

**New this session — and it corrects the triage file.** Proposal Z.4 says *"arxiv.org may be
reachable; try."* It was tried, exactly once:

```
WebFetch https://arxiv.org/abs/2212.12287
  -> {"error_type":"EGRESS_BLOCKED","domain":"arxiv.org",
      "message":"Access to arxiv.org is blocked by the network egress proxy."}
```

**`arxiv.org` is blocked.** It is not retried here and it was not attempted through a second
channel (`curl` through the same proxy would be the same policy layer, i.e. a retry). Add it to
the blocked list. Note that `attacks/oler-lower-bound/README.md` records an *earlier* session
having "read the relevant sections" of arXiv:2212.12287 — so the block is new relative to that
work, and any future worker who reads that line should not conclude arXiv is reachable now.

`WebSearch` works. `WebFetch` was 5-for-5 blocked across this session and the last.

### 1.1 The exact questions a human with library access should answer

Stated so they can be answered without re-reading this file. **Q1 is the one that matters.**

> **Q1 (decides novelty at n = 16).** In Gáspár & Tarnai, *Periodica Polytechnica Ser. Civ. Eng.*
> **44**:1 (2000) 13–32, in the table of upper bounds of maximum packing density for the
> **equilateral triangle**: what is the printed numerical bound on the **row n = 16**?
> Also print rows n = 17, 18, 22–30, and copy the closed-form formula for the triangle.
>
> *Why it decides anything:* re-derived in §5.2 below, a density upper bound `D` for n = 16
> converts to `s(16) >= 2*sqrt(16*pi/(sqrt3*D))`. Their row beats this repo's unmerged sketch
> bound `s(16) >= 2+6sqrt3` **iff their number is `<= 0.75590121366`**.
>
> *Direct link (blocked from here, fine from a browser):* `https://pp.bme.hu/ci/article/view/648`,
> PDF at `https://pp.bme.hu/ci/article/download/648/403/4701`. Also on ResearchGate,
> publication 266884543.

> **Q2 (settles the load-bearing word).** In the same paper: are the triangle bounds asserted as
> **theorems** (rigorous, with proof), or are they explicitly qualified as *heuristic* /
> *conjectural* in the body — and if heuristic, exactly which step is not proved? The abstract's
> first sentence appears to read "The paper gives **heuristic** upper bounds…" (see §2), but the
> abstract's word choice does not by itself tell us whether the triangle table is a theorem.

> **Q3.** Nurmela & Östergård, *Discrete Comput. Geom.* **22** (1999) 439–457: confirm from the
> body that optimality for n ≤ 27 in the **square** is proved by subdividing the square into
> tiles, enumerating which tiles are occupied, and eliminating occupancy combinations that admit
> no valid separation. Record what makes the elimination rigorous, and the tile count / running
> time. (`https://doi.org/10.1007/PL00009472`)

> **Q4.** Payan, *Discrete Math.* **165–166** (1997) 555–565: the standing gap from
> `../../README.md` — is the k = 6 (n = 20) case written out in the body? Unchanged by this audit
> and still open; listed here so one library trip closes everything at once.

---

## 2. Lead 1 — Gáspár & Tarnai (2000): **NOT RESOLVED. Blocked and unread.**

**Verdict: this audit cannot determine whether Gáspár–Tarnai publishes an n = 16 bound at least
as strong as the repo's `s(16) >= 2+6sqrt3`.** `pp.bme.hu` is 403 at the egress proxy. The
standing instruction of proposal Z is unchanged and is repeated here as the operative one:

> **Assume the Gáspár–Tarnai n = 16 bound is already known and possibly stronger, until a human
> reads that table line.** Do not claim novelty for the n = 16 lower bound in any PR, issue, or
> file until Q1 is answered.

### 2.1 What was actually obtained (all tier (iii), one arguably (ii)/(iii))

Three separate `WebSearch` queries returned renderings of the article's abstract. The longest and
most complete, which reads as a full verbatim abstract rather than a paraphrase:

> The paper gives **heuristic** upper bounds for the density of packings of non-overlapping equal
> circles in a square, an equilateral triangle, and a circle. The area of interstices at the
> boundary of these domains is calculated with greater precision than by other authors, so the
> obtained upper bounds are sharper than those known before. Because the function int (x) appears
> in the relationships, the upper bounds are not monotonous functions of the circle number. Not
> only the formulae of upper bounds of the maximum packing density are given, but their numerical
> values are listed up to 30 circles.

*Tier:* (iii) search-snippet. It is plausibly the true abstract — the "int (x) … not monotonous"
sentence is too specific and too oddly-worded to be model invention — but it was **not read from
the publisher's page**, and this audit will not upgrade it on plausibility alone.

A fourth query returned, also tier (iii)/(iv): *"Gáspár and Tarnai used Groemer's and Oler's
inequalities to obtain upper bounds for circle packing in the square, the equilateral triangle
and the circle"*, and, for the square, *"the extra interstice area for a circle touching the side
of the triangle is d²"*.

### 2.2 The "heuristic" question — settled as far as snippets can settle it

Proposal Z.1 records that "one search rendering of the abstract called the bounds *heuristic* and
another did not", and asks for this to be settled. **Three of three renderings obtained today
contain the word "heuristic"**, in the same syntactic position (first sentence, modifying "upper
bounds"). Combined with the one prior rendering that omitted it, the tally across all known
renderings is **4 contain it, 1 omits it**.

*Reading recorded, not concluded:* the balance of snippet evidence is that the word "heuristic"
**is** in the published abstract. Both readings are preserved:

- **Reading A (favoured by the evidence).** The abstract self-describes the bounds as heuristic.
  If the triangle table is genuinely non-rigorous, then even a G–T row below 0.7559 is **not** a
  competing *theorem*: it would be prior art for the *number* but would not supersede a rigorous
  lower bound. This repo's n = 16 bound is itself only `sketch`, so this does not make the repo's
  bound better — it means the two are not the same kind of object and a novelty claim would have
  to be phrased about the number, not about rigour.
- **Reading B (not excluded).** "Heuristic" describes the derivation style while the resulting
  inequality is nonetheless proved, or the word attaches to some domains and not the triangle.

**Neither reading can be chosen without the body.** That is Q2.

### 2.3 What the abstract's own content implies, if it is genuine (tier (v) inference)

- *"the area of interstices at the boundary … calculated with greater precision than by other
  authors, so the obtained upper bounds are sharper than those known before."* Their baselines
  are Groemer and Oler — the same two inequalities this repo uses. So a G–T triangle row for
  n = 16 is, if rigorous, **necessarily below 0.83060** (§5.3).
- *"Because the function int (x) appears in the relationships, the upper bounds are not
  monotonous functions of the circle number."* **This forecloses interpolation.** One cannot
  estimate the n = 16 row from the n = 15 and n = 20 rows, or from an asymptotic formula. Q1 must
  be answered by reading the literal row.
- **A second, separate prior-art exposure this audit did not expect.** "Refine the boundary
  interstice area on top of Oler/Groemer" is *structurally the same idea* as round-1 approach
  **F** ("Oler-with-vacancy-correction") and as the covering/counting family behind
  PRs #98/#104. So Gáspár–Tarnai is candidate prior art for **the method**, not only for the
  n = 16 number. This was not noted in the triage file.

### 2.4 How much sharpening would G–T need? (calibration, `numerical`, §5.3)

| n = 16, equilateral triangle | density bound `D` | equivalent `s(16) >=` |
|---|---|---|
| Groemer 1960, applied to the containing triangle | 0.85266602 | 11.66796539 |
| Oler 1961, applied to the containing triangle | 0.83060265 | 11.82191831 |
| **threshold — G–T beats the repo iff `D <=` this** | **0.75590121** | **12.39230485** = 2+6√3 |
| best-known construction (so the truth is `<=` this) | 0.71817481 | 12.71362877 |

- Groemer → Oler is a **2.59 %** sharpening of the density bound.
- Oler → threshold would require a further **8.99 %**.
- Threshold → truth leaves **4.99 %** of headroom.

*Tier (v) judgement, offered as calibration and not as an answer:* asking a boundary-interstice
refinement to deliver 3.5× the Groemer→Oler gain, landing within 5 % of the true density, is a
lot. But it is exactly the kind of gain a careful per-boundary-circle accounting can produce, and
0.7559 sits comfortably inside the interval where the answer is genuinely undetermined. **This
audit does not guess.** Q1.

---

## 3. Lead 2 — Nurmela & Östergård (1999): **uncited prior art for a live approach.** Say so.

**Finding, tier (iii) search-snippet, and this audit believes it is correct.** A `WebSearch`
rendering describing the method of *More Optimal Packings of Equal Circles in a Square*, DCG
**22** (1999) 439–457, states that the method

> involved tiling the square, considering combinations of tiles that could contain circles,
> eliminating combinations that don't allow sufficient spacing between circles, and finally
> proving a guessed optimal packing is indeed optimal,

extending proven optimality in the square to **n ≤ 27**.

**Compare round-2 approach I** (`../approaches-round-2/README.md`, "Grid-forcing occupancy
patterns"), quoted from its own text:

> "the uniform k×k subdivision of an equilateral triangle into k² congruent side-d/k cells …
> its cells have diameter d/k < 2 whenever k > d/2 … any 16 valid points occupy 16 *distinct*
> cells … **Phase 1 — enumerate occupancy patterns**: which 16 of the 25 cells are occupied …
> **Phase 2 — refute each pattern** as a 16-variable constraint-satisfaction problem".

Tile the container; enumerate which tiles are occupied; eliminate the occupancy patterns that
cannot be separated. **These are the same method**, differing only in the container. Approach I
records **"Dependencies. None unresolved."** and cites no prior art whatsoever; the only
square-container precedents anywhere in the repo are Markót & Csendes (interval B&B, a different
method) in `candidate-approaches` and `experiments/circle-packing-bnb`. Grep confirms:
**Nurmela and Östergård are not mentioned anywhere in this repository except in the round-3
triage file itself.**

**This belongs on issues #97 and #110.** Concretely, and stated for whoever routes it:

1. Approach I is **not novel in method**. It is the 1999 Nurmela–Östergård tile/occupancy
   -elimination scheme transferred from the square to the equilateral triangle. That transfer may
   still be worth doing — a container transfer is legitimate new work — but the write-up must
   cite the precedent and must not present the mechanism as new.
2. The precedent is also **encouraging**, and this is the more useful half: it says the method
   *demonstrably reaches n = 27 in a square*, which is far past where round-2 feared it would
   die. Approach I's kill-criterion (sample 1000 patterns at d = 8.5, extrapolate node counts) is
   the right measurement, but its pessimistic prior should be revised by the precedent.
3. **Before any further work on I**, Q3 should be answered, because the body will contain the
   pruning tricks that make the elimination affordable — which is exactly what approach I's
   "most likely to be wrong" section says it lacks.

*What this audit did NOT establish:* that the description above is accurate to the paper. It is a
model's rendering of an indexed page. The body was not obtained (Springer, paywalled;
`link.springer.com` not probed). **Tier (iii).** Treat item 1 as a strong warning, not as a
settled attribution, until Q3 is answered.

---

## 4. Lead 3 — Amore, arXiv:2212.12287 (2022): the substance is confirmed; the triage's
## characterisation of issue #13 is not

### 4.1 The paper (tier (ii)/(iii))

Two independent queries returned matching, verbatim-reading abstract text for *Circle packing in
regular polygons* (Paolo Amore, Universidad de Colima; arXiv:2212.12287, 23 Dec 2022; published
*Phys. Fluids* **35** (2023) 027130):

> … intensive numerical experiments spanning several polygons (the largest number of sides being
> 16) and **up to 200 circles (400 circles in the special cases of the equilateral triangle and
> the regular hexagon)** … Some of the configurations that we have found possibly are not global
> maxima of the packing fraction, particularly for N ≫ 1, due to the great computational
> complexity of the problem, but nonetheless they should provide good lower bounds for the
> packing fraction at a given N.

**So proposal Z.4's factual claim is correct: Amore covers the equilateral triangle up to
N = 400, with the author's own caveat about global maximality.** Tier (ii)/(iii) — arxiv.org is
blocked (§1), so the tables themselves were not seen and **no Amore value is available to this
repo**.

### 4.2 Where the triage overstates — recorded as a disagreement

Proposal Z.4 says: *"Issue #13 frames past-34 as untouched territory; that framing needs
correcting against this paper."* **Issue #13 does not say that.** Read via the GitHub API today,
#13 says:

> "Past n = 34 the literature **thins out**, which is exactly the region where an apparent
> improvement is most likely to be a bug."

and it is built entirely around benchmarking against **Graham & Lubachevsky's own published
values at n = 37, 40, 42, 43, 46, 49, 56, …, 254**. Far from treating the region as untouched,
#13's whole scope is "extract those published d(n) into `reference.py` and reproduce them".
So #13's framing is **milder and better** than the triage represents it.

**The substantive correction still stands, but it lands elsewhere:**

- **On #13:** its warning is accurate but its source list is incomplete. Amore (2022) is a second,
  much more recent published benchmark covering the equilateral triangle to N = 400, and it is
  absent from #13 and from `experiments/circle-packing-search/reference.py` (which stops at
  n = 36). Any past-34 record claim must check Amore, not only Graham–Lubachevsky. Add it.
- **On proposal AD** ("Record hunt at 35 ≤ n ≤ 60"): AD's premise is that the equilateral triangle
  is a *"benchmark orphan … untouched by the post-1995 metaheuristic wave"* and that "the soft
  region is past 34". **That premise is materially wrong.** Amore is precisely the post-1995
  metaheuristic wave, applied to this container, reaching N = 400 — i.e. AD's entire proposed
  hunting ground is already covered by a 2023 *Physics of Fluids* paper. AD is not thereby dead
  (Amore disclaims global optimality), but it is a *record-matching* exercise against a modern
  strong baseline, not virgin territory, and its expected value should be re-rated accordingly.
- **A sharper point.** `attacks/oler-lower-bound/README.md` line 48 records that an earlier
  worker **read the relevant sections of Amore** — for its restatement of Oler's inequality. So
  this repo had the paper open and did not notice that it also contains the packing tables that
  moot AD's premise. That is a reading-for-one-purpose failure, and it is worth a line in
  `FINDINGS.md` (the manager's to write, not this worker's).

---

## 5. Independent corroboration of the triage's §0.1 and §0.2

Decorrelated second check. Everything below was re-derived from the *statements of the
inequalities* — not from the triage file, not from `oler_bound.py` — by
`experiments/packing-r3-audit/audit_calibration.py`, exact in `sympy`. Status `numerical`.

### 5.1 §0.1 — Oler's floor: **CONFIRMED, three ways.**

Oler's inequality, normalised to minimum mutual distance 1: for a convex region of area `A` and
perimeter `P` containing `n` points at pairwise distance `>= 1`,
`n <= (2/sqrt3)A + P/2 + 1`.

Applied to our object — an equilateral triangle of side `d` holding `n` points at distance `>= 2`,
scaled by 1/2 so the separation is 1, giving a triangle of side `d/2`:

```
A = (sqrt3/4)(d/2)^2,  P = 3(d/2)   =>   n <= d^2/8 + 3d/4 + 1
```

`sympy` expands the substitution to exactly `d**2/8 + 3*d/4 + 1`, and `solve` returns the positive
root `d = sqrt(8n+1) - 3` **symbolically**, not numerically. So:

- **CONFIRMED** `d(n) >= sqrt(8n+1) - 3`.
- **CONFIRMED exactly tight at triangular numbers**, and more strongly than the triage checked it:
  substituting `d = 2(k-1)` gives `k**2/2 + k/2 = k(k+1)/2` **as a polynomial identity in k**, so
  tightness holds for *every* k, not merely the six spot-checked. All six spot values (k = 2…7 →
  3, 6, 10, 15, 21, 28) also reproduce.
- **CONFIRMED** `d(16) >= sqrt(129) - 3 = 8.357816691600547` and
  `s(16) >= 2sqrt3 + sqrt129 - 3 = 11.82191830673830`.

No disagreement with §0.1. Its status labelling is also right: the inequality is `cited` (Oler
1961, read in full by the worker on issue #17), its application to this container is `sketch`.

### 5.2 §Z.1 — the calibration: **CONFIRMED, and here is the derivation the task asked for.**

The triage gives the threshold 0.7559 without showing how a density bound becomes a bound on
`s(16)`. Derivation, in full:

**Convention.** For `n` **unit** circles packed in an equilateral triangle of side `s`,
```
density  :=  n * pi * 1^2 / area(triangle)  =  n*pi / ((sqrt3/4) s^2).
```
**Conversion.** Let `D_n` be any valid *upper* bound on that density over all packings of n unit
circles in an equilateral triangle. The optimal packing has side exactly `s(n)`, so its density
`n*pi/((sqrt3/4)s(n)^2)` is one of the densities `D_n` bounds. Hence

```
n*pi / ((sqrt3/4) s(n)^2)  <=  D_n
     =>   s(n)^2  >=  4*n*pi / (sqrt3 * D_n)
     =>   s(n)    >=  2 * sqrt( n*pi / (sqrt3 * D_n) ).                        (*)
```
Note the direction: a **smaller** density bound is a **stronger** result. Inverting (*), a claimed
lower bound `L` on `s(n)` is *equivalent* to the density bound `D = 4*n*pi/(sqrt3 * L^2)`, and a
published `D_n` beats `L` exactly when `D_n <= D`. (The script checks the map round-trips
symbolically.)

**At n = 16 against the repo's `L = 2 + 6sqrt3`:**
```
D  =  64*pi / (sqrt3 * (2+6sqrt3)^2)  =  8*pi*(14*sqrt3 - 9) / 507  =  0.755901213657...
```
**CONFIRMED** — the triage's 0.7559 is right, to every digit it printed.

**Why the density convention is the right one — and this is the actual evidence, not an
assumption.** The convention was *not* assumed: it is pinned by the fact that it is the only one
under which **both** of the triage's published baselines reproduce from their primary
inequalities (§5.3). Two independent inequalities landing on the triage's two printed numbers to
4 decimal places is not a coincidence.

### 5.3 The two baselines: **CONFIRMED**, and the "Groemer 0.8527" number is now sourced

The triage prints "plain Oler 0.8306, Groemer 0.8527" without saying where Groemer's comes from.
This audit identified and re-derived both.

- **Oler.** From §5.1, `s(16) >= 11.82191831`; via the definition, density `= 0.83060265`.
  **Matches 0.8306.**
- **Groemer.** Groemer, *Math. Z.* **73** (1960) 285–294, p. 285, Satz — quoted verbatim in
  `../../README.md`, where an earlier worker read it from the free GDZ scan (**that quotation is
  tier (i); this audit did not re-open the scan, so its use here is tier (iv) on this repo's own
  transcription**): for `n` unit circles in a convex region of area `F` and perimeter `U`,
  ```
  n*sqrt12 <= F - kappa*U + lambda,   kappa = (2-sqrt3)/2,  lambda = sqrt12 - pi(sqrt3 - 1).
  ```
  Take the region to be the containing triangle of side `s`: `F = sqrt3 s^2/4`, `U = 3s`. Solving
  at n = 16 gives `s(16) >= 11.66796539`, density `= 0.85266602`. **Matches 0.8527.**

So the triage's Groemer figure is Groemer's own inequality applied to the containing triangle —
consistent with the tier-(iii)/(iv) snippet in §2.1 saying Gáspár–Tarnai take Groemer and Oler as
their baselines. Both numbers are corroborated and their provenance is now on the record.

*Consistency note:* Oler (0.83060) is sharper than Groemer (0.85267), as it must be — Oler's
inequality is the later refinement. If the ordering had come out the other way, one of the two
transcriptions would be wrong.

### 5.4 §0.2 — the Q(√3) family: **PARTIALLY CONFIRMED. One claim is FALSE. Loudly.**

**Confirmed.** Reading the best-known table from this repo's own transcription of
Graham–Lubachevsky's printed 15-significant-digit `d(n)`
(`experiments/circle-packing-search/reference.py`, `GL_D`, converted by `s = 2/d + 2sqrt3`):

| n | GL prints d(n) | s(n) | closed form |
|---|---|---|---|
| 17 | 0.211324865405187 | 12.9282032302755 | `6 + 4√3` ✓ |
| 24 | 0.174457630187010 | 14.9282032302755 | `8 + 4√3` ✓ |
| 31 | 0.148543145110506 | 16.9282032302755 | `10 + 4√3` ✓ |

and the structural claims: `s(24)-s(17) = 2` and `s(31)-s(24) = 2` **exactly**, index spacing 7,
and `s(17) = s(12) + 2` with the proven `s(12) = 4 + 4√3`. All confirmed symbolically.

> ### ⚠️ DISAGREEMENT — §0.2's exclusivity claim is false as written
>
> §0.2 asserts: *"**No other open n in 16–34 has a best-known value expressible as a + b√3 with
> small integers**"*. **This is wrong. It misses n = 27.**
>
> Graham–Lubachevsky print `d(27) = 0.166666666666667`, i.e. `1/6`, giving
> ```
> s(27)  =  2*6 + 2*sqrt3  =  12 + 2*sqrt3  =  15.4641016151378
> ```
> which agrees with the printed decimal to 2.4e-14 — pure rounding of `1/6` at 15 digits. It is
> `a + b√3` with `a = 12`, `b = 2`: smaller integers than any of 17, 24, 31.
>
> **n = 27 is open.** The settled set is n ≤ 15, the triangular numbers, and n = 20. Δ(6) = 21 and
> Δ(7) = 28 are the triangular numbers in range; **27 is neither**. It is Δ(7) − 1, i.e. the
> **first open case of the Erdős–Oler conjecture (k = 7)** — which `../../README.md` states is
> "Open for k ≥ 7", and which issue #91 attacked for a whole campaign before being closed.
>
> A full scan (a, b integers in −40..40, tolerance 2e-11) over every open n in 16–34 with a GL
> entry returns exactly **{17, 24, 27, 31}** — not {17, 24, 31}. No other n in the range hits.
>
> **Why this matters, and it matters more than the miss itself.** §0.2's operative conclusion is
> *"n = 17, not n = 16, is the cheapest open case for exact work"*, and proposal **Y** is staffed
> to certify 17, 24, 31 in that order. **n = 27 is cheaper than all three, and by a wide margin.**
> Its conjectured optimum is the side-2 triangular lattice on 28 points with one point deleted:
> the coordinates are integer combinations of `(2,0)` and `(1,√3)`, already in `Q(√3)`, needing no
> optimiser run, no contact-graph extraction, and no exact solve of a contact system. An exact,
> *tight* certificate for `s(27) <= 12 + 2√3` is close to free — and no exact tight certificate
> currently exists for any open n, which is precisely the gap proposal Y exists to fill.
>
> **Recommended correction:** Y's target list becomes **27, 17, 24, 31**, in that order. The n = 27
> certificate should be attempted first, as a same-session warm-up that validates the tightness
> machinery on a case where the answer is structurally known, before that machinery is pointed at
> n = 17 where it is not.
>
> *Caveats, stated so this disagreement is not overread.* (a) `s(27) = 12 + 2√3` is the
> **construction** side only; it asserts nothing about optimality, and proving `s(27) = s(28)` is
> exactly the open Erdős–Oler k = 7 problem — do not conflate. (b) The value rests on GL's printed
> decimal for n = 27, and GL themselves say (per `reference.py`'s docstring) that n = 21, 27, 28,
> 35, 36 were run only briefly with results "consistent with the existing results" — so the
> best-known status of the n = 27 row is `numerical` and thinly sourced, like everything else in
> that table.
>
> *Probable cause of the triage's miss (tier (v)):* n = 27 and n = 28 carry the identical printed
> `d`, and 28 is triangular; a scan that filtered out triangular numbers by value rather than by
> index would drop 27 along with 28.

**A methodological note this audit owes the reader.** The first run of §5.4 typed the best-known
table from the auditor's own recollection and produced a *different*, larger set of disagreements
(n = 19, 25, 28, 32). Those were **artefacts of a wrong table** and are retracted. The scan was
rebuilt on the repo's own transcription of the published values and rerun; only n = 27 survives.
The retraction is recorded rather than quietly deleted because it is the same failure mode this
whole audit is about — asserting a number whose source you did not open — committed by the
auditor, caught by checking against a source, one hour apart.

---

## 6. Summary of findings and where each routes

| # | Finding | Tier | Routes to |
|---|---|---|---|
| 1 | Gáspár–Tarnai n = 16 row **unread and unreadable**; `pp.bme.hu` 403 at egress. Standing instruction: **assume it is known**. | blocked | #97, #110 — Q1 |
| 2 | `arxiv.org` is **now also blocked** (EGRESS_BLOCKED). Triage's "may be reachable" is out of date. | (i) first-party | #110 |
| 3 | "Heuristic" is in the G–T abstract on 4 of 5 known renderings; both readings preserved; body needed. | (iii) | #110 — Q2 |
| 4 | G–T's method (refine boundary interstices over Oler/Groemer) is candidate prior art for **approach F** and the covering family, not only for the n = 16 number. | (v) | #97, #110 |
| 5 | **Nurmela–Östergård 1999 is uncited prior art for round-2 approach I** — same tile/occupancy-elimination method, published, reaching n = 27 in the square. | (iii) | **#97, #110** — Q3 |
| 6 | Amore (2022) does cover the equilateral triangle to **N = 400**; Z.4's substance is right. | (ii)/(iii) | #13 |
| 7 | But **issue #13 never claimed "untouched territory"** — the triage mischaracterises it. The real correction lands on proposal **AD**, whose "benchmark orphan" premise is wrong, and on `reference.py`, which stops at n = 36. | (i) issue text | #13, #110 |
| 8 | §0.1 Oler floor **confirmed**, tightness strengthened from 6 spot checks to a polynomial identity. | `numerical` | #110 |
| 9 | §Z.1 threshold **0.755901213657 confirmed**; conversion derived; density convention *pinned* by both baselines reproducing. | `numerical` | #110 |
| 10 | §0.2 closed forms for 17, 24, 31 **confirmed**; **exclusivity claim FALSE — n = 27 missed**; Y's target list should become 27, 17, 24, 31. | `numerical` | **#110, proposal Y** |

## 7. What this audit did not do

- Did not read a single paper body. **Nothing here is `cited`.**
- Did not probe `pp.bme.hu`, `www.math.ucsd.edu` or `www.packomania.com` at all — prior denials
  stand and `RULES.md`/the proxy README forbid retrying them. `arxiv.org` was probed exactly once,
  through one channel, and not retried.
- Did not verify §0.2's claim that n = 16's PSLQ candidate has a degree-10 minimal polynomial.
- Did not check the n = 16 row of Melissen–Schuur or the Payan body (Q4 unchanged).
- Did not check `link.springer.com`, `researchgate.net` or `citeseerx.ist.psu.edu` reachability;
  a future worker may find one of them open, and the CiteSeerX survey
  *New Approaches to Circle Packing in a Square* (Szabó et al.) surfaced repeatedly in search and
  is a plausible secondary route to Gáspár–Tarnai's **square** table — though not its triangle
  table, which is the one Q1 needs.
