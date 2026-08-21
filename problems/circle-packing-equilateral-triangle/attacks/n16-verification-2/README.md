# Verification pass 2 over the $n=16$ covering lower bound

**Claim type: neither construction nor optimality.** (Problem
[`../../RULES.md`](../../RULES.md) §1 asks for that sentence first.) Nothing here asserts a bound
of its own beyond what the certificates on disk already contain; it re-derives them adversarially.

- Examiner: `claude` (Claude Opus 5), 2026-08-22, branch `claude/circle-equklatetal-problem-sa7tx7`
- Code: [`experiments/packing-n16-verify-2/`](../../../../experiments/packing-n16-verify-2/) —
  Python standard library (`fractions`) only. **No float in any decision, anywhere.**
- Continues [`../n16-verification/`](../n16-verification/), whose method — try to break it first,
  then read the argument — this file follows. It does **not** reuse that pass's code.

> ## THIS GRANTS NO STATUS. Read this before using anything below.
>
> Repo [`RULES.md`](../../../../RULES.md) §5 and this problem's `RULES.md` §3: `verified:review`
> requires an examiner from a **different model family than the author**, writing an independent
> checker. I wrote the independent checker — but I am **Claude Opus 5, and so is every author of
> every artefact examined here**. The family-decorrelation half of the requirement is not met.
>
> **Everything below stays `sketch` and stays non-assumable, including everything I confirm.**
> What this pass buys is error-finding, not certification. A Codex pass is still required.

I did not read, import, or adapt `experiments/packing-n16-covering/certify.py` (the author's
certifier) or `experiments/packing-n16-verify/manager_covering_check.py` (the previous pass).
`covercheck.py` was written from `../../README.md` and `../../RULES.md` §2 alone. The only thing I
read from the author's tree is the certificate **data**.

---

## 0. Headline

| | |
|---|---|
| **Standing record $a_{16}\ge 89267/20000 = 4.46335$** | **CONFIRMED**, exactly, in independent code. No break found. |
| **The same certificate establishes more than it claims** | $a_{16}\ \ge\ 446335/99998 = 4.4634392687853754\ldots$ — see §2. |
| **The three push lanes** (`n16-covering-2`, `n16-shapes`, `n16-dual`) | **No artefact exists in this tree or on any local branch.** Nothing to verify. §4. |
| **Highest exactly-verified lower bound surviving this check** | $\boxed{a_{16}\ \ge\ \tfrac{446335}{99998}},\qquad s(16)\ \ge\ \tfrac{446335}{49999}+2\sqrt3 = 12.3909801527\ldots$ |

Ceiling check: $4.46344 < 4.6247636$, headroom $0.1613$. **Nothing here comes near settling
$n=16$**, and nothing here should be described as if it did.

---

## 1. Disagreements, with witnesses

Three, none of them fatal to the bound. Ordered by how much damage they could do downstream.

### D1 — `KILL-CRITERION.md` K4's ceiling $a \lesssim 4.5603$ is not a theorem, and its per-piece area cap is **false**

**Where:** [`../n16-covering/KILL-CRITERION.md`](../n16-covering/KILL-CRITERION.md), K4.

K4 caps the area of a piece of diameter $<1$ at $\tfrac{3\sqrt3}{8} = 0.6495190\ldots$ — the area
of the *regular hexagon of diameter 1* — flagging it honestly as "asserted, not cited". It is not
merely uncited; **as a statement about convex sets of diameter $\le 1$ it is false**, and it is
false by a wide margin:

| convex set of diameter 1 | area | vs $3\sqrt3/8 = 0.649519$ |
|---|---:|---|
| regular hexagon, circumradius $1/2$ | $0.649519$ | $=$ |
| **the disk of diameter 1** | $\pi/4 = \mathbf{0.785398}$ | **$+21\%$** |
| Graham's largest small hexagon (Graham 1975) | $0.674981$ | $+3.9\%$, and this is the *hexagon* optimum |

So even restricted to six-sided pieces the cap is wrong. Replacing it with the isodiametric bound
$\pi/4$ (which *is* a theorem) and keeping K4's own proved corner bound $\pi/6$ for the three
corner pieces:

