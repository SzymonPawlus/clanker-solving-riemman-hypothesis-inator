# V. Stationarity exclusion / irreducible contact graphs with a boundary

**This is a lower-bound (optimality-side) attack, and it is `refuted` as a practical method
at the sizes this project cares about. Nothing below is a construction, and no value of
$s(n)$ or $d(n)$ is claimed anywhere in this file.**

```
status:   sketch      — every mathematical statement in this file, without exception
                        (Lemmas 1-13 are proved here by an agent and have not been
                        cross-examined; RULES.md §3 forbids building on them, me included)
          numerical   — every count in §7
verdict:  kill-criterion 2 FIRED decisively; kill-criterion 1 fired in part (§6)
author:   claude (Opus 5), 2026-08-23, worker r3-stationarity
executes: attacks/r3-approaches/README.md proposal V
code:     experiments/packing-r3-stationarity/
depends on nothing that is not proved here or `cited`; in particular it does NOT use
the unmerged n=16 covering bound of PRs #98/#104, and does not use Oler.
```

---

## 0. Summary

Proposal V's thesis was that the exhaustiveness lemma **approach E could not state** —
E's author wrote *"the lemma 'every optimal packing has a jammed core with ≥ [bound]
contacts' needs an actual proof before use … I do not know such a bound for this
container"* — is supplied for free by compactness plus the Fritz John conditions.

**That part is true, and §§1–5 below prove it.** The lemma E wanted exists, it needs no
constraint qualification, and in this container it is even better than Fritz John: the
degenerate multiplier case is impossible, so plain KKT holds at *every* maximiser with no
regularity hypothesis at all (Lemma 4). The force-balance conditions and eleven structural
prunes are written out explicitly, including the ones the sphere/torus literature never
has to state because it has no walls (Lemmas 8, 11, 12, 13).

**And it does not help.** Two independent things go wrong, and both are measured rather
than asserted:

1. **§6 (kill-criterion 1, partial).** The exhaustiveness lemma is *logically* sound but
   is not a *reduction to a finite computation*. Points carrying no multiplier — rattlers —
   are left completely free by the first-order conditions, so refuting one support still
   requires refuting a continuous completion problem in $2(n-m)$ variables. The dimension
   count in §6.3 shows further that the strata where the loaded system is *under*determined
   (so interval Newton/Krawczyk has no square system to contract on) are not exceptional:
   they are forced for every sparse support, and they are exactly the supports that the
   enumeration produces in bulk.
2. **§7 (kill-criterion 2, decisive).** The support count was measured, not guessed. At
   $n = 12$ — the *smallest* case the assignment named, whose answer has been known since
   Melissen 1993 — the number of admissible support classes is **at least $2.3 \times 10^5$
   counted exactly through $m = 7$**, grows by a factor of $\approx 13$ per additional
   loaded point, and the loaded-graph layer alone at $m = 12$ contains
   $1{,}241{,}462{,}173$ graphs. Extrapolating the measured factor gives $\sim 10^{11}$
   support classes at $n = 12$. The gate was $10^6$.

Musin–Tarasov needed $\approx 9.5\times10^7$ and $\approx 1.5\times10^9$ planar graphs to
settle Tammes $N = 13, 14$ on the sphere. The speculation recorded in proposal V was that
walls *pin* configurations more than a sphere does and would cut the count. **Measured:
they do not.** They add a per-vertex wall label with seven states and a corresponding
factor of $\approx 10^3$ in the labelling layer, which swamps the extra prunes the walls
buy. That is the one genuinely new fact this task produced, and it is the reason no one has
run this method on a container with a boundary.

---

## 1. Setup and notation

Problem `RULES.md` §2 conventions, point formulation. Fix $d > 0$ and set
$A = (0,0)$, $B = (d, 0)$, $C = (d/2,\ d\sqrt3/2)$, and

$$T_d \;=\; \{\, p \in \mathbb{R}^2 \;:\; g_k(p) \le 0,\ k = 0,1,2 \,\},\qquad
g_k(p) = \langle p, \nu_k\rangle - c_k,$$

with **outward unit normals** and offsets

