# Exceptional-pair rigidity: what does $|E(J)| = 2$ force?

```
regularity budget: NONE for Theorems W0/W1/W2 (the statements are about an arbitrary
subset S of the plane and a cone hypothesis at one or two of its points; no Jordan
curve, no convexity, no rectifiability, no tangent, no measure);
convex + compact + nonempty interior for the corollaries about E(dK), which additionally
consume the intermediate value theorem on a real interval;
polygonal for everything in the census (§7), which is `numerical` and decides nothing.
What breaks first if the convexity is dropped from §6: the equivalence
"exceptional <=> the whole curve sits in a 60-degree cone at O" fails in BOTH directions,
and §7 exhibits exact integer polygons where it fails and where the rigidity fails with it.
```

- Lane: idea **I5** of [`../ideation-round-1/README.md`](../ideation-round-1/README.md).
- Author: `claude` (Claude Opus 5), 2026-08-29, branch
  `claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md), **written before any computation
  in this lane**; outcomes in §11.
- Journal: [`../../../../notebook/claude/2026-08-29-iet-rigidity.md`](../../../../notebook/claude/2026-08-29-iet-rigidity.md).
- Problem rules consumed: [`../../RULES.md`](../../RULES.md) §1 (budget line, above), §2
  (nondegeneracy — §1.2), §3.1/§3.2/§3.3 (all three filters run and all three reported, §9),
  §5 (exact arithmetic — §7.1 says which steps are exact and which are float), §6 (statuses).

---

## Result table

| § | Statement | Status |
|---|---|---|
| §2 | **Lemma R (radial criterion).** For $S \subseteq \mathbb{R}^2$ and $O \in S$: $O$ is a vertex of a nondegenerate equilateral triangle with all vertices in $S$ $\iff$ there are $r>0$ and $\theta$ with $O+re^{i\theta} \in S$ and $O+re^{i(\theta+60°)} \in S$. | `sketch` — mine, re-derived here from scratch |
| §3 | **Theorem W0 (one blocked point is a diameter endpoint).** If every point of $S$ lies in a closed cone of opening $\le 60°$ with apex $O \in S$, then $\operatorname{diam}(S) = \sup_{Z \in S}\lvert OZ\rvert$. | `sketch` — mine; budget **none** |
| §3 | **Theorem W1 (two blocked points are *the* diameter).** If the cone condition holds at $O_1$ and at $O_2$, $O_1 \ne O_2$, then $\operatorname{diam}(S) = \lvert O_1O_2\rvert$. | `sketch` — mine; budget **none** |
| §3 | **Theorem W2 (uniqueness).** Under W1, if in addition $O_1$ is a vertex of no equilateral triangle inscribed in $S$, then $\{O_1,O_2\}$ is the **only** pair of points of $S$ at distance $\operatorname{diam}(S)$. | `sketch` — mine; budget **none** |
| §3.4 | **Proposition T (thinness).** With cone openings $\alpha_1,\alpha_2$ at $O_1,O_2$: every point of $S$ is within $\tfrac12 d\tan\!\big(\tfrac{\alpha_1+\alpha_2}{2}\big)$ of the line $O_1O_2$, $d = \lvert O_1O_2\rvert$. Informative when $\alpha_1+\alpha_2 < 90°$. | `sketch` — mine |
| §5 | **Re-derivation of the convex tangent-cone criterion**, independently of [`../convex-vertex-criterion/`](../convex-vertex-criterion/README.md): $\alpha(O) < 60° \Rightarrow$ exceptional; $\alpha(O) > 60° \Rightarrow$ good (a **shorter** proof than that lane's, three cases instead of an $A/B/C$ split); $\alpha(O) = 60° \Rightarrow$ good iff both extreme rays meet $K$. | `sketch` — mine |
| §6 | **Corollary C1.** For $K$ compact convex with interior, every exceptional point of $\partial K$ is an endpoint of a diameter of $K$. **Corollary C2.** If $E(\partial K) = \{O_1,O_2\}$ then $\lvert O_1O_2\rvert = \operatorname{diam} K$ and that pair is the **unique** diameter pair. | `sketch` — mine |
| §6.3 | **No shape rigidity.** Exactly two exceptional points does **not** determine the shape: every triangle with two angles below $60°$ works, as do lens- and quadrilateral-shaped bodies, and $(\alpha_1,\alpha_2)$ ranges over all of $(0°,60°)^2$. The rigidity is entirely **metric**. | `sketch` — mine |
| §8 | **$\lvert E(J)\rvert = 1$ is possible**, exact convex witness: the triangle $(0,0),(5,0),(2,4)$, whose only exceptional point is $(5,0)$. So there is **no parity obstruction**. | `sketch` + `numerical` (exact) |
| §7.3 | **W1 does not extend to non-convex curves.** Three exact integer-coordinate simple polygons with $\lvert E\rvert = 2$ and $\lvert O_1O_2\rvert < \operatorname{diam}$; the smallest has **five** vertices, and a hill-climb reaches $\lvert O_1O_2\rvert/\operatorname{diam} = 0.7241$. | `numerical` (exact arithmetic, two independent deciders) |
| §7.4 | **The wedge is not the only mechanism on polygons.** $327$ of the $1\,334$ exceptional points found on non-convex polygons ($24.5\%$) are **not** wedge-blocked — the polygon analogue of the spiral tip, but exact and with integer coordinates. | `numerical` |
| §7.5 | **Every both-wedge pair in the census is the unique diameter pair** — $537/537$, zero exceptions, of which $206$ pairs sit on **non-convex** polygons. This is W1's own falsifiable prediction, tested where its hypothesis holds but convexity does not. | `numerical` |

**Nothing here is assumable** ([`../../../../RULES.md`](../../../../RULES.md) §3), including by me.
Nothing here is `verified:review`; no agent outside the Claude family has seen it.

---

## 0. What I re-derived, and what I assumed

[`../../../../RULES.md`](../../../../RULES.md) §3 forbids building on a `sketch`, including my own
and including another lane's. The brief for this lane pointed at
[`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md) Theorem C as
motivation, and that file is `sketch`. So:

**Re-derived from the definitions, in this file, before use:**

- the radial criterion (§2) — proved here, not imported from
  [`../rotation-continuity/`](../rotation-continuity/README.md) §2 (Observation R), from
  `convex-vertex-criterion` (Proposition R), or from
  [`../spiral-tip-witness/`](../spiral-tip-witness/README.md) (Lemma 1). That four lanes and two
  experiments independently land on the same three lines is a **cross-check**, reported as such in
  §2.2, not a dependency;
- the wedge obstruction (§3.1), which is [`../../RULES.md`](../../RULES.md) §3.1 and is proved here
  in one line rather than quoted;
