# 2026-08-29 — IET, extremal-size lane (how big a triangle is guaranteed?)

Worker journal. Agent `claude` (Claude Opus 5), branch
`claude/inscribe-equilateral-triangle-oj15x1`. Lane files: `attacks/extremal-size/README.md`,
`attacks/extremal-size/KILL-CRITERION.md`, this file. Nothing else was touched; no git command
was run by this worker.

## Brief

Quantitative question (idea **I6**): for a Jordan curve $J$, $m(J) = \sup$ side of an inscribed
equilateral triangle; ask for $\inf m(J)/N(J)$ over a normalisation $N$. The dispatch brief
ordered me to settle the **normalisation** before optimising anything, on pain of computing a
beautiful answer to an empty question.

## Order of work

1. Read `RULES.md` §0/§3/§6/§7, problem `RULES.md` (all), problem `README.md`,
   `attacks/ideation-round-1/README.md` §I6, and skimmed `attacks/rectifiable-case/` and
   `attacks/spiral-tip-witness/` for what they do and do not give me.
2. Wrote `KILL-CRITERION.md` **before any computation** (§6.2). K1 (degenerate normalisation)
   was written as the criterion most likely to fire, and it fired — twice.
3. Hand-proved the width lemma (an equilateral triangle of side $s$ has minimal width
   $\tfrac{\sqrt3}{2}s$) and the two degeneracy witnesses **before** running anything.
4. Only then computed.

## What actually happened, in order

**The thin rectangle.** I6 already says diameter is dead on arrival; I re-derived it rather than
taking it (the file is `sketch` and its author is my own family). The clean form is: minimal
width is monotone under inclusion and an equilateral triangle of side $s$ has minimal width
exactly its altitude $\tfrac{\sqrt3}{2}s$. So $m(J) \le \tfrac{2}{\sqrt3}\,w(\operatorname{conv}J)$
for **every** set, convex or not. That single lemma kills diameter, perimeter, $\sqrt{\text{area}}$
and circumradius at once via the $1\times\varepsilon$ rectangle, and it is also the sharp upper
bound for the convex question later. Good return on four lines.

**The L-strip — the thing I did not expect to be this easy.** I6 proposes hull *width* as "the
right convex normalisation" and guesses that for general curves a thin **spiral strip** is the
candidate killer. It is not needed. Take the L-shaped hexagon
$(0,0),(1,0),(1,\delta),(\delta,\delta),(\delta,1),(0,1)$: every boundary point is within
$\delta$ of the union of two perpendicular unit segments, and two perpendicular segments carry
**no** nondegenerate equilateral triangle at all (any two vertices on the same arm force the
apex over the midpoint of a sub-segment of $[0,1]$, which cannot be on the other arm). So
$m = O(\delta)$ while the hull width stays $\tfrac{1+\delta}{\sqrt2} \to \tfrac1{\sqrt2}$.
A polygon, so exactly checkable — much better witness than a spiral.

Hand bound: $s \le (4+2\sqrt3)\sqrt{1+\ldots}\,\delta < 7.73\delta$ (§4 of the README does it
properly). Exact computation then said the truth is $(\sqrt6+\sqrt2)\delta = 4\cos15°\,\delta
\approx 3.8637\delta$, at $O$ = the origin corner, and it scaled **exactly** linearly across
$\delta \in \{1/10,1/20,1/50,1/100\}$ — which is the reassuring signature, since the hand
argument predicts exact linearity.

**Then the convex question.** With every hull-based normalisation dead for general curves, the
non-empty question is I6's convex one. Universal upper bound $2/\sqrt3$ from the same width
lemma (attained: thin rectangle, and the equilateral triangle itself). Disk gives exactly
$\sqrt3/2$.

