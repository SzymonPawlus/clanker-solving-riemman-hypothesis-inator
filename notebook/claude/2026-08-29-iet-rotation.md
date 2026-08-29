# 2026-08-29 — the 60° rotation route for the triangle peg problem (issue #132)

Worker lane: exactly three files —
`problems/inscribed-equilateral-triangle/attacks/rotation-continuity/README.md`,
`.../KILL-CRITERION.md`, and this entry. The problem `README.md` and `RULES.md`, the convex lane
`attacks/convex-vertex-criterion/`, and `experiments/inscribed-triangle-polygons/` belong to
concurrent workers; I touched none of them. No git run here — the dispatcher commits.

Order of work: read repo `RULES.md`, then problem `RULES.md` and `README.md` (both had appeared on
the branch by the time I looked — my first `ls` of `problems/` did not show the directory at all,
the second did, so the dispatcher committed between them).

---

## 1. The elementary observation — held up, and is an iff

Checked it before building on it, as instructed. It is three lines and it is right: for
$q \in J \cap \rho_{O,60°}(J)$ with $q \ne O$, the points $O, \rho^{-1}(q), q$ have two equal sides
and a $60°$ angle between them, and isosceles-with-apex-$60°$ forces equilateral. Nondegenerate
because $q \ne O$.

Two things I did not expect and that turned out to matter:

- **It is an equivalence, not an implication.** Given any inscribed equilateral triangle $O,A,B$,
  either $B = \rho_{+60}(A)$ or $A = \rho_{+60}(B)$. So testing the **single** orientation $+60°$
  is complete. Problem `RULES.md` §3.2 states only the $\Leftarrow$ half, which is all it needs;
  but the $\Rightarrow$ half is what upgrades my §3 computation from "the trick failed here" to
  "$O$ is genuinely an exceptional point". Without it the $30°$-apex result would be a statement
  about a method, not about the curve.
- **No limit is taken anywhere.** The degenerate solution $O$ is present from the start and is
  excluded by hand rather than by an estimate. That is why noncollapse is free in this route, and
  it is the cleanest illustration I have seen of why the triangle case is not the square case.

Symbolic check: for $p$ at polar $(r,\theta)$ and $q = \rho_{60}(p)$, sympy returns
$|Op| = |Oq| = |pq| = r$. Good.

## 2. The counterexample — clean, exact, and better than I expected

The brief suggested the $30$–$30$–$120$ triangle and it works. Vertices
$O = (0,0)$, $A = (1,0)$, $C = (\tfrac12, \tfrac{\sqrt3}{6})$; exact angles $30°, 30°, 120°$;
$|OA| = 1$, $|OC| = |AC| = \sqrt3/3$. Exact segment-intersection in $\mathbb{Q}(\sqrt3)$ over all
nine segment pairs gives

```
T ∩ rho_{O,+60}(T) = {(0,0)}      T ∩ rho_{O,-60}(T) = {(0,0)}
T ∩ rho_{A,±60}(T) = {(1,0)}
T ∩ rho_{C,+60}(T) = {(1/2,0), (1/2,√3/6), (2/3,0), (3/4,√3/12)}
```

The rotated triangle at $O$ has vertices $(0,0), (\tfrac12,\tfrac{\sqrt3}{2}), (0,\tfrac{\sqrt3}{3})$
— the last one is exactly $\tfrac{1}{\sqrt3}$ straight up, since $|OC| = 1/\sqrt3$ and $C$ is at
$30°$, so $\rho_{60}(C)$ is at $90°$. Pleasant enough to be worth writing down.

**The reason, which is better than the computation.** $T$ is convex, so $T$ lies in the closed cone
at $O$ spanned by directions $[0°, 30°]$, and $\rho_{60}(T)$ lies in the cone $[60°, 90°]$. Two
closed cones with disjoint direction arcs meet only at the apex. That is global for free — no
"pulled off near $O$" local argument needed, which is what the brief suggested and which would have
been more work and weaker. Convexity is the load-bearing hypothesis; for a reflex polygon a $<60°$
vertex may still be a triangle vertex.

This is a rediscovery of the wedge test already in problem `RULES.md` §3.1. I found it
independently and only noticed the overlap when I read that file. What my version adds is the exact
intersection sets (so the rotation route and the wedge test are checked to agree, not merely to be
compatible) and the confirmation that $T$ *does* inscribe equilateral triangles elsewhere: at the
$120°$ vertex the output includes $(\tfrac12,\tfrac{\sqrt3}{6}), (\tfrac13,0), (\tfrac23,0)$ with
all three sides exactly $1/3$.

