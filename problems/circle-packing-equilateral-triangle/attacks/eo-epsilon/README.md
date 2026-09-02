# Attack: getting the Erdős–Oler deficit off $\varepsilon = 0$

**Claim type: lower bound (optimality direction).** No construction and no upper bound on
$s(n)$ appears anywhere in this file (problem [`../../RULES.md`](../../RULES.md) §1 asks for
that sentence first).

> **Explicit $\varepsilon$ proved: $0$.**
> **Non-explicit: $\varepsilon_7 > 0$** — Theorem E below gives $d(27) > a^\* =
> \frac{-3+\sqrt{217}}2$ *strictly*, with **no modulus**, for every $k$ at once. On the
> $\varepsilon$-scale of [`../eo-oler-equality/`](../eo-oler-equality/) §5 that is exactly the
> $0^+$ the brief classifies as insufficient, and I report it as such rather than as "the
> $\varepsilon$ I got" ([`KILL-CRITERION.md`](./KILL-CRITERION.md) K4).
>
> **The assigned route is dead at step 1, and provably so** (Proposition V): *no* quantitative
> Lemma T, however sharp, can produce $\varepsilon > 0$, because T2 is an identity and the
> sharpest admissible face bound returns the target verbatim.

- Kill-criteria, written before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md)
- Code: [`experiments/packing-eo-epsilon/verify.py`](../../../../experiments/packing-eo-epsilon/) —
  stdlib only, every decision exact over $\mathbb Q$ or $\mathbb Z$; floats appear only in
  printed columns, never in an `assert`
- Transcript: [`out/report.txt`](../../../../experiments/packing-eo-epsilon/out/report.txt)
- Journal: [`notebook/claude/2026-08-21-eo-epsilon.md`](../../../../notebook/claude/2026-08-21-eo-epsilon.md)
- Author: `claude` (Claude Opus 5 — convergent role, `RULES.md` §8: this is checking, exact
  calculation and one literature reduction), 2026-08-21

**Normalisation, asserted in code (§0 of the transcript).** Separation $1$; $E$ finite with
pairwise distances $\ge 1$; $n = |E|$; $E \subseteq T(a)$, the *closed* equilateral triangle of
side $a$; $P = \operatorname{conv}(E)$; $A,M$ area and perimeter; $b = |E \cap \partial P|$.
$$\Phi(K) := \tfrac2{\sqrt3}A(K)+\tfrac12 M(K),\quad
\operatorname{slack}(E) := \Phi(P)+1-n,\quad
\operatorname{def}(a,n) := \tfrac{a^2+3a+2}2-n = \Phi(T(a))+1-n .$$
$\operatorname{def} = \operatorname{slack} + G$ with $G := \Phi(T(a))-\Phi(P)\ge0$; both
summands are $\ge0$. The repo's certificates use separation $2$ and side $d = 2a$; **nothing
here reads them**, and the conversion ($d=12$, $s = 12+2\sqrt3$ at $a=6$) is asserted in code
only so the number can be checked against the certificate convention.

## Status table

| What | Status |
|---|---|
| **Groemer 1960 $\equiv$ Oler 1961**, and Groemer's equality clause *is* the equality characterisation of Oler | `sketch` (§1; the reduction is mine, the two inputs are `cited`) — settles the open question of [`../eo-literature/`](../eo-literature/) §3 |
| **Theorem E** — $\operatorname{def}(a,n)=0 \Rightarrow a\in\mathbb Z_{\ge1}$, $E$ the full lattice triangle, $n$ triangular; hence $d(T(k)-1) > a^\*_k$ *strictly* for every $k\ge2$ | `sketch` (§2), **non-explicit** |
| **Theorem Q** — quantitative Lemma T, explicit, tight-vanishing at exactly the two equality shapes | `sketch` (§3), proved and adversarially scanned |
| **Proposition V** — step 1 of the programme is vacuous: no quantitative Lemma T yields $\varepsilon>0$ | `sketch` (§4) — this is the finding that matters |
| Lemma T (T1) and identity T2 of `../eo-oler-equality/` | re-derived here and exactly re-checked; still `sketch` (§5) |
| Oler's inequality; Groemer's Satz with its equality clause | `cited` — see the caveat in §1 |

