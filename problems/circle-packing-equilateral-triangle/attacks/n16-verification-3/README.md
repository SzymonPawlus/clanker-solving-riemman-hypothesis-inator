# Verification pass 3 over the $n=16$ covering lower bound

**Claim type: neither construction nor optimality** (problem [`../../RULES.md`](../../RULES.md)
§1 asks for that line first). Nothing here asserts a bound of its own. It re-derives, from
scratch, the bound already claimed in [`../n16-covering-2/`](../n16-covering-2/), and tries to
break it.

- Examiner: `claude` (Claude Opus 5), worker **V3**, 2026-08-22, issue #97,
  branch `claude/circle-packing-subagents-9yg5gt`
- Code: [`experiments/packing-n16-verify-3/`](../../../../experiments/packing-n16-verify-3/) —
  Python standard library only for every accept/reject decision (`fractions`, and
  $\mathbb{Q}(\sqrt3)$ as pairs of `Fraction`). NumPy/SciPy appear in exactly one file
  (`break_attempt.py`), which decides nothing.
- Predecessors, not reused: [`../n16-verification/`](../n16-verification/),
  [`../n16-verification-2/`](../n16-verification-2/).

> ## THIS GRANTS NO STATUS
>
> Repo [`RULES.md`](../../../../RULES.md) §5 and this problem's `RULES.md` §3: `verified:review`
> requires an examiner from a **different model family than the author**. I am **Claude Opus 5**,
> the author is Claude Opus 5, and so were the three checkers before me. **I cannot grant
> `verified:review` and I am not granting it.** Everything below — including everything I
> confirm — stays `sketch` and stays non-assumable. What this pass buys is a fourth *independent
> reconstruction* and a documented failure to break the claim. A **Codex** pass is still required.

**Independence.** I did not read, import, adapt or run `verify_c1.py`, `q3.py`, `exact_1p2r3.py`,
`rational_cert.py`, `selftest.py`, or either predecessor's certifier. `check_v3.py` was written
from [`../../README.md`](../../README.md) (the statement and the reduction) and
[`../../RULES.md`](../../RULES.md) §2 (the conventions) alone. The only things I took out of
`experiments/packing-n16-covering-2/` are certificate **data**: the vertex table printed in the
attack README (re-transcribed by hand into [`cert_v3.py`](../../../../experiments/packing-n16-verify-3/cert_v3.py))
and `cert_rational.json`.

---

## 0. Headline

| | |
|---|---|
| $a_{16}\ge 1+2\sqrt3$, hence $s(16)\ge 2+6\sqrt3 = 12.392304845413264\ldots$ | **CONFIRMED** — certificate and limiting argument both reconstructed independently |
| The 15-piece certificate at $a=1+2\sqrt3$ | 15 pieces, all in $T_a$, all strictly convex, **all of squared diameter exactly 1**, pairwise interior-disjoint, union **exactly** $T_a$ with no sliver — all exact, coverage proved without any area argument |
| The dilation step (the one that matters) | **airtight**; written out in full in §4 |
| Discriminating test on the D1 witness that kills the naive lemma | dilation returns the **sharp** $a_4\ge\sqrt3$, not the false $a_4>\sqrt3$ |
| The purely rational, strictly-sub-diameter-1 certificate | **CONFIRMED independently**: $a_{16}\ \ge\ \tfrac{446410161513599}{10^{14}}$ with **no limiting argument at all** |
| Attempt to refute | **failed** — 120 multistart minimax runs; best 16-point configuration needs $a=4.62476358$, nowhere near $4.4641$ |
| $a_n$ table for $n\le15$ used as capacity input | **all 15 rows re-derived exactly** from the problem README's $s(n)$ column; no errors |
| Corrections found | **one**, in a `sketch` auxiliary claim, not in the bound — §7 |

Ceiling check (`RULES.md` §7): $4.4641016 < 4.6247636$, headroom $0.1613$ in $a$. **Nothing here
comes near settling $n=16$** and nothing here should be described as if it did.

---

## 1. (a) Restating the claim in my own words and normalisation

