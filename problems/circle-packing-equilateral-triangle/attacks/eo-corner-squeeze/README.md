# Attack: squeezing the forced corner occupancy, and why counting corners cannot close Erdős–Oler

**Claim type: neither construction nor optimality — no bound on $s(n)$, upper or lower, is
claimed anywhere in this file.** (Problem [`../../RULES.md`](../../RULES.md) §1 asks for that
sentence first.) What is here is: an independent re-derivation of the corner constraint this
attack was handed, one *new elementary proof* of its strongest instance, and a **no-go result**
showing that corner occupancy plus region capacity cannot decide the Erdős–Oler conjecture —
demonstrated by running the method on cases where the answer is already known. Nothing enters
`results/`; nothing here is assumable, including by me (repo [`RULES.md`](../../../../RULES.md) §3).

- Route: take Prover A's conditional Erdős–Oler ([`../eo-hull-deficit/`](../eo-hull-deficit/) §4,
  §9) contrapositively — a $k = 7$ counterexample must be lattice-dense at every corner at every
  integer scale — and push that rigidity against the global count of 27.
- Code: [`experiments/packing-eo-corner-squeeze/`](../../../../experiments/packing-eo-corner-squeeze/)
  — one command, Python standard library only, exact arithmetic throughout.
- Transcript: [`out/report.txt`](../../../../experiments/packing-eo-corner-squeeze/out/report.txt).
- Kill-criterion, written before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md).
- Author: `claude` (Claude Opus 5), 2026-08-21.

| What | Status |
|---|---|
| §2 Re-derivation of Prover A's Theorem 3 / Corollary 4 / (CIO-$j$) | `sketch` — his, re-derived here; **still `sketch`, same-family agreement grants nothing** |
| §3 **Lemma P** — the top-scale corner constraint, proved without Oler and without CIO | `sketch` — mine; three lines, exactly checked, depends on nothing but the separation hypothesis |
| §4 Aggregate accounting (Viviani floor vs CIO floor vs capacity ceiling) | `sketch` — mine; closed-form, exactly checked for $k \le 12$ |
| §5 **The no-go**: the corner-occupancy relaxation is feasible at $k = 4, 5, 6, 7$ | `numerical` — exact integer witnesses, each re-verified against every constraint |
| §6 The surviving profile at $k = 7$ | `numerical` — explicit |
| Oler's inequality; $d(n)$ for $n \le 15$, $n = 20, 21$ | `cited` — see [`../../README.md`](../../README.md) |

---

## 0. Kill-criterion outcome, stated up front

> **K1 (primary).** *"If the corner-occupancy relaxation turns out to be feasible at $k = 6$
> — where Erdős–Oler is `cited`-true, so the geometric system is infeasible — then the relaxation
> provably cannot decide Erdős–Oler, and it cannot decide $k = 7$ either. Record the explicit
> feasible witness, report the refutation, and stop."*
>
> **MET, and more strongly than the criterion asked.** The relaxation is feasible not only at
> $k = 6$ but at $k = 4$ and $k = 5$, whose Erdős–Oler cases rest on **unqualified** citations
> (Melissen 1993 for $n = 9$; Payan 1997 for $n = 14$) rather than on the $n = 20$ attribution
> that [`../../README.md`](../../README.md) flags. So the no-go does not depend on the qualified
> row. Explicit integer witnesses at all four $k$ are in §5; each is re-verified against every one
> of the several thousand constraints.
>
> **The sharpest form of the failure.** For $a$ just below $k-1$ we have
> $\lfloor \mathrm{Oler}(a)\rfloor = T(k) - 1$ exactly, and the relaxation is feasible at
> $n = T(k)-1$. So **the relaxation's bound equals Oler's bound exactly: it closes zero of the
> missing one point**, at every $k$ tested. This is the corner-count analogue of the Relaxation
> Barrier in [`../eo-hull-deficit/`](../eo-hull-deficit/) §6, reached by a completely different
> route, and it is the third independent time this project has hit exact break-even.
>
> **K2, K3 (controls).** *Not met.* Every exact certificate in the repo ($n = 3,\dots,21$) passes
> exact separation, exact Viviani, exact containment, and **every** computed region capacity, with
> several boxes exactly tight. See §5.2.

