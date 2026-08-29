# Cross-examination: round 2 (rectifiable-case, spiral-tip-witness, half-density-obstruction)

**Examiner: Claude Sonnet 5, 2026-08-29, same conversation as the authoring workers.**

**This is not cross-family review.** Per [`../../../../RULES.md`](../../../../RULES.md) §5 and
§8, `verified:review` requires an examiner from a *different model family* than the author.
Sonnet 5 and Opus 5 (the author of all three claims below) are the same family — the closest
decorrelation available today, with Codex unavailable, but explicitly **not** the thing §5 asks
for. **No status is granted by this file.** Every claim below stays `sketch`, exactly as its own
lane recorded, pending a genuine cross-family (Codex) or human review. What follows is a real
attempt at the reconstruction §5 describes, offered as due diligence and a map of where to look
next, not as a promotion.

Method, per [`../../RULES.md`](../../RULES.md) §6.2 and the repo `RULES.md` §5: each claim was
restated independently, each step re-derived from the definitions (not read and agreed with), and
attacked at the standard failure points before being accepted. Two computational claims were
re-verified with fresh, independently written exact arithmetic — not the authors' code, no
`sympy` geometry predicates.

---

## Verdict 1 — Theorem T, `attacks/rectifiable-case/README.md`

> If the arclength parametrisation of a rectifiable Jordan curve is differentiable at $t_0$, then
> $\gamma(t_0)$ is a vertex of an inscribed equilateral triangle.

```
status: sketch (unchanged — same-family examination cannot promote it)
examined-by: Claude Sonnet 5 (claude), 2026-08-29 — same model family as the author (Claude
             Opus 5); this does NOT satisfy RULES.md §5's cross-family requirement
depends-on: the Jordan curve theorem (classical, not `cited` in this repo, not in Mathlib per
            problems/inscribed-equilateral-triangle/RULES.md §6.3), Lebesgue's a.e.-differentiability
            of Lipschitz functions, the area formula for injective Lipschitz maps R -> R^2 — all
            standard real analysis, used correctly and only where declared. No dependency on any
            other lane's sketch (Lemma 3/no-nesting is re-derived from scratch in the file, as it
            claims).
```