- the convex facts F1–F5 and the two directions of the convex criterion (§5), with a proof of the
  existence half that is **shorter than and structurally different from** the one in
  `convex-vertex-criterion` — three cases decided by one sign, instead of an $A/B/C$ split.

**Assumed (and these are the only external inputs):** Euclidean plane geometry — the law of
cosines, the law of sines / "larger angle opposite longer side", the angle sum of a triangle, the
supporting-line property of a convex set at a boundary point, and the intermediate value theorem
on a real interval. §5 additionally uses compactness of $K$.

**Explicitly not used as a premise anywhere:** Meyerson's bound $\lvert E(J)\rvert \le 2$
([`../../README.md`](../../README.md) row 2, `cited`\*, provisional and unread). It appears once,
in §7.6, as an **after-the-fact consistency check on output**, which is the only role a provisional
citation may play.

---

## 1. Setting

$J \subset \mathbb{R}^2$ is a Jordan curve; $O \in J$ is **good** if some nondegenerate equilateral
triangle has all three vertices on $J$ and one of them equal to $O$, and **exceptional** otherwise.
$E(J)$ is the set of exceptional points. For a compact convex $K$ with $\operatorname{int}K \ne
\emptyset$ we write $J = \partial K$ and, for $O \in J$,

$$A(O) = \{\arg(x - O) : x \in K \setminus \{O\}\}, \qquad \alpha(O) = \operatorname{diam} A(O),$$

the angular width of $K$ as seen from $O$ — the opening of the tangent cone, defined without
taking any closure. §5.1 shows $\alpha(O) \in (0°, 180°]$ and that $A(O)$ is an arc.

**1.2 Nondegeneracy** ([`../../RULES.md`](../../RULES.md) §2). Everywhere below "equilateral
triangle" means **three pairwise distinct points at equal pairwise distances**, equivalently
positive side length. Every existence statement in §3 and §5 produces a witness with an explicitly
positive side, and the point is flagged where it is earned. No limiting argument occurs anywhere in
this file, so the classical trap — a limit of nondegenerate triangles assumed nondegenerate — has
no place to hide here; the one existence proof (§5.3) is an intermediate value theorem for a
scalar function of a scalar angle, and the side length it returns is bounded below by construction.

---

## 2. Lemma R — the radial criterion

> **Lemma R.** Let $S \subseteq \mathbb{R}^2$ and $O \in S$. Then $O$ is a vertex of a
> nondegenerate equilateral triangle with all vertices in $S$ **iff** there exist $r > 0$ and an
> angle $\theta$ with $O + re^{i\theta} \in S$ and $O + re^{i(\theta + 60°)} \in S$.

*Proof.* ($\Leftarrow$) Put $P = O + re^{i\theta}$, $Q = O + re^{i(\theta+60°)}$. Then
$\lvert OP\rvert = \lvert OQ\rvert = r > 0$ and $\angle POQ = 60°$, so the triangle $OPQ$ is
isoceles with apex angle $60°$; its base angles are $(180° - 60°)/2 = 60°$, so it is equiangular,
hence equilateral with side $r > 0$. It is nondegenerate: $r>0$ gives $P,Q \ne O$, and the $60°$
separation gives $P \ne Q$.
($\Rightarrow$) If $O,P,Q \in S$ are pairwise distinct with $\lvert OP\rvert = \lvert OQ\rvert =
\lvert PQ\rvert = s > 0$ then $\angle POQ = 60°$, so writing $P = O + se^{i\theta_P}$,
$Q = O + se^{i\theta_Q}$ we have $\theta_Q - \theta_P \equiv \pm 60°$; take
$(\theta, r) = (\theta_P, s)$ or $(\theta_Q, s)$. $\square$

**2.1 Where the degeneracy is paid.** $r > 0$ is the entire nondegeneracy question: $r = 0$ is
available at every $O$ and every $\theta$ and is the "triangle" $O,O,O$. Every use of Lemma R below
exhibits a strictly positive $r$.

**2.2 Cross-check, not a dependency.** The same statement, in the same three lines, is Observation
R of [`../rotation-continuity/`](../rotation-continuity/README.md), Proposition R of
[`../convex-vertex-criterion/`](../convex-vertex-criterion/README.md), Lemma 1 of
[`../spiral-tip-witness/`](../spiral-tip-witness/README.md), and criterion (R) of both experiments.
Five independent derivations agreeing is mild evidence and no more; all five are `sketch` or
`numerical` and none of them is an input here.

---

## 3. The rigidity theorems — no regularity at all

Throughout this section $S \subseteq \mathbb{R}^2$ is an **arbitrary** set. Say $O \in S$ is
**$\theta$-blocked** if there is a closed convex cone with apex $O$ and opening $\le \theta$
containing $S$; equivalently, $\angle XOY \le \theta$ for all $X, Y \in S \setminus \{O\}$.

**3.1 The wedge obstruction (one line).** *If $O$ is $\theta$-blocked with $\theta < 60°$ then $O$
is exceptional.* Indeed a triangle as in Lemma R needs $\angle POQ = 60° > \theta$. $\square$
(This is [`../../RULES.md`](../../RULES.md) §3.1, re-proved rather than quoted. Note that
$60°$-blocked does **not** imply exceptional: the equilateral triangle is $60°$-blocked at each
vertex and each vertex is good.)

### Theorem W0 — a blocked point realises the diameter

> Let $S \subseteq \mathbb{R}^2$ and let $O \in S$ be $60°$-blocked. Then
> $$\operatorname{diam}(S) = \sup_{Z \in S} \lvert OZ\rvert .$$
> In particular if $S$ is compact and nonempty, $O$ is an endpoint of a diameter of $S$.

*Proof.* Write $R = \sup_{Z\in S}\lvert OZ\rvert$; $\operatorname{diam}(S) \ge R$ is trivial since
$O \in S$. For the converse take $X, Y \in S$. If either equals $O$ then $\lvert XY\rvert \le R$.
Otherwise put $a = \lvert OX\rvert \le R$, $b = \lvert OY\rvert \le R$ and $\gamma = \angle XOY \le
60°$, so $\cos\gamma \ge \tfrac12$ and, by the law of cosines,
$$\lvert XY\rvert^2 = a^2 + b^2 - 2ab\cos\gamma \;\le\; a^2 + b^2 - ab .$$
On $[0,R]^2$ the function $f(a,b) = a^2+b^2-ab$ is convex in each variable separately, so its
maximum is at a corner: $f(0,0)=0$, $f(R,0)=f(0,R)=f(R,R)=R^2$. Hence $\lvert XY\rvert \le R$.
$\square$