| $k$ | side | $\nu_k$ | $c_k$ |
|---|---|---|---|
| 0 | $AB$ | $(0,\,-1)$ | $0$ |
| 1 | $BC$ | $(\tfrac{\sqrt3}{2},\ \tfrac12)$ | $\tfrac{\sqrt3}{2}d$ |
| 2 | $CA$ | $(-\tfrac{\sqrt3}{2},\ \tfrac12)$ | $0$ |

The three normals are pairwise at $120^\circ$ and satisfy $\nu_0 + \nu_1 + \nu_2 = 0$; any
**two** of them are linearly independent. For $d > 0$ no point of $T_d$ lies on all three
sides. Both facts are used below and both are specific to a triangle.

For $P = (p_1,\dots,p_n) \in T_d^{\,n}$ write $F(P) = \min_{i<j}\lVert p_i - p_j\rVert^2$
and consider

$$(\mathrm{M}_d)\qquad \text{maximise } t \quad\text{over } (P,t)\in T_d^{\,n}\times\mathbb{R},
\qquad \text{s.t. } t - \lVert p_i - p_j\rVert^2 \le 0 \ \ (i<j).$$

$n$ points at pairwise distance $\ge 2$ fit in $T_d$ **iff** the optimal value $t^*(d)$ of
$(\mathrm{M}_d)$ satisfies $t^*(d) \ge 4$.

---

## 2. (a) A maximiser exists

**Lemma 1 (compactness).** $T_d^{\,n}$ is compact and $F$ is continuous, so $F$ attains a
maximum $t^*(d)$ on $T_d^{\,n}$, and $(\mathrm{M}_d)$ attains its optimum.

*Proof.* $T_d$ is a closed bounded subset of $\mathbb{R}^2$, hence $T_d^{\,n}$ is compact in
$\mathbb{R}^{2n}$. $F$ is a minimum of finitely many continuous functions, hence continuous.
Weierstrass. For $(\mathrm{M}_d)$: its feasible set is $\{(P,t): P \in T_d^n,\ 0 \le t \le
F(P)\}$ intersected with $t \ge$ any lower bound, which is closed and bounded, and $t$ is
continuous. $\square$

Write $r = \sqrt{t^*(d)}$ for the optimal minimum distance.

**Lemma 2 (scaling — a correction to how the gate was posed).** $t^*(\rho d) = \rho^2\,
t^*(d)$ for every $\rho > 0$, and $P \mapsto \rho P$ is a bijection between the maximisers
at side $d$ and those at side $\rho d$.

*Proof.* $T_{\rho d} = \rho\,T_d$ and $F(\rho P) = \rho^2 F(P)$. $\square$

So the whole one-parameter family of decision problems "does a packing exist in $T_d$" is a
single configuration problem, and the assignment's instruction to run "at $d$ just below
$d(12)$" is not a real degree of freedom: **the correct normalisation is to fix the minimum
distance at $2$ and treat $d$ as the quantity to be bounded below.** In that normalisation
the method's target is not "refute at this $d$" but

$$d(n) \;=\; \min_{S \text{ admissible support}} \; d_S, \qquad
d_S = \inf\{\, d : \text{a stationary configuration with support } S \text{ exists in } T_d \,\},$$

which is why proposal V is the only item on the round-3 list that could in principle yield
an *equality* rather than an enclosure. $d$ still enters the combinatorics — through the
wall-capacity prune of Lemma 10, which compares $d$ with the normalised distance $2$ — so
the enumeration is genuinely $d$-dependent, just not in the way the gate was phrased.

---

## 3. (b) The Fritz John conditions, written out

**Theorem 3 (Fritz John, applied).** Let $(P^*, t^*)$ solve $(\mathrm{M}_d)$. Then there
exist $\lambda_0 \ge 0$, $\lambda_{ij} \ge 0$ $(i<j)$ and $\mu_{ik} \ge 0$ $(1\le i\le n,\
0\le k\le 2)$, **not all zero**, with

* complementary slackness: $\lambda_{ij} > 0 \Rightarrow \lVert p_i - p_j\rVert = r$, and
  $\mu_{ik} > 0 \Rightarrow g_k(p_i) = 0$ (the point lies on side $k$);