**Restatement in my own words.** Parametrise $J$ by arclength $\gamma:\mathbb R/L\mathbb Z\to
\mathbb R^2$ (1-Lipschitz, injective, $|\gamma'|=1$ a.e.). If $\gamma$ has an honest derivative of
unit length at one parameter $t_0$, then $O=\gamma(t_0)$ — one single point — is provably a vertex
of *some* inscribed equilateral triangle, whose side length the proof does not control (only that
it's macroscopic). I could restate this precisely, which per §5.1 is the first bar.

**What I independently reconstructed, line by line, without reading the proof text first for the
steps that mattered:**

- The differentiability estimate (1) and its two consequences (2)–(3): re-derived the bound
  $\sin\theta(s)\le 1/3$, i.e. $\theta(s)<\arcsin(1/3)\approx19.47°<30°$, directly from
  $|\gamma(s)-O-(s-t_0)u|\le\frac14|s-t_0|$ by decomposing into components parallel/perpendicular
  to $u$. Matches.
- **Lemma 0** (cone confinement forces macroscopic triangles): re-derived; correct, and it is what
  kills the "purely local" route the lane reports as refuted — I agree that route is dead for the
  stated reason.
- **Lemma 1** (localisation by compactness + injectivity): re-derived the compactness argument
  independently (sequence $s_n$, subsequential limit $s^*$, continuity forces $\gamma(s^*)=O$,
  contradicting injectivity since $d(s^*,t_0)\ge\delta>0$). Correct, and genuinely uses only
  Jordan (injectivity + continuity), no rectifiability.
- **Corollary 1.1** ($\mathcal H^1(J\cap B(O,\rho))\le\frac83\rho$): re-derived the parameter-window
  bound $|s-t_0|<\frac43\rho$ from (2), and the area-formula step ($\mathcal H^1(\gamma(A))=|A|$
  for injective arclength parametrisations — a standard, citable real-analysis fact, used
  correctly). Constant $8/3$ confirmed independently.
- **Sub-lemma 2a** (the Banach-indicatrix-style partition inequality $\int\#h^{-1}(y)\,dy\le
  \mathrm{Var}(h)$) — this is the "proved inline in four lines" step the dispatcher flagged as the
  kind that hides a factor. I re-derived it from the definitions: partition into $n$ pieces,
  $\int N_n(y)\,dy=\sum_i\mathrm{osc}_{I_i}(h)\le\sum_i\mathrm{Var}_{I_i}(h)=\mathrm{Var}(h)$
  exactly (additivity of variation over a partition, not merely an inequality), then Fatou against
  $\#h^{-1}(y)\le\liminf_n N_n(y)$. This is correct and standard; I found no hidden factor.
- **Lemma 2** (some $\tau<\rho$ has exactly two crossings): re-derived the full chain —
  $\int_0^\rho m^+(\tau)\,d\tau\le\frac43\rho$ from Sub-lemma 2a applied to $g$ on
  $[t_0,t_0+\frac43\rho]$ (variation $\le$ length of interval since $g$ is 1-Lipschitz), hence
  $|\{m^+\ge2\}|\le\frac13\rho$ by a direct Markov/Chebyshev-style bound
  ($\int(m^+-1)\ge|\{m^+\ge2\}|$ since $m^+\ge1$ everywhere on $(0,\rho)$), same for $m^-$, giving
  $|\{m^++m^-\ge3\}|\le\frac23\rho<\rho$. **I confirm both constants, $8/3$ and $2/3$,
  independently**, and confirm $2/3<1$ is the load-bearing inequality that makes the bad set a
  proper subset of the interval it lives in.
- **The $140°$ claim**: re-derived from the angular bound $\theta(s)<\arcsin(1/3)$: the two
  surviving points $p^\pm$ have directions within $\arcsin(1/3)\approx19.47°$ of $\pm u$
  respectively, so their angular separation lies in $[180°-2\arcsin(1/3),\,180°+2\arcsin(1/3)]
  \approx[141.06°,218.94°]$ — confirming both stated bounds ($>140°$, $<220°$) with margin, and
  confirming both resulting arcs of $\partial B(O,\tau)\setminus\{p^+,p^-\}$ have width $>140°>60°$.
- **Lemma 3 (no-nesting)** — the step the lane itself names as weakest and asks to be re-derived,
  not read. I did this from the bare statement, not the proof text, working the case split (does
  $R(J)\setminus\{O\}$ sit inside $\Omega$ or $E$?) myself: the nested case forces, via
  isometry-invariance of Lebesgue measure and "an open set inside a null set is empty", the
  identity $\overline\Omega=\overline{\Omega'}$ and hence $J=J'$, contradicting
  $J\cap J'=\{O\}$; the externally-tangent sub-case is killed by exhibiting an open positive-measure
  subset of $\Omega'\setminus\Omega$ from a boundary point of $J$, contradicting equal finite
  measures. My derivation landed in the same place as the file's proof (and, independently, as the
  neighbouring `half-density-obstruction` lane's Lemma A, which I also re-derived — see Verdict 3).
  Three independent derivations by two different lanes of this same problem's author, agreeing, is
  weak decorrelation evidence (same author, same session) but the *content* of each derivation is
  self-contained and I checked it on its own terms, not by comparison. **I could not break it.**
- **The "$\Omega$ meets $\partial B(O,\tau)$" step**: re-derived that $O\in\partial\Omega$ gives a
  point of $\Omega$ arbitrarily close to $O$, hence inside $B(O,\tau)$; that
  $\Omega\not\subseteq\overline{B(O,\tau)}$ follows from $\varepsilon<\mathrm{diam}(J)/2$; and that
  connectedness of $\Omega$ plus the intermediate value theorem on $x\mapsto|x-O|$ then produces a
  point of $\Omega$ at distance exactly $\tau$. Correct.

**Consistency check with the spiral-tip witness — the specific item the dispatcher asked for.**
Verified by direct computation, not just agreement-in-principle: the spiral tip's Theorem 3 gives
chord/arc ratio $c/\sqrt{1+c^2}$, a **constant strictly less than 1** for every $c>0$ (since
$c^2<1+c^2$ always). If $\gamma$ were differentiable at $s=0$ with $|\gamma'(0)|=1$, the definition
of the derivative forces $|\gamma(s)-\gamma(0)|/s\to1$ as $s\to0$. A ratio that is *identically*
$c/\sqrt{1+c^2}\ne1$ for all $s$ is stronger than merely failing to converge to 1 — it rules out
unit-speed differentiability at the tip outright. So the spiral tip's exceptional point is exactly
a non-differentiability point of the required kind, Theorem T's hypothesis never fires there, and
Corollary T3 ("no rectifiable exceptional point with differentiable unit-speed parametrisation") is
not violated. **The two results do not collide; I confirm this independently rather than taking
either lane's word for it.**

**Attempts to break it, and what survived.**

- Attacked the ordering of quantifiers in Corollary 1.1 / Lemma 2 for a hidden circularity (does
  $\varepsilon$ depend on $\rho$ in a way that invalidates "for every $\rho\le\varepsilon$")? No —
  $\varepsilon$ is fixed once from $\delta$, then $\rho$ ranges freely below it; no circularity.
  Redid the constraint bookkeeping for the ordering "$\varepsilon<\frac34\delta$" then "$\varepsilon
  <\frac12\mathrm{diam}(J)$" and confirmed shrinking $\varepsilon$ a second time doesn't invalidate
  the first constraint (both are upper bounds on $\varepsilon$, compatible).
- Attacked whether $\delta$ from differentiability could be larger than half the curve's total
  length, making the parameter window $(t_0-\delta,t_0+\delta)$ wrap around $\mathbb R/L\mathbb Z$
  and break the "compact complement" argument in Lemma 1. This is a real gap in the exposition
  (never stated), but not a real gap in the mathematics: differentiability at $t_0$ gives *some*
  valid $\delta$, and (1) holds a fortiori for any smaller $\delta$, so replacing $\delta$ by
  $\min(\delta, L/4)$ before invoking Lemma 1 repairs it with no cost. **Minor, cosmetic, does not
  affect the verdict.**
- Attacked the claim "$\#(J\cap\partial B(O,\tau))=m^+(\tau)+m^-(\tau)$" for double-counting risk
  if a forward and a backward parameter mapped to the same point of $J$. Ruled out by injectivity
  of $\gamma$ directly (distinct parameters, distinct points), no gap.
- Tried to find a curve satisfying (1)–(3) at $t_0$ while having a *third* strand pass through
  $B(O,\varepsilon)$ at every scale simultaneously with the forward/backward strands, to see if
  Lemma 2's $\frac23\rho$ bound could be pushed to $\rho$ (vacuous). Could not: the bound comes from
  an absolute Lipschitz-variation budget ($\frac43\rho$ over each half-window) that a third strand
  must also spend, and the arithmetic ($\frac43\rho-\rho=\frac13\rho$ per side) is a hard ceiling,
  not an estimate that degrades with more strands — more strands make the excluded-radius set
  *larger*, never removes the bound's validity, they just fall inside the already-excluded
  $\frac23\rho$ measure or force the point count for that side above 1, which is exactly what's
  being bounded.

**not-checked:** I did not attempt to verify that "$\mathcal H^1(\gamma(A))=|A|$ for injective,
arclength-parametrised, a.e.-unit-speed $\gamma$" is stated with full generality correctly (I know
this fact from standard real analysis — the area formula for injective Lipschitz curves — but did
not re-derive it from first principles the way I did the rest; it is standard and I am treating it
as such, the way the file itself does). This is not load-bearing for Theorem T's main line (the
file itself flags it as removable, used only for the density remark and Corollary T1, not for
Theorem T proper), so it does not weaken the verdict on Theorem T, but it does mean **Corollary T1
(the a.e. statement) rests on one fact I took on trust** rather than re-derived.

**Strongest residual objection.** None that survives scrutiny. This is a carefully built,
correctly compressed argument; every constant I checked ($8/3$, $2/3$, $140°$, $\arcsin(1/3)$)
came out exactly as claimed, and the step the lane itself flagged as weakest (Lemma 3) held up
under an independent from-scratch derivation. The honest caveat is only in scope, not in
correctness: Theorem T is a genuinely narrower statement than Meyerson's reported theorem (a.e. on
rectifiable curves with a differentiability hypothesis at the point, vs. all-but-two on arbitrary
Jordan curves), and the file says so plainly (§8, §10).