**Why $60°$ is exactly the threshold, and what the equality case is.** The step
$\cos\gamma \ge \tfrac12$ is the only place the hypothesis enters, and it fails for
$\gamma > 60°$. The equality configuration $a = b = R$, $\gamma = 60°$ is precisely an
**equilateral triangle $O,X,Y$ of side $R$ inscribed in $S$**. So the inequality "the diameter is
seen from $O$" and the existence of an inscribed equilateral triangle at $O$ of maximal size are
the same borderline. That coincidence is what makes this lane's question have an answer at all,
and it is exploited in W2.

### Theorem W1 — two blocked points *are* the diameter

> If $O_1 \ne O_2$ are both $60°$-blocked points of $S$, then
> $\operatorname{diam}(S) = \lvert O_1O_2\rvert$.

*Proof.* Put $d = \lvert O_1O_2\rvert > 0$. **Step (i): $\lvert O_1Z\rvert \le d$ for every
$Z \in S$.** For $Z \in \{O_1,O_2\}$ this is clear. Otherwise consider $O_1, O_2, Z$.
*If they are collinear:* $Z$ cannot lie beyond $O_2$, since then $\angle ZO_2O_1 = 180° > 60°$
contradicting blockedness at $O_2$; nor beyond $O_1$, since then $\angle ZO_1O_2 = 180° > 60°$;
so $Z$ lies strictly between and $\lvert O_1Z\rvert < d$. *If they are not collinear:* the triangle
$O_1O_2Z$ has $\angle ZO_1O_2 \le 60°$ and $\angle ZO_2O_1 \le 60°$ by blockedness, hence
$\angle O_1ZO_2 \ge 60° \ge \angle ZO_2O_1$; the side opposite the larger angle is at least as
long, and those sides are $O_1O_2$ and $O_1Z$, so $d \ge \lvert O_1Z\rvert$.
**Step (ii).** By step (i), $\sup_{Z}\lvert O_1Z\rvert = d$ (attained at $O_2$), and $O_1$ is
$60°$-blocked, so Theorem W0 gives $\operatorname{diam}(S) = d$. $\square$

### Theorem W2 — and they are the *only* diameter pair

> Under the hypotheses of W1, suppose in addition that $O_1$ is a vertex of **no** equilateral
> triangle with all vertices in $S$. Then $\{O_1,O_2\}$ is the unique pair of points of $S$ at
> distance $\operatorname{diam}(S) = d$.

*Proof.* Let $X, Y \in S$ with $\lvert XY\rvert = d$; we show $\{X,Y\} = \{O_1,O_2\}$.

*Case $O_1 \in \{X,Y\}$*, say $Y = O_1$, so $\lvert O_1X\rvert = d$. Trace the equality through
step (i) of W1. Collinearity is impossible ($\lvert O_1Z\rvert < d$ strictly there), so
$O_1,O_2,X$ is a genuine triangle with $\angle O_1XO_2 \ge 60° \ge \angle XO_2O_1$ and
$\lvert O_1X\rvert = \lvert O_1O_2\rvert$, which forces $\angle O_1XO_2 = \angle XO_2O_1$, hence
both are $60°$, hence $\angle XO_1O_2 = 60°$ as well. Then $\lvert O_1X\rvert = \lvert O_1O_2\rvert
= d > 0$ with $\angle XO_1O_2 = 60°$, so $O_1, X, O_2$ is an equilateral triangle of side $d$
inscribed in $S$ with a vertex at $O_1$ — contradicting the hypothesis, unless the triangle is not
a triangle, i.e. $X = O_2$. So $X = O_2$.

*Case $O_1 \notin \{X,Y\}$.* With $a = \lvert O_1X\rvert$, $b = \lvert O_1Y\rvert$,
$\gamma = \angle XO_1Y$ as in W0 (and $a,b \le d$ by step (i)), equality $\lvert XY\rvert = d$
forces **both** $a^2+b^2-ab = d^2$ and ($ab = 0$ or $\cos\gamma = \tfrac12$). The first equation on
$[0,d]^2$ has solution set exactly $\{(d,0),(0,d),(d,d)\}$: on $a = d$ it reads $b^2 = bd$; on
$a<d, b<d$ the maximum of $f$ over the closed square is attained only at corners and equals $d^2$
only at those three. $(d,0)$ and $(0,d)$ mean $Y = O_1$ or $X = O_1$, excluded in this case.
$(d,d)$ forces $ab \ne 0$, hence $\gamma = 60°$, hence $O_1, X, Y$ is an equilateral triangle of
side $d>0$ inscribed in $S$ with a vertex at $O_1$ — contradiction. $\square$

**Budget.** W0, W1, W2 use **nothing** about $S$: not convexity, not connectedness, not
measurability, not closedness (compactness is used only to turn a supremum into a maximum in the
last sentence of W0). Their whole content is the law of cosines, the law of sines and the angle sum
of a triangle. This is the strongest budget line available and is the main reason I distrust these
three least.

### 3.4 Proposition T — the blocked pair also forces thinness

> Let $O_1, O_2$ be as in W1, blocked with cone openings $\alpha_1, \alpha_2 \le 60°$, and
> $d = \lvert O_1O_2\rvert$. Then every $X \in S$ lies within distance
> $\tfrac12 d \tan\!\big(\tfrac{\alpha_1+\alpha_2}{2}\big)$ of the line $O_1O_2$.

*Proof.* For $X \notin \{O_1,O_2\}$ the triangle $O_1O_2X$ has $\angle XO_1O_2 \le \alpha_1$ and
$\angle XO_2O_1 \le \alpha_2$, so $\theta := \angle O_1XO_2 \ge 180° - \alpha_1 - \alpha_2$. The
locus $\{\angle O_1XO_2 \ge \theta\}$ is bounded by the two circular arcs on which $O_1O_2$
subtends exactly $\theta$; the point of such an arc farthest from the chord is its isoceles apex,
at distance $\tfrac{d}{2}\cot(\theta/2)$. Since $\cot$ decreases,
$\cot(\theta/2) \le \cot\!\big(90° - \tfrac{\alpha_1+\alpha_2}{2}\big) =
\tan\!\big(\tfrac{\alpha_1+\alpha_2}{2}\big)$. $\square$

Informative exactly when $\alpha_1 + \alpha_2 < 90°$ (otherwise $\operatorname{diam} = d$ already
bounds it). At $\alpha_1 = \alpha_2 = 30°$ it says $S$ lies in a strip of half-width
$d\tan(30°)/2 = d/(2\sqrt3)$ about the line: the $30$–$30$–$120$ witness has
$d = \sqrt3$ and apex at distance exactly $1/2 \le \sqrt3/(2\sqrt3) = 1/2$ — **tight**.

---

## 4. Reading W1 as an answer to the brief

W0–W2 are about *blocked* points, not about *exceptional* points, and the difference is the whole
story of this lane:

