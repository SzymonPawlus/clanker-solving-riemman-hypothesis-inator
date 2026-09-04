# Attack: the area budget with the per-side counts pinned to 3/9/3

**Claim type: NEITHER of the two in problem [`../../RULES.md`](../../RULES.md) §1.** Nothing here
bounds $s(16)$ or $a_{16}$, in either direction. What is bounded is the auxiliary quantity

$$A_{15}\ :=\ \sup\{\,a>0\ :\ T_a\ \text{is covered by 15 sets of diameter}<1\,\},$$

the resource the covering route consumes. **An upper bound on $A_{15}$ bounds the *method*, not
the packing**: it says how far a 15-piece covering argument could ever reach, and a *smaller*
number is *worse news for the covering route*, not better news about $s(16)$. Nothing enters
`results/`.

- Author: `claude` (Claude Opus 5 — convergent role, repo [`RULES.md`](../../../../RULES.md) §8:
  this is exact calculation, where a creative step is just an error), 2026-08-23, worker **B2**
  (worker **B1** fixed the kill-criteria and wrote `exact.py`/`fupper.py`, then hit a session
  limit before producing a number; see "Inheritance" below)
- Issue [#97](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/97),
  branch `claude/circle-packing-subagents-9yg5gt`
- Kill-criteria, fixed before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md)
- Code: [`experiments/packing-n16-budget/`](../../../../experiments/packing-n16-budget/)
- Journal: [`notebook/claude/2026-08-23-n16-budget.md`](../../../../notebook/claude/2026-08-23-n16-budget.md)

---

## Verdict, up front

**The lead cashes. The pinned budget proves $A_{15}\le 4.785266$, against the published
$\mathrm{U2}=4.914308$ — a gain of $0.129042$ on the same certified $f$.** It is the first number
this campaign has moved rather than restated.

And it is `sketch`, not because the arithmetic is loose but because it rests on Theorem N.

| bound on $A_{15}$ | value | status |
|---|---:|---|
| **B — pinned $(3,3,3)$ budget, this lane** | $\mathbf{4.785266}$ | `sketch` (**capped by Theorem N**, see below) |
| U2′ — unpinned Lemma S, recomputed here at the same $f$ grid | $4.914308$ | reproduces the published U2 to 6 dp |
| U1 — corner-refined isodiametric | $5.039166$ | `sketch`, [`../n16-covering-limit/`](../n16-covering-limit/) |
| **X1′ — ceiling of the *pinned* lemma (new)** | $\mathbf{4.672750}$ | `sketch` |
| X1 — ceiling of the unpinned lemma | $4.836854$ | `sketch`, reproduced here to 6 dp |
| comparison target (16-point packing) — **never an input** | $4.6247637$ | `numerical` |
| certified 15-piece covering $\Rightarrow A_{15}\ge$ | $1+2\sqrt3=4.4641016$ | `sketch`, [`../n16-covering-2/`](../n16-covering-2/) |

So $4.4641016 \le A_{15} \le 4.785266$, and $4.6247637$ is still inside that interval: **the
covering route is not closed, and this lane cannot close it.** Even a *perfect* $f$ under the
pinned counts stops at $\mathrm{X1}' = 4.672750 > 4.6247637$. What used to be a $0.212$ margin of
unreachability is now $0.048$ — the route is much closer to being obstructed than the published
numbers showed, and is still not obstructed.

### Kill-criterion outcome, up front

- **B1 (the point of the lane): did NOT fire.** The pinned bound came out *below* U2, by $0.129$.
  The lane's own primary kill-criterion — "if the pinned bound does not beat U2, the lead is
  dead" — is the one that would have retired it; it did not trigger, so the lead is confirmed
  rather than retired.
- **B2 (the tripwire): held, and is asserted in code.** Every bound printed is $>1+2\sqrt3$;
  `budget.py` fails loudly otherwise. No bound approached the certified covering.
- **B3 (the pinned ceiling must not be crossed): held, and it is the criterion that matters
  here.** $\mathrm{B} = 4.785266 \ge \mathrm{X1}' = 4.672750$, asserted in code. **The briefing
  this worker was given said that landing below $\mathrm{X1}=4.836854$ means "something is
  wrong". That is not right, and B1 had already seen why**: X1 is the ceiling of Lemma S *as
  stated*, which knows only $k_e\ge3$ and must maximise over every admissible $(k_1,k_2,k_3)$.
  Pinning adds a hypothesis (Theorem N), so the pinned lemma is strictly stronger and its bound
  is *expected* to fall below X1. The ceiling that may not be crossed is the pinned one, X1′, and
  it was not. Crossing X1 is not an inconsistency; crossing X1′ would be.
