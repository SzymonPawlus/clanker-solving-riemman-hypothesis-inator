# Verification 4: independent reconstruction of Theorem N (`../n16-structure/`)

**Claim type: NEITHER** of problem [`../../RULES.md`](../../RULES.md) §1 — this file reviews a
covering-counting theorem and asserts no bound on $s(16)$ in either direction. Nothing enters
`results/`.

- Reviewer: `claude`, worker **V4** (Claude Opus 5 — convergent role, repo
  [`RULES.md`](../../../../RULES.md) §8), 2026-08-22, issue
  [#97](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/97)
- Under review: [`../n16-structure/README.md`](../n16-structure/README.md), authored by the campaign
  **manager** (Claude Opus 5), previously unreviewed
- My code: [`experiments/packing-n16-verify-4/`](../../../../experiments/packing-n16-verify-4/) —
  written from the geometry, standard library only, exact `Fraction` / $\mathbb{Q}(\sqrt3)$ in every
  decision. **I did not read, import, adapt or run `experiments/packing-n16-structure/`**; the only
  contact with that directory was `grep` for the string `Borsuk` (item 6).
- The 15 polygons were re-transcribed **by hand from the table in
  [`../n16-covering-2/README.md`](../n16-covering-2/README.md)**, not from any code.

> **This cannot grant `verified:review`.** The author is Claude Opus 5 and so am I;
> [`RULES.md`](../../../../RULES.md) §5 requires a different model family, and problem
> [`RULES.md`](../../RULES.md) §3 requires the other agent to reimplement the check from the problem
> statement. What follows is an independent **same-family reconstruction**. Theorem N stays
> `sketch`, and the two corrections below are not repaired by my agreeing with the rest.

---

## Verdict summary

| # | item | verdict |
|---|---|---|
| 1 | Lemma 3, corner reach $2/\sqrt3$, incl. the quantifier | **confirmed** |
| 2 | class disjointness / additivity of the three bounds | **confirmed** |
| 3 | floor-plus-one, and where integer $\lvert M_e\rvert$ occurs | **confirmed** |
| 4 | Lemma 4, $\delta = a - 2\sqrt3$ | **confirmed** (re-derived twice) |
| 5 | Lemma 2, Viviani, inequality direction | **confirmed** |
| 6 | $d\ge4$ branch, $3\sqrt3$, Borsuk-freeness | **confirmed** |
| 7 | §4 exact verification against the certificate | **confirmed-with-correction** (scope: the certificate's pieces have diameter exactly 1, so it is not an instance of Theorem N) |
| 8 | §5.1's retraction of the Lemma-S combination | **refuted** — the arithmetic reproduces, the conclusion drawn from it does not |
| 9 | attempt to break it | **the headline corollary is refuted**; Theorem N itself survived every attack I made |

**Two corrections, both in the sentence *after* a correct theorem** — the exact failure shape
`FINDINGS.md` logged for 2026-08-21. Theorem N is, as far as I can reconstruct it, **correct**.

---

## 1. Lemma 3 — the corner-reach constant $2/\sqrt3$

**checked.** Re-derived from scratch. $P$ on $AB$ at distance $\alpha$ from the apex, $Q$ on $AC$ at
distance $\beta$, apex angle $60^\circ$, so $|PQ|^2 = \alpha^2+\beta^2-2\alpha\beta\cos60^\circ
=\alpha^2+\beta^2-\alpha\beta$. The minimisation is an exact algebraic identity, which I verified
symbolically over `Fraction` rather than by calculus:
$$\alpha^2+\beta^2-\alpha\beta \;=\; \tfrac34\alpha^2 + \bigl(\beta-\tfrac\alpha2\bigr)^2 .$$
Hence $\tfrac34\alpha^2 \le |PQ|^2 < 1$, so $\alpha^2 < 4/3$ and $\alpha < 2/\sqrt3 = 2\sqrt3/3 =
1.1547\ldots$; $(2/\sqrt3)^2 = 4/3$ confirmed exactly in $\mathbb{Q}(\sqrt3)$. The minimum is at
$\beta=\alpha/2$, value $3\alpha^2/4$, as stated.

**The quantifier is sound, and the write-up's justification for it is not.** "This holds for every
point of the trace, since the bound was derived from an arbitrary pair" is loose — arbitrariness of
*a pair* is not what is needed. The correct argument, which does give the claim: **fix any single**
$Q\in S_i\cap AC$; then for **every** $P\in S_i\cap AB$ we have $|PQ|\le\operatorname{diam}S_i<1$,
so the inequality $\tfrac34|AP|^2<1$ holds for that $P$. So every trace point on $AB$ is within
$2/\sqrt3$ of the apex. The conclusion stands; I recommend the one-line rephrasing, because as
written the sentence is the kind of hand-wave that hides a genuine quantifier error elsewhere.

**not-checked.** Nothing.

**verdict: confirmed.**

## 2. Class disjointness and the additivity of the three bounds

**checked.** Membership is decided by an integer-valued function (how many of the three sides the
piece meets), so the four classes partition the pieces — disjointness is immediate and I confirm the
one sentence carries it. I then checked the three bounds separately for double counting:

- $c\ge3$ counts the three apex pieces. They are two-side, not three-side, **because** $a>4/\sqrt3$
  (Lemma 2) — the hypothesis is genuinely used here, not decorative. Distinct because the apexes are
  $a>1$ apart.
- $b$ is a sum over the three sides of $b_e = \#\{$one-side pieces meeting $e\}$. A one-side piece
  meets exactly one side, so the three sets are disjoint and $b=\sum_e b_e$. No two-side piece
  enters any $b_e$ (that is what Lemma 3 buys), no no-side piece meets any side, no three-side piece
  exists. So the per-side bounds add and none of them touches $c$'s pieces.
- $d$ counts no-side pieces only, via Lemma 4.

Since there are no three-side pieces, the total is in fact **equal** to $c+b+d$, not merely $\ge$.

**not-checked.** Nothing.

**verdict: confirmed.**

## 3. Floor-plus-one, and whether integer $\lvert M_e\rvert$ occurs

**checked.** Re-derived in the form that survives non-measurable pieces, which is what the theorem
needs (the $S_i$ are arbitrary sets): if $k$ traces cover $M_e$ then by countable subadditivity of
**outer** Lebesgue measure on the line, $|M_e| \le \sum_i \lambda^*(S_i\cap e) \le \sum_i
\operatorname{diam}(S_i\cap e) < k$. So $k > |M_e|$, i.e. $k \ge \lfloor |M_e|\rfloor + 1$ — for
integer $|M_e|$ as well as non-integer, and $\lceil\cdot\rceil$ is one too few exactly at integers.
Confirmed. (Minor: the write-up says the trace lengths "sum to more than $|M_e|$"; subadditivity
gives $\ge$, and the strictness comes from each length being $<1$. The conclusion is unaffected.)

**Where integer $|M_e| = a - 4/\sqrt3$ occurs:** exactly at $a = k + 4/\sqrt3$. In the range the
write-up uses, that is $a = 2+4/\sqrt3 = 4.309401$ and $a = 3+4/\sqrt3 = 5.309401$. The second is
one of the two thresholds quoted in §5, and there floor-plus-one gives $4$ where ceiling gives $3$ —
so the distinction is load-bearing precisely where the write-up invokes it. At the headline value
$a = 1+2\sqrt3$, $|M_e| = 1+2\sqrt3-4\sqrt3/3 = 2.1547\ldots$ is **not** an integer, so the headline
does not depend on this subtlety. All four facts confirmed exactly.

**not-checked.** Nothing.

**verdict: confirmed.**

## 4. Lemma 4 — the inner-parallel side $\delta = a - 2\sqrt3$

**checked.** Derived twice, independently of the write-up's one-line reason.

1. *Inradius scaling.* Eroding a triangle by $t$ gives the similar triangle scaled by $(r-t)/r$,
   $r$ the inradius. For an equilateral triangle of side $a$, $r = a/(2\sqrt3)$, so $t=1$ gives
   $\delta = a(1 - 1/r) = a - a/r = a - 2\sqrt3$, since $a/r = 2\sqrt3$ **independently of $a$**.
   Sanity: $a = 2\sqrt3$ gives $\delta = 0$ and inradius exactly $1$. ✔
2. *Directly in the triangular chart*, which is a different computation. With
   $(u,v)\mapsto u e_1+v e_2$, the three side-distances are $u\sqrt3/2$, $v\sqrt3/2$,
   $(a-u-v)\sqrt3/2$ (Viviani), so
   $D = \{u\ge 2/\sqrt3,\ v\ge 2/\sqrt3,\ u+v\le a-2/\sqrt3\}$, an equilateral triangle of side
   $(a-2/\sqrt3) - 2\cdot(2/\sqrt3) = a - 6/\sqrt3 = a - 2\sqrt3$. ✔ (`6/sqrt3 == 2*sqrt3` checked
   exactly in $\mathbb{Q}(\sqrt3)$ — this is the spot where a stray $\sqrt3$ would live.)

The second half of Lemma 4 (a piece meeting $D$ meets no side) is Lemma 1's contrapositive and is
correct: a piece meeting side $e$ has every point at distance $<1$ from $e$, and every point of $D$
is at distance $\ge1$ from $e$.

**not-checked.** Nothing.

**verdict: confirmed. No separation-1/separation-2 factor is hiding here.**

## 5. Lemma 2 — no piece meets three sides for $a > 4/\sqrt3$

**checked.** Direction is right: the three distances from $p_1$ are $0$, $<1$, $<1$, summing to
$<2$; Viviani makes the sum equal to the height $a\sqrt3/2$; so $a\sqrt3/2 < 2$, i.e.
$a < 4/\sqrt3 = 4\sqrt3/3 = 2.3094\ldots$ — a **contradiction** in the stated range $a>4/\sqrt3$,
which is the direction claimed. I also checked the step the write-up passes over: Viviani is about
distances to the three *lines*, while Lemma 1 bounds distance to the *segment*. For an acute
triangle the foot of the perpendicular from any point of the triangle onto a side-line lies inside
that side (the triangle sits inside the slab bounded by the perpendiculars at the two endpoints), so
the two agree and the substitution is legal. $4/\sqrt3 = 4\sqrt3/3$ confirmed exactly.

**not-checked.** Nothing.

**verdict: confirmed.**

## 6. The $d\ge4$ branch and its Borsuk-freeness

**checked.** The circumradius of an equilateral triangle of side $\delta$ is $\delta/\sqrt3$, so the
centroid of $D$ is at distance $\delta/\sqrt3$ from each apex, and
$\delta/\sqrt3\ge1 \iff \delta\ge\sqrt3 \iff a \ge 2\sqrt3+\sqrt3 = 3\sqrt3 = 5.196152\ldots$
(exact in $\mathbb{Q}(\sqrt3)$). With $\delta\ge\sqrt3>1$ the three apexes are also pairwise $\ge1$
apart, so the four points are pairwise $\ge1$ apart and occupy four distinct pieces. The write-up's
note is right: this is plain pigeonhole on four points and needs **no** partition-optimality input,
Borsuk or otherwise — nothing here asserts that three parts *cannot* do better, only that four
separated points exist.

**Borsuk-freeness of the published version, confirmed.** `grep -rniE "borsuk|4\.6188|8.*sqrt"` over
`attacks/n16-structure/` and `experiments/packing-n16-structure/` returns exactly one hit: the
sentence in §2 saying no Borsuk-type input is required. The retracted threshold
$8\sqrt3/3 = 4.618802$ appears nowhere in the lane. For the record I computed both constants:
$8\sqrt3/3 = 4.618802$ (the false one, below the best-known packing $4.6247637$) and $3\sqrt3 =
5.196152$ (the correct one, far above it).

**not-checked.** The author's `structure.py` was not read beyond that `grep`.

**verdict: confirmed.**

## 7. §4's exact verification against the standing certificate

**checked — everything, from my own transcription and my own checker.** I typed the 15 polygons out
of `../n16-covering-2/README.md`'s table into `verify4.py`, computed each piece's convex hull
exactly, and reproduced every line of §4's table:

| §4 prediction | my independent result |
|---|---|
| all pieces inside $T_a$ | ✔ every vertex satisfies $u,v\ge0$, $u+v\le a$ exactly |
| max squared diameter | ✔ exactly $1$ |
| two-side $=3$ | ✔ and they are pieces $\{0,4,14\}$ |
| one-side $=9$ | ✔ $\{1,2,3,5,8,9,11,12,13\}$ |
| no-side $=3$ | ✔ $\{6,7,10\}$ |
| three-side $=0$ | ✔ |
| $5$ pieces per side | ✔ all three sides |
| $\delta = a-2\sqrt3 = 1$ | ✔ exactly; $D$'s apexes pairwise at squared distance exactly $1$ |
| the 3 no-side pieces cover $D$ | ✔ residue empty by half-plane clipping, no area identity |
| no single piece covers $D$ | ✔ (control fails as it must) — I added: no **pair** of $\{6,7,10\}$ covers $D$ either |
| two-side traces $<2/\sqrt3$ | ✔ every vertex of a two-side piece is at squared distance $\le1<4/3$ from its apex |

I added a transcription check the author's §4 does not have: **the 15 pieces I transcribed do cover
$T_a$** (exact residue subtraction, residue empty). If I had mistyped a vertex, that check would
fail, and one of my five corruption tests confirms it does fail under a $1/30$ perturbation. My
coverage routine was smoke-tested first (square by two half-triangles: covered; by one: not; by a
5%-short copy: not; by three *overlapping* strips: covered) and then fed five deliberate
corruptions, all caught. One honest note on my own process: my first corruption test *passed* the
checker, and it was the test that was wrong — I had moved a shared vertex **outward**, which grows
the union. Corruption tests need the sign checked too.

**correction (scope, not arithmetic).** Every piece of this certificate has diameter **exactly 1**.
Theorem N's hypothesis is diameter **strictly** $<1$. So the standing certificate is *not* an
instance of Theorem N, and §4 cannot be what it is billed as — "exact verification against the
standing certificate" reads as a test that could have refuted the theorem, and it could not have:
had the counts come out $3/8/4$, Theorem N would have been untouched. What §4 actually establishes
is that the object the searches converge to is *consistent with* the structure Theorem N forces in
the open range. That is worth having, and the diameter-exactly-1 fact is stated plainly elsewhere in
both lanes, so nothing is concealed — but the section overstates its own power.

**not-checked.** `n16-covering-2`'s dilation argument, and its claim that the pieces are pairwise
interior-disjoint (irrelevant to Theorem N, which is disjointness-free).

**verdict: confirmed-with-correction.**

## 8. §5.1 — "the obvious next step is dead"

**checked, and this is where I part company with the write-up.**

Both numbers reproduce. Exactly, by rational interval arithmetic on $\pi$ and $\sqrt3$ to 30 digits:
$$\tfrac{\sqrt3}{4}a^2 = 3\cdot\tfrac\pi6 + 12\cdot\tfrac\pi4 = \tfrac{7\pi}{2}
\quad\Longrightarrow\quad a = \sqrt{14\pi/\sqrt3} \in [5.039165715,\ 5.039165715],$$
matching the published U1 $= 5.039166$ to 6 dp; U0 $=5.216032$ likewise. Row 2 reproduces at
$4.920765783$ (mpmath, 200 bits — it contains $\arcsin$).

**The two conclusions drawn from those numbers do not follow.**

**(a) Row 1 is not an independent confirmation of U1 — it is the same inequality.** "Reproduces that
lane's U1 to six decimal places, from a completely different derivation of the counts" overstates
it: $3\cdot\pi/6 + 12\cdot\pi/4$ uses only "3 corner pieces, 12 other pieces", and
`n16-covering-limit`'s Lemma S(a) already had exactly that. No class information beyond it enters
either side. Two evaluations of one formula agreeing is an arithmetic check, which is worth
running — it is not decorrelated evidence for the number.

**(b) "The structure is identical; my row 2 is worse only because their $f$ is stronger" is false,
and the retraction that rests on it does not hold.** Lemma S does **not** know the class counts. It
knows only $k_e\ge3$ and $\sum_e k_e\le 12$, and `outer.py` therefore **maximises** the right-hand
side over every admissible $(k_1,k_2,k_3)$. Theorem N pins the split at exactly $3/9/3$, which
deletes the $k_e\ge4$ branches. Holding $f$ fixed at the same capped closed form for both sides:

| budget, same capped closed-form $f$ | ceiling on $A_{15}$ |
|---|---:|
| Lemma S as stated (max over admissible $k$; attained at $k=(4,4,4)$) | $5.039166$ — it **degenerates back to U1** |
| Theorem N's forced $3/9/3$, middle $a-4/\sqrt3$ | $\mathbf{4.920766}$ |

So at equal $f$-quality the forced counts are worth $0.118$, not nothing. And
`n16-covering-limit` itself says its binding case is "$\ell=(a-2)/4\approx0.66$" — i.e. U2 is decided
by the $k_e=4$ branch, which is exactly the branch Theorem N excludes. Feeding the forced counts
into that lane's *certified* $f$ at $\ell = (a-4/\sqrt3)/3 \approx 0.87$ is therefore an untried
combination that plausibly lands **below** U2 $=4.914308$; a back-of-envelope substitution of the
LP's typical $\approx0.02$ improvement over the closed form puts it near $4.88$. I have not
certified that — I did not rerun that lane's slab LP — but the write-up's claim is the opposite one,
and it is the claim that redirects the campaign: "**a worker sent to combine them would have spent a
day rediscovering U1**" is, on this evidence, wrong, and it retires a live lead.

**not-checked.** The slab-LP $f$ itself (that lane's certified numbers were taken at face value);
whether the concave envelope $\hat f$ differs from $f$ on the relevant interval — both the author's
row 2 and my reproduction of it use $f$, not $\hat f$, so **neither is a certified bound**, only a
like-for-like comparison.

**verdict: refuted** (the arithmetic is right; the retraction it supports is not).

## 9. Attempt to break it — and the headline corollary falls

**Theorem N itself survived.** I could not construct a covering satisfying its hypotheses that
violates its conclusion, and I found no $a$ in the claimed range where the counting function is
wrong: my independent implementation of $c=3$, $b=3(\lfloor a-4/\sqrt3\rfloor+1)$, $d\in\{1,3,4\}$
reproduces §3's table row for row, and both thresholds ($3\sqrt3$; $3+4/\sqrt3$) land where §5 says.

**The headline corollary is false.** §3 asserts, in bold, and `FINDINGS.md` repeats:

> $1+2\sqrt3$ is the least $a$ at which fifteen pieces are necessary.

Counterexample, exact and elementary. Take the unit triangular lattice with five points per side:
$\{i e_1 + j e_2 : i,j\ge0,\ i+j\le4\}$. That is **15 points, all in the closed $T_4$, pairwise at
distance $\ge1$** (the form $du^2+du\,dv+dv^2$ takes integer values $\ge1$ on nonzero integer
vectors; minimum exactly $1$, checked exactly). A piece of diameter $<1$ contains at most one of
them, so **every** covering of $T_4$ by diameter-$<1$ pieces uses at least 15 pieces. Writing
$N(a)$ for the minimum number of such pieces, $N$ is non-decreasing, so

$$N(a)\ \ge\ 15\quad\text{for every } a\ \ge\ 4, \qquad 4\ <\ 1+2\sqrt3 = 4.4641\ldots$$

Fifteen pieces are necessary a full $0.4641$ **below** the claimed threshold. The least such $a$ is
at most $4$; and since $s(15) = 8+2\sqrt3$ is `cited` optimal (Oler, triangular number), $a_{15}=4$
exactly, so no point-pigeonhole argument can push it below $4$ either.

What is true is the qualified version, which §3's own prose says before the bold sentence drops the
qualifier: **$1+2\sqrt3$ is the least $a$ at which *Theorem N's counting* forces fifteen pieces.**
Theorem N is unharmed — it is a valid lower bound — but it is not close to tight: at $a=4$ it forces
**10** where the truth is $\ge15$. A bound that is 5 pieces slack at $a=4$ arriving at 15 exactly at
$1+2\sqrt3$ is therefore **not** evidence that $1+2\sqrt3$ is where anything changes.

**The mechanism claimed for the plateau does not survive either.** The searches converge on
$A_{15}=\sup\{a: T_a$ is coverable by 15 pieces$\}$. Theorem N bounds
$\min\{a: N(a)\ge15\}$ — a *different* quantity, which I have just shown is $\le4$. Theorem N
constrains $A_{15}$ only from above, via $A_{15}\le3\sqrt3$, and even that is weaker than the
one-line $A_{15}\le a_{16}\le4.6247637$ (best-known packing, `numerical`). So "it is not a
coincidence, and it is not an artefact of the search" is not established by anything in the file;
the coincidence of two constants remains, at this point, a coincidence.

**verdict: refuted (the corollary and §1's explanation), Theorem N confirmed.**

---

## Corrections

State them plainly; each is a documented success, not a defect of the lane.

1. **§3's bold sentence and the corresponding sentence in `FINDINGS.md` are false as written.**
   Replace "the least $a$ at which fifteen pieces are necessary" with "the least $a$ at which
   *Theorem N's counting* forces fifteen pieces". 15 pieces are in fact necessary for all $a\ge4$,
   by the 15-point triangular lattice in $T_4$. §1's "it is not a coincidence" claim, and the
   `FINDINGS.md` framing "the optimisers were sitting on the first point where the count they
   achieve equals the count that is forced", both go with it: what is forced at $1+2\sqrt3$ is 15,
   and 15 is also forced at $4.0$, where the searches are nowhere near.
   *`FINDINGS.md` is outside my file ownership; the manager needs to amend it.*
2. **§5.1's retraction is not supported.** Its two rows reproduce exactly, but row 1 is the same
   inequality as U1 rather than an independent route to it, and row 2's comparison holds $f$
   unequal. At equal $f$, forcing the counts is worth $0.118$ and removes precisely the $k_e=4$
   branch that decides U2. The lead it retires should be un-retired.
3. **§4's scope.** The certificate's pieces have diameter exactly $1$, so it is not an instance of
   Theorem N; §4 is a consistency check, not a test the theorem could have failed.
4. **Two wording fixes with no consequence for the result.** Lemma 3's "derived from an arbitrary
   pair" should be "fix any point of the other trace, then the bound holds for every point of this
   one"; Theorem N's edge step should read "sum to at least $|M_e|$", the strictness coming from
   each trace being shorter than $1$. Also, the "deep $=1$" entries in §3's table use $d\ge1$ when
   $0<\delta<1$, which is true but is not part of the stated theorem.

## Status after this review

Theorem N and its four lemmas: **still `sketch`**, and unchanged in substance — I reconstructed
every step and landed in the same place. This review **cannot** promote them
([`RULES.md`](../../../../RULES.md) §5: same model family, and the author is Claude Opus 5 as I am).
The corollary in §3, the framing in §1, and the retraction in §5.1 should be treated as
**`refuted`** until rewritten.

## Reproduce

```bash
python3 experiments/packing-n16-verify-4/verify4.py     # 61 exact checks, under 2 s, "FAILURES: none"
```

Optional, and explicitly *not* exact — it contains $\arcsin$, so it is mpmath at 200 bits and
decides nothing that is reported as a bound:

```bash
python3 experiments/packing-n16-verify-4/budget3.py     # the item-8 like-for-like comparison
```

Python standard library only for `verify4.py`; no seeds, no network, no floats in any decision
(`approx()` formats printed columns and seeds one integer search that is then confirmed exactly).
