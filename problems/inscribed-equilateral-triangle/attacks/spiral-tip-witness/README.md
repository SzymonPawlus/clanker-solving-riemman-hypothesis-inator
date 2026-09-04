# The spiral tip: an exceptional point that the wedge obstruction does not see

```
regularity budget: Jordan + rectifiable — and both are *conclusions*, not hypotheses.
The witness is one explicit curve, given by a closed formula; nothing here is assumed
about a general Jordan curve, and no theorem about all Jordan curves is claimed. What
breaks first if you weaken "Jordan": nothing in this file, because Jordanness of the
witness is proved in §4 rather than assumed. What breaks if you weaken the *witness*:
see §5.4 — the construction dies at beta >= 60 degrees, sharply.
```

- Lane: **construction** (idea **I2** of
  [`../ideation-round-1/README.md`](../ideation-round-1/README.md)).
- Author: `claude` (Claude Opus 5), 2026-08-29, branch
  `claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md), **written before any computation
  in this lane** (see its provenance section for the honest qualification). Outcomes in §11.
- Journal: [`../../../../notebook/claude/2026-08-29-iet-spiral.md`](../../../../notebook/claude/2026-08-29-iet-spiral.md).
- Problem rules consumed: [`../../RULES.md`](../../RULES.md) §1 (budget line, above), §2
  (nondegeneracy — §2 below), §3.1 / §3.2 / §3.3 (three filters, all three run and all three
  reported — §9), §5 (exact arithmetic — §8 says exactly which steps are exact and which are
  float), §6 (statuses).

## Result table

| § | Statement | Status |
|---|---|---|
| §2 | **Lemma 1 (radial form of the criterion).** For any $S \subseteq \mathbb{R}^2$ and $O \in S$: $O$ is a vertex of a nondegenerate equilateral triangle with all vertices in $S$ $\iff$ there are $r>0$ and $\theta$ with $O + re^{i\theta} \in S$ and $O + re^{i(\theta+60°)} \in S$. | `sketch` — mine, re-derived from scratch here (§2.1), not imported |
| §3 | **Lemma 2 (rotating-wedge obstruction).** If for every $r>0$ the set $J \cap \partial B(O,r)$ lies in a closed circular arc of angular length $< 60°$ (an arc allowed to *depend on $r$*), then $O$ is exceptional. | `sketch` — mine; two lines from Lemma 1 |
| §4 | **The witness $J_{c,\beta}$ is a Jordan curve**, with interior identified exactly. | `sketch` — mine; explicit homeomorphism, no Jordan curve theorem used for the *construction*, used once for the interior |
| §5 | **Theorem 1.** For every $c>0$ and $\beta \in (0°,60°)$, $O = 0$ is an exceptional point of $J_{c,\beta}$. | `sketch` — mine; exact, four lines from Lemmas 1–2 |
| §6 | **Theorem 2.** The direction set of $J_{c,\beta}$ at $O$ is **all of $S^1$ at every scale**, so no wedge obstruction — local or global — applies at $O$. | `sketch` — mine |
| §7 | **Theorem 3.** $J_{c,\beta}$ is **rectifiable**, of total length $2\sqrt{1+c^2}/c + \beta$; and the unit-speed parametrisation is not differentiable at $O$, with chord/arc ratio the constant $c/\sqrt{1+c^2}$. | `sketch` — mine; the length is an elementary integral |
| §5.5 | **Corollary (all rotations at once).** $J \cap \rho_{O,\alpha}(J) = \{O\}$ for every $\alpha$ whose residue mod $360°$ lies in $(\beta,\,360° - \beta)$. | `sketch` — mine |
| §10 | **Corollary (all corner roles at once), hand-off to I3.** $O$ is a vertex of an inscribed triangle in the corner role (apex angle $\alpha$, adjacent-side ratio $\lambda$) **iff** $|\alpha + (\ln\lambda)/c| \le \beta \pmod{360°}$. | `sketch` — mine, and the least-checked statement in the file |
| §8 | Numerical cross-checks: embeddedness, disjointness, exceptional-point census | `numerical` — float, cross-check only; **no decision in §2–§7 rests on it** |

**Nothing here is assumable** ([`../../../../RULES.md`](../../../../RULES.md) §3), including by me.

**Dependency hygiene.** §2–§7 use only: elementary plane trigonometry, the fact that
$t \mapsto e^{-ct}$ is a strictly decreasing bijection $[0,\infty) \to (0,1]$, and — once, in §4.3
only, for identifying the interior — the Jordan curve theorem. In particular this file does **not**
import Observation R from [`../rotation-continuity/README.md`](../rotation-continuity/README.md) §2
or Proposition R from [`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md),
both of which are `sketch` and therefore unassumable; Lemma 1 is re-derived from scratch in §2.1 and
the agreement with those two lanes is reported in §2.2 as a *cross-check*, not as a dependency.
Meyerson's theorem is used nowhere as an input; it appears only in §10 as an external consistency
check **on** the conclusion, and [`../../README.md`](../../README.md) now marks it `cited`\* (provisional,
provenance P2, no source text read), which is another reason it must not be an input.

---

## 1. What this lane is for, and what would have made it fail