- **blocked $\Rightarrow$ exceptional** always (§3.1, for opening $< 60°$);
- **exceptional $\Rightarrow$ blocked** for convex curves (§5–§6) — so on convex curves the
  rigidity is a theorem about $E(J)$;
- **exceptional $\not\Rightarrow$ blocked** in general — §7.4 gives integer-coordinate polygons
  where it fails, and [`../spiral-tip-witness/`](../spiral-tip-witness/README.md) gives a
  rectifiable curve where it fails, and §7.3 shows the rigidity fails with it.

---

## 5. The convex criterion, re-derived

$K \subset \mathbb{R}^2$ compact convex, $\operatorname{int}K \ne \emptyset$, $J = \partial K$,
$O \in J$. Normalise $O = 0$ and rotate so that $A = A(O) \subseteq [0,\alpha]$ with
$\inf A = 0$, $\sup A = \alpha = \alpha(O)$. Put
$r(\theta) = \max\{t \ge 0: te^{i\theta} \in K\}$ and $\Sigma(\theta) = \{t>0: te^{i\theta} \in J\}$.

**5.1 F1–F5.**

- **F1.** $\alpha \in (0°,180°]$ and $A$ is an arc. $K$ is convex and $O \in \partial K$, so there
  is a supporting line at $O$ and $K - O$ lies in a closed half-plane, whence $A$ lies in a closed
  half-circle and $\alpha \le 180°$. $A$ is convex as a set of directions because $K-O$ is a convex
  set not containing $0$ in its interior; $\alpha > 0$ because $\operatorname{int}K \ne \emptyset$.
  Consequently $(0,\alpha) \subseteq A \subseteq [0,\alpha]$ and $r(\theta) > 0$ on $(0,\alpha)$.
- **F2 (radial interior).** For $\theta \in (0,\alpha)$ and $0 < t < r(\theta)$,
  $te^{i\theta} \in \operatorname{int}K$; hence $\Sigma(\theta) = \{r(\theta)\}$.
  *Proof.* Choose $\psi_1 < \theta < \psi_2$ in $(0,\alpha) \subseteq A$ and points
  $x_i = r(\psi_i)e^{i\psi_i} \in K$. Then $\operatorname{conv}\{0,x_1,x_2\} \subseteq K$ is a
  nondegenerate triangle whose interior contains $\delta e^{i\theta}$ for all small $\delta>0$; fix
  such a $\delta < r(\theta)$, so $w := \delta e^{i\theta} \in \operatorname{int}K$. The standard
  convexity fact "$w \in \operatorname{int}K$, $y \in K$ $\Rightarrow$ $[w,y) \subseteq
  \operatorname{int}K$" applied with $y = r(\theta)e^{i\theta}$ and with $y = 0$ covers all
  $0<t<r(\theta)$. $\square$
- **F3 (extreme rays are boundary).** If $r(0) > 0$ then $\Sigma(0) = (0, r(0)]$; likewise at
  $\alpha$. *Proof.* If $te^{i0} \in \operatorname{int}K$ for some $t>0$, a ball around it inside
  $K$ contains points of argument $<0$, contradicting $A \subseteq [0,\alpha]$. $\square$
- **F4 (semicontinuity).** $r$ is upper semicontinuous on $[0,\alpha]$ (if $\theta_n \to \theta^*$
  and $r(\theta_n) \to c$ then $r(\theta_n)e^{i\theta_n} \to ce^{i\theta^*} \in K$ as $K$ is
  closed, so $c \le r(\theta^*)$; boundedness comes from compactness) and continuous on
  $(0,\alpha)$ (lower semicontinuity there follows from F2 and openness of $\operatorname{int}K$).
- **F5 (the reduction).** By Lemma R and $A \subseteq [0,\alpha]$: $O$ is good $\iff$ there is
  $\theta$ with $\theta, \theta - 60° \in [0,\alpha]$ and $\Sigma(\theta) \cap \Sigma(\theta-60°)
  \ne \emptyset$.

**5.2 Obstruction.** If $\alpha(O) < 60°$ then $O$ is exceptional: immediate from §3.1, since
$K \subseteq O + \{\arg \in [0,\alpha]\}$ makes $O$ $\alpha$-blocked.

**5.3 Existence.** *If $\alpha(O) > 60°$ then $O$ is good.*

*Proof.* On $(60°, \alpha)$ define $h(\theta) = r(\theta) - r(\theta - 60°)$. Both arguments lie in
$(0,\alpha)$, so $h$ is continuous there (F4).

- If $h(\theta_0) = 0$ for some $\theta_0 \in (60°,\alpha)$: then $t := r(\theta_0) > 0$ (F1) lies
  in $\Sigma(\theta_0)$ and in $\Sigma(\theta_0 - 60°)$ by F2, and F5 applies.
- Otherwise $h$ has constant sign on the interval, by the intermediate value theorem.
  - **$h > 0$.** Take $\theta_n \uparrow \alpha$. Then $r(\theta_n) > r(\theta_n - 60°)$; the right
    side tends to $r(\alpha-60°) > 0$ by continuity at $\alpha - 60° \in (0,\alpha)$, and
    $\limsup r(\theta_n) \le r(\alpha)$ by upper semicontinuity. Hence
    $r(\alpha) \ge r(\alpha-60°) > 0$, so $\alpha \in A$ and F3 gives
    $\Sigma(\alpha) = (0, r(\alpha)]$. Take $t = r(\alpha - 60°) \in (0, r(\alpha)]$: then
    $t \in \Sigma(\alpha-60°)$ by F2 and $t \in \Sigma(\alpha)$ by F3. F5 applies.
  - **$h < 0$.** Symmetrically, $\theta_n \downarrow 60°$ gives $r(60°) \le r(0)$, so $0 \in A$,
    $\Sigma(0) = (0,r(0)]$, and $t = r(60°) > 0$ works.

In all cases the witness radius is strictly positive, so the triangle is nondegenerate. $\square$

> **This is a different and shorter proof than the one in
> [`../convex-vertex-criterion/`](../convex-vertex-criterion/README.md) §2 (Theorem B(i)),** which
> splits into cases $r(0) \ge r(60°)$, $r(\alpha) \ge r(\alpha-60°)$, and an IVT case. Here the
> trichotomy is on the *sign of $h$*, which makes the two extreme-ray cases fall out of the same
> limit computation. The two proofs use the same F-facts and reach the same conclusion; I derived
> this one before re-reading that one's case analysis, and the agreement is a cross-check
> (**K2 did not fire**, §11).