## Kill-criterion outcomes, stated up front (`RULES.md` §6.3)

> **K1 (correctness of the imported base).** *Not met.* Lemma T and T2 re-derived from scratch
> and exactly re-checked; no violation, exactly the two predicted equality triples, all Euler
> counts correct. Step 3 of Lemma T — its author's own least-certain step — **I can follow and
> reproduce**; see §5.
>
> **K2 (my own bound).** *Not met.* Theorem Q survived 174 914 exactly-decided triangles
> including degenerate slivers, both equality shapes, and $S$ up to $87$. Two harness bugs of
> mine (test triples with a side $<1$; $k=1$ in the square-free scan) fired K2 spuriously on
> the first run and are recorded in §6 rather than quietly fixed.
>
> **K3 (the decisive scope test).** **MET — and it is the result.** Proposition V (§4) shows a
> per-face bound on $\tau$ can never beat the target, so the brief's step 1 cannot carry any
> $\varepsilon$. I did not re-scope; explicit $\varepsilon$ from the assigned route is $0$ and
> that is the first line of this file.
>
> **K4 (non-explicit is not explicit).** **MET.** Theorem E gives $\varepsilon_7>0$ with no
> modulus. Reported as non-explicit throughout.
>
> **K6 (duplication).** Credited, not reclaimed: the window $[a^\*,6)$
> (`../eo-boundary-counting/` §2), the refutation of face-excess nonnegativity
> (`../oler-slack-analysis/` §4, `../eo-boundary-counting/` §4), the Barrier Theorem
> (`../eo-hull-deficit/` §6), the $\varepsilon$-scale and Lemma T / T2 / T3 / T4
> (`../eo-oler-equality/`).

---

## 1. Groemer's inequality *is* Oler's — and it comes with the equality case

[`../eo-literature/`](../eo-literature/) §3 leaves this open: *"I did not read Groemer, Oler, or
the Zassenhaus paper this session and cannot settle this."* It is settled by two lines of
algebra, and the consequence is that this repo has been treating a `cited` equality theorem as a
missing one.

Groemer's Satz, as transcribed on [`../../README.md`](../../README.md) from **p. 285 of the GDZ
scan** (the statement page, which that file records as read): for $n$ unit circles packed in a
convex region of area $F$ and perimeter $U$,
$$n\sqrt{12}\;\le\;F-\varkappa U+\lambda,\qquad \varkappa=\tfrac{2-\sqrt3}2,\quad
\lambda=\sqrt{12}-\pi(\sqrt3-1),$$
with equality **iff** the region is the convex hull of the circles *and* the hull $H$ of the
centres decomposes into equilateral triangles of side $2$ whose vertices are all centres (or $H$
degenerates to a segment or a point).

**Apply it to the convex hull of the circles itself**, $K = H\oplus B_1$ — which is exactly
$\operatorname{conv}\bigl(\bigcup_i B_1(c_i)\bigr)$, so the first equality condition is
automatic. Steiner gives $F = A(H)+M(H)+\pi$ and $U = M(H)+2\pi$, and substituting:
$$F-\varkappa U+\lambda \;=\; A(H)+\tfrac{\sqrt3}2M(H)+\sqrt{12},$$
i.e. $n\le \frac{A(H)}{2\sqrt3}+\frac{M(H)}4+1$ at separation $2$, i.e., rescaling
$A\mapsto A/4$, $M\mapsto M/2$,
$$\boxed{\;n\;\le\;\tfrac2{\sqrt3}A(P)+\tfrac12M(P)+1\;}$$
which is **Oler's inequality verbatim**. Every $\pi$ cancels; the check is done symbolically
over the basis $\{1,\sqrt3,\pi,\pi\sqrt3\}$ with $\sqrt3\cdot\sqrt3=3$ in `verify.py` §4, and
the rescaling is re-checked exactly against $T(k)$ for $k\le7$.