Every exceptional point this repository can currently exhibit is **wedge-obstructed**: the whole
curve lies in a cone of opening $< 60°$ at $O$, so no two points of $J$ subtend $60°$ there at all.
That is [`../../RULES.md`](../../RULES.md) §3.1, it is the mechanism behind the
$30$–$30$–$120$ witness of [`../rotation-continuity/README.md`](../rotation-continuity/README.md)
§3, and it is Theorem A of [`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md).
One mechanism, seen three times.

The question this lane asks is whether that is the *only* mechanism. It is not.

> **What this appears to show.** There is an explicit rectifiable Jordan curve with a point $O$ at
> which the achieved direction set is **all of $S^1$ at every scale** — so the wedge obstruction
> says nothing whatsoever — and which is nevertheless exceptional.

The hedge is deliberate ([`../../../../RULES.md`](../../../../RULES.md) §7, which applies
proportionally to any claim of novelty). Everything below is `sketch`: I wrote it, I checked it,
and by [`../../../../RULES.md`](../../../../RULES.md) §3 that is not enough for anyone — including
me — to build on it. §13 names the steps where I think an error would actually be, and the step I
am least sure of is §10's spiral-similarity corollary, not the main theorem. What would make this
claim collapse is a mistake in **Lemma 3**; everything else is bookkeeping on top of it.

The mechanism is different in a way that can be stated in one sentence: the wedge obstruction
confines $J$ to a narrow cone *once and for all*; the spiral tip confines $J$ to a narrow cone
**on each circle separately**, and lets that cone rotate as the radius shrinks. The union of the
cones is everything; the criterion never sees a union.

**The part that was genuinely at risk** — and which the ideation entry flagged as unproved — is
that the spiral arm has to *close up* into a Jordan curve, and the closing arc is part of $J$ too.
Criterion **K3c** of [`KILL-CRITERION.md`](./KILL-CRITERION.md) is the sharp form of the worry:
the arm accumulates on $O$, so the closing arc must reach $O$ through the complement of the arm,
and if that complement were disconnected in the wrong way there would be no construction at all.
§4.1 settles it: the complement of a spiral arm near its tip **is** connected, the closing arc must
therefore itself spiral into $O$, and the construction below is the choice that makes the resulting
two-armed configuration checkable in closed form.

---

## 2. Lemma 1 — the criterion, re-derived

> **Lemma 1.** Let $S \subseteq \mathbb{R}^2$ and $O \in S$. Then $O$ is a vertex of a
> **nondegenerate** equilateral triangle with all three vertices in $S$ **iff** there exist
> $r > 0$ and $\theta \in \mathbb{R}$ with
> $$O + re^{i\theta} \in S \quad\text{and}\quad O + re^{i(\theta + 60°)} \in S.$$

**regularity budget: none.** $S$ is used only as a set of points: not closed, not connected, not
injectively parametrised. This matters, because it means every use of Lemma 1 below is a
set-membership statement and no topology can leak in unnoticed.

### 2.1 Proof

Normalise $O = 0$ and identify $\mathbb{R}^2 = \mathbb{C}$.

($\Leftarrow$) Put $P = re^{i\theta}$, $Q = re^{i(\theta+60°)}$, both in $S$ by hypothesis. Then
$|OP| = |OQ| = r$, and by the law of cosines
$$|PQ|^2 = r^2 + r^2 - 2r^2\cos 60° = 2r^2 - r^2 = r^2 ,$$
so $|OP| = |OQ| = |PQ| = r$. Nondegeneracy ([`../../RULES.md`](../../RULES.md) §2): $r > 0$ is
given, so $P \ne O$ and $Q \ne O$; and $P \ne Q$ because $e^{i60°} \ne 1$. Three distinct points at
equal pairwise distance $r > 0$, i.e. a nondegenerate equilateral triangle of side exactly $r$.

($\Rightarrow$) Let $O, P, Q \in S$ be a nondegenerate equilateral triangle of side $s > 0$. Then
$|OP| = |OQ| = s$, so $P = se^{i\theta_P}$, $Q = se^{i\theta_Q}$ for some arguments, and by the law
of cosines again
$$\cos \angle POQ = \frac{s^2 + s^2 - s^2}{2s\cdot s} = \tfrac12,$$
so the unsigned angle $\angle POQ$ is $60°$, i.e. $\theta_Q - \theta_P \equiv \pm 60° \pmod{360°}$.
If $+$, take $r = s$, $\theta = \theta_P$; if $-$, take $r = s$, $\theta = \theta_Q$. $\square$

**Restated for use.** Define for each $r > 0$ the **direction set at radius $r$**
$$\Theta_S(r) \;=\; \{\,\theta \in \mathbb{R}/360° \;:\; O + re^{i\theta} \in S\,\}.$$
Then Lemma 1 says:

> $O$ is exceptional for $S$ $\iff$ for every $r > 0$, no two elements of $\Theta_S(r)$ differ by
> exactly $60°$ (mod $360°$).

This is the only form used below. Note it is a statement about **each circle separately**: the
criterion cannot compare points at different radii, and that is the whole leverage of this lane.

### 2.2 Cross-check, *not* a dependency

Lemma 1 is the polar restatement of "Observation R" in
[`../rotation-continuity/README.md`](../rotation-continuity/README.md) §2
($O$ good $\iff J \cap \rho_{O,60°}(J) \supsetneq \{O\}$) and of "Proposition R" in
[`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md) §1
($\Sigma(\theta) \cap \Sigma(\theta - \pi/3) \ne \emptyset$ for some $\theta$). I derived it before
re-reading either. The three agree, which is worth recording: **K1** of
[`KILL-CRITERION.md`](./KILL-CRITERION.md) would have halted the lane had they not. The two other
statements are `sketch`, so the agreement is decorrelation evidence only and confers nothing; and
note one real difference — the convex lane's Proposition R can drop the "mod $360°$" because
convexity puts all directions in a half-plane. **Here it cannot be dropped**, since our direction
sets wrap all the way round, and a version of Lemma 1 that quietly worked with unsigned differences
in $[0°,180°]$ instead of residues mod $360°$ would be a genuine error. It is used mod $360°$
throughout.

---

## 3. Lemma 2 — the rotating wedge

> **Lemma 2.** Let $J \subseteq \mathbb{R}^2$, $O \in J$. Suppose that for every $r > 0$ there is a
> closed arc $I_r \subseteq \mathbb{R}/360°$ of angular length $|I_r| < 60°$ with
> $\Theta_J(r) \subseteq I_r$. Then $O$ is exceptional for $J$.

*Proof.* Let $\theta, \theta' \in \Theta_J(r)$. Both lie in the closed arc $I_r$ of length
$|I_r| < 60° < 180°$, so the residue $\theta' - \theta \pmod{360°}$ lies in
$[-|I_r|, |I_r|]$, an interval containing neither $+60°$ nor $-60°$. By Lemma 1, $O$ is
exceptional. $\square$

**Why this is a second mechanism and not a rebranding of the first.** The wedge test of
[`../../RULES.md`](../../RULES.md) §3.1 is exactly the special case $I_r \equiv I$ **constant in
$r$**: then $J$ lies in the single cone $\{O + t u: t \ge 0,\, u \in I\}$ and the direction set
$\bigcup_r \Theta_J(r) \subseteq I$ is small. Lemma 2 permits $I_r$ to *rotate with $r$*, and then
$$\textstyle\bigcup_{r>0} I_r \ \text{ can be all of } \ \mathbb{R}/360°.$$
That is the whole content of this lane; §5 and §6 exhibit a curve where it happens.

**An honest limitation of Lemma 2.** It is a sufficient condition only. This lane says nothing
about whether *every* exceptional point is of wedge or rotating-wedge type — see §12.

---

## 4. The witness

**Definition.** Fix a **pitch** $c > 0$ and an **offset** $\beta$ with $0 < \beta < 60°$. Write
$O = 0$, identify $\mathbb{R}^2 = \mathbb{C}$, and set

$$S \;=\; \{\,e^{-ct}e^{it} \;:\; t \ge 0\,\}, \qquad
C \;=\; e^{i\beta}\,S \;=\; \{\,e^{-ct}e^{i(t+\beta)} : t \ge 0\,\}, \qquad
B \;=\; \{\,e^{is} : 0 \le s \le \beta\,\},$$

$$\boxed{\,J_{c,\beta} \;=\; \{0\} \,\cup\, S \,\cup\, C \,\cup\, B\,}$$

Two logarithmic spiral arms of the same pitch, one the other rotated by $\beta$, both winding into
$O$; closed off at the far end by the $\beta$-arc of the unit circle joining their outer endpoints
$P_0 = 1$ and $Q_0 = e^{i\beta}$. **Reference parameters used for the numerics: $c = 2$,
$\beta = 30°$.**

The essential feature is not "logarithmic": it is that each arm meets each circle about $O$
**exactly once**, and the two arms meet it $\beta$ apart. §12.1 states the general version.

### 4.1 Why there are two arms — the answer to kill-criterion K3c

A single arm spiralling into $O$ is an arc from $O$ to $P_0$; to close it into a Jordan curve one
needs a second arc from $P_0$ back to $O$, and that arc must reach $O$ **without meeting the first**.
That is possible, and only just: in the punctured disc $\{0 < |z| < \varepsilon\}$, the complement
of the arm is *connected* — pass to the universal cover $w = \log z$, where the arm's preimage is
the family of parallel lines $\{\operatorname{Re} w = -c(\operatorname{Im} w - 2\pi k)\}$, $k \in
\mathbb{Z}$; the complement is a disjoint union of parallel strips permuted transitively by the deck
transformation $w \mapsto w + 2\pi i$, so downstairs it is a single spiralling channel. Hence a
closing arc can reach $O$, but it must itself spiral in, through that channel, winding infinitely
often. **The closing arc is forced to be a second spiral tip.** K3c is therefore not met — but it is
the reason the construction has the shape it has, and it is why "close the arm up somewhere far
away" is not an option.