Work in the chart $x = ue_1+ve_2$, $e_1=(1,0)$, $e_2=(\tfrac12,\tfrac{\sqrt3}2)$, so that
$|ue_1+ve_2|^2 = u^2+uv+v^2$ and
$$T_a\;=\;\{(u,v)\;:\;u\ge0,\ v\ge0,\ u+v\le a\}$$
is a closed equilateral triangle of side $a$ (its chart corners $(0,0),(a,0),(0,a)$ are the
Cartesian $(0,0),(a,0),(a/2,a\sqrt3/2)$ of problem `RULES.md` §2, rescaled). Call a finite
$X\subset T_a$ **separated** if all pairwise distances are $\ge1$ — **non-strict**, per §2. Put
$$a_n \;=\;\inf\{\,a\;:\;T_a\text{ contains a separated set of size }n\,\}.$$

> **The claim.** $a_{16}\ \ge\ 1+2\sqrt3$.
>
> Unpacked with no reference to any certificate: *for every $a<1+2\sqrt3$, it is impossible to
> place 16 points in a closed equilateral triangle of side $a$ with all $\binom{16}{2}$ pairwise
> distances at least 1.*

That restatement is precise, and it is what the attack file asserts. Two things it does **not**
say, both of which I checked the file also does not say: it does not claim $a_{16}=1+2\sqrt3$
(the true value is somewhere in $[1+2\sqrt3,\,4.6247637]$), and it does not claim anything about
$T_a$ at $a=1+2\sqrt3$ itself.

```
checked:      the statement is unambiguous once the normalisation is fixed, and the attack's
              normalisation matches the problem RULES.md §2 chart up to the stated rescaling.
not-checked:  nothing.
verdict:      confirmed
```

---

## 2. (b) The reduction $s(n)=2a_n+2\sqrt3$, and the $n=16$ conversion

Re-derived from [`../../README.md`](../../README.md) without looking at any attack file
([`table_check.py`](../../../../experiments/packing-n16-verify-3/table_check.py) carries the
derivation as a docstring):

1. A unit circle inside a triangle of side $s$ has its centre $\ge1$ from each side; that locus
   is the inner-parallel equilateral triangle. Moving a side inward by 1 shortens it by
   $1/\tan30° = \sqrt3$ at **each** end, so the centre triangle has side $d=s-2\sqrt3$.
2. Two unit circles are non-overlapping iff their centres are $\ge2$ apart. So
   $s(n)=2\sqrt3+d(n)$ with $d(n)$ the least side admitting $n$ points at separation $\ge2$.
3. $a_n$ is defined at separation **1**. The similarity $x\mapsto2x$ is a bijection between
   separation-1 configurations in $T_a$ and separation-2 configurations in $T_{2a}$, in both
   directions. Hence $d(n)=2a_n$ and
   $$\boxed{\,s(n)=2a_n+2\sqrt3\,}$$

Step 3 is the standing trap (`FINDINGS.md`, 2026-08-21: a manager broadcast a wrong table after
mis-diagnosing a separation-1/separation-2 slip). I did it in one direction only and then checked
the wrong version explicitly: the slip $s=a_n+2\sqrt3$ would give $7.9282$ for $n=16$, which is
not the number the attack reports, so the attack is not making it.

Conversion, exact, in `S = span_Q{1,\sqrt3,\sqrt6,\sqrt{33}}` with dictionary equality:
$$s(16)\;\ge\;2(1+2\sqrt3)+2\sqrt3\;=\;2+6\sqrt3\;=\;12.392304845413264\ldots$$
`conversion exact match: True`.

```
checked:      the reduction re-derived from the problem README; the sep-1/sep-2 rescale;
              2*(1+2 sqrt3) + 2 sqrt3 == 2 + 6 sqrt3 as an exact identity, not numerically.
not-checked:  nothing.
verdict:      confirmed
```

---

## 3. (c) The 15-piece certificate, from first principles

[`check_v3.py`](../../../../experiments/packing-n16-verify-3/check_v3.py), run on my own
transcription of the vertex table at $a=1+2\sqrt3$:

| check | method | result |
|---|---|---|
| **C1** every listed vertex in the closed $T_a$ | exact sign tests $u\ge0$, $v\ge0$, $u+v\le a$ in $\mathbb{Q}(\sqrt3)$ | **pass** |
| **C2** each piece strictly convex, and no listed vertex redundant | exact convex hull (monotone chain) of the listed vertices; hull size must equal the listed count | **pass**, sizes $4,5,5,5,4,5,6,6,5,5,6,5,5,5,4$ — 3 quadrilaterals (the corners), 9 pentagons, 3 hexagons, exactly as claimed |
| **C3** squared diameter | exact max of $u^2+uv+v^2$ over all hull vertex pairs. A polygon lies in the convex hull of its vertices and a compact set has the diameter of its hull, so this max **is** the diameter | **exactly 1** for **every one** of the 15 pieces |
| **C4** all 105 pairs interior-disjoint | exact convex intersection (Sutherland–Hodgman over $\mathbb{Q}(\sqrt3)$), area must be exactly 0 | **pass**, no overlaps |
| **C5** $T_a\setminus\bigcup P_i=\varnothing$ | see below — **no area argument used** | **pass**, 0 uncovered parts |
| **C6** areas sum to area $T_a$ | exact | equal (chart $2\cdot\text{area}=13+4\sqrt3$, i.e. area $=\tfrac{\sqrt3}4(13+4\sqrt3)=8.62917$) — reported as a **cross-check only** |

