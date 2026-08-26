# r5-eo7 — proposal AE: a certified finite lower-bound theorem at $k = 7$, and the one hypothesis it still needs

```
claim kinds:  a LOWER bound (optimality direction), restricted to line-structured
              configurations — plus one CONSTRUCTION (an exact 22-point witness).
status:       numerical  — the branch-and-bound certificates and every count below
              sketch     — the reduction (§2), Lemma A, facts F1–F4, and the
                           conditional theorem (§6)
              refuted    — the δ-robust form of the conditional theorem (§7)
author:       claude (worker r5-eo7), 2026-08-24
executes:     ../r4-approaches/README.md §1, proposal AE (ranked first)
code:         ../../../../experiments/packing-r5-eo7/
```

**Nothing in this file is assumable** (repo `RULES.md` §3). This does **not** prove
Erdős–Oler at $k = 7$ and must never be read as doing so (`RULES.md` §7). What it
produces is the finite object AE asked for, plus an honest account of the gap that
remains — including a **negative result about the gap that AE did not anticipate** and
that a follow-up must answer before spending another round here (§7).

---

## 0. One-paragraph summary

Erdős–Oler at $k = 7$ is the open statement that $27 = \Delta(7) - 1$ points at pairwise
distance $\ge 1$ do not fit in a closed equilateral triangle of side $a < 6$. This lane
proves, by certified interval branch-and-bound over an explicit **3-parameter** space,
that **at most 25 such points fit if the configuration lies on a family of equally
spaced parallel lines with spacing $\ge \sqrt3/2$** — which every unit-separation
lattice does. The target for $k=7$ is $\le 26$, so the certificate closes the
line-structured case with one point of slack. It is validated against the `cited` cases
$k = 4, 5, 6$ (all close) and $k = 3$ (**does not** close — §5.3). An exact
$\mathbb{Q}(\sqrt3)$ witness puts 22 lattice points in $T(5999/1000)$, so the truth for
the certified quantity lies in $[22, 25]$. The remaining gap to EO(7) is isolated as one
falsifiable hypothesis (§6). **§7 then measures that hypothesis's only usable form and
finds it fails**: the counting bound is *discontinuous* at zero perturbation — allowing
the configuration to be within $\delta = 10^{-9}$ of the lines instead of exactly on
them already pushes the bound from 24 to 27, past the target. So the conditional
theorem is real but requires **exact** collinearity, which no packing satisfies.

---

## 1. Pinning the statement — what exactly is being quantified over

AE says "$\max_\Lambda |\Lambda \cap T(a)| \le 26$ for $a < 6$, over unit-separation
lattices" and calls the parameter space 3-dimensional. Getting the quantifier right
matters more than the computation, so here it is explicitly.

**Conventions** (problem `RULES.md` §2, `../eo-exhaustion/` §0). $T(a)$ is the *closed*
equilateral triangle $A = (0,0)$, $B = (a,0)$, $C = (a/2, a\sqrt3/2)$. Separation is
$\ge 1$ (Oler normalisation); the repo's $d$-normalisation is $d = 2a$, so EO(7) is
$d(27) \ge 12$. All inequalities are non-strict except where marked.

**Definition (line-structured).** A finite $P \subset \mathbb R^2$ is *$h$-line-structured*
if there are a unit vector $u$, a real $h$, and $\tau \in \mathbb R$ with
$$P \;\subset\; \bigcup_{j \in \mathbb Z}\;\bigl\{\, x : \langle x, u^\perp\rangle = \tau + j h \,\bigr\}.$$

**Theorem L (certified; `numerical`).** *Let $a' < 6$ and let $P \subset T(a')$ have
pairwise distances $\ge 1$. If $P$ is $h$-line-structured for some $h \ge \sqrt3/2$,
then $|P| \le 25$.*

**Corollary L′ (the lattice case AE asked for; `numerical`).** *Let $\Lambda \subset
\mathbb R^2$ be a lattice whose shortest non-zero vector has length $\ge 1$, let
$t \in \mathbb R^2$, and let $a' < 6$. Then $|(\Lambda + t) \cap T(a')| \le 25$.*

Corollary L′ follows from Theorem L because a lattice is automatically line-structured
with an admissible spacing — §2.1. **Theorem L is strictly stronger than AE's target**:
it never uses that the point set is a lattice, only that it sits on equally spaced
lines. That matters for §6, because the forcing hypothesis one has to assume is
correspondingly weaker.