Given that, the choice above is the one that makes everything computable: take the second arm to be
a *congruent copy* of the first, so that the two arms stay a constant angle apart on every circle.

### 4.2 Radial normal form — the one computation everything rests on

> **Lemma 3.** Let $\tau(r) = -(\ln r)/c$, read mod $360°$. Then
> $$\Theta_J(r) = \begin{cases} \{\tau(r),\ \tau(r)+\beta\}, & 0 < r < 1,\\[2pt]
> [\,0,\ \beta\,], & r = 1,\\[2pt] \emptyset, & r > 1,\end{cases}$$
> and $0 \in J$. In particular $\Theta_J(r)$ is contained in a closed arc of length exactly
> $\beta$ for every $r > 0$.

*Proof.* $t \mapsto e^{-ct}$ is a strictly decreasing bijection $[0,\infty) \to (0,1]$; let
$t = \tau(r)$ be its inverse, so the point of $S$ at distance $r$ from $O$ exists iff
$0 < r \le 1$ and is then **unique**, namely $e^{-c\tau(r)}e^{i\tau(r)}$, of direction
$\tau(r) \bmod 360°$. Since $C = e^{i\beta}S$ is $S$ rotated about $O$, which changes no distance,
$C$'s point at distance $r$ is unique too and has direction $\tau(r) + \beta$. Every point of $B$
has $|z| = 1$ and the directions occurring are exactly $[0,\beta]$. Finally $\tau(1) = 0$, so at
$r = 1$ the contributions of $S$ and $C$ are the directions $0$ and $\beta$, already in $[0,\beta]$.
$\square$

This is exact: it uses no property of $\exp$ beyond strict monotonicity, and no floating point.

### 4.3 $J_{c,\beta}$ is a Jordan curve, and its interior is a spiral channel

> **Proposition 4.** $J = J_{c,\beta}$ is a Jordan curve. Its interior is
> $$\Omega \;=\; \{\, r\,e^{i(\tau(r)+t)} \;:\; 0 < r < 1,\ 0 < t < \beta \,\},$$
> an open spiral channel of angular width $\beta$ pinching to a point at $O$.

*Proof of Jordanness.* Define $\gamma$ on $[0,3]$ by
$$\gamma(u) = \begin{cases} 0, & u = 0,\\ e^{-ct(u)}e^{it(u)},\quad t(u) = \tfrac1u - 1, & 0 < u \le 1,\\ e^{i(u-1)\beta}, & 1 \le u \le 2,\\ e^{i\beta}\gamma(3-u), & 2 \le u \le 3.\end{cases}$$
Continuity: on $(0,1]$, $t(u)$ is continuous, and as $u \downarrow 0$, $t \to \infty$ and
$|\gamma(u)| = e^{-ct} \to 0 = \gamma(0)$. At $u=1$: $t(1) = 0$ gives $\gamma(1) = 1$, matching the
arc at $u=1$. At $u=2$: the arc gives $e^{i\beta}$, and $e^{i\beta}\gamma(1) = e^{i\beta}$. At
$u=3$: $e^{i\beta}\gamma(0) = 0 = \gamma(0)$, so $\gamma$ factors through the circle
$[0,3]/(0\!\sim\!3)$. Its image is $\{0\} \cup S \cup B \cup C = J$.

Injectivity, by Lemma 3. Two points with different moduli are different. At modulus $r \in (0,1)$
there are exactly two points of $J$, one on $S$ (direction $\tau(r)$) and one on $C$
(direction $\tau(r)+\beta$), distinct because $0 < \beta < 360°$; and $\gamma$ hits each once, since
$u \mapsto t(u)$ is injective on $(0,1]$ and likewise on $[2,3)$. At modulus $1$ the points are the
arc $B$, on which $\gamma|_{[1,2]}$ is injective, and its two ends coincide with $\gamma(1)$ from
$S$ and $\gamma(2)$ from $C$ as required. Modulus $0$ is $\gamma(0) = \gamma(3)$ only. So $\gamma$
is a continuous injection of a circle into the plane, i.e. $J$ is a Jordan curve. **No
approximation, no limit, and no Jordan curve theorem is used for this.**

*Proof of the interior.* The map $\Psi(r,t) = r e^{i(\tau(r)+t)}$ is a homeomorphism
$(0,\infty) \times (\mathbb{R}/360°) \to \mathbb{C}\setminus\{0\}$ — it is polar coordinates
composed with the shear $(r,t) \mapsto (r, t + \tau(r))$, both homeomorphisms. In $(r,t)$
coordinates, Lemma 3 says $J \setminus \{0\}$ is exactly
$\{0<r<1\} \times \{0,\beta\} \ \cup\ \{1\} \times [0,\beta]$. Hence
$\mathbb{C}\setminus J = W \sqcup V$ with
$$W = \Psi\big((0,1)\times(0,\beta)\big), \qquad
V = \Psi\big((0,\infty)\times(\beta,360°)\big) \cup \Psi\big((1,\infty)\times(\mathbb{R}/360°)\big),$$
both open. $W$ is connected and bounded; $V$ is connected (the two displayed pieces overlap on
$\{r>1\} \times (\beta,360°)$) and unbounded. By the Jordan curve theorem $\mathbb{C}\setminus J$
has exactly two components, so $\{W, V\}$ are they; $V$ is unbounded, hence $V = E$ and
$W = \Omega$. $\square$

Two remarks worth keeping. First, $\Omega$ contains **no** sector of positive aperture at $O$: at
radius $r$ it occupies only the arc $(\tau(r), \tau(r)+\beta)$, of width $\beta < 60°$. So the
sector criterion of [`../rotation-continuity/README.md`](../rotation-continuity/README.md) §5 is
inapplicable here, as it must be. Second, $J \cap B(O,\varepsilon)$ is not a crosscut of
$B(O,\varepsilon)$ for any $\varepsilon$ — it is two infinitely-winding arms — so Hypothesis (C) of
that lane's Theorem C fails at $O$, and it fails through its *cone* clause, not through the extra
component that lane worried about. §12.2 says why that is useful information for the rectifiable
lane.

---

## 5. Theorem 1 — $O$ is exceptional

> **Theorem 1.** For every $c > 0$ and every $\beta \in (0°, 60°)$, the point $O = 0$ is an
> **exceptional** point of the Jordan curve $J_{c,\beta}$: no equilateral triangle inscribed in
> $J_{c,\beta}$ has $O$ as a vertex.

*Proof.* By Lemma 3, for $0 < r < 1$ the set $\Theta_J(r) = \{\tau(r), \tau(r)+\beta\}$ is contained
in the closed arc $I_r = [\tau(r), \tau(r)+\beta]$ of length $\beta < 60°$; for $r = 1$,
$\Theta_J(1) = [0,\beta] = I_1$, also of length $\beta < 60°$; for $r > 1$, $\Theta_J(r) = \emptyset
\subseteq I_r$ for any choice. Apply Lemma 2. $\square$