Per-piece areas reproduce the attack's table exactly: three corners at **exactly $\tfrac12$**,
nine edge pieces in $[0.566987,0.616025]$, three interior pieces in $[0.584936,0.589102]$. The
side subdivision $1,\ \sqrt3-1,\ 1,\ \sqrt3-1,\ 1$ is visible directly in the certificate: the
vertices on $v=0$ are $u\in\{0,\,1,\,\sqrt3,\,1+\sqrt3,\,2\sqrt3,\,1+2\sqrt3\}$, whose successive
differences are exactly those five numbers, summing to $1+2\sqrt3$.

**C5, the check that actually matters.** Depth-first exact residue search. Each stack item is a
closed convex polygon $Q$ paired with an index $j$, maintaining the invariant
$Q\setminus\bigcup_i P_i \;=\; Q\setminus\bigcup_{i\ge j}P_i$ (pieces below $j$ provably meet $Q$
in zero area). $Q$ is split by the **first** piece it actually touches, using
$\complement\operatorname{int}P=\bigcup_{e\in\partial P}\{\text{closed outer half-plane of }e\}$,
valid because $P$ is convex. Zero-area parts are dropped, and **that is sound, not slack**:
$\bigcup P_i$ is closed, so $T_a\setminus\bigcup P_i$ is relatively open in $T_a$, and a non-empty
relatively open subset of a triangle has positive area. Result: 4 434 nodes, peak stack 17, no
uncovered part, ~20 s. This uses neither the area identity nor disjointness, so it is immune to
the overlap-plus-hole failure mode, which §6 then demonstrates on a corrupted input.

**The load-bearing negative result.** All 15 diameters are **exactly 1**, not $<1$. Since this
problem's separation is non-strict, a closed piece of diameter exactly 1 may legally hold two
separated points. **So the certificate at $a=1+2\sqrt3$, on its own, proves nothing at all.** The
attack file says this itself, in bold, and it is correct to. The bound comes entirely from §4.

**Independent confirmation of the rational fallback.** My checker also passes
`experiments/packing-n16-covering-2/cert_rational.json` — 15 pieces, all rational, C1–C6 all pass,
max squared diameter $\tfrac{199282032302597545822661932801}{199282032302598438642984960000}
=0.999999999999996 < 1$ **strictly**. With strict diameters the pigeonhole applies directly at
that $a$, with no limiting argument whatsoever, giving
$$a_{16}\;\ge\;\frac{446410161513599}{10^{14}}\;=\;4.46410161513599,\qquad
s(16)\;\ge\;12.3923048454\ldots$$
This is the number a reader uncomfortable with the equality case should quote, and it is now
confirmed in two independently written checkers. It is $1.7\times10^{-14}$ below $1+2\sqrt3$.

```
checked:      15 pieces; containment in T_a; strict convexity with no redundant vertex; exact
              squared diameters (all exactly 1); all 105 interior-disjointness pairs; complete
              coverage of T_a by exact residue search with no area shortcut and no disjointness
              assumption; area identity as a cross-check; the side subdivision; per-piece areas;
              and the same battery on cert_rational.json, which passes with STRICT diameters.
not-checked:  the attack's claim that four vertices are rattlers with max-min slack 0.137 (a
              statement about the certificate's provenance, load-bearing for nothing);
              its "peak residue 9 parts" (my algorithm differs, so the number is not comparable).
verdict:      confirmed
```

---

## 4. (d) The dilation argument — audited, and stress-tested on the D1 witness

Reconstructed independently (docstring of
[`dilation_check.py`](../../../../experiments/packing-n16-verify-3/dilation_check.py)); $A:=1+2\sqrt3$.