**A circular result I nearly shipped, recorded per `RULES.md` §0.** My first run reported the
relaxation **infeasible at $k = 4$** — i.e. a proof of Erdős–Oler at $k = 4$ by pure counting.
It was circular. The single violated constraint was the capacity of the *whole triangle*, and
that capacity had been computed from the cited table entry $d(9) = 3$ — which **is** Erdős–Oler at
$k = 4$. The guard is now explicit in the code (`geom.EXCLUDE`), and §5.1 spells it out, because
this is precisely the failure mode `RULES.md` §7 predicts: a fluent argument that quietly assumes
what it proves. Had the same bug survived to $k = 7$ it would have read as a solved open problem.

**What survives the kill:** §3 is a genuinely new, elementary, Oler-free proof of the strongest
instance of the corner constraint, valid for every $k$, and it explains structurally *why* that
instance is break-even rather than merely observing that it is. §4 isolates the one place where
the three corners genuinely interact ($k \ge 7$ only) and shows the interaction is too small by a
quadratic margin. §5 is the no-go.

---

## 1. Setup and notation

Oler normalisation throughout: minimum separation **1**, containing equilateral triangle $T$ of
side $a$. (The repo's certificates use separation 2 and side $2a$; the code halves every
coordinate on load. Several workers slipped on this today; re-checked here.)

For a corner $V$ let $u_V(p)$ be the corner coordinate normalised so that

$$\Delta_V(t) \;=\; \{p \in T : u_V(p) \le t\}$$

is the closed corner triangle at $V$ of side $t$. With $A = (0,0)$, $B = (a,0)$,
$C = (a/2, a\sqrt3/2)$,

$$u_A = x + \tfrac{y}{\sqrt3}, \qquad u_B = (a-x) + \tfrac{y}{\sqrt3}, \qquad
u_C = a - \tfrac{2y}{\sqrt3}, \qquad
\boxed{u_A + u_B + u_C = 2a}$$

the last being Viviani's theorem in this normalisation. Each $u_V \in [0,a]$; the three corners
have $u$-triples $(0,a,a)$, $(a,0,a)$, $(a,a,0)$. Write

$$S_j^{(V)} \;=\; \bigl|\{p \in E : u_V(p) < j\}\bigr|, \qquad
N(t) = \max \#\{\text{unit-separated points in a closed triangle of side } t\},$$

$T(m) = m(m+1)/2$, $\mathrm{Oler}(a) = \tfrac{a^2}{2}+\tfrac{3a}{2}+1$, and
$\varepsilon(a) = \mathrm{Oler}(a) - n$.

**The target.** Erdős–Oler at $k$: $n = T(k)-1$ unit-separated points force $a \ge k-1$. Oler
alone gives only $a \ge a_0(k) = \tfrac{-3+\sqrt{8T(k)-7}}{2}$; at $k = 7$, $a_0 = 5.86546\ldots$
against the truth $6$. **The gain any argument must produce is exactly one point** — measured in
points, never in side length.

**Lattice reference.** The triangular lattice of $T(k)$ points in $T$ of side $k-1$ has
$u_A = i + j$, $u_B = (k-1) - i$, $u_C = (k-1) - j$ for $0 \le i, j$, $i + j \le k-1$; every $u_V$
is a non-negative integer and $S_j^{(V)} = T(j)$ exactly, for every $j$ and every $V$.

---

## 2. The corner constraint, re-derived

Prover A's Theorem 3 (CIO) and Corollary 4 are `sketch` and therefore **not assumable, including
by their author** (`RULES.md` §3). I re-derived both from scratch before using them. What I
checked, and what I did not:

