# n=16 six-direction (dodecagonal-norm) tomography: certification attempt — killed by node growth

**Claim type: NEITHER of the two in [`../../RULES.md`](../../RULES.md) §1.** No bound on
$s(16)$ or $a_{16}$ is asserted, in either direction. Everything exact below bounds the
*auxiliary* relaxation values $M_6(n)$ only. Nothing enters `results/`.

- Author: `claude`, worker **T2** (Fable 5), 2026-08-23, issue
  [#97](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/97),
  branch `claude/circle-packing-subagents-9yg5gt`. Predecessor T1 died before writing anything;
  nothing here is inherited from it. I1's proposal ([`../n16-approaches/`](../n16-approaches/)
  §P1) was **re-derived, not inherited** — every formula and control below was rebuilt from the
  chart definition, and I1's one reused artifact (its 4.49 witness JSON) was checked with an
  independently written exact checker.
- Code: [`experiments/packing-n16-tomography/`](../../../../experiments/packing-n16-tomography/)
  (`tomography.py`; transcript `out/run.log`, per-run JSON in `out/`).
- Journal: [`notebook/claude/2026-08-23-n16-tomography.md`](../../../../notebook/claude/2026-08-23-n16-tomography.md)
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md), written before any computation.

## Kill-criterion outcome — up front

**K2 fired. The certification strategy is dead at this effort level; the relaxation itself
stays alive (K1 did not fire).** The pre-registered n=10 gate (branch-and-cut at $a=2.888$,
0.34% below the known transition $3t$, caps 600 s / 300 000 nodes) hit its time cap at
**269 741 nodes with only 15 of 45 pairs resolved** at maximum depth. Both pre-registered
extrapolations put $n=16$ at or beyond I1's $10^9$-node gate:

| fit | basis | predicted nodes at $n=16$ |
|---|---|---|
| per-$n$ (optimistic) | completed trees $n{=}4{:}\,3037$, $n{=}5{:}\,8821$ | $\approx 1.1\times10^9$ |
| per-pair | same data vs pair count $6\to10$ | $\approx 5\times10^{16}$ |

Measured throughput: ~450 exactly-certified nodes/s on 1 core, so $10^9$ nodes ≥ 26 days.
Per the criterion, caps were not raised and no $n=16$ run was attempted. **Nothing above
$1+2\sqrt3$ was certified.**

| assertion | status |
|---|---|
| six-projection identity and the $\cos15°$ loss bound (derivation below) | `sketch` — elementary, re-derived here |
| rational thresholds $r_f \le t/w_f$ (relaxation direction), verified in $\mathbb{Q}(\sqrt3)$ | exact computation, `numerical` evidence class |
| exact lattice witnesses: $M_6(3)\le s$, $M_6(6)\le 2s$, $M_6(10)\le 3s$, $M_6(15)\le 4s = 3.86372 < 4 = a_{15}$, $s=\tfrac{96593}{100000}$ | `numerical` — exact rational verification of explicit configs |
| $M_6(4)\le \tfrac{16731}{10000}$ (corners+centroid, below $a_4=\sqrt3$) | `numerical`, exact witness |
| re-verification of I1's $M_6(16)\le 449/100$ with an independent checker | `numerical`, exact |
| **ceiling tightened**: $M_6(16)\le \tfrac{4485}{1000}=4.485$, exact witness from this lane's own search (`out/witness_n16_4485_1000.json`; $4.485>1+2\sqrt3$ exactly since $(4.485-1)^2=12.145>12$, so K1 still does not fire) | `numerical`, exact witness |
| branch-and-cut with exact Farkas leaves certifies $M_6(4)>167/100$, $M_6(5)>48/25$ | `numerical` — every leaf carries an exact rational certificate, but single-authored, unreviewed |
| K2 gate measurements and the two extrapolations | `numerical`; the fits are 2-point — weakest step, see below |
| verdict "certification intractable by disjunctive B&C at this effort" | assessment, not a theorem |

Nothing here is assumable, including by me (repo `RULES.md` §3).

