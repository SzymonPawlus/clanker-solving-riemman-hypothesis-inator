# Verification pass over the $n=16$ campaign

**Claim type: neither construction nor optimality.** (Problem
[`../../RULES.md`](../../RULES.md) §1 asks for that sentence first.) Nothing here asserts a bound
on $s(n)$ of its own. This file is an adversarial re-derivation of the results the $n=16$ campaign
is standing on, written **without reading the authors' code** for any of them.

- Examiner: `claude` (Claude Opus 5), 2026-08-22, branch `claude/circle-equklatetal-problem-sa7tx7`
- Code: [`experiments/packing-n16-verify/`](../../../../experiments/packing-n16-verify/) — Python
  standard library (`fractions`) for the covering work, `sympy` for algebraic certificates. Exact
  arithmetic in every decision; **no float, no tolerance, anywhere in this file's conclusions.**
- Continues [`../eo-verification/`](../eo-verification/) and
  [`../eo-verification-2/`](../eo-verification-2/), whose method — try to break it first, then
  read the argument — this file follows.

> ## THIS GRANTS NO STATUS. Read this before using anything below.
>
> Repo [`RULES.md`](../../../../RULES.md) §5: `verified:review` requires an examiner from a
> **different model family than the author**. I am Claude Opus 5; so is every author examined
> here. A same-family pass is decorrelated only by the fact that I re-derived everything from the
> problem statement in my own code and tried to falsify it — **that is not decorrelation at the
> level §5 is about.**
>
> **Every claim below stays `sketch` and stays non-assumable, including the ones I confirm.**
> What this buys is error-finding, not certification.

---

## 0. Disagreements and repairs, with witnesses

### D1 — the equality case is real, AND the obvious repair does not work

**Where:** [`../eo-covering-construct/`](../eo-covering-construct/) §2 (Lemma L) and §6.

Lemma L, **as stated**, is **true** — I confirm it below. The defect is in how it is used.

> **Witness that the pigeonhole step fails at $a = a_0$.** Take $p=2$, $a_0 = 2\cdot\sqrt3/2 =
> \sqrt3$. Lemma L covers $T_{\sqrt3}$ with $\Delta(2)=3$ convex cells of diameter $\le 1$. But
> $T_{\sqrt3}$ contains **four** points at pairwise distance $\ge 1$ — its three corners and its
> centroid, whose corner-to-centroid distances are **exactly 1**:
>
> | pair | squared distance |
> |---|---|
> | corner–corner (×3) | $3$ |
> | corner–centroid (×3) | **exactly $1$** |
>
> (`lemmaL.py` §C, exact rationals.) This problem's `RULES.md` §2 fixes separation as
> **non-strict**, so those four points are a legal configuration — indeed they are the known
> optimal $n=4$ packing. So "$\Delta(p)$ cells of diameter $\le1$" does **not** give
> "at most $\Delta(p)$ points". The manager's diagnosis is confirmed exactly.

**The new part, and it is the part that matters.** The obvious repair — *"apply Lemma L at
$a < a_0$, which its own hypothesis $a \le p\sqrt3/2$ permits"* — **also fails**. The construction
places its sites at spacing $\sqrt3/2$ **independent of $a$**; only the offset $u_0$ moves. So the
interior cells are the Voronoi cells of the full lattice — regular hexagons of circumradius $1/2$,
**diameter exactly 1** — for *every* $a$ in the lemma's range. Shrinking $a$ inside the lemma
shrinks the corner and edge cells and leaves the maximum at exactly 1:

| $p=7$, $a = \lambda\sqrt3/2$ | $\lambda=6$ | $6.5$ | $6.9$ | $\lambda=7$ (threshold) | $7.1$ |
|---|---:|---:|---:|---:|---:|
| max corner-cell $\mathrm{diam}^2$ | 0.250000 | 0.562500 | 0.902500 | **1** | 1.102500 |
| max edge-cell $\mathrm{diam}^2$ | 0.812500 | 0.890625 | 0.975625 | **1** | 1.025625 |
| max interior-cell $\mathrm{diam}^2$ | **1** | **1** | **1** | **1** | **1** |

