# 2026-08-22 — worker V5: independent verification of the n = 16 upper-bound certificate

Issue #97, branch `claude/circle-packing-subagents-9yg5gt`. Role: verification (`RULES.md` §8
convergent). Model Opus 5; the certificate's author (worker U2) is Fable 5 — decorrelated inside
the agent, but the same model *family*, which caps what I can grant.

Deliverable: `problems/circle-packing-equilateral-triangle/attacks/n16-verification-5/README.md`.
Code: `experiments/packing-n16-verify-5/`.

## What I did

Wrote a checker from the problem `README.md` and `RULES.md` §2 before opening any sibling lane's
code. Exact `Fraction` plus a $\mathbb{Q}(\sqrt3)$ ordered field with an exact `sign()` routine
(same-sign parts immediate; opposite signs by comparing $a^2$ with $3b^2$, which cannot tie
because $\sqrt3$ is irrational). No float decides anything.

Derived myself, and only then compared with U2's write-up:

- containment at the fixed placement: $y \ge 0$, $\sqrt3 x - y \ge 0$, $\sqrt3(d-x) - y \ge 0$,
  each edge oriented by the opposite vertex;
- minimal enclosing side: only the $BC$ constraint involves $d$, so
  $d_{\min} = \max_i (x_i + \tfrac{y_i}{3}\sqrt3)$. I landed on the exact same closed form U2
  prints, attained at the same point (index 0).

## Result

Confirmed, no corrections. Every load-bearing number reproduced exactly: min $\mathrm{dist}^2
= 4 + 7.205320\times10^{-13}$; $d - d_{\min} = 3.0831\times10^{-14}$ (**not tight**, honest upper
bound); 20 pair contacts; 13 wall incidences over 10 distinct points; 3 corner points; exact
rigidity rank 30 over $\mathbb{Q}(\sqrt3)$; 3 self-stresses; rattler with 0 contacts.

Status: **construction only**. Cannot be `verified:review` — that needs Codex.

## Three things worth remembering

**1. The squaring step is sound in the direction that matters, and the guard everyone would drop
is the wrong one.** $\sqrt3 x \ge y \iff x \ge 0 \wedge 3x^2 \ge y^2$ needs $y \ge 0$ only for the
*completeness* direction. Dropping $y \ge 0$ makes a checker over-strict; dropping `x >= 0` makes
it **unsound** — it then accepts mirrored points at $x<0$. U2 flagged the right line of code for
review but named $y \ge 0$ as the risk; the actual live wire is the `x >= 0` guard. I built the
mutant and exhibited a point it accepts and the exact test rejects. Worth carrying to any future
containment encoding in this repo.

**2. The checker-disagreement resolved into a units mismatch, not an error of fact.**
n16-dual's "10 wall contacts" counts *points touching a wall*; U2's "13" counts *(point, edge)
incidences*. Both are correct counts of different things; only the second is a count of
constraints, because the three corner points each sit on two edges. I built the
"corner-counted-once" $30\times30$ matrix explicitly and it does have rank 30 — so the isostatic
reading is internally consistent, which is exactly why it was believable. The error is upstream of
the linear algebra, in what got counted. This is the same shape as the Approach C recount and the
manager arithmetic incident in `FINDINGS.md`: a discrepancy with an available explanation stops
being a question too early. Building the *other* side's matrix and watching it come out at rank 30
is what turned "who is right" into "what is each counting".

**3. The repo's stored float packing for $n=16$ is not the certificate's configuration.**
11 of 16 points coincide to $<10^{-5}$; four form a rearranged sub-block (the two bottom-edge gaps
$0.35132 \leftrightarrow 0.21623$ swap, three interior points move by $0.091$); the rattler differs
by $9.4\times10^{-3}$ inside the same cage. Both report the same minimum distance to 16 digits.
So the two lanes' contact counts were counts of different point sets — a second, independent
reason they need not have agreed. I am deliberately *not* calling this non-uniqueness of the
optimum: floats cannot distinguish "equal" from "equal to $10^{-16}$".

## Where I was weakest

The literature check. `WebFetch` is blocked, and the search backend cheerfully affirmed
$d(16) = 0.216227269309782$ — the exact digit string I had put in my own query. That is not
confirmation, it is an echo, and it is precisely the mechanism by which a guess becomes a
`cited` claim. Recorded as **not obtained**. The one real triangulation was accidental: the
backend volunteered $d(17) = (3-\sqrt3)/6$ unprompted, and it matches the repo's transcription of
GL's table to all 15 printed digits, which corroborates the transcription (not the source).

## Budget

~35 min wall, one core, no long runs, nothing left running.
