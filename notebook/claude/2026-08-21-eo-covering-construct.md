# 2026-08-21 — building the covering: 34 → 28, and 26 is still 2 away

Worker W1 (Constructor), branch `claude/circle-equklatetal-problem-sa7tx7`. Files:
`problems/circle-packing-equilateral-triangle/attacks/eo-covering-construct/**`,
`experiments/packing-eo-covering/**`, this journal. A partner worker (W2) had the lower-bound side
of the same question; I did not touch its paths.

## The brief and what actually happened

Brief: cover $T_a$, $a<6$, by $\le26$ sets of diameter $<1$ and Erdős–Oler at $k=7$ falls out; or
find the obstruction. Prior state of the repo: hexagons 34, uniform sub-triangles 36, isodiametric
floor 20, requirement 26. The framing I was handed was "the gap is 34 → 26 and the leverage is all
at the boundary."

The first thing I did was re-measure the hexagon covering, expecting to confirm 34. It is **28**,
and the alignment that achieves it is not a fiddly optimum — it is the $\Delta(7)$ triangular
lattice of spacing $\sqrt3/2$ dropped into the triangle. That reframed the whole task before I had
written any real code: the gap is 2, not 8, and the previously-quoted 34 was a scan artefact.

Then the reframing repeated one level up. `eo-small-cases` §4.1 reads the covering deficit off the
$m^2$ subdivision and gets $(k-2)(k-3)/2 = 10$ at $k=7$, growing quadratically. That is a property
of the wrong scheme. The lattice scheme gives $\Delta(\lceil 1.1547(k-1)\rceil)$, which is
$\Delta(k)$ exactly for $k=4,5,6,7$ — **deficit 2, flat in $k$** — and then jumps to 11 at $k=8$
because $1.1547\times7 = 8.083$ just clears the integer. $k=7$ is the last case where this route is
even close, which I did not anticipate and which nothing in the repo said.

## What I actually proved (in the exact-certificate sense)

$T_a$ splits into $\Delta(p)$ convex cells of diameter $\le1$ for $a\le p\sqrt3/2$, machine-checked
in exact $\mathbb{Q}(\sqrt3)$ arithmetic for $p\le10$. The threshold is sharp for the scheme and the
reason is clean: the corner of $T_a$ has to sit inside the corner site's Voronoi hexagon, whose
reach in the corner direction is the circumradius $1/2$, and at $a=p\sqrt3/2$ it sits exactly on a
hexagon vertex. Every verified maximum squared diameter is exactly 1, for every $p$ — that
coincidence is the corner constraint being tight, not a coincidence.

Working in the basis $e_1=(1,0), e_2=(1/2,\sqrt3/2)$ was the thing that made exactness painless:
$|ue_1+ve_2|^2 = u^2+uv+v^2$ is rational, so no square root ever appears in a distance, and the
only irrationality left is in the coordinates ($\sqrt3/2$ spacing), which a 30-line
$\mathbb{Q}(\sqrt3)$ class with an exact sign test handles. I would use this basis again for
anything in this problem.

## Where it stopped, and my honest read of why

Power-diagram search (26–28 free sites and weights, annealed coordinate descent): 28 → max
diameter $0.984$; 27 → $1.031$; 26 → $1.038$. The cliff is between 28 and 27, and 26 costs almost
nothing more than 27 — the 27-cell optima are 26-cell optima with a nearly redundant cell. So the
barrier is at 28.

I calibrated the optimiser on the two cases with known answers ($a=2,N=4$ and $a=3,N=9$, both
exactly 1) and it recovers them to $5\times10^{-4}$, so the $1.038$ is real and not optimiser
weakness at the 4 % level.