That is the whole proof. Its brevity is the point: the construction was chosen so that global
disjointness is a statement about **one** circle at a time, and on each circle it is the trivial
observation that two directions $\beta$ apart are not $60°$ apart.

### 5.1 Global disjointness, pair by pair, as the brief demanded

The brief asked for every pairing to be ruled out explicitly rather than hand-waved. Lemma 3
does them all at once, but here they are separately, so that a cross-examiner can attack each.

| Pairing | Constraint from $|OP| = |OQ| = r$ | Angular difference forced | $= \pm60°$? |
|---|---|---|---|
| **arm $S$ vs arm $S$** | same $r$ $\Rightarrow$ same $t$ (strict monotonicity of $e^{-ct}$) $\Rightarrow$ **same point** | $0°$ | no |
| **arm $C$ vs arm $C$** | same, $C$ being a rotated copy of $S$ | $0°$ | no |
| **arm $S$ vs arm $C$** | $r$ determines the $S$-point and the $C$-point uniquely | exactly $\beta$ | no, since $0 < \beta < 60°$ |
| **arc $B$ vs arc $B$** | both at $r = 1$; directions in $[0,\beta]$ | at most $\beta$ | no |
| **arc $B$ vs arm $S$** | $B$ lives only at $r = 1$, where $S$'s only point is $P_0 = 1$, of direction $0 \in [0,\beta]$ | at most $\beta$ | no |
| **arc $B$ vs arm $C$** | at $r=1$, $C$'s only point is $Q_0 = e^{i\beta}$, direction $\beta \in [0,\beta]$ | at most $\beta$ | no |
| **anything vs $O$** | $r = 0$ | — | degenerate, excluded by §2 |

The arm-versus-arm rows use **only** that the radial function is *strictly* monotone — kill-criterion
**K2** would have fired on a merely weakly monotone arm, and does not. The rows involving $B$ are the
ones the ideation entry could not close, and they close because $B$ was placed at the **single**
radius that the arms attain at their outer endpoints, so it can only ever be compared against those
two points.

### 5.2 The size of the triangle that fails to exist

Theorem 1 is not an asymptotic or limiting statement, so [`../../RULES.md`](../../RULES.md) §2's
noncollapse worry does not arise: no sequence of triangles is taken, and no limit is claimed
nondegenerate. Lemma 1 associates to a putative triangle at $O$ its side length $r$, and the proof
excludes **every** $r > 0$ separately. There is nothing to collapse.

### 5.3 Where the quantifiers actually are

$O$ exceptional means: for all $r > 0$, for all pairs in $\Theta_J(r)$, the difference is not
$\pm60°$. The proof discharges the inner statement uniformly in $r$ by a single inequality
$\beta < 60°$, with a margin: the closest any pair on $J$ comes to subtending $60°$ at $O$ is
$60° - \beta = 30°$ for the reference parameters. The construction is therefore **stable**: it is
not a knife-edge coincidence, and nothing in it depends on a transcendental identity.

### 5.4 Sharpness in $\beta$, and what breaks at $\beta = 60°$

At $\beta = 60°$ the construction fails, and instructively: the arc $B$ then spans exactly $60°$,
so its own endpoints $P_0 = 1$ and $Q_0 = e^{i60°}$ are two points of $J$ at equal distance $1$
from $O$ subtending exactly $60°$ — and $\{O, P_0, Q_0\}$ is an inscribed equilateral triangle of
side $1$. $O$ is then a *good* vertex, by an explicit triangle. Likewise for $\beta > 60°$ the arc
contains such a pair. So the hypothesis $\beta < 60°$ is used, is necessary for this closing arc,
and its failure is visible rather than mysterious. (A cleverer closing arc that spirals *outward*
instead of running along a circle could relax this; it is not needed and is not pursued.)

### 5.5 Corollary: all rotations at once

> **Corollary 5.** For $J = J_{c,\beta}$ and any angle $\alpha$, writing $\bar\alpha \in [0°,360°)$
> for the residue of $\alpha$ mod $360°$,
> $$J \cap \rho_{O,\alpha}(J) = \{O\} \iff \beta < \bar\alpha < 360° - \beta .$$
> Equivalently, since $\rho_{O,\alpha}$ and $\rho_{O,-\alpha}$ produce the same triangles: **$O$ is
> the apex of an inscribed isosceles triangle of apex angle $\theta \in (0°,180°)$ if and only if
> $\theta \le \beta$.** Every apex angle above $\beta$ — including $60°$ and $90°$ — is blocked.

*Proof.* $z \in J \cap \rho_{O,\alpha}(J)$, $z \ne O$, means $|z| = r \in (0,1]$ with some
$\theta \in \Theta_J(r)$ equal to $\arg z$ and $\arg z - \alpha \in \Theta_J(r)$ (rotation about $O$
preserves $|z|$). For $r<1$, $\Theta_J(r) = \{\tau, \tau+\beta\}$, so this needs
$\alpha \equiv 0$ or $\pm\beta$. For $r = 1$, $\Theta_J(1) = [0,\beta]$, so it needs
$([0,\beta] - \alpha) \cap [0,\beta] \ne \emptyset$, which holds exactly when
$\bar\alpha \le \beta$ or $\bar\alpha \ge 360°-\beta$; and that condition already contains
$\alpha \equiv 0, \pm\beta$. Conversely each such $\alpha$ does give a $z$ on $B$, so the two
sides match. $\square$

Taking $\alpha = 60°$ recovers Theorem 1 in the language of
[`../rotation-continuity/README.md`](../rotation-continuity/README.md). Taking $\alpha = 90°$ gives
the statement used in the square test (§9.2). The corollary also says the exceptionality is *not*
fragile in $\alpha$: for the reference parameters $O$ is the apex of **no** inscribed isosceles
triangle whose apex angle exceeds $30°$ — the $60°$ case is one point of a whole blocked interval,
not a coincidence at one angle. §8.1 item 5 measures the transition and finds it at $30.0°$.

---

## 6. Theorem 2 — the direction set is full, so no wedge sees this

> **Theorem 2.** For every $\varepsilon > 0$,
> $$\Big\{\tfrac{z - O}{|z-O|} \;:\; z \in J_{c,\beta} \cap B(O,\varepsilon),\ z \ne O\Big\} \;=\; S^1 .$$
> Consequently there is **no** closed convex cone $K$ with apex $O$ and opening $< 360°$ such that
> $J \cap B(O,\varepsilon) \subseteq K$, for any $\varepsilon$ — a fortiori the wedge test of
> [`../../RULES.md`](../../RULES.md) §3.1, which requires opening $< 60°$ and containment of the
> *whole* curve, does not apply at $O$ even in its localised form.

*Proof.* Given a direction $\theta_0$ and $\varepsilon > 0$, choose an integer $k$ with
$\theta_0 + 360°k > \tau(\varepsilon)$; then $t = \theta_0 + 360°k \ge 0$ gives the point
$e^{-ct}e^{it} \in S$ of modulus $e^{-ct} < \varepsilon$ and direction $\theta_0$. $\square$

So at $O$ the two hypotheses that would ordinarily explain an exceptional point are both false: the
directions are unrestricted, and they are unrestricted **at every scale**. The obstruction lives
entirely in the pairing of direction with radius. This is the deliverable.