**Circularity guard.** No value of $a_{16}/d(16)/s(16)$ enters any computation; the code never
reads `experiments/circle-packing-search/out/`; a named comment in `tomography.py` restates the
guard. $4.6247637$ appears in this file only as a comparison target, twice, both labelled.

## The $\cos15°$ derivation, written out

Chart $e_1=(1,0)$, $e_2=(\tfrac12,\tfrac{\sqrt3}2)$; the point $(u,v)$ is $ue_1+ve_2$, and
$T_a=\{u\ge0,\,v\ge0,\,u+v\le a\}$. A difference $\Delta=(du,dv)$ has Cartesian image
$\Delta_c=(du+\tfrac{dv}2,\ \tfrac{\sqrt3}2 dv)$. Project onto the unit directions
$d_\theta=(\cos\theta,\sin\theta)$ at $\theta = 0°,30°,\dots,150°$ and expand:

| $\theta$ | $\langle \Delta_c, d_\theta\rangle$ | form |
|---|---|---|
| $90°$ | $\tfrac{\sqrt3}2\,dv$ | $w=\tfrac{\sqrt3}2$, $L=dv$ |
| $30°$ | $\tfrac{\sqrt3}2(du+\tfrac{dv}2)+\tfrac{\sqrt3}4 dv=\tfrac{\sqrt3}2(du+dv)$ | $w=\tfrac{\sqrt3}2$, $L=du+dv$ |
| $150°$ | $-\tfrac{\sqrt3}2(du+\tfrac{dv}2)+\tfrac{\sqrt3}4 dv=-\tfrac{\sqrt3}2\,du$ | $w=\tfrac{\sqrt3}2$, $L=du$ |
| $0°$ | $du+\tfrac{dv}2=\tfrac12(2du+dv)$ | $w=\tfrac12$, $L=2du+dv$ |
| $60°$ | $\tfrac12 du+\tfrac{dv}4+\tfrac{3dv}4=\tfrac12(du+2dv)$ | $w=\tfrac12$, $L=du+2dv$ |
| $120°$ | $-\tfrac12 du-\tfrac{dv}4+\tfrac{3dv}4=\tfrac12(dv-du)$ | $w=\tfrac12$, $L=dv-du$ |

So $\mathrm{dod}(\Delta):=\max_f w_f|L_f(\Delta)| = \max_\theta|\langle\Delta_c,d_\theta\rangle|$.
The twelve signed directions $\pm d_\theta$ are spaced $30°$ around the circle, so any nonzero
vector makes an angle $\le15°$ with the nearest one, giving

$$\cos15°\cdot|\Delta| \ \le\ \mathrm{dod}(\Delta)\ \le\ |\Delta|,\qquad
\cos^215°=\tfrac{1+\cos30°}2=\tfrac{2+\sqrt3}4 .$$

Hence a Euclidean packing (pairwise $\ge1$) satisfies pairwise $\mathrm{dod}\ge t:=\cos15°$,
and with $M_6(n)$ := least $a$ admitting $n$ points in $T_a$ at pairwise $\mathrm{dod}\ge t$:

$$t\cdot a_n\ \le\ M_6(n)\ \le\ a_n \qquad\text{(the sandwich; both sides used as tripwires).}$$

A certified lower bound on $M_6(16)$ is a lower bound on $a_{16}$; the pair constraints are
disjunctions of 12 half-planes, so certification is finite rational LP (Farkas) work.

**Rational thresholds.** For certification the true thresholds $t/w_f$ (which live in
$\mathbb{Q}(\sqrt2,\sqrt3)$, not $\mathbb{Q}(\sqrt3)$ — I1's "leaves in $\mathbb{Q}(\sqrt3)$"
was slightly off) are replaced by rational $r_{\text{normal}}=\tfrac{1115355}{1000000}\le
\tfrac{2t}{\sqrt3}$ and $r_{\text{side}}=\tfrac{1931851}{1000000}\le 2t$, proved exactly via
$3r^2-2\le\sqrt3$ resp. $r^2-2\le\sqrt3$ in `Fraction` arithmetic. Replacing a threshold by a
smaller one only *enlarges* the feasible set, so infeasibility of the rational-threshold problem
still implies $a_{16}>a$ — and the weakening is $<2\times10^{-6}$ relative. This makes every
certificate pure $\mathbb{Q}$, no field extension needed at all.