**Step 1 (certificate).** 15 closed convex $P_0,\dots,P_{14}$ with $\bigcup P_i=T_A$ and
$\operatorname{diam}P_i=1$ each. — §3, PASS.

**Step 2 (dilation).** Fix $0<a<A$ and put $\mu=a/A\in(0,1)$. The map $h(x)=\mu x$ is a
similarity of ratio $\mu$ fixing the chart origin, and
$h(T_A)=\{(u,v):u,v\ge0,\ u+v\le\mu A\}=T_a$ — **exactly**, not approximately. So $h(P_0),\dots,
h(P_{14})$ are 15 closed convex sets whose union is $T_a$, with
$\operatorname{diam}h(P_i)=\mu\cdot1=\mu<1$.

**Step 3 (pigeonhole).** If $X\subset T_a$ were separated with $|X|=16$, then since 15 sets cover
$T_a$, two distinct points of $X$ share some $h(P_i)$ and are at distance
$\le\operatorname{diam}h(P_i)=\mu<1$. Separation only demands $\ge1$, so this is a contradiction.
Hence **no** separated 16-set exists in $T_a$, **for every** $a<A$.

**Step 4 (conclusion).** $a_{16}=\inf\{a:T_a\text{ has 16 separated points}\}$ and every $a<A$ is
excluded, so $a_{16}\ge A$. No compactness is needed for this direction; the infimum formulation
gives it directly.

**Is it airtight?** Yes. The three places this kind of argument usually leaks are all closed here.
(i) *Does the limit hold uniformly?* — there is no limit: a single explicit covering is exhibited
for each individual $a<A$, and the conclusion is a statement about each $a$ separately. (ii) *Is
$\operatorname{diam}(\mu P)=\mu\operatorname{diam}(P)$?* — yes, $h$ is a similarity, and this is
where the strict inequality $\mu<1$ is manufactured out of a piece of diameter exactly 1. (iii)
*Is equality at $a=A$ smuggled in?* — no: step 3 fails at $\mu=1$ and the conclusion allows
$a_{16}=A$. The write-up in `../n16-covering-2/` states exactly this and does not overreach.

**The discriminating test.** The naive lemma "$T_a$ covered by $k$ sets of diameter $\le1$
$\Rightarrow$ no $k+1$ separated points" is **false**, and `../n16-verification/` D1 is the
witness. I rebuilt that witness from scratch rather than reading it: $T_{\sqrt3}$, cut by its
centroid $(\tfrac{\sqrt3}3,\tfrac{\sqrt3}3)$ and its three edge midpoints into three
quadrilaterals. Run through **my own** checker: covered, pairwise interior-disjoint, and squared
diameter **exactly 1** for all three. And the four points $(0,0),(\sqrt3,0),(0,\sqrt3)$ and the
centroid have exact squared distances $3,3,1,3,1,1$ — all $\ge1$, so $T_{\sqrt3}$ holds **four**
separated points under three diameter-1 cells. The naive lemma dies.

Now run the §4 argument on that same witness: for every $a<\sqrt3$, $T_a$ is covered by three sets
of diameter $a/\sqrt3<1$, so $T_a$ has no 4 separated points, so $a_4\ge\sqrt3$. And the `cited`
value is $a_4=(s(4)-2\sqrt3)/2=(4\sqrt3-2\sqrt3)/2=\sqrt3$ exactly. **The dilation argument
returns the sharp value on the configuration that kills the naive one, and does not overshoot to
the false $a_4>\sqrt3$.** This is the check the attack file asks a reviewer to repeat first; it is
the right check, and it passes.

```
checked:      every step of the dilation argument, reconstructed and written out; that h(T_A)=T_a
              exactly; that strictness is manufactured legitimately by the similarity ratio; that
              the conclusion permits equality; and the D1 discriminating test rebuilt from
              scratch and run through my own checker and my own exact distance computation.
not-checked:  nothing load-bearing.
verdict:      confirmed
```

---

## 5. (e) Trying to break it

`RULES.md` §5 point 4. The claim is false iff some $a<A$ admits 16 separated points; equivalently,
writing $m$ for the largest achievable minimum pairwise distance among 16 points in the **unit**
triangle, $a_{16}=1/m$, so a break needs $m>1/A=0.2240092377$.

[`break_attempt.py`](../../../../experiments/packing-n16-verify-3/break_attempt.py): 120 random
multistarts (Dirichlet-seeded), each polished by a sequential-LP minimax solver of my own with a
shrinking trust region and exact re-projection into the triangle. Seed 20260822.