Also noted: a triangle has at most two angles below $60°$, since three would sum to under $180°$.
So this witness is automatically extremal for the "at most two exceptional points" bound. For a
convex curve generally, interior angle $< 60°$ means exterior angle $> 120°$, and exterior angles
total $360°$, so at most two. That the local criterion reproduces the literature's *sharp* constant
is the strongest consistency signal I got all session.

## 3. The three framings

**Area/measure.** I got a real lemma out of it and then watched it fail, exactly as the brief
warned. If $J \cap \rho(J) = \{O\}$ then $J' \setminus \{O\}$ is connected and disjoint from $J$,
so it sits inside $\Omega$ or inside $E$. The $\Omega$ case dies: $\overline{\Omega'} \subseteq
\overline\Omega$ with equal Lebesgue measure (isometry), the difference is null, $\Omega \cap E'$ is
open and null hence empty, so $\overline\Omega = \overline{\Omega'}$, so $E = E'$, so
$J = \partial E = \partial E' = J'$ — contradiction. Nesting is impossible, with **no regularity at
all**. The $E$ case is external tangency and is exactly the $30°$-wedge witness, so there is nothing
to extract. Net: the measure argument is a *reduction* (curve intersection $\to$ region overlap),
not a proof. I very nearly wrote "so they cannot be nested, hence they overlap, hence they cross";
that sentence is false and the witness is the reason.

**Tangent cone.** This is the right framing, with one substitution that is easy to get wrong: the
condition must be on the tangent cone of the **filled region** $\overline\Omega$, not of the
**curve** $J$. An outward cusp (region $\{0\le x\le 1, |y|\le x^2\}$) has a perfectly tame
one-dimensional curve-tangent-cone at the tip and zero region-aperture, and the route fails there.
Any version phrased in terms of limit directions along $J$ is either false or silently assuming a
local graph. With the right substitution: a closed sector of aperture $\ge 60°$ inside
$\overline\Omega$ at $O$ suffices, with the $60°$ threshold sharp on both sides.

**Winding number / degree.** Nothing. Under $J \cap J' = \{O\}$ the domains are disjoint by the
lemma above, so $w_J + w_{J'} \in \{0,1\}$ and there is no parity to exploit. A degree argument that
did produce a contradiction here would be proving something false, since the witness realises the
configuration. Recorded as a dead end rather than as an untried idea.

## 4. The mistake — and it is the useful part of the session

My first draft of the write-up had:

> $\mathcal{H}^1$-a.e. point of a **rectifiable** Jordan curve is a vertex, because arclength
> parametrisation is differentiable a.e. and a differentiability point gives a local graph.

I wrote it fluently, it felt airtight, and I had already put it in the claim table before I went
back to re-derive the separation step rather than re-read it. It does not work. What is true at a
differentiability point $t_0$ (with $\gamma$ $1$-Lipschitz, $\gamma'(t_0) = u$):

- $J \cap B(O,\varepsilon)$ lies in a thin double cone $D$ about $O + \mathbb{R}u$ — **fine**;
- the forward and backward arcs leave $B(O,\varepsilon)$ on opposite sides, so there **is** a
  crosscut through $O$ separating the two fat sectors $S_\pm$ — **fine**;
- therefore $J \cap B(O,\varepsilon)$ is that crosscut and nothing else — **not fine**. The
  estimates only sandwich $|\gamma(s) - O|$ between $(1-\eta')|s-t_0|$ and $|s-t_0|$. That permits
  $|\gamma(s)-O|$ to be non-monotone with $o(1)$ relative oscillation, i.e. the curve can leave and
  re-enter every small ball, at every scale, while still being differentiable at $t_0$. So
  $B(O,\varepsilon)\setminus J$ can have a third component trapped inside $D$ — and $\Omega$ could
  be it, in which case both $S_\pm \subseteq E$ and there is no fat sector.

I could not construct such a curve and I could not exclude it, so the rectifiable case is **not
established** and is recorded as such. Differentiability of the *parametrisation at a point* does
not make the *image* a graph near that point; that is the smuggled-regularity failure the problem
`RULES.md` §0 predicts, and I committed it in writing before catching it.

What survives is Theorem C under an explicit crosscut hypothesis, which I can discharge for $C^1$
(every point) and for polygons (every point of interior angle $\ge 60°$). That is a much smaller
theorem than the one I first wrote, and it is the one I can defend.

## 5. Varying $O$

The honest picture is that the lane is misnamed: "rotation-continuity" suggests the difficulty is a
continuity/degree statement in $O$, and it is not — or at least, that is not the *first* difficulty.

- Continuity in $O$ fails in the expected way: $O_n \to O$ with witnesses $q_n$ gives
  $q_n \to q \in J \cap \rho_O(J)$ but possibly $q = O$. Upper semicontinuity is the wrong
  direction; intersections vanish in limits, they do not appear.
- Polygonal approximation fails on obligation 3 of problem `RULES.md` §4: the side produced is a
  quarter of the sector radius, and nothing bounds that below along a roughening sequence.
- **But §4 above shows the trouble starts earlier**: I cannot certify a fat sector even at a fixed,
  apparently well-behaved point of a rectifiable curve. So the ordered obstacle list is (a) a local
  geometric question with no rotation in it — must $\overline\Omega$ have a sector of positive
  aperture somewhere? — and only then (b) uniform noncollapse. (a) is strictly easier and I do not
  know its answer; that is the issue I would open next.

Two instincts I had and rejected, recorded so they are not re-derived: "the exceptional set has at
most two points so pick any other $O$" (circular — that *is* the theorem), and "the tangent cone
must be fat somewhere by compactness" (not a statement I can even formulate correctly, and the
outward cusp shows it is not local-trivial).

## 6. Square contrast

Ran it, per problem `RULES.md` §3.2. Everything I proved goes through verbatim for an arbitrary
angle $\alpha \in (0°,180°)$ with "$\ge 60°$" replaced by "$\ge \alpha$": a sector of aperture
$\ge \alpha$ at $O$ yields $p,q \in J$ with $|Op| = |Oq| > 0$ and $\angle pOq = \alpha$. At
$\alpha = 60°$ that is the equilateral theorem **only because** isosceles-with-apex-$60°$ closes
the figure. At $\alpha = 90°$ it returns a right-isosceles corner and leaves the fourth vertex
$p + q - O$ entirely unconstrained. So the machine does not transfer, and the *reason* it does not
is a one-line fact about triangles, not a subtlety. Dimension heuristic agrees: equilateral
triangles are a $4$-parameter family against $3$ conditions (expect a $1$-dimensional solution set,
robust); squares are $4$ against $4$ (expect isolated solutions, so only a degree count can force
one, and that is what degenerates for rough curves).

## 7. Literature

Not my lane — the literature worker's file is thorough and I added nothing to it. One lane-specific
finding: search summaries describe Meyerson's proof as rotating by $60°$ about points of a **triod**
and running in three stages (polygonal triods, end-straight triods, general by approximation and
limits). If accurate: the observation in §1 is the classical mechanism, my §5-equivalent is the
polygonal stage, and the stage I cannot do is the one that takes the rest of the paper. Every
scholarly host was blocked by the egress proxy (`arxiv.org`, `math.brown.edu`, `math.elte.hu`,
`matwbn.icm.edu.pl`, `doi.org`, `zbmath.org`, `ams.org`, …), so I read no source text; this is a
flagged search target at provenance P3, not a citation, and I kept it out of the known-results
table.

## 8. Housekeeping

- All computation exact in $\mathbb{Q}(\sqrt3)$ (problem `RULES.md` §5). No floats anywhere.
- The script is inline in the attack README rather than in `experiments/`, because this lane owns no
  `experiments/` directory. It has not been cross-checked against the shared polygon enumerator;
  that is flagged in the README as the next verification step.
- Three filters run and reported: wedge test (§2 — my own witness *is* the filter's witness), square
  contrast (§6), polygon control (only partially — my own exact computation, not the shared
  enumerator).
- Nothing in the attack rests on a `cited` row of the problem README; Meyerson appears only as an
  external cross-check on my conclusions.
- Tier: `tier:non-claim` — everything is `sketch`, `refuted`, or exact `numerical` outside
  `results/`, and no assumable claim is created, altered, or relied on. The P3 literature note is
  explicitly *not* a citation, which is what keeps it out of the verification-critical tier; if a
  reviewer disagrees with that reading, the tier should be raised rather than argued about.

---

**Weakest step.** Lemma A, Case B — the bookkeeping that turns "$J' \setminus \{O\}$ lies in $E$"
into "$\Omega' \subseteq E$" runs through four connectedness-and-complement steps
($J \setminus \{O\} \subseteq E'$, then $\Omega' \cap J = \emptyset$, then $\Omega' \subseteq \Omega$
or $E$, then eliminating the first), and each is individually easy, which is exactly the condition
under which I stop checking. Everything downstream — Lemma B, Theorem C, the whole square contrast —
hangs off it. If a reviewer redoes one thing, redo that, from the statement and not from my proof.
