# 2026-08-29 — the rectifiable case of the 60° rotation route (resumed lane)

Worker lane: exactly three files —
`problems/inscribed-equilateral-triangle/attacks/rectifiable-case/README.md`,
`.../KILL-CRITERION.md` (pre-existing, **not** rewritten), and this entry. Four other workers were
concurrently in `attacks/half-density-obstruction/`, `attacks/spiral-tip-witness/`,
`experiments/inscribed-triangle-angular/`, and PR #133; I touched none of those. I ran no git
command — the dispatcher commits.

This lane had been started by an earlier worker who wrote `KILL-CRITERION.md` and was then killed
by a rate limit. I inherited the pre-registration and honoured it: I did not touch that file, and
below I record which of its criteria fired.

Reading order actually followed: repo `RULES.md` §0/§1/§3/§5/§6, problem `RULES.md` (all of it),
problem `README.md`, `attacks/rotation-continuity/README.md` (all 603 lines), then this lane's
`KILL-CRITERION.md`. Only then did I write a line of anything.

---

## 1. The first thing I did was check that C1 fires — and it does

The kill-criterion's §C1 predicted, on the record before any computation, that the "work with the
rotation criterion directly in the pair (radius, angle)" route the brief suggested would die,
because at a differentiability point all of $J$ near $O$ sits in a thin double cone and no two
points of a thin double cone subtend $60°$ at $O$.

That is exactly right, and it is worth stating as a lemma rather than as a disappointment:

> at a point where the arclength parametrisation is differentiable with unit speed, **every**
> inscribed equilateral triangle with a vertex at $O$ has side $\ge \varepsilon$, where
> $\varepsilon$ is any radius for which $J \cap B(O,\varepsilon)$ lies in a double cone of
> half-angle $< 30°$.

So the answer, if there is one, is a *macroscopic* triangle, and no amount of local analysis at
$O$ can produce it. The local pair route is dead, C1 fired, and I recorded it as `refuted` rather
than quietly weakening it. The lane survived because the surviving route is *semi*-local: local
information about the **interior domain** $\Omega$ near $O$, cashed out globally through the
no-nesting lemma.

## 2. The move that unlocked it

The neighbouring lane's gap is: extra strands of $J$ can re-enter $B(O,\varepsilon)$ at every
scale, so $B(O,\varepsilon)\setminus J$ can have a third component trapped in the cone, and
$\Omega$ could be that component.

Two observations killed the trapped component.

**(a) Localisation is free.** Every point of $J$ close enough to $O$ has a *parameter* close to
$t_0$. If not, take $\gamma(s_n)\to O$ with $d(s_n,t_0)\ge\delta$; compactness of the parameter
circle gives $s_n \to s^*\ne t_0$ and continuity gives $\gamma(s^*) = O = \gamma(t_0)$, which
contradicts injectivity. No regularity used at all. The rotation-continuity lane already uses this
in passing; I re-derived it because everything downstream leans on it.

**(b) Differentiability at one point is a length bound, not just a direction bound.** With (a),
$\mathcal{H}^1(J\cap B(O,\rho))$ is the *parameter* measure of $\{s : |\gamma(s)-O|<\rho\}$, and
the differentiability sandwich $|\gamma(s)-O| \ge (1-\eta')|s-t_0|$ confines that set to an
interval of length $2\rho/(1-\eta')$. So the curve has length at most $2\rho/(1-\eta')$ in
$B(O,\rho)$, against the $2\rho$ that the through-strand already spends.

I had expected to need Besicovitch's density theorem for 1-rectifiable sets here (route (ii) of
the brief). I do not: **differentiability at the single point $t_0$, plus injectivity, gives the
density bound at that point for free.** That is the step I am most pleased with and also the one
I double-checked hardest, because "I derived a famous theorem in two lines" is exactly the shape
of a mistake. It is not the famous theorem: it is the density bound *at a point where the
parametrisation is differentiable*, which is a much weaker statement (Besicovitch's theorem gets
density 1 at a.e. point of an arbitrary 1-rectifiable **set**, with no parametrisation in sight).

Then the Banach-indicatrix count does the rest: the through-strand alone accounts for $2\rho$ of
the budget, so the radii carrying any *extra* crossing have measure at most
$2\rho\eta'/(1-\eta')$, which is $\tfrac23\rho < \rho$ at $\eta' = \tfrac14$. Hence there is a
radius $\tau < \rho$ at which the circle meets $J$ in **exactly two** points — one on each side of
the cone. Two points cut the circle into two arcs each wider than $120°$; $\Omega$ meets the circle
(it has points inside and outside), so one of those arcs lies in $\Omega$; an arc wider than $60°$
contains a pair at angular separation exactly $60°$; and the no-nesting lemma converts that into an
intersection of $J$ with its own $60°$ rotate.

The trapped component is not merely unconstructed: it needs at least four crossings, and four
crossings can only happen on a set of radii of measure $< \rho$.

## 3. Things I checked because I did not trust myself

- **Banach's indicatrix.** I did not want a citation I could not read, so I proved the only
  direction I need from scratch: equal partitions, $\int N_n = \sum_i \mathrm{osc}_i \le
  \mathrm{Var}$, $\#g^{-1}(\tau)\le\liminf N_n(\tau)$ because $k$ distinct preimages eventually sit
  in $k$ distinct subintervals, then Fatou. Four lines, no source needed.
- **The no-nesting lemma.** The neighbouring lane's Lemma A. I could not import it (repo
  `RULES.md` §3 forbids building on a `sketch`, my own family's included), so I re-derived it. My
  version is slightly different: I only need $\Omega\cap\rho(\Omega)=\emptyset$, and in the case
  $\Omega\subseteq\Omega'$ I get the contradiction from an open set $\Omega'\cap E$ of positive
  measure rather than from boundary-taking. It landed in the same place, which is mild evidence
  and not verification.