---

## Verdict 2 — the spiral-tip witness, `attacks/spiral-tip-witness/README.md`

> $J=\{0\}\cup S\cup e^{i\beta}S\cup\mathrm{arc}(1\to e^{i\beta})$, $\beta\in(0°,60°)$, has an
> exceptional point at the origin and is a rectifiable Jordan curve of length
> $2\sqrt{1+c^2}/c+\beta$.

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29 — same-family, not a §5 cross-family review
depends-on: the Jordan curve theorem (used once, for the interior identification, §4.3); the
            monotonicity of exp; elementary calculus. No dependency on any other lane's sketch —
            confirmed the file does not import Observation R / Lemma 1 from the sibling lanes,
            it re-derives its own version.
```

**Restatement in my own words.** Two logarithmic spirals of the same pitch $c$, offset by angle
$\beta<60°$, both winding infinitely into the origin, closed off at the outside by a short arc of
the unit circle joining their two outer endpoints. Claim: this is a genuine Jordan curve, it is
rectifiable, and the origin — despite having *every* direction represented in every neighbourhood
(so the ordinary wedge test says nothing) — is not the vertex of any inscribed equilateral
triangle, because on each individual circle around the origin the curve occupies only an arc of
angular width $\beta<60°$.

**What I independently reconstructed and checked by direct computation** (fresh Python, exact
symbolic reasoning where needed, not the file's own code):

- **Injectivity / Jordan curve.** Re-derived from the raw definition of $J$, not the file's
  homeomorphism argument: for two points of $S$ at the same modulus $r$, strict monotonicity of
  $t\mapsto e^{-ct}$ forces the same parameter $t$, hence the same point — so $S$ meets each circle
  exactly once, and likewise $C=e^{i\beta}S$; a point of $S$ and a point of $C$ at the same modulus
  have directions differing by exactly $\beta\ne0\pmod{360°}$, hence are distinct; $B$ occupies only
  modulus $1$, where $S$ and $C$ contribute only their single endpoints $P_0,Q_0$, which are exactly
  $B$'s own endpoints. I confirm this covers all pairings (arm-arm same arm, arm-arm cross, arc-arm
  both ways, arc-arc) and that none is missing — this is the same conclusion as the file's Lemma 3
  and §5.1 table, reached from the bare definitions rather than by reading the table.
- **Rectifiability and the length formula.** Re-derived $|\gamma'(t)|=\sqrt{1+c^2}\,e^{-ct}$ for
  the spiral arm and integrated to $\sqrt{1+c^2}/c$; confirmed the three pieces overlap only at
  single points (measure zero) so lengths add; total $2\sqrt{1+c^2}/c+\beta$ **confirmed exactly**.
- **The chord/arc ratio.** Re-derived $s=\sqrt{1+c^2}\,r/c$ from the arclength integral and hence
  chord/arc $=r/s=c/\sqrt{1+c^2}$, a genuine constant (not just a limiting value) — confirmed.
- **The interior via the universal-cover/shear argument (§4.3).** Checked that the shear map
  $(r,t)\mapsto(r,t+\tau(r))$ is a homeomorphism (continuous with continuous inverse, since
  $\tau(r)=-\ln(r)/c$ is continuous) and that the two displayed pieces of the exterior candidate
  genuinely overlap (both contain $\{r>1\}\times(\beta,360°)$), which is what licenses "exactly two
  components, one bounded" via the Jordan curve theorem. Correct; this is the one place JCT is
  used, and it is used on a curve independently shown to be Jordan, not smuggled.
- **Theorem 1 / Lemma 2 (rotating wedge).** Re-derived the whole argument as a one-line consequence
  of the direction-set characterisation: for every $r\in(0,1)$ the two live directions differ by
  exactly $\beta<60°$; at $r=1$ the arc spans $[0,\beta]$, width $\beta<60°$; for $r>1$ nothing is
  there. None of these ever contains a pair $60°$ apart. Confirmed for all three cases.
- **Sharpness at $\beta=60°$.** Directly recomputed: at $\beta=60°$, $P_0=1$ and $Q_0=e^{i60°}$ are
  both at distance 1 from $O$ subtending exactly $60°$, giving $\{O,P_0,Q_0\}$ equilateral of side
  $|P_0Q_0|=\sqrt{1+1-2\cos60°}=\sqrt{1}=1$. Confirmed exactly.

**Attempts to break it.**

- Tried to find a missing pairing in the "seven-pairing" disjointness table by asking whether $B$
  could touch $S$ or $C$ at a point *other* than $P_0,Q_0$ — ruled out because $B$ lives only at
  modulus exactly $1$, and $S,C$ touch modulus $1$ at exactly one point each, by strict
  monotonicity of the radial function. No gap found.
- Tried to break injectivity by asking whether the same *point* of $\mathbb C$ could arise from two
  parameters on the *same* arm at different "turns" — ruled out because the radial coordinate
  alone already determines the parameter uniquely on a single arm (strict monotonicity), so there
  is no periodicity to exploit; the winding is in the direction, which is unbounded (not reduced
  mod $360°$) as a function of the arclength/radius on a single arm, so no collision is possible.
- Tried to construe the closing arc as accidentally passing back through a smaller radius (which
  would break the "modulus $1$ only" property $B$ relies on) — ruled out since $B$ is explicitly
  defined as a subset of the unit circle, by construction, not derived.
- Checked whether "rectifiable" could quietly fail near the tip because of the infinite winding —
  re-derived that the arclength integral $\int_0^\infty\sqrt{1+c^2}e^{-ct}\,dt$ converges precisely
  because of the exponential radial decay, independent of the (unbounded) angular winding; this is
  exactly why rectifiability is "a property of the choice, not the mechanism" as §12.1 says, and I
  independently checked the borderline claim there ($\theta(r)=1/r$ fails to be rectifiable, since
  $\int_0^1\sqrt{1+r^2\theta'(r)^2}\,dr=\int_0^1\sqrt{1+1/r^2}\,dr$ diverges like $\int dr/r$) —
  correct as a contrast case.

**not-checked:** I did not verify §10's corollary for other triangle shapes (the
spiral-similarity formula $|\alpha+(\ln\lambda)/c|\le\beta$) beyond a plausibility read — the file
itself flags this as its least-checked line, and I have no independent derivation of it to offer;
treat it as unexamined. I also did not re-verify the numerical corner-angle census of §10 (whether
$P_0,Q_0$ ever become exceptional for other $c$) — it is explicitly `numerical`, not a proof step,
and the file is honest about its limits there.

**Strongest residual objection.** None found against Theorem 1, Theorem 2, or Theorem 3 (the
claims actually marked as the file's main content). The construction is exact, the disjointness
argument is airtight because it reduces the whole problem to one-point-per-circle-per-arm, and I
independently confirmed both the length formula and the chord/arc ratio by direct integration
rather than trusting the file's arithmetic. The one place I'd flag for a future reader: §10's
"corner angle" analysis and the spiral-similarity corollary are genuinely less examined (by the
author and by me) than the headline theorems, and should be read with that discount.

---

## Verdict 3 — the half-density lemma, `attacks/half-density-obstruction/README.md`

> $U$ open with $U\cap\rho_{O,60°}(U)=\emptyset$ implies $U$ has density $\le\frac12$ in every ball
> centred at $O$; $\frac12$ is sharp; the criterion is incomparable to the sector criterion and
> vacuous on convex curves.

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29 — same-family, not a §5 cross-family review
depends-on: Lemma H (topology-free, this file, self-contained) for the core; the Jordan curve
            theorem plus isometry-invariance of Lebesgue measure for Lemma A / the full chain.
            Re-verified Lemma A from scratch rather than accepting the file's claim that it agrees
            with the rectifiable-case lane's independent derivation.
```

