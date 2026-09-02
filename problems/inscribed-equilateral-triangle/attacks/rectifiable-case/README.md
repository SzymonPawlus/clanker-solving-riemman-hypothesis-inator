# Attack: the rectifiable case — closed, in the affirmative

**regularity budget: rectifiable Jordan + differentiability of the arclength parametrisation at
the one point $t_0$ (equivalently: a unit tangent direction at $O$ in the parametrised sense).**
Drop rectifiability and there is no arclength parametrisation, so the hypothesis cannot even be
*stated*; drop differentiability at $t_0$ and the conclusion is **false** — the $30°$ apexes of a
$30$-$30$-$120$ triangle are exceptional points of a rectifiable curve
([`../../RULES.md`](../../RULES.md) §3.1). Nothing here says anything about a general continuous
Jordan curve, and §8 says exactly where the argument stops.

- **Outcome: (A).** The lane's open question is answered *yes*, with a self-contained proof.
- Author: `claude` (Claude Opus 5), 2026-08-29. Resumed lane — the kill-criterion is a previous
  worker's, written before any computation, and is honoured, not rewritten.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md). Which criteria fired: §9.
- Journal: [`../../../../notebook/claude/2026-08-29-iet-rectifiable.md`](../../../../notebook/claude/2026-08-29-iet-rectifiable.md).
- The question came from [`../rotation-continuity/README.md`](../rotation-continuity/README.md)
  §6.4, which reached it honestly and stopped. That file also contains a **false side-length
  clause** which this lane refutes with an exact witness (§7) — a correction request, since that
  file is not mine to edit.

| § | Statement | Status |
|---|---|---|
| §2 | **Observation R.** $O$ is a vertex of an inscribed equilateral triangle $\iff J \cap R_{60}(J) \supsetneq \{O\}$ | `sketch` — mine, re-derived here; not assumable |
| §3 | **Lemma 0 (no small triangles).** At a cone-confined point, every inscribed equilateral triangle with vertex $O$ has side $\ge \varepsilon$ | `sketch` — mine |
| §3 | The purely local (radius, angle) route of the brief | **`refuted`** — kill-criterion C1 fired, as it predicted |
| §4 | **Lemma 1 (localisation).** $J \cap B(O,\varepsilon) \subseteq \gamma((t_0-\delta,t_0+\delta))$ for some $\varepsilon>0$ | `sketch` — mine; no regularity used |
| §5 | **Lemma 2 (thin annulus count).** Some $\tau<\rho$ has $\#\bigl(J \cap \partial B(O,\tau)\bigr) = 2$ | `sketch` — mine; this is the step that closes the gap |
| §6 | **Lemma 3 (no nesting).** $J \cap R(J) = \{O\} \Rightarrow \Omega \cap R(\Omega) = \emptyset$ | `sketch` — mine, independently re-derived; the same statement is the neighbouring lane's Lemma A |
| §6 | **Theorem T.** Differentiability of $\gamma$ at $t_0$ $\Rightarrow$ $\gamma(t_0)$ is a vertex. Hence $\mathcal{H}^1$-a.e. point of a rectifiable Jordan curve is a vertex | `sketch` — mine; depends on §2, §4, §5, §6 |
| §6.4 | **Corollary.** Outcome (B) is impossible: there is no rectifiable Jordan curve with an exceptional point at which $\gamma$ is differentiable | `sketch` — mine; contrapositive of Theorem T |
| §7 | The side-length clause of `rotation-continuity` Lemma B / Theorem C ("of side $\varepsilon/2$") | **`refuted`** — exact witness, unit square at $(\tfrac12,0)$ |
| §7 | Exact witness data for the unit square and the controls | `numerical` (exact in $\mathbb{Q}(\sqrt3)$, no floating point) |
| §9 | Square non-transfer ([`../../RULES.md`](../../RULES.md) §3.2), run at general angle | `sketch` — checked; the argument does **not** transfer |

**Dependency hygiene.** Every argument below is self-contained and rests only on: the Jordan curve
theorem, planar Lebesgue measure, Lebesgue's theorem that a Lipschitz function of one variable is
differentiable a.e., and an elementary partition inequality proved inline in §5. It uses **nothing**
from [`../rotation-continuity/README.md`](../rotation-continuity/README.md) — its Lemma A is
re-proved here from scratch, because a `sketch` may not rest on a `sketch`, including one from my
own model family ([`../../../../RULES.md`](../../../../RULES.md) §3). It uses **nothing** from the
`cited`\* rows of [`../README.md`](../README.md), which are provisional; Meyerson appears in §10
only as an external consistency check *on* my conclusion, never as an input.

---

## 1. Setting and the exact question

$J \subset \mathbb{R}^2$ is a **rectifiable** Jordan curve of length $L$, and
$\gamma : \mathbb{R}/L\mathbb{Z} \to \mathbb{R}^2$ is its arclength parametrisation: continuous,
injective, $1$-Lipschitz, with $|\gamma'| = 1$ a.e. $\Omega$ is the bounded complementary
component, $E$ the unbounded one; by the Jordan curve theorem
$\partial\Omega = \partial E = J$ and $\overline\Omega = \mathbb{R}^2 \setminus E$.
$R_\alpha$ denotes rotation by $\alpha$ about $O$, and $R = R_{60°}$.

> **(Q)** Let $t_0$ be a parameter at which $\gamma$ is differentiable with $|\gamma'(t_0)| = 1$,
> and $O = \gamma(t_0)$. Must $O$ be a vertex of an equilateral triangle inscribed in $J$?

**Answer: yes** (§6). Because $\gamma$ is $1$-Lipschitz it is differentiable a.e., and because it
is the arclength parametrisation $|\gamma'| = 1$ wherever the derivative exists, off a null set —
so (Q) covers $\mathcal{H}^1$-a.e. point of $J$.

**The hypothesis has teeth** (kill-criterion A3). It is not a restatement of the conclusion: the
$120°$ apex of a $30$-$30$-$120$ triangle *is* a vertex of an inscribed equilateral triangle and
fails the hypothesis, and the $30°$ apexes fail it and are *not* vertices. Nor is it vacuous: it
holds off a null set on every rectifiable curve.

**Standing constants.** Fix $\eta' = \tfrac14$ once and for all. Differentiability at $t_0$ gives
$\delta > 0$ with

$$\bigl|\gamma(s) - O - (s-t_0)u\bigr| \le \tfrac14 |s - t_0| \qquad (|s-t_0| < \delta), \tag{1}$$

where $u = \gamma'(t_0)$, $|u| = 1$. Two consequences used constantly, both immediate from (1) and
from $\gamma$ being $1$-Lipschitz:

$$\tfrac34\,|s-t_0| \;\le\; |\gamma(s) - O| \;\le\; |s - t_0|, \tag{2}$$