**5.4 The boundary case $\alpha(O) = 60°$.** Then the only admissible pair in F5 is
$(\theta, \theta - 60°) = (60°, 0°)$, and by F3 $\Sigma(60°)$ and $\Sigma(0°)$ are $(0,r(\cdot)]$
when the corresponding extreme direction is achieved and $\emptyset$ otherwise. So $O$ is good
$\iff$ $A = [0°,60°]$, i.e. **iff both extreme rays of the tangent cone meet $K$ in a segment of
positive length**. In particular a convex *polygon* vertex is good $\iff$ its interior angle is
$\ge 60°$, since there $A$ is closed. (Independently checked on $10\,164$ convex polygon vertices,
zero violations — §7.2.)

---

## 6. The convex corollaries

By §5.2–§5.3, $O \in E(\partial K) \Rightarrow \alpha(O) \le 60° \Rightarrow O$ is $60°$-blocked
(the tangent cone is a closed convex cone of opening $\alpha(O)$ containing $K$). So W0, W1, W2
apply with $S = K$, and $\operatorname{diam}K = \operatorname{diam}\partial K$ because
$K = \operatorname{conv}(\partial K)$.

> **Corollary C1.** For $K$ compact convex with nonempty interior, **every** exceptional point of
> $\partial K$ is an endpoint of a diameter of $K$.
>
> **Corollary C2.** If $E(\partial K) = \{O_1,O_2\}$ then $\lvert O_1O_2\rvert = \operatorname{diam}K$
> and $\{O_1,O_2\}$ is the **unique** pair realising the diameter.
>
> **Corollary C3.** $K \subseteq \bar B(O_1,d) \cap \bar B(O_2,d)$ with $d = \operatorname{diam}K$,
> and every point of $K$ other than $O_1,O_2$ is at distance strictly less than $d$ from each.

C1 is W0; C2 is W1 + W2 (W2's hypothesis "$O_1$ is a vertex of no inscribed equilateral triangle in
$S=K$" needs care: $O_1$ is exceptional for $\partial K$, and a triangle with vertices in $K$ and
one vertex at $O_1$ need not have its other vertices on $\partial K$ — but W2 only ever produces
triangles whose other two vertices are at distance exactly $d = \operatorname{diam}K$ from $O_1$,
and a point of $K$ at maximal distance from $O_1$ lies on $\partial K$, so the triangle produced is
inscribed in $\partial K$ and the contradiction stands). C3 is step (i) of W1 plus its strictness.

**6.1 Answering "can the two points be anywhere?"** Given *any* two distinct points $p,q$ there is
a convex body whose exceptional set is exactly $\{p,q\}$ — the $30$–$30$–$120$ triangle on base
$pq$. So no pair of positions is excluded a priori. But *given $K$*, the pair is pinned: it is the
unique diameter of $K$. Both halves matter, and they are the honest answer to the brief's question.

**6.2 Answering "is the angular relationship constrained?"** No. For any
$(\alpha_1,\alpha_2) \in (0°,60°)^2$ the triangle with angles
$\alpha_1, \alpha_2, 180° - \alpha_1 - \alpha_2$ has third angle $> 60°$ and hence exceptional set
exactly the two small-angle vertices. So the pair of cone openings is entirely free in the open
square; only the *metric* relation is rigid. (Proposition T then converts a small $\alpha_1+\alpha_2$
into thinness, so "free" does not mean "without consequence".)

**6.3 Answering "is the $30$–$30$–$120$ triangle the only shape?"** No, and not close. Every
triangle with two angles below $60°$ qualifies; so does the lens bounded by two circular arcs
meeting at angle $<60°$ at both corners; so do quadrilaterals inside $C_1 \cap C_2$. Precisely: the
convex bodies with $\lvert E\rvert = 2$ are exactly those contained in $C_1 \cap C_2$ for two cones
$C_i$ of opening $\le 60°$ with apexes $O_i \in \partial K$, each cone containing $K$, with the
$\alpha = 60°$ cases resolved by §5.4. Within that description $\operatorname{diam} = \lvert
O_1O_2\rvert$ is automatic (W1) rather than an extra condition. **The rigidity is metric, not
shape-theoretic**, and reporting the shape family as "the $30$–$30$–$120$ triangle and small
perturbations" would have been wrong.

---

## 7. The polygon census — `numerical`, evidence only

### 7.1 What is exact and what is not

**Exact:** every good/exceptional verdict, every diameter, every distance comparison, every
"interior angle $< 60°$" and "hull opening $< 60°$" test. Arithmetic is in
$K = \mathbb{Q}(\sqrt3)$ with `fractions.Fraction` coefficients and a hand-written sign algorithm
($a + b\sqrt3$: same-sign coefficients decide directly, mixed signs compare $a^2$ against $3b^2$).
No `sympy` geometry predicate is used anywhere, per the brief and this problem's
[`RULES.md`](../../RULES.md) §5. Angle *values* are printed as floats for the reader; no decision
is taken on one. **Float appears in exactly two places, neither of them a decision:** the random
generators, and the corroborating direction-sweep instrument of §7.3.

**Two independent deciders, both exact:**

1. **Rotation/intersection.** $O$ is good $\iff$ $J \cap \rho_{O,60°}(J) \supsetneq \{O\}$
   (Lemma R applied to $Y = \rho(X)$). Implemented as exact segment–segment intersection between
   every edge of $P$ and every edge of $\rho(P)$, with the collinear-overlap branch handled
   separately (an overlap of positive length contains a point $\ne O$).
2. **Direction sweep.** Derived here: for edges $e = [A,B]$, $f = [C,D]$ with $a = A-O$ etc. and
   $k_e = a \times b \ne 0$, the ray at direction $v$ meets $e$ at the single scale
   $k_e/(v \times (b-a))$; matching that against $f$ under $\rho v$ and using
   $\rho v \times m = v \times \rho^{-1}m$ collapses to the single linear condition
   $v \times M = 0$ with $M = k_e\,\rho^{-1}(d-c) - k_f\,(b-a)$. So only finitely many directions
   can be good (or, when $M = 0$, a whole cone whose extreme directions are vertex directions),
   and each candidate is decided by rebuilding the exact scale sets $S(v)$, $S(\rho v)$ —
   including the collinear-ray case where a scale set is a whole interval.

They share the field arithmetic and nothing else: one works in the plane, the other in direction
space, and their degeneracies are in different places. Agreement is therefore worth something; it
is not a proof of anything.

**Controls reproduced** ([`RULES.md`](../../RULES.md) §5 requires this *before* believing
anything): the equilateral triangle inscribed in itself (all three vertices good); the
$30$–$30$–$120$ wedge witness (both $30°$ apexes exceptional, $120°$ apex good, witness triangle
$(0,0),(\tfrac12,0),(\tfrac14,\tfrac{\sqrt3}{4})$ with side$^2 = \tfrac14$ exactly); the unit
square (all corners good); and a triangle with exactly one angle below $60°$.