## New structural fact found on the way: the lattice compresses by exactly $\cos15°$

The unit triangular lattice's nearest steps $(1,0),(0,1),(1,1),(1,-1)$ are all *parallel to one
of the six directions*, so on them $\mathrm{dod}=|\cdot|$ exactly, and the whole $T_k$ lattice
scales down by $t$ while staying dod-feasible. With rational spacing
$s=\tfrac{96593}{100000}\ge t$ (proved exactly), this gives exact witnesses

$$M_6(15)\ \le\ 4s\ =\ 3.86372\ <\ 4\ =\ a_{15},$$

answering I1's flagged early check (*"does $M_6(15)<4$ hold?"*) **by construction, no search
needed** — the true value is pinned to $[4t,4s]=[3.863703,3.863720]$ by the sandwich. Same for
$n=3,6,10$; and corners+centroid ($n=4$) is also direction-aligned, pinning
$M_6(4)\in[\sqrt3 t,\,1.6731]$. So on lattice-like $n$ the relaxation pays the full $\cos15°$
factor, and the lane's hope always was exactly the gap between
$(1+2\sqrt3)/t=4.6216$ and the (comparison target only) conjectured $4.6247637$ — a 0.07%
window. I1's numeric transition $\approx4.483$ sits inside the corresponding sandwich
$[t\cdot4.6248,\,4.6248]=[4.467,\,4.6248]$ (comparison target only, second and last use).

**The corner defect of P4–P6 does *not* apply here** (the pre-registered twenty-minute check):
those relaxations replaced the container and lost the corners; this one keeps $T_a$ exactly and
relaxes only the metric. What kills it is different — see below.

## Controls (all passed, transcript in `out/run.log`)

1. **Threshold soundness**: $r_f\le t/w_f$ proved exactly in $\mathbb{Q}(\sqrt3)$.
2. **Hex-cheat rejection**: I1's $M_3(4)\le\tfrac32$ corner-cheat config fails the exact dod
   check (as it must — re-derived with my own checker).
3. **Independent re-verification** of I1's $M_6(16)\le449/100$ witness (my checker, its JSON).
4. **Two-sided branch-and-cut controls whose answers are NOT in the Euclidean table** — a
   pipeline that merely reproduced $a_4=\sqrt3$, $a_5=2$ would *fail* these (the control trap
   another lane fell into):
   - $n=4$: certifies INFEASIBLE at $a=\tfrac{167}{100}$ (3037 nodes, 2784 exact Farkas
     leaves) and returns FEASIBLE with an exact rational witness at $a=\tfrac{1674}{1000}$;
     target value $\sqrt3\cos15°=1.673033$, bracketed both sides.
   - $n=5$: INFEASIBLE at $a=\tfrac{48}{25}$ (8821 nodes), FEASIBLE at $a=\tfrac{1932}{1000}$;
     target $2\cos15°=1.931852$.
   Both certified brackets are consistent with (slightly weaker than) the a-priori sandwich, as
   they must be; either control would have caught a flipped sign, a wrong threshold direction,
   or an unsound Farkas check.

## The growth gate (the kill)

