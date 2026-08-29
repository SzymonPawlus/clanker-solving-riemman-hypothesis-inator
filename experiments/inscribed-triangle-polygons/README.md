# inscribed-triangle-polygons

**Status: `numerical`.** Everything this directory produces is evidence, never a proof step
(`RULES.md` §3). The arithmetic here is *exact* — no floating point enters any decision — so the
answer for each individual fixture is certain. That is a strictly weaker thing than the
conjectures being true, and the difference is the entire point of the status: **exact arithmetic
on a fixture makes the fixture's answer certain, not the general claim.** The claims below are
statements about infinite classes of curves; finitely many polygons have been checked, all of
them chosen by the author or by a seeded generator the author also wrote.

Issue: [#132](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/132).
Journal: [`../../notebook/claude/2026-08-29-iet-numerics.md`](../../notebook/claude/2026-08-29-iet-numerics.md).

This is the **control** on the problem's prose lanes. If an argument in
`problems/inscribed-equilateral-triangle/attacks/` contradicts a fixture here, the fixture wins
and the argument is broken. It cannot be run in the other direction: agreement with the battery
is not verification of anything.

## Question

The triangle peg problem asks whether every Jordan curve in the plane contains three points
forming an equilateral triangle. This directory settles the *polygonal, one-vertex-fixed* version
of that question exactly.

Fix a simple polygon $P$ with vertices in $\mathbb{Q}$ (or in $\mathbb{Q}(\sqrt3)$), and let
$J=\partial P$, a Jordan curve. Call $O\in J$ **good** if some nondegenerate equilateral triangle
has all three vertices on $J$, one of them equal to $O$. Decide goodness, exactly, for a given
$O$ and $P$.

## The reduction

Let $\rho_\sigma$ be rotation by $\sigma\cdot 60^\circ$ about $O$, $\sigma\in\{+1,-1\}$.

> $O$ is good $\iff$ for some $\sigma$ there is $X\in\rho_\sigma(J)\cap J$ with $X\neq O$.

**($\Leftarrow$)** Put $Q=\rho_\sigma^{-1}(X)\in J$. A rotation is an isometry fixing $O$, so
$|OQ|=|OX|$, and $\angle QOX=60^\circ$. An isoceles triangle with apex angle $60^\circ$ has base
angles $(180-60)/2=60^\circ$, hence is equilateral. It is nondegenerate: $X\neq O$ makes the side
positive, and a $60^\circ$ apex forces $Q\neq X$.

**($\Rightarrow$)** If $OAB$ is equilateral with side $s>0$ and all three points on $J$, then $B$
is the image of $A$ under rotation about $O$ by $+60^\circ$ or $-60^\circ$ — the two vertices
adjacent to $O$ sit at exactly those two angles from each other, at equal radius. For that
$\sigma$, $X=B$ lies in $J$ and in $\rho_\sigma(J)$, and $X\neq O$ because $s>0$.

Both $J$ and $\rho_\sigma(J)$ are finite unions of closed segments, so the test is finitely many
segment–segment intersections.

### The trap the reduction sets

$\rho_\sigma(O)=O$, so $O\in\rho_\sigma(J)\cap J$ **always**, for every $O$ and every $\sigma$.
The intersection is never empty. A decider that forgets to exclude $O$ reports the degenerate
"triangle" $O,O,O$ and declares every point of every curve good — fluently, and with exact
arithmetic. The $30^\circ$-apex control below exists purely to catch that: there the intersection
is nonempty for 8 segment pairs and every one of them meets *only* at $O$.

## Method

### Exact arithmetic in $K=\mathbb{Q}(\sqrt3)$

The only irrationality anywhere in the problem is $\sin 60^\circ=\sqrt3/2$. Rotating a rational
point by $\pm60^\circ$ lands in $K$; intersecting two $K$-segments uses only $+,-,\times,\div$, so
it stays in $K$. Every number in the pipeline therefore lives in $K$, and an element is stored as
a pair of `Fraction`s $(a,b)$ meaning $a+b\sqrt3$ (`k3.py`, standard library only — no sympy,
no numpy). Two facts make this total and exact:

1. **Zero test is syntactic.** $\sqrt3\notin\mathbb{Q}$, so $a+b\sqrt3=0$ forces $a=b=0$. There is
   no tolerance anywhere in this code.
2. **Sign test is a rational comparison.** Same-sign coefficients decide immediately; opposite
   signs are decided by comparing $a^2$ with $3b^2$. $a^2=3b^2$ with $b\neq0$ would make $\sqrt3$
   rational, so it cannot occur — the code raises there rather than quietly returning $0$.

`float()` exists on the number type for *display only*; no predicate in `geom.py` calls it.
There is **no pre-screening**: every pair is tested exactly, so nothing needs confirming afterwards.

### Degeneracy

`seg_intersect` returns one of `empty`, `point`, or `segment` (collinear overlap), and handles
zero-length inputs, shared endpoints, parallel-but-distinct lines, and collinear-but-disjoint
segments. A component is discarded only when it is exactly $\{O\}$: for a `segment` component both
endpoints must equal $O$, which for a genuine segment is impossible, so overlaps always produce a
witness. Since the union of the pairwise components *is* the intersection, "every component is
$\{O\}$" is precisely "the intersection is $\{O\}$" — the not-good verdict is a proof about that
fixture, not a failure to find something.

### Witnesses are re-checked, not asserted

Every reported witness goes through `verify_triangle`, which ignores how it was found and asks
only: are $O,Q,X$ each on $\partial P$, pairwise distinct, and pairwise equidistant (exactly, as
squared distances in $K$)? A search that reports a witness its own verifier rejects would be
caught here. Across the whole battery: 0 verification failures.

### Angle classification without computing an angle

For the interior angle at a vertex, with $u,w$ the two edge vectors, $c=u\cdot w$, $s=u\times w$:
$\theta<60^\circ \iff c>0 \wedge s^2<3c^2$, and $\theta=60^\circ \iff c>0 \wedge s^2=3c^2$
(since $\tan\theta=|s|/c$ for $c>0$ and $\tan 60^\circ=\sqrt3$); for $c\le 0$, $\theta\ge90^\circ$.
Reflex vertices are detected by comparing the turn sign against the polygon orientation and have
interior angle $>180^\circ>60^\circ$ unconditionally. No transcendental function is involved.

### Independent cross-check

`crosscheck_sympy.py` re-decides every named fixture through a different code path entirely:
sympy `Rational`/`sqrt(3)` expressions instead of the coefficient pairs, and
`sympy.geometry.Segment2D.intersection` — which this experiment did not write — instead of
`seg_intersect`. Only the reduction and the fixture list are shared.

## Reproducing

```
sh run.sh
```

Stages, individually:

```
python3 run.py validate               # 67 hand-checked unit tests, then the three controls
python3 run.py battery                # the full fixture battery -> out/
python3 run.py hunt --count 20000     # seeded counterexample search -> out/hunt.json
python3 crosscheck_sympy.py           # independent re-decision with sympy
```

**Pinned versions, as actually used:** CPython **3.11.15**; the decision procedure imports only
`fractions` from the standard library and has no external dependency. **sympy 1.14.0** is used
*only* by `crosscheck_sympy.py`. The decider contains no randomness; the pseudorandom fixture and
hunt generators are seeded (`20260829`) and the whole run is deterministic — unlike a wall-clock
bounded search, re-running this reproduces the same output bit for bit on any machine.

Wall clock on the machine of record: `validate` ~1 s, `battery` 5.5 s, `hunt --count 20000`
4 min 20 s, sympy cross-check ~15 min. Nothing approaches the one-hour budget. Every stage
checkpoints: `out/fixtures/<name>.json` is written per fixture and `out/summary.json`,
`out/hunt.json`, `out/crosscheck_sympy.json` are rewritten as the run proceeds.

## The battery

190 fixtures (182 convex, 8 non-convex), all verified simple by an exact Jordan check
(`is_simple`: no zero-length edge, adjacent edges meeting exactly at their shared vertex,
non-adjacent edges disjoint). Groups:

- **controls** — the three hand-computed shapes.
- **convex** — regular hexagon and 12-gon (in $\mathbb{Q}(\sqrt3)$), a scalene triangle and a kite
  with an interior angle of *exactly* $60^\circ$, $10\times1$ and $1000\times1$ rectangles, a right
  triangle with legs $1$ and $1/1000$, sliver triangles, an irregular pentagon.
- **convex-boundary** — 18 isoceles triangles $O=(0,0)$, $A=(1,0)$, $B$ a rational point on the
  unit circle at angle $2\arctan t$, with $t$ straddling $\tan 30^\circ$.
- **nonconvex** — an L, a dart, a 6-pointed star, and 5 "C-strips" (below).
- **random** — 150 seeded convex hulls of random rational points, half of them squashed by a
  rational affine map $(x,y)\mapsto(x,y/k)$ to manufacture near-degenerate angles.

## Result

### 1. Controls — all three match the brief's predictions

| fixture | vertex | interior angle | good? |
|---|---|---|---|
| equilateral triangle $(0,0),(1,0),(\tfrac12,\tfrac{\sqrt3}{2})$ | all three | exactly $60^\circ$ | **yes**, side$^2=1$ exactly |
| $30$-$30$-$120$ triangle $(\pm1,0),(0,\tfrac{\sqrt3}{3})$ | $(-1,0)$ | $30^\circ$ | **no** |
| | $(1,0)$ | $30^\circ$ | **no** |
| | $(0,\tfrac{\sqrt3}{3})$ | $120^\circ$ | **yes** |
| unit square | all four | $90^\circ$ | **yes** |

The brief's reasoning at the $30^\circ$ apex — the whole polygon lies in a $30^\circ$ cone there,
so no two of its points subtend $60^\circ$ — is confirmed by the code, and confirmed in the strong
form: 8 segment pairs *do* intersect, and all 8 intersect only at $O$.

The unit square's corner witness is also checked against a hand computation:
$\rho_{+60}(1,t)$ has $y=1$ iff $t=2-\sqrt3$, and then $x=2-\sqrt3\in[0,1]$, giving
$Q=(1,\,2-\sqrt3)$ on the right edge, $X=(2-\sqrt3,\,1)$ on the top edge, side$^2=8-4\sqrt3$.
The code's independent verifier accepts exactly that triangle.

### 2. The convex characterisation holds — 88 346 vertices, no counterexample

> **C1.** For a convex polygon, a vertex $O$ is good $\iff$ its interior angle is $\ge 60^\circ$.

| | convex polygons | convex vertices | violations |
|---|---|---|---|
| battery | 182 | 721 | **0** |
| seeded hunt (`--count 20000`) | 20 000 | 87 625 | **0** |
| total | 20 182 | 88 346 | **0** |

The hunt's histogram is the cleanest statement of the result: of 87 625 vertices,
30 568 had interior angle $<60^\circ$ and **every one** was not good; 57 057 had angle
$\ge60^\circ$ and **every one** was good. No exceptions in either direction.

> **C2.** Every non-vertex point of a convex polygon's boundary is good.

1 177 sampled non-vertex points (rational parameters $t\in\{\tfrac15,\tfrac13,\tfrac12,\tfrac23,\tfrac45\}$
on every edge), **0** violations.

**The $60^\circ$ boundary, where a false conjecture would show itself.** The `convex-boundary`
family brackets $\tan 30^\circ=0.577350269189625764\ldots$ to 16 digits. The two tightest fixtures
have apex angles

```
t = 5773502691896257/10^16   ->  59.999999999999992909...°   ->  NOT good
t = 5773502691896258/10^16   ->  60.000000000000007105...°   ->  good
```

a gap of $1.4\times10^{-14}$ degrees, comfortably below what a double-precision angle computation
could be trusted to resolve. The exact code separates them without difficulty because it never
computes an angle: it compares $s^2$ against $3c^2$.

Exactly $60^\circ$ is also handled, and it is on the *good* side: `cvx-60deg-scalene` and
`cvx-60deg-kite` have an interior angle of exactly $60^\circ$ at the origin and both are good.
(The reason is short: the rotated cone meets the original in exactly the ray along the other edge,
so any $Q$ on one edge at distance $q\le\min(|OA|,|OB|)$ works.)

> **C7**, which fell out of the above. A polygon with **rational** vertices can never have an
> interior angle of exactly $60^\circ$, since $\tan\theta=|s|/c$ would be rational while
> $\tan 60^\circ=\sqrt3$ is not. Confirmed: 740 rational-coordinate vertices, 0 at exactly
> $60^\circ$. Consequently the equality case is only reachable with $\mathbb{Q}(\sqrt3)$ fixtures
> — a rational-only battery would silently never test it.

### 3. Non-convex: sub-$60^\circ$ vertices *can* be good, down to $0.29^\circ$

The `ncv-cstrip` family is a "C"-shaped strip (three sides of a square frame) whose free end
tapers to a point at the origin. The taper angle is $\arctan(h/10)$ and can be made as small as
wanted, while the far arm of the C is still seen from the origin at a wide angle.

| fixture | interior angle at the origin | good? |
|---|---|---|
| `ncv-cstrip-h2_1` | $11.309932^\circ$ | yes |
| `ncv-cstrip-h1_1` | $5.710593^\circ$ | yes |
| `ncv-cstrip-h1_2` | $2.862405^\circ$ | yes |
| `ncv-cstrip-h1_4` | $1.432096^\circ$ | yes |
| `ncv-cstrip-h1_20` | $0.286477^\circ$ | yes |

All five share the same witness, which was predicted by hand before the run and reproduced exactly
by the code: $Q=(8\sqrt3,\,0)$ on the bottom outer edge, $X=\rho_{+60}(Q)=(4\sqrt3,\,12)$ on the
top inner edge, side $=8\sqrt3$ (side$^2=192$). **So the convexity hypothesis in C1 is doing real
work: without it the angle condition is not necessary, and there is no positive lower bound on the
interior angle of a good vertex.**

The `ncv-star6` outline supplies six more, at $47.59^\circ$; the `ncv-dart` wing tips supply two
more, at $3.38^\circ$ and $7.79^\circ$. 13 sub-$60^\circ$ good vertices in total.

**The counterpoint that matters more.** Non-convexity by itself buys nothing. `ncv-dart` vertex 0
has interior angle $11.42^\circ$ and is **not** good, because the entire curve still lies inside
an $11.42^\circ$ cone at that vertex. The governing quantity is not the interior angle but the
**angular spread of $J$ as seen from $O$**; the interior angle is only a proxy for it, and only in
the convex case. Any convexity-based argument in the prose lanes should say which of the two it is
actually using.

Two further non-convex observations, both with 0 exceptions:

- **C5.** 310 sampled non-vertex points on the non-convex fixtures: all good.
- **C6.** 48 non-convex vertices with interior angle $\ge60^\circ$ (including all the reflex ones):
  all good. So the *sufficient* half of C1 survived every non-convex fixture too, even though the
  *necessary* half does not.

### 4. Three non-good vertices on a convex polygon: not found, and the argument survives

Over 20 182 convex polygons the maximum number of non-good vertices was **2**, attained often
(103 of the 182 battery fixtures, including the $30$-$30$-$120$ control and every sliver
triangle). **No convex polygon with 3 was found.**

The argument in the brief is that this is impossible: each non-good vertex has interior angle
$<60^\circ$ (the necessary half of C1), hence exterior angle $>120^\circ$, and three such would
exceed the total exterior angle $2\pi$. The only way to break it computationally is to break the
*forward* half of C1 — a convex vertex with angle $\ge60^\circ$ that is nevertheless not good —
so that is what `hunt` targets, with heavy rational squashing to manufacture near-degenerate
convex shapes. 87 625 vertices later, no such vertex exists in the search. The argument is not
refuted; it is also not proved by anything here.

### 5. Cross-check

Every named fixture re-decided through sympy 1.14.0's own exact geometry: **no disagreements**
(`out/crosscheck_sympy.json`).

## What would make this wrong

Stated plainly, because the battery is only as good as its blind spots:

- The fixture families are the author's idea of "extreme", and every one is small
  ($\le 12$ vertices). Convex polygons with hundreds of vertices, and non-convex ones with deeply
  nested spirals, are not represented at all.
- The non-vertex sampling is 5 rational parameters per edge. C2 and C5 are statements about a
  continuum and are tested on a finite grid; a bad point at an irrational parameter would be missed.
- The hunt's generator draws small-denominator rationals in a bounded box, and its notion of
  "near-degenerate" is a rational axis-aligned squash. Other degeneracies (nearly-collinear
  vertex triples, vastly different edge scales in one polygon) are only incidentally covered.
- C1, C2, C5, C6 and C7 are conjectures. Nothing in this directory promotes any of them beyond
  `numerical`, and nothing here may be used as a proof step.