**Consequence for the convex lane.** [`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md)
Theorem B says that for a **convex** curve, $\alpha(O) > 60°$ implies $O$ is good. Here the cone
generated by $J - O$ is all of $\mathbb{R}^2$ ($\alpha(O) = 360°$ in that lane's normalisation, or
rather the notion degenerates), yet $O$ is exceptional. That is not a contradiction — that lane
hypothesises convexity throughout — but it does show the convexity hypothesis in Theorem B is
**not removable**, which is a sharper statement than "the proof uses convexity". I record it as an
observation about their theorem's hypotheses and claim nothing about their file.

---

## 7. Theorem 3 — the witness is rectifiable, and $O$ is a winding point

> **Theorem 3.** $J_{c,\beta}$ is rectifiable, of total length
> $$\mathcal{H}^1(J_{c,\beta}) \;=\; \frac{2\sqrt{1+c^2}}{c} \;+\; \beta \qquad (\beta\text{ in radians}),$$
> which for the reference parameters $c = 2$, $\beta = \pi/6$ is $\sqrt{5} + \pi/6 = 2.7595\ldots$
> Moreover, parametrising $S \cup \{O\}$ by arclength $s$ from $O$:
> $$|\gamma(s) - \gamma(0)| \;=\; \frac{c}{\sqrt{1+c^2}}\, s \quad\text{for all } s,$$
> so the chord/arc ratio at $O$ is the **constant** $c/\sqrt{1+c^2} \in (0,1)$, and $\gamma$ is
> **not differentiable at $O$**.

*Proof.* Parametrise $S$ by $t \mapsto e^{(-c+i)t}$, $t \in [0,\infty)$; then
$|\gamma'(t)| = |{-c+i}|\,e^{-ct} = \sqrt{1+c^2}\,e^{-ct}$ and
$\int_0^\infty \sqrt{1+c^2}\,e^{-ct}\,dt = \sqrt{1+c^2}/c < \infty$. $C = e^{i\beta}S$ is an
isometric copy, so it has the same length; $B$ is a unit-circle arc of length $\beta$. The three
overlap only in the two points $P_0, Q_0$, so the lengths add. For the second claim, the arclength
from $O$ to the point of parameter $t$ is $L(t) = \int_t^\infty \sqrt{1+c^2}e^{-c\sigma}d\sigma
= \sqrt{1+c^2}\,e^{-ct}/c$, whose value is exactly $\sqrt{1+c^2}/c$ times the modulus
$r = e^{-ct}$; so $r = cs/\sqrt{1+c^2}$ where $s = L(t)$. A unit-speed curve differentiable at $s=0$
would have $|\gamma(s)-\gamma(0)|/s \to 1$; here the ratio is constantly $c/\sqrt{1+c^2} < 1$.
$\square$

So **$O$ is a non-wedge exceptional point on a rectifiable Jordan curve.** Note *how* the tangent
fails to exist: not by oscillating in scale — the chord/arc ratio is literally constant — but by
**infinite winding**, $\arg(\gamma(s)) = \tau(r(s)) \to \infty$ as $s \downarrow 0$. This is the
cleanest possible failure of differentiability, and §12.2 records what it does and does not say for
the rectifiable lane.

For the reference parameters the geometry is concrete: each full turn multiplies the radius by
$e^{-2\pi c} = e^{-4\pi} \approx 3.49 \times 10^{-6}$, and the tip germ is exactly self-similar
under $z \mapsto e^{-2\pi c} z$, which is why numerics at one scale suffice (§8).

---

## 8. Exact versus numerical — what rests on what

[`../../RULES.md`](../../RULES.md) §5 requires exact arithmetic for decisions. Here is the ledger, and
kill-criterion **K5** is the reason it is explicit.

**Exact, no arithmetic in $\mathbb{R}$ at all.** Every step of §2–§7. The decisions are:
(i) $e^{-ct}$ is strictly decreasing — calculus, not computation; (ii) $0 < \beta < 60°$ — a
comparison between two chosen rational multiples of $\pi$ (for the reference parameters,
$\pi/6 < \pi/3$); (iii) $\beta \ne 0 \pmod{360°}$; (iv) two directions in an arc of length
$\beta$ differ by at most $\beta$. **No floating-point comparison decides anything.** The
transcendence of the logarithmic spiral is confined to the *parametrisation* and never enters a
decision, because Lemma 3 replaces "where is the curve" by "one point per radius per arm", which is
a statement about monotonicity.

**Float, and cross-check only.** Everything in this section. It can corroborate the above; it
cannot and does not support it.

### 8.1 What was checked, and the results

Script: [`../../../../notebook/claude/2026-08-29-iet-spiral.md`](../../../../notebook/claude/2026-08-29-iet-spiral.md)
carries the code inline and the exact invocation; it is `numpy` only, no seeds (deterministic), and
**no `sympy` geometry predicate is used anywhere** — segment predicates are reimplemented from
orientation sign tests, per **K4** and the repo's experience today of `Segment2D.intersection`
returning off-segment witnesses on 3 of 176 boundary cases.

The curve is discretised by truncating each arm at $|z| = r_{\min}$ and joining the two truncations
to $O$ by straight segments. **This is a different curve from $J$** — the truncation destroys the
tip — so these checks are corroboration of the *finite* part of the picture only.

1. **Criterion sanity (symbolic, `sympy` algebra, not geometry).** With $P = re^{i\theta}$,
   $Q = re^{i(\theta+60°)}$, all three of $|OP|, |OQ|, |PQ|$ simplify to $r$; and
   $\cos\angle POQ = 1/2$ from $|OP|=|OQ|=|PQ|=s$. Lemma 1 survives (**K1** not met).
2. **Embeddedness (K4).** Brute-force all-pairs non-adjacent segment-crossing test, own sign-test
   predicate, on discretisations with 950–15888 segments and $c \in \{0.3, 1, 2\}$,
   $\beta \in \{30°,55°\}$, down to $r_{\min} = 10^{-9}$ — up to 11 full turns of the spiral:
   **zero** non-adjacent crossings in every run (seven runs). Agrees with the exact injectivity
   proof of §4.3, which is the point of running it: two independent routes to the same answer.
3. **Radial normal form (Lemma 3).** For every sampled vertex of modulus $r < 1$, the direction
   deviates from $\{\tau(r), \tau(r)+\beta\}$ by at most $9.8\times10^{-15}$ — machine noise.
4. **The main claim.** No proper crossing of $J$ with $\rho_{O,60°}(J)$ in any run. Quantitatively,
   $\min_p \operatorname{dist}(\rho_{O,60°}(p), J)/|p|$ over vertices $p$ is
   **$0.4115$** ($c=2,\beta=30°$; $0.4117$ at the finer resolution), $0.1401$ ($c=0.3,\beta=30°$),
   $0.0604$ ($c=1,\beta=55°$) —
   scale-invariantly bounded away from $0$, as the self-similarity of §7 predicts, and shrinking as
   $\beta \to 60°$, as §5.4 predicts.
5. **Corollary 5, as a falsifiable prediction.** The gap $J$ vs $\rho_{O,\alpha}(J)$ was measured
   across $\alpha$. It is bounded away from zero exactly for $\beta < |\alpha| < 360°-\beta$ and
   zero for $|\alpha| \le \beta$ — the predicted transition, at the predicted place, in every
   parameter set tried. **A discrepancy here was the one real surprise of the lane and is recorded in
   §11 under K5**: at $|\alpha| < \beta$ the intersection is a *tangential overlap of two arcs of
   the same circle*, which a strict crossing-counter reports as zero. The counter was not wrong; it
   was the wrong instrument, and the distance-based detector shows the predicted behaviour. Had I
   read the crossing counts as the answer I would have recorded a false refutation of my own
   Corollary 5.

   The measured transition for the reference parameters ($c=2$, $\beta=30°$), gap normalised as in
   item 6:

   | $\alpha$ | $0.5°$ | $5°$ | $28°$ | $29.8°$ | **$30.2°$** | $32°$ | $45°$ | $60°$ | $90°$ | $180°$ | $332°$ | $359.5°$ |
   |---|---|---|---|---|---|---|---|---|---|---|---|---|
   | gap | $1.3\text{e-}6$ | $9.1\text{e-}6$ | $4.7\text{e-}6$ | $9.7\text{e-}6$ | $3.1\text{e-}3$ | $3.1\text{e-}2$ | $2.2\text{e-}1$ | $4.1\text{e-}1$ | $7.0\text{e-}1$ | $9.8\text{e-}1$ | $4.7\text{e-}6$ | $1.3\text{e-}6$ |

   Zero to machine noise for $|\alpha| \le \beta = 30°$, and lifting off immediately past it —
   the transition is at $30.0°$, not near it. The same table for $(c,\beta) = (0.3,30°)$ and
   $(1,55°)$ breaks at $30°$ and $55°$ respectively.
6. **Exceptional-point census (K6).** For each of 80 vertices $X$ along $J$, the *normalised gap*
   $$g(X) \;=\; \min_{p}\ \frac{\operatorname{dist}\big(\rho_{X,60°}(p),\ J\big)}{|p - X|}$$
   was computed over vertices $p$ of $J$, with $X$'s own neighbourhood excluded. $g(X) = 0$ means
   $X$ is a good vertex; $g(X)$ bounded away from $0$ is the signature of exceptionality. Numbers
   in §10.

   **The exclusion window is the subtle part, and I got it wrong first.** My initial version
   excluded $p$ within a fixed *metric* distance $10^{-3}\cdot\operatorname{diam}$ of $X$ — which,
   for an $X$ deep in the spiral at radius $10^{-6}$, swallows the entire inner spiral and measures
   only the far half of the curve. Every such $X$ then reported the same gap as $O$ itself, which
   would have read as "the whole inner spiral is exceptional" — i.e. as an apparent violation of
   Meyerson's bound produced entirely by my own instrument. The fix is an **index** window: the
   spiral is sampled geometrically, so a fixed number of vertices either side of $X$ is a fixed
   *relative* neighbourhood, which is what a self-similar tip requires. §11 (K6) records this.

---

## 9. The three filters ([`../../RULES.md`](../../RULES.md) §3), all run

### 9.1 Wedge test (§3.1)

**Run; it does not apply, and that is the result.** Theorem 2: the direction set at $O$ is all of
$S^1$ at every scale, so $J$ lies in no cone of opening $<60°$ — not globally, not locally. The
witness of §3.1 (the $30$–$30$–$120$ triangle) is the *other* mechanism; this file exhibits a point
that the §3.1 test certifies nothing about and that is exceptional anyway. The filter's own warning
("do not over-read it") is what this lane makes precise.

### 9.2 Square test (§3.2) — why nothing here transfers to squares

Run the construction verbatim with $90°$ in place of $60°$. Since $\beta < 60° < 90°$, Lemma 2's
argument goes through unchanged and gives: **$O$ is not a vertex of any square inscribed in $J$**
either (two adjacent square vertices are equidistant from $O$ and subtend $90°$), and more generally
Corollary 5 blocks every apex angle above $\beta$.

This produces **no** statement about the square peg problem, for a reason of logical polarity that
is worth stating rather than asserting:

- The square peg problem asks for the **existence** of *some* inscribed square. This lane produces a
  **non-existence** statement at *one specified point*. A curve can have — and this one does have —
  points that are not square vertices while still inscribing squares elsewhere. Exhibiting a
  non-vertex is not exhibiting a curve with no inscribed square, and no amount of such points adds
  up to one unless *all* points are non-vertices, which §10 shows is false here.
- More sharply: the substitution $60° \to 90°$ turns a true statement into another true statement
  about the *same* curve, and neither is a claim about all Jordan curves. There is nothing to
  transfer. The §3.2 reference non-transfer (three points close a triangle, four do not close a
  square) is not even reached, because this lane never closes a figure — it forbids one.
- The converse worry — *does this construction disprove something known?* — is §10.

**Pass.** A construction of counterexamples has the wrong polarity to prove an existence theorem,
and the $90°$ version is checked numerically too (§8.1 item 5's table: the gap between $J$ and
$\rho_{O,90°}(J)$ is $7.0\times10^{-1}$, i.e. they are nowhere near meeting).

### 9.3 Polygon control (§3.3) — honestly inapplicable, and why that itself is informative

> **[Correction, dispatcher, 2026-08-29 — this sub-claim is `refuted`.]** The
> `exceptional-set-polygons` lane exhibited an explicit **17-vertex rational simple polygon** whose
> tip is exceptional and **not** wedge-type: a polygonal spiral channel of constant angular width
> $w = \arcsin(3/5) \approx 36.87° < 60°$, wound through $221°$. Every circle about the tip meets
> $J$ in an arc of width $w$, so the tip is exceptional; but the directions from the tip span
> $258°$, so no cone of opening $< 60°$ contains $J$. Confirmed by the committed exact decider and
> by a second decider that lane wrote from scratch (own $\mathbb{Q}(\sqrt3)$, Cramer's rule rather
> than segment intersection): exactly one of the 17 vertices is exceptional.
>
> **The wrong step is "unboundedly many turns".** The rotating-wedge mechanism only needs the arc
> to be *narrower than $60°$ at each radius separately* — **finite** rotation suffices, and a
> polygon can supply it. So the mechanism this lane discovered is **not** exclusive to
> non-polygonal curves, and the polygon control is not inapplicable after all: it applies, and it
> refutes this sub-claim.
>
> This does not touch the lane's Theorems 1–3 or the spiral witness itself, which stand. What it
> removes is the belief that the mechanism cannot be seen on a polygon — and that belief was the
> stated reason for declaring the §3.3 control inapplicable. The witness also kills
> "exceptional $\Rightarrow$ hull vertex": its tip is interior to $\operatorname{conv}(J)$.


The problem's exact polygon enumerator (`experiments/inscribed-triangle-polygons/`) cannot check
this claim, and I did not pretend otherwise:

> **~~Every exceptional point of a simple polygon is wedge-type.~~ REFUTED — see the correction
> note immediately below.** A polygon has finitely many
> vertices and straight edges, so at each boundary point the curve locally occupies a fixed pair of
> directions; the rotating-wedge mechanism needs $I_r$ to rotate through unboundedly many turns as
> $r \to 0$, which requires infinitely many direction changes in every neighbourhood. *(`sketch`,
> mine, and stated as motivation rather than used.)*

So the mechanism of this lane is **invisible to polygons by construction**, and agreement with a
polygon census would have been evidence about nothing. This also disposes of an approximation route
([`../../RULES.md`](../../RULES.md) §4): truncating the spiral at any positive radius removes $O$ from the
curve entirely, so the exceptional point is *not* a limit of exceptional points of the truncations.
The infinitude of the winding is load-bearing, not decorative.

What was done instead is §8: a discretisation used only for embeddedness and for corroborating the
exact statements, with its own limitations stated.

---

## 10. Consistency with the literature — Meyerson's bound, handled per §7 discipline

[`../../README.md`](../../README.md) row 2 records **$|E(J)| \le 2$ for every Jordan curve** (Meyerson
1980), status `cited`\*, provenance P2 — no source text read, so provisional. Kill-criterion **K6**
requires me to treat an apparent excess of exceptional points as evidence of my own error.

**What is claimed here: $|E(J_{c,\beta})| \ge 1$, namely $O \in E(J_{c,\beta})$.** That is
compatible with the bound with room to spare, and no part of Theorem 1 is in tension with any row of
that table.

**Where a second or third exceptional point could come from.** The only two points of $J$ with a
corner are $P_0 = 1$ and $Q_0 = e^{i\beta}$. In the local coordinates of §4.3, expanding
$\tau(1-u) = u/c + O(u^2)$, the interior angle of $\Omega$ is $\arctan c$ at $P_0$ and
$90° + \arctan(1/c)$ at $Q_0$ (they sum to $180°$, a useful check). *(`sketch`, mine.)* So $Q_0$'s
angle always exceeds $90°$, while $P_0$'s is below $60°$ exactly when $c < \sqrt3$. **This is why the
reference pitch is $c = 2$**: it puts both corner angles above $60°$ ($63.43°$ and $116.57°$), so no
corner is even a candidate.

**What the numerics say, as `numerical` evidence only.** Normalised gaps $g(X)$ as defined in §8.1
item 6, index window $k = 8$, 80 sampled vertices per parameter set. A value at the discretisation
floor (a few times $10^{-2}$ here, set by the chord length) means "good"; a value an order of
magnitude above the floor is the signature of exceptionality.

| $(c,\beta)$ | $\arctan c$ | $g(O)$ | $g(P_0)$ | $g(Q_0)$ | census of 80: median / max | apparent $E(J)$ |
|---|---|---|---|---|---|---|
| **$(2, 30°)$ — reference** | $63.43°$ | **$4.12\times10^{-1}$** | $8.4\times10^{-4}$ | $2.5\times10^{-3}$ | $1.2\times10^{-2}$ / $3.5\times10^{-2}$ | $\{O\}$ |
| $(0.3, 30°)$ | $16.70°$ | **$1.40\times10^{-1}$** | $2.7\times10^{-4}$ | $3.4\times10^{-3}$ | $5.5\times10^{-4}$ / $7.4\times10^{-3}$ | $\{O\}$ |
| $(1, 30°)$ | $45°$ | **$3.23\times10^{-1}$** | **$2.77\times10^{-1}$** | $2.2\times10^{-3}$ | $9.0\times10^{-3}$ / $2.7\times10^{-2}$ | $\{O, P_0\}$ |
| $(1, 55°)$ | $45°$ | **$6.0\times10^{-2}$** | **$5.3\times10^{-2}$** | $8.8\times10^{-4}$ | $2.1\times10^{-3}$ / $6.3\times10^{-2}$ | $\{O, P_0\}$ |

Read this carefully, because it is the one place the lane touches the literature.

- **For the reference parameters the count is one.** $g(O)$ is more than an order of magnitude above
  every other sampled value, and both corners sit at the floor. Consistent with $E(J) = \{O\}$.
- **At $c = 1$ a second point appears exceptional**, namely the corner $P_0$, whose interior angle
  is then $45° < 60°$. That is $|E(J)| = 2$ — Meyerson's bound **attained**, and attained by a
  *mixed* pair: one ordinary wedge-type corner and one spiral tip. If it holds up it is a mildly
  interesting remark; it is `numerical` and I do not assert it.
- **Nothing produced three.** In every parameter set exactly one or two values stand clear of the
  floor, and $Q_0$ never does. Had a third appeared, **K6** required me to suspect my construction
  first, and §8.1 item 6 records the instrument bug that would have manufactured exactly that
  false positive if I had not caught it.
- **The behaviour at $P_0$ is not monotone in $c$** ($c = 0.3$: good; $c = 1$: exceptional;
  $c = 2$: good), which is what one expects when goodness at a sharp corner is decided by the
  *global* position of the far side of the curve rather than by the local angle — the "do not
  over-read the wedge test" warning of [`../../RULES.md`](../../RULES.md) §3.1, showing up on the
  other side.

None of this is a proof about $E(J)$: a finite sample cannot certify a negative at uncountably many
points, and the discretisation truncates the tip and so is a different curve. Only **Theorem 1** —
$O \in E(J)$, proved exactly in §5 — is claimed.

**Corollary for other triangle shapes — offered to idea I3, not developed here.** The same
bookkeeping with a spiral similarity $\sigma(z) = \lambda e^{i\alpha}z$ ($\lambda > 0$) in place of a
rotation gives, by the argument of Corollary 5 with $\tau(r/\lambda) = \tau(r) + (\ln\lambda)/c$:

> $O$ is a vertex of an inscribed triangle in the corner role with apex angle $\alpha$ and adjacent
> side ratio $\lambda$ **iff** $|\alpha + (\ln \lambda)/c| \le \beta \pmod{360°}$.

This is exactly the "pitch curve" that
[`../ideation-round-1/README.md`](../ideation-round-1/README.md) I3 predicted, with $\beta$
supplying a *band* rather than a curve because of the outer arc. **This is the least-checked
statement in this file** — I verified the $\lambda = 1$ case (Corollary 5) carefully and the
$\lambda \ne 1$ case once, and I did not check it numerically. It says $|E_T(J)| \ge 1$ for many
shapes $T$, never $\ge 3$, so it triggers no §7 concern; I record it as a hand-off to whoever claims
I3 and I do not build on it.

---

## 11. Kill-criterion outcomes

Against [`KILL-CRITERION.md`](./KILL-CRITERION.md), written before any computation here.

| # | Criterion | Outcome |
|---|---|---|
| **K1** | criterion itself wrong | **not met.** Re-derived from scratch (§2.1); agrees with both other lanes' forms, with the mod-$360°$ caveat of §2.2 recorded. |
| **K2** | arm-vs-arm not clean | **not met.** Strict monotonicity of $e^{-ct}$ gives it in one line (§5.1, row 1). |
| **K3** | global disjointness cannot be closed | **not met — this is the lane's substance.** Closed by Lemma 3: the closing arc is placed at the single radius $r=1$, so it meets only $P_0$ and $Q_0$ in the comparison. K3a and K3b do not arise; **K3c was the real obstacle** and is resolved, not dodged, in §4.1 — the closing arc genuinely cannot avoid spiralling into $O$, and the construction accepts that and makes it a second congruent arm. |
| **K4** | not a Jordan curve | **not met.** Exact injectivity proof (§4.3) plus an independent brute-force all-pairs check on five discretisations (§8.1 item 2), agreeing. |
| **K5** | a float decides something | **not met**, and the ledger is §8. The one place a float nearly misled me is recorded honestly: proper-crossing counts at $|\alpha| < \beta$ read as zero because the true intersection there is a *tangential* overlap along the unit circle, and the count was unstable under refinement ($5$ crossings at one resolution, $0$ at another). Had I let that decide anything I would have "refuted" my own Corollary 5. The decision instrument was replaced by a distance-based one; no §2–§7 statement ever depended on either. |
| **K6** | three or more exceptional points | **not met**, but it came closest of any criterion, and by my own error. One point is claimed, $O$. The first census *appeared* to make the entire inner spiral exceptional — which would have been an apparent violation of Meyerson's bound — and the cause was my exclusion window, a fixed metric radius that swallowed the whole inner spiral for any $X$ near $O$ (§8.1 item 6). Fixed to an index window; the count is then one for the reference parameters and two at $c = 1$, where the sharp corner $P_0$ also appears exceptional. Two is Meyerson's bound, attained, not exceeded. §10 has the table and the caveats. **This is exactly the failure mode K6 exists to catch, and it was caught by the criterion rather than by luck.** |
| **K7** | already someone else's example | **unresolved, and must stay so here.** No scholarly host is reachable from this session ([`../../README.md`](../../README.md) provenance warning), so I could not look. Spiral examples are natural enough that an expert may well know this one; the ideation entry guessed ~40% already known. Per [`../../RULES.md`](../../RULES.md) §6.1, **"not found" is not evidence of novelty**, and this file claims none. |

**Verdict: the construction stands.** The witness exists, global disjointness closed, and it is
rectifiable.

---

## 12. What this does *not* show, and what to do next

### 12.1 The generalisation, so that nobody over-reads the log spiral

Nothing in §5 uses the logarithmic form. The same proof gives:

> Let $\theta_1, \theta_2 : (0,1] \to \mathbb{R}/360°$ be continuous, and let the two arms be
> $A_i = \{r e^{i\theta_i(r)} : 0 < r \le 1\}$ — so each arm meets each circle $\partial B(O,r)$,
> $0 < r \le 1$, in **exactly one point**, and each accumulates only at $O$. Close them at $r=1$ by
> an arc $B'$ of $\partial B(O,1)$ running from $e^{i\theta_1(1)}$ to $e^{i\theta_2(1)}$. If, for
> every $r \in (0,1]$, the set $\{\theta_1(r), \theta_2(r)\}$ — together with the directions spanned
> by $B'$ when $r = 1$ — lies in an arc of length $< 60°$, then the tip is exceptional. *(`sketch`,
> mine; it is Lemma 2 with Lemma 3 replaced by the hypothesis.)*

Taking $\theta_i$ monotone with $\theta_i(r) \to \infty$ as $r \downarrow 0$ makes the direction set
full, which is the interesting case; $\theta_i(r) = -(\ln r)/c$ and $-(\ln r)/c + \beta$ is the
witness above. Rectifiability holds iff $\int_0^1 \sqrt{1 + r^2\,\theta_i'(r)^2}\,dr < \infty$,
which **fails** for spirals that wind fast enough (e.g. $\theta_i(r) = 1/r$). So **rectifiability is
a property of the choice, not of the mechanism**: a non-rectifiable version of this witness exists
too, and the rectifiable one was chosen deliberately because it is the one that bears on §12.2.

### 12.2 For the rectifiable lane (owned elsewhere — this is a note, not work in their file)

[`../rectifiable-case/README.md`](../rectifiable-case/README.md) records the open question of
whether $\mathcal{H}^1$-a.e. point of a rectifiable Jordan curve is a vertex, and notes correctly
that no "every point" statement can hold. This witness adds three things, all of which are `sketch`
and none of which resolves their question:

1. The exceptional point can be a **winding point** rather than a corner — a point where the
   unit-speed parametrisation fails to be differentiable with chord/arc ratio constant (§7). So the
   a.e.-differentiability route cannot be pushed to "all points of positive lower density" or
   similar without excluding winding, and the exceptional set of a rectifiable curve is not confined
   to corners.
2. It is a **non-wedge** exceptional point on a rectifiable curve, which is what makes it different
   from the $30$–$30$–$120$ triangle they already cite.
3. It is *not* a counterexample to their target: $O$ is a single point, hence $\mathcal{H}^1$-null,
   and it is exactly a non-differentiability point, so an a.e. statement survives it untouched.

### 12.3 The question this lane opens and does not answer

Lemma 2 subsumes the wedge test and certifies a strictly larger class of exceptional points (§3).
**Is every
exceptional point of every Jordan curve of rotating-wedge type?** — i.e. does $O \in E(J)$ imply
that $\Theta_J(r)$ lies in an arc of length $< 60°$ for every $r$? It does **not**: $\Theta_J(r)$
need only avoid $60°$-separated pairs, and e.g. $\Theta_J(r) = \{0°, 100°, 200°\}$ does that without
lying in any small arc. So the honest statement is that rotating-wedge is a mechanism, not a
classification, and the classification question — what can $\{\Theta_J(r)\}_{r>0}$ look like at an
exceptional point of a Jordan curve? — is open as far as this lane knows, and is the natural
successor issue. It is also the right frame in which to ask why the bound is **two** and not one:
nothing in this file explains that, and any claimed proof of Meyerson's bound from this machinery
should be regarded with the suspicion of [`../../../../RULES.md`](../../../../RULES.md) §7.

### 12.4 Lean

Lemma 1 and Lemma 2 are plain plane geometry with no topology, in the same class that
[`../../RULES.md`](../../RULES.md) §6.3 identifies as reachable (`Geometry.Euclidean.Angle.*`). Lemma 3 is
monotonicity of `Real.exp`. **Proposition 4 (Jordanness) is not** a Lean target: it needs the Jordan
curve theorem for the interior, absent from Mathlib per that section. A worthwhile formalisation
target is therefore "Lemma 1 + Lemma 2 + Lemma 3 $\Rightarrow$ no equilateral triangle inscribed in
the *set* $J_{c,\beta}$ has $O$ as a vertex", which is Theorem 1 with the word *Jordan* removed —
and which is the entire mathematical content.

---

## 13. For a cross-examiner: where to attack

Ranked by where I think an error would actually be, not by where the argument looks hardest.

1. **Lemma 3, the $r = 1$ row.** Everything funnels through it. The arc $B$ is the only part of $J$
   that occupies a whole interval of directions at one radius, so if any point of $B$ had modulus
   $\ne 1$, or if $S$ or $C$ had a second point at modulus $1$, §5.1's last three rows collapse.
   Reconstruct it from the definition of $J$, not from my table.
2. **Lemma 1's mod-$360°$ bookkeeping (§2.2).** The convex lane can work with unsigned differences
   in $[0°,180°]$; here the direction sets wrap. Check that Lemma 2's step "the residue lies in
   $[-|I_r|, |I_r|]$" is right for an arc of length $\beta$ placed anywhere on the circle, including
   across $0°$.
3. **§4.3's identification $\Omega = W$.** I use the Jordan curve theorem exactly once, to say
   $\mathbb{C}\setminus J$ has two components, and then argue $V$ is unbounded so $W$ is the
   interior. Check that $V$ is connected — the two displayed pieces must genuinely overlap — and
   that $\Psi$ is a homeomorphism and not merely a bijection.
4. **Injectivity of $\gamma$ at the junctions** ($u = 1$, $u = 2$, $u = 0 \sim 3$), which is where a
   "Jordan curve" that is not one would hide.
5. **§10's corner-angle computation** and the claim it supports. It is a first-order expansion and I
   did not do it to second order; if it is wrong, the claim "$E(J) = \{O\}$" weakens (though
   Theorem 1 does not).
6. **§10's spiral-similarity corollary**, which I flag myself as the least-checked line in the file.

What I am *most* confident of: Theorem 1, which is four lines from Lemma 3 and does not touch
topology at all. What I am *least* confident of: anything in §10 beyond "$O$ is exceptional".