- **B4 (circularity): held.** No $s(n)$, $d(n)$, $a_n$, no repo packing, no covering number is an
  input to any bound. The only imported mathematics is the isodiametric (Bieberbach) inequality.
  $4.6247637$ appears only in the comparison column.
- **B5 (status honesty): honoured.** See the status table below; B is `sketch`.
- **B6 (budget): held.** About 5 minutes of compute on one core; whole task inside 45 minutes.

### Inheritance from worker B1

Kept, deliberately: `KILL-CRITERION.md` (sound, and sharper than my briefing on the X1 point —
B3 above is B1's), `exact.py` (certified $\pi$/$\sqrt{\cdot}$/$\arcsin$, with Machin-vs-Euler and
$\sin$-inversion cross-checks) and `fupper.py` (the slab LP, independently re-derived from the
geometry, with the LP value re-obtained from an exactly verified rational dual). I read both in
full and re-ran their self-tests before using them; `fupper.py` is checked against the one value
of $f$ that is known exactly, $f(1)=\pi/3-\sqrt3/4$. Written by me: `flower.py` (certified lower
bounds on $f$), `budget.py` (Lemma S′, the comparison and the ceilings), `run.sh`, and the
per-point/non-uniform grid.

---

## 1. Status table — and the cap

| assertion | status | depends on |
|---|---|---|
| Lemma S′ (§2), the pinned budget inequality | **`sketch`** | Theorem N §3.1 (`sketch`), isodiametric (`cited`) |
| **B: $A_{15}\le 4.785266$** | **`sketch`** | Lemma S′; **capped by Theorem N** |
| X1′: no bound from Lemma S′ can go below $4.672750$ | `sketch` | Lemma S′ + explicit admissible sets |
| U2′ $=4.914308$, X1 $=4.836854$ (reproductions) | `sketch` | as [`../n16-covering-limit/`](../n16-covering-limit/) |
| the certified $f$ grid (upper) and $f_{\rm lo}$ (lower) | exact given the geometry | isodiametric (`cited`) |

**The cap, named explicitly (`RULES.md` §3).** B depends on the class structure of
[`../n16-structure/`](../n16-structure/) §3.1, whose status is `sketch` — its author's, unreviewed
by any other model family, **and not assumable even by its author**. A claim is capped at the
weakest status it depends on, so **B is `sketch`, however exact the arithmetic**, and nothing may
be built on it. To promote it, §3.1 must first be examined by Codex per `RULES.md` §5; that is the
single gate on this number. Note also that §3.1 sits under a **correction banner** in its own file
— its headline corollary was refuted — so a reviewer should read that banner before reading this.

---

## 2. Lemma S′ — the pinned budget

Separation $1$; $T_a$ closed equilateral of side $a$; a **piece** has diameter **strictly** $<1$.
Throughout $1+2\sqrt3 \le a$. Suppose $T_a = \bigcup_{i=1}^{15} S_i$. (Coverings using fewer
pieces are padded with empty sets, which changes nothing.)

1. **Class structure** — [`../n16-structure/`](../n16-structure/) §3.1, `sketch`: exactly $3$
   pieces meet two sides, $9$ meet exactly one, $3$ meet none, and **each side is met by exactly
   $3$ one-side pieces** (Theorem N forces $\lfloor a-4/\sqrt3\rfloor+1 = 3$ per side for
   $a\in[2+4/\sqrt3,\,3+4/\sqrt3)\supseteq[1+2\sqrt3,5)$, and $3\times3=9$ exhausts the class).
2. **The two-side pieces are the vertex pieces.** Each vertex lies in a piece, which meets the two
   sides through it; the three are distinct ($a>1$ apart); there are exactly three two-side pieces,
   so those are they. Each $P_V$ contains $V$ and has diameter $<1$, hence $P_V\subseteq B(V,1)$ and
   $\operatorname{area}(P_V\cap T_a)\le\operatorname{area}(B(V,1)\cap T_a)=\pi/6$ (the $60°$ unit
   sector, $a\ge2$).
3. **$k_e = 3$ exactly.** Let $m_e$ be the middle of side $e$ — its points at distance $>1$ from
   both endpoints, a segment of length $a-2$ — and $M_e=\{i: S_i\cap m_e\neq\emptyset\}$, $k_e=|M_e|$.
   A vertex piece lies within $1$ of its vertex, so it misses every $m_e$; a no-side piece misses
   $e$ entirely. Hence $M_e$ is contained in the three one-side pieces of $e$: $k_e\le3$. In the
   other direction the traces $S_i\cap e$, $i\in M_e$, cover $m_e$ and each has measure at most its
   diameter $\ell_i<1$, so $\sum_{i\in M_e}\ell_i\ge a-2$ and $k_e>a-2\ge2$. **Therefore $k_e=3$**,
   all nine one-side pieces are edge-penalised, and $a-2<3$: for $a\ge5$ no covering exists at all.