**Theorem 3 (CIO), re-derived.** Given $t_A, t_B, t_C \ge 0$ with $t_U + t_V \le a$ for each pair,
put $K = T \cap \bigcap_V \{u_V \ge t_V\}$ and $E' = E \setminus \bigcup_V \Delta_V(t_V)$. Then
$|E'| \ge n - \sum_V m_V$ with $m_V = |E \cap \Delta_V(t_V)|$, and Oler applied to $E'$ plus
monotonicity $\operatorname{conv}(E') \subseteq K$ gives $|E'| \le B(K)$. I recomputed
$A(K) = A(T) - \tfrac{\sqrt3}{4}\sum t_V^2$ and $M(K) = 3a - \sum_V t_V$ (each side of $T$ loses
$t_U$ at one end and $t_V$ at the other, and each cut edge returns $t_V$), giving
$B(T) - B(K) = \sum_V \tfrac{t_V^2+t_V}{2}$. The degenerate-$E'$ cases check out as he states
them: $B(K) \ge 1$ handles $|E'| \le 1$; a convex set has perimeter $\ge 2\,\mathrm{diam}$, so
$|E'| = 2$ gives $B(K) \ge 2$; $m$ collinear points span a segment of length $\ge m-1$ in $K$, so
$M(K) \ge 2(m-1)$ and $B(K) \ge m$.

**The side condition is load-bearing and I checked every use.** The closed forms for $A(K)$ and
$M(K)$ require $t_U + t_V \le a$; without it the formula double-subtracts overlapping corner
triangles and the lemma is **false**, not merely unproven. Every use below is a *single* corner
($t_V = t$ at one corner, $0$ at the other two), so the condition reads $t \le a$, and every $j$
used satisfies $j \le \lfloor a \rfloor \le a$. This is the failure the manager flagged as most
likely; it does not occur here.

**(CIO-$j$), the contrapositive I actually use.** Suppose $n = T(k)-1$ points are unit-separated
in $T$ of side $a < k-1$. Then $\varepsilon(a) = \mathrm{Oler}(a) - n < \mathrm{Oler}(k-1) - n = 1$,
**strictly**, because $\mathrm{Oler}$ is increasing and $\mathrm{Oler}(k-1) = T(k)$. Apply Theorem 3
at one corner with $t < j$ and let $t \to j^-$: since $E$ is finite, $|E \cap \Delta_V(t)| = S_j^{(V)}$
for $t$ close enough to $j$, and $\tfrac{t^2+t}{2} \to T(j)$, so

$$T(j) - S_j^{(V)} \;\le\; \varepsilon(a) \;<\; 1 \qquad\Longrightarrow\qquad
\boxed{S_j^{(V)} \;\ge\; T(j)} \quad\text{for every corner } V,\ 1 \le j \le \lfloor a \rfloor .$$

The last step is integrality, and **it is the strict inequality $\varepsilon(a) < 1$ that makes it
work** — with $\varepsilon \le 1$ one gets only $S_j \ge T(j) - 1$, which is vacuous. The
supremum $1$ is not attained, and the constraint is closed, so the strictness transfers. I flag
this because it is the step the reviewing worker nearly filed as an off-by-one against Prover A,
and because a reader who writes "gain $\ge 1$" instead has a strictly weaker claim.

At $k = 7$: $S_j^{(V)} \ge T(j)$ for $j = 1,\dots,5$ and all three corners, i.e. **at least
$1, 3, 6, 10, 15$ points within corner-distance $1,2,3,4,5$ of every corner simultaneously.**
That is the rigid object this attack was pointed at.

**What I did not verify:** Oler's inequality itself (`cited`, read in full by
[`../oler-lower-bound/`](../oler-lower-bound/)); and the monotonicity of perimeter under inclusion
of convex sets, which I used as standard.

**Status is unchanged by any of this.** I am the same model family as the author, so my agreement
grants nothing (`RULES.md` §5). (CIO-$j$) stays `sketch`, and §5's no-go is stated so that it does
not depend on (CIO-$j$) being true — see §5.3.

---

## 3. Lemma P — the top-scale constraint, with no Oler in it

The single strongest instance, $j = \lfloor a \rfloor = k-2$, has an elementary proof that needs
neither Oler's inequality nor CIO nor anything with a status weaker than `cited`.

> **Lemma P.** Let $E$ be unit-separated in the closed equilateral triangle $T$ of side $a$, and
> let $k \ge 3$ satisfy $k - 2 \le a < k-1$. Then for every corner $V$,
> $$\bigl|\{p \in E : u_V(p) \ge k-2\}\bigr| \;\le\; 2k-2 .$$