| | |
|---|---|
| best minimum separation found | $m=0.2162272693$ |
| implied $a_{16}\le 1/m$ | $4.6247635795$ |
| what a break would need | $m>0.2240092377$, i.e. $a<4.4641016151$ |
| Melissen–Schuur best known ($s=12.713629$) | $a=4.6247636924$ |

**No counterexample.** Every local optimum landed at or above $a=4.6247$ — a full $0.16$ above
the bound under audit; nothing came within reach of $4.4641$. As a by-product the search
independently reproduced the Melissen–Schuur best-known packing to $1.1\times10^{-7}$, which the
problem `RULES.md` §4 calls a good outcome in itself (validated pipeline). I also looked for a
structural break — a way the covering could be legal while the pigeonhole is not — and the only
candidate is the diameter-exactly-1 equality case, which §4 shows is handled.

```
checked:      120 independent multistart minimax optimisations, my own solver, seed pinned;
              no 16-point configuration anywhere near a < 1+2 sqrt3.
not-checked:  this is FLOATING POINT and it decides nothing. A failed break is not evidence for
              the bound (problem RULES.md §5); it discharges the §5.4 obligation and no more.
verdict:      no break found
```

---

## 6. The checker was attacked before it was believed

[`selftest_v3.py`](../../../../experiments/packing-n16-verify-3/selftest_v3.py) — one control plus
ten corruptions; every corruption must be rejected.

| # | corruption | rejected by |
|---|---|---|
| 0 | *(control)* unmodified certificate | — accepted, as it must be |
| 1 | piece 6 dilated $\times1.001$ about its centroid | C3, squared diameter $>1$ |
| 2 | **interior piece translated by $(1/100,0)$: an overlap and a hole of exactly equal area** | **C5 (coverage), 58 uncovered parts — while C6 (the area identity) still passes** |
| 3 | one vertex moved $10^{-6}$ outside $T_a$ | C1 (and C3) |
| 4 | piece 7 deleted (14 pieces) | C5 |
| 5 | piece 10 shrunk $\times0.999$: a genuine sliver hole | C5 (and C6) |
| 6 | a collinear extra vertex listed on piece 0 | C2 (hull size $\ne$ listed count) |
| 7 | `"4.464101615137754"` in an exact scalar field | parser (`RULES.md` §2: decimal strings banned) |
| 8 | a decimal string inside a $\mathbb{Q}(\sqrt3)$ pair | parser |
| 9 | the honest $a=1+2\sqrt3$ certificate reported as *strictly* sub-diameter-1 | checker refuses: it reports `exactly 1`, never `strictly below 1` |
| 10 | the same 15 pieces claimed to cover a **larger** $T_a$ | C5 |

Corruption 2 is the one the brief asked for and the one that justifies the algorithm: it is a
translation, so the total area is preserved **exactly**, the area identity `C6` passes, and only
the residue search sees that part of $T_a$ is uncovered. Any checker that infers coverage from
"areas sum to $|T_a|$" accepts it.

---

## 7. Corrections

**One, and it is not in the bound.** The bound, its certificate and its limiting argument are all
confirmed. The correction is to an auxiliary `sketch` claim in `../n16-covering-2/`, §"Why this is
where the family stops", finding **1** ("The coarse structure is forced").

> **The case split over $n_2$ is not exhaustive: $n_2\in\{4,5\}$ is never treated, so "the layout
> is 3 corner + 9 edge + 3 interior" is not established.**

Reconstructing that argument: with $4<a<5$ and 15 sets of diameter $<1$ covering $T_a$, each side
meets $\ge5$ pieces, so $n_1+2n_2\ge15$, and with $n_1+n_2=15-n_{\rm int}$ this gives
$n_2\ge n_{\rm int}$ — all correct. Also correct: the middle $a-2=2.4641$ of each side needs
$\ge3$ one-side pieces, so $n_1\ge9$, hence $n_2\le6$; and $n_2=6$ forces $n_{\rm int}=0$, which
leaves the incentre — at distance $a/(2\sqrt3)=1.2886>1$ from every side, so unreachable by any
piece meeting a side — uncovered. So $n_2=6$ is genuinely excluded and $n_2\ge3$ (each corner
needs a piece meeting both its sides). But the file then jumps from "$n_2=3$ gives $n_1\ge9$,
$n_{\rm int}\le3$" straight to "so the layout is 3 corner + 9 edge + 3 interior". **$n_2=4$ and
$n_2=5$ are consistent with every inequality derived** ($n_2=4$: $n_1\ge9$, $n_{\rm int}\le2$;
$n_2=5$: $n_1\ge9$, $n_{\rm int}\le1$) and are not ruled out anywhere in the file.