- **The quantifier, against the $30$-$30$-$120$ witness (kill-criterion A2).** At a $30°$ apex the
  two one-sided directions $u_1,u_2$ subtend $30°$, not $180°$, so no unit $u$ satisfies the
  hypothesis with error $\tfrac14$: it would need $|u_1 - u| \le \tfrac14$ and $|u_2 + u| \le
  \tfrac14$, hence $|u_1+u_2| \le \tfrac12$, whereas $|u_1+u_2| = 2\cos 15° \approx 1.93$. So one
  side is off by at least $\cos 15° \approx 0.97$. My hypothesis genuinely excludes the
  known exceptional points, and it excludes them *quantitatively*, not by appeal to a picture.
- **The square test (A1).** Ran the whole argument at general angle $\alpha$. Everything survives
  for $\alpha \in (0°,120°]$ and outputs an inscribed **isosceles** triangle with apex $\alpha$ at
  $O$. At $\alpha = 60°$ and only there, isosceles-with-apex-$60°$ *is* equilateral. At $90°$ the
  output is an isosceles right triangle and the fourth square vertex is unconstrained. So the
  argument does not transfer, and the honest reading is that what I actually proved is a statement
  about *isosceles* triangles, which is a much cheaper kind of statement than square peg.

## 4. A wrong sub-claim I found in the neighbouring lane

`attacks/rotation-continuity/README.md` Lemma B and Theorem C both assert the triangle has **side
$\varepsilon/2$**. That does not follow: the sector construction produces a point of
$\overline\Omega \cap \rho(\overline\Omega)$ at radius $\varepsilon/2$, but Lemma A is a
non-constructive contrapositive and says nothing about *where* $J$ meets $\rho(J)$.

It is not merely unjustified, it is false, and my own Lemma 0 predicts it must be: at a point where
the curve is cone-confined at scale $\varepsilon$, no triangle of side $<\varepsilon$ exists at
all, while Theorem C claims one of side $\varepsilon/2$. Exact witness: the unit square at
$O=(\tfrac12,0)$. Lemma B applies with $I=[60°,120°]$ and $\varepsilon=1$ (that sector is inside
the square), predicting side $\tfrac12$; the exact enumeration says the *only* inscribed
equilateral triangle with a vertex there is $\{(\tfrac12,0),(0,\tfrac{\sqrt3}{2}),(1,\tfrac{\sqrt3}{2})\}$,
side exactly $1$.

The conclusions of Lemma B and Theorem C are unaffected; only the side-length clause is wrong. I
did not edit their file (§2 file ownership) — the correction request is in my README, and it
should be handled by whoever owns that lane.

## 5. Computation

Wrote my own exact decider in $\mathbb{Q}(\sqrt3)$ from scratch (`rect.py`, inlined in the lane
README) rather than reusing `experiments/inscribed-triangle-polygons/`, because problem
`RULES.md` sets the audit standard as independent reimplementation. Standard library only; the
zero test is syntactic ($a+b\sqrt3=0 \iff a=b=0$) and the sign test compares $a^2$ against $3b^2$.
Per the brief I used **no** sympy geometry predicate anywhere.

- Validation gate first, before believing anything: equilateral triangle (all three vertices good,
  side$^2 = 1$), the $30$-$30$-$120$ wedge witness (both $30°$ apexes not good, $120°$ apex good
  with min side$^2 = 1/12$), unit square corners good with side$^2 = 8-4\sqrt3$. All match the
  committed enumerator's published control table.
- Side-length refutation as above.
- Cross-check + census: my decider against `decide_good` on all 190 committed fixtures — 783
  vertices and 5481 non-vertex boundary points, **0 disagreements**. And the census my theorem
  actually predicts: every non-vertex boundary point of every fixture (convex and non-convex,
  including the C-strips whose taper is under $0.3°$) is good — **0 violations in 5481**.

Total compute a few minutes, far inside the one-hour budget. The census is the slow part (~4 min)
because it re-decides every point twice.

**And the honest caveat about that census**: a polygon *cannot* exhibit the configuration my
theorem rules out. With finitely many segments, the nearest other strand to a non-vertex point is
at positive distance, so a fat sector is automatic. The census confirms the conclusion on a class
where the mechanism is trivial. Problem `RULES.md` §3.3 says exactly this and it is worth
repeating: agreement is "merely not-yet-dead", and here it is weaker than usual.

## 6. Where I think this is most likely to be wrong

In descending order of my own worry:

1. **The no-nesting lemma.** It is the only place where plane topology and measure interact, and
   it is the step where a fluent wrong paragraph is cheapest to write. An examiner should
   re-derive it rather than read it, and should specifically attack the two case splits and the
   use of $\lambda(\Omega')=\lambda(\Omega)$.
2. **"$\Omega$ meets $\partial B(O,\tau)$".** Trivial-looking, and it is trivial, but it is doing
   real work: it is the only step that uses that $\Omega$ is *not* contained in a small ball.
3. **The indicatrix bound's interaction with plateaus.** A 1-Lipschitz $g$ can be constant on an
   interval, and then $\#g^{-1}(\tau)$ is infinite for that one $\tau$. That costs nothing (one
   value is a null set, and the inequality still holds — the integral is just $+\infty$ on a null
   set), but I want a reviewer to look at it rather than take my word.

What I am *not* worried about is §7 territory. The statement is strictly weaker than the reported
Meyerson theorem in the problem `README.md` — a.e. point of a *rectifiable* curve, versus all but
two points of *any* Jordan curve. If anything it is a consistency check on that row rather than a
challenge to it.