Two consequences, and the second is why this section exists.

1. **The `sketch` table in [`../../README.md`](../../README.md) §"Groemer — co-credit rejected"
   is measuring the wrong thing**, exactly as `../eo-literature/` §3 guessed: it applies
   Groemer's inequality to the *containing triangle* while Oler's route goes through the hull of
   the centres. Applied to the same region the two inequalities coincide. This changes nothing
   about the co-credit rejection — Groemer still proves no statement about triangles and settles
   no particular $n$ — but the slack column is not a property of Groemer's inequality. *(I am
   recording this here and not editing `../../README.md`; that file is not mine to change under
   this brief.)*
2. **The equality characterisation of Oler is `cited`, not missing.**
   [`../oler-lower-bound/`](../oler-lower-bound/) §5.2 lists it as the missing rigidity (R2),
   and [`../eo-oler-equality/`](../eo-oler-equality/) spends a whole attack proving special
   cases of it (T2.1, T4). Groemer's clause gives the general statement outright, and it is
   exactly the class that `../eo-oler-equality/` §3 (T3) identifies independently:

   > **Equality in Oler $\iff$ $\operatorname{conv}(E)$ is tiled by unit equilateral triangles
   > all of whose vertices lie in $E$** (or $E$ is degenerate).

   T3 proved the *converse* direction from Pick's theorem; Groemer supplies the hard direction.

**Caveat, stated at the strength the evidence supports (`RULES.md` §3, K5).** This repo has read
p. 285 and p. 294 of Groemer's scan and **not** pp. 286–293, i.e. not the proof. The equality
clause is therefore `cited` at the same strength as the inequality itself — an author's
statement in a published paper, quoted from the primary source, whose proof nobody here has
checked. My reduction above is `sketch`: the algebra is verified exactly, but it is my algebra.

---

## 2. Theorem E — Oler's bound is attained only at integer side and triangular $n$

> **Theorem E.** Let $E$ be a set of $n\ge1$ points with pairwise distances $\ge1$ in the closed
> equilateral triangle $T(a)$, $a>0$. If $\operatorname{def}(a,n) = \frac{a^2+3a+2}2-n = 0$, then
> $$a\in\mathbb Z_{\ge1},\qquad E=\Lambda\cap T(a)\ \text{for a unit triangular lattice }\Lambda,
> \qquad n=\tfrac{(a+1)(a+2)}2 .$$
> **Corollary E1.** For every $n$ that is not a triangular number, $d(n) > a^\*_n$ *strictly*,
> where $a^\*_n$ is the positive root of $\frac{a^2+3a+2}2=n$. Equivalently
> $\varepsilon_n := \operatorname{def}(d(n),n) > 0$.
> **Corollary E2.** For every $k\ge2$, $\varepsilon_k > 0$ at $n=T(k)-1$; in particular
> $\varepsilon_7>0$, i.e. $d(27) > \frac{-3+\sqrt{217}}2 = 5.865459931\ldots$

*Proof of E.* $\operatorname{def} = G+\operatorname{slack}$ with $G=\Phi(T)-\Phi(P)\ge0$ (area
and perimeter are monotone under inclusion of convex bodies) and $\operatorname{slack}\ge0$
(Oler). So $\operatorname{def}=0$ forces both to vanish.

$G=0$ forces $A(P)=A(T)$. If $P\subsetneq T$ were closed and convex, pick $q\in T\setminus P$; a
small ball around $q$ misses the closed set $P$ and meets $\operatorname{int}T$ in a non-empty
open set, so $A(T\setminus P)>0$. Hence $P=T(a)$ — in particular $P$ is non-degenerate, which
already discharges Groemer's degenerate alternative (a segment or a point has $A=0$, hence
$G>0$).