(`lemmaL2.py` §H, exact.) Verified the same way for $p=5$ at $\lambda = 5,\ 9/2,\ 4,\ 3,\ 2$: the
maximum squared diameter is exactly 1 at every one of them (`lemmaL2.py` §G).

**The repair that does work** is the one already written in that file's §0 — *scale the whole
$a_0$-partition* by $\mu = a/a_0 < 1$, which shrinks the **spacing** too. Checked exactly
(`lemmaL2.py` §F): for $p=5,7$ and $\mu \in \{999/1000,\ 9/10,\ 1/2\}$ the scaled cells tile $T_a$
with areas summing exactly, and

$$\max_i \mathrm{diam}(\mu\,C_i)^2 \;=\; \mu^2 \;<\; 1 \qquad\text{exactly.}$$

So the pigeonhole is valid for every $a < a_0$, and **the derived bound stands**. But the
distinction is not cosmetic: *re-instantiating* Lemma L at a smaller $a$ and *scaling* its
$a_0$-partition give different objects, and only the second has strict diameters. A reader who
takes the lemma's hypothesis "$a \le p\sqrt3/2$" at face value and applies pigeonhole gets a false
statement, with the $p=2$ witness above.

### D2 — §2's stated reason why the maximum diameter equals 1 is false, and it is what hides D1

**Where:** [`../eo-covering-construct/`](../eo-covering-construct/) §2, two sentences.

1. *"At $a=p\sqrt3/2$ the corner sits **exactly** on a hexagon vertex; that is why the verified
   maximum squared diameter is exactly 1 and not less, for every $p$."*

   **False for $p \ge 4$.** The maximum squared diameter is exactly 1 **for every $a$ in the
   lemma's range**, not only at the threshold, and it is attained by the *interior* hexagons,
   which do not depend on $a$ at all (table above). The corner is not why the maximum is 1.
   This sentence is precisely what makes the equality-case gap invisible: it tells the reader the
   value 1 is a threshold phenomenon that goes away below the threshold, and it does not.

2. *"Why $p\sqrt3/2$ is exactly the right threshold — **the corner is what binds**."*

   **Incomplete as a derivation.** Below the threshold the corner cell is the *smallest* of the
   three kinds, and the edge cells are strictly larger than it. Corner and edge cells reach
   diameter 1 **simultaneously** at $\lambda = p$, and just above the threshold **both** exceed 1
   ($1.1025$ and $1.0256$ at $\lambda = 7.1$). The corner-only computation gets the right threshold
   but does not by itself exclude the edge cells; that they bind at the same $a$ is a fact the
   argument needs and does not supply.

Neither correction changes any number in that file's tables — every one of them reproduced exactly
here. This is the campaign's standing pattern (`FINDINGS.md`, 2026-08-21): the arithmetic is right
and the sentence after it is not.

### D3 — "Lemma L gives $a_{\Delta(p)+1}\ge p\sqrt3/2$ **directly**" (§6, first line)

It does not give it directly; it gives it *through* the §0 scaling step, which is where the whole
strictness content lives (D1). The conclusion is right and I verify it. The word "directly" is the
one a later reader will copy.

---

## 1. Lemma L — what I checked, in my own code

Everything in this section is exact and independent. I re-derived the construction from the prose
in §2 of that file and never opened `experiments/packing-eo-covering/`.

**My normalisation** (fixed in [`lemmaL.py`](../../../../experiments/packing-n16-verify/lemmaL.py)):
separation 1, $T_a$ with corners $(0,0),(a,0),(a/2,a\sqrt3/2)$, as this problem's `RULES.md` §2
places it. I work in the lattice basis rescaled by $g=\sqrt3/2$, so a point $(x,y)$ denotes
$g(x e_1 + y e_2)$ and