**Proof.** The region $\{u_V \ge k-2\}$ is the trapezoid between the line $u_V = k-2$ and the side
of $T$ opposite $V$. Take coordinates in which that opposite side is horizontal: write $x$ for the
horizontal coordinate and let $w$ be the trapezoid's vertical extent, so
$w = (a - (k-2))\tfrac{\sqrt3}{2} < \tfrac{\sqrt3}{2}$ because $a < k-1$. Two points of $E$ in the
trapezoid differ vertically by some $v \le w$ and horizontally by $h$, and $h^2 = d^2 - v^2 \ge
1 - w^2 > \tfrac14$. Their horizontal projections therefore lie at mutual distance at least
$g = \sqrt{1-w^2}$ inside an interval of length at most $a$ — the opposite side is the longest
horizontal chord of the trapezoid — so $m$ points force $(m-1)g \le a$, i.e.

$$m \;\le\; 1 + \frac{a}{\sqrt{1-w^2}} .$$

Finally $\dfrac{a}{\sqrt{1-w^2}} < 2k-2$ for $a < k-1$: squaring, this is
$a^2 + 3(k-1)^2\bigl(a-k+2\bigr)^2 < 4(k-1)^2$, whose left side is increasing on $[k-2, k-1]$ and
equals the right side exactly at $a = k-1$. Hence $m < 2k-1$, so $m \le 2k-2$. $\blacksquare$

**It is exactly (CIO-$(k-2)$).** With $n = T(k)-1$, $\;n - (2k-2) = T(k) - 1 - 2k + 2 =
\tfrac{(k-1)(k-2)}{2} = T(k-2)$, so Lemma P says $S_{k-2}^{(V)} \ge T(k-2)$ — the top-scale
instance of §2, for every $k$, with a completely different proof. That is the independent
verification `RULES.md` §3 asks for before building on a `sketch`, at least at this one scale.

**And it says why that instance is break-even.** At $a = k-1$ the inequality above is an
*equality*: the lattice puts $(k-1) + k = 2k-1$ points in $\{u_V \ge k-2\}$ (a row of $k-1$ and the
full side of $k$), and the bound is $1 + (k-1)/\tfrac12 = 2k-1$. The constraint gains exactly one
point as $a$ drops below $k-1$, and **exactly one point is what the whole conjecture needs** — so
this constraint is worth precisely the target and not a sliver more. Verified exactly for
$k = 3,\dots,12$ over a grid of rational $a$ (`lemmas.py`); the "floor" column of the transcript
never exceeds $2k-2$ and reaches it at every $a$ close enough to $k-1$.

---

## 4. Aggregate accounting: where the three corners interact, and by how little

Corner constraints at one corner are break-even (§3). The hope was that three corners *at once*
overcount. Viviani makes that precise. For every point, $\sum_V u_V = 2a$, so
$\sum_V \lfloor u_V \rfloor \le \lfloor 2a \rfloor = 2k-3$ for $a \in [a_0(k), k-1)$. Summing over
$E$ and rewriting $\sum_p \lfloor u_V(p) \rfloor = \sum_{j=1}^{k-2}\bigl(n - S_j^{(V)}\bigr)$:

$$\mathcal S \;:=\; \sum_V \sum_{j=1}^{k-2} S_j^{(V)} \;\ge\; \underbrace{n\,(k-3)}_{V(k)} .$$

Against this, (CIO-$j$) gives $\mathcal S \ge C(k) = 3\sum_{j=1}^{k-2}T(j) = \tfrac{k(k-1)(k-2)}{2}$
and the capacities give $\mathcal S \le U(k) = 3\sum_{j=1}^{k-2}N(j^-)$. Exactly (`lemmas.py`,
integer arithmetic, $k \le 12$):

$$V(k) - C(k) \;=\; \frac{(k-1)(k-6)}{2}$$

| $k$ | 4 | 5 | 6 | **7** | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| $V(k)-C(k)$ | −3 | −2 | 0 | **+3** | +7 | +12 | +18 |
| $U(k)-V(k)$ | 6 | 11 | 18 | **27** | 41 | 57 | 75 |

Two readings, and the second is the one that matters.

1. **The three corners do interact, and only from $k = 7$.** Below $k = 7$ Viviani adds nothing to
   (CIO-$j$); at $k = 6$ it exactly ties; from $k = 7$ it forces $\tfrac{(k-1)(k-6)}{2}$ units of
   corner occupancy *beyond* what CIO alone demands (3 units at $k = 7$). This is the only place
   in the whole attack where the corners genuinely talk to each other, and it is real.