$$\tfrac{\sqrt3}{4}a^2 \;\le\; 3\cdot\tfrac{\pi}{6} + 12\cdot\tfrac{\pi}{4}
\;\Longrightarrow\; a \;\le\; 5.0391657\ldots$$

which is **above the packing ceiling $4.6247636$ and therefore vacuous.** There is no rigorous
area-based ceiling on this method below the packing ceiling.

**Why this matters right now.** K4 says "if the search stalls within 1% of that ceiling, stop".
Three lanes are pushing upward from $4.4634$. A lane that reads $4.5603$ as a hard wall will
either abandon a live push, or — worse — see a correct certificate at $a^\star \in (4.5603,
4.6248)$, conclude it must be buggy, and discard it. **$a^\star > 4.5603$ contradicts nothing that
has been proved.** The only hard tripwire is the packing ceiling.

`experiments/packing-n16-verify-2/area_ceiling.py`.

### D2 — the K3 ceiling is stated unconditionally; it rests on a packing this repo has not certified

**Where:** [`../n16-covering/README.md`](../n16-covering/README.md), "Kill-criteria" and "The
method has a ceiling".

The ceiling $a_{16}\le 4.6247636$ comes from Melissen–Schuur (1995) via Graham–Lubachevsky. That
is literature, status `numerical`, and **`attacks/n16-exact/certificates/` is empty** — the only
in-repo object is an 80-dps `mpmath` refinement, which `RULES.md` §2 explicitly does not accept as
exact. The previous pass wrote the conditional form ("*once* the Melissen–Schuur packing is
exactly certified … until it lands, the honest ceiling is the conditional one"); `n16-covering`
drops the conditional and asserts the ceiling flat.

This is this campaign's standing pattern — the arithmetic is right and the sentence after it is
one step too broad — and it is worth fixing now precisely because the ceiling is the **only**
tripwire that would catch a wrong certificate near the top. A tripwire whose own status is
overstated is the wrong thing to be relying on when three lanes are climbing toward it.

No number changes: $4.4634 \ll 4.6248$ either way.

### D3 — nit: "the remaining headroom is at most $0.161$ in $a$" is false as an inequality

Headroom is $4.6247636 - 4.46335 = 0.1614136 > 0.161$. Rounded the wrong way. Harmless; recorded
because "at most" is an inequality and this file's readers copy inequalities.

---

## 2. The standing certificate: confirmed, and it proves more than it claims

### 2.1 What I checked, in my own code

`experiments/packing-n16-covering/sub_s2_cert.json`, $a = 89267/20000$, in the triangular basis
$e_1=(1,0)$, $e_2=(1/2,\sqrt3/2)$ with $|ue_1+ve_2|^2 = u^2+uv+v^2$ rational.

| # | check | method | result |
|---|---|---|---|
| 1 | piece count is exactly **15** | — | **ok** (16 would prove nothing about 16 points) |
| 2 | every piece is a simple, **strictly** convex polygon | all turns same strict sign; repeated/collinear vertices rejected | **ok**, vertex counts $[6,6,6,5,5,5,5,5,4,4,5,5,5,5,4]$ |
| 3 | every vertex in $T_a$ ($u,v\ge0$, $u+v\le a$) | exact rational | **ok** → convex piece $\subseteq$ convex $T_a$ |
| 4 | **strict** max squared diameter over **all** vertex pairs of **all** pieces | recomputed, not read | $\tfrac{2499900001}{2500000000} < 1$ **strictly** |
| 5 | reported `max_sq_diam` equals what I computed | — | **ok** |
| 6 | all $\binom{15}{2}=105$ pairs interior-disjoint | exact Sutherland–Hodgman convex clipping, area $=0$ | **ok** |
| 7 | areas sum **exactly** to $\operatorname{area}(T_a)$ | shoelace, $2\sum = a^2$ | **ok**, difference exactly $0$ |
| 8 | grid probe: 10011 rational points of $T_a$, each in $\ge1$ piece | offset by $1/7919$ off the certificate's rationals | **ok**, no holes |
| 9 | grid probe: no point in the **interior** of two pieces | — | **ok** |

**On the diameter, since strictness is the whole game.** The maximum is attained in piece 9,
between $(0,0)$ and $(49999/50000,\,0)$. I recompute it rather than read it, and I compare it to 1
as an exact rational. The slack is $1 - \max = \tfrac{99999}{2500000000} = 4.0\times10^{-5}$.
**Every one of the 15 pieces** is separately below 1 (per-piece maxima run from $0.9996278$ to
$0.9999600$) — so this is a converged optimum, not one piece carrying the certificate.

**On the covering argument, since "areas sum" alone does not give it.** Checks 3, 6, 7 together
give: $U=\bigcup F_i$ is closed, $U\subseteq T_a$, and $|T_a\setminus U| = 0$ (equality in
$|U|\le\sum|F_i|$ needs the zero-measure overlaps from check 6). $T_a\setminus U$ is relatively
open in $T_a$, and a nonempty relatively open subset of a nondegenerate triangle has positive
measure — so it is empty. Checks 8–9 are an independent, differently-shaped confirmation of the
same conclusion.

### 2.2 What I tried, to break it — `adversarial.py`

| attack | outcome |
|---|---|
| the 3 corners of $T_a$, edge midpoints, quarter-points, centroid | all covered |
| 2001-point exact probe along **each** of the 3 edges of $T_a$ | no hole on any edge |
| 8-direction $\varepsilon=10^{-7}$ probe around **every** one of the 31 distinct piece vertices | no wedge missing |
| second- and third-largest squared diameters | also $<1$ |
| per-piece maxima, all 15 | all $<1$ |
| union area recomputed via total pairwise overlap | overlap exactly 0; union $=|T_a|$ |
| 15 pieces distinct as vertex sets | yes |
| the same pieces dilated to the ceiling $a=4.6247636$ | max sq. diam $=1.0736 \ge 1$ — **invalid, as it must be**, since a 16-point packing exists there |

**No break found.**

### 2.3 The checker is calibrated — it rejects things

A checker that has never rejected anything is not evidence. Ten corruptions of the **real**
certificate, each rejected (`negative_controls.py`):

| control | rejected by |
|---|---|
| C1 max diameter **exactly 1** (the Lemma L equality case) | strict diameter test: `1 < 1 : False` |
| C2 max diameter just over 1 | strict diameter test |
| C3 $a$ inflated by $10^{-3}$, pieces unchanged | area identity |
| C4 one piece deleted | count, area identity, **and** grid probe found the hole |
| C5 a piece duplicated (16 pieces, coincident pair) | count, disjointness, area, probe |
| C6 one piece split in two — a **valid covering** with 16 pieces | count: "16 pieces would prove nothing about 16 points" |
| C7 a piece translated within $T_a$ | disjointness, probe (holes **and** overlaps) |
| **C8 overlap + equal-area hole** — the area-only argument's exact blind spot | disjointness and probe; **the area identity does not fire**, which is the point |
| C10 a piece translated genuinely outside $T_a$ | containment, probe |
| C9 decimal string in an exact field | parser (`RULES.md` §2) |

C1 and C8 are the two that matter. C1 is the failure that broke Lemma L. C8 is the failure the
first certifier's argument was open to.

### 2.4 The unused margin — the certificate establishes $a_{16}\ge 446335/99998$

$2499900001 = 49999^2$. So the certified maximum diameter is **exactly** $49999/50000 = 0.99998$,
not merely "$<1$": the certificate is carrying $2\times10^{-5}$ of unused diameter slack.

Dilation $S_\mu$ about the chart origin by a rational $\mu>0$ is linear: it maps the 15 pieces to
15 convex polygons, preserves simplicity, convexity and interior-disjointness, multiplies every
area by $\mu^2$ and every squared distance by $\mu^2$, and maps $T_a \to T_{\mu a}$. So the image
is a 15-piece convex covering of $T_{\mu a}$ of maximum diameter $\mu\cdot\tfrac{49999}{50000}$,
which is **strictly** below 1 for every $\mu < 50000/49999$. Hence for every rational

$$a' \;<\; a\cdot\frac{50000}{49999} \;=\; \frac{446335}{99998},$$

$T_{a'}$ has no 16 points at pairwise distance $\ge1$, so $a'$ is not in the (upward-closed) set
of admissible sides, so

$$\boxed{\;a_{16}\ \ge\ \frac{446335}{99998} = 4.4634392687853754\ldots\;}\qquad
s(16)\ \ge\ \frac{446335}{49999} + 2\sqrt3 = 12.3909801527\ldots$$

No compactness or attainment argument is needed — it is an infimum over an upward-closed set.

**This is not prose.** `scale_up.py` emits five explicitly dilated certificates, at
$a' = 4.463439$, $4.4634392$, $4.46343926$, $4.463439268$, and
$\tfrac{223167499999950001}{49999000000000000} = 4.4634392687843754$, and puts **each** through
the full nine-check `covercheck.py` above — count, convexity, containment, strict diameter,
all 105 disjointness pairs, exact area identity, and both grid probes. All pass exactly. The
supremum is the only limiting step, and it is one line.

The gain is small — $8.9269\times10^{-5}$ in $a$, $1.785\times10^{-4}$ in $s$ — but it is exact,
free, and it is what the certificate **actually** proves. Note that
[`../n16-covering/KILL-CRITERION.md`](../n16-covering/KILL-CRITERION.md) already defines the
deliverable this way: "*the bound reported is $a_{16}\ge a^\star$ where $a^\star$ is the supremum
of side lengths for which such a covering is exhibited*." The write-up reported the exhibited $a$,
not the supremum. **Anyone producing the next certificate should report the supremum
$a\cdot 1/\mathrm{diam}_{\max}$, not the value the optimiser froze at.**

### 2.5 Verdict

**CONFIRMED**, with the bound corrected upward.

- $a_{16} \ge 89267/20000$ — **confirmed** (in fact strictly $>$).
- $a_{16} \ge 446335/99998$ — **confirmed**, by the dilation family above.
- Status remains **`sketch`**: same model family (see the banner), and novelty is unchecked.

---

## 3. Scope notes that travel with the bound

- **Novelty is UNVERIFIED.** Literature egress is blocked (`../eo-literature/`). Pigeonhole
  against a covering by small-diameter pieces is a standard discrete-geometry move and
  Melissen–Schuur's own $n=16,17,18$ paper has not been read here. **Assume this is known.**
- **This is a lower bound at an open case**, so no published value can confirm it. The only
  external checks available are (i) it must not exceed the packing ceiling — it does not, by
  $0.161$ — and (ii) the same method at $p=2,3,4$ must not exceed the `cited` values, which the
  previous pass checked and I did not re-run.
- **The strictness rule is not negotiable.** Separation here is non-strict (`../../RULES.md` §2),
  so a piece of diameter exactly 1 kills the pigeonhole. Witness on the record: $T_{\sqrt3}$ holds
  four pairwise-separated points (three corners plus centroid, corner-to-centroid distance exactly
  1) while three cells of diameter exactly 1 cover it. My control C1 is that failure, injected
  into the real certificate, and it is rejected.
- **Polygons only.** The vertex-pair maximum *is* the diameter because a polygon's extreme points
  are among its vertices. A curved piece invalidates that step, and any $\pi$ appearing in a
  curved-piece diameter needs a certified rational enclosure. `covercheck.py` refuses anything
  that is not a simple strictly-convex polygon.

---

## 4. The three push lanes — nothing to verify

`n16-covering-2`, `n16-shapes` and `n16-dual` were named to me as live. As of this pass:

| lane | state |
|---|---|
| `attacks/n16-covering-2/` | **does not exist** in this worktree |
| `attacks/n16-shapes/` | **does not exist** |
| `attacks/n16-dual/` | **does not exist** |
| local branches under `refs/heads/claude/` | only `circle-equklatetal-problem-sa7tx7` (this one) |
| remote-tracking `refs/remotes/origin/claude/` | 16 branches, none for these three lanes |
| newest artefacts in the tree | `n16-covering/README.md` and `packing-n16-verify/manager_covering_check.py` |

The only exact covering object anywhere in the tree is `sub_s2_cert.json`. `sub_s1/s2/s6/s7/
seed2.json` and `opt_n15_*.json` are **float** optimiser output (`"a": 4.5`, `"max_diam":
1.0080…`) and are hypotheses, not certificates — `RULES.md` §2 excludes them. The best float
`a_max` on disk is `sub_s1.json`'s $4.4639000641$, which is $2.5\times10^{-4}$ above what is
certified; that is the size of the prize still sitting in the existing search output, and it is
small.

**Verdict for the three lanes: could-not-follow, for want of an artefact.** Not a criticism — they
are mid-flight. When they land, the checkers in `experiments/packing-n16-verify-2/` take a path
argument and will run on them unmodified.

### Standing instructions for whoever verifies the next certificate

1. **Recompute the maximum squared diameter; never read it.** Compare to 1 as an exact rational,
   strictly. Report the per-piece maxima too — one piece at exactly 1 among fourteen good ones is
   the shape of the error that killed Lemma L.
2. **Check the count first.** 16 pieces is a valid covering that proves nothing (control C6).
3. **Disjointness is not optional and is not inherited from "it came from a subdivision."** Check
   all $\binom k2$ pairs by exact clipping, and run a grid probe as well — control C8 shows the
   area identity alone passing a certificate with a hole in it.
4. **Report the supremum** $a/\mathrm{diam}_{\max}$, not the exhibited $a$ (§2.4).
5. **The only hard ceiling is $4.6247636$**, and even it is `numerical` until `n16-exact` lands
   (D2). **K4's $4.5603$ is not a ceiling** (D1) — do not discard a certificate for exceeding it.
6. **$a^\star > 4.6247636$ is definitely wrong.** Anything within $10^{-3}$ of it triggers
   `RULES.md` §7: label `extraordinary-claim`, do not merge, do not announce, request review from
   both humans. A covering valid for every $a$ below the ceiling would settle $n=16$, open since
   1995 — which is overwhelmingly more likely to be a bug than a discovery.

---

## 5. What is safe to build on

`RULES.md` §3's flat answer: **nothing here is assumable and nothing here changes any status.**
The column below answers the weaker question — did an independent reader re-derive it in their own
exact code and try to break it?

| Claim | Re-derived? | Safe to build on? |
|---|---|---|
| `sub_s2_cert.json` is 15 strictly-convex polygons, in $T_a$, pairwise interior-disjoint, tiling $T_a$ exactly, max sq. diameter $\tfrac{2499900001}{2500000000}<1$ | yes, exactly, plus 8 break attempts and 10 negative controls | **Yes as mathematics, `sketch` as status** |
| $a_{16}\ge 89267/20000 = 4.46335$ | yes | **Yes as mathematics, `sketch` as status.** Novelty unchecked — do not call it new |
| $a_{16}\ge 446335/99998 = 4.4634392688$ | yes — five dilated certificates machine-checked, plus a one-line supremum | **Yes as mathematics, `sketch` as status** |
| $a_{16}\le 4.6247636$ (the ceiling) | **no** — literature value, `n16-exact/certificates/` is empty | **Not yet.** Use it as a tripwire, cite it as literature, do not treat it as certified (D2) |
| K4's $a\lesssim 4.5603$ area ceiling | yes — and its per-piece cap is **false** | **NO** (D1). The rigorous replacement, $a\le 5.0392$, is vacuous |
| "headroom is at most 0.161" | yes — it is $0.1614136$ | **NO** (D3) |
| `n16-covering-2` / `n16-shapes` / `n16-dual` | nothing exists to check | **Nothing to say** |

### Claimed proofs of open cases — my independent verdict

**One lower bound at an open case, and it is not close to settling it.** $s(16) \ge
12.3909801527$ against the best known packing $s(16) \le 12.7136287741$. The interval for $s(16)$
is $[12.3909802,\ 12.7136288]$, still $0.3226$ wide. $n=16$ remains open, and nothing in this
directory or the one it examines changes that.

---

## 6. Reproducing

```bash
cd experiments/packing-n16-verify-2
python3 covercheck.py          # 9 checks on the standing certificate + 5 self-tests
python3 adversarial.py         # 8 families of break attempts, ~30 s
python3 negative_controls.py   # 10 corruptions of the real certificate, all rejected
python3 scale_up.py            # 5 dilated certificates, each fully re-checked
python3 area_ceiling.py        # D1: the K4 arithmetic, and its rigorous replacement
```

Python standard library only (`fractions`, `json`, `itertools`). No seeds, no tolerances, no
network, no float in any decision. Every script exits non-zero on any failure.