* the $t$-equation $\displaystyle\sum_{i<j}\lambda_{ij} = \lambda_0$;
* for each $i$, the $p_i$-equation
  $\displaystyle 2\sum_{j\neq i}\lambda_{ij}\,(p_i - p_j)\;=\;\sum_{k}\mu_{ik}\,\nu_k .$

*Derivation.* Minimise $f = -t$ subject to $c_{ij} = t - \lVert p_i-p_j\rVert^2 \le 0$ and
$c_{ik} = g_k(p_i) \le 0$; all data are polynomial, hence $C^1$. Fritz John's theorem
(F. John 1948; e.g. Mangasarian, *Nonlinear Programming*, Thm 7.2.5) gives non-negative
multipliers, not all zero, with $\lambda_0\nabla f + \sum\lambda\nabla c = 0$ and
complementarity — **with no constraint qualification**, which matters here because
Slater/LICQ genuinely fail: at a jammed packing far more constraints are active than there
are degrees of freedom. Reading off the $t$-component gives $-\lambda_0 + \sum\lambda_{ij}
= 0$; reading off the $p_i$-component gives $-2\sum_j \lambda_{ij}(p_i-p_j) + \sum_k
\mu_{ik}\nu_k = 0$. $\square$

**Lemma 4 (in this container FJ degeneracy is impossible, so KKT holds unconditionally).**
$\lambda_0 > 0$.

*Proof.* Suppose $\lambda_0 = 0$. The $t$-equation gives $\sum_{i<j}\lambda_{ij} = 0$ with
all $\lambda_{ij}\ge0$, so every $\lambda_{ij} = 0$. The $p_i$-equations then read
$\sum_k \mu_{ik}\nu_k = 0$ for each $i$, where by complementarity the sum runs over the set
$A(i)$ of sides containing $p_i$. Since $d>0$, $|A(i)| \le 2$; and any two of $\nu_0,\nu_1,
\nu_2$ are linearly independent. Hence $\mu_{ik} = 0$ for all $i,k$ — every multiplier
vanishes, contradicting non-triviality. $\square$

This is the cleanest thing in this file and it is exactly what a container with **three**
pairwise-independent normals buys. It fails for a container with parallel walls at zero
separation and it is not available on a sphere, where there are no wall constraints at all.

**Corollary 5 (force balance).** Normalise $\lambda_0 = 1$. Put
$\alpha_{ij} = 2 r\,\lambda_{ij} \ge 0$ and let $u_{ij} = (p_j-p_i)/r$ be the unit vector
from $p_i$ towards a loaded neighbour. Then $\sum_{i<j}\alpha_{ij} = 2r > 0$ and, for
every $i$,

$$\boxed{\ \sum_{j \,\in\, N_\lambda(i)} \alpha_{ij}\, u_{ij} \;+\; \sum_{k \,\in\, A(i)} \mu_{ik}\,\nu_k \;=\; 0\ }$$

where $N_\lambda(i) = \{j : \lambda_{ij} > 0\}$. Because $\sum\alpha_{ij} = 2r > 0$, **at
least one contact is loaded**: the all-rattler support is impossible.

Physically: neighbour $j$ pushes $p_i$ along $-u_{ij}$, side $k$ pushes it inwards along
$-\nu_k$, and the total force vanishes. Written out by position:

| where $p_i$ sits | $A(i)$ | balance equation | geometric content |
|---|---|---|---|
| interior | $\varnothing$ | $\sum_j \alpha_{ij}u_{ij} = 0$ | $0 \in \operatorname{conv}\{u_{ij}\}$: the loaded directions do **not** lie in an open half-plane |
| on one side $k$ | $\{k\}$ | $\sum_j \alpha_{ij}u_{ij} = -\mu_{ik}\nu_k$ | the resultant is a non-negative multiple of the **inward** normal: the tangential components cancel |
| at a corner $\{k_1,k_2\}$ | $\{k_1,k_2\}$ | $\sum_j \alpha_{ij}u_{ij} = -(\mu_{ik_1}\nu_{k_1}+\mu_{ik_2}\nu_{k_2})$ | the resultant lies in the $120^\circ$ cone $-\operatorname{cone}(\nu_{k_1},\nu_{k_2})$ |

