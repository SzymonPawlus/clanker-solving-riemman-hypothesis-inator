# Attack: the fractional covering relaxation — weight < 16 beats 15 pieces

**Claim type: OPTIMALITY / LOWER BOUND** (problem [`../../RULES.md`](../../RULES.md) §1): this
file asserts $a_{16} \ge c$, hence $s(16) \ge 2c + 2\sqrt3$, for an explicit $c$. No packing is
claimed optimal; nothing enters `results/`.

- Worker `claude` F2 (Fable 5 — generative role per repo [`RULES.md`](../../../../RULES.md) §8),
  2026-08-22, issue #97, branch `claude/circle-packing-subagents-9yg5gt`
- Kill-criteria fixed before computing: [`KILL-CRITERION.md`](./KILL-CRITERION.md)
- Code: [`experiments/packing-n16-fractional/`](../../../../experiments/packing-n16-fractional/)
  — numpy/scipy for the *search* only; every decision that enters a certificate is integer or
  `Fraction` arithmetic
- Journal: [`notebook/claude/2026-08-22-n16-fractional.md`](../../../../notebook/claude/2026-08-22-n16-fractional.md)

## RESULT PLACEHOLDER

(filled in after runs)

## Kill-criterion outcome

(filled in after runs)

## Lemma F — the fractional pigeonhole, and where the extra unit comes from

Chart as fixed by the campaign: $e_1=(1,0)$, $e_2=(\frac12,\frac{\sqrt3}2)$, so
$|u e_1 + v e_2|^2 = Q(u,v) = u^2+uv+v^2$ is rational in $(u,v)$ and
$T_a = \{u \ge 0,\, v \ge 0,\, u+v \le a\}$. Separation is **non-strict** ($\ge 1$).

> **Lemma F.** Let $S_1,\dots,S_M$ be sets with $\operatorname{diam} S_i < 1$ **strictly**, and
> let $y_1,\dots,y_M \ge 0$ satisfy $\sum_{i\,:\,x \in S_i} y_i \ge 1$ for every $x \in T_a$
> (a *fractional cover* of $T_a$). Then every $C \subseteq T_a$ with pairwise distances $\ge 1$
> has $|C| \le \sum_i y_i$. In particular, if $\sum_i y_i < n$ for an integer $n$, then $T_a$
> contains no $n$ points at pairwise distance $\ge 1$, so $a_n \ge a$ — indeed $a_n > a$.

*Proof.* Two distinct points of $C$ are at distance $\ge 1 > \operatorname{diam} S_i$, so
$|S_i \cap C| \le 1$ for every $i$. Since $y_i \ge 0$,
$$\sum_i y_i \;\ge\; \sum_i y_i\,|S_i \cap C| \;=\; \sum_i \sum_{x \in C \cap S_i} y_i
\;=\; \sum_{x \in C}\; \sum_{i\,:\,x \in S_i} y_i \;\ge\; \sum_{x \in C} 1 \;=\; |C|,$$
where the middle equality is exchanging a finite double sum and the last inequality is the
covering condition at each $x \in C \subseteq T_a$. If $\sum_i y_i < n$ then $|C| \le
\lfloor \sum_i y_i \rfloor \le n-1$ because $|C|$ is an integer. $\square$

Three remarks, each load-bearing:

1. **The budget is $< n$, not $\le n-1$.** The manager's brief asked for total weight $\le 15$;
   the proof gives the strictly stronger threshold $< 16$, because $|C|$ is an integer. That is
   almost one full extra piece of budget relative to the integral method, *on top of* the
   fractional sharing. This widening of scope is exactly the move `FINDINGS.md` warns about, so
   it is listed under "what to review hardest" below and is exercised by the controls: above a
   known $a_n$ the pipeline must (and does) fail to find weight $< n$.
2. **Strict diameters.** Separation is non-strict, so a piece of diameter exactly 1 can hold two
   admissible points; every certified piece here has squared diameter $\le (63/64)^2$ exactly.
