# 2026-08-29 — inscribed equilateral triangle: the angular exact decider

Worker journal for the `experiments/inscribed-triangle-angular/` lane. A resumed lane: a
previous worker was killed mid-task by a rate limit and left `angular.py` (~719 lines),
`brute.py`, `q3.py`, an empty `out/`, and a dispatcher-written README marking everything
INCOMPLETE and claiming nothing.

## What I inherited, and what I did with it

I read all of it before running any of it, as instructed. The verdict, per file:

- **`q3.py` — kept.** Exact $\mathbb{Q}(\sqrt3)$, standard library only, its own
  representation and its own sign algorithm (isolate the radical, then compare $a^2$ with
  $3b^2$; the case $a^2=3b^2,\,b\ne0$ raises rather than returning 0, which is right —
  it would make $\sqrt3$ rational). Genuinely independent of the sibling's `k3.py`. I wrote
  tests for it and it passes; I found nothing wrong with it.
- **`angular.py` — rewritten, keeping the derivation.** The mathematics in its docstring is
  correct and I re-derived all of it independently before touching the code: the criterion
  (R), the cone/arc characterisation of which edges a ray meets, the scale formula
  $s_e(v)=k/\mathrm{cross}(v,b-a)$, and — the good idea in the file — the reduction of
  "equal radii" to the single **linear form** $\mathrm{cross}(v,M)=0$ with
  $M=k_e\rho^{-1}(d-c)-k_f(b-a)$. I checked the cross-multiplication is an equivalence
  (both denominators are nonzero on the closed cone: $b-a$ is never in the cone spanned by
  $a$ and $b$, since it has a negative coefficient in that basis), and that $s>0$ is
  automatic on the cone, which is what makes the degeneracy exclusion airtight.

  What I did **not** keep is its control flow. It enumerated ordered edge pairs and then
  tried to merge the resulting arcs with a hand-rolled absorb loop that has a branch doing
  literally `pass`; the merged output is what the structural questions depend on, so I
  replaced the whole thing with a **breakpoint sweep** — sort the finitely many directions
  where the combinatorics can change, decide each one directly, and handle each open gap by
  the linear form. That is provably complete (a gap can only be *entirely* good if $M=0$
  for some pair, since finitely many pairs otherwise give finitely many points), and it
  makes $G(O)$ a computed object rather than a merge artifact.

  I also changed the parametrisation from squared radius to **scale along the direction
  vector**. The inherited `_witness_for` reconstructed the witness point by extracting a
  square root in $K$ and returned `None` when the root did not exist. That was unnecessary:
  since $|\rho v|=|v|$, matching radii is matching scale, and the witness is
  $(O,\,O+sv,\,O+s\rho v)$ with $s\in K$ — always exactly representable. Every witness now
  comes out exact, and there is no `_sqrt_in_K` in the codebase.
- **`brute.py` — kept as a pre-screen only**, never as a decider, and said so in the README.

So: salvageable derivation, rewritten implementation.

## The flagged blind spot was real and is now the first test

The handover note said the *float* brute force missed collinear-ray directions. That
diagnosis was right and it is the natural failure mode for this algorithm: a direction in
which the ray runs **along** an edge is where the radial set stops being a finite set of
points and becomes an **interval**. It is not exotic — $O$ interior to an edge gives two such
directions, $O$ a vertex gives two more (both incident edges).

My `_edge_scales` handles it in one uniform branch, `cross(a,b)==0`: reduce both endpoints to
multiples of $v$, take the closed interval between them, intersect with $s>0$. The
half-openness at $0$ *is* the exclusion of the degenerate triangle $O,O,O$, so the whole
degeneracy question lives in one `if`. `TestCollinearRays` is the first test class and
asserts, among other things, that **no radial interval is ever closed at $s=0$** — a decider
that got that wrong would call every boundary point good.

Two controls exercise it end to end: the equilateral triangle inscribed in itself (both rays
collinear at every vertex) and the $120°$ apex of the $30$-$30$-$120$ triangle, good in
exactly three directions, two of them collinear. The apex witness comes out with
side$^2=1/3$ — the same triangle the previous worker had hand-checked. That is the one
mathematical statement I inherited that I can confirm rather than re-derive.

## Cross-validation, and an honest note on what it covers

190/190 sibling fixtures agree; 2 270 boundary points; 0 disagreements; 0 rejected witnesses;
`simple`/`convex`/`orientation` agree too. **No disagreement means nothing to adjudicate** —
the weaker of the two outcomes I was hoping for.

The thing I want on the record, because it is easy to oversell the agreement: the sibling's
battery is **182 convex fixtures to 8 non-convex**. So it is a strong check on convex answers
and a weak one on exactly the non-convex regime the rest of my task is about. I therefore
wrote a second decider inside this lane (`rotcheck.py`, the rotation algorithm by plane
segment intersection) and made the exceptional-set census take every decision twice. That is
deliberately *not* an independent idea — it is the sibling's idea reimplemented — and it
should be read as coverage, not as a second opinion.

## An exact fact that fell out, and is worth someone checking

For a polygon with **rational** vertices and a rational boundary point $O$: $k_e$, $k_f$ and
$b-a$ are rational, and $\rho^{-1}(w)=(w_x/2+\tfrac{\sqrt3}{2}w_y,\,-\tfrac{\sqrt3}{2}w_x+w_y/2)$,
so the $\sqrt3$-parts of $M$ are $k_e w_y/2$ and $-k_e w_x/2$. Both vanish only if $k_e=0$
(excluded, the edge is transversal) or $w=d-c=0$ (excluded, no zero-length edge). **So $M$ is
never $0$ over a rational polygon**, and $G(O)$ is a *finite* set of isolated directions —
an arc component is impossible without coordinates in $\mathbb{Q}(\sqrt3)$ proper.

This is a `sketch` — my own argument, elementary but unreviewed, and per `RULES.md` §3 I may
not build on it, including myself. It is stated in the README as an argument with the
computation reported separately as the check, not as the reason for the computation. The
computation is the honest part: `run.py structure`.

## Budget and process notes

- Validated on the three hand-known controls *before* any batch run, per `RULES.md` §6.
- Every stage checkpoints to `out/` and every long run was launched with a `timeout` and
  killed by me, not left orphaned.
- I ran no git command; the dispatcher commits.
- Status of everything in the directory is `numerical` and the README says so in its first
  line. Exact arithmetic makes each fixture's answer certain; it makes no general claim true.