2. **It is nowhere near enough, and the shortfall grows.** The capacity ceiling exceeds the
   Viviani floor by $U(k)-V(k) > 0$ for every $k$ — with the conjectural extension
   $N(j^-) = T(j+1)-2$ this is exactly $k^2-4k+6$, and with only what is proven it is larger
   still. So the aggregate can never be contradictory: **the gap widens quadratically in $k$.**

### 4.1 The overlap, computed exactly (lines 1 and 2 of the brief)

At $k = 7$, $a = 5.99$, with $u_A+u_B+u_C = 2a$ throughout:

| $j$ | $T(j)$ | $\Delta_U(j)^\circ \cap \Delta_V(j)^\circ$ | cap | triple intersection | cap | do the three cover $T$? |
|---:|---:|---|---:|---|---:|---|
| 1 | 1 | empty | – | empty | – | no |
| 2 | 3 | empty | – | empty | – | no |
| 3 | 6 | triangle, side $2j-a = 0.01$ | 1 | empty | – | no |
| 4 | 10 | triangle, side $2.01$ | 6 | inverted triangle, side $3j-2a = 0.02$ | 1 | **yes** |
| 5 | 15 | triangle, side $4.01$ | 15 | inverted triangle, side $3.01$ | 10 | **yes** |

$\Delta_U(j)$ and $\Delta_V(j)$ meet exactly when $2j > a$ (so $j \ge 3$); all three meet — and,
equivalently, cover $T$ — exactly when $3j > 2a$ (so $j \ge 4$), because a point outside all three
would have $\sum_V u_V \ge 3j > 2a$. Since they cover, inclusion–exclusion is an **identity**:

$$27 \;=\; \sum_V S_j^{(V)} \;-\; \sum_{\text{pairs}} \bigl|E \cap \Delta_U^\circ \cap \Delta_V^\circ\bigr|
\;+\; \bigl|E \cap \Delta_A^\circ \cap \Delta_B^\circ \cap \Delta_C^\circ\bigr| .$$

So the forced double count is real and computable — and it is comfortably absorbed:

| $j$ | (CIO) $\sum_V S_j^{(V)} \ge$ | forced $\sum_{\text{pairs}} \ge$ | capacity of $\sum_{\text{pairs}} \le$ | margin |
|---:|---:|---:|---:|---:|
| 4 | 30 | $30 - 27 = 3$ | $3 \times 6 = 18$ | 15 |
| 5 | 45 | $45 - 27 = 18$ | $3 \times 15 = 45$ | 27 |

The brief's arithmetic is right — $3\,T(5) = 45 > 27$, so the three scale-5 corner blocks must
share at least 18 points — but the shared regions are big: a triangle of side $10 - a > 4$ holds up
to 15 unit-separated points and three of them hold 45. **The overlap is forced and not
contradictory, by a margin of 27 points at $j = 5$ and 15 at $j = 4$.** That is not a near miss,
and it is why line 1 and line 2 of the brief do not bite.

(One caution recorded for the next reader: the *complementary* pair region
$\{u_A \ge j\} \cap \{u_B \ge j\}$ is a **rhombus** of side $a-j$ with a vertex at $C$, not a
triangle. I derived a contradiction at $j = 4$ from the triangle reading in scratch, and it
evaporated on correcting the region — the rhombus holds up to 8 points, not 4. In corner
coordinates $T$ has vertices $(0,a), (a,0), (a,a)$, not $(0,0), (a,0), (0,a)$, and that is where
the error came from.)

---

## 5. The no-go: the corner-occupancy relaxation is feasible where the truth is not

### 5.1 The relaxation

Give each point its **shell vector** $\sigma(p) = (\lfloor u_A \rfloor, \lfloor u_B \rfloor,
\lfloor u_C \rfloor)$ and let $z_c$ count the points in cell $c$. Every constraint below is a
genuine consequence of the geometric system, so the system is a relaxation:

| | constraint | source |
|---|---|---|
| (T) | $\sum_c z_c = n$ | definition |
| (C-$j$) | $S_j^{(V)} \ge T(j)$ | §2 (`sketch`); at $j = k-2$ also §3 |
| (K-$j$) | $S_j^{(V)} \le N(j^-)$ | capacity of the open corner triangle, `cited` |
| (B) | $\sum_{c \subseteq R} z_c \le \mathrm{cap}(R)$ for **every** corner-coordinate box $R$ | Oler on the convex region $R$, plus the cited $N$ table when $R$ is an equilateral triangle |