$\operatorname{slack}=0$ is then equality in Oler, so by §1 the triangle $T(a)$ is tiled by unit
equilateral triangles with all vertices in $E$. Each side of $T(a)$ is a union of unit edges of
that tiling, so $a$ is a positive integer, $E$ is the full lattice triangle, and
$n=\frac{(a+1)(a+2)}2$ (which is consistently equal to $\operatorname{Oler}(a)$). $\square$

*Proof of E1.* $d(n)$ is attained: $T(a)$ decreases to $T(d)$ as $a\downarrow d$ (with the
triangles nested, $T(a)=\frac a{a'}T(a')$), the configuration space is compact, and "pairwise
distance $\ge1$" is closed, so a limit of $n$-point configurations is an $n$-point
configuration. If $d(n)=a^\*_n$ the minimiser has $\operatorname{def}=0$, and Theorem E makes
$n$ triangular. $\square$

*Proof of E2.* $n=T(k)-1$ gives $a^\*_k = \frac{-3+\sqrt{4k^2+4k-7}}2$, and $4k^2+4k-7$ is never
a perfect square for $k\ge2$: $(2a+3)^2=(2k+1)^2-8$ forces $(k-a-1)(k+a+2)=2$, whose only integer
solution is $k=1,a=-1$. So $a^\*_k\notin\mathbb Z$, $n$ is not triangular, and E1 applies.
(Exhaustively re-checked for $2\le k\le200\,000$.) $\square$

| $k$ | $n=T(k)-1$ | $a^\*_k$ | window | $\varepsilon_k$ |
|---:|---:|---|---|---|
| 2 | 2 | $0.561552812809$ | $[a^\*,1)$ | $>0$ (E-O known) |
| 5 | 14 | $3.815072906367$ | $[a^\*,4)$ | $>0$ (E-O known) |
| 6 | 20 | $4.844288770225$ | $[a^\*,5)$ | $>0$ (E-O known) |
| **7** | **27** | $5.865459931328$ | $[a^\*,6)$ | $>0$, **open**; conjecture is $\varepsilon_7=1$ |
| 8 | 35 | $6.881527307120$ | $[a^\*,7)$ | $>0$, open |

