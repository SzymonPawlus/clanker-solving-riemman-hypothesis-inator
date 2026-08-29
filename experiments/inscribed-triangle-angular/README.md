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

