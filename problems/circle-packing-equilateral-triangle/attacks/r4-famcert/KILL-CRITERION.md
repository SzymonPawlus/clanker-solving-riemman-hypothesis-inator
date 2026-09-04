# Kill-criterion — r4-famcert (four-grain staircase family)

## As stated in the assignment

Two triggers:

1. **Reproduction failure.** If the generator cannot reproduce the known members
   (`n = 17, 24, 31` and the proven `n = 4, 7, 12`), STOP and report that the claimed
   geometric mechanism is wrong — that would refute the mechanism even if the numeric law
   held.
2. **Infeasibility past 31.** If `n = 40` or `n = 49` turns out infeasible in exact arithmetic
   after an honest attempt to resolve the seam-depth freedom, that is a first-class finding:
   the value law would not continue past 31 and the "family" would be a coincidence over six
   terms. Report loudly; do not force a fit.

## Verdict: **did not fire** (neither trigger)

**Trigger 1 did not fire.** Gate 1 reproduced all six known members as feasible and tight, with
the three `cited` proven optima (`n = 4, 7, 12`) matching their published values exactly and
`n = 24` matching the committed `r3-qsqrt3` certificate point-for-point.

One caveat kept on the record rather than buried: at `n = 17` and `n = 31` the generator emits a
*different* valid packing at the same `s` (shared 12/17 and 30/31 points). Both are feasible and
tight, so trigger 1 is not met — but the `n = 17` gap is wider than the single known rattler
explains, and that is unexplained. It is flagged as the first thing to review in README §1.

**Trigger 2 did not fire.** `n = 40` (780 pairs) and `n = 49` (1176 pairs) both verify feasible
and tight in exact `Q(√3)` arithmetic.

Note that the authoring worker's *first* `n = 49` transcription was infeasible, due to a
seam-depth degree of freedom, and had to be corrected. So trigger 2 came close to firing for a
transcription reason rather than a mathematical one. This is why each member is verified and
never extrapolated, and why `n = 60` is **not** claimed.

## Scope of the non-firing

Not firing means the construction exists and checks out at these `n`. It does **not** mean:

- that the law continues (`n = 60` uncertified);
- that these values are optimal (nothing here touches lower bounds);
- that they are records (Amore 2022 covers the triangle to `N = 400` and is behind the egress
  block);
- that they are assumable (`numerical`, same model family, no independent cross-family checker).
