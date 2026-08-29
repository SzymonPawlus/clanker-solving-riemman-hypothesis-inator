# inscribed-triangle-angular — a second, structurally different exact decider

**Status: `numerical`.** Exact arithmetic makes each *individual* fixture's answer certain —
there is no tolerance anywhere and every reported triangle is re-checked by a verifier that
knows nothing about how it was found. It makes **no general claim** true. Nothing here is a
proof step, and nothing here may be built on (`../../RULES.md` §3, and this problem's
[`RULES.md`](../../problems/inscribed-equilateral-triangle/RULES.md) §6.4). Polygons are the
most regular curves there are; agreement on them is weak evidence about the general case and
none at all about the wild one.

regularity budget: polygonal (simple polygons with vertices in $\mathbb{Q}(\sqrt3)$)

---

## Question

For $O$ on a Jordan curve $J$, call $O$ **good** if some **nondegenerate** equilateral triangle
has all three vertices on $J$ and one of them equal to $O$; **exceptional** otherwise. This
directory decides goodness exactly for simple polygons — the same question the committed
sibling [`../inscribed-triangle-polygons/`](../inscribed-triangle-polygons/) decides — by a
**different algorithm**, so that agreement between the two is worth more than either alone.

## The criterion, and why it is three lines

Write $\rho$ for the rotation by $+60°$ about $O$ and $u(t)=e^{it}$.

> **(R)** $O$ is good $\iff$ there are an angle $t$ and a radius $r>0$ with
> $O+r\,u(t)\in J$ **and** $O+r\,u(t{+}60°)\in J$.

*($\Leftarrow$)* Put $A=O+r\,u(t)$, $B=O+r\,u(t{+}60°)$. Then $|OA|=|OB|=r>0$ and
$\angle AOB=60°$. An isoceles triangle with apex angle $60°$ has base angles $(180-60)/2=60°$,
so $OAB$ is equiangular, hence equilateral with side $r>0$; it is nondegenerate because $r>0$
gives $A,B\ne O$ and the $60°$ separation gives $A\ne B$.
*($\Rightarrow$)* If $O,A,B$ is nondegenerate equilateral on $J$ with side $s>0$ then
$|OA|=|OB|=s$ and $\angle AOB=60°$, so with $A=O+s\,u(\alpha)$, $B=O+s\,u(\beta)$ we get
$\beta-\alpha=\pm60°$; take $(t,r)=(\alpha,s)$ or $(\beta,s)$. $\square$

The criterion was re-derived here before any code was written, and it checks out. **$r>0$ is
the whole degeneracy question**: $r=0$ is available at every $O$ and every $t$ and is the
"triangle" $O,O,O$. Every radial set in this implementation is built with $r>0$ by
construction — that is where this lane pays the debt the rotation picture pays by discarding
the fixed point $O$ of the rotation (`problems/.../RULES.md` §2).

## Why this is a different algorithm, not the same one run twice

The sibling decides goodness by intersecting the polygon with its own $60°$ rotate about $O$:
$O(n^2)$ **segment–segment intersections in the plane**, solving for two segment parameters,
then discarding the intersection component equal to $\{O\}$.

This lane never intersects two segments. The object here is the **multivalued radial
function**: each ray from $O$ meets $\partial J$ in a finite set, and the question is whether
$R(t)$ and $R(t{+}60°)$ ever share a value as $t$ sweeps. The work happens in **direction
space**.

**Scale parametrisation (this is what removes the square roots).** Take a direction as a
nonzero vector $v\in K^2$, $K=\mathbb{Q}(\sqrt3)$ — *not* a unit vector. Since
$|\rho v|=|v|$, matching the radius on the two rays is the same as matching the **scale** in

$$S(v)=\{\,s>0:\ O+s v\in J\,\},$$

so (R) becomes: *$O$ is good $\iff$ $S(v)$ meets $S(\rho v)$ for some $v\ne0$.* A witness
triangle is then $(O,\;O+sv,\;O+s\rho v)$ with $s\in K$, **exactly representable** — no square
root ever has to be extracted.

**The sweep.**