This is a **partition/capacity scheme with genuine per-region capacities**, which the manager's
retraction correctly identifies as a live move (capping a piece by its true capacity is not the
same as summing Oler over pieces, and can beat Oler — his $k = 3$ witness shows it does). Boxes
range over all integer $[l_V, h_V]$ per corner: 100 binding boxes at $k = 4$, 5164 at $k = 7$.
Areas are exactly rational after Oler's $2/\sqrt3$ weighting; only perimeters are intervals, and
they are rounded outward, so every capacity is a rigorous upper bound.

**The circularity guard.** Testing level $k$ must not use $d(T(k)-1) = k-1$ from the cited table,
because that value *is* the statement under test. Without the guard the whole-triangle box
capacity imports the answer and the relaxation reports "infeasible" at every $k$ — which is what
my first run did, and it is the only reason this file is not an accidental extraordinary claim.
Values at levels below $k$ are kept: using Erdős–Oler at $k-1$ to study $k$ is induction.

### 5.2 The controls (K2, K3) pass

All twelve non-degenerate exact certificates in the repo
($n = 3,4,5,6,7,8,9,10,14,15,20,21$) are loaded, halved,
and checked in exact $\mathbb{Q}(\sqrt3,\sqrt{11})$: all $\binom{n}{2}$ separations $\ge 1$,
$u_A+u_B+u_C = 2a$ identically, $0 \le u_V \le a$; then the configuration is embedded in a
rational-sided triangle and **every** box capacity is tested against the true count. Up to 13845
boxes per certificate, **no violation anywhere**, and the tightest boxes have slack $0$ — so the
capacities are sharp enough to be worth something, not vacuous. The lattice certificates
reproduce $S_j^{(V)} = T(j)$ exactly, as §1 requires.

### 5.3 The result

Integer feasibility (a feasibility claim needs a *witness*, not a search method: the randomised
restart search `relax.find_feasible_random` is tried first because it is fast, and whatever it
returns is re-verified against **every** constraint by `relax.check_solution`; the exhaustive
`relax.feasible` is the fallback and is the only routine that could report INFEASIBLE):

| $k$ | $n = T(k)-1$ | $a$ | $\varepsilon(a)$ | cells | binding boxes | verdict | Erdős–Oler at this $k$ |
|---:|---:|---|---:|---:|---:|---|---|
| 4 | 9 | $2.99$ | $0.955$ | 16 | 100 | **FEASIBLE** | **`cited`-true** (Melissen 1993, $d(9)=3$) |
| 5 | 14 | $3.99$ | $0.945$ | 28 | 538 | **FEASIBLE** | **`cited`-true** (Payan 1997, $d(14)=4$) |
| 6 | 20 | $4.99$ | $0.935$ | 43 | 1874 | **FEASIBLE** | **`cited`-true**, qualified ($d(20)=5$) |
| 7 | 27 | $5.99$ | $0.925$ | 61 | 5164 | **FEASIBLE** | open |

> **The corner constraints have no contradiction visible to counting**, at $k = 7$ — and,
> decisively, **none at $k = 4$, $k = 5$ or $k = 6$ either.**

A precision that matters, because the loose version of this sentence is wrong. At $k = 4,5,6$ the
corner constraints *are* jointly contradictory in the literal sense: Erdős–Oler is true there, so
no configuration satisfies them, because no configuration exists at all. The question is never
"is the system contradictory" — for a true conjecture it always is. The question is **whether a
given class of argument can exhibit the contradiction**, and the honest test is to run that class
of argument on a case where the contradiction is known to be there. That is what §5.3 does, and
the class fails the test.

At $k = 4$ and $k = 5$ this rests on unqualified citations, so the conclusion is independent of the
$n = 20$ attribution flagged in [`../../README.md`](../../README.md). A relaxation that cannot see
the contradiction in a case where one certainly exists cannot be the thing that supplies it at
$k = 7$. **The route is dead, and it is dead for a reason that does not depend on (CIO-$j$)
being true** — adding a valid constraint can only shrink a feasible set, so if the relaxation
including (C-$j$) is feasible, so is the relaxation without it.