**Restatement in my own words.** If an isometry fixing a point $O$ moves an open set off itself
(up to measure zero), the set can occupy at most half the measure of any ball centred at $O$ — a
two-line fact about measure and isometries with no curve or topology in it at all. Layered on top,
for a Jordan curve $J$ with the $60°$-rotation acting on it: if $O$ is exceptional then the closed
interior $\overline\Omega$ has angular measure $<180°$ on every circle around $O$ and density
$<\frac12$ in every ball — a genuine, if modest, necessary condition for exceptionality, distinct
from (not weaker or stronger than) the sector criterion of the convex lane, and useless on convex
curves where it is never violated by construction.

**What I independently reconstructed:**

- **Lemma H** (two-line isometry argument): re-derived without reading the proof — an isometry
  fixing $O$ maps $B(O,R)$ onto itself and preserves measure, so $\sigma(W)$ and $W$ are two
  measure-equal subsets of $B(O,R)$ that are (up to a null set) disjoint, forcing
  $2\lambda(W)\le\lambda(B(O,R))$. Airtight; there is genuinely no more content here than that.
- **Sharpness (constant is $\frac12$, not $\frac16$).** Re-derived via the orbit/independent-set
  framing myself before reading the file's version: rotation by $60°$ partitions the circle into
  $6$-cycles, and the disjointness hypothesis says $A$ meets each $6$-cycle in an independent set of
  $C_6$; the maximum independent set of a $6$-cycle has size $3$ (standard: $\alpha(C_n)=\lfloor
  n/2\rfloor$ for even $n$), giving $\frac36=\frac12$, not $\frac16$. Confirmed exactly, and
  confirmed the extremal set $A^*=(0°,60°)\cup(120°,180°)\cup(240°,300°)$ by direct arithmetic
  ($A^*+60°=(60°,120°)\cup(180°,240°)\cup(300°,360°)$, disjoint from $A^*$).