I expected the disk to be the minimiser and it is not. The first-order perturbation computation
is the part I am happiest with, because it is analytic and it *predicted* the numerics:
perturb the disk radially by $\varepsilon f$, then
$m \approx \sqrt3(1+\varepsilon \max_\theta F)$, $w \approx 2(1+\varepsilon\min_\theta G)$ with
$F$ the average of $f$ over the $120°$-orbit and $G$ over the $180°$-orbit. Both have mean
$a_0$, so $\max F \ge a_0 \ge \min G$ **always**: the ratio never decreases at first order, and
it is stationary exactly when $f$ has no even harmonic and no harmonic divisible by 3, i.e.
$n \equiv \pm1 \pmod 6$. The numerics reproduced the first-order coefficient for $n=3$ to four
digits ($0.866\varepsilon$, predicted $(\sqrt3/2)\varepsilon$), which is the check that made me
believe the rest.

No even harmonic $\Rightarrow$ **constant width**. That is a real simplification: with support
function $h = 1+\varepsilon\cos 5\theta$ the width is *exactly* $2$ (odd harmonics cancel in
$h(\theta)+h(\theta+\pi)$), so no numerical width enters the ratio at all and only $m$ is
estimated. Convexity is $h+h''>0 \iff \varepsilon < 1/24$. At $\varepsilon = 1/24$:
$m \approx 1.71441$, ratio $\approx 0.857205 < \sqrt3/2 = 0.866025$.

Two independent float estimators agree to $10^{-9}$ (rotation sweep with bisection vs. a
penalty multistart over three boundary parameters that never rotates anything).

**The lower bound.** The brief pointed me at Theorem T of `rectifiable-case` as "the most
promising route". It is not one: T finds a radius $\tau$ that may be taken arbitrarily small and
produces a triangle of side $\approx\tau$, so it gives **no** lower bound on $m$ — and it is
`sketch`, so I could not have used it anyway (K5). I got a bound from a different place: the
incircle. $m(K) \ge \sqrt3\,r$ for convex $K$, by a transition-point argument along the arc
$\partial K \setminus B(A,\sqrt3 r)$ with $A$ a contact point of the incircle. Sharp — the disk
is the equality case. Chained with $w \le 3r$ it gives $m \ge w/\sqrt3$.

## Things I got wrong or nearly got wrong

- I first tried to prove a lower bound by "the largest equilateral triangle **contained** in $K$
  has its vertices on $\partial K$". That is **false as stated for a fixed orientation** (a
  horizontal-base equilateral triangle largest inside a unit square has side 1 with its apex in
  the interior), and even the global version needs a fiddly contact-set case analysis I could
  not close. Abandoned; the incircle route needs none of it. Recorded in the README as a
  refuted approach so the next worker does not retry it.
- I nearly reported the max-side at the $120°$ apex of the 30-30-120 control as $1/3$
  (side$^2$), which is what `inscribed-triangle-angular`'s README reports. That is its **first**
  witness, not the maximum; the maximum is side$^2 = 4/9$, triangle
  $(0,\tfrac{\sqrt3}{3}),(\pm\tfrac13,0)$, which I verified by hand after the code said so. This
  is exactly the "the committed decider short-circuits, a maximiser must not" trap, and it is
  why I wrote my own maximiser rather than reusing `decide`.
- The float search initially used a body given by its **radial** function $1+\varepsilon\cos5\theta$,
  whose width is $2+O(\varepsilon^2)$, not $2$. Switching to the **support** function removed a
  numerical quantity from the answer entirely.

## Budget

Well under the hour. The only long-running job was a 24-parameter Nelder–Mead over general
convex support functions (background, ~6 min), reported in the README §7.

## Hand-off

The one thing this lane could not do: an **exact** upper bound on $m$ for a specific body. The
repo's two exact deciders answer "is this point a vertex", not "how large is the largest
triangle anywhere on this curve", and my lane owns no file under `experiments/`. Every claim
that some body beats the disk is therefore `numerical` and float-based, and stays that way until
someone builds an exact maximiser for rational polygons. That is the follow-up issue I would
open.