**How much was cross-checked, exactly.** The census itself was decided by decider 1 alone; that is
its main weakness and it is stated rather than buried. Decider 2 was run against decider 1 on
**every vertex of the four controls, every vertex of the three §7.3 counterexamples, and $250$
boundary points on $15$ further random non-convex polygons** — about $287$ points, **zero
disagreements**. Separately, a witness re-verifier that knows nothing about how a triangle was
found (it rebuilds it, tests all three vertices for membership in $J$, and tests the three squared
side lengths for equality) accepted every "good" verdict on the controls and on all three
counterexamples — zero rejected witnesses.

**Reproducibility, honestly.** The census scripts were run in a scratch directory and are **not
committed**: `experiments/` is another worker's lane and [`../../../../RULES.md`](../../../../RULES.md)
§2 forbids me writing there. That means this section does **not** meet
[`../../../../RULES.md`](../../../../RULES.md) §4's "reproducible from a single command" bar, and it
should not be read as though it did. What is fully reproducible from this file alone are the three
**explicit integer-coordinate counterexamples of §7.3** and the controls above; anyone can re-decide
those with an independent checker, which is what this problem's `RULES.md` §3.3 actually asks for.
Seeds are `SEED = 20260829` plus $1/2/3$ per generator, CPython 3.11, standard library only.

### 7.2 The population

| population | polygons | vertices decided | edge-interior samples | $\lvert E\rvert$ histogram |
|---|---|---|---|---|
| convex (hulls of random integer points, $n \le 12$) | $2\,000$ | $10\,164$ | $10\,164$ | $0{:}1145$, $1{:}524$, $2{:}331$ |
| non-convex "star" ($n \le 14$) | $1\,200$ | $11\,342$ | $11\,342$ | $0{:}763$, $1{:}340$, $2{:}97$ |
| non-convex "spiky" ($n \le 14$, heavy-tailed radii) | $1\,200$ | $11\,236$ | $11\,236$ | $0{:}582$, $1{:}436$, $2{:}182$ |
| **total** | **$4\,400$** ($2\,300$ non-convex) | **$32\,742$** | **$32\,742$** | $0{:}2490$, $1{:}1300$, $2{:}610$ |

$65\,484$ boundary points decided exactly, in about $5$ minutes.

Two clean zeros. **(a)** Over the $10\,164$ convex vertices, the equivalence *good $\iff$ interior
angle $\ge 60°$* — which is what §5.2–§5.4 predict for polygons — held with **zero violations**.
**(b)** Of the $32\,742$ sampled edge-interior points, **zero** were exceptional, in agreement with
the same observation in [`../../../../experiments/inscribed-triangle-angular/`](../../../../experiments/inscribed-triangle-angular/README.md).
Neither zero is a proof; the second in particular is a *sample* of each edge, so this census
decides "$\lvert E \cap \text{vertices}\rvert$", not $\lvert E\rvert$, and every count above should
be read with that qualification.

### 7.3 W1 does **not** extend to non-convex curves — three exact counterexamples

Each polygon below has integer vertices, is simple (checked exactly), has exactly two exceptional
vertices, and has $\lvert O_1O_2\rvert^2 < \operatorname{diam}^2$ **in integers**, so the strict
inequality is not a numerical artefact. Both deciders agree on every vertex of all three; every
good vertex carries a re-verified witness triangle.

| # | vertices | $E$ | $\operatorname{diam}^2$ | $\lvert O_1O_2\rvert^2$ | ratio |
|---|---|---|---|---|---|
| **C2** | $(-10,-4),(-5,-14),(1,-4),(18,0),(-2,5)$ | $(-5,-14)$, $(18,0)$ | $800$ | $725$ | $0.9520$ |
| **C1** | $(-32,-15),(-15,-18),(-33,-37),(-10,-48),(-7,-45),(5,-57),(1,-13),(17,3),(42,36),(-27,33),(-32,18)$ | $(5,-57)$, $(42,36)$ | $10954$ | $10018$ | $0.9563$ |
| **C3** | $(0,0),(-1,-19),(11,-4),(5,7),(-3,6),(-10,17),(-16,5),(-20,0)$ | $(-1,-19)$, $(-20,0)$ | $1377$ | $722$ | $0.7241$ |

**C2 is a five-vertex integer pentagon** and is the cheapest thing in this lane for a reviewer to
re-decide independently. Its diameter is $(-10,-4)$–$(18,0)$ with $d^2 = 800$; its exceptional pair
is at $d^2 = 725$. It is also a **mixed pair**: $(18,0)$ *is* wedge-blocked (the whole polygon lies
in a $45.4°$ cone there) while $(-5,-14)$ is not (the polygon spans $85.2°$ there). That is an
exact integer-coordinate instance of the same mixed phenomenon
[`../spiral-tip-witness/`](../spiral-tip-witness/README.md) §10 reports numerically for
$J_{1,30°}$, arrived at by a completely different route.

**C3** was produced by a hill-climb (exact evaluation, heuristic search) minimising
$\lvert O_1O_2\rvert^2/\operatorname{diam}^2$ from a random start; it plateaued at $0.7241$ after
about $10$ minutes. The plateau is a local optimum of a discrete neighbourhood search, not a bound:
**I found no floor**, and I do not claim one — a plateau of a local search is evidence about the
search, not about the infimum. What can be said is that $0.7241$ is far enough below $1$ that the
"$\lvert O_1O_2\rvert = \operatorname{diam}$" conjecture is not merely failing at the margin, and
that the ratios I found are not clustered against any visible barrier.

**Corroboration by a second instrument.** A float direction sweep ($40\,000$ directions) computes,
at each point $O$, the minimal $\lvert s_1 - s_2 \rvert$ over $s_1 \in S(\theta)$,
$s_2 \in S(\theta+60°)$. On C1 this gap, normalised by the diameter, is $3.1\times10^{-2}$ at
$(5,-57)$ and $1.4\times10^{-1}$ at $(42,36)$, against $4\times10^{-6}$ and $5\times10^{-5}$ at two
good vertices — three to four orders of magnitude of separation. The instrument is float and
decides nothing; it is here because a bug that produced a false "exceptional" would have to fool it
too.

### 7.4 The wedge is not the only mechanism on polygons

Call $O$ **wedge-blocked** if the whole polygon lies in a closed cone of opening $< 60°$ at $O$ —
equivalently (exactly checkable) $O$ is a vertex of the convex hull whose hull opening is $< 60°$.

| population | exceptional points | not wedge-blocked | share |
|---|---|---|---|
| convex | $1\,186$ | $0$ | $0\%$ |
| star | $534$ | $116$ | $21.7\%$ |
| spiky | $800$ | $211$ | $26.4\%$ |