1. **Breakpoints.** Let $D$ be the directions of $V-O$ over the vertices $V\ne O$, together
   with their $\rho^{-1}$ images, together with the four axis directions (thrown in only so
   that every gap is under $180°$, making $d_i+d_{i+1}$ a valid interior representative).
   Between two cyclically consecutive elements of $D$, both the set of edges met by the ray at
   $v$ and the set met by the ray at $\rho v$ are **constant**, and both consist only of edges
   whose line misses $O$ — because an edge whose line contains $O$ is met only in the one or
   two directions *along* it, and those are vertex directions, hence already in $D$.
2. **On an open gap.** For an edge $e=[A,B]$ with $a=A-O$, $b=B-O$, $k=\operatorname{cross}(a,b)\ne0$,
   the ray at $v$ meets $e$ iff $v$ lies in the closed cone spanned by $a,b$, and then at the
   single scale $s_e(v)=k/\operatorname{cross}(v,b-a)>0$. For an ordered pair $(e,f)$ met by $v$
   and by $\rho v$ respectively, equal scales says
   $k_e/\operatorname{cross}(v,b{-}a)=k_f/\operatorname{cross}(\rho v,d{-}c)$. Both denominators
   are nonzero on the gap, so cross-multiplying is an *equivalence*, and since a rotation
   preserves the cross product ($\operatorname{cross}(\rho v,m)=\operatorname{cross}(v,\rho^{-1}m)$)
   the condition collapses to a single **linear form**

   $$\operatorname{cross}(v,\,M)=0,\qquad M=k_e\,\rho^{-1}(d-c)-k_f\,(b-a).$$

   $M\ne0$: at most the two directions $\pm M$ in this gap are good from $(e,f)$.
   $M=0$: the **entire gap** is good from $(e,f)$ — this says the line of $f$ is the $60°$
   rotate about $O$ of the line of $e$, the only way a one-parameter family of inscribed
   triangles can sit at $O$.
3. **At a breakpoint.** Decided directly by `good_at_direction`, which rebuilds $S(v)$ and
   $S(\rho v)$ from scratch. **This is where the collinear rays live.**

Because there are finitely many pairs, a gap that is entirely good must have $M=0$ for some
pair. So the sweep returns the **complete good-direction set**

$$G(O)=\{\,v:\ S(v)\ \text{meets}\ S(\rho v)\,\},$$

not merely a witness — which is what lets this lane answer questions the rotation decider
cannot answer cheaply.

**The degeneracies land in different places.** There: collinear overlap of an edge with a
rotated edge, and the intersection component $\{O\}$. Here: $M=0$, and the collinear-ray
intervals. That is what makes agreement between the two informative rather than circular.

## Collinear rays — the case that was flagged, and what it actually is

The previous worker's note said its *float* brute force missed collinear-ray directions. The
diagnosis in the handover was right: a direction in which the ray runs **along** a polygon edge
is where the radial set degenerates from a finite set of points to a **whole interval**, and a
grid sampler steps over it. It is not exotic:

- $O$ interior to an edge ⟹ **two** opposite collinear directions, each seeing a half-open
  interval $(0,\lVert\cdot\rVert]$;
- $O$ a vertex ⟹ **both** incident edges are collinear rays.

`_edge_scales` handles it in one uniform branch (`cross(a,b)==0`), returning a closed interval
of scales intersected with $s>0$; the half-openness at $0$ is exactly the exclusion of the
degenerate triangle. It is the **first** thing the test suite checks
(`TestCollinearRays`), and the controls exercise it:

- the equilateral triangle inscribed in itself — at each vertex *both* rays are collinear;
- the $120°$ apex of the $30$-$30$-$120$ control, good in exactly **three** directions
  $210°,240°,270°$, of which $210°$ runs along an edge and $270°$ has its $\rho$-image along an
  edge. Witness side$^2=1/3$, i.e. the triangle
  $(0,\tfrac{\sqrt3}{3}),(-\tfrac12,\tfrac{\sqrt3}{6}),(0,0)$ — the same triangle the previous
  worker had hand-checked, reproduced independently here.

## Reproducing

```sh
sh run.sh          # everything, ~30 min; each stage checkpoints into out/
```

Pinned: **CPython 3.11.15**, standard library only — `fractions`, `math`, `json`, `random`,
`unittest`. **No sympy, no numpy, no library geometry predicate anywhere.** All generators are
seeded (`SEED = 20260829`); the run is deterministic. Individual stages:

```sh
python3 -m unittest -q test_angular   # 25 tests, ~45 s
python3 run.py validate               # hand-checked controls + collinear rays
python3 run.py fixtures               # re-decide the sibling's 190 committed fixtures
python3 run.py explore                # structure of G(O)
python3 critical.py                   # the critically good points
python3 run.py hunt 1500              # exceptional-set census
```

### Files

| file | what |
|---|---|
| `q3.py` | exact $K=\mathbb{Q}(\sqrt3)$; own representation and own sign algorithm, independent of the sibling's `k3.py` |
| `angular.py` | the sweep: radial scale sets, `good_at_direction`, `good_directions` (all of $G(O)$), `decide` |
| `rotcheck.py` | an **independent second decider** in this lane, by plane segment intersection — see below |
| `shapes.py` | exact rational polygon families and seeded generators |
| `fixtures_io.py` | reads the sibling's committed fixture JSON **as data**; imports no code from it |
| `brute.py` | a float brute force, inherited; a **pre-screen only**, decides nothing |
| `run.py`, `critical.py`, `run.sh` | drivers |
| `test_angular.py` | 25 tests |
| `out/` | all results, checkpointed |

**Nothing here imports the sibling experiment's code.** The two deciders share only polygon
coordinates and the recorded answers being compared.

## Result

### 1. Controls — every hand-computed answer reproduced

| control | answer | exact quantity |
|---|---|---|
| equilateral triangle inscribed in itself | all 3 vertices good | side$^2=1$; **exactly one** good direction each |
| $30$-$30$-$120$, the §3.1 wedge witness | both $30°$ apexes **exceptional**, $120°$ apex good | side$^2=1/3$; exactly 3 good directions, $210°/240°/270°$ |
| unit square | all 4 corners good | side$^2=8-4\sqrt3$; exactly one good direction, $15°$ |
| `rotated-pair` (an edge **and** its own $60°$ rotate about $O$) | good | one **arc** component, exactly $315°\ldots360°$ |

The square's $8-4\sqrt3$ and the $30$-$30$-$120$'s $1/3$ agree with the sibling's independent
hand computations. The last row is the $M=0$ branch, constructed on purpose because random
rational polygons essentially never produce it; the arc predicted by hand
($\pm$ the cone of $e=[(1,-1),(1,0)]$, i.e. $-45°\ldots0°$) is exactly what came out.

### 2. Cross-validation against the sibling — 190/190, zero disagreements

Every one of the sibling's 190 committed fixtures was re-decided from scratch: every vertex,
and every recorded edge sample.

| | compared | disagreements |
|---|---|---|
| fixtures | 190 | **0** |
| vertices | 783 | **0** |
| edge-interior samples | 1 487 | **0** |
| **boundary points total** | **2 270** | **0** |

Also compared and agreeing on all 190: `simple`, `convex`, `orientation`. Every `good` verdict
of this lane carries a triangle that `recheck_witness` — which knows nothing about how it was
found — accepts: 0 rejected witnesses.

**Including the two fixtures where `sympy` was wrong.** `cvx-iso-t5773502691896257/10^16` and
`…258/10^16` bracket $\tan30°$ at the 16th digit ($1.4\times10^{-14}$ degrees apart, one on
each side of $60°$). Both are in the battery and this lane separates them the same way the
sibling does — by a different route, since it never computes an angle *or* a plane
intersection.

**No disagreement was found, so there is nothing to adjudicate.** That is the weaker of the two
outcomes available; a disagreement would have been worth more.

### 3. Where the cross-validation is weak, and what was done about it

The sibling's battery is **182 convex fixtures against 8 non-convex** ones. Agreement on it
therefore says very little about the non-convex answers this lane was asked to produce. So this
lane carries a **second decider of its own**, `rotcheck.py`: the rotation algorithm
($O$ good $\iff$ some $X\ne O$ lies in $J\cap\rho(J)$), written from scratch here, sharing with
the sweep only the field arithmetic and the vector helpers. Every decision in the
exceptional-set census is taken **twice**, by the sweep and by `rotcheck`.

This is deliberately *not* an independent idea — it is the sibling's idea, reimplemented — and
that is the point: it supplies the non-convex coverage the fixture battery lacks, while the
190-fixture agreement supplies the independent-idea check on the convex side.

### 4. What the good-direction set looks like — and when it can contain an interval

