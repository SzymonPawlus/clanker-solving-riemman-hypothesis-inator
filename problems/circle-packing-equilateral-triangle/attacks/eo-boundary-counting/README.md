# Attack: the Erdős–Oler boundary count — which version is true, and why it still cannot be used

**Claim type: neither.** No bound on $s(n)$, upper or lower, is claimed anywhere in this file
(problem [`../../RULES.md`](../../RULES.md) §1 asks for that sentence first). What is here is one
proved-and-sharp counting lemma, one structural impossibility theorem, exact refutations of two
hypotheses (including one that this attack itself proposed), and a precise statement of the window
that Erdős–Oler $k = 7$ actually lives in. Nothing enters `results/`; nothing here is assumable,
including by me (repo [`RULES.md`](../../../../RULES.md) §3).

- Code: [`experiments/packing-eo-boundary/`](../../../../experiments/packing-eo-boundary/) — one
  command, Python standard library only, exact arithmetic for every decision
- Transcript: [`out/report.txt`](../../../../experiments/packing-eo-boundary/out/report.txt)
- Journal: [`notebook/claude/2026-08-21-eo-boundary-counting.md`](../../../../notebook/claude/2026-08-21-eo-boundary-counting.md)
- Predecessor: [`../oler-slack-analysis/`](../oler-slack-analysis/) — refuted step (i) of this
  route and flagged step (ii); this file settles step (ii)
- Author: `claude` (Claude Opus 5 — convergent role, `RULES.md` §8: exact calculation and
  checking, not ideation), 2026-08-21

## Status table

| What | Status |
|---|---|
| **P1** $\;\lvert E \cap \partial T\rvert \le 3\lfloor a\rfloor$, and it is attained | `sketch` (proof below); the attaining family is `numerical`, exactly verified |
| **P2** $\;b \le \sum_{\text{hull edges}}\lfloor p_i\rfloor \le \lfloor 3a\rfloor$, $= 3\lfloor a\rfloor$ when $\{a\} < 1/3$ or the hull is a triangle | `sketch` |
| **P3** $\;b \le 3\lfloor a\rfloor$ in general | `numerical` — local search only, **not proved**, not assumable |
| **T1** no function $\Phi$ of the boundary count can carry Oler's boundary term | `sketch` (proof below), with exact witnesses |
| **W1** hypothesis H fails *at the extremal lattice*, not only on degenerate sets | `refuted` — exact witnesses, independent of T1 |
| **Lemma C** corner clearance $\Rightarrow$ quantified Oler gain | `sketch` |
| **C1** one corner clear of $E$ at reach $1$ $\Rightarrow$ the $k$ case follows | `sketch` — depends on Lemma C, so capped there |
| **O1** the $k = 7$ open window is $a \in [\,(-3+\sqrt{217})/2,\ 6)$ | `sketch` (arithmetic on top of `cited` Oler) |
| Oler's inequality itself | `cited` — Oler 1961, see [`../oler-lower-bound/`](../oler-lower-bound/) |

**Kill-criterion outcome, stated up front** (`RULES.md` §6.3). Three were written down before the
deciding computations (journal, "Kill-criteria"); two fired.

> **KC-1** — *"an exact configuration with more than $3\lfloor a\rfloor$ points on $\partial T$
> refutes P1."* **Not met.** No such configuration was found and P1 is proved below.
>
> **KC-2** — *"if $b$ collapses under an $\varepsilon$-perturbation at near-extremal
> configurations, the count-based route is dead regardless of how good the bound on $b$ is; record
> that and do not look for a restricted H′."* **MET — §4.** $b$ drops from $3(k-1)$ to $3$ at the
> triangular lattice itself, with $n$ and $a$ unchanged to $O(\varepsilon)$.
>
> **KC-3** — *"if validity of any $\Phi(b)$ forces the result to be weaker than Oler near the
> lattice, the family is dead; do not re-scope to $\Phi(n,b)$ and call it a boundary count."*
> **MET, and worse than anticipated — §5.** No $\Phi$ exists at all.

**What to review hardest**, if you are the cross-examiner: the big-leg assignment step in §3's
proof of P1 (the inequality $\gamma_i \ge n_i$ and the empty-side case analysis), and the claim in
§4 that the perturbed lattice really has $b = 3$ — that is the load-bearing fact for both T1 and
the conclusion of this attack. Both are exactly checked in code, but the *proof* of P1 is prose.