**The sharpest form.** For $a \in (a_0(k), k-1)$ we have $\lfloor \mathrm{Oler}(a)\rfloor = T(k)-1$
exactly, and the relaxation is feasible at $n = T(k)-1$. So the relaxation's best bound *is*
$\lfloor\mathrm{Oler}(a)\rfloor$: **it closes exactly $0$ of the missing $1$**, at every $k$
tested. Three independent routes in this project — the deficit relaxation
([`../eo-hull-deficit/`](../eo-hull-deficit/) §6), corner cuts (ibid. §5), and now corner
occupancy with cell capacities — all land on exact break-even. That coincidence is itself the
finding: the one point is not recoverable from any bound that sees only *how many* points are
*where*.

### 5.4 How far from deciding? Exactly one point of capacity

A refutation is more useful with a distance attached. Reduce **every** capacity in the system
(box caps, cell caps and the $N(j^-)$ ceilings) by a uniform $\tau$ points and ask for the least
$\tau$ that makes it infeasible (`tighten.py`):

| $k$ | $\tau = 0$ | $\tau = 1$ |
|---:|---|---|
| 4 | feasible | **infeasible** |
| 5 | feasible | **infeasible** |

The result is not trivial: after the $\tau = 1$ tightening the total cell capacity is still 19
against $n = 9$ at $k = 4$, and 35 against $n = 14$ at $k = 5$, so infeasibility is not simply a
shortage of room. ($k = 6$ and $k = 7$ at $\tau = 1$ were **not completed** inside the compute budget — proving
infeasibility is far more expensive than exhibiting a witness — so they are reported as unknown,
not as agreeing.)

So at $k = 4, 5$ the relaxation is exactly **one point of capacity** away from deciding the cases
it should decide. That is not a claim that some single capacity is off by one — it is a uniform tightening,
and a real proof would have to find that point somewhere specific. But it is the same "exactly one
point" that Lemma P produces at the top scale, that Oler's slack $\varepsilon(a) < 1$ measures,
and that [`../eo-hull-deficit/`](../eo-hull-deficit/) §5 finds in every corner cut. Four
independent measurements of the same missing unit.

---

## 6. What survives: the profile, and why it is not a counterexample

The $k = 7$ witness, 27 points over 22 cells, at $a = 5.99$ (cells written
$(\lfloor u_A\rfloor,\lfloor u_B\rfloor,\lfloor u_C\rfloor)$, all with $\sum \lfloor u_V\rfloor
\in \{9,10,11\}$ as Viviani requires):

```
(0,4,5):1 (1,5,4):1 (1,5,5):1 (2,3,5):1 (2,4,5):1 (2,5,3):3 (3,2,5):2 (3,3,4):1
(3,3,5):1 (3,4,4):1 (4,2,3):1 (4,3,4):1 (4,4,1):1 (4,4,2):1 (4,5,2):1 (5,0,5):1
(5,1,4):3 (5,2,3):1 (5,3,3):1 (5,4,2):1 (5,5,0):1 (5,5,1):1
```

Its corner profiles, against the floor CIO demands and the ceiling capacity allows:

| | $S_1$ | $S_2$ | $S_3$ | $S_4$ | $S_5$ |
|---|---:|---:|---:|---:|---:|
| CIO floor $T(j)$ | 1 | 3 | 6 | 10 | 15 |
| corner $A$ | 1 | 3 | 8 | 13 | 18 |
| corner $B$ | 1 | 4 | 8 | 13 | 19 |
| corner $C$ | 1 | 3 | 6 | 12 | 19 |
| capacity ceiling $N(j^-)$ | 1 | 4 | 8 | 13 | 19 |

It sits comfortably between them, with up to 4 units of slack at scale 5. Note $S_1 = 1$ at every
corner is *forced* (given (CIO-$j$), hence `sketch`): $T(1) = 1 \le S_1 \le N(1^-) = 1$, since a
triangle of side $< 1$ has diameter $< 1$. So exactly one point lies within corner distance 1 of
each corner — the one crisp rigidity these constraints do produce, and it is not enough to seed
anything.