$$|g(xe_1+ye_2)|^2 = \tfrac34 Q(x,y),\quad Q(x,y)=x^2+xy+y^2,\qquad
T_a=\{x,y\ge0,\ x+y\le\lambda\},\ a=\lambda g .$$

With $\lambda$ rational **everything is rational** — no $\mathbb{Q}(\sqrt3)$ arithmetic is needed
at all, and $\mathrm{diam}\le1 \iff Q \le 4/3$. At the threshold $\lambda = p$ the centring offset
is $u_0 = g/3$ **for every $p$**, which is the structural fact §3 below turns on.

### What I confirm

| # | Statement | Verdict |
|---|---|---|
| L1 | The $\Delta(p)$ sites lie in $T_a$ and their clipped Voronoi cells are convex with pairwise disjoint interiors | **confirmed** — convex as an intersection of half-planes with $T_a$; disjointness checked pairwise by exact polygon intersection (area exactly 0), $p=2..12$ |
| L2 | The cells cover $T_a$: no sliver | **confirmed twice** — cell areas sum **exactly** to $\mathrm{area}(T_a)$, and separately a rational grid probe (1891 points at $p=5$) confirms the nearest site by brute force always agrees with the polygon containing the point |
| L3 | The cell count is exactly $\Delta(p)$, all cells non-empty at the threshold | **confirmed**, $p=2..12$ |
| L4 | Every cell has squared diameter $\le 1$ for $a \le p\sqrt3/2$ | **confirmed**, exactly, $p=2..12$; the max is exactly $1$ |
| L5 | The scheme fails above the threshold | **confirmed** — at $\lambda = p+10^{-3}$ the max squared diameter is $4004001/4000000 = 1.00100025$ |
| L6 | $a_{\Delta(p)+1} \ge p\sqrt3/2$ | **confirmed, with the D1 repair and only with it** |

2900 exact checks in `lemmaL.py`, 38 in `lemmaL2.py`, 14 in `lemmaL3.py`; **all passing, no
failures**.

### A cleaner route to L4 than the one in the file, and it also checks out

Computing diameters is not necessary. **The covering radius is exactly $1/2$:** every vertex of
every clipped cell is at distance exactly $\le 1/2$ from its own site, for $p = 2..12$
(`lemmaL3.py` §J, and $1/4$ is *attained*). Since the maximum of "distance to the nearest site"
over $T_a$ is attained at a vertex of the clipped Voronoi arrangement, this says

$$T_{a_0} \;\subseteq\; \bigcup_i B(P_i,\ 1/2),$$

and then any two points sharing a nearest site are $\le 1$ apart **by the triangle inequality** —
no diameter computation, no case split into corner/edge/interior. Two independent routes to L4
that agree is the strongest thing in this section.

### The controls: no known value is violated

The lemma is only worth anything if it never exceeds a known $a_n$. Converting the `cited` table
via $a = (s(n)-2\sqrt3)/2$:

| $p$ | $n=\Delta(p)+1$ | bound $p\sqrt3/2$ | Oler | trivial $a_{\Delta(p)}=p-1$ | known $a_n$ | beats both? |
|---:|---:|---:|---:|---:|---:|:--|
| 2 | 4 | **1.732051** | 1.372281 | 1 | $\sqrt3 = 1.732051$ — **attained** | yes |
| 3 | 7 | 2.598076 | 2.274917 | 2 | $1+\sqrt3 = 2.732051$ | yes |
| 4 | 11 | 3.464102 | 3.216991 | 3 | $2+\tfrac{2\sqrt6}3 = 3.632993$ | yes |
| 5 | **16** | **4.330127** | 4.178908 | 4 | open ($\le 4.6247636$) | **yes** |
| 6 | **22** | **5.196152** | 5.152067 | 5 | open | **yes** |
| 7 | 29 | 6.062178 | **6.132169** | 6 | open | no — Oler wins |
| 8 | 37 | 6.928203 | **7.116844** | 7 | open | no |

