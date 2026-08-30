# 2026-08-30 — the exact inscribed-triangle maximiser (resumed lane)

Worker journal, agent `claude` (Claude Opus 5), branch
`claude/inscribe-equilateral-triangle-oj15x1`. Lane files:
`experiments/inscribed-triangle-maximiser/**` and this file. Nothing else was touched; no git
command was run by me.

## What I was handed

A directory of ~1 170 lines written by a worker killed mid-task, swept into an unrelated
commit, never run, no tests, no output, and a dispatcher-written README correctly claiming
nothing. The instruction was to treat it as unvalidated and either validate or rewrite.

## What I did, in order

1. **Read `qs3.py` and `maximiser.py` before running them.** The candidate-set argument in the
   `maximiser.py` docstring is the load-bearing part: the maximiser is exact only if the finite
   candidate direction set provably contains a maximiser. I re-derived it — for an ordered pair
   of transversal edges the matching condition collapses to the linear form
   `cross(v, M_ef) = 0`, so either two isolated directions, or (when `M_ef = 0`) a whole arc on
   which side² is `k_e²/(|b−a|² sin² t)`, maximal where `|sin|` is minimal, which on an arc
   inside an open half turn is an endpoint — and arc endpoints are vertex directions. That is
   correct as written. So the algebra survived; I kept it.
2. **Ran the three external validations before anything else.** Equilateral → 1. Unit square →
   side² = 8 − 4√3 exactly, i.e. sec 15°. 30-30-120 → 4/9 at the 120° apex, both 30° apexes
   exceptional. The square is the one that matters: it is a classical number from outside this
   project, and it is a *maximum*, not a witness.
3. **Wrote a second maximiser from a different parametrisation** (`pairmax.py`): walk ordered
   edge pairs, parametrise by the position `t` of one vertex along an edge, and use that
   side²(t) = |P(t) − O|² is a *convex* quadratic, so the max over the (closed, interval)
   feasible set is at an endpoint. This has a much shorter optimality argument than the
   direction-space one and shares nothing with it but the field arithmetic. Both agree on all
   2 270 fixture boundary points, exactly.
4. **Cross-checked against both committed deciders** on all 190 committed fixtures: 2 270
   points, 0 boolean disagreements, 0 witnesses rejected by either lane's verifier, 0
   disagreements with the recorded `good` flags. I was told six checkers had failed this
   session against zero real errors, so I expected my own bug rather than a discovery. I found
   neither: nothing to adjudicate, which is the weaker outcome.
5. **Global max over O**: exact per O; globally exact only *given* Lemma V (a `sketch` of the
   previous worker's, that a maximiser has a vertex at a polygon vertex). I did not upgrade it
   and I did not blur the distinction — 8 613 sampled edge points, all solved exactly, zero
   beat their polygon's vertex maximum, 4 fixtures tie. Evidence, not proof.
6. **The constant-width body.** This is the part that mattered outside the lane.

## The one real defect in the inherited code

`lp.py`'s LP derivation was right. Its `lambda_upper_at` ranked candidate constraints by
`(c_j − ⟨t,n_j⟩)/m_j`, skipping every constraint with `m_j = 0`. Those are ordinary walls of
the polytope in `t` and can sit in the optimal basis — and on the very direction that attains
the maximum, they do. The function found no valid dual triple at all and returned `None`, i.e.
the module could not have produced a single number. Ranking by the residual
`c_j − (⟨t,n_j⟩ + λ m_j)` over *all* constraints fixes it; the bound then lands within 1.2e-6
of the float optimum. Same shape as the defect the sibling lane hit yesterday: correct algebra,
control flow that could not reach the answer. `dual_bound` also had a dead
`... if False else None, None, None` assignment, removed.

## The constant-width result

`extremal-size` §7 claims the disk is not extremal for m/w, via `h = 1 + cos(5θ)/24`, and says
its m is a float. The claim needs *only an upper bound* on m, because w = 2 is exact and
because every inscribed triangle is in particular a contained one, so m(K) ≤ M(K) and no lemma
about maximal triangles touching the boundary is needed. Chain: outer polygon of 192 rational
half planes from the support function (upper bounds only, so containment is free) → an a priori
side bound from an antipodal slab → 3 600 rational directions with a certified angular gap →
rotate any triangle onto the nearest sampled direction, which puts it in the outer parallel
body at r ≈ 1.21e-3 → exact weak-duality certificate at each direction. Result:

    m(K)² ≤ 368394053/125000000 = 2.947152424 < 3,   so m/w ≤ 0.85836363 < √3/2 = 0.86602540.

So the claim is **confirmed and upgraded from float to exact**, not refuted. I would have
preferred the refutation; it is the more valuable outcome and it is not what the arithmetic
said.

I validated the LP chain against three bodies whose answer is known before believing it on the
one whose answer is not: the disk (√3), the unit square (sec 15°), a near-equilateral triangle
(≈1). In each the bound sits just above the truth, never below. The disk row is the sharpest
available check, since the disk is the body the whole question is normalised against.

## What I am least sure of

- **Lemma V**, and I left it `sketch`. Its Case 2 is argued more loosely than Case 1.
- The **rotation-onto-a-sampled-direction** step in `cw.py`: it is the only step that turns
  3 600 directions into all directions. It is elementary (2R sin(δ/2) ≤ Rδ, R = s/√3) and
  written out in full in the module docstring so a reviewer can attack it, but if it is wrong
  the §6 bound is a statement about 3 600 directions and nothing more.
- I produced **no lower bound on m(K)** for the constant-width body. Bracketing m/w from both
  sides exactly, as the brief asked, would need an IVT argument on R_K(θ+60°) − R_K(θ) with
  exact enclosures from inner and outer polygons; I ran out of budget before attempting it, and
  I would rather say that than dress the upper bound up as a bracket.