**What this is and is not.** Every prior result in this repo sits at $d(27)\ge a^\*$; Theorem E
upgrades that to $d(27) > a^\*$, for every $k$ at once, from `cited` inputs. But **E1's last
step is a compactness argument by contradiction and extracts no modulus**: it says the minimum
is not at $a^\*$, not how far from $a^\*$ it is. Making it explicit needs a *quantitative*
stability version of Groemer/Oler ("$\operatorname{slack}(E)<\varepsilon$ $\Rightarrow$ $E$ is
within $\delta(\varepsilon)$ of a lattice-tiled configuration"), which I do not have and which
Groemer's statement page does not provide. The brief is right that this route delivers $0^+$;
what §1 adds is that the $0^+$ is *already available* and does not need an equality theorem to
be proved first.

---

## 3. Theorem Q — the quantitative Lemma T the brief asked for

Write $S=x+y+z$, $\alpha=y+z-x$, $\beta=z+x-y$, $\gamma=x+y-z$, $Q=\alpha\beta\gamma$, and
$m(S)=(S-2)^2(4-S)$. Heron gives $16A^2=SQ$, hence the closed form
$$\tau(x,y,z)\;=\;\tfrac2{\sqrt3}A+\tfrac S2-2\;=\;\sqrt{\tfrac{SQ}{12}}+\tfrac{S-4}2 .$$

> **Theorem Q.** Let $x,y,z\ge1$ be the sides of a (possibly degenerate) triangle.
> - If $S\ge4$: $\tau=\frac2{\sqrt3}A+\frac{S-4}2$ *exactly*, so $\tau\ge\frac{S-4}2$ and
>   $\tau\ge\sqrt{SQ/12}$.
> - If $3\le S\le4$:
>   $$\tau\;\ge\;\frac{SQ-3(4-S)^2}{12}\;=\;\frac{S\bigl(Q-m(S)\bigr)+(4-S)(S-3)(S^2-S+4)}{12}
>   \;\ge\;\frac S{12}\bigl(Q-m(S)\bigr)+\frac56(S-3)(4-S).$$
>
> Both summands are $\ge0$, and they vanish **simultaneously exactly** at $S=3$ (forcing
> $(1,1,1)$) and at $S=4,\ Q=0$ (forcing $(2,1,1)$) — the two equality shapes of Lemma T and no
> others.

*Proof.* Put $N=\frac{SQ}{12}-\frac{(4-S)^2}4$ and $D=\sqrt{\frac{SQ}{12}}+\frac{4-S}2$, so that
rationalising $\tau=\sqrt{SQ/12}-\frac{4-S}2$ gives $\tau=N/D$ (and $\tau=0=N$ in the single
case $D=0$, i.e. $S=4,Q=0$). $N\ge0$ *is* Lemma T. For fixed perimeter the area is maximal for
the equilateral triangle, so $\frac2{\sqrt3}A\le\frac{S^2}{18}$ and hence
$D\le\frac{S^2}{18}+\frac{4-S}2$, whose derivative $\frac S9-\frac12$ is negative on $[3,4]$, so
$D\le1$ at $S=3$. With $N\ge0$ and $0<D\le1$, $\tau=N/D\ge N$. The middle equality is the
polynomial identity $S\,m(S)-3(4-S)^2=(4-S)(S-3)(S^2-S+4)$ (both sides expand to
$(4-S)(S^3-4S^2+7S-12)$), the first summand is $\ge0$ because $Q\ge m(S)$ on the feasible
polytope (Lemma T Step 3), and the last inequality uses $S\ge3$ and $S^2-S+4\ge10$ on $[3,4]$.
$\square$

The *shape* reading, which is what a metric discharging argument would want: $Q-m(S)$ measures
departure from the isoceles family $(1,1,S-2)$, and $(S-3)(4-S)$ measures departure of the
perimeter from $\{3,4\}$. Along the segment $(1,1,t)$ joining the two equality shapes the bound
is exact to within a factor:

| $t$ | $\tau$ | fine bound | ratio |
|---|---|---|---|
| $1.1$ | $0.080400791855$ | $0.078825000$ | $0.980$ |
| $1.25$ | $0.188367386791$ | $0.176757812$ | $0.938$ |
| $1.5$ | $0.322821961869$ | $0.265625000$ | $0.823$ |
| $1.75$ | $0.364139870078$ | $0.223632812$ | $0.614$ |
| $1.9$ | $0.292527371169$ | $0.114825000$ | $0.393$ |

**Break-testing (K2).** Decided exactly ($\tau\ge B\iff \frac{SQ}{12}\ge(B+\frac{4-S}2)^2$ when
the right side is non-negative), $0$ violations of either form over: a $\frac1{12}$-grid on
$[1,4]^3$ (7 761), the degenerate family $x=y+z$ (3 721), 142 347 random rationals with sides in
$[1,7]$ (seed 20260821), 6 058 fine perturbations at both equality shapes, all integer triples
with sides $\le29$ (13 427), and 1 600 near-degenerate slivers with long side up to $12$ and gap
down to $10^{-6}$.

---

## 4. Proposition V — why step 1 of the programme cannot carry any $\varepsilon$

This is the finding. **It is not a statement about my Theorem Q being too weak; it holds for the
sharpest possible face bound.**

> **Proposition V.** Let $\Psi$ be any function of a triangle's side lengths with
> $0\le\Psi(f)\le\tau(f)$ for every triangle with sides $\ge1$ — i.e. any correct quantitative
> Lemma T, *including $\Psi=\tau$ itself*. Then for every $E$ and every triangulation,
> identity T2 gives
> $$\operatorname{slack}(E)=\sum_f\tau(f)-\!\!\sum_{e\ \mathrm{int}}\!(\ell_e-1)\;\ge\;
> \sum_f\Psi(f)-\!\!\sum_{e\ \mathrm{int}}\!(\ell_e-1),$$
> and to conclude $\operatorname{slack}(E)\ge\varepsilon$ one must prove
> $$\sum_f\Psi(f)-\sum_{e\ \mathrm{int}}(\ell_e-1)\;\ge\;\varepsilon. \tag{$*$}$$
> The strongest instance of $(*)$, $\Psi=\tau$, **is literally the target statement**
> $\operatorname{slack}(E)\ge\varepsilon$, because T2 is an identity and not an inequality.

Three consequences.

- **(V1)** No quantitative Lemma T is a strengthening of anything: the inequality it produces is
  weaker than or equal to the very statement it is supposed to prove. Sharpening $\Psi$ towards
  $\tau$ moves $(*)$ towards the target and never past it. **Step 1 of the brief's programme is
  vacuous in isolation**, at any sharpness, for any $\varepsilon>0$.
- **(V2)** Therefore *all* the content must live in an independent upper bound on
  $\sum_{e\ \mathrm{int}}(\ell_e-1)$ (step 3), and any bound strong enough to close $(*)$ with
  $\Psi=\tau$ is equivalent to the target. The decomposition supplies no leverage: it is a
  change of variables, not an inequality.
- **(V3)** The natural local repair — distribute the interior-edge debt evenly over the two
  faces sharing each edge and ask for a per-face bound — is *exactly* the refuted face-excess
  hypothesis. Writing $j_f$ for the number of $\partial P$-edges of $f$, the exact
  redistribution is
  $$\operatorname{slack}(E)=\sum_f\sigma(f),\qquad
  \sigma(f)=\tfrac2{\sqrt3}A_f-\tfrac{1+j_f}2+\tfrac12\!\!\sum_{e\in f\cap\partial P}\!\!\ell_e,$$
  so for a face with all three edges interior $\sigma(f)=\frac2{\sqrt3}A_f-\frac12$, which is
  negative for every face of area $<\frac{\sqrt3}4$ — e.g. $\sigma=-0.157472629$ at the face
  $(1,1,\tfrac{19}{10})$. That reproduces `../oler-slack-analysis/` §4 and
  `../eo-boundary-counting/` §4 (**theirs, credited**) from the $\tau$ side, and shows the two
  refutations are the same refutation.

  ($\sigma(f)\ge-\frac12$ always, and $\sum_f\sigma(f)=0$ is verified exactly on every $T(k)$
  lattice, $k\le7$, in `verify.py` §6.)

**Where that leaves the brief's steps 2 and 3.** V does not kill them; it relocates them. Step 2
("force some face far from both equality shapes") is not *by itself* usable, because a face far
from both can sit next to interior edges long enough to pay for it — that is precisely the
$(\mathrm{FE},\mathrm{BE})\to(-7.5,+7.5)$ discontinuity that `../eo-oler-equality/` §6 measured.
A working argument must couple the two sums globally, i.e. must be a genuine stability theorem
for Oler, not a face-local estimate. Everything I tried inside the decomposition reduced to
bookkeeping: for each of $\operatorname{slack}$, the face excess, the boundary-edge excess and
$\sigma$, the "improvement" I derived turned out to be the same identity rearranged, which is
the structural reason the whole family sits at $\varepsilon=0$.

---

## 5. Verification of the imported `sketch`es (K1) — Lemma T and T2

Both are `sketch` and hence not assumable, including by their author (`RULES.md` §3). I
re-derived both before using them.

**Lemma T.** Re-derived from Heron in the $\tau=\sqrt{SQ/12}+\frac{S-4}2$ form, which makes the
whole statement a single rational comparison $SQ\ge3(4-S)^2$ when $S<4$ and trivial when
$S\ge4$. Exactly scanned: $0$ violations in 173 314 triangles, and the union of equality triples
over all scans is exactly $\{(1,1,1),(1,1,2)\}$.

**Step 3 — the author's own least-certain step — checks out, and I can reproduce it.** The claim
is $\min\{\alpha\beta\gamma\}=(S-2)^2(4-S)$ over
$\Delta_S=\{\alpha+\beta+\gamma=S,\ 4-S\le\alpha,\beta,\gamma\le S-2\}$ for $S\in[3,4]$.
(a) With $\gamma$ fixed, $\alpha\beta=\alpha(S-\gamma-\alpha)$ is a downward parabola, hence
concave, hence minimised on any interval at an endpoint — this is exact, not heuristic — so a
minimiser may be taken with $\alpha$ at a bound; repeating with $\beta$ puts at least two
coordinates at bounds, i.e. at a vertex. (b) Vertex enumeration is complete: both-upper
$(S-2,S-2)$ forces the third coordinate to $4-S$, feasible iff $S\ge3$; both-lower $(4-S,4-S)$
forces $3S-8$, feasible iff $S\le3$; one-of-each $(S-2,4-S)$ forces $S-2$ and is in the same
orbit as the first. So for $S\in(3,4]$ the vertices are exactly the permutations of
$(S-2,S-2,4-S)$, and $\Delta_3=\{(1,1,1)\}$. (c) In side coordinates that vertex is $(1,1,S-2)$.
Backed by an exact grid over $\Delta_S$ for 121 values of $S$: the grid minimum never fell below
$m(S)$.

**Identity T2.** Re-derived (Euler plus $3F=2|\mathcal E|-b$ gives $F=2n-b-2$ and
$|\mathcal E_{\mathrm{int}}|=3n-2b-3$; $\sum_fA_f=A(P)$ and $\sum_fp_f=M(P)+2L_{\mathrm{int}}$).
Both counts, the area sum and both sides of the identity verified on nine explicit
triangulations — $T(k)$ for $k=2\ldots7$, $T(7)$ minus its apex ($n=27$, $b=17$, slack $0$), the
lattice-convex hull with a $\sqrt3$ edge (slack $\frac{\sqrt3-1}2$, confirming
`../eo-oler-equality/` §3's correction to (R2)), and a generic non-lattice quadrilateral.
Coordinates are exact in $\mathbb Q\times\mathbb Q\sqrt3$, so $\frac2{\sqrt3}A_f$ is *rational*
and every area decision is exact; lengths use rigorous rational enclosures of width $10^{-24}$.

Verdict: **K1 not met.** Neither import is broken. Both remain `sketch` — my re-derivation is
also mine, and `RULES.md` §3 caps the whole file at `sketch` regardless.

---

## 6. What I refuted, what broke, and what I did not do

**Refuted here.** The brief's step 1 as a source of $\varepsilon$ (Proposition V). Also, three
things I tried and which all collapsed into the same identity, recorded so nobody repeats them:

1. *Bound $\operatorname{slack}$ below by $\frac12(M(P)-b)$.* **False** — three collinear points
   at spacing $1$ have $M=4$, $b=3$, slack $0$. And in general
   $\operatorname{slack}-\frac12(M-b)$ is precisely the (refuted) face excess.
2. *Use "each side of $T(a)$ carries at most $\lfloor a\rfloor+1$ points", hence $b\le15$, in
   the $P=T$ case.* Substituting gives $\operatorname{slack}=\frac{a^2+3a-52}2$, i.e. the
   deficit itself. Circular; it is a count-based boundary term, already dead per the brief.
3. *Peel a strip off $T(a)$ and combine the proven Erdős–Oler cases $k\le6$ with Oler on the
   strip.* At $a\to6^-$: top region of side $<5$ holds $\le19$ (from $d(20)=5$), strip
   $(6,5,h=\frac{\sqrt3}2)$ holds $\le13$ by Oler, total $\le32$ against a requirement of
   $\le26$. A thin strip that holds $\le6$ shrinks the top by only $O(\sqrt\delta)$. This is the
   $I+(m-1)$ partition loss again.

**My own errors, recorded (`RULES.md` §0).** The first run of `verify.py` reported eight failed
checks. All eight were bugs in *my test harness*, not in the mathematics: two adversarial scans
generated triples with a side $<1$, outside Lemma T's hypothesis, and the perfect-square scan
started at $k=1$, where $4k^2+4k-7=1$ genuinely is a square (with $a=-1<0$, which the proof
excludes). The `sqrt3`-edge witness I first wrote down was also the wrong configuration. Fixed
and re-run clean; the point of recording it is that a scan reporting a violation of a correct
lemma is evidence about the scan.

**Not done.** No quantitative stability version of Oler — that is what an explicit $\varepsilon$
needs and I do not have it. No lattice-forcing (`../eo-oler-equality/` §7 N1 remains
`numerical`). No covering/true-capacity work: two other workers hold that.

---

## 7. Honest accounting (`RULES.md` §7)

**The $\varepsilon$ I proved: explicit $0$; non-explicit $\varepsilon_7>0$.** I did not prove
Erdős–Oler at $k=7$ and nothing here should be read as progress towards $\varepsilon=1$ beyond
strictness at the single point $a^\*$.

**Which of steps 1–3 blocked, and why.** Step 1 — provably, and not for want of sharpness.
Proposition V shows the $\tau$-decomposition is a change of variables: any face-shape bound fed
through T2 returns an inequality weaker than or equal to the target. Step 2 is then unusable in
isolation (a far-from-extremal face can be paid for by long interior edges, per
`../eo-oler-equality/` §6), and step 3 as stated *is* the target. The route needs a global
stability theorem, which is a different and harder object than a quantitative Lemma T.

**My least-certain step**, in order:

1. **Groemer's equality clause as I use it (§1).** This repo has read the statement page, not
   the proof, and I am relying on a one-sentence equality condition transcribed from a scan. If
   that clause has a hypothesis the transcription dropped, Theorem E's central step fails. It is
   also the step where I most want a cross-examiner to re-read the scan rather than my summary.
2. **The Steiner substitution in §1.** The algebra is verified exactly, but if Groemer's $F,U$
   mean something other than the area and perimeter of the containing region — or if his circles
   are required to be interior rather than merely packed — the reduction changes.
3. **Theorem E's compactness step (E1).** Routine, but it is where "non-explicit" enters, and I
   want it stated as an existence argument and never as a bound.

**Nothing here may be built on.** Every statement in this file is `sketch` (`RULES.md` §3),
including my re-derivations of other people's `sketch`es, and the file is capped there however
elementary the individual steps look. Nothing enters `results/`.

### Reusable outputs

- **Groemer $\equiv$ Oler, with the equality case `cited`** (§1) — retires the "missing equality
  characterisation" of `../oler-lower-bound/` §5.2 and answers `../eo-literature/` §3.
- **Theorem E** (§2) — $\operatorname{def}=0$ only at integer side and triangular $n$; strict
  positivity of $\varepsilon_k$ for every $k\ge2$, non-explicit.
- **Theorem Q** (§3) — the explicit quantitative Lemma T, with its exact decision procedure.
  Correct and reusable; by Proposition V, not by itself useful for $\varepsilon$.
- **Proposition V** (§4) — the no-go that should stop the next worker from re-running step 1.