Every row is consistent; nothing exceeds a known value. Three further points the file does not
make:

- **At $p=2$ the bound is attained exactly**, so it is *sharp* and can never be strengthened to a
  strict inequality by any argument of this shape. That is also the D1 witness — the sharp case
  and the broken case are the same configuration.
- The bound must beat not only Oler but the **trivial monotonicity bound**
  $a_{\Delta(p)+1}\ge a_{\Delta(p)} = p-1$. It does so exactly for $p\le6$.
- So the useful range is exactly **$n=16$ and $n=22$** — the other winning rows ($n=4,7,11$) are
  `cited` values already, where the bound is a reproof, not news. At $n=4$ it is a *tight* reproof
  of $s(4)=4\sqrt3$, which I confirm: the matching packing
  (`../exact-algebraic-constructions/certificates/n004-exact.json`) verifies exactly in my own
  checker, tight, min squared distance exactly 4.

### General $p$: the file calls this a `sketch`; it is closer to done than that

At the threshold $u_0 = g/3$ **independently of $p$**, so the construction is *locally the same
object* for every $p$. Census of cells translated to their own site (`lemmaL2.py` §E):

| $p$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| distinct cell shapes | 3 | 6 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |

and $\mathrm{shapes}(12) = \mathrm{shapes}(7)\cup\mathrm{shapes}(8)$ exactly. So "no other cell is
worse than the corner cell", which the file verifies case-by-case per $p$, is a statement about
**seven** cell shapes, not about $p$. A complete proof needs only the stabilisation step (a
Voronoi cell of a lattice site depends only on the sites within a bounded radius, and the
boundary configuration repeats by translation). **I did not write that proof**, so I am not
promoting the general-$p$ claim; I am saying the remaining gap is a paragraph, not a research
problem, and that $p=5$ — the only one $n=16$ needs — is verified outright.

---

## 2. Verdict on Lemma L and the $n=16$ bound

**Lemma L stands, with the §0 scaling repair, and only with it.**

$$\boxed{a_{16}\ \ge\ \tfrac{5\sqrt3}{2} = 4.3301270\ldots}\qquad
\text{i.e.}\qquad s(16)\ \ge\ 2\sqrt3 + 5\sqrt3 = 7\sqrt3 = 12.1243557\ldots$$

against Oler's $a_{16}\ge4.1789083$ ($s \ge 11.8219183$) — an improvement of $0.1512187$ in $a$
and $0.3024374$ in $s$. The proof, in the form I verified it, is four lines:

1. At $a_0 = 5\sqrt3/2$ the 15 clipped Voronoi cells of the centred spacing-$\sqrt3/2$ array are
   convex, cover $T_{a_0}$, and every one has diameter $\le1$ (exact, `lemmaL.py`; independently,
   covering radius $=1/2$, `lemmaL3.py`).
2. For $a<a_0$ scale that partition by $\mu = a/a_0$: 15 sets covering $T_a$, each of diameter
   $\le\mu<1$ (exact, `lemmaL2.py` §F).
3. 16 points at pairwise distance $\ge1$ in $T_a$ would put two in one set, at distance
   $\le\mu<1$. Contradiction. So $T_a$ holds at most 15 such points for every $a<a_0$.
4. $a_{16}$ is attained (compactness), hence $a_{16}\ge a_0$.

**Caveats that travel with it, all of them the author's own and all of them correct:**

- **This grants no status.** Same model family; see the banner. It is `sketch` before and after.
- **Novelty is unverified and should be assumed absent.** Pigeonhole against a lattice covering is
  a standard discrete-geometry move. I retried the literature egress this session
  (`ris.utwente.nl`, the Melissen–Schuur PDF): `CONNECT tunnel failed, response 403`, the same
  block [`../eo-literature/`](../eo-literature/) recorded. **Nobody in this repo has checked
  whether $s(16)\ge7\sqrt3$ is in Melissen–Schuur (1995) or Melissen's thesis, and until someone
  does, "beats Oler" must not be written as "new".**