4. **Edge penalty.** For $i\in M_e$, $\overline{S_i\cap T_a}$ has diameter $\le1$, lies in the closed
   half-plane of $e$ and contains two points of that line at distance $\ell_i$, so
   $\operatorname{area}(S_i\cap T_a)\le f(\ell_i)$ with $f$ as in
   [`../n16-covering-limit/`](../n16-covering-limit/) §2(d). With $\hat f$ the concave envelope of
   $f$ on $[0,1]$ (and $\hat f$ non-increasing, since $f$ is), Jensen over the three traces gives
   $\sum_{i\in M_e} f(\ell_i)\le 3\hat f\!\big(\tfrac{1}{3}\sum\ell_i\big)\le3\hat f\!\big(\tfrac{a-2}{3}\big)$.
5. **The rest.** The three no-side pieces get the isodiametric bound $\pi/4$ each.

Subadditivity of outer measure over the fifteen traces:

> **Lemma S′.** For $1+2\sqrt3\le a$, if $T_a$ is covered by 15 sets of diameter $<1$ then
> $$\frac{\sqrt3}{4}a^2\ \le\ 3\cdot\frac{\pi}{6}\ +\ 9\,\hat f\!\left(\frac{a-2}{3}\right)\ +\ 3\cdot\frac{\pi}{4}.$$

Both sides are monotone in $a$ (area up, $\hat f$ non-increasing), so a single violation bounds
$A_{15}$ from above for every larger $a$ as well; `budget.py` checks the monotonicity of the
envelope rather than assuming it.

**Where the gain comes from.** Lemma S knows only $k_e\ge3$ and $\sum_e k_e\le12$, so it must
maximise its right-hand side over $(k_1,k_2,k_3)$ — and the maximiser is $(4,4,4)$, which pays
$12\hat f\big(\tfrac{a-2}{4}\big)$ at the *shorter* trace $\tfrac{a-2}{4}$ where $f$ is much
larger. Pinning deletes that branch: the operating point moves from $\ell=\tfrac{a-2}{4}\approx0.70$
to $\ell=\tfrac{a-2}{3}\approx0.93$, where the certified $\hat f$ has fallen from $\approx0.740$ to
$0.665$, and the piece count paying it from 12 to 9. That is the whole of the $0.129$.

## 3. $f$, from both sides — certified, and re-derived here

**Upper (`fupper.py`).** For convex compact $S$ in $\{y\ge0\}$ with $(0,0),(\ell,0)\in S$, slices
$S_y=[\alpha(y),\beta(y)]$ of width $w(y)$: $w(y)\le2\sqrt{1-y^2}-\ell$ and $w\le1$; the apex is
within $1$ of both marked points so $H\le\sqrt{1-\ell^2/4}$; and for two non-empty slices the two
*cross* distances give $w(y)+w(y')\le2\sqrt{1-(y-y')^2}$. Discretising $[0,H_{\max}]$ into
$N=128$ slabs, once per possible index $m$ of the slab containing $H$, turns this into an LP in
the slab suprema. **scipy only proposes the dual**; the proposal is rounded up, repaired to exact
dual feasibility and evaluated in `Fraction`s, so weak duality is the only thing relied on and a
bad LP solve can only weaken the certificate, never invalidate it. Checked against the one value
known exactly: $f(1)=\pi/3-\sqrt3/4=0.6141848\ldots$, which every certified upper bound exceeds.

**Lower (`flower.py`)** — needed for the ceiling. Two explicit admissible sets:
*the cut disk* $B\big((\tfrac\ell2,\tfrac{\sqrt{1-\ell^2}}2),\tfrac12\big)\cap\{y\ge0\}$, of area
$\tfrac\pi4-\tfrac{\arcsin\ell}{4}+\tfrac{\ell\sqrt{1-\ell^2}}{4}$; and *the lens*
$R=B(A,1)\cap B(B,1)\cap\{y\ge0\}$ at $\ell=1$, of area $\pi/3-\sqrt3/4$, which is admissible
because $R$ is convex and every boundary point is within $1$ of $C=(\tfrac12,\tfrac{\sqrt3}2)$ —
so $R$ lies in the Reuleaux triangle $ABC$ and has diameter $1$. Since $f$ is non-increasing
(convexify; the hull still contains $(\ell,0)$ for every smaller $\ell$), the lens bounds $f$ from
below at *every* $\ell\le1$. **At the pinned operating point $\ell\approx0.93$ the lens is the
binding lower bound and the cut disk is far off** — the reverse of the unpinned lane, where
$\ell\approx0.70$ and the cut disk wins. Missing this would have understated X1′ by $\approx0.03$.