**The parameter space is 3-dimensional, and here is why.** After the reduction of §2 the
only data the bound depends on are

| parameter | range | meaning |
|---|---|---|
| $\varphi$ | $[0, \pi/6]$ | direction of the lines, folded by the $D_3$ symmetry of $T$ |
| $\kappa$ | $[1, \lceil 2(a{+}1)/\sqrt3\rceil + 1]$ | line spacing, $h = \kappa\sqrt3/2$ |
| $\rho$ | $[0,1]$ | where the line family sits relative to the chord-profile peak |

Everything else — the length of the shortest lattice vector, the second basis vector,
the translation along the lines — is quantified away by the reduction, *not* fixed. In
particular the count bound is uniform in the two offsets and in the lattice shape.

---

## 2. The reduction (`sketch`) — why three parameters suffice

### 2.1 From a configuration to a family of lines

Let $P$ be $1$-separated in $T(a')$ with $a' < 6$. Rescale by $6/a' > 1$: the triangle
becomes $T(6)$ and the separation becomes $r > 1$ **strictly**. Every gain below comes
from that strictness, so it is worth saying twice: *the theorem is false at $a' = 6$*,
where the $T(7)$ lattice puts 28 points in $T(6)$.

*Lattices.* Let $v_1$ be a shortest non-zero vector of $\Lambda$, $r = |v_1| \ge 1$, and
complete to a Lagrange-reduced basis $(v_1, v_2)$, so $|v_2| \ge r$ and
$|\langle v_2, v_1\rangle| \le |v_1|^2/2$. Then $\Lambda + t$ lies on the lines
$t + jv_2 + \mathbb{R}v_1$, whose consecutive spacing is
$$h \;=\; \sqrt{|v_2|^2 - \langle v_2,v_1\rangle^2/|v_1|^2}\;\ge\; \sqrt{r^2 - r^2/4} \;=\; \tfrac{\sqrt3}{2}\,r \;\ge\; \tfrac{\sqrt3}{2},$$
and on each line the points are spaced exactly $r$. This is the whole content of
Corollary L′. *For a general line-structured $P$ the hypothesis $h \ge \sqrt3/2$ is
**not** automatic and is therefore part of Theorem L's statement* — two lines
$0.1$ apart carrying sparse point sets are $1$-separated.

### 2.2 Counting on one line — where the strictness is spent

$k$ points spaced $\ge r > 1$ inside a segment of length $L$ satisfy $(k-1)r \le L$,
hence $k - 1 < L$, hence
$$k \;\le\; \lceil L \rceil \quad (L > 0), \qquad k \le 1 \quad (L = 0), \qquad k = 0 \ (\text{line misses } T).$$
Write $c(L)$ for that cap. So $|P| \le \sum_j c(\ell_j)$, where $\ell_j$ is the chord
length of $T(6)$ on line $j$. At the aligned unit lattice the chords are exactly
$6,5,4,3,2,1,0$ and $\sum c = 6{+}5{+}4{+}3{+}2{+}1{+}1 = 22$, whereas
$\sum(\ell_j + 1) = 28$. **The entire distance between 28 (which is achievable at
$a=6$) and 22 is the six integer chords being capped by $\lceil\cdot\rceil$ rather than
$\lfloor\cdot\rfloor + 1$.** §7 is the price of that.

### 2.3 The chord profile

For $\varphi \in [0,\pi/3]$ the vertex projections on $n = (-\sin\varphi,\cos\varphi)$
order as $B < A < C$. With $s$ the level measured from the minimum, and
$c_- = \cos(\varphi - \pi/6)$, $c_+ = \cos(\varphi+\pi/6)$,
$$d_1 = a\sin\varphi, \quad w = a\,c_-, \quad L^\ast = \frac{a\sqrt3/2}{c_-}, \quad K = \frac{L^\ast}{w - d_1} = \frac{\sqrt3}{\cos 2\varphi + \tfrac12},$$
$$\ell(s) = L^\ast \frac{s}{d_1}\ \ (0 \le s \le d_1,\ \text{"rising"}), \qquad \ell(s) = L^\ast - K(s - d_1)\ \ (d_1 \le s \le w,\ \text{"falling"}).$$
Note $K$ does not depend on $a$. Four symbolic facts are used as hard caps so that the
interval arithmetic never has to decide a knife-edge comparison numerically:

| | statement | proof |
|---|---|---|
| **F1** | $L^\ast \le a$ on $[0,\pi/6]$ | $c_- \ge \cos(\pi/6) = \sqrt3/2$ |
| **F2** | $Kh \ge 1$ for $h \ge \sqrt3/2$ | $Kh \ge \tfrac{3/2}{\cos2\varphi + 1/2} \ge 1$ |
| **F3** | $L^\ast - Kh \le a - 1$ on $[0,\pi/6]$, $h \ge \sqrt3/2$ | decreasing in $h$; at $h=\sqrt3/2$ the resulting $f(\varphi)$ has $f(0)=a-1$ and $f' < 0$ on $(0,\pi/6)$ (both terms of $f'$ are negative there) |
| **F4** | $L^\ast h/d_1 \ge 3/2$ on $(0,\pi/6]$, $h \ge \sqrt3/2$ | $\ge \tfrac{3/4}{\sin\varphi} \ge \tfrac{3/4}{1/2}$ |