and, writing $\theta(s)$ for the angle between $\gamma(s) - O$ and $u$ (or $-u$, whichever is
smaller), the component of $\gamma(s)-O$ perpendicular to $u$ is at most $\tfrac14|s-t_0|$ while
its length is at least $\tfrac34|s-t_0|$, so

$$\sin\theta(s) \le \tfrac13, \qquad\text{i.e.}\qquad \theta(s) \le \arcsin\tfrac13 = 19.47\ldots° \;<\; 30°. \tag{3}$$

Write $D$ for the closed double cone $\{x : \angle(x-O, \pm u) \le \arcsin\tfrac13\}$.

---

## 2. Observation R — the reduction

> **Observation R.** For any $S \subseteq \mathbb{R}^2$ and $O \in S$: some equilateral triangle
> with all vertices in $S$ has $O$ as a vertex $\iff$ $S \cap R_{60}(S) \supsetneq \{O\}$.

**regularity budget: none.** $S$ is used only as a point set.

*Proof.* ($\Leftarrow$) Take $q \in S \cap R(S)$ with $q \ne O$ and put $p = R^{-1}(q) \in S$. A
rotation about $O$ is an isometry fixing $O$, so $|Op| = |Oq| > 0$ and $\angle pOq = 60°$. An
isosceles triangle with apex angle $60°$ has base angles $(180°-60°)/2 = 60°$, hence is
equilateral. It is nondegenerate: the side is $|Oq| > 0$, and $p \ne q$ since $\angle pOq = 60° \ne 0$.
($\Rightarrow$) If $O,A,B$ is equilateral with all vertices in $S$ then $B = R_{+60}(A)$ or
$A = R_{+60}(B)$; in the first case $B \in S \cap R(S)\setminus\{O\}$, in the second $A$ is. $\square$

Note $R(O) = O$, so $O \in J \cap R(J)$ **always**: the whole content is producing a *second*
point ([`../../RULES.md`](../../RULES.md) §2). No limit is taken anywhere in this file, so the
noncollapse obligation is discharged by construction and not by an estimate.

---

## 3. Lemma 0, and the death of the purely local route (`refuted`)

> **Lemma 0.** Suppose $J \cap B(O,\varepsilon) \subseteq D$ for a closed double cone $D$ of
> half-angle $\eta < 30°$ about a line through $O$. Then **every** equilateral triangle inscribed
> in $J$ with a vertex at $O$ has side $\ge \varepsilon$.

*Proof.* Suppose $O,p,q$ is such a triangle of side $r < \varepsilon$. Then $p,q \in J \cap
B(O,\varepsilon) \subseteq D$, so each of $p - O$, $q - O$ makes an angle $\le \eta$ with $+u$ or
with $-u$. Hence $\angle pOq$ is within $2\eta < 60°$ of $0°$ or of $180°$, so it cannot equal
$60°$. $\square$

By (3), Lemma 0 applies at every point satisfying the hypothesis of (Q). Therefore:

> **`refuted`: the local-pair route.** *"At a differentiability point, use the density of $J$ near
> $O$ in the double cone plus a continuity or measure argument in the pair (radius, angle) to
> produce $r$ and $\theta$ with $O + re^{i\theta} \in J$ and $O + re^{i(\theta+60°)} \in J$."*
> This is route (i) of the lane brief and it is **dead**, not merely unproven: for every
> $r < \varepsilon$ no such $\theta$ exists at all. The kill-criterion's §C1 predicted exactly this
> before any computation, and it was right.

That is worth stating positively rather than as a loss. It says the triangle to be found is
necessarily **macroscopic**, which is why every local argument at $O$ must fail, and it tells you
what kind of argument can succeed: one that uses local information about the *interior domain*
and cashes it out globally. §6 is that argument.

Lemma 0 is also the tool that refutes the neighbouring lane's side-length clause (§7).

---

## 4. Lemma 1 — localisation, and the length bound it hands over

> **Lemma 1.** For every $\delta > 0$ there is $\varepsilon > 0$ with
> $J \cap B(O,\varepsilon) \subseteq \gamma\bigl((t_0-\delta,\, t_0+\delta)\bigr)$.

**regularity budget: Jordan only** — injectivity and compactness, no rectifiability, no tangent.

*Proof.* If not, there are $\varepsilon_n \downarrow 0$ and parameters $s_n$ with
$d(s_n, t_0) \ge \delta$ (distance in $\mathbb{R}/L\mathbb{Z}$) and $|\gamma(s_n) - O| < \varepsilon_n$.
The set $\{s : d(s,t_0) \ge \delta\}$ is compact, so a subsequence converges to some $s^*$ with
$d(s^*,t_0) \ge \delta$, and continuity gives $\gamma(s^*) = O = \gamma(t_0)$ — contradicting
injectivity of $\gamma$. $\square$

**This is where the neighbouring lane's "third strand" fear is disarmed, half-way.** Extra strands
of $J$ inside $B(O,\varepsilon)$ are real and are not excluded; but they cannot come from far-away
parameters. Every one of them is $\gamma(s)$ for $s$ near $t_0$, and therefore obeys (1)–(3).

**Corollary 1.1 (a length bound at $O$, from differentiability alone).** Fix $\delta$ as in (1),
take $\varepsilon$ from Lemma 1 and shrink it so that $\varepsilon < \tfrac34\delta$ (this makes
$\tfrac43\rho < \delta$ for every $\rho \le \varepsilon$, so (1)–(3) are available on the whole
parameter window used below). Then for every $\rho \le \varepsilon$,

$$\mathcal{H}^1\bigl(J \cap B(O,\rho)\bigr) \;=\; \bigl|\{\, s : |\gamma(s)-O| < \rho \,\}\bigr| \;\le\; \bigl|\{\, s : \tfrac34|s-t_0| < \rho \,\}\bigr| \;=\; \tfrac83\rho .$$

*Proof.* The first equality is the area formula for the injective arclength parametrisation
($\mathcal{H}^1(\gamma(A)) = |A|$ for measurable $A$); the inequality is Lemma 1 followed by (2). $\square$

Two remarks, because this is the pivotal step and it looks too cheap.

- It gives $\limsup_{\rho\to0}\mathcal{H}^1(J\cap B(O,\rho))/2\rho \le 1$ (send $\eta' \to 0$
  instead of fixing $\tfrac14$), i.e. **upper density $\le 1$ at $O$ — for free**. The lane brief
  suggested reaching for the fact that $\mathcal{H}^1$-a.e. point of a rectifiable curve has linear
  density $1$ (Besicovitch). **That is not needed.** Differentiability at the single point $t_0$,
  plus injectivity, already supplies the bound at that point. This matters for status: no
  unreadable citation enters the proof.
- It is *not* the Besicovitch theorem in disguise. That theorem gives density $1$ at a.e. point of
  an arbitrary $1$-rectifiable **set**, with no parametrisation available; the statement above is
  about a point where a parametrisation is differentiable, and is proved in two lines precisely
  because that hypothesis is much stronger.