**Normalisation.** Separation $1$, triangle side $a$; $T$ is the closed equilateral triangle,
$E \subseteq T$ finite with pairwise distances $\ge 1$, $P = \operatorname{conv}(E)$, $n = |E|$,
$M(\cdot)$ perimeter, $A(\cdot)$ area. The repo's certificates use separation $2$ and side
$d = 2a$; nothing here reads them, so there is nothing to convert.

---

## 1. What was asked, and what turned out to be the case

[`../oler-slack-analysis/`](../oler-slack-analysis/) §4 records a two-step route to the
floored-perimeter statement $n \le \frac{a^2}{2} + \frac32\lfloor a\rfloor + 1$:

1. **Hypothesis H**: $n \le \frac{2}{\sqrt3}A(P) + \frac b2 + 1$, i.e. Oler's boundary term
   *counted* instead of *measured*. **Refuted there** by flat near-collinear arcs.
2. **Step (ii)**: $b \le 3\lfloor a\rfloor$, "since a side of length $a$ carries at most
   $\lfloor a\rfloor + 1$ separated points and the three corners are shared". Recorded there as
   *separately unjustified*, because $b$ counts points on $\partial P$, and a hull vertex can sit
   strictly inside $T$.

The brief for this attack was: find the version of the boundary count that is actually true and
actually usable. The answer is not the one the brief anticipated.

> **Step (ii) is true.** In the reading it should have had — points on $\partial T$ — it is true,
> and sharp for every $a \ge 1$ (§3). In the reading as literally written — points on
> $\partial P$ — it is true up to $\lfloor 3a\rfloor$, it is true outright when $\{a\} < 1/3$ or
> the hull is a triangle, and a search finds no counterexample to the full statement (§3.3).
>
> **And it is useless.** Not because the bound is weak — it is exactly sharp — but because there
> is **no function of $b$ at all** that can stand in Oler's boundary slot (§5). The route dies at
> the composition of its two steps, not at either one taken alone.

That is a more complete kill than "step (ii) is unjustified" would have been: it closes the whole
family of repairs rather than one member of it, so nobody has to come back and try
$\Phi(b) = b/2 + c$, or $b$-on-$\partial T$, or a cleverer floor.

## 2. Where Erdős–Oler $k = 7$ actually lives — `sketch`

Worth pinning down before anything else, because it sizes the target. Oler (`cited`) gives
$n \le \frac{a^2}{2} + \frac{3a}{2} + 1$, so $27$ points force $a^2 + 3a - 52 \ge 0$. Let $a^\*$
be the positive root, $a^\* = \tfrac{-3+\sqrt{217}}{2}$; then

$$\tfrac{(a^\*)^2}{2} + \tfrac{3a^\*}{2} + 1 = \tfrac{(a^\*)^2 + 3a^\* + 2}{2} = \tfrac{52+2}{2} = 27$$

exactly, with no radical arithmetic needed. Certified rational bracket (exact, in code):
$5.865459 < a^\* < 5.865460$.

> **O1.** Oler alone already proves the $k = 7$ case of Erdős–Oler for every $a < a^\*$. The
> entire open window is $a \in [a^\*, 6)$, of width $6 - a^\* < 0.1346$.

**Integrality of $n$ is load-bearing here**, and it is the one place this quantity is easy to get
wrong by a factor of two. Since $n$ is an integer, RHS $< 27$ *already* forces $n \le 26$; one does
not need RHS $< 26$. Both thresholds, exactly (transcript §1):

| $k$ | $T(k)$ | $n = T(k)-1$ | $a$ with RHS $= n$ — **the window** | gap to $k-1$ | $a$ with RHS $= n-1$ | gap if integrality is not used |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 6 | 5 | 1.701562 | **0.298438** | 1.372281 | 0.627719 |
| 4 | 10 | 9 | 2.772002 | **0.227998** | 2.531129 | 0.468871 |
| 6 | 21 | 20 | 4.844289 | **0.155711** | 4.684658 | 0.315342 |
| 7 | 28 | 27 | 5.865460 | **0.134540** | 5.728416 | 0.271584 |

Both columns are in **separation-1, $a$ = side of the point triangle** units; neither is a
separation-1/separation-2 slip. The right-hand column is what one gets by asking Oler's real-valued
RHS to reach $T(k)-2$ rather than to drop below $T(k)-1$; the bolded column is the actual set of
$a$ at which $T(k)-1$ points are not excluded. **The bolded one is the open window.** Everything in
the table is an exact rational computation performed here.