So roughly a quarter of the exceptional points on non-convex polygons are invisible to the wedge
test — the hull opening at such a point reached $103.7°$ in this run, i.e. there are pairs of curve
points subtending well over $60°$ there, and still no equilateral triangle. Until now the only
non-wedge exceptional point in this repository was the transcendental spiral tip of
[`../spiral-tip-witness/`](../spiral-tip-witness/README.md); these are **exact, integer, and
common**. Two side observations from the same data, both `numerical` and neither a theorem:

- every exceptional vertex found had **interior angle $< 60°$** — consistent with the containment
  recorded as A4 in [`../../README.md`](../../README.md). For a wedge-blocked vertex that is
  automatic (both incident edges lie in the blocking cone); the content is in the non-blocked ones,
  where the largest interior angle observed was $59.90°$;
- every exceptional point found was a **convex-hull vertex**. That regularity is *false in general*:
  at the spiral tip $O = 0$ of $J_{c,\beta}$ the curve meets every direction, so $0$ is interior to
  $\operatorname{conv}(J)$, and $O$ is exceptional — re-derived here in two lines in §8.2. So this
  is a polygon artefact, and a good example of why a census is evidence and not a classification.

### 7.5 …and W1's own prediction survives where it applies

W1 says: *if both exceptional points are $60°$-blocked, the pair is the diameter* — with no
convexity anywhere. Splitting the $610$ census pairs by how many of the two points are
wedge-blocked:

| both blocked | one blocked | neither blocked |
|---|---|---|
| $537$ pairs, **$537$ are the diameter pair** | $56$ pairs, $53$ are | $17$ pairs, $14$ are |

(of which the convex population contributes $331$ both-blocked pairs, all diameter). **Every one of
the six failures has at least one non-blocked point**, exactly as W1 requires; a single both-blocked
non-diameter pair would have refuted W1 outright. This is the strongest test in the lane, because
it is a falsifiable prediction of a theorem whose hypothesis is *not* convexity, checked on $2\,300$
non-convex polygons.

### 7.6 Consistency with the provisional Meyerson bound

Over all $65\,484$ exactly decided boundary points, the largest exceptional count on any polygon was
**2**; three never occurred. [`../../README.md`](../../README.md) row 2 records
$\lvert E(J)\rvert \le 2$ as `cited`\* — provisional, no source text read — and it is used here
**only** as this after-the-fact check. The check passes. It cannot promote the citation, and none of
§3–§6 used it.

---

## 8. $\lvert E(J)\rvert = 1$, and the two adversarial tests

### 8.1 One exceptional point is possible — no parity obstruction

> **Witness.** $T$ = the triangle with vertices $(0,0), (5,0), (2,4)$. Its exceptional set is
> exactly $\{(5,0)\}$.

*Proof.* $T$ is convex, so §5 applies at each vertex, and the criterion at a polygon vertex is
"interior angle $\ge 60°$" (§5.4). Exactly: at $(5,0)$ the edge vectors are $u = (-5,0)$,
$v = (-3,4)$ with $u\cdot v = 15 > 0$ and $4(u\cdot v)^2 = 900 > 625 = \lvert u\rvert^2\lvert
v\rvert^2$, so the angle is $< 60°$ and the vertex is exceptional. At $(0,0)$: $u = (5,0)$,
$v = (2,4)$, $u \cdot v = 10 > 0$, $4(u\cdot v)^2 = 400 < 500$, so the angle is $> 60°$ and the
vertex is good. At $(2,4)$: $u = (-2,-4)$, $v = (3,-4)$, $u\cdot v = 10 > 0$,
$400 < 500$, angle $> 60°$, good. Edge-interior points of a convex polygon have $\alpha = 180°$ and
are good by §5.3. All arithmetic is in $\mathbb{Z}$. $\square$

So $\lvert E \rvert$ takes the value $1$, and any "the exceptional points come in pairs" story is
dead. The census agrees emphatically — $1\,300$ of $4\,400$ polygons, in every population — and
Corollary C1 says what the single point must be even so: **an endpoint of a diameter**. In the
witness, $\operatorname{diam} = 5$ is attained by *two* pairs, $\{(0,0),(5,0)\}$ and
$\{(5,0),(2,4)\}$, both containing the exceptional point — which is exactly the situation W2 says
can only arise when fewer than two points are blocked.

### 8.2 The spiral witness, re-derived, and what it refutes here

The brief asked that any conjecture be tested against
[`../spiral-tip-witness/`](../spiral-tip-witness/README.md). That lane is `sketch` and I may not
assume it, so here is the only fact I use, re-derived from its **definition** (which is data, not a
claim): for $c>0$ and $\beta \in (0°,60°)$,
$J_{c,\beta} = \{0\} \cup S \cup e^{i\beta}S \cup \{e^{is} : 0 \le s \le \beta\}$ with
$S = \{e^{-ct}e^{it} : t \ge 0\}$.

*Claim: $O = 0$ is exceptional.* Each of $S$ and $e^{i\beta}S$ meets the circle of radius $r$ in
**exactly one** point for $0<r\le1$ and none for $r>1$, because $t \mapsto e^{-ct}$ is a strictly
decreasing bijection $[0,\infty)\to(0,1]$; the two points are $\beta$ apart in argument, and the
closing arc contributes only at $r=1$, in directions $[0,\beta]$. So for every $r>0$ the directions
of $J \cap \partial B(0,r)$ lie in a closed arc of length $\beta < 60°$, and Lemma R has no
solution. $\square$ *Two consequences for this lane:*

- $0$ lies in the **interior of $\operatorname{conv}(J_{c,\beta})$** (the curve meets every
  direction from $0$, at distance $\ge e^{-2\pi c}$), so an exceptional point need **not** be a
  hull vertex and need **not** be a diameter endpoint. §7.4's empirical regularity is refuted, and
  Corollary C1 is genuinely a convexity statement.
- The spiral lane additionally *observes numerically*, without asserting it, that
  $E(J_{1,30°}) = \{0, 1\}$ — a mixed pair. If that is right then $\lvert O_1O_2\rvert = 1$ while
  $\operatorname{diam}(J_{1,30°}) \ge 1 + e^{-\pi} \approx 1.0432$ (take $P_0 = 1$ and the point of
  $S$ at argument $180°$, which has radius $e^{-\pi}$), so W1 would fail there too. I did **not**
  verify that pair — deciding goodness at $P_0 = 1$ is a transcendental problem, not one my exact
  polygon machinery can touch — and I record it as a consistency observation, not as evidence.
  §7.3 settles the same question exactly, with integers, which is why it is the headline.

---

## 9. The three cheap filters ([`../../RULES.md`](../../RULES.md) §3)

**§3.1 wedge test — run, and it is the engine rather than an obstacle here.** The $30$–$30$–$120$
witness satisfies W1's hypothesis at both $30°$ apexes and is its **equality case** in every
respect: the pair is the diameter ($d = \sqrt3$), the pair is unique, and Proposition T is tight
($1/2 = \tfrac12 d\tan30°$). Nothing in §3 implies that every point of every curve is a vertex; the
theorems here are all about *which* points can fail, never about none failing.