Consequences, stated precisely so this is not read more broadly than it is:

- **The bound $a_{16}\ge1+2\sqrt3$ is unaffected.** It rests on the certificate plus §4 and on
  nothing in that section.
- The Euler/trivalence count that follows ("caps the interior vertices at $I=16$ and fixes
  $\sum_f\deg f=75$") is conditional on the 3+9+3 layout and inherits the gap.
- Finding 1 is labelled `sketch` by its author, so nothing downstream is entitled to assume it.
  This is a gap in an unassumable claim, not a broken dependency. But anyone building an
  exhaustion argument on "the structure is forced" must close $n_2\in\{4,5\}$ first.

**One near-miss, recorded because it looked like a disagreement and was not.** My checker first
reported `cert_rational.json` as FAIL with $a\approx6.2\times10^{14}$. Cause: its JSON writes
`"a": ["446410161513599", "100000000000000"]`, meaning numerator/denominator, while my own
convention for a two-element exact scalar is $p+q\sqrt3$. Both readings are defensible and the
repo pins **neither** — problem `RULES.md` §2 fixes the interval encoding and the meaning of
`side_length`, but there is no schema at all for *covering* certificates. That is a real hole in
§2 for a class of certificate the repo is now producing routinely, and it is exactly the kind of
silent mutual misreading §2 exists to prevent. Not a defect in the attack; a suggestion for §2.

---

## 8. What this pass is worth

- **`sketch`, unchanged.** Four Claude Opus 5 checkers now agree. Under `RULES.md` §5 that is
  worth error-finding, not certification, because the failure modes are correlated. **A Codex
  examiner writing a fifth independent checker is still the only route to `verified:review`.**
- What is genuinely new here: the coverage of $T_a$ is now confirmed by a **second, structurally
  different** algorithm (depth-first residue with an index invariant, versus the predecessor's
  breadth-first residue list), the dilation argument has been written out step by step and
  stress-tested against the one witness known to break its naive cousin, and a documented attempt
  to refute the bound failed while independently reproducing the best-known packing.
- **Novelty of the underlying idea remains unverified** — scholarly hosts are blocked here, and
  `../n16-covering-2/` is right to say "assume this is known".

---

## 9. Second task: the three concurrent constructor lanes

Polled at the end of this session (they run on a different model, which is the point —
`RULES.md` §8):

| lane | attack dir | experiment dir | state when polled |
|---|---|---|---|
| M1 mixed capacity | `../n16-mixed-capacity/` | `experiments/packing-n16-mixed/` | **empty** — nothing to verify |
| O2 occupancy | `../n16-occupancy/` | `experiments/packing-n16-occupancy/` | `KILL-CRITERION.md` and `occ.py` present; `out/` holds **control runs only** ($n=4,6,7,10$), no $n=16$ certificate, no attack README |
| C5 covering-max | `../n16-covering-max/` | `experiments/packing-n16-covermax/` | **empty** — nothing to verify |

**No constructor certificate had landed, so none is verified here.** O2's controls being on the
known small cases is the right order of work (problem `RULES.md` §6.1, `RULES.md` §6 "validate on
a tiny instance first"), but a control run is not a claim and I have not checked them. Whoever
verifies those lanes must write their own checker again; `check_v3.py` in this directory is
reusable for any *covering* certificate in the $T_a$ chart and rejects the ten corruptions in §6,
but it is Claude-authored and so cannot promote anything on its own.

---

## Reproduce

```bash
cd experiments/packing-n16-verify-3
python3 check_v3.py                                   # exact Q(sqrt3) certificate at a = 1+2sqrt3   (~20 s)
python3 check_v3.py ../packing-n16-covering-2/cert_rational.json   # the strict rational certificate (a few minutes)
python3 table_check.py                                # reduction s(n)=2a_n+2sqrt3 and the a_n table  (instant)
python3 dilation_check.py                             # the dilation audit + the D1 sharpness test    (instant)
python3 selftest_v3.py                                # 1 control + 10 corruptions                    (~4 min)
python3 break_attempt.py 120 20260822                 # the failed refutation (floats; decides nothing)
```

Exact arithmetic and the Python standard library for every decision; seeds pinned; no network.