$G(O)$ is **always a finite union of closed arcs and isolated directions**. That is structural,
not observed: the breakpoints $D$ are finite, on each open gap the pair of edge-sets met by $v$
and $\rho v$ is constant, and for each of the finitely many ordered pairs the good set inside
that gap is either the whole gap ($M=0$) or at most the two points $\pm M$. So an *interval*
component requires $M=0$ for some pair.

**Over a polygon with rational vertices and a rational $O$, $M$ is never zero, so $G(O)$ is
finite.** Short argument: $k_e,k_f$ and $b-a$ are rational, and

$$\rho^{-1}(w)=\Big(\tfrac{w_x}{2}+\tfrac{\sqrt3}{2}w_y,\ -\tfrac{\sqrt3}{2}w_x+\tfrac{w_y}{2}\Big),$$

so the $\sqrt3$-parts of $M=k_e\rho^{-1}(w)-k_f(b-a)$ are $k_ew_y/2$ and $-k_ew_x/2$. Both
vanish only if $k_e=0$ (excluded — the edge is transversal) or $w=d-c=0$ (excluded — no
zero-length edge). **This is a `sketch`: my own argument, elementary but unreviewed, and per
`../../RULES.md` §3 nothing here is built on it — it is stated so a reviewer can attack it, and
the computation below is reported as the check, not as its consequence.**

The computation (`run.py structure`, all 190 fixtures, 927 boundary points, every proposed
direction re-decided by the independent checker):

| | |
|---|---|
| arc components over all rational-vertex fixtures | **0** |
| arc components over the whole battery | **1** |
| where | `ctl-tri-30-30-120`, at the **midpoint of the base** |
| components there | $\{0°\}\ \cup\ [30°,90°]\ \cup\ \{120°\}$ — 3 components, one an interval |

That one is hand-checkable and worth stating, because it is a **one-parameter family of
inscribed equilateral triangles at a single point** sitting inside the repo's own wedge-test
control. At $O=(0,0)$, the midpoint of the base of the $30$-$30$-$120$ triangle
$(\pm1,0),(0,\tfrac{\sqrt3}{3})$, the two upper edges lie on the lines $x+\sqrt3y=1$ and
$-x+\sqrt3y=1$. Both are at distance $\tfrac12$ from $O$, and their normals are at $60°$ and
$120°$ — so the left edge's line **is** the $+60°$ rotate of the right edge's line about $O$.
Every $\theta\in[30°,90°]$ therefore gives an inscribed triangle; at $\theta=30°$ and $90°$ the
side is $\tfrac{\sqrt3}{3}$ (side$^2=1/3$), at $\theta=60°$ it is $\tfrac12$ (side$^2=1/4$).
The code produces exactly those, exactly.

**How many components can $G(O)$ have?** No bound was found. Observed maxima:

| population | points | max components |
|---|---|---|
| the 190 committed fixtures | 927 | **13** (`ncv-dart`) |
| seeded non-convex polygons (`run.py explore`) | 2 353 | **29** |

The component count grows with the number of edges, which is what the sweep predicts: the
count is bounded by $O(n^3)$ (breakpoints $\times$ edge pairs) and nothing observed suggests a
constant bound. **A convex vertex has very few**: 1 for every corner of a square or a
rectangle, 1 at each vertex of the equilateral triangle, 3 at the $120°$ apex.

### 5. Critically good points — good for exactly one direction

A **critically good** point is one with $|G(O)|=1$: goodness holds, but only just. It is the
non-convex analogue of the convex lane's exactly-$60°$ boundary case, and it is where a
perturbation turns a good point exceptional.

They are not rare, and the first examples are the controls themselves: **every vertex of the
equilateral triangle and every corner of the unit square is critically good** (one direction
each — $0°$ and $15°$ respectively). `critical.py` re-derives six more on seeded non-convex
polygons and commits them to `out/critical_fixture.json`, each with:

- the exact polygon and the exact $O$;
- the exact good direction and scale in $K$, with $G(O)$ recomputed and asserted to have
  exactly one component and no arc;
- the exact triangle, accepted by `recheck_witness`;
- confirmation from the independent `rotcheck` decider — and, since there is only one good
  direction, that decider's witness is **the same triangle**, which it is in all six.

Their interior angles are $78°$, $92°$, $119°$, $147°$, $195°$, $201°$ — including reflex ones.
So being critically good is not a statement about the interior angle at $O$; it is a statement
about the whole curve as seen from $O$.