3. **No disjointness, no containment.** The $S_i$ may overlap and may stick out of $T_a$
   (replacing $S_i$ by $S_i \cap T_a$ changes nothing); only the trace on $T_a$ and the
   diameter matter. The integral method's 15 disjoint pieces are the special case
   $y_i \in \{0,1\}$.

**Dilation.** If every piece has $\operatorname{diam} \le D \le 1$ and the cover has weight
$< n$ on $T_a$, then for every $\mu < 1/D$ the similarity $x \mapsto \mu x$ gives a fractional
cover of $T_{\mu a}$ by sets of diameter $\le \mu D < 1$ with the same weight, so
$a_n \ge \mu a$ for all such $\mu$, hence $a_n \ge a/D$. (Same limit argument as
[`../n16-covering-2/`](../n16-covering-2/); the closed inequality survives the supremum.)

## The sandwich — why the method can neither overshoot nor undershoot the integral one

Let $\omega(a)$ = max number of pairwise-$\ge1$-separated points in $T_a$, $\tau_f(a)$ = the
infimum of $\sum y_i$ over fractional covers by diameter-$<1$ sets, and $\tau(a)$ = the least
number of diameter-$<1$ sets covering $T_a$. Then
$$\omega(a) \;\le\; \tau_f(a) \;\le\; \tau(a).$$
The left inequality is Lemma F applied to a maximum separated set. The right takes $y_i = 1$ on
an optimal integral cover. Consequences:

- *Soundness ceiling:* for $a \ge a_{16}$ a 16-point separated set exists, so
  $\tau_f(a) \ge 16$ and no certificate of weight $< 16$ can exist — the method cannot prove
  more than the truth. (This also means the method's theoretical reach is bounded only by
  $a_{16}$ itself; unlike the integral method there is no known structural ceiling below it.)
- *Never weaker than the integral method:* wherever 15 pieces cover, weight 15 $< 16$ is a
  fractional cover; every integral certificate is a fractional one.

## Where gain is possible — the bulk rates, checked

A tiling by regular hexagons of diameter 1 spends weight $1/(3\sqrt3/8) = 8/(3\sqrt3) =
1.53960\ldots$ per unit area. Kershner's optimal covering density for congruent disks is
$2\pi/\sqrt{27}$; diameter-1 disks have area $\pi/4$, so such a covering also spends
$(2\pi/\sqrt{27})/(\pi/4) = 8/\sqrt{27} = 8/(3\sqrt3)$ per unit area — **the same rate**, as the
brief said (arithmetic re-derived; both equal $1.539600717\ldots$).

One honest caveat on interpreting that agreement: Kershner's theorem (`cited` in spirit; not
re-checked here) bounds *1-fold* coverings by congruent disks. I know of no theorem that the
**fractional** rate in the bulk cannot beat $8/(3\sqrt3)$ — the uniform-measure dual below only
forces rate $\ge 4/\pi = 1.2732$. So "fractional gains nothing in the bulk" is a plausible
hypothesis, not a proved fact; what is certain is only that fractional can never do *worse*
than $8/(3\sqrt3)$ (tile with hexagons). The corners and edges — where the integral record's
pieces are provably lossy (corner pieces of area $\frac12$ against the $\pi/6$ sector cap) —
remain the concrete place where sharing weight across overlapping pieces can help, and the
piece family below is built to offer the LP exactly those shapes.

## The dual ceiling