> **Provenance of the two columns, recorded rather than overwritten.** A coordination message from
> the manager supplied the values $0.628 / 0.469 / 0.315 / 0.272$ as the true gaps and stated that
> the values $0.298 \to 0.135$ (which are the bolded column) were a separation-1/separation-2 slip
> by another worker. **Those supplied values are wrong and are not used anywhere in this attack.**
> They were kept in this table only because reproducing them exactly is what identifies the cause:
> they are the root of $\mathrm{RHS}(a) = T(k)-2$ rather than of $\mathrm{RHS}(a) = T(k)-1$, i.e.
> they omit the integrality of $n$. The manager has since retracted them and independently reached
> the same diagnosis; the other worker's figures were right throughout. Nothing here was derived
> from the supplied numbers — §2 was computed from Oler's inequality directly, before the message
> arrived, which is why the two columns could be reconciled at all.

Also verified exactly for $k = 2,\dots,14$: **Oler's RHS at $a = k-1$ is exactly $T(k)$**. So the
gain Erdős–Oler needs is exactly **one point**, independent of $k$: at any $a < k-1$ the RHS is
already $< T(k)$, so a gain of $1$ suffices to reach $\le T(k)-2$. The side-length window shrinks
with $k$ while the required gain does not — which is why progress on this problem must be counted
in points, never in side length.

## 3. The boundary count that is true

### 3.1 P1: points on $\partial T$ — `sketch`

> **Lemma P1.** Let $a \ge 1$ and let $E \subseteq T$ have pairwise distances $\ge 1$. Then
> $$\lvert E \cap \partial T\rvert \;\le\; 3\lfloor a\rfloor .$$

Write $k = \lfloor a \rfloor \ge 1$. Label the corners $A_1, A_2, A_3$ and let side $i$ be the
closed segment $A_iA_{i+1}$ (indices mod 3). Let $m_i = \lvert E \cap \text{side } i\rvert$, let
$s$ be the number of corners lying in $E$, and let $B = \lvert E\cap\partial T\rvert$. A point of
$E$ on $\partial T$ lies on two sides exactly when it is a corner, so

$$B \;=\; \textstyle\sum_i m_i - s. \tag{1}$$

**Per-side bound.** Suppose side $i$ is non-empty. Let $\alpha_i$ be the distance from $A_i$ to
the nearest point of $E$ on side $i$, and $\beta_i$ the distance from $A_{i+1}$ to the nearest such
point; put $\gamma_i = \alpha_i + \beta_i$. The $m_i$ points lie in a sub-segment of length
$a - \gamma_i$ and are pairwise $\ge 1$ apart along it, so $m_i - 1 \le a - \gamma_i$, and since
$m_i - 1$ is an integer,

$$m_i \;\le\; 1 + \lfloor a - \gamma_i\rfloor. \tag{2}$$

**Corner bound.** Let $A_j \notin E$ and suppose both sides meeting at $A_j$ are non-empty. Let
$x = \beta_{j-1}$ and $y = \alpha_j$ be the two legs at that corner, both $> 0$; the two
corresponding points of $E$ subtend a $60^\circ$ angle at $A_j$, so their distance satisfies
$x^2 - xy + y^2 \ge 1$. If $0 \le y \le x$ then $x^2 - xy + y^2 = x^2 - y(x-y) \le x^2$; hence

$$\max(x, y) \;\ge\; 1. \tag{3}$$

**Assignment.** Call such a corner *chargeable*, and charge it to one adjacent side carrying a leg
$\ge 1$ (possible by (3)). Let $n_i \in \{0,1,2\}$ be the number of corners charged to side $i$.
Side $i$ has only two legs, both non-negative, and the $n_i$ charged ones are each $\ge 1$, so
$\gamma_i \ge n_i$; as $n_i$ is an integer, $\lfloor a - \gamma_i\rfloor \le \lfloor a\rfloor - n_i$.
With (2),

$$m_i \;\le\; 1 + k - n_i \qquad \text{for every non-empty side } i. \tag{4}$$

**Case $z' = 3$ (no empty side).** Every unoccupied corner is chargeable, so
$\sum_i n_i = 3 - s$. Summing (4) and using (1),
$B \le 3 + 3k - (3-s) - s = 3k$. $\;\square$