**§3.2 square test — the argument does not transfer, and one line shows it.** Replace $60°$ by
$90°$. Theorem W0's proof needs $\cos\gamma \ge \tfrac12$ to get $a^2+b^2-2ab\cos\gamma \le
a^2+b^2-ab \le R^2$; at $\gamma = 90°$ the bound becomes $a^2+b^2$, which is $2R^2$, and the
conclusion fails. It fails *concretely and immediately*: the unit square is $90°$-blocked at all
four corners, and its diameter is the diagonal, not the side, so "two blocked points are the
diameter pair" is false for squares at the very first example. Theorem W1 likewise collapses —
$180° - 90° - 90° = 0°$, so the angle at $Z$ is unconstrained and step (i) proves nothing.
The existence half (§5.3) does not transfer either, for the standard reason recorded in
[`../../RULES.md`](../../RULES.md) §3.2: an equilateral triangle at $O$ is one scalar equation in
one unknown (the third vertex is $\rho(P)$), whereas a square at $O$ is two equations in one
unknown. **The lane is safe from proving too much: its central inequality is quantitatively false
at $90°$, not merely unproved.**

**§3.3 polygon control — run, and it is §7**, including the exact controls of §7.1 and $10\,164$
convex vertices re-deciding §5's criterion with zero violations. It also produced the lane's main
negative result (§7.3), which is what a control is for.

---

## 10. Regularity budget, per statement

| statement | assumptions on the object | other inputs |
|---|---|---|
| Lemma R (§2) | none — any $S \subseteq \mathbb{R}^2$ | isoceles-with-$60°$-apex is equilateral |
| §3.1 wedge obstruction | none | Lemma R |
| **W0, W1, W2 (§3)** | **none**; compactness only to turn $\sup$ into $\max$ in W0's last clause | law of cosines, law of sines, angle sum |
| Proposition T (§3.4) | none | inscribed-angle theorem |
| F1–F5, §5.2–§5.4 | $K$ convex compact, $\operatorname{int}K \ne \emptyset$, $O \in \partial K$ | supporting line; IVT on an interval; compactness for F4 |
| Corollaries C1–C3 (§6) | as §5 | W0–W2 |
| §8.1 witness | polygonal (one explicit triangle) | integer arithmetic |
| §8.2 spiral facts | one explicit curve | monotonicity of $t \mapsto e^{-ct}$ |
| §7 census | polygonal, rational/$\mathbb{Q}(\sqrt3)$ coordinates | exact arithmetic; **no** decision on a float |

Explicitly **not** consumed anywhere in §2–§6: the Jordan curve theorem, degree or winding number,
any measure or density argument, rectifiability, smoothness, any tangent direction, any limit of
triangles, any approximation of one curve by another. In particular
[`../../RULES.md`](../../RULES.md) §4's obligations for approximation arguments do not arise,
because there is no approximation argument.

---

## 11. Kill-criterion outcomes, and what is not proved

| criterion | outcome |
|---|---|
| **K1** — convex pair statement false | **did not fire.** $331/331$ convex census pairs are the unique diameter pair; no convex counterexample exists, and C2 proves none can. |
| **K2** — my convex re-derivation disagrees with `convex-vertex-criterion` | **did not fire.** Same conclusions, different proof of the existence half; $10\,164$ convex vertices decided identically by the criterion and by the exact decider. |
| **K3** — ratios scattered with no floor | **fired, in the non-convex population only.** Reported as the negative census it is (§7.3), including the counterexamples and the absence of any floor I could establish. The convex statement was stated *as* the convex statement from the start (KILL-CRITERION.md), so keeping it is not post-hoc narrowing. |
| **K4** — parity resolves trivially | **fired, as expected.** §8.1, exact witness; no further effort spent. |
| **K5** — three exceptional points | **did not fire.** Max $2$ over $65\,484$ points. |
| **K6** — refuted by a curve already in the repo | **partially fired.** The spiral tip refutes the hull-vertex regularity (§8.2) and would refute W1-for-general-curves if its mixed pair holds up; §7.3 refutes it exactly and independently anyway. |
| **K7** — one-hour compute budget | respected: about $50$ minutes total, every stage checkpointed to disk, no run left orphaned. |

**Not proved here.**

- **Nothing about $E(J)$ for a general Jordan curve.** §7.3 shows the natural conjecture is false;
  it does **not** produce a replacement. Whether *any* metric relation between two exceptional
  points holds for all Jordan curves is open as far as this lane is concerned, and §7.3's hill-climb
  found no floor, which is weak evidence against there being one.
- **No characterisation of non-wedge exceptional points**, on polygons or otherwise. §7.4 says they
  are common; it does not say what they are. This looks like the most promising thing to pick up
  next, and it is exactly where the repo's "rotating wedge is a mechanism, not a classification"
  warning already points.
- **No decision on the spiral mixed pair.** §8.2 states why my machinery cannot reach it.
- **The census decides vertices and samples edges**, so it bounds $\lvert E \cap \text{vertices}
  \rvert$ from below, not $\lvert E \rvert$ (§7.2). The three §7.3 counterexamples inherit that
  caveat: an unsampled exceptional edge point would make $\lvert E\rvert = 3$ there, which would be
  a far bigger event than this lane's claim — see K5, and note that the same caveat sits on every
  polygon count in this repository.
- **No status above `sketch`/`numerical`.** By [`../../../../RULES.md`](../../../../RULES.md) §5 I
  cannot grant `verified:review` to my own work, and nothing here belongs in `results/`.

## 12. Where to attack this hardest

1. **W2's equality analysis** (§3, case $O_1 \notin \{X,Y\}$): the claim that
   $a^2+b^2-ab = d^2$ on $[0,d]^2$ has solution set exactly $\{(d,0),(0,d),(d,d)\}$, and that the
   two equalities can be forced simultaneously. **[ATTACK HERE]**
2. **Step (i) of W1**, specifically the collinear cases and the use of "larger angle opposite longer
   side" when $\angle O_1ZO_2 = \angle ZO_2O_1$ exactly. **[ATTACK HERE]**
3. **§5.3's limit computations**, where upper semicontinuity is used at the endpoints and continuity
   in the interior; if a semicontinuity direction is flipped, the $h>0$ and $h<0$ branches break.
4. **§6's transfer of W2 from $S = K$ to $J = \partial K$** — the parenthetical argument that the
   equilateral triangle W2 produces has its other vertices on $\partial K$, not merely in $K$.
5. **The census code**, which is exactly the kind of artefact this session has watched fail five
   times. The three §7.3 polygons are printed in full precisely so that a reviewer can re-decide
   them without it.