- It is a lower bound at an **open** case, so no published value can confirm or contradict it; the
  controls above are the only external check available, and they pass.

---

## 3. Live lanes

Written as their files landed. Where a lane had produced no certificate by the end of this pass,
that is stated rather than guessed at.

### 3.1 What I built for them, and what it is calibrated against

| checker | what it checks | calibration |
|---|---|---|
| [`packcheck.py`](../../../../experiments/packing-n16-verify/packcheck.py) | packing certificates: all $\binom n2$ squared distances $\ge4$, containment in the **closed** triangle at the fixed placement, `side_length` $=s$ not $d$, decimal strings rejected, and the **exact minimal enclosing side** $d_{\min}=\max_i(x_i+y_i/\sqrt3)$ for tightness | 167 checks on the repo's 8 existing exact certificates ($n\le6$), all pass, all tight; **both negative controls fire** — a triangle shrunk by $10^{-3}$ and a pair moved together by $10^{-3}$ are each rejected |
| [`lemmaL.py`](../../../../experiments/packing-n16-verify/lemmaL.py) + `lemmaL2/3.py` | coverings: exact squared diameters, containment, pairwise interior-disjointness, area identity, grid probe, covering radius | reproduces Lemma L at $p=2..12$; the above-threshold control fails as it must |

**On tightness, since it is the one that lets an inflated certificate through.** Problem
`RULES.md` §2 requires the minimal enclosing value, and containment alone certifies only
$s(n)\le s$. `packcheck.py` computes $d_{\min}$ exactly and reports `TIGHT: d - d_min = 0` or the
exact excess. Any $n=16$ record claim must show $d = d_{\min}$ **exactly**, not "to $10^{-12}$".

### 3.2 Per-lane state at the close of this pass

| lane | state when I looked | verdict |
|---|---|---|
| `n16-exact` | `certificates/` empty; working data is an 80-dps `mpmath` refinement (`experiments/packing-n16-exact/out/refined.json`) with $d = 9.2495271590\ldots$, $s = 12.7136287741\ldots$ | **no certificate to verify yet.** The refinement agrees with Graham–Lubachevsky's $d(16)=0.216227269309782$ to the digits printed ($a = d/2 = 4.62476357950\ldots = 1/d(16)$), which is the right target. It is 80-digit floating point, so it is a hypothesis, not a certificate (`RULES.md` §2 bans decimal strings in exact fields, and these are decimal strings) |
| `n16-covering` | `KILL-CRITERION.md` only; float optimiser output `opt_n15_*.json` in flight | **no certificate to verify yet.** Its mechanism section is correct and states the strictness point exactly right: pieces must have diameter **strictly** $<1$ because separation is non-strict. Its K3 ceiling ($a^\star > 4.62476 \Rightarrow$ wrong) is the correct ceiling, and for the right reason — 16 points at separation $\ge1$ in $T_a$ force $\ge16$ pieces of diameter $<1$ |
| `n16-upper` | `KILL-CRITERION.md` only | **nothing to verify yet.** Its abort-and-exactify trigger and its refusal to write a summary line before the exact gate are the right procedure |
| `n16-capacity` | directory does not exist in this tree | **nothing produced** |

### 3.3 Standing instructions for whoever verifies these next

- **Covering certificates.** Reject any piece with squared diameter $=1$ exactly: for this route
  it must be $<1$ strictly, and D1 is what that rule is protecting against. Check the area
  identity *and* a grid probe — the area identity alone cannot catch a piece list that double
  covers one region and misses another of equal measure, and the probe can.
- **A covering bound above $4.6247635795$ is wrong**, unconditionally, once the Melissen–Schuur
  packing is exactly certified — and that certification is `n16-exact`'s deliverable, so the two
  lanes gate each other. Until it lands, the honest ceiling is the *conditional* one.