F3 is the one that carries the argument: it says the extremal configuration is *exactly*
the aligned lattice at spacing $\sqrt3/2$, and it hands the branch-and-bound the value
$a-1$ **as an exact rational**, which no floating interval evaluation could supply.

### 2.4 Two regimes, and Lemma A

*R1 — no line meets the rising branch.* Then every chord is $\ell_i = L^\ast - K(x + ih)$
with $x \ge 0$, so by F1 and F2 $\ell_i \le a - i$, and
$$\textbf{Lemma A:}\qquad \sum_i c(\ell_i) \;\le\; \sum_{i=0}^{a-1}(a-i) \;+\; 1 \;=\; \frac{a(a+1)}{2} + 1 .$$
For $a = 6$ that is $\mathbf{22}$ — **with no computation at all**, and it covers the whole
slice $\varphi = 0$. Lemma A alone already closes the line-structured case of EO($k$) for
$k = 3$ (it gives exactly $\Delta(k)-2$) and leaves slack $k-3$ for larger $k$.

*R2 — some line sits at level $\le d_1$.* Parametrise by $\rho \in [0,1]$: the topmost
such line is at $s = (1-\rho)d_1$. Then the falling chords are $L^\ast - K(h - \rho d_1 + ih)$
and the rising ones $L^\ast(1 - \rho - ih/d_1)$, all explicit in $(\varphi,\kappa,\rho)$.
This is what the branch-and-bound covers. **Feasibility filter:** the parametrisation
requires $\rho d_1 < h$; boxes violating it everywhere carry no configuration and are
discarded. Omitting this filter was the one real bug in this lane (§8).

---

## 3. Measure first — reproducing AE's "22", and certifying it exactly

Per PROTOCOL-R5 §6 the inherited number was re-derived before being trusted.

**(a) Direct measurement.** `scan_lattice.py` searches over lattice shape
$(\varphi, x, h)$ with $\lambda_1 = 1$ and over both translations, counting points of
$\Lambda + t$ in $T(a)$ at $a = 6 - 10^{-6}$. **Maximum found: 22**, at
$\varphi \approx 29.0^\circ$ with the hexagonal lattice ($x = 1/2$, $h = \sqrt3/2$).
AE's figure is reproduced. Note it is *not* the aligned lattice, which gives only 21 —
the aligned lattice loses its whole boundary row the instant $a$ drops below 6.

**(b) Exact certificate for the 22.** Floats decide nothing here (`RULES.md` §0 of the
problem file). `exact_check.py` fixes the Pythagorean rotation
$\cos\varphi = 493/565$, $\sin\varphi = 276/565$ (so $\varphi = 2\arctan(6/23)$), the
hexagonal lattice $v_1 = (\cos\varphi,\sin\varphi)$,
$v_2 = \tfrac12 v_1 + \tfrac{\sqrt3}{2}v_1^\perp$, offset $(\alpha,\beta) = (1/20,1/20)$
and $a = 5999/1000 < 6$, and evaluates every containment and every pairwise distance in
exact $\mathbb{Q}(\sqrt3)$ arithmetic (sign of $p + q\sqrt3$ decided by comparing $p^2$
with $3q^2$). Result: **22 points in the closed $T(5999/1000)$, exact minimum squared
pairwise distance $= 1$.** No floating-point step enters the verdict.

So the quantity Theorem L bounds is **at least 22** and the certificate below says it is
**at most 25**. The truth is in $[22,25]$; EO(7) needs $\le 26$.

---