### 6. How large is the exceptional set? — never 3, in 51 587 exactly-decided boundary points

The problem README records, as `cited`\* (provisional — the source has not been read here),
**Meyerson (1980): $\lvert E(J)\rvert\le2$ for every Jordan curve, and $2$ is attained.** Three
exceptional points on a polygon would contradict that. Per `../../RULES.md` §7 the finding
would be reported as "this appears to show", checked to destruction and flagged — so this run
was set up to find one if it exists. Every decision in the **hunt** is taken **twice**, by the
sweep and by the independent `rotcheck` decider; the battery row is instead covered by the
190/190 agreement with the sibling in §2.

| population | polygons | boundary points decided | max exceptional found |
|---|---|---|---|
| the 190 committed fixtures (`run.py structure`) | 190 | 927 | **2** |
| seeded hunt (`run.py hunt 1500`, killed by its own timeout at 1450) | 1 450 | 50 660 | **2** |
| **total** | **1 640** | **51 587** | **2** |

Of the 1 450 hunted polygons, 1 394 were non-convex; the distribution of the exceptional count
was $0\!:\!422$, $1\!:\!271$, $2\!:\!757$. Over the battery it was $0\!:\!21$, $1\!:\!66$,
$2\!:\!103$. **Three was never found**, and the bound $2$ is not merely respected but routinely
attained — including by the $30$-$30$-$120$ control, which is the standard sharpness example.

Two further observations, both zero-exception across everything run here:

- **Every exceptional point found was a vertex.** No sampled edge-interior point — 1 487 in the
  battery cross-check, thousands more in the hunt and in `explore` — was ever exceptional. This
  extends the sibling's C2/C5 to the non-convex hunt, and it is what one expects: at an
  edge-interior point both along-edge rays see a whole interval of radii, which is a lot of
  freedom to match.
- **The sweep and `rotcheck` never disagreed** — 0 internal disagreements over 50 660 points —
  and no witness was ever rejected by `recheck_witness`.

So the run **confirms** the cited bound rather than contradicting it. That is a useful
independent check on a citation this project has not been able to read, and nothing more: it
tests polygons, and Meyerson's theorem is about all Jordan curves.

## What would make this wrong

Listed as blind spots, not as reassurances.

1. **The exceptional set is sampled, not solved.** For each polygon I decide the vertices and
   2–3 rational interior points per edge. The true exceptional set could contain an
   edge-interior point I did not sample. Every exceptional point ever found here was a vertex,
   but that is an observation, not a theorem, and **this lane does not decide, for a given
   edge, the set of $O$ on it that are exceptional** — that is a one-parameter family and would
   need a different computation. So "max exceptional found = 2" is a lower bound on a maximum,
   over a sample.
2. **Non-convex agreement rests on my own second decider.** The sibling battery is 182 convex
   to 8 non-convex, so the 190/190 agreement is mostly a convex check. `rotcheck.py` supplies
   the non-convex coverage, but it implements *the sibling's idea*, so it is coverage, not a
   third independent opinion. A shared misconception about the rotation criterion would not be
   caught by it. The criterion itself is re-derived in this README, which is the mitigation.
3. **Polygons are the most regular curves there are.** Nothing here says anything about
   non-polygonal Jordan curves, and per this problem's `RULES.md` §3.3 agreement on polygons is
   weak evidence about the general case and none about the wild one.
4. **The generators are not a sample of anything.** `random_star` and `random_spiky` are
   seeded, deterministic and adversarially shaped toward thin spikes, but they are not uniform
   over any natural family; $n\le12$ in the battery and $n\le15$ in the hunt. "No counterexample
   found" is a statement about this search, not about polygons.
5. **The finiteness-of-$G(O)$ argument is a `sketch`.** It is elementary and stated above so it
   can be attacked, but it is my own and unreviewed, and per `../../RULES.md` §3 nothing here —
   including this file — builds on it.
6. **Meyerson's bound is `cited`\*, i.e. provisional in this repo.** This computation is
   consistent with it. It cannot promote it, and if the citation turns out to say something
   else, the computation stands and the framing does not.
7. **The hunt did not finish.** It was launched for 1 500 polygons under a wall-clock timeout
   and was cut off at 1 450, per the compute budget in `../../RULES.md` §6. The reported
   numbers are the last checkpoint, which is why they are odd numbers.