Below, only the crude form $|A_\rho| \le \tfrac43\rho$ *per side* is used, where
$A_\rho^{+} = \{s \in (t_0, t_0+\delta) : |\gamma(s) - O| < \rho\} \subseteq (t_0,\, t_0 + \tfrac43\rho]$
by (2), and symmetrically $A_\rho^{-}$. **That is a statement about parameters only**, so the area
formula — the first equality above — is used for the density remark and in Corollary T1, and is
*not* load-bearing for Theorem T. A reviewer who distrusts it can delete it and lose nothing but
the remark.

---

## 5. Lemma 2 — most small circles meet $J$ exactly twice

This is the step that closes the gap. Write $g(s) = |\gamma(s) - O|$, a $1$-Lipschitz function, and
$\sigma = \tfrac43\rho$.

> **Sub-lemma 2a (a partition inequality; elementary, proved here so nothing is cited).** Let
> $h : [a,b] \to \mathbb{R}$ be continuous. Then
> $\int_{\mathbb{R}} \#h^{-1}(y)\, dy \;\le\; \operatorname{Var}_{[a,b]}(h)$.

*Proof.* For $n \ge 1$ split $[a,b]$ into $n$ equal subintervals $I_1,\dots,I_n$ and set
$N_n(y) = \#\{i : y \in [\min_{I_i} h,\ \max_{I_i} h]\}$. Then
$\int_{\mathbb{R}} N_n(y)\,dy = \sum_i \operatorname{osc}_{I_i}(h) \le \sum_i \operatorname{Var}_{I_i}(h) = \operatorname{Var}_{[a,b]}(h)$.
If $h^{-1}(y)$ contains $k$ distinct points then for $n$ large enough they lie in $k$ distinct
subintervals, each of which then has $y$ in its closed range; so $\#h^{-1}(y) \le \liminf_n N_n(y)$
(also when $\#h^{-1}(y) = \infty$, by taking $k$ arbitrary). Fatou finishes. $\square$

> **Lemma 2.** Under the hypothesis of (Q), for every $\rho \le \varepsilon$ there exists
> $\tau \in (0,\rho)$ with $\#\bigl(J \cap \partial B(O,\tau)\bigr) = 2$, the two points lying one
> in each half of the cone $D$.

*Proof.* Let $m^{+}(\tau) = \#\{s \in (t_0, t_0+\delta) : g(s) = \tau\}$ and $m^{-}$ likewise for
$s \in (t_0-\delta, t_0)$. For $\tau \in (0,\rho)$, Lemma 1 says every point of
$J \cap \partial B(O,\tau)$ has a parameter in $(t_0-\delta,t_0+\delta)$, and $g(t_0) = 0 \neq \tau$,
so by injectivity of $\gamma$

$$\#\bigl(J \cap \partial B(O,\tau)\bigr) \;=\; m^{+}(\tau) + m^{-}(\tau).$$

**Each is $\ge 1$.** $g(t_0) = 0$ and $g(t_0+\sigma) \ge \tfrac34\sigma = \rho > \tau$ by (2), so
the intermediate value theorem gives a forward preimage; symmetrically a backward one.

**Each is $1$ for most $\tau$.** By (2) again, every $s \in (t_0,t_0+\delta)$ with $g(s) \le \rho$
satisfies $s - t_0 \le \tfrac43\rho = \sigma$, so all forward preimages of levels in $(0,\rho)$ lie
in $(t_0, t_0+\sigma]$. Applying Sub-lemma 2a to $g$ on $[t_0, t_0+\sigma]$, whose variation is at
most $\sigma$ because $g$ is $1$-Lipschitz,

$$\int_0^{\rho} m^{+}(\tau)\, d\tau \;\le\; \operatorname{Var}_{[t_0,\,t_0+\sigma]}(g) \;\le\; \sigma \;=\; \tfrac43\rho,$$

and since $m^{+} \ge 1$ on $(0,\rho)$,
$\bigl|\{\tau \in (0,\rho) : m^{+}(\tau) \ge 2\}\bigr| \le \int_0^\rho (m^+ - 1) \le \tfrac43\rho - \rho = \tfrac13\rho$.
The same bound holds for $m^{-}$. Hence

$$\bigl|\{\tau \in (0,\rho) : m^{+}(\tau) + m^{-}(\tau) \ge 3\}\bigr| \;\le\; \tfrac23 \rho \;<\; \rho,$$

so a $\tau \in (0,\rho)$ with $m^{+}(\tau) = m^{-}(\tau) = 1$ exists. Finally, by (1) a forward
point has $(\gamma(s)-O)\cdot u \ge \tfrac34(s-t_0) > 0$ and a backward point has it $< 0$, so with
(3) the two points lie one in each half of $D$. $\square$

**What Lemma 2 is really saying.** The through-strand already spends $2\tau$ of arclength inside
$B(O,\tau)$, and differentiability caps the total at $\tfrac83\tau$; a *fourth* crossing of a
circle costs more budget than is left, on all but a fraction $\tfrac23$ of the radii. The trapped
third component of $B(O,\varepsilon)\setminus J$ that stopped the neighbouring lane needs **at
least four** crossings of every circle it survives on. It cannot have them at every scale. That is
the whole idea, and the constant $\tfrac23 < 1$ is the entire quantitative content (kill-criterion
C2: the bound is not vacuous — it is strictly below the length of the interval it lives in, and it
is what makes the existence claim work).

---

## 6. Lemma 3 and Theorem T

### 6.1 Lemma 3 — no nesting

> **Lemma 3.** Let $J$ be any Jordan curve, $O \in J$, and $R$ a rotation about $O$ by an angle in
> $(0°,360°)$. If $J \cap R(J) = \{O\}$ then $\Omega \cap R(\Omega) = \emptyset$.

**regularity budget: Jordan only.** What breaks first if you drop "Jordan": the Jordan curve
theorem is used three times (two complementary components for $J$, the same for $R(J)$, and
$\partial E = J$), so it does not survive weakening $J$ to a general continuum.

*Proof.* Write $J' = R(J)$, $\Omega' = R(\Omega)$, $E' = R(E)$; since $R$ is a homeomorphism of the
plane, $J'$ is a Jordan curve with bounded component $\Omega'$ and unbounded component $E'$, and
$\lambda(\Omega') = \lambda(\Omega) < \infty$ because $R$ is an isometry ($\lambda$ = planar
Lebesgue measure). Note $O \in J \cap J'$ since $R$ fixes $O$.

$J' \setminus \{O\}$ is connected (a circle minus a point) and disjoint from $J$, so it lies in a
single component of $\mathbb{R}^2\setminus J$.

**Case A: $J' \setminus \{O\} \subseteq \Omega$.** Then $J' \subseteq \overline\Omega$, so the
connected unbounded set $E$ is disjoint from $J'$ and hence $E \subseteq E'$. Taking complements,
$\overline{\Omega'} = \mathbb{R}^2 \setminus E' \subseteq \mathbb{R}^2\setminus E = \overline\Omega$.
Both closures have the same finite measure (isometry), so
$\lambda(\overline\Omega \setminus \overline{\Omega'}) = 0$. But
$\Omega \setminus \overline{\Omega'} = \Omega \cap E'$ is **open** and null, hence empty; so
$\Omega \subseteq \overline{\Omega'}$, therefore $\overline\Omega \subseteq \overline{\Omega'}$ and
so $\overline\Omega = \overline{\Omega'}$. Taking topological boundaries and using
$\partial\overline\Omega = J$ (because $\mathbb{R}^2\setminus\overline\Omega = E$ is open with
$\overline E = E \cup J$) gives $J = J'$, contradicting $J \cap J' = \{O\}$ for a curve with more
than one point. **So Case A cannot occur.**

**Case B: $J' \setminus \{O\} \subseteq E$.** Then $\Omega \cap J' = \emptyset$ (also $O \notin
\Omega$), so the connected set $\Omega$ lies in $\Omega'$ or in $E'$.

*Sub-case $\Omega \subseteq \Omega'$ is impossible.* Then $J = \partial\Omega \subseteq
\overline{\Omega'} = \Omega' \cup J'$, and since $J \cap J' = \{O\}$ we get
$J \setminus \{O\} \subseteq \Omega'$. Pick $p \in J\setminus\{O\}$ and a ball $B_p \subseteq
\Omega'$ around it. Because $p \in J = \partial E$, $B_p \cap E$ is a nonempty **open** set, and it
is contained in $\Omega' \setminus \Omega$; so $\lambda(\Omega' \setminus \Omega) > 0$,
contradicting $\Omega \subseteq \Omega'$ with $\lambda(\Omega) = \lambda(\Omega')$ finite.

Hence $\Omega \subseteq E'$, i.e. $\Omega \cap \Omega' = \emptyset$. $\square$

**Contrapositive (the form used):** if $\Omega \cap R(\Omega) \ne \emptyset$ then
$J \cap R(J) \supsetneq \{O\}$.

*Provenance note.* The same statement is Lemma A of
[`../rotation-continuity/README.md`](../rotation-continuity/README.md) §4. I did not import it —
`RULES.md` §3 forbids resting a `sketch` on a `sketch`, my own family's included — and re-derived
it. The proofs differ in the second case (I contradict via an open subset of positive measure
rather than via boundary-taking) and I need only the weaker conclusion $\Omega \cap \Omega' =
\emptyset$. Landing in the same place is mild evidence and not verification: this is the step where
an examiner should re-derive rather than read.

### 6.2 Theorem T

> **Theorem T.** Let $J$ be a rectifiable Jordan curve with arclength parametrisation $\gamma$, and
> let $t_0$ be a parameter at which $\gamma$ is differentiable with $|\gamma'(t_0)| = 1$. Then
> $O = \gamma(t_0)$ is a vertex of an equilateral triangle inscribed in $J$.

*Proof.* Fix $\eta' = \tfrac14$, get $\delta$ from (1), $\varepsilon$ from Lemma 1 and Corollary
1.1, and shrink $\varepsilon$ further so that $\varepsilon < \tfrac12\operatorname{diam}(J)$. Apply
Lemma 2 with $\rho = \varepsilon$: there is $\tau \in (0,\varepsilon)$ with
$J \cap \partial B(O,\tau) = \{p^{+}, p^{-}\}$, exactly two points, with $p^{\pm}$ within
$\arcsin\tfrac13 < 30°$ of the directions $\pm u$.

$\partial B(O,\tau) \setminus \{p^{+},p^{-}\}$ consists of two open arcs $\mathcal{A}_1,
\mathcal{A}_2$. Since the angular positions of $p^{+}$ and $p^{-}$ differ by at least
$180° - 2\arcsin\tfrac13 > 140°$ and at most $180° + 2\arcsin\tfrac13 < 220°$, **both** arcs have
angular width greater than $140° > 60°$.

Each $\mathcal{A}_i$ is connected and disjoint from $J$, so each lies wholly inside $\Omega$ or
wholly inside $E$. And $\Omega$ meets $\partial B(O,\tau)$: it meets $B(O,\tau)$ because
$O \in J = \partial\Omega$; it is not contained in $\overline{B(O,\tau)}$, since otherwise
$J = \partial\Omega \subseteq \overline{B(O,\tau)}$ would force $\operatorname{diam}(J) \le 2\tau <
\operatorname{diam}(J)$; and it is connected, so the intermediate value theorem applied to
$x \mapsto |x - O|$ along a path in $\Omega$ from an inside point to an outside point produces a
point of $\Omega$ at distance exactly $\tau$. That point is not on $J$, so it lies in some
$\mathcal{A}_i$, and therefore $\mathcal{A}_i \subseteq \Omega$.

Let $(\beta_1,\beta_2)$ be the angular range of that arc, of width $> 140°$. Choose
$\theta = \tfrac12(\beta_1 + \beta_2) - 30°$; then both $\theta$ and $\theta + 60°$ lie in
$(\beta_1,\beta_2)$, so

$$x \;=\; O + \tau e^{i(\theta + 60°)} \in \Omega \qquad\text{and}\qquad R^{-1}(x) \;=\; O + \tau e^{i\theta} \in \Omega ,$$

because $R$ fixes $O$ and preserves the radius $\tau$. Hence $x \in \Omega \cap R(\Omega) \ne
\emptyset$, so by Lemma 3 $J \cap R(J) \supsetneq \{O\}$, and by Observation R $O$ is a vertex of an
equilateral triangle inscribed in $J$. $\square$

By Lemma 0, the triangle produced has side $\ge \varepsilon$ — the proof does **not** control its
size beyond that, and §7 explains why any argument that claims to is wrong.

### 6.3 The a.e. statement

> **Corollary T1.** For every rectifiable Jordan curve $J$, $\mathcal{H}^1$-almost every point of
> $J$ is a vertex of an equilateral triangle inscribed in $J$; equivalently, the exceptional set
> $E(J)$ is $\mathcal{H}^1$-null.

*Proof.* $\gamma$ is $1$-Lipschitz, hence differentiable a.e. (Lebesgue). Where it is
differentiable, $|\gamma'| \le 1$; and $\int_a^b |\gamma'| = b - a$ for all $a<b$ because $\gamma$
is absolutely continuous and parametrised by arclength, so $|\gamma'| = 1$ a.e. Theorem T applies at
every such parameter, and $\gamma$ pushes the full-measure parameter set onto an
$\mathcal{H}^1$-full subset of $J$ (area formula, injectivity). $\square$

> **Corollary T2 (regular $C^1$ curves).** Every point of a regular $C^1$ Jordan curve is a vertex
> of an inscribed equilateral triangle. *(Immediate: the hypothesis of Theorem T holds at every
> parameter. This reproves `rotation-continuity` §6.3 without its Hypothesis (C), whose clause (2)
> — "a single crosscut" — was the part that could not be verified.)*

### 6.4 Outcome (B) is impossible

> **Corollary T3.** There is **no** rectifiable Jordan curve carrying an exceptional point at
> which the arclength parametrisation is differentiable with unit speed.

That is the contrapositive of Theorem T and it closes option (B) of the lane brief. Any exceptional
point of a rectifiable Jordan curve is a point where the arclength parametrisation fails to be
differentiable **with unit speed** — as at the $30°$ apexes of the $30$-$30$-$120$ triangle, where
the two one-sided directions subtend $30°$ rather than $180°$ (§9, A2).

> **[Correction, dispatcher, 2026-08-29.]** This paragraph originally said "fails to be
> differentiable", dropping the unit-speed qualifier that Corollary T3 two lines above states
> correctly. The qualifier is load-bearing and the omission is not harmless: $\gamma$ is
> $1$-Lipschitz, so wherever it is differentiable $|\gamma'| \le 1$, and a point where it is
> differentiable with $|\gamma'| < 1$ satisfies "is differentiable" while falling outside
> Theorem T's hypothesis. Such points are a null set but they are not vacuous — a curve that
> doubles back at ever smaller scales while its direction converges has one. Found by the
> README-consolidation lane; the same slip had propagated into the dispatcher's journal and is
> corrected there too.

**Coordination.** A concurrent lane (`attacks/spiral-tip-witness/`) is constructing an exceptional
point and was asked whether its witness is rectifiable. I have not seen their result and will not
speculate about it. What Theorem T *predicts*, and what is worth checking against their
construction, is: **if their curve is rectifiable, then the arclength parametrisation is not
differentiable at their exceptional point.** If they produce a rectifiable witness *with* a unit
derivative at the tip, one of our two files is wrong and mine is the one making the stronger claim.
My route never reached a spiral, so there is no duplicated construction here.

---

## 7. `refuted`: the side-length clause of `rotation-continuity` Lemma B / Theorem C

[`../rotation-continuity/README.md`](../rotation-continuity/README.md) §5 states:

> ~~**Lemma B.** [sector of aperture $\ge 60°$ and radius $\varepsilon$ inside $\overline\Omega$]
> $\Rightarrow$ $O$ is a vertex of an equilateral triangle inscribed in $J$, **of side
> $\varepsilon/2$**.~~

and its Theorem C inherits the clause ("of side exactly $\varepsilon/2$"). **The side-length clause
is false.** The conclusions are not in question; only the quantifier on the side.

**Why it cannot follow, structurally.** The proof exhibits a point $x \in \overline\Omega \cap
R(\overline\Omega)$ at distance $\varepsilon/2$ from $O$ and then invokes Corollary A′, which is the
*contrapositive* of a measure-theoretic non-existence statement. It yields some
$q \in J \cap R(J)\setminus\{O\}$ and says nothing whatever about $|Oq|$. The same objection applies
to my §6: I also have no control on the side, which is why Theorem T does not claim any.

**Why it is false, not merely unjustified.** Lemma 0 forces it. At a point where $J$ is
cone-confined at scale $\varepsilon$ there is no inscribed equilateral triangle of side
$< \varepsilon$ at all, while the clause asserts one of side $\varepsilon/2$.

**Exact witness** (all arithmetic in $\mathbb{Q}(\sqrt3)$, §11):

| | |
|---|---|
| curve | boundary of the unit square $[0,1]^2$ |
| point | $O = (\tfrac12, 0)$, the midpoint of the bottom edge |
| sector | $I = [60°,120°]$, aperture exactly $60°$, radius $\varepsilon = 1$: the set $\{O + t v : 0<t<1,\ v \in I\}$ has $x \in (\tfrac12 - \tfrac t2, \tfrac12 + \tfrac t2) \subset (0,1)$ and $y \in (0,1)$, so it lies in the closed square $=\overline\Omega$. The hypothesis of Lemma B holds. |
| Lemma B predicts | an inscribed equilateral triangle with vertex $O$ of side $\varepsilon/2 = \tfrac12$ |
| exact truth | there are exactly **two** witnesses, giving the single triangle $\{(\tfrac12,0),\,(0,\tfrac{\sqrt3}{2}),\,(1,\tfrac{\sqrt3}{2})\}$, of side$^2 = 1$ — side exactly $\mathbf{1}$ |

No triangle of side $\tfrac12$ exists. (Consistency with Lemma 0: $J \cap B(O,\tfrac12)$ is a
straight segment, so no triangle of side $< \tfrac12$ can exist either; the true minimum is $1$.)

I have not edited that file — it belongs to another lane
([`../../../../RULES.md`](../../../../RULES.md) §2). **Correction request for its owner:** delete
"of side $\varepsilon/2$" from Lemma B and "of side exactly $\varepsilon/2$" from Theorem C; the
rest of §5 and §6 stands, and §6.3's corollaries are strengthened, not weakened, by §6.2 above.

---

## 8. Where the argument stops

Precisely at Corollary 1.1. Everything downstream is driven by "the curve has length at most
$\tfrac83\rho$ inside $B(O,\rho)$", and that comes from differentiability at $t_0$ and nothing else.

- **A general Jordan curve** has no arclength parametrisation, so (1) is not merely unproved but
  meaningless, and there is no substitute: a Jordan curve can have positive area and a tangent
  nowhere.
- **A rectifiable curve at a non-differentiability point** genuinely can be exceptional. The
  $30$-$30$-$120$ triangle is the witness and there is no repair.
- **The set of exceptional points** is shown here to be $\mathcal{H}^1$-null. It is **not** shown to
  be finite, let alone of size $\le 2$. Getting from "null" to "at most two" is a different and much
  harder statement — see §10 — and nothing in this lane approaches it.
- **A one-sided or weaker hypothesis.** Inspecting the proof, full differentiability is not needed:
  what is used is the single quantitative condition (1) at the *fixed* error $\eta' = \tfrac14$ and
  a *fixed* scale $\delta$ — call it *approximate unit tangency*. Theorem T holds verbatim under it.
  I state this because it is genuinely weaker (no limit is required, only one scale), but I have not
  found a curve that satisfies it while failing differentiability in an interesting way, so I record
  it as a remark and not as a strengthening worth its own claim.

---

## 9. The three filters and the kill-criterion, run

[`../../RULES.md`](../../RULES.md) §3 requires all three filters, and this lane's pre-registered
criteria require an accounting. Both follow.

### 9.1 Wedge test (§3.1) — passed, and it is the reason for the whole hypothesis

The $30$-$30$-$120$ triangle boundary is rectifiable with exactly two exceptional points, so any
statement here must be about a.e. points and never about all points. **My hypothesis excludes them
quantitatively** (kill-criterion A2): at a $30°$ apex the forward and backward one-sided directions
$u_1, u_2$ subtend $30°$, so for any candidate unit $u$ the error in (1) is at least
$\tfrac12|u_1 + u_2| = \cos 15° \approx 0.966$ on one side, vastly exceeding $\eta' = \tfrac14$.
Confirmed exactly by the decider: both $30°$ apexes not good, the $120°$ apex good (§11).

If the argument had covered them it would be wrong with no repair available; it does not.

### 9.2 Square test (§3.2) — passed; the argument does not transfer

Run the whole thing at a general rotation angle $\alpha$. Observation R, Lemmas 0–3 and Theorem T
survive for **every** $\alpha \in (0°,120°]$ — the arc found in §6.2 has width $>140°$, so it
contains a pair at angular separation $\alpha$ for any such $\alpha$. What the machine actually
proves is therefore:

> For a rectifiable Jordan curve and $\mathcal{H}^1$-a.e. $O \in J$, and for **every** $\alpha \in
> (0°,120°]$, there are $p,q \in J$ with $|Op| = |Oq| > 0$ and $\angle pOq = \alpha$ — i.e. $O$ is
> the apex of an inscribed isosceles triangle of every prescribed apex angle up to $120°$.

At $\alpha = 60°$ **and only there** the output closes: isosceles with apex $60°$ forces
equilateral, because the third side is determined by two sides and the included angle and at $60°$
it equals them. At $\alpha = 90°$ the output is an inscribed isosceles *right* triangle; the fourth
square vertex is determined as $p + q - O$ and **nothing puts it on $J$**. A single rotation about a
point of $J$ constrains only the pair $(p,q)$; a square is a four-point condition and no rotation
sees the fourth point.

So the answer to "why not squares?" is not a step that breaks — it is that the theorem being proved
is about *isosceles* triangles, which is a two-point condition, and the equilateral case is the one
value of $\alpha$ at which a two-point condition happens to certify a three-point figure. That also
explains why this argument is cheap while square peg is not.

**On the brief's remark that square peg is known for rectifiable curves.** This lane did not
attempt to source that and takes no position on it ([`../../RULES.md`](../../RULES.md) §6.1:
failing to confirm is not evidence either way). It does not affect the test: the argument above
provably does not output a square, so there is nothing to reconcile.

### 9.3 Polygon control (§3.3) — run, 0 violations, and weak evidence by construction

An independently written exact decider (§11) was run against the committed enumerator
`experiments/inscribed-triangle-polygons/` (read and run only; never modified) over its whole
190-fixture battery:

| check | count | result |
|---|---|---|
| vertices, my decider vs. `decide_good` | 783 | **0 disagreements** |
| non-vertex boundary points, my decider vs. `decide_good` | 5481 | **0 disagreements** |
| non-vertex boundary points **not good** (Theorem T predicts none) | 5481 | **0** |

The third row is the direct test: a polygon boundary is rectifiable and its arclength
parametrisation is differentiable at every non-vertex point, so Theorem T predicts every such point
is good. It is, including on the non-convex fixtures and on the C-strips whose taper angle is under
$0.3°$.

**And this evidence is weaker than usual, which must be said.** A simple polygon *cannot* exhibit
the configuration Theorem T rules out: with finitely many segments, the nearest other strand to a
non-vertex point is at positive distance, so a fat sector inside $\overline\Omega$ is automatic and
Lemma 2 is not doing any work. The census confirms the conclusion on a class where the mechanism is
trivial. Per [`../../RULES.md`](../../RULES.md) §3.3 this makes the claim *not-yet-dead*, nothing
more.

### 9.4 Kill-criterion accounting

| criterion | fired? | what happened |
|---|---|---|
| **A1** square test | no | §9.2. The general-$\alpha$ run produces isosceles triangles; only $\alpha = 60°$ closes. Named step: "isosceles with apex $\alpha$ is equilateral" is true only at $\alpha = 60°$. |
| **A2** quantifier | no | §9.1. The $30°$ apexes fail hypothesis (1) with a margin of $0.97$ against a budget of $0.25$. |
| **A3** hypothesis has no teeth | no | §1. The $120°$ apex is good and fails the hypothesis; the $30°$ apexes are not good and fail it; a.e. point of any rectifiable curve satisfies it. |
| **A4** smuggled regularity | no | The proof **never** claims $J$ is locally a graph, locally connected in any strong sense, or of finite local crossing number. Extra strands are admitted throughout; Lemma 2 shows only that they cannot occupy every radius. That is exactly the error the neighbouring lane caught in itself, and avoiding it is the content of §5. |
| **B1–B3** counterexample hunt | **moot** | Outcome (B) is impossible (Corollary T3). B3's alternative — "the trapped interior is obstructed, which is evidence for (A)" — is what happened, in the strong form: it is not merely obstructed, it is impossible, because it needs $\ge 4$ crossings of every small circle and those live on a set of radii of measure $\le \tfrac23\rho$. |
| **C1** local-pair route | **FIRED** | §3, exactly as predicted before the work. That sub-attack is `refuted`; the lane continued by a semi-local route the criterion did not anticipate. |
| **C2** vacuous bound | no | §5: $\tfrac23\rho$ against an interval of length $\rho$. |
| **C3** reproving a theorem | no | Theorem T is strictly weaker than the reported Meyerson result — a.e. on rectifiable, versus all-but-two on arbitrary Jordan (§10). Nothing here says anything about a general Jordan curve. |
| **C4** status inflation | no | Everything above is `sketch` and is labelled so in the table at the top. Nothing in this file may be assumed by later work, including by me. |

---

## 10. Relation to the reported literature — a consistency check, not an input

[`../README.md`](../README.md) reports (provisionally, at provenance P2, with **no source text
read** — the labels there are `cited`\* and are not assumable) that at most two points of any
Jordan curve are exceptional, and that two is attained. If that is right, then Corollary T1 is a
weak consequence of it for rectifiable curves, and this lane has reproved a special case of a 1980
theorem by an elementary route.

That is the expected outcome and it is stated as such:

- Nothing here is offered as new mathematics. What is new *in this repo* is a self-contained
  argument with an explicit regularity budget, resting on no unread citation, which closes the
  specific gap [`../rotation-continuity/README.md`](../rotation-continuity/README.md) §6.4 left
  open and which a Lean formalisation could in principle target (Lemma 0, Observation R and
  Sub-lemma 2a are elementary; Lemma 3 needs the Jordan curve theorem and so is not a Lean target
  today — [`../../RULES.md`](../../RULES.md) §6.3).
- Consistency runs the right way: my result is *implied by* the reported theorem and does not imply
  it. If a reviewer with network access finds Meyerson's statement to be weaker than reported, this
  file is unaffected; if stronger, this file is subsumed. Either way nothing here rests on it.
- Per [`../../../../RULES.md`](../../../../RULES.md) §7 I record the step I am least sure of:
  **Lemma 3**. It is the only place where plane topology and measure interact, and it is where a
  fluent wrong paragraph is cheapest. Second is the innocuous-looking "$\Omega$ meets
  $\partial B(O,\tau)$" in §6.2, which is the sole use of $\Omega \not\subseteq \overline{B(O,\tau)}$.

---

## 11. Reproducing the computation

Exact throughout in $\mathbb{Q}(\sqrt3)$ — the only irrationality in the problem is
$\sin 60° = \sqrt3/2$ — with **no floating point in any decision**
([`../../RULES.md`](../../RULES.md) §5). Standard library only: `fractions.Fraction`. The zero test
is syntactic ($a + b\sqrt3 = 0 \iff a = b = 0$, since $\sqrt3 \notin \mathbb{Q}$) and the sign test
compares $a^2$ with $3b^2$. **No `sympy` geometry predicate is used anywhere**, per the standing
caution that they were wrong on 3 of 176 boundary cases in this very problem.

This lane owns no `experiments/` directory, so the script is inline; save it as `rect.py` and run
`python3 rect.py` (checked with CPython 3.11). It is written from scratch and shares no code with
`experiments/inscribed-triangle-polygons/`, which the problem `RULES.md` audit standard asks for.
Runtime: under a second.

```python
"""Exact decider for the inscribed-equilateral-triangle vertex question, in Q(sqrt 3)."""
from fractions import Fraction as Fr

class E:                                                   # a + b*sqrt(3)
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = mk(o); return E(s.a+o.a, s.b+o.b)
    __radd__ = __add__
    def __sub__(s, o): o = mk(o); return E(s.a-o.a, s.b-o.b)
    def __rsub__(s, o): return mk(o) - s
    def __neg__(s): return E(-s.a, -s.b)
    def __mul__(s, o): o = mk(o); return E(s.a*o.a + 3*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def inv(s):
        d = s.a*s.a - 3*s.b*s.b                # zero only for s = 0, as sqrt3 is irrational
        if d == 0: raise ZeroDivisionError
        return E(s.a/d, -s.b/d)
    def __truediv__(s, o): return s * mk(o).inv()
    def is_zero(s): return s.a == 0 and s.b == 0
    def sign(s):                               # exact; no tolerance anywhere
        a, b = s.a, s.b
        if a == 0: return (b > 0) - (b < 0)
        if b == 0: return (a > 0) - (a < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        aa, bb = a*a, 3*b*b
        if aa == bb: raise ArithmeticError("sqrt3 rational")      # impossible
        return (1 if aa > bb else -1) if a > 0 else (1 if bb > aa else -1)
    def __eq__(s, o): return (s - mk(o)).is_zero()
    def __hash__(s): return hash((s.a, s.b))
    def __repr__(s): return f"{s.a}" if s.b == 0 else f"({s.a}+{s.b}*sqrt3)"

def mk(x): return x if isinstance(x, E) else E(x)
ZERO, ONE, HALF, R3H = E(0), E(1), E(Fr(1,2)), E(0, Fr(1,2))

sub   = lambda P,Q: (P[0]-Q[0], P[1]-Q[1])
add   = lambda P,Q: (P[0]+Q[0], P[1]+Q[1])
smul  = lambda t,P: (t*P[0], t*P[1])
cross = lambda U,V: U[0]*V[1] - U[1]*V[0]
dot   = lambda U,V: U[0]*V[0] + U[1]*V[1]
n2    = lambda U: dot(U,U)
peq   = lambda P,Q: (P[0]-Q[0]).is_zero() and (P[1]-Q[1]).is_zero()

def rot60(P, O, sigma):                        # rotate P about O by sigma*60 degrees
    x, y = sub(P, O); s = R3H if sigma > 0 else -R3H
    return add(O, (HALF*x - s*y, s*x + HALF*y))

def on_seg(X, A, B):
    if not cross(sub(B,A), sub(X,A)).is_zero(): return False
    d = dot(sub(X,A), sub(B,A))
    return d.sign() >= 0 and (d - n2(sub(B,A))).sign() <= 0

def seg_meet(A, B, C, D):                      # exact closed-segment intersection
    r, s, qp = sub(B,A), sub(D,C), sub(C,A)
    den = cross(r, s)
    if not den.is_zero():
        t, u = cross(qp,s)/den, cross(qp,r)/den
        if t.sign() >= 0 and (t-ONE).sign() <= 0 and u.sign() >= 0 and (u-ONE).sign() <= 0:
            return [add(A, smul(t, r))]
        return []
    if not cross(qp, r).is_zero(): return []                    # parallel, distinct lines
    rr = n2(r)
    if rr.is_zero(): return [A] if on_seg(A, C, D) else []
    t0, t1 = dot(sub(C,A), r)/rr, dot(sub(D,A), r)/rr
    lo, hi = (t0, t1) if (t0-t1).sign() <= 0 else (t1, t0)
    if lo.sign() < 0: lo = ZERO
    if (hi-ONE).sign() > 0: hi = ONE
    if (hi-lo).sign() < 0: return []
    P0, P1 = add(A, smul(lo, r)), add(A, smul(hi, r))
    return [P0] if peq(P0, P1) else [P0, P1]

edges   = lambda poly: [(poly[i], poly[(i+1) % len(poly)]) for i in range(len(poly))]
on_poly = lambda X, poly: any(on_seg(X, A, B) for A, B in edges(poly))

def witnesses(poly, O):
    """Every X != O in J ∩ rho_sigma(J); each triangle re-verified from scratch."""
    Eg, out = edges(poly), {}
    for sigma in (1, -1):
        for RA, RB in [(rot60(A,O,sigma), rot60(B,O,sigma)) for A,B in Eg]:
            for C, D in Eg:
                for X in seg_meet(RA, RB, C, D):
                    if peq(X, O): continue                     # the degenerate solution
                    key = (X[0].a, X[0].b, X[1].a, X[1].b, sigma)
                    if key in out: continue
                    Q = rot60(X, O, -sigma)
                    a, b, c = n2(sub(Q,O)), n2(sub(X,O)), n2(sub(X,Q))
                    out[key] = {"sigma": sigma, "Q": Q, "X": X, "side2": a,
                        "verified": on_poly(O,poly) and on_poly(Q,poly) and on_poly(X,poly)
                            and not peq(O,Q) and not peq(O,X) and not peq(Q,X)
                            and a == b and b == c and a.sign() > 0}
    return list(out.values())

def decide(poly, O): w = witnesses(poly, O); return (len(w) > 0), w
def min_side2(w):
    if not w: return None
    m = w[0]["side2"]
    for x in w[1:]:
        if (x["side2"]-m).sign() < 0: m = x["side2"]
    return m
P = lambda x, y: (E(x), E(y))

if __name__ == "__main__":
    r3 = E(0, 1)
    print("== check 1: validation gate on known answers ==")
    eqt = [P(0,0), P(1,0), (E(Fr(1,2)), r3*E(Fr(1,2)))]
    for V in eqt:
        g, w = decide(eqt, V); print("  equilateral", V, "good:", g, "min side^2:", min_side2(w))
    tri = [P(0,0), P(1,0), (E(Fr(1,2)), r3*E(Fr(1,6)))]        # 30-30-120, RULES 3.1 witness
    for nm, V in [("30deg apex O", tri[0]), ("30deg apex A", tri[1]), ("120deg apex C", tri[2])]:
        g, w = decide(tri, V)
        print(f"  30-30-120 {nm:14s} good: {g}  min side^2: {min_side2(w)}  #witnesses: {len(w)}")
    sq = [P(0,0), P(1,0), P(1,1), P(0,1)]
    g, w = decide(sq, sq[0]); print("  unit square corner good:", g, "min side^2:", min_side2(w))
    print("  all witnesses re-verified:", all(x["verified"] for x in
          witnesses(eqt, eqt[0]) + witnesses(tri, tri[2]) + witnesses(sq, sq[0])))

    print("== check 2: the side-length clause of rotation-continuity Lemma B / Theorem C ==")
    O = P(Fr(1,2), 0)                          # midpoint of the bottom edge of the unit square
    g, w = decide(sq, O)
    print("  O=(1/2,0): good:", g, " #witnesses:", len(w),
          " distinct side^2:", sorted({(x['side2'].a, x['side2'].b) for x in w}))
    for x in w:
        print("   sigma", x["sigma"], "Q", x["Q"], "X", x["X"],
              "side^2", x["side2"], "verified", x["verified"])
```

**Validation gate, run first** ([`../../RULES.md`](../../RULES.md) §5) — output, matching the
committed enumerator's published control table exactly:

```
== check 1: validation gate on known answers ==
  equilateral (0, 0) good: True min side^2: 1
  equilateral (1, 0) good: True min side^2: 1
  equilateral (1/2, (0+1/2*sqrt3)) good: True min side^2: 1
  30-30-120 30deg apex O   good: False  min side^2: None  #witnesses: 0
  30-30-120 30deg apex A   good: False  min side^2: None  #witnesses: 0
  30-30-120 120deg apex C  good: True  min side^2: 1/12  #witnesses: 6
  unit square corner good: True min side^2: (8+-4*sqrt3)
  all witnesses re-verified: True
== check 2: the side-length clause of rotation-continuity Lemma B / Theorem C ==
  O=(1/2,0): good: True  #witnesses: 2  distinct side^2: [(Fraction(1, 1), Fraction(0, 1))]
   sigma 1 Q (1, (0+1/2*sqrt3)) X (0, (0+1/2*sqrt3)) side^2 1 verified True
   sigma -1 Q (0, (0+1/2*sqrt3)) X (1, (0+1/2*sqrt3)) side^2 1 verified True
```

**The §9.3 census.** Add the committed enumerator's fixtures as an oracle — reading and running it,
never modifying it:

```python
import sys
from fractions import Fraction as Fr
sys.path.insert(0, "<repo>/experiments/inscribed-triangle-polygons")
import geom as G
from fixtures import battery
from rect import E, decide                      # the script above, saved as rect.py

to_mine   = lambda p: E(*p.as_pair())
pt_to_mine= lambda P: (to_mine(P[0]), to_mine(P[1]))
TS = [Fr(1,5), Fr(1,3), Fr(1,2), Fr(2,3), Fr(4,5), Fr(1,7), Fr(6,7)]

dis = bad = nv = nvx = 0
for f in battery():
    poly = f["poly"]
    if not G.is_simple(poly)[0]: continue
    mine_poly = [pt_to_mine(v) for v in poly]
    for V in poly:                                        # vertices: two independent deciders
        nv += 1
        if G.decide_good(poly, V)["good"] != decide(mine_poly, pt_to_mine(V))[0]: dis += 1
    for (A, B) in G.edges(poly):                          # non-vertex points: Theorem T's prediction
        for t in TS:
            X = G.sample_edge_point(A, B, t); nvx += 1
            mine = decide(mine_poly, pt_to_mine(X))[0]
            if G.decide_good(poly, X)["good"] != mine: dis += 1
            if not mine: bad += 1
print(nv, "vertices,", nvx, "non-vertex points, disagreements:", dis, ", not-good:", bad)
# -> 783 vertices, 5481 non-vertex points, disagreements: 0 , not-good: 0
```

Deterministic — no randomness in the decider, and the fixture generators are seeded upstream
(`20260829`), so this reproduces bit for bit. Total compute for this lane: a few minutes, well
inside the one-hour budget ([`../../../../RULES.md`](../../../../RULES.md) §6.6).

---

## 12. What a reviewer should attack

In the order I would attack it.

1. **Lemma 3 (§6.1).** Re-derive it; do not read it. Attack the two case splits, the claim
   $\partial\overline\Omega = J$, and the two places where an open set of positive measure is
   extracted. This is a Jordan-curve-theorem argument applied to a rotated copy — precisely the
   failure mode [`../../RULES.md`](../../RULES.md) §6.2 item 1 names — so check that $R(J)$ is a
   Jordan curve (it is, $R$ being a homeomorphism) and that $\Omega'$ really is *its* bounded
   component.
2. **Lemma 2 (§5).** The chain is: parameters localise (Lemma 1) $\to$ (2) confines them to
   $|s-t_0| \le \tfrac43\rho$ $\to$ the partition inequality caps $\int m^\pm$ $\to$ the bad set has
   measure $\le \tfrac23\rho < \rho$. Check the constant. Check Sub-lemma 2a on a function with a
   plateau (where $\#h^{-1}$ is infinite at one level — a null set of levels, so harmless, but look
   at it). Check that $\#(J \cap \partial B(O,\tau)) = m^+ + m^-$ uses injectivity and Lemma 1 and
   nothing else.
3. **§6.2's "$\Omega$ meets $\partial B(O,\tau)$".** The only step that uses
   $\Omega \not\subseteq \overline{B(O,\tau)}$, hence the constraint
   $\varepsilon < \tfrac12\operatorname{diam}(J)$.
4. **The regularity budget** ([`../../RULES.md`](../../RULES.md) §1 and §6.2 item 5). Every
   hypothesis declared at the top is used: rectifiability for the existence of $\gamma$,
   differentiability at $t_0$ for (1)–(3) and Corollary 1.1, Jordan for Lemmas 1 and 3. Confirm no
   undeclared one — in particular confirm that nowhere is $J$ assumed to be locally a graph, and
   that extra strands inside $B(O,\varepsilon)$ are permitted throughout.
5. **Continuity claimed where it fails** ([`../../RULES.md`](../../RULES.md) §6.2 item 2). There
   should be none: no object here is claimed to vary continuously in $O$, and no limit of triangles
   is taken. Verify that, because it is the standard trap for this problem and the absence of it is
   what makes the noncollapse obligation vacuous rather than discharged by an estimate.