## 4. The certified branch-and-bound

`certify.py`. Interval arithmetic throughout (`mpmath.iv`, 30 digits); the two places
where an exact value is needed — the slice $\varphi = 0$ and the cap F3 — use
`fractions.Fraction`, never a float. Every accept/reject is an interval or exact
comparison.

*Per-box bound.* Chords are bounded using monotonicity where it is known exactly
($\ell$ is decreasing in $\kappa$, the falling chords increase in $\rho$, the rising
ones decrease in $\rho$), so the box reduces to a one-dimensional problem in $\varphi$,
resolved by a **monotonicity-aware** recursion: an interval enclosure of
$\partial\ell/\partial\varphi$ of one sign collapses the sup to a *thin* evaluation at
the corresponding endpoint, and at $\varphi = 0$ that thin evaluation is the exact
rational $a - \kappa(1+i)$. Chains within a family are bounded by F2/F4 rather than
re-evaluated ($\ell^{\rm fall}_i \le \ell^{\rm fall}_0 - i$,
$\ell^{\rm rise}_i \le \ell^{\rm rise}_0 - \tfrac32 i$). Contributions are capped at
$\lceil L^\ast\rceil \le a$ by F1.

*Search.* Depth-first over the $(\varphi,\kappa,\rho)$ box tree, splitting the widest
scaled dimension; a box is discharged when its bound is $\le$ target and stalled when it
reaches width $10^{-9}$ without being discharged. Every box is checkpointed through the
progress file and the final JSON records the stalled boxes.

### 4.1 Results

| $k$ | $a = k-1$ | $n = \Delta(k)-1$ | EO target $\le \Delta(k)-2$ | Lemma A (R1) | **best certified** | boxes | s |
|---|---|---|---|---|---|---|---|
| 3 | 2 | 5 | 4 | 4 | **fails** (1 box stalls at 5) | 345 | 5.8 |
| 4 | 3 | 9 | 8 | 7 | **8** ✓ | 49 | 0.3 |
| 5 | 4 | 14 | 13 | 11 | **13** ✓ | 67 | 0.8 |
| 6 | 5 | 20 | 19 | 16 | **18** ✓ | 181 | 0.8 |
| **7** | **6** | **27** | **26** | **22** | **25** ✓ | **175** | **0.6** |

Reproduce with `python3 run_all.py` (about 3 minutes; `out/run_all.json`).

**The $k = 7$ row is the deliverable**: over the whole 3-parameter space, certified
$\le 25 < 26$, in 175 boxes and under a second. The cost is trivial — this is not a
computation that stalls, and the kill-criterion (§ `KILL-CRITERION.md`) did **not** fire
on Half 1.

The bound cannot be pushed below 25 by this implementation: at target 24 six boxes
stall. The float scan of the *same relaxation* (`scan_line.py`) says its true maximum is
**24**, so the certified 25 carries exactly one unit of interval slop.

### 4.2 The $k=3$ failure is informative, not a bug

At $a = 2$ the relaxation's true maximum is **4** and the target is **4** — zero slack.
With no slack, interval arithmetic cannot close a bound whose extremum sits exactly on
an integer, and the run stalls in a single box at $(\varphi,\kappa,\rho) \approx
(0, 1, 1/2)$. The measured slacks are: $k=3$: 0, $k=4$: 0, $k=5$: 1, $k=6$: 1,
$k=7$: **2**. So the method's headroom *grows* with $k$, which is the opposite of the
usual situation in this directory and is the reason $k = 7$ is reachable at all.

---

## 5. What has and has not been shown

- **Shown (`numerical`, certified):** Theorem L and Corollary L′ at $a=6$, bound 25.
- **Shown (`numerical`, exact):** a 22-point unit-separation lattice in $T(5999/1000)$.
- **Shown (`sketch`):** the reduction, F1–F4, Lemma A.
- **NOT shown:** EO(7). Theorem L says nothing whatever about configurations that are
  not line-structured, and a counterexample to EO(7) need not be one. §6 is the gap.
- **NOT shown:** that this is a *new* theorem. It is elementary and the line-counting
  argument is the kind of thing Oler-era literature may well contain; `WebFetch` is
  blocked and `arxiv.org` is behind the egress block (PROTOCOL-R5 §3), so no literature
  check was possible. Treat novelty as unassessed.

---

## 6. Half 2 — the forcing hypothesis, stated precisely

