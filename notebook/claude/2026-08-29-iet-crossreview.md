# Cross-examination of `attacks/convex-vertex-criterion/README.md` — Sonnet 5 pass

I was dispatched as a decorrelation check on `attacks/convex-vertex-criterion/` — separate model
(Sonnet 5, not Opus) from both the README's author and `AUDIT.md`'s auditor, both Opus 5. Wrote up
the full result in `attacks/convex-vertex-criterion/CROSS-REVIEW.md`; this entry is the shorter
narrative version for the journal.

**Verdict, in short: Theorems A, B(i), B(ii), C(a), C(b), Proposition D, and Corollary E all
survive independent reconstruction. No new mathematical error found.** I specifically hunted for a
second instance of the closure-vs-achieved-directions bug that killed the original (C2) — the
brief named this as the standard failure class here — and did not find one: Theorem A/C use the
tangent cone `T(O)` only as an upper bound (the safe direction for a closure), while Theorem B's
existence proof carefully derives membership in the achieved set `A` from positivity of `r(\theta)`
rather than from `T(O)` directly. That discipline is real and I traced it through every step.

I independently reconfirmed both of `AUDIT.md`'s substantive corrections rather than taking them on
trust:

- **E1 (continuity, not just semicontinuity, of `r`).** Re-derived the sandwiching-triangle
  argument myself, then checked it against `K^*` using a parametrization neither README nor AUDIT
  used (`r(\theta)=\min(\tan\theta,1)\sec\theta`), confirming `r(\theta)\to0=r(0)` continuously —
  the `K^*` mechanism really is `\Sigma(0)=\emptyset`, not a jump.
- **E2 (Proposition D's witness misattributed to "Case C").** Recomputed the `120°`-triangle's
  radial function from scratch (`r(\theta)=1/(\cos\theta+\sqrt3\sin\theta)`), found `r(0)=1\ge
  r(\pi/3)=1/2` so **Case A** fires, giving the real witness `(0,0),(1/2,0),(1/4,\sqrt3/4)` side
  `1/2` — not the README's stated side-`\sqrt3/3` triangle, which is a genuine *second* inscribed
  triangle at the same vertex (root of `F` at `\theta_0=\pi/2`, verified `r(\pi/2)=r(\pi/6)=1/\sqrt3`
  exactly) but is not what Case A or Case C actually construct there.

**Computational work, done fresh rather than rerun.** Wrote three independent exact-arithmetic
checkers (no floats, no sympy geometry predicates — the brief flagged those as unreliable and I
avoided them entirely):

1. 3000 random convex integer polygons, exact-fraction angle test — max 2 vertices with `\alpha<60°`
   and max 2 with `\alpha\le60°` across all trials, consistent with Theorem C's sharp bound.
2. ~950 boundary vertices across ~140 random convex polygons, exact `\mathbb Q(\sqrt3)` rotation-
   and-intersection test of the polygon corollary of Theorem B (`good \iff \alpha\ge60°`) — zero
   disagreements after a fix (below).
3. Hand exact-arithmetic reconstruction of `K^*` and of Proposition D's witness (§5, §7 of
   CROSS-REVIEW.md).

**Worth recording on its own: I hit the exact class of bug the brief warned about, in my own
code, on my first attempt.** My rotation-and-intersection checker's first version handled only
transversal crossings and silently dropped touching/collinear cases. It agreed with the theorem on
950/950 random polygon vertices — and then flatly said "not good" at all three vertices of the
equilateral triangle (the one hand-built case that actually probes the delicate `\alpha=60°`
boundary), because rotating an equilateral triangle `60°` about its own vertex maps one edge exactly
onto another, producing a shared-edge touching case my sign-only test discarded. Diagnosed and fixed
it (added exact endpoint-containment and collinear-overlap detection) before trusting the checker
again; after the fix, all three vertices correctly report "good" and the full sweep still agrees.
This is precisely the "treat a disagreement as your own bug until adjudicated" instruction from the
dispatch, and it happened for real rather than as a hypothetical caution.

**Not-checked, honestly:** the literature provenance (Meyerson 1980, out of this lane's scope), the
`\beta`-generalization remark in README §6 (both files already mark it unchecked and it's not one
of the core theorems), full first-principles proofs of three named textbook facts (supporting
hyperplane theorem, `[w,y)\subseteq\mathrm{int}\,K`, uncountability of `\partial K`) — sanity-checked
conceptually, not re-derived from convexity axioms, and I don't believe any of the three is where an
error would hide — and a fresh curved-body (non-polygon) numerical exercise of Theorem B's Case C
specifically, which I verified completely by hand but did not also re-code myself.

**On what this cross-examination can certify.** `RULES.md` §5/§8 reserve `verified:review` for a
different *model family* (Claude vs. Codex is the given example); Sonnet and Opus share the Claude
lineage, so whether this satisfies that bar is a policy call, not a technical one, and I said so
plainly in `CROSS-REVIEW.md` rather than presuming to grant the status myself. `README.md` and its
status line are not in my lane (`RULES.md` §2) regardless, so I did not touch them. What I can and
do certify is the technical content: every step I could restate, I restated and re-derived from the
definitions rather than reading and agreeing, and I found no load-bearing gap.

Files touched: `problems/inscribed-equilateral-triangle/attacks/convex-vertex-criterion/
CROSS-REVIEW.md` (new), this entry (new). Nothing else edited, per the dispatch's lane restriction.
Scratch scripts used for the computations lived in the session scratchpad, not committed (matching
the directory's own convention that ad hoc numerics are not checked in outside `experiments/`).
