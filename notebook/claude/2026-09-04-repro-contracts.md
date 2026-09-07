# 2026-09-04 — reproduction contracts for four packing experiment lanes

Issue #272. `tier:non-claim`: packaging and reproduction contracts only. No mathematical claim,
no status promotion, no numerical result changed.

## What I was asked to do

An audit of `origin/main` (HEAD `12fa645`) reported three directories whose advertised
reproduction command dies on a bare interpreter with a raw `ModuleNotFoundError`. Two earlier
review rounds each caught one instance of this class; these three were the remainder.

## Verifying before fixing

The instruction I took most seriously was *verify each finding yourself* — on this repo a
correction is as error-prone as the bug (`notebook` memory: "corrections overshoot").

That paid off immediately. My first attempt at a "bare" baseline used the host `python3`, and
`packing-r5-eo7` **passed**, exit 0 — apparently contradicting the audit. The host interpreter
turns out to have `mpmath` 1.3.0 and `sympy` 1.14.0 installed but not `numpy`. So the host is
*partially* bare, in exactly the way that hides an mpmath bug while exposing a numpy one.

Had I trusted that run I would have reported the audit as wrong on eo7. Had I trusted the audit
without running anything I would have been right by luck. Neither is a check.

The real baseline is `python3 -m venv --without-pip`, with `ENABLE_USER_SITE = False` (venvs
disable the user site directory, which is where this host's mpmath lives) and all four of
numpy/scipy/mpmath/sympy confirmed absent by `importlib.util.find_spec`. Against that, all three
findings reproduced exactly, at the reported line numbers.

**Lesson worth keeping: "it ran on my machine" is not a bare test, and a dev box is the worst
possible place to test an absence.** The mpmath case is invisible on any machine that has ever
installed sympy, since sympy depends on mpmath.

## Route taken, and why all three went the same way

The task offered two idioms already on `main`: make the import an *optional* diagnostic
(`try/except ImportError` + `SKIPPED (optional)`, as in `packing-r3-qsqrt3`), or *declare* it
(pinned `pyproject.toml` + fail-fast preflight exiting 2, as in `packing-r6-nontri`). I expected
to use one of each and was mildly suspicious when all three landed on "declare" — so I checked
each against the question "what would remain if this were skipped?"

- **r4-delaunay** — `scipy.optimize.linprog`. STEP 0 is exact and stdlib-only, but STEPS 1–4 (the
  Oler control, both LPs, the verdict) *are* the finding. Skipping the LP leaves self-checks and
  no result. Declare.
- **r5-theta2** — cvxpy SDP for θ′, scipy MILP for α, scipy LP over networkx cliques for χ̄_f,
  mpmath at 60 dps for the exact distance-2 ties. The self-test's job is to check the instrument
  against known values; an instrument that did not run has nothing to self-test. Declare.
- **r5-eo7** — `mpmath.iv` at `iv.dps = 30`. Every accept/reject in the branch-and-bound is an
  outward-rounded interval comparison, and that rounding *is* the soundness of the lane. Declare —
  and explicitly do **not** reimplement.

That last one is where the "reimplement it yourself" route had to be refused rather than merely
not-chosen. `packing-r6-stairthm` did swap out a dependency for a stdlib `Lin` class and survived
a direct soundness attack, but that was exact linear-form arithmetic over `Fraction`. Hand-rolled
*interval* arithmetic is a different animal: a single wrong rounding direction silently converts a
non-proof into an apparent proof, and nothing in the output looks different. This is the repo's
signature failure mode (RULES.md §0) with a rounding mode attached.

## Two things I found that the audit did not

**1. r4-delaunay was broken a second, independent way.** With numpy and scipy installed it *still*
exited 1 — `FileNotFoundError: 'out/report.txt'` — because `run.py` wrote a cwd-relative path
while the documented command runs from the repo root. Every LP had already been solved; the
crash was in the last four lines. A dependency preflight alone would have "fixed" this directory
into a still-failing state, and I would have reported a green fix that was not green.

I only caught it because the brief said to run the advertised command *as advertised* and paste
real exit codes. Running it from inside the directory — the natural thing — hides it.

The fix anchors the path to the script directory. The regenerated `out/report.txt` came back
**byte-identical** to the committed one, which is simultaneously the proof that I changed no
number and an independent reproduction of the whole LP result.

**2. The audit was wrong about `packing-r3-sdpgate`.** It was listed as publishing "no
single-command reproduction instruction at all". It ships `reproduce.sh` — a `set -euo pipefail`
runner that `cd`s to its own directory, four labelled stages, and even a pinned cvxpy fallback
(`pip install 'cvxpy==1.9.2'`). I nearly wrote it up as a shortfall on the strength of the
handoff. Findings inherited from another agent's audit are `sketch`, not `cited`, including the
negative ones — that cuts both ways and I should treat an inherited *accusation* with the same
suspicion as an inherited *claim*.

## Bonus: `packing-r6-secondline`

Asked to bare-test it, I found a fourth instance of the class. It *declares* numpy correctly in
`pyproject.toml` and documents the venv install in its README — and still produced a raw
traceback, because declaring a dependency does not stop a bare interpreter from crashing. The
pyproject is documentation; the preflight is enforcement. Added the preflight only; the route was
already correct.

`witness28.py` there runs green bare, and should: it is the exact-rational witness. Same shape as
`analyse_p1.py` in theta2, which regenerates the write-up's tables from committed JSON on the
stdlib alone. Both are worth protecting — **the exact and archival parts of a lane should not
inherit the float stack's dependencies**, and in both cases they already didn't.

## Outstanding

Reported on the PR, not silently dropped:

- `packing-r3-audit` (sympy), `packing-r3-stationarity` (networkx/numpy/sympy **plus an external
  `geng`/nauty binary via `subprocess`** — a distinct and harder §4 problem, and it has no README
  at all), `packing-r5-bnb24` (numpy, only in `arbb/geom.py`), `packing-r6-interaction`
  (numpy/scipy) still publish no single-command reproduction. I inspected their imports but did
  not bare-test them or write the commands; doing that inside the remaining budget would have
  meant guessing at entry points for directories I had not run.
- `packing-r3-sdpgate` needs nothing — see above.

I stopped adding fixes at roughly the hour rather than rushing five directories I had not
verified. A half-checked reproduction contract is worse than an absent one, because it looks
checked.