- **A packing claim beating $a_{16}\le4.6247635795$** is an `RULES.md` §7 extraordinary claim.
  The specific failure mode to check first is the one named in the brief: a raw side length not
  divided by the achieved separation. `packcheck.py` cannot make that mistake — it takes $s$ from
  the certificate and recomputes $d_{\min}$ from the coordinates — so run the coordinates through
  it and compare, rather than comparing reported scalars.
- **`eo-covering-construct` §6's "$a_{16}\le4.6304$"** is that lane's own optimiser output and is
  weaker than the published $4.6247636$. Not an error; do not quote it as the record.

---

## 4. What is safe to build on

The flat answer `RULES.md` §3 requires: **nothing here is assumable, and nothing here changes any
status.** The column below answers the weaker question — has an independent reader re-derived it
from the statement, in their own exact code, and tried to break it?

| Claim | Re-derived? | Safe to build on? |
|---|---|---|
| **Lemma L as stated** ($T_a$ = $\Delta(p)$ convex cells, diameter $\le1$, $a\le p\sqrt3/2$), $p=2..12$ | yes, exactly, two independent routes | **Yes** — but only ever together with D1's warning |
| **The scaled partition**: for $a<a_0$, $\Delta(p)$ sets of diameter $\mu<1$ covering $T_a$ | yes, exactly | **Yes.** This, not Lemma L, is the object the bound needs |
| **$a_{16}\ge5\sqrt3/2$, $s(16)\ge7\sqrt3$** | yes, all four steps | **Yes as mathematics, `sketch` as status.** Novelty unchecked — do not call it new |
| **$a_{22}\ge3\sqrt3$** | yes (same lemma at $p=6$) | **Yes**, same caveats |
| **"the corner cell is the binding one" / "that is why the max is 1"** | yes | **NO** (D2). The interior hexagons pin the maximum at 1 at every $a$; the edge cells bind simultaneously with the corner |
| **Applying Lemma L at $a<a_0$ and pigeonholing** | yes — and it is false | **NO** (D1). Witness: 4 points in $T_{\sqrt3}$ against 3 cells |
| **Lemma L for general $p$** | census through $p=12$; the stabilisation argument is not written | **Partly** — verified where it is used ($p=5$, $p=7$); "all $p$" is still the author's `sketch`, though a short one |
| **$n=16$ lane certificates** | none existed to check | **Nothing to say.** No certificate, no verdict |
| **$a_{16}\le4.6247635795$ (Melissen–Schuur via G–L)** | no — it is a 15 s.f. table value, not yet certified in this repo | **Not yet.** Treat as literature until `n16-exact` produces exact coordinates |

### Claimed proofs of open cases — my independent verdict

**One, and it is a lower bound, not an optimality proof.** $a_{16}\ge5\sqrt3/2$ and
$a_{22}\ge3\sqrt3$ improve on Oler at two open cases. They are correct as mathematics — I rebuilt
every step in exact arithmetic and tried to break the one step that is breakable (D1) and found
that it *is* broken as stated and *is* repaired by the file's own §0. They settle no case: $s(16)$
remains open between $7\sqrt3 = 12.1244$ and $12.7136$. And their novelty is unverified with the
literature egress blocked, which for a bound this elementary is the likeliest place the claim
dies.

## 5. Reproducing

```
cd experiments/packing-n16-verify
python3 lemmaL.py          # 2900 exact checks: Lemma L, threshold, controls
python3 lemmaL2.py         # 38: shape census, the scaling repair, which cell binds
python3 lemmaL3.py         # 14: grid probe, covering radius
python3 packcheck.py --selftest   # 167: 8 known certificates + 2 negative controls
```

Standard library plus `sympy`; no seeds, no tolerances, no float in any decision; every script
exits non-zero on any failure.
