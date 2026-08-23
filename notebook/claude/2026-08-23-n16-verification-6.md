# 2026-08-23 — n16 verification round 6 (worker V6, issue #97)

Branch `claude/circle-packing-subagents-9yg5gt`. Role: convergent verification / adversarial
audit. Deliverable `attacks/n16-verification-6/README.md`; code in
`experiments/packing-n16-verify-6/`. No `git` run, no files touched outside my three paths.

## What I set out to avoid

Two failure modes, both documented in `FINDINGS.md`. (a) Reading the manager's argument, finding
it agreeable, and writing "confirmed" — `RULES.md` §5 says that is how two Claudes talk each other
into the same error. (b) Inventing a refutation to look useful — the campaign already has one
over-stated refutation. So the rule I held myself to: every "confirmed" had to come from a
reconstruction I could have done without the file in front of me, and every "refuted" had to come
with a runnable demonstration, not an argument.

## Item 1 — the manager's fracverify

I wrote `v6check.py` with a deliberately different algorithm for check (D). fracverify carries
(region, accumulated weight) pairs and splits them; I build the arrangement of all piece-edge
lines plus T_N's three lines, and evaluate total incident weight just inside each sector at each
arrangement vertex using a symbolic infinitesimal. Both agree: all three controls valid, same
bounds. My version also reports that the minimum incident weight is *exactly* K in all three —
the coverings are pointwise tight, which is why the 1/65536 weight perturbations (A20/A21) are
caught.

The brief asked me to break the region-splitting argument. I could not, and I think I now know
why it is not breakable rather than merely unbroken. Two facts:

1. `W(x) = Σ w_i 1_{S_i}(x)` is a non-negative combination of indicators of **closed** sets, hence
   upper semi-continuous, hence `{W < K}` is **open**, hence any covering failure has positive
   area. The "lost sliver" failure mode the brief warned about cannot exist as long as pieces are
   closed. This is the fact I most want someone to check independently — the whole soundness of
   (D) rests on it and it is one line.
2. `clip()` discards only zero-area sets, and each discarded set lies in the boundary line of the
   halfplane, which is in *both* closed halfplanes, so it survives in a retained region.

Together the early drop and the descending-weight order are safe. I recorded both derivations in
the README rather than just the verdict, so the next reviewer can attack the reasoning and not
just the conclusion.

Then 21 corruptions, 16 new. fracverify rejected everything that threatens a bound. It did fail
three things that are not bound-threatening: it mis-decodes `box` pieces whose `u+v` bounds are
zero or negative (C1 — a sign that flips and a constraint that vanishes, demonstrated on a grid),
it accepts decimal strings and bare floats in exact fields against problem `RULES.md` §2 (C2), and
it `KeyError`s instead of rejecting on a weight naming a missing piece (C3). C1 is the one that
matters: it is a §3.4 checker disagreement, and `gen_family` can produce negative `L3`, so a
future certificate will hit it.

One residual hole I could not close: fracverify never tests convexity, and `sqdiam` takes a max
over *vertices* while `split` uses the *intersection of edge halfplanes*. If those could disagree
— if the halfplane intersection could escape the vertex hull — the diameter would be
under-measured, which is a genuine false-accept. I probed 171,299 random integer polygons and
found zero escapes, but that is evidence, not a proof, and I have said so.

## Item 2 — the manager's "family is inadequate" verdict

I set out expecting to confirm it, then found the argument skips a step, then found the
conclusion probably survives anyway for a *different* reason than the one the manager gave. That
sequence is worth recording because both of the intermediate positions were wrong.

The parts that are right: the bound is genuinely scale-free (it is (side)/(max diameter)); the
arithmetic 281/63 < 1+2√3 is exact (109² = 11881 < 3·63² = 11907); the LP's constraint signs are
correct, and `q_max` is what the bound formula assumes — so both of the manager's own listed
alternatives are ruled out.

The part that is missing: the LP is **not** the continuum relaxation restricted to a piece family.
`membership_matrix` credits a piece on a row only if the piece contains the *entire* row, so the
LP is the continuum LP over the pieces' **erosions**; and `sweep16` uses `r_bulk = 3`, so most
rows are size-3 triangles, i.e. erosion by 3 units. With one unit of erosion the reachable N is
62·(1+2√3) = 276.8, so at N = 281 the method is already past its own granularity reach and no
conclusion about the family follows from the comparison as the manager set it up. F2's README
does flag the erosion cost and estimates it at 1–2 units of N, but that estimate comes from
controls whose optimal covers are lattice-aligned (a₆ = 2 and a₁₀ = 3 cost zero units); the
1+2√3 cover is not lattice-aligned in a 1/64 grid.

The trap I nearly fell into: reading the N=281→282 slope (0.080 per unit) as saying "you'd need
N ≈ 248 to reach 15", which would have made the family look catastrophically bad. The controls
kill that extrapolation outright — the LP value drops by 1.0 (n=4, n=10) and by **2.0** (n=6)
across a single unit of N at the threshold. A locally-flat, globally-step-like function is exactly
the shape that produced the coincidental "plateau explanation" already in `FINDINGS.md`, and I
would have reproduced that error if I had not looked at the control rows.

So: `confirmed-with-correction`. The lane's negative stands, but it is a negative about *this
implementation at this resolution* (`step_bulk = 4`, `step_edge = 6`, `r_bulk = 3`), not about
the fractional relaxation. The KILL-CRITERION's "no re-scoping to 'but a richer family would…'"
clause was written to stop motivated re-scoping; it should not be read as having *established*
that a richer family would not help.

## Item 3 — Theorem N §3.1

Re-derived all of it on paper: Lemmas 1–4, c ≥ 3, b ≥ 3(⌊a−4/√3⌋+1), d ≥ 3 at δ ≥ 1, class
disjointness, and the exactly-3/9/3 corollary including the "5 pieces per side" count. Everything
checks. The two places where an error would have been invisible are both handled correctly: the
b-bound uses floor-plus-one rather than ceiling (right, because each trace interval is *strictly*
shorter than 1), and M_e deletes *open* end intervals while Lemma 3 gives a *strict* bound, so the
two fit together with no gap.

`confirmed` — but V4 confirmed it too, and V4 is Claude and so am I. Two correlated draws. I said
so explicitly in the deliverable and flagged that B2's published-number claim inherits the cap.

## Item 4

Nothing had landed from the four live workers by the end of my window — kill-criteria and
in-progress code only. Said so rather than implying coverage I do not have.

## What I could not do

Grant `verified:review`. Everyone in this campaign is Claude; `RULES.md` §5 needs a different
model family. I have written that at the top of the deliverable so it cannot be quietly assumed.

## Budget

~40 min wall clock, 1 core, no background jobs left running.