| $n$ | pairs | $a$ (rel. gap below transition) | result | nodes | exact leaves | time |
|---|---|---|---|---|---|---|
| 4 | 6 | $167/100$ (0.18%) | certified | 3 037 | 2 784 | 5.7 s |
| 5 | 10 | $48/25$ (0.61%) | certified | 8 821 | 8 086 | 16.8 s |
| 10 | 45 | $2888/1000$ (0.34%) | **TIME_CAP, not certified** | 269 741 | 247 254 | 600 s |
| 16 | 120 | $447/100$ target (0.29% below I1's numeric 4.483) | **not attempted — K2 fired** | — | — | — |

The gaps were chosen uniform (~0.2–0.6%) so the gate instances sit in the same near-threshold
regime as the $n=16$ target; $n=10$ and $n=15$ transitions are *known in closed form* ($3t$,
$4t$) by the lattice fact, so the gate needed no search and cannot have been placed too easy.
The $n=15$ gate and $n=12$ instance were rendered moot by the $n=10$ timeout (K2 is an ANY-fire
criterion; caps were not raised after seeing numbers, per the pre-registration).

**Why the tree explodes (mechanism, `sketch`).** Any two points with $|dv|\ge r_{\text{normal}}$
satisfy their pair constraint through the $dv$-form alone, *regardless of $u$* — so horizontal
"rows" at $v$-spacing $\ge 2t/\sqrt3\approx1.1154$ decouple completely, and the same holds in
the other two lattice directions by symmetry. Near-threshold feasible sets therefore contain
high-dimensional continua (whole rows slide freely), and a disjunctive LP refutation must carve
away polyhedral *volume*, not isolated points. The sort-symmetry rows kill the $16!$ relabeling
but not these continuous degeneracies. This is the honest post-mortem: the relaxation's metric
is too flat along its own six directions for naive branch-and-cut, even though its *value*
(numerically $\approx4.483$) still sits above the record.

## What is delicate / what to review hardest

1. **The Farkas box-absorption step** (`BranchAndCut._exact_farkas`). At a pruned leaf the float
   dual $y$ is clipped to $y\ge0$ and rationalized; with $z=A^\top y$, $\beta=b^\top y$ computed
   exactly, the leaf is accepted iff $\sum_k a\cdot\min(z_k,0)>\beta$. Soundness argument: every
   $x$ feasible for the node's rows satisfies $z^\top x\le\beta$ (nonneg combination) *and*
   $x\in[0,a]^{2n}$ (implied by the node's own containment rows, which are always present), so
   the inequality certifies emptiness without needing $z=0$ exactly. **Review this hardest** —
   it is the load-bearing exactness claim of the whole artifact.
2. **WLOG sort rows** $(u_i{+}v_i)\le(u_{i+1}{+}v_{i+1})$: sound because any configuration can
   be relabeled into sorted order and the constraints are label-symmetric. Second-hardest.
3. **Threshold direction**: $r_f\le t/w_f$ (not $\ge$) is what makes the rational problem a
   relaxation. One flipped inequality here would fabricate bounds; the two-sided controls are
   the guard.
4. **The 2-point extrapolation** is the weakest link of the kill *quantitatively* — but K2 also
   fired on the direct, measurement-only $n=10$ timeout, which needs no fit.
5. The FEASIBLE verdicts rationalize an LP point and re-check exactly; a failure there returns
   `FEASIBLE_FLOAT_ONLY` (never observed) rather than a false certificate.

## What would revive the lane

Not more nodes — structure. (a) Exploit the row-decoupling *positively*: condition on the
$v$-multiset pattern (an integer partition-like object) and certify each pattern by a 1-D
interval argument, turning volume into combinatorics; (b) tie the six directions' degeneracies
together with cuts valid across whole disjunction sets (disjunctive/split cuts with exact
rational rounding); (c) an SDP/SOS route is orthogonal (I1's P2, still solver-blocked). Any
revival keeps the exact ceiling $M_6(16)\le449/100$ and so profits at most $+0.026$ over the
record — budget accordingly.

## Reproduce

```
cd experiments/packing-n16-tomography && python3 tomography.py controls   # ~50 s
python3 tomography.py gate 10 2888/1000 300000 600                        # the kill, 600 s
python3 tomography.py search 16 4485/1000 12                              # the 4.485 ceiling witness
```

Deterministic (seeds fixed, `random`/`numpy` 20260823); scipy `linprog(method="highs")` floats
decide only *which* leaves to certify — every reported bound is re-derived in `Fraction`.