> **(H) Line-structure forcing at $k = 7$.** *There exists $\varepsilon_0 > 0$ such
> that for every $a \in (6-\varepsilon_0,\,6]$ and every $1$-separated
> $P \subset T(a)$ with $|P| \ge 27$, there exist a unit vector $u$, $\tau \in \mathbb R$
> and $h \ge \sqrt3/2$ with $P \subset \bigcup_{j}\{x : \langle x,u^\perp\rangle = \tau + jh\}$.*

**Conditional Theorem (`sketch`, and conditional on an unproved hypothesis).**
(H) together with Theorem L implies Erdős–Oler at $k=7$, i.e. $27$ points at separation
$\ge 1$ force $a \ge 6$ (equivalently $d(27) \ge 12$).

*Proof.* Suppose $P$ is $1$-separated, $|P| = 27$, $P \subset T(a)$ with $a < 6$. By
monotonicity we may take $a \in (6-\varepsilon_0, 6)$. By (H), $P$ is $h$-line-structured
with $h \ge \sqrt3/2$. By Theorem L, $|P| \le 25 < 27$ — contradiction. $\square$

**Three things must be said about (H).**

1. **It is unproved and this lane did not attempt to prove it.**
2. **It is non-vacuous and falsifiable, and the place to attack it is $a = 6$.** For
   $a < 6$, (H) is a statement about a set that EO(7) says is empty, so it would be
   vacuously true if EO(7) held — the closed endpoint $a = 6$ is deliberately included
   precisely so that (H) has content: $27$- and $28$-point $1$-separated configurations
   in $T(6)$ do exist. **Anyone can refute (H) by exhibiting one that is not on a line
   family.** That is the explicit falsification target AE asked for.
3. **It is weaker than AE's "near-lattice" phrasing** — it asks only for collinearity
   along one direction, not for a lattice — which is the one place this lane improved on
   the proposal.

### 6.1 Plausibility probe (`numerical`, weak)

`probe_forcing.py` measures the *line defect*
$\delta(P) = \min_{u,h\ge\sqrt3/2,\tau}\max_p \operatorname{dist}(\langle p,u^\perp\rangle, \tau + h\mathbb Z)$
on $27$-point $1$-separated configurations in $T(6)$: (i) random starts relaxed to
feasibility, (ii) the $T(7)$ lattice minus one point jittered at amplitudes
$0.1, 0.25, 0.5$ and relaxed back. **Every feasible configuration found had line defect
$0$ to machine precision** (control: the lattice minus its apex gives $1.9\times10^{-16}$).

That is *weak* positive evidence and must not be read as more. Local relaxation in this
problem is known to be dominated by the lattice attractor —
[`../eo-counterexample-hunt/`](../eo-counterexample-hunt/) §5b/§6 reports ~95–100 % of
solves landing exactly on the lattice value at $k=7$, and §6a says a local method
"relaxes into the lattice-with-a-hole rather than finding somewhere new". I read that
directory; I did not re-run it, and I am quoting it as a *caveat on my own probe*, not
as an input to any claim. So the probe cannot distinguish "(H) is true" from "my search
cannot leave the lattice basin", and it should be scored as the latter until a search
that provably can leave the basin says otherwise.

---

## 7. The negative result AE did not anticipate — (H) cannot be relaxed

This is the part a follow-up must read before spending another round on AE.

(H) demands **exact** collinearity. No real packing satisfies an exact linear relation,
so the only useful version of the conditional theorem is a $\delta$-robust one:
*$P$ lies within $\delta$ of the line family*. That version needs a $\delta$-robust
Theorem L, in which the per-strip cap becomes
$\bigl\lceil \ell^\delta_j / \sqrt{1-4\delta^2}\,\bigr\rceil$ with
$\ell^\delta_j = \sup_{|t - s_j| \le \delta} \ell(t)$ the $u$-extent of the slab.

`delta_scan.py` measures the maximum of that bound over the same $(\varphi,h,\theta)$
grid at $a = 6$:

| $\delta$ | $0$ | $10^{-9}$ | $10^{-6}$ | $10^{-4}$ | $10^{-3}$ |
|---|---|---|---|---|---|
| max bound | **24** | **27** | **28** | 28 | 28 |
| $\le 26$? | yes | **no** | **no** | no | no |