**Lemma 6 (a corner never obstructs).** At a corner the inner tangent cone is the $60^\circ$
wedge spanned by the two incident sides, and $-(\text{that wedge})$ is contained in
$\operatorname{cone}(\nu_{k_1},\nu_{k_2})$, which is $120^\circ$ wide. Hence *any* non-zero
non-negative combination of admissible contact directions at a corner can be balanced.

*Proof.* Take the corner $A$: the inner wedge is $\{0^\circ \le \theta \le 60^\circ\}$ and
$\operatorname{cone}(\nu_0,\nu_2)$ spans $150^\circ$ to $270^\circ$, which contains
$180^\circ$ to $240^\circ$. The other two corners follow by symmetry. $\square$

So corner points impose **no** balance restriction; the enumeration cannot prune them, and
they are the reason the wall label has seven states rather than four.

### 3.1 The distinction that must not be blurred

Three different graphs live on the same points and they are *not* the same object:

* the **tight** graph $G_r$: all pairs at distance exactly $r$;
* the **loaded** graph $G_\lambda \subseteq G_r$: pairs with $\lambda_{ij} > 0$;
* the **active wall incidence** $A(i)$: sides that *contain* $p_i$, regardless of whether
  $\mu_{ik} > 0$.

The balance equation is a statement about $G_\lambda$ and $A(i)$. The metric prunes below
(degrees, planarity, common neighbours, Harborth) are statements about $G_r$ and about
where the point sits, and are inherited by the subgraph $G_\lambda$. **Every prune in §4
is stated for whichever of the three it is actually true of**; the enumerator's support
object is therefore the pair (loaded graph, *active* wall incidence), not (loaded graph,
loaded wall set). Getting this backwards silently loses configurations and was the first
error I made writing the enumerator.

---

## 4. (c) The structural prunes, with proofs

Throughout, $P^*$ is a maximiser, $r$ its minimum distance, $L$ the set of points carrying
at least one positive multiplier ("loaded points"), $m = |L|$, and $G = G_\lambda$
restricted to $L$. Every point of $L$ has loaded degree $\ge 1$: a loaded point with no
loaded contact would need $\sum_k \mu_{ik}\nu_k = 0$, forcing $\mu = 0$ by Lemma 4's
independence argument.