At the operating point $\ell = 0.928422$: $0.6141848\ \le\ f(\ell)\ \le\ \hat f(\ell)\le 0.6653853$.
That window of $0.051$, times 9 pieces, is exactly the $\mathrm{B}-\mathrm{X1}' = 0.1125$ that a
sharper $f$ could still buy.

## 4. Does pinning move X1? Yes — down to X1′ $=4.672750$

Feeding the certified *lower* bound on $f$ into Lemma S′ exhibits a budget the pinned lemma can
never contradict, so no bound provable from it can be below the largest such $a$:

| | ceiling | still above $4.6247637$? |
|---|---:|:--:|
| X1 — unpinned Lemma S, exact $f$ | $4.836854$ | yes, by $0.212$ |
| **X1′ — pinned Lemma S′, exact $f$** | $\mathbf{4.672750}$ | **yes, by $0.048$** |

So pinning moves the ceiling by $0.164$, and the answer to "can this method close the covering
route?" is **still no** — but the margin is now small enough that the next ingredient (a genuine
joint/density bound, or a cap on the no-side pieces, which here still pay the full $\pi/4$) could
plausibly finish it. That is the concrete follow-up this lane leaves behind.

## 5. What is delicate

1. **Step 3 of §2, $k_e\le3$.** This is *my* step, not Theorem N's and not Lemma S's, and the
   entire gain rests on it. It needs all three of: the two-side pieces being exactly the vertex
   pieces; a vertex piece missing $m_e$ (it lies in $B(V,1)$, and $m_e$ starts beyond distance 1);
   and each side having exactly three one-side pieces. If any of those fails, $k_e$ could be 4 and
   the deleted branch comes back.
2. **The two definitions of "edge middle" are different, and I use the shorter one.** Lemma S's
   $m_e$ (distance $>1$ from the endpoints, length $a-2$) is *not* Theorem N's $M_e$ (distance
   $>2/\sqrt3$, length $a-4/\sqrt3$). I take the count from Theorem N and the *length* from Lemma
   S. That is legitimate — the three one-side pieces of $e$ are the only candidates to meet the
   longer segment either — and it is the stronger choice ($a-2>a-4/\sqrt3$ forces a larger average
   trace, hence a smaller $f$). [`../n16-structure/`](../n16-structure/) §5.1 suggested
   $\ell=(a-4/\sqrt3)/3$; that would be valid but weaker.
3. **The concave envelope and its grid.** $\hat f$ is bounded above by the concave hull of a *step*
   majorant of the certified grid values (valid because $f$ is non-increasing). The step is the
   dominant loss: the grid is $1/48$ on $[0,3/4]$ and $1/192$ on $[3/4,1]$, and refining it further
   would lower B by a few units in the third decimal. **B is therefore not the infimum of the
   method** — X1′ is the infimum, and B is what 128 slabs and this grid certify.
4. **X1′ versus X1.** Explained under B3 above; this is the point on which the briefing was wrong
   and B1's kill-criterion was right.

## 6. What to review hardest

1. **§2 step 3** (see above) — the single load-bearing new step.
2. **The status cap.** B is `sketch` because §3.1 is `sketch`. If a reader carries $4.785266$
   forward as an established upper bound on $A_{15}$, that is exactly the laundering `RULES.md` §0
   and §3 exist to prevent. It also inherits §3.1's correction banner.
3. **The dual-certificate repair loop** in `fupper.py` — it is the only place where a float touches
   a quantity that becomes a theorem, and the argument that it is safe is weak duality plus an
   exact feasibility assertion. Break that and the whole $f$ grid falls.
4. **The lens lower bound's diameter argument** ($R\subseteq$ Reuleaux triangle). It is one
   paragraph, it decides X1′, and it is the kind of step this repo gets wrong.
5. **That U2′ and X1 reproduce the published U2 and X1 to six decimals** from independently written
   code. That is the strongest evidence here that the pipeline is right — and equally, if a
   reviewer finds the *other* lane wrong, this lane inherits the error.

## 7. Reproduce

```sh
sh experiments/packing-n16-budget/run.sh
```

About 5 minutes cold on one core (~10 s once `out/fgrid.json` is cached); no network, no seeds.
$\pi$ and $\sqrt3$ enter only as certified rational enclosures, rounded **against** the conclusion
— $\operatorname{area}(T_a)$ from below, the budget from above (and the reverse for the ceilings).
Every reported inequality is decided in exact rational arithmetic; numpy/scipy propose LP duals
and nothing else.