By LP duality (stated here only as the trivial weak direction, which is all that is used):
any measure $\mu \ge 0$ on $T_a$ with $\mu(S) \le 1$ for every diameter-$<1$ set $S$ has
$\mu(T_a) \le \sum y_i$ for every fractional cover — same double-counting as Lemma F. The
uniform measure of density $4/\pi$ is feasible by the isodiametric inequality (`cited`: a set of
diameter $<1$ has area $\le \pi/4$), giving
$$\tau_f(a) \;\ge\; \frac{4}{\pi}\cdot\frac{\sqrt3}{4}a^2 \;=\; \frac{\sqrt3}{\pi}a^2 .$$
This reaches the fatal value 16 at $a = \sqrt{16\pi/\sqrt3} = 5.38709\ldots$ — far above the
region of interest, so **the uniform dual does not obstruct the lane anywhere near the
target**; at the best-known packing side $4.6247637$ it gives only $11.79$. (For comparison,
the atomic measure on a unit triangular lattice has rate $2/\sqrt3 = 1.1547 < 4/\pi$ — weaker.)
The only ceiling known below $5.387$ is the sandwich itself: $\tau_f \ge \omega \ge 16$ from
$a_{16}$ on. A useful negative for a future worker would be an explicit *non-uniform* feasible
measure of mass $\ge 16$ at some $a < 5.387$; none is produced here.

## Certification — how a continuum condition becomes a finite exact check

Everything lives on an integer grid of $1/64$ of the separation distance; $T$ has side $N$
units. The certificate is:

- **Pieces.** Convex polygons of two kinds. *Boxes*: $\{L_1 \le u \le U_1,\ L_2 \le v \le U_2,\
  L_3 \le u+v \le U_3\}$ with integer bounds and all three widths $\le 63$. *Polys*: convex
  polygons with rational vertices (corner/edge sectors — convex hulls of the lattice points
  within distance 63 of an apex inside a $60°$ wedge — and corner quads reaching past the
  lattice hull near the wedge bisector). A poly's region is *defined* as the intersection of
  the halfplanes derived from its vertex list, so region $=$ hull(vertices) by construction and
  its exact diameter is the max pairwise $Q$ over vertices.
- **Diameter cap, exact.** For a box, $Q$ is convex, so its max over the difference polytope
  $\{|\Delta u| \le w_1, |\Delta v| \le w_2, |\Delta u + \Delta v| \le w_3\}$ — a *superset* of
  the true difference body, hence a safe overestimate — is attained at a vertex; the code
  enumerates all line-pair intersections exactly. With all widths $= 63$ this gives exactly
  $63^2 = 3969$, i.e. diameter $63/64 < 1$. Every piece is checked $\le 3969$ both at
  generation and again at certification.
- **Coverage, exact and overlap-proof.** $T_N$ is partitioned into its $N^2$ unit lattice
  triangles. The constraint per cell counts only pieces containing the **entire** cell (all
  three vertices satisfy every halfplane — integer comparisons throughout). Cells partition
  $T_N$, so per-cell total weight $\ge 1$ implies the covering condition at every point of
  $T_N$. This is deliberately *not* an area identity — overlapping pieces plus an equal-area
  hole would pass an area test; they cannot pass this one.
- **Weights, exact.** The LP proposal is rounded **up** to multiples of $2^{-16}$; per-cell sums
  are integer arithmetic on numerators; the total is compared to $n \cdot 2^{16}$ exactly.
- **Bound.** With $Q_{\max}$ the exact max squared piece diameter (units²), the certificate
  proves $a_{16} \ge N/\sqrt{Q_{\max}}$ by the dilation remark; decimal values below are
  floor-truncated lower bounds computed by integer square root.

The price of cell granularity is that a piece only "counts" on cells it fully contains —
effectively an erosion of up to 1 unit for non-lattice-aligned edges. The controls quantify
this: it costs 1–2 units of $N$ ($\approx 0.02$–$0.03$ in the final bound).

**Circularity guard.** The only $n=16$-specific input is the named constant
`EXCLUDE_POINTS = 16` (the pigeonhole budget). No number derived from any 16-point packing is
an input; `4.6247637` and `4.62` appear only in the *tripwire* that refuses and flags
suspiciously strong output after the fact (repo `RULES.md` §7).

## CONTROLS PLACEHOLDER

## DELICATE PLACEHOLDER

## Reproduce

```bash
cd experiments/packing-n16-fractional
python3 fractional.py control          # K1: n=4, 6, 10 — must pass before anything else
python3 fractional.py sweep16 285 282 288
```