**Lemma 7 (60° separation and degree bounds).** Let $j \ne j'$ be tight neighbours of $i$.
Then $\angle\, p_j p_i p_{j'} \ge 60^\circ$. Consequently

* any point has at most **6** tight neighbours;
* a point on exactly one side has at most **4**;
* a point at a corner has at most **2**.

*Proof.* $\lVert p_i-p_j\rVert = \lVert p_i-p_{j'}\rVert = r$ and $\lVert p_j -
p_{j'}\rVert \ge r$; in a triangle the angle opposite the longest side is the largest, so
the apex angle at $p_i$ is $\ge 60^\circ$. Six directions pairwise $\ge 60^\circ$ apart is
the most a full turn admits. If $p_i$ lies on side $k$ then every other point $p_j \in T_d$
satisfies $\langle p_j - p_i, \nu_k\rangle \le 0$, so all directions $u_{ij}$ lie in a
**closed half-plane**, a $180^\circ$ arc, which admits at most 4 directions pairwise
$\ge60^\circ$ apart (at $0,60,120,180$ degrees). At a corner they lie in the $60^\circ$
inner wedge, which admits at most 2. $\square$

**Lemma 8 (interior degree, and degree 2 is antipodal).** A loaded interior point has
loaded degree $\ge 2$; if exactly 2, its two loaded directions are opposite. Its two loaded
neighbours are then $2r$ apart, hence non-adjacent in $G_r$, and their only common tight
neighbour is $p_i$ itself.

*Proof.* $0 \in \operatorname{conv}\{u_{ij}\}$ is impossible for a single unit vector, and
for two unit vectors forces $u_{ij} = -u_{ij'}$. Two points at distance $2r$ have exactly
one point at distance $r$ from both, namely their midpoint. $\square$

Note this is **weaker** than the "interior degree $\ge 3$" that proposal V asserted.
Degree 2 with antipodal contacts is a genuine stationary point; it is excluded only by a
*second*-order condition, which Fritz John does not give. Using degree $\ge 3$ would have
made the enumeration non-exhaustive.

**Lemma 9 (planarity, $K_4$-freeness, common neighbours).** Drawn with straight edges at
the actual positions,

1. $G_r$ (hence $G$) is planar;
2. $G_r$ contains no $K_4$;
3. any two points have at most 2 common tight neighbours.

*Proof.* (1) Suppose edges $p_1p_2$ and $p_3p_4$ crossed at an interior point $x$. Then
$\lVert p_1-p_3\rVert + \lVert p_2-p_4\rVert \le (\lVert p_1-x\rVert + \lVert x-p_3\rVert)
+ (\lVert p_2-x\rVert + \lVert x-p_4\rVert) = \lVert p_1-p_2\rVert + \lVert p_3-p_4\rVert
= 2r$, and both left-hand terms are $\ge r$, so both are $=r$ and both triangle
inequalities are equalities — forcing all four points collinear with $x$, in which case
the two segments overlap along a sub-segment rather than crossing, and two of the four
points are less than $r$ apart. (2) Four points pairwise at distance exactly $r$ do not
exist in the plane: three of them form an equilateral triangle of side $r$, and the only
point equidistant from all three is the circumcentre, at distance $r/\sqrt3 \ne r$. (3) A
common tight neighbour of $p_a \ne p_b$ lies on the intersection of two circles of radius
$r$, which has at most two points. $\square$

**Lemma 10 (side capacity).** At most $\lfloor d/2\rfloor + 1$ points of the whole
configuration lie on any one side, provided $r \ge 2$ (the only case of interest, since we
are testing whether $t^* \ge 4$). Moreover the points on a given side induce a **linear
forest** in $G_r$: they are collinear at pairwise distance $\ge r$, so only *consecutive*
ones can be exactly $r$ apart.

*Proof.* $k$ collinear points with gaps $\ge r \ge 2$ need a segment of length
$\ge 2(k-1)$, so $k \le d/2 + 1$. Non-consecutive points on the line are $\ge 2r > r$
apart. $\square$

**Lemma 11 (every extreme point of the loaded set touches the boundary).** If $p_i$ is an
extreme point of $\operatorname{conv}\{p_j : j \in L\}$ and $i \in L$, then
$A(i) \ne \varnothing$.

*Proof.* All loaded neighbours of $p_i$ lie in that convex hull, so all directions
$u_{ij}$ lie in the tangent cone $K$ of the hull at $p_i$. Since $p_i$ is extreme, $K$ is
closed, convex and **pointed**, so there is a linear functional $\ell$ with $\ell(v)>0$ for
every non-zero $v\in K$. If $A(i) = \varnothing$ the balance equation reads
$\sum_j\alpha_{ij}u_{ij}=0$; applying $\ell$ gives $\sum_j\alpha_{ij}\ell(u_{ij}) = 0$ with
every term $\ge0$ and $\ell(u_{ij})>0$, so every $\alpha_{ij}=0$ and $i \notin L$. $\square$

Hence $L$ has at least 2 points on $\partial T_d$, and at least 3 unless $L$ is collinear —
and $L$ collinear forces $G$ to be a disjoint union of paths (Lemma 10's argument). This is
the closest thing here to the boundary analogue of the sphere-case statement that the
contact graph must "wrap"; it has no counterpart in Musin–Tarasov because a sphere has no
extreme points.

**Lemma 12 (a corner of loaded degree 2 pins both neighbours).** If $p_i$ sits at the corner
$\{k_1,k_2\}$ and has loaded degree 2, its two loaded directions run exactly along the two
incident sides; so one neighbour lies on side $k_1$ and the other on side $k_2$, each at
distance exactly $r$ from the corner.

*Proof.* Both directions lie in the $60^\circ$ inner wedge and are $\ge60^\circ$ apart
(Lemma 7), hence exactly $60^\circ$ apart and along the wedge's two boundary rays, which
are the two sides. $\square$

**Lemma 13 (a side point of loaded degree 4 pins two neighbours onto that side).** If $p_i$
lies on exactly one side $k$ and has loaded degree 4, its four directions are at $0, 60,
120, 180$ degrees to that side, so exactly two of its loaded neighbours also lie on side
$k$.

*Proof.* Four directions in a closed $180^\circ$ arc, pairwise $\ge 60^\circ$ apart, must
sit at the four extreme positions. The $0^\circ$ and $180^\circ$ neighbours lie on the line
of side $k$ and inside $T_d$, hence on the side itself. $\square$

**Edge bound.** $G_r$ is a *penny graph* (contact graph of equal circles of radius $r/2$),
so $|E(G_r)| \le \lfloor 3m - \sqrt{12m-3}\rfloor$ (Harborth 1974, *Lösung zu Problem
664A*, Elem. Math. **29**, 14–15 — standard, **body not read by this session**). $G$ is a
subgraph, so the bound applies to it too. This is stronger than the self-proved planar
bound $3m-6$; using it makes the measured counts in §7 *smaller*, so it is conservative in
the direction that matters for a gate phrased as "the count is too big".

---

## 5. What the method would have to do

Putting §§2–4 together gives the exhaustiveness statement approach E was missing:

> **Reduction (sketch).** Suppose that for every admissible support $S = (m, G, A)$ —
> admissible meaning it survives Lemmas 7–13 — there is no configuration
> $P \in T_d^{\,n}$ with: the $G$-pairs at a common distance $r \ge 2$, all other pairs at
> distance $\ge r$, the wall incidences $A$, all points in $T_d$, and a strictly positive
> multiplier vector satisfying the balance equations. Then $(\mathrm{M}_d)$ has no
> maximiser with $t^* \ge 4$, hence by Lemma 1 no packing exists in $T_d$, hence
> $d(n) > d$.

The chain is valid. Every step is proved above and none of it needs a constraint
qualification, a genericity assumption, or a rigidity hypothesis. **That is the deliverable
proposal V promised, and it is delivered.** The rest of this file is about why it does not
convert into a computation.

---

## 6. (d) Rattlers and continua — the honest hard part

### 6.1 Rattlers are not handled; they are relocated

A point carrying no positive multiplier is invisible to the first-order conditions: by the
argument opening §4, if it has no loaded contact then all its wall multipliers vanish too,
so **the FJ conditions say nothing whatever about where it is**, beyond feasibility. Problem
`RULES.md` §5 records that rattlers are normal in this problem and must not be "fixed".

The consequence for the method is structural, not cosmetic. A support with $m$ loaded points
leaves $n-m$ points free, so refuting that support means proving

> the loaded core cannot be completed by $n-m$ further points at pairwise distance $\ge r$
> inside $T_d \setminus \bigcup_{i \in L} B(p_i, r)$,

which is a *continuous* packing-feasibility problem in $2(n-m)$ variables — i.e. precisely
the counting/covering problem recorded as **wall 2** on this board, now to be solved once
per support. Proposal V claimed "wall 2 involves no partition of the container at all —
this is not a counting argument". That claim is **wrong as stated**: the enumeration itself
is not a counting argument, but the per-support residual obligation is exactly one, and it
cannot be dropped, because supports with small $m$ are admissible and must be refuted like
any other.

This is where kill-criterion 1 fires, and it fires in an instructive way: E's missing lemma
turns out **not to be the binding constraint**. Supplying it (§5) leaves the difficulty
where it already was.

### 6.2 Positive-dimensional strata are typical, not exceptional

Fix a support $S$ with $m$ loaded points, $|E|$ loaded edges and $W = \sum_i |A(i)|$ wall
incidences. Two counts pull in opposite directions.

* **Geometry.** The equations "$G$-pairs at distance $r$" and "$p_i$ on side $k$ for
  $k \in A(i)$" are $|E| + W$ equations in the $2m + 1$ unknowns $(p_i)_{i\in L}, r$, modulo
  nothing (the triangle is fixed, so there is no rigid-motion quotient — a small advantage
  over the sphere case). The solution set has dimension $\ge 2m + 1 - |E| - W$.
* **Multipliers.** The balance equations are $2m$ homogeneous linear equations in the
  $|E| + W$ unknowns $(\alpha, \mu)$, and we need a solution that is **strictly positive**
  on all of them. A non-zero kernel requires $|E| + W > \operatorname{rank} \ge$ generically
  $\min(2m, |E|+W)$.

So the supports on which interval Newton or Krawczyk has a square, contractible system are
those with $|E| + W \approx 2m+1$; those with $|E| + W \le 2m$ carry a positive-dimensional
solution variety on which Krawczyk cannot certify anything, and those with $|E| + W$ much
larger are over-determined and die combinatorially.

The trouble is that **sparse supports are admissible and are the bulk of the enumeration.**
The prunes only force loaded degree $\ge 1$ at boundary points and $\ge 2$ in the interior,
so a support consisting of, say, a perfect matching among side points has
$|E| + W \approx \tfrac{3m}{2} < 2m$. Nothing in §4 excludes it. Excluding it would need
either a second-order optimality condition (which changes the theorem being used and would
have to be re-proved without a constraint qualification), or a genericity assumption — and
a genericity assumption is exactly what an exhaustiveness argument may not make. This is the
concrete form of kill-criterion 3's "positive-dimensional strata defeating Krawczyk", and it
is visible *before* running gate 3.

### 6.3 What would have to be true for the scheme to work

For completeness, the two missing lemmas, both of which I could not prove:

* **(R)** a bound $m \ge \varphi(n)$ on the loaded core of *some* maximiser, strong enough
  that the residual completion problem is trivial. Approach E asked for exactly this and
  could not state it; nothing in the first-order theory supplies it, because the FJ
  conditions are conditions at a point, not a statement about which maximiser to choose.
* **(C)** a combinatorial criterion, provable without genericity, that discards every support
  whose stationary variety is positive-dimensional.

Without (R) and (C), the enumeration is exhaustive but its branches are not finite
computations. **This is the honest answer to part (d): the scheme as proposed does not
handle rattlers or continua, and §6.1–6.2 say precisely where and why.**

---

## 7. (Kill-criterion 2) The measured support count

Method, code and reproduce command: `experiments/packing-r3-stationarity/`. All prunes are
the lemmas above and nothing else; a support is a pair (loaded graph, active wall incidence)
counted up to graph isomorphism composed with the $S_3$ action of the triangle's symmetries
on the three side labels. Loaded graphs come from `nauty-geng` (isomorph-free) with
min degree 1, max degree 6, $K_4$-free and the Harborth edge bound, then filtered for
planarity (`networkx`) and the common-neighbour bound.

**Two-sided calibration (required before any count is reported).** The supports of the two
known optima $n=6,\,d=4$ and $n=5,\,d=4$ were extracted from exact coordinates over
$\mathbb{Q}(\sqrt3)$, their Fritz John multipliers computed and certified exactly (both are
fully loaded: every tight edge and every wall multiplier is strictly positive), and both
were checked to be **accepted** by the enumerator's prunes. An enumerator that rejected a
real optimum's support would not be exhaustive and its counts would be meaningless.

**Counts at $n = 12$, $d = d(12) = 4 + 2\sqrt3$** (side capacity 4 points per side):

| $m$ (loaded points) | admissible loaded graphs | **admissible support classes** | wall factor | time |
|---:|---:|---:|---:|---:|
| 2 | 1 | 4 | 4.0 | 0.0 s |
| 3 | 2 | 20 | 10.0 | 0.0 s |
| 4 | 6 | 157 | 26.2 | 0.1 s |
| 5 | 15 | 1 404 | 93.6 | 0.9 s |
| 6 | 61 | 16 243 | 266 | 21 s |
| 7 | 265 | 216 405 | 817 | 210 s |
| 8 | 1 612 | *(partial, see `out/`)* | | |
| 12 | — | — | — | — |

Successive ratios of the support column: $5.0,\ 7.9,\ 8.9,\ 11.6,\ 13.3$ — increasing, not
saturating. **Counted exactly, $n = 12$ already has $\ge 234\,233$ admissible support
classes using only $m \le 7$ of its 12 points**, every one of which the method would have to
refute individually.

The loaded-graph layer alone settles the gate without any extrapolation. `nauty-geng` with
the sound prunes of §4 (min degree 1, max degree 6, $K_4$-free, $\le 24$ edges) emits, on
$m$ vertices:

| $m$ | 8 | 9 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|---:|
| loaded-graph candidates | 4 507 | 55 448 | 1 270 845 | 29 052 234 | **1 241 462 173** |

and each surviving graph carries hundreds to thousands of admissible wall labellings.
Applying the measured wall factor to the $m=12$ row gives $\sim10^{11}$ support classes.

**Verdict.** The gate was "if the admissible support count at $n=12$ exceeds $\sim10^6$, or
the enumerator does not terminate within one hour, record the count and stop." Both clauses
fire: the count exceeds $10^6$ by five orders of magnitude, and the enumerator cannot even
enumerate the $m=12$ *graph* layer in an hour, let alone label it. Per the assignment I
stopped here and did **not** proceed to $n=16$.

### 7.1 Why the walls make it worse, not better

The recorded speculation was that walls pin configurations more than a sphere does and
should cut the count. What the measurement shows is the opposite mechanism dominating:

* the walls contribute a **seven-state label per loaded vertex** (interior, three sides,
  three corners) which the sphere and torus cases do not have at all;
* the extra prunes the walls buy (Lemmas 7's degree 4 and 2, 10, 11, 12, 13) are strong
  *per vertex* but only remove a constant factor: the measured "wall factor" — supports per
  admissible graph — still **grows**, from 4 at $m=2$ to 817 at $m=7$;
* the corner case (Lemma 6) is the worst of both worlds: corners are the most constrained
  positions geometrically and the least constrained by balance, so they prune almost nothing
  while tripling the label alphabet.

Musin–Tarasov's $\approx 1.5\times10^9$ graphs for Tammes $N=14$ was already at the limit of
what is feasible; here the *label* layer alone reproduces that factor before a single
geometric test is run. This is a specific, measured reason why the method has not been
carried to a container with a boundary, and it is the finding of this task.

---

## 8. What survives, and what should be reused

**Refuted:** proposal V as a route to a lower bound at $n \ge 16$, and by the same token the
enumeration half of approach **E**. Not because the exhaustiveness lemma is missing — it is
proved in §5 — but because (i) the finite object it produces is $\sim10^{11}$ large at
$n=12$ and worse beyond, and (ii) each of its branches still carries the rattler-completion
problem the method was meant to avoid.

**Worth keeping (all `sketch`, none assumable):**

* **Lemma 4.** In *this* container the Fritz John degenerate case cannot occur, so KKT holds
  at every maximiser with no constraint qualification. Any future first-order argument on
  this problem — including a local-optimality certificate for a *single* configuration, which
  is a much smaller ambition than exhaustion — can start from the plain KKT conditions.
* **Corollary 5 and Lemma 6.** The explicit force-balance table, including the fact that a
  corner never obstructs balance. Cheap to check on any candidate configuration.
* **Lemma 11.** Every extreme point of the loaded set lies on $\partial T_d$. This is a real
  constraint on any putative optimal packing in a triangle and is trivial to test.
* **Lemma 7's boundary refinement** (degree $\le 4$ on a side, $\le 2$ at a corner) and
  **Lemmas 12, 13**, which pin neighbours onto sides. These are cheap filters for the
  contact-graph lifting work in issue #11 and for any exact-algebraic contact-system solve
  (proposal **Y**): they say immediately which contact systems cannot be optimal.
* The correction in §3.1 that the support object must pair the loaded graph with the
  **active** wall incidence, and the correction in Lemma 8 that interior loaded degree 2 is
  admissible (proposal V's "degree $\ge3$" is false for stationary points).

**Not attempted:** kill-criterion 3 (the exclusion gate). It is moot once gate 2 fires, and
§6.2 predicts its outcome anyway.