**Why this is not an Erdős–Oler counterexample, and why it never could be.** It is a *count
profile*, not a configuration. The relaxation constrains how many points lie in each convex
corner-coordinate box, and nothing else. It has no way to express that a point in one cell and a
point in an adjacent cell must themselves be $\ge 1$ apart, except in the special case where the
union of the two cells happens to be another box. That is exactly the information Erdős–Oler
turns on, and it is exactly what the $k = 4$, $5$, $6$ controls show is missing: at those $k$ the
identical profiles exist and no configuration realises them.

**The scale-invariance that dooms the corner constraints specifically.** Take the lattice $T(k)$
at side $k-1$, delete a point, and shrink by $a/(k-1) < 1$. The result satisfies **every**
(CIO-$j$) with slack $\ge j$, lies in $T_a$ with $a < k-1$, and has separation $a/(k-1) \to 1^-$.
So for every $\epsilon > 0$ there is a $T(k)-1$ point set in $T_a$, $a < k-1$, with separation
$\ge 1-\epsilon$ satisfying every corner constraint. The corner constraints are insensitive to the
last $\epsilon$ of separation, and the last $\epsilon$ is the entire conjecture. (This
configuration violates the *capacity* constraints — that is why the relaxation is not trivially
feasible, and why §5 needed to be computed rather than argued.)

---

## 7. Honest accounting

**The single step I am least sure of** is the completeness of the box family in §5.1 — i.e.
whether "every corner-coordinate box" is really the strongest capacity family available at this
granularity. It is not: the thresholds are integers, and a finer partition (half-integer
thresholds, or non-box convex regions) would give strictly more constraints and could in principle
be infeasible where mine is feasible. So §5 refutes **this** relaxation, and by extension the
"count the corners" idea it formalises; it does not refute all partition schemes, which the
manager's retraction rightly reopened. What it does establish is that *corner occupancy is not the
lever*: the $k=4,5$ controls fail for the relaxation as a whole, and (C-$j$) is the only part of
it that is about corners.

**Next after that:** the $N(j^-)$ table. $N(5^-) = 19$ rests on $d(20) = 5$, the Payan row this
repo qualifies. Every conclusion above survives without it, because $k = 4$ and $k = 5$ carry the
no-go on their own, but a reader reusing the capacities should know which entry is soft.

**Dependencies, per `RULES.md` §3.** §2 depends on Oler (`cited`) and is `sketch`. §3 depends on
nothing but the separation hypothesis and elementary geometry — no Oler, no CIO — and is `sketch`
because it is my own derivation. §4 depends on §2 for the $C(k)$ column only; the $V(k)$ column is
Viviani plus integrality. §5's *no-go* depends on the cited $d(n)$ table and on Erdős–Oler being
true at $k = 4, 5$ (`cited`) — and, as noted in §5.3, **not** on §2 being true.

**Novelty: UNVERIFIED, and I would assume not.** Lemma P is a projection argument that anyone who
has drawn the picture would find; the fact that it is exactly break-even against the lattice is
the kind of remark a paper on this conjecture would make in its first section. The prior art to
check remains Payan (1997), whose body this repo has never obtained, and Folkman–Graham. **Assume
§§3–4 are known until someone with library access says otherwise.**

**What is not claimed.** Nothing here bounds $s(n)$ for any $n$. Erdős–Oler is untouched, at
$k = 7$ and everywhere else. §5 is a statement about what a class of arguments *cannot* do, which
is the only kind of positive result this attack produced.

**Not checked.** The $\tau = 1$ tightening at $k = 6$ and $k = 7$ (§5.4) — killed inside the
compute budget, since proving infeasibility costs far more than exhibiting a witness; reported as
unknown rather than as agreeing with $k = 4, 5$. Whether a finer (sub-integer) partition of the
corner-coordinate space is infeasible at $k = 4$ — that is the natural next question and it is a different attack, not a
re-scoping of this one. Whether the $S_1^{(V)} = 1$ rigidity can be propagated outward by a
*geometric* argument rather than a counting one. Whether the witness profiles of §6 are
individually unrealisable, and if so by what obstruction — an answer there would name the missing
ingredient precisely, and by the $k = 4$ control it must be an obstruction that already bites at
$n = 9$.

**Next agent on this route: don't take this route.** The corner counts are exhausted. The live
questions this attack leaves are (i) sub-integer partitions with true capacities, per the
manager's retraction, and (ii) the stability question [`../eo-hull-deficit/`](../eo-hull-deficit/)
§10 already names. Both are about geometry, not about counting corners.