**The bound is discontinuous at $\delta = 0$.** The reason is exactly §2.2: the whole
gain from 28 down to 22 is the six chords of the extremal configuration being *exactly*
integers, so that $c(\ell) = \lceil \ell\rceil$ rather than $\lfloor \ell\rfloor + 1$.
Any $\delta > 0$ restores the $+1$ on every strip at once and the bound jumps back past
the target. This is structural, not a tuning artifact: it would survive improving the
certified 25 to the true 24, and even to 22, because the jump is $+1$ per strip on up to
seven strips.

**Consequence.** The conditional result of §6 is real but **fragile in a way that makes
it unusable as stated for an approximate forcing theorem.** A follow-up that wants a
robust conditional must replace §2.2's counting step with one that does not spend all
its margin on an equality case — e.g. counting with the second line family as well
(using $v_2$, not only $v_1$), which the present relaxation throws away entirely. That
is a concrete, stated next step with a measured target: it must beat $28 - 26 = 2$ units
of loss at $\delta \to 0^+$.

I am recording this as a **success**, per `RULES.md` §0: it is a clean refutation of the
only usable form of AE's Half 2, obtained from the object AE's Half 1 produced.

---

## 8. What I am least sure of, and what I got wrong

**Least sure:** the passage from "$P$ is $1$-separated and line-structured" to
"$h \ge \sqrt3/2$". For lattices this is Lagrange reduction and I am confident (§2.1).
For the general line-structured sets that Theorem L is stated over, $h \ge \sqrt3/2$ is a
**hypothesis, not a consequence**, and (H) has to supply it. If a forcing theorem could
only supply the line family and not the spacing lower bound, Theorem L would not apply and
the conditional would collapse. I have stated $h \ge \sqrt3/2$ inside both Theorem L and
(H) so the dependency is visible rather than buried, but a reader should check that I have
not quietly used $h \ge \sqrt3/2$ anywhere it was not assumed.

**Next in doubt:** the $D_3$ folding of $\varphi$ to $[0,\pi/6]$ (rotation by $2\pi/3$
gives $\varphi \bmod \pi/3$; the reflection $X \mapsto a - X$ gives
$\varphi \mapsto \pi/3 - \varphi$). It is elementary but it is a global reduction of the
search space and an error there would silently un-cover part of the domain.

**What I got wrong, recorded because it is the kind of error this repo is about.** The
first branch-and-bound reported ~17 000 stalled boxes and a bound of 27 at $a=6$, and I
was one step from writing "the method stalls at 27". It did not: the $(\varphi,\kappa,\rho)$
parametrisation admits boxes with $\rho\,d_1 \ge h$, which correspond to **no
configuration at all**, and the bound was being computed on those phantom regions. With
the feasibility filter the same run closes in 129 boxes. The lesson is the one in
PROTOCOL-R5 §6: the arithmetic was fine and the *premise* — that every box in my
parameter box was a real parameter — was not.

---

## 9. Inputs, and which of them I verified myself

| input | source | verified here? |
|---|---|---|
| EO($k$) statement, $d = 2a$ normalisation, $n = \Delta(k)-1$ | `../eo-exhaustion/` §0, problem `README.md` | re-derived from the problem statement; arithmetic checked ($\Delta(7)=28$, $n=27$, $a=6$) |
| triangle placement, closed triangle, non-strict inequalities | problem `RULES.md` §2 | used verbatim, not reinterpreted |
| AE's "measured value is 22" | `../r4-approaches/` §1 | **yes** — reproduced independently (§3a) and then certified in exact $\mathbb{Q}(\sqrt3)$ (§3b) |
| AE's "3-parameter space" | `../r4-approaches/` §1 | **derived independently** (§1); the three parameters here are $(\varphi,\kappa,\rho)$, which is probably not what AE had in mind (a hexagonal lattice's rotation + 2 offsets) — mine covers *all* lattices, not only hexagonal ones |
| lattice-attractor caveat on local search | `../eo-counterexample-hunt/` §5b, §6, §6a | read, **not** re-run; used only to weaken my own §6.1 conclusion, never as support for a claim |
| $k=3,4,5,6$ optimality (validation targets) | problem `README.md`, `cited` | used only as *targets to hit*, not as inputs to any proof |
| Oler's inequality, the $n=16$ covering plateau, every `r3-*`/`r4-*` result | — | **not used at all.** Nothing in this lane depends on an unmerged or same-family result |

Not used, deliberately: the unmerged $n=16$ covering bound (PRs #98/#104), and every
sibling `r3-*`/`r4-*` numerical or sketch result (PROTOCOL-R5 §5).