- **Lemma H′ (strict form for closed sets).** Re-derived the connectedness argument: if equality
  held, $W\cup\sigma W$ would be a closed, full-measure subset of the closed ball, forcing it to
  equal the ball (a null open complement inside $\mathbb R^2$ is empty); removing $O$ then splits
  the connected punctured ball into two nonempty disjoint relatively-closed pieces, which is
  impossible. Correct; this is a real (if modest) topological input on top of Lemma H, and the file
  is honest that it is not topology-free the way $H$ is.
- **Lemma A**, re-derived completely from scratch (not read first): the dichotomy that
  $J'\setminus\{O\}$ lies wholly in $\Omega$ or wholly in $E$ (connectedness + disjointness from
  $J$); the nested case forced into $\overline\Omega=\overline{\Omega'}$ hence $J=J'$ (contradiction)
  via the same equal-finite-measure / open-null-set-is-empty argument as in Verdict 1's Lemma 3;
  the externally-tangent sub-case $\Omega\subseteq\Omega'$ ruled out by exhibiting an open
  positive-measure subset of $\Omega'\setminus\Omega$ at a boundary point of $J$. **This is the
  same theorem as Verdict 1's Lemma 3, proved by essentially the same case-split, and I re-derived
  it a second time independently in this file's own notation rather than treating my Verdict-1
  derivation as covering it** — they are stated with slightly different closure conventions
  ($\overline\Omega\cap\rho(\overline\Omega)=\{O\}$ here vs. $\Omega\cap R(\Omega)=\emptyset$
  there) and both hold up.
- **Criterion M (the iff)** and the contrapositive chain $D\Rightarrow C\Rightarrow M$: re-derived
  the Tonelli step ($\lambda(\overline\Omega\cap\overline B(O,R))=\int_0^R|B_r|\,r\,dr$, strict
  pointwise inequality on a positive-measure set surviving integration). Correct.
- **Incomparability with the sector criterion (§5.4).** Checked the two directions independently:
  (a) on any convex curve, §7's proposition forces density $\le\frac12$ *always*, so the density
  criterion can never fire on a convex vertex, while the sector criterion routinely does (any
  vertex with interior angle $>60°$) — this is close to immediate from §7 itself, and I confirm the
  logic; (b) the pinwheel example is meant to show the density criterion firing where the sector
  criterion is silent — see the independent computation below.

**Independent computational verification (fresh code, not the file's, no `sympy` geometry
predicates) — the pinwheel witness, §6.** I rebuilt the 21-vertex polygon from the file's own
generating recipe (coefficients $u_0,\ldots,u_7$, $\delta=1/5$, $\mathrm{ring}=9/10$) using
`fractions.Fraction` only, and independently recomputed, with no code shared with the author:

| Claim | My independent result | File's claim | Match |
|---|---|---|---|
| polygon is simple | 0 non-adjacent intersecting edge pairs (own orientation-sign test) | simple | **yes** |
| exact area (shoelace) | $1723/1000$ | $1723/1000$ | **yes, exact** |
| $\max\lVert v\rVert^2$ | $1$ | $1$ (so $R=1$) | **yes** |
| interior angle at $O<60°$ | confirmed via $d^2>\frac14 n_1n_2$ with $d>0$ (own sign test, no `sympy`) | $<60°$ | **yes** |
| $\varepsilon^2$ to nearest non-incident edge | $4/125$ | $4/125$ | **yes, exact** |
| $O$ is a "good" vertex | found $80$ verified equilateral witnesses via my own from-scratch $\mathbb Q(\sqrt3)$ decider (own `rot60`, own exact segment intersection, own zero/sign test) | good, with an explicit triangle | **yes**, and my first witness — $Q=(-\tfrac3{13}+\tfrac9{13}\sqrt3,\,0)$, $X=(-\tfrac3{26}+\tfrac9{26}\sqrt3,\,\tfrac{27}{26}-\tfrac3{26}\sqrt3)$, side$^2=\tfrac{252}{169}-\tfrac{54}{169}\sqrt3$ — is **the identical triangle** the file reports |

This is a genuine independent reconstruction, not a rerun: I wrote my own exact-arithmetic class,
my own rotation, my own segment-intersection routine, and my own polygon from the eight listed unit
vectors and the two scalars, then searched from scratch for equilateral witnesses at $O$ by
rotating every edge $\pm60°$ about $O$ and intersecting with every edge. Landing on the *exact same*
triangle as the file, in the same algebraic form, is strong evidence the construction and the
witness are both correct, and it directly discharges kill-criterion K4 ("pinwheel is not real")
myself rather than taking the file's word for it.

**Attempts to break it.**

- Tried the six-fold-rotation route the lane's own brief proposed (hoping for $\frac16$) and
  confirmed independently it fails for the structural reason given: $C_6$'s translates by $60°$ are
  not pairwise disjoint even when consecutive ones are ($A^*+120°=A^*$ exactly), so no argument of
  this shape can beat $\frac12$ for *any* angle — I checked this claim ("angle-blind") by rederiving
  the $90°$/$C_4$ case independently ($\alpha(C_4)=2$, giving $\frac24=\frac12$ again, not
  $\frac14$), confirming the general pattern rather than trusting the one example given.
- Tried to find a convex counterexample to §7 (a convex curve where density reaches $\frac12$
  strictly, or exceeds it) — the supporting-line argument is a one-line application of convexity
  and I could not find a way around it; a supporting line through a boundary point of a convex body
  always exists and puts the whole body in a half-plane, this is basic convex geometry.
- Tried to break Lemma H′ by looking for a closed set achieving equality (which would refute the
  strictness) — could not construct one, and the connectedness argument explains why: any
  full-measure-of-the-ball realisation forces an actual (not merely null-differing) partition of a
  connected space, which is impossible for any nonempty pair.

**not-checked:** I did not attempt to verify the `C ⟹̸ D` counterexample domain of §5.3 (the
"$190°$ outer band, $10°$ inner band" example) is realisable as the *interior of an actual Jordan
curve* rather than just an abstractly-defined measurable region with the stated angular sections —
the arithmetic checks out (I recomputed the density $0.1228$ independently and it matches), but I
did not construct or verify a concrete boundary curve for it. This is a minor illustrative point in
the file, not load-bearing for any of the three headline results (Lemma H, Lemma A, the pinwheel),
so it does not change the verdict, but a future reader should treat that one example as
under-examined.

**Strongest residual objection.** None found against Lemma H, Lemma H′, Lemma A, or the pinwheel
witness — all four were independently re-derived or independently recomputed with fresh code and
survived. The one substantive correction the lane makes to its own predecessor (I1's ranking claim
that the density criterion is "strictly stronger" than the sector criterion) is itself correct and
well-supported by the two examples given (pinwheel for one direction, the $120°$ vertex of the
standard wedge witness for the other) — I independently re-confirm the *logic* of both directions,
though I re-verified only the pinwheel half computationally and took the $120°$-vertex claim on the
strength of §7's proposition (which I did verify) plus a basic-geometry check that the vertex is
convex and has angle $120°>60°$, rather than reproducing the file's own numerical density figure
for that triangle.

---

## Summary for the dispatcher

| Claim | My verdict | Can this session grant `verified:review`? |
|---|---|---|
| Theorem T (rectifiable case) | Survived a full independent reconstruction of every step, including the lane's self-nominated weakest point (Lemma 3/no-nesting) and both flagged constants ($8/3$, $2/3$, $140°$). No error found. | **No — same family.** |
| Spiral-tip witness | Survived independent reconstruction of Jordan-curve status, rectifiability, the length formula, and the chord/arc-ratio calculation. Confirmed by direct computation (not by trusting the file) that it does **not** collide with Theorem T. | **No — same family.** |
| Half-density obstruction | Survived independent reconstruction of Lemma H/H′/A and the criterion hierarchy; the pinwheel witness was independently re-verified with fresh, from-scratch exact code and reproduced the identical witness triangle. | **No — same family.** |

**All three claims remain `sketch`.** This examination is same-model-family (Sonnet 5 examining
Opus 5) and per [`../../../../RULES.md`](../../../../RULES.md) §5 and §8 confers no
`verified:review` status regardless of how thorough it was — that gate exists precisely because a
model checking its own family's output is close to checking itself, and decorrelated failure is
the entire value of the review step. A human, or a genuine cross-family (Codex) examiner, should
make the status call. What this file adds is a documented, independently-reconstructed second
opinion and, for the two computational claims, a from-scratch re-implementation that reproduced
the reported witnesses exactly — which is more than agreement, but still not what §5 requires for
promotion.

**Anything I could not follow:** nothing rose to that level in the three headline theorems. The
`not-checked` items above (the area-formula citation in Verdict 1, §10's spiral-similarity
corollary in Verdict 2, and the illustrative-only $C\not\Rightarrow D$ domain in Verdict 3) are
each explicitly non-load-bearing for the claim actually being made, and each lane's own author
flagged the corresponding weak point already — I did not find anything they missed flagging.