The measured waste, per cell area normalised to diameter 1: interior cells $0.647$ against the
hexagon ceiling $0.6495$ — **at the ceiling, nothing to win**; edge cells $0.55$ against an
individual ceiling of $0.609$; corner cells $0.464$ against a *proved* ceiling of $\pi/6$. On
paper the individual ceilings add up to 26. They are not jointly reachable: the deep-notch
boundary row that reaches $0.609$ forces the rows above it into an alternating-gap regime at
$0.611$ each — better than a cut hexagon ($0.541$) but permanently $0.039$ below a regular one, so
it wins for two rows and loses from the third, and $T_6$ is seven rows deep. That is the
obstruction, stated as sharply as I can state it: **the locally optimal boundary shape taxes the
interior more than it saves at the boundary, past two rows.**

## What I got wrong on the way

Twice, by hand, on the row recursion. First I estimated the boundary saving at "2 pieces, exactly
what is needed" and briefly believed 26 was reachable; the error was assuming the freed area lands
in cells that are still hexagons. Then I computed the third and fourth rows of the deep-notch stack
as $0.583, 0.587$ — decaying — and wrote that into a draft as "the disturbance oscillates instead
of decaying". Both wrong: the recursion settles into a clean period-2 cycle at $0.6109$ for every
row. I only caught it because I scripted the arithmetic (`rows.py`) before publishing the
paragraph, having decided that any number appearing in a conclusion had to come out of a file. The
corrected version is a *better* argument for the same conclusion, which is the annoying pattern:
the hand-waved version was wrong in the direction that flattered my own narrative.

Third one, smaller: I convinced myself the $\Delta(7)$ hexagon union reaches $a=6.696$ (expanding
the array triangle by the hexagon inradius) and briefly thought the optimiser was broken for
reporting less. The corners stick out — expanding a triangle by $\delta$ moves a corner out by
$2\delta$, not $\delta$. The corner is the binding constraint everywhere in this problem and I had
to re-learn that from the wrong direction.

## The by-product I did not go looking for

Lemma L gives $a_{\Delta(p)+1} \ge p\sqrt3/2$, which **beats Oler exactly for $p\le6$** — at
$n=4,7,11,16,22$. At $n=4$ it is tight and reproves $s(4)=4\sqrt3$ in three lines. At $n=16$ and
$n=22$ it is the best lower bound in this repo. I ran an independent packing optimiser to try to
contradict it (it reproduces the known exact $a_7$ and $a_{11}$ to $5\times10^{-5}$, and its
$a_{16}\le4.630$, $a_{22}\le5.648$ leave my bounds intact). Novelty **UNVERIFIED** and I assume
known: this is a standard-shaped argument and scholarly hosts are blocked at this session's egress.

## Kill-criterion

Neither fired, and I want that on the record rather than retro-fitted. K1 was "stop at $\ge30$" —
I reached 28. K2 was "stop if the interior is at the hexagonal ceiling and the residual gap exceeds
the removable boundary waste" — the interior is at the ceiling, but the arithmetic says $\sim2.5$
cells of the 4-cell waste is individually removable against a 2-cell requirement, so K2 does not
strictly fire. I stopped on the compute budget with the obstruction identified (joint
non-reachability, §4 of the attack), not on either criterion. Writing them down in advance still
paid: without K2 I would have kept re-running the optimiser instead of measuring the cell areas,
and the cell-area table is the whole finding.

## For whoever picks this up

- Optimise the subdivision's **vertices** under convexity constraints, not sites. Power diagrams
  are a proper subfamily of convex partitions and I stayed inside it the whole time.
- The one question that would settle the route for good: is $3\sqrt3/8$ the maximum density of a
  partition of the plane into diameter-1 sets? If yes, $\tfrac23(k-1)^2 \le \Delta(k)-2$ fails for
  $k\ge10$ and the covering route is closed permanently above $k=9$. I asserted this in the attack
  and flagged it as an assertion; it is the load-bearing unproved thing in my write-up.
- Problem `RULES.md` §3 wants a second, independently written checker for anything computational.
  Everything I produced has exactly one, mine.