**Empty sides.** If $z'$ sides are non-empty, only corners with both adjacent sides non-empty are
chargeable; let $u'$ be their number. Summing (4) over non-empty sides,
$B \le z'(1+k) - u' - s$.
- $z' = 2$: the one corner between the two non-empty sides is either occupied ($s \ge 1$, $u' = 0$)
  or chargeable ($u' = 1$); either way $B \le 2 + 2k - 1 = 2k+1 \le 3k$ for $k \ge 1$.
- $z' = 1$: $B \le 1 + k \le 3k$ for $k \ge 1$.
- $z' = 0$: $B = 0$.

The hypothesis $a \ge 1$ is needed and sharp: for $a < 1$ the triangle has diameter $< 1$, so
$B \le 1 > 0 = 3\lfloor a\rfloor$.

### 3.2 P1 is sharp for every $a \ge 1$ — `numerical`

On each side put points at arc-distances $0, 1, \dots, k-1$ from that side's first corner; the
next corner is the position-$0$ point of the next side. That is $3k$ distinct points. Within a
side the gaps are $1, \dots, 1, a-k+1 \ge 1$; across an occupied corner the two legs are $a-k+1$
and $1$, and $(a-k+1)^2 - (a-k+1) + 1 \ge 1$ because $a - k + 1 \ge 1$.

Verified exactly (§2 of the transcript) for $a = 1, \tfrac32, 2, \tfrac52, 3, \tfrac{17}{4}, 5,
\tfrac{59}{10}, 6$: separation, containment, boundary incidence and the count $3\lfloor a\rfloor$,
all in $\mathbb{Q}(\sqrt3)$ with no floating point. So **the floor in P1 is real**, not an artefact
of the proof — at $a = 5.9$ the answer is $15$, not $17 = \lfloor 3a\rfloor$.

Every point of this family is also a hull-boundary point, so it shows $b = 3\lfloor a\rfloor$ is
attained in the hull reading too.

### 3.3 P2/P3: points on $\partial P$ — `sketch` / `numerical`

> **Lemma P2.** With $p_1,\dots,p_V$ the edge lengths of the hull $P$,
> $$b \;\le\; \sum_{i=1}^{V} \lfloor p_i \rfloor \;\le\; \lfloor 3a\rfloor \;=\; 3\lfloor a\rfloor + \lfloor 3\{a\}\rfloor,$$
> and $b \le 3\lfloor a\rfloor$ whenever $\{a\} < 1/3$, and whenever $V \le 3$.

*Proof.* Every hull vertex is a point of $E$. The points of $E$ on the closed edge $i$ number
$m_i \le \lfloor p_i\rfloor + 1$ (separation along a segment of length $p_i$), and summing over
edges double-counts each of the $V$ vertices, so $b = \sum m_i - V \le \sum \lfloor p_i\rfloor$.
Then $\sum\lfloor p_i\rfloor \le \lfloor \sum p_i\rfloor = \lfloor M(P)\rfloor \le \lfloor 3a\rfloor$,
using $M(P)\le M(T)$ for nested convex sets. Finally $p_i \le \operatorname{diam}(T) = a$ gives
$\lfloor p_i\rfloor \le \lfloor a\rfloor$, so $V \le 3$ already yields $3\lfloor a\rfloor$. $\square$

> **P3 (conjecture, `numerical`, not assumable).** $b \le 3\lfloor a\rfloor$ for all $a \ge 1$.

Equivalently $a_{\mathrm{conv}}(b) \ge \lceil b/3\rceil$, where $a_{\mathrm{conv}}(b)$ is the least
side of an equilateral triangle holding $b$ points in convex position at separation $1$. A
float multistart search (transcript §3b; search only, no decision taken in floating point) gives

| $b$ | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| $a_{\mathrm{conv}}$ found | 1.000 | 2.001 | 2.004 | 2.019 | 3.008 | 3.156 | 3.214 | 4.108 |
| $\lceil b/3\rceil$ | 1 | 2 | 2 | 2 | 3 | 3 | 3 | 4 |

consistent throughout, and *tight* at $b \equiv 1 \pmod 3$. **This is evidence, not a proof**; the
gap between P2 and P3 is exactly the two extra points $\lfloor 3\{a\}\rfloor$ can allow when
$\{a\} \ge 1/3$, and closing it needs a statement about convex polygons in $T$ with near-integer
edge lengths that I do not have. It is also, per §5, not worth having.

## 4. W1: hypothesis H fails at the extremal lattice — `refuted`

The published refutation of H uses flat, near-collinear sets. That invites the repair *"H is
presumably fine for fat, lattice-like configurations, which is all Erdős–Oler needs."* It is not.

**Construction.** Take the triangular lattice $T(k)$ at separation $1$ (side $k-1$) — the
configuration where Oler is *exactly tight*. Scale it by $\lambda = 1 + \delta$, then push every
point that lies on the boundary strictly inside: edge points along the inward normal by
$\varepsilon$, corner points along the inward bisector by $\varepsilon$. A corner moves inward
perpendicular to each of its two sides by only $\varepsilon\sin 30^\circ = \varepsilon/2$, while
the edge points move by $\varepsilon$, so the edge points end up **strictly inside** the triangle
spanned by the three moved corners. With $\lambda = 101/100$, $\varepsilon = 1/1000$, exactly
verified:

| $k$ | $n$ | $a$ | $b$ before | $b$ after | $\min\text{sep}^2$ | H's RHS | H holds | violation |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 6 | 2.0200 | 6 | 3 | 1.016604 | 4.5367 | **False** | $+1.4633$ |
| 4 | 10 | 3.0300 | 9 | 3 | 1.016604 | 7.0852 | **False** | $+2.9148$ |
| 5 | 15 | 4.0400 | 12 | 3 | 1.016604 | 10.6538 | **False** | $+4.3462$ |
| 6 | 21 | 5.0500 | 15 | 3 | 1.016604 | 15.2425 | **False** | $+5.7575$ |
| 7 | 28 | 6.0600 | 18 | 3 | 1.016604 | 20.8513 | **False** | $+7.1487$ |

Separation, containment, the convex hull, the hull-boundary count and the area are all computed
exactly in $\mathbb{Q}(\sqrt3)$; the comparison in the "H holds" column is an exact sign test.

**KC-2 fired.** The diagnosis is one line: $b$ is *not stable* under a perturbation that changes
neither $n$ nor $a$ to leading order, and it appears on the **larger** side of H. So a bound on $b$
— even the exactly sharp P1/P3 — cannot rescue anything of H's shape. This is what the brief's
"boundary, counted rather than measured" was really up against.

Per KC-2 I stopped here rather than looking for a restricted H′ (say, "H holds when $\operatorname{conv}(E) = T$
and all three corners are occupied"); the perturbation above applies to any such restriction that
is stated in terms of incidences, because incidences are what the perturbation destroys.

## 5. T1: there is no count-based boundary term at all — `sketch`

> **Theorem T1.** There is **no** function $\Phi$ for which
> $$n \;\le\; \tfrac{2}{\sqrt3}A(\operatorname{conv}E) \;+\; \Phi(b) \;+\; 1$$
> holds for every finite unit-separated $E$. The same holds with $A(T)$ in place of
> $A(\operatorname{conv}E)$, $T$ any triangle containing $E$.

*Proof.* Apply the §4 family. It has $b = 3$ for every $k$, its hull is a triangle of side
$\to k-1$, so $\frac{2}{\sqrt3}A(\operatorname{conv} E) \to \frac{(k-1)^2}{2}$ while
$n = T(k) = \frac{k^2+k}{2}$. Hence

$$\Phi(3) \;\ge\; n - \tfrac{2}{\sqrt3}A - 1 \;\longrightarrow\; \tfrac{k^2+k}{2} - \tfrac{(k-1)^2}{2} - 1 \;=\; \tfrac{3k-3}{2},$$

unbounded in $k$, while the argument of $\Phi$ stays $3$. $\square$

Exactly computed lower bounds on $\Phi(3)$ (transcript §5): $2.963, 4.415, 5.846, 7.257, 8.649,
10.020, 11.371$ for $k = 3,\dots,9$ — increasing, and matching $\frac{3k-3}{2}$ up to the
$O(\delta,\varepsilon)$ of the construction.

Two independent corroborations, kept because they fail in the *opposite* regime and so make the
conclusion robust to an error in the §4 construction:

- **Flat arcs** ($p_j = (j, \eta\,j(m-j))$, exactly verified separation, all in convex position,
  area $\to 0$) force $\Phi(b) \ge b - 1$ for every $b$: here the *area* term degenerates rather
  than the count.
- **The lattice** has $M(P) = b$ exactly (every hull boundary edge has length exactly $1$), so
  even granting $\Phi(b) = b-1$, the resulting boundary term $b$ exceeds Oler's own
  $\frac{M(P)}2 + 1$ for all $b > 2$ — a count bound is strictly *weaker* than Oler precisely at
  the extremal configurations.

**KC-3 fired**, and more sharply than it was written: the obstruction is not a bad choice of
$\Phi$, it is that no $\Phi$ exists.

**Honest scope of T1.** It is about a term depending on $b$ alone. A term $\Phi(n, b)$ is *not*
excluded by this argument — but such a term is no longer a boundary count, it is a
re-parametrisation of the inequality, and the §4 family constrains it too ($\Phi(T(k), 3) \ge
\frac{3k-3}{2}$). Also untouched: bounds using $b$ together with *metric* data. That is exactly
what Oler already does, with $M(P)$.

## 6. What survives: measure the corners, do not count them — `sketch`

The failure mode in §4 is instability of an incidence count. The repair is to use a quantity that
moves continuously, and the corner clearance is the natural one.

For corner $A_i$ let $\hat w_i$ be the inward unit bisector and
$u_i = \tfrac{2}{\sqrt3}\min_{p\in E}\langle p - A_i,\ \hat w_i\rangle \ge 0$. Cutting the
$60^\circ$ corner perpendicular to the bisector at bisector-height $\tfrac{\sqrt3}{2}u_i$ removes
an equilateral triangle of side $u_i$: area $\tfrac{\sqrt3}{4}u_i^2$, perimeter change
$-2u_i + u_i = -u_i$. By construction $P$ lies in the complementary half-plane.

> **Lemma C.** If the three cuts are pairwise disjoint (equivalently $u_i + u_j \le a$ for $i\ne j$),
> then
> $$n \;\le\; \tfrac{a^2}{2} + \tfrac{3a}{2} + 1 \;-\; \sum_{i=1}^{3}\tfrac{u_i^2 + u_i}{2}.$$
> If instead $u_i + u_j > a$ for some pair, then $\max(u_i,u_j) > a/2$ and using that single cut
> alone gives a gain of at least $\tfrac{a^2}{8} + \tfrac{a}{4}$.

*Proof.* $P \subseteq T'$, the hexagon $T$ minus the three disjoint cuts, so $A(P) \le A(T')$ and
$M(P) \le M(T')$ (perimeter is monotone under inclusion of convex sets). Feed
$A(T') = \tfrac{\sqrt3}{4}a^2 - \sum\tfrac{\sqrt3}{4}u_i^2$ and $M(T') = 3a - \sum u_i$ into
Oler. $\square$

If every point of $E$ is at distance $\ge t_i$ from $A_i$ then $u_i \ge t_i$, because a point of
$T$ makes an angle $\le 30^\circ$ with the bisector at $A_i$, so
$\langle p - A_i, \hat w_i\rangle \ge |p-A_i|\cos 30^\circ$.

**What this would need for $k = 7$, exactly.** §2 says the missing gain at $a \to 6^-$ is $1$. With
a common clearance $t$ that is $3(t^2+t)/2 \ge 1$, i.e.

$$t \;\ge\; t_7 \;=\; \tfrac{-3+\sqrt{33}}{6}, \qquad 0.457427 < t_7 < 0.457428$$

(exact bracket; $t_7$ is characterised by $t^2 + t = \tfrac23$). For $a \ge 2$ the second branch of
Lemma C gives a gain $\ge \tfrac{a^2}{8}+\tfrac a4 \ge 1$ outright, so the dichotomy is clean.

**One corner is enough, and the threshold does not depend on $k$.** The gain is a *sum* over
corners, so it does not need to be shared out:

> **Corollary C1** (`sketch`; depends on Lemma C `sketch` and Oler `cited` — **not assumable**).
> If some corner $A_i$ of $T$ has $u_i \ge 1$ — in particular if **no point of $E$ lies within
> distance $1$ of that corner** — then $T(k)-1$ points cannot fit in $T$ with $a < k-1$.
> Equivalently: Erdős–Oler for any $k$ reduces to configurations that have a point within reach $1$
> of *every* corner.

*Proof.* A single cut needs no disjointness hypothesis, and $u_i \ge 1$ gives gain
$\tfrac{u_i^2+u_i}{2} \ge 1$. For $a < k-1$ Oler's RHS is $< T(k)$, so $n < T(k)-1$, so
$n \le T(k)-2$. $\square$ (Arithmetic checked exactly for $k = 3,\dots,14$, transcript §6.)

This has exactly the signature a usable mechanism must have: a **$k$-independent constant $\ge 1$**,
supplied by the **three corners**, of which there are always three whatever $k$ is. It is the only
thing in this attack with that signature.

**And this is exactly where it stops.** The lattice $T(7)$ has points *at* the corners: $t = 0$,
gain $0$. Lemma C is a genuine inequality and it is stable, but it is vacuous on the only
configurations that matter unless it is paired with a statement forcing small clearance to imply
near-lattice structure. That pairing is **approach O** (quantitative Oler stability) in
[`../approaches-round-2/`](../approaches-round-2/), not this attack, and I am not starting it here.

## 7. What the unbounded-negative face excess rules out for discharging

The brief's third direction was a discharging scheme on the triangulation. The predecessor
attack's §1 already contains the fact that kills the naive version, and it is worth stating as a
constraint rather than leaving it implicit:

- The **total** face excess equals $\tfrac{2}{\sqrt3}A(P) - \tfrac{2n-b-2}{2}$ and the **total**
  boundary-edge excess equals $\tfrac12(M(P)-b)$. Both are functions of $(A(P), M(P), n, b)$ only.
  *No choice of triangulation changes either total.*
- Therefore a discharging scheme whose rules move charge between faces and boundary edges cannot
  change what is being proved: it can only redistribute two fixed totals. It can be a *proof
  technique* for a statement about those totals, never a route to a different statement.
- Since the total face excess is unbounded below (flat arcs) while $b$ stays equal to $n$, any
  discharging rule that discharges *to boundary edges by count* is bounded above by $b/2$ worth of
  charge and cannot cover an unbounded deficit. Discharging must reach the boundary **edge
  lengths**, i.e. it must be metric, not combinatorial.

Concretely: this rules out any rule of the form "each interior face sends $c$ to each incident
boundary edge, each boundary edge absorbs at most $f(\text{degree})$", and every variant whose
final accounting is a function of the combinatorial data $(n, b, F)$ alone. It does *not* rule out
a metric discharging scheme in which a boundary edge's capacity depends on $\ell_e$ — but that is
Oler's own proof, which is where these totals came from.

## 8. Against the mid-flight constraints from coordination

Three constraints reached me while this was in flight. Each is addressed, and one of them I have
to correct.

**(i) "Judge progress in points, never in side length; the required gain is one point, for every
$k$."** Agreed, verified exactly for $k = 2,\dots,14$, and folded into §2. My §6 threshold is
stated in points for exactly this reason: Corollary C1 asks for a gain of $1$ and gets it from a
single corner, with a constant that does not move with $k$.

**(ii) "A counting bound over independent regions cannot exceed $T(k)-1$; the load-bearing part
must be the coupling between regions."** Consistent with everything here, and §5 and §7 are the
same statement seen from two other sides:

- §5 (T1) says the failure is not that per-region counts are too weak but that **no function of a
  count occupies Oler's boundary slot at all** — an aggregation of counts has nothing to aggregate
  *into*.
- §7 says a discharging scheme can only redistribute two totals that are already fixed by
  $(A, M, n, b)$, so a scheme that couples regions **combinatorially** buys nothing either; the
  coupling has to be metric.

So I did not run the strip/row decomposition (direction 2 of my brief), which is approach N's
mechanism and is covered by the cap. P1 is *not* such a scheme: it is a sharp count of a
sub-population, not a capacity table summed to bound $n$, and it is not offered as a route to a
bound on $n$ — §5 is precisely the argument that it cannot be.

**(iii) "The honest boundary bound is $b \le \lfloor 3a\rfloor$; repair the step knowing that."**
This one I have to push back on — for the $\partial T$ reading — and it is checkable in one line.
(This item did not come from the arithmetic the manager later retracted; it stands on its own and
is addressed on its own.)

$\lfloor 3a\rfloor$ is what the arc-length argument gives (consecutive boundary points have
arc-separation $\ge$ chord $\ge 1$ around a closed curve of length $M(H) \le 3a$), and that
argument is correct. But it is **not attainable**, so it is not the honest bound. For points on
$\partial T$ the truth is $3\lfloor a\rfloor$ — proved in §3.1 and attained for every $a \ge 1$
in §3.2. Concretely at $a = 5.9$:

| | arc-length bound $\lfloor 3a\rfloor$ | truth (P1, attained) |
|---|---:|---:|
| $\lvert E \cap \partial T\rvert$ at $a = 5.9$ | 17 | **15** |

The two extra points the arc-length bound allows cannot be realised, because a $60^\circ$ corner
forces one of its two adjacent legs to be $\ge 1$ (§3.1, inequality (3)) and that charge is what
converts $\lfloor 3a \rfloor$ into $3\lfloor a\rfloor$. For the hull reading the arc-length bound
is currently the best *proved* one (P2), but a search finds nothing above $3\lfloor a\rfloor$
there either (P3).

In the **hull** reading $\lfloor 3a\rfloor$ remains the best bound I can prove (P2), so the
message is right there and my disagreement is confined to $\partial T$ — but P3 says even that is
probably not tight.

The correction does not rescue the route — §5 kills it whatever the bound is — but the record
should say $3\lfloor a\rfloor$ rather than $\lfloor 3a\rfloor$, because a future attack that reads
"$\lfloor 3a\rfloor$ is the honest bound" will conclude the floored-perimeter step is
*unreachable*, when in fact it is reachable and merely useless. Those are different failure
diagnoses and only one of them is true.

## 9. Duplication check (`RULES.md` §6.1)

Checked against [`../candidate-approaches/`](../candidate-approaches/) (A–H) and
[`../approaches-round-2/`](../approaches-round-2/) (I–O):

- **F (vacancy-corrected Oler)** conjectures an analytic correction term shaped by vacancy
  structure. T1 is a *negative* result about a different slot — the boundary term, not an additive
  vacancy correction — and it constrains F: whatever F's correction is, it may not be a function of
  the boundary count.
- **N (strip counting)** was proposed, tried and dropped in round 2. My brief's route 2 (horizontal
  strips of height $\sqrt3/2$) is N's mechanism — a 1-D projection capacity per strip — and I did
  **not** re-run it. P1 is a different object: an exact, sharp count on $\partial T$, proved rather
  than searched, and it is not a capacity argument.
- **O ($\Delta(k)+1$ stability)** is where §6 hands off, deliberately and without duplicating its
  literature list.
- **B/L/M (partition, pigeonhole ceiling, capacity aggregation)** are per-$n$ computational
  certificates; nothing here overlaps them.
- Nothing in A–H or I–O contains P1, P2, T1 or Lemma C.

## 10. Honest accounting

**The step I am least sure of.** The empty-side case analysis in P1's proof (§3.1). The main case
$z' = 3$ I have re-derived twice and it is exactly corroborated by the search in transcript §3;
the degenerate cases are routine but they are prose, unchecked by anything, and they are exactly
where an "obviously" would hide an error. Second least sure: the assertion in Lemma C that the
three corner cuts are the only loss, i.e. that $A(P) \le A(T')$ and $M(P) \le M(T')$ with $T'$ the
hexagon — the perimeter monotonicity is standard but I have not verified the disjointness
bookkeeping on an example.

**Third least sure, and it is the one a reader will most want to be true: Corollary C1.** It is
short, it has the right shape, and short arguments with the right shape are exactly what
`RULES.md` §0 warns about. It rests entirely on Lemma C, whose disjointness bookkeeping is the
item above; C1 uses only the single-cut branch, which is the part that needs no disjointness, so I
believe it — but "this appears to show" is the correct verb, and it is `sketch` and not assumable.
Note what it is *not*: it is a reduction, not a proof of any case of Erdős–Oler, and the
configurations it removes are exactly the ones that were never the difficulty.

**Not proved.** P3 (the full hull-reading bound). It is `numerical` and it is *not* assumable,
including by me.

**Novelty: UNVERIFIED.** P1 is elementary and is plausibly folklore in the Oler/Folkman–Graham
line; T1 is a negative result of the kind that usually goes unpublished because nobody writes down
the failed strengthening. No literature check was performed here at all — that is
verification-critical work under `CLAUDE.md` and belongs to a separate claim with a separate
review. Assume both are known.

**Exactness.** Every decision above — every sign, every comparison producing a conclusion — is an
exact test in $\mathbb{Q}$ or $\mathbb{Q}(\sqrt3)$. The only floating point in the experiment is
inside two *searches* (transcript §3 and §3b), whose outputs are labelled `numerical` and are used
for no decision. No perimeter or length is compared anywhere: the arguments were arranged so that
only areas, squared distances and rational perimeters occur, which removes the need for interval
arithmetic entirely.

**Dependencies (`RULES.md` §3).** §2 (O1) uses Oler's inequality, `cited`. §6 (Lemma C) uses Oler's
inequality, `cited`, plus monotonicity of area and perimeter under inclusion of convex sets
(classical). §3, §4, §5 use nothing but elementary geometry and the definitions — in particular
**none of them depends on the predecessor attack's `sketch` identity**, which is why W1 stands on
its own even if that identity is wrong. §7 quotes the predecessor's §1, which is `sketch`, and is
therefore stated as a constraint on design rather than as a theorem.

**Not checked.** Whether P3 is true. Whether Lemma C composes with anything to close any part of
the $[a^\*, 6)$ window. Whether the $\Phi(n,b)$ variant left open in §5 admits a valid choice.
Whether $a_{\mathrm{conv}}(b) = \lceil b/3\rceil$ exactly at $b \equiv 1 \pmod 3$, which the search
suggests and which would be the natural extremal statement behind P3.
