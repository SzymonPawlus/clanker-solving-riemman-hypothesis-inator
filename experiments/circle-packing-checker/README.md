# Exact-arithmetic packing checker

**Status:** `numerical` — this is a tool, not a mathematical claim. It certifies
*constructions* (upper bounds `s(n) <= c`), never optimality.

Issue: [#2](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/2).

---

## The question

Given a claimed packing certificate in the format of
[`problems/circle-packing-equilateral-triangle/RULES.md`](../../problems/circle-packing-equilateral-triangle/RULES.md)
§2, is the packing *actually feasible*? Not "feasible to within a tolerance" —
feasible.

This matters because of the failure mode that problem's `RULES.md` §0 names: every
optimiser returns a configuration that overlaps by ~1e-9 and reports a side length
beating the world record, and that result is always wrong. A checker that uses
floating point cannot tell that case apart from a genuine packing, for a reason that
is not a bug and cannot be engineered away — see "What exact arithmetic buys" below.

## The method

By the reduction in
[`problems/circle-packing-equilateral-triangle/README.md`](../../problems/circle-packing-equilateral-triangle/README.md),
packing `n` unit circles into an equilateral triangle of side `s` is equivalent to
placing `n` points at pairwise distance `>= 2` in an equilateral triangle of side

```
d = s - 2*sqrt(3)
```

so the check is a finite conjunction of algebraic inequalities:

1. `|p_i - p_j|^2 >= 4` for all `C(n,2)` pairs,
2. each point in the closed triangle `A=(0,0)`, `B=(d,0)`, `C=(d/2, d*sqrt(3)/2)`,
   i.e. `y >= 0`, `sqrt(3)*x - y >= 0`, `sqrt(3)*(d - x) - y >= 0`,
3. the reported `side_length` is consistent with the coordinates.

**The problem's `README.md` is the definition of correctness, not this code.** Per
that problem's `RULES.md` §3 the other agent reimplements this independently; any
disagreement between the two is a finding to investigate.

### Representation: why not `Fraction`

Optimal packings here are algebraic, not rational. The triangular-lattice optimum has
row offsets of exactly `sqrt(3)`, so `s(6) = 4 + 2*sqrt(3)` and `s(10) = 6 + 2*sqrt(3)`;
other known optima bring in `sqrt(6)` and `sqrt(33)`. `fractions.Fraction` cannot hold
these, and rounding them defeats the entire exercise, because **the inequalities are
tight at the optimum**: distances are exactly 2, points sit exactly on the boundary. A
checker that cannot distinguish "touching" from "overlapping by 1e-40" is useless
precisely on the inputs we care about.

So the primary representation is **exact symbolic algebraic numbers** (`sympy.Expr`
built only from integers, rationals and radicals). Arithmetic on them is symbolic and
therefore exact; the only work is *deciding a sign*, which `packcheck/exact.py` does
with a decision procedure:

1. Enclose the value in a rational interval (`Fraction` endpoints) computed with exact
   integer root extraction (`math.isqrt` and an integer n-th root). If the enclosure
   excludes 0, the sign is settled — rigorously, since the enclosure provably contains
   the value.
2. Otherwise decide `value == 0` **exactly**: an algebraic number is zero iff its
   minimal polynomial over `Q` is `x`. This is a decision procedure, not a heuristic.
3. If non-zero, double the precision and return to step 1. This terminates, because the
   enclosure width goes to 0 while `|value| > 0` is fixed.

If a sign genuinely cannot be settled (unsupported expression, precision ceiling), the
checker raises rather than guessing. There is no path on which "small" becomes "zero".

`coordinate_type: "interval"` is also supported, using rigorous outward-rounded
rational intervals. It is **conservative**: it can refuse a feasible packing but can
never accept an infeasible one.

### Trade-offs of the choice

| | symbolic algebraic (used for the reference certificates) | rational intervals |
|---|---|---|
| Certifies exact contact (`distance == 2`) | yes | no — only degenerate boxes |
| Speed | slower; a zero test needs `minimal_polynomial` | fast |
| Nested/high-degree radicals | can get slow | unaffected |
| Failure direction | raises `UndecidedSign` | rejects (fails closed) |

Since *every* optimal packing has contacts, interval mode cannot certify an optimum.
That is why the reference certificates are `algebraic`. Interval mode is there for
certificates that come out of a rigorous numerical enclosure with genuine slack.

## What exact arithmetic buys

The float checker in `tests/naive_float.py` exists only to make the argument concrete.
It faces a dilemma that is intrinsic, not a coding error:

* **Tolerance 0 rejects a valid packing.** `sqrt(3)` is not representable, so in the
  true `n = 10` packing a pair of circles that touch exactly comes out at distance
  `1.9999999999999998`. Test: `test_float_checker_with_zero_tolerance_rejects_a_valid_packing`.
* **Any tolerance large enough to fix that accepts infeasible packings.** At the
  smallest round tolerance that admits the true packing (`1e-9`), the float checker
  accepts an overlap of `1e-12` — and of `1e-18`, and `1e-30`. Test:
  `test_float_checker_with_a_working_tolerance_accepts_infeasible_packings`.
* **Below ~1e-16 relative the perturbation does not even exist in `float`.** The
  coordinate `2 - 1e-18` rounds to exactly `2.0`. Test:
  `test_float_checker_cannot_even_represent_the_perturbation`.

No tolerance does both jobs. The exact checker does both, with no tolerance parameter
at all.

## The result

`./run.sh` — one command, from scratch.

* **Accepts** the classical triangular-lattice optima for the triangular numbers
  `n = 3, 6, 10` (`certificates/n{003,006,010}-triangular.json`), including under
  `--require-tight`, and confirms `s(6) = 4 + 2*sqrt(3)` and `s(10) = 6 + 2*sqrt(3)`
  as recorded in the problem README.
* **Rejects**, for each of those, single-coordinate perturbations of
  `1e-6, 1e-12, 1e-18, 1e-30, 1e-60` — as overlaps, as points pushed outside each of
  the three edges, and as a shrunk `side_length`.
* **Rejects** an overlap of `sqrt(3) - 17320508075688772935/10**19` (~`2.7e-20`, and
  irrational), while **accepting** a separation by the same amount — so the rejections
  are discrimination, not blanket pessimism.
* **Rejects** malformed certificates as malformed: JSON floats, `n` mismatches, unknown
  `coordinate_type`, irrational coordinates declared `rational`.
* A source audit (`tests/test_no_floats.py`) parses every module of `packcheck` and
  fails on any float literal, `float()` call, `.evalf()`, or import of `numpy` /
  `decimal`. `math` is admitted only for `math.isqrt`.

131 tests, ~2 s.

## Spec ambiguities found

These are **findings**, reported rather than silently resolved. An independent
reimplementation may reasonably choose differently, and the disagreement would be
informative rather than a bug.

1. **Where is the triangle?** `README.md` and `RULES.md` §2 give coordinates but never
   fix the triangle's position or orientation. This checker assumes the canonical
   placement `A=(0,0)`, `B=(d,0)`, `C=(d/2, d*sqrt(3)/2)` and does not search over
   rigid motions, so a valid packing written against a different placement is
   rejected. **The certificate format should state the placement, or carry the three
   vertices explicitly.**
2. **Is `side_length` `s` or `d`?** The format says "value of `s(n)`" and the tables
   quote `s`, so it is read as `s`. Worth stating outright, since the whole document
   otherwise works in the point formulation where `d` is natural.
3. **What does "the reported side length is consistent with the coordinates" mean?**
   Containment alone only certifies `s(n) <= s`, so an inflated `s` passes. This
   checker additionally computes the exact minimal side `d_min = max_i (x_i + y_i/sqrt(3))`
   for the canonical placement and reports non-tightness as a warning
   (`--require-tight` promotes it to a failure). Whether tightness is *required* is
   not stated in the spec.
4. **How is an `interval` coordinate written?** `RULES.md` §2 permits
   `coordinate_type: "interval"` but gives no encoding. This checker requires
   `[[xlo, xhi], [ylo, yhi]]` and rejects anything else rather than guessing.
5. **Open or closed triangle; strict or non-strict distance?** Both must be
   non-strict — every optimum has circles touching the sides and each other — but the
   spec says "inside" and "distance >= 2" without comment. Forced, but worth writing down.
6. **May `side_length` be a decimal string?** `"10.928"` is exactly `1366/125`, which
   is a legitimate rational, but it is almost certainly truncated optimiser output.
   This checker parses it exactly and emits a warning. Arguably the format should ban
   decimal literals outright.

## Layout

```
packcheck/exact.py     exact reals: integer roots, rational intervals, sign decision
packcheck/checker.py   certificate parsing + the three geometric checks
packcheck/__main__.py  CLI
make_certificates.py   generates the n = 3, 6, 10 reference certificates
certificates/          those certificates (regenerated by run.sh)
tests/                 validation: accepts, rejects, float comparison, no-float audit
run.sh                 the one command
```

## Usage

```bash
uv run python -m packcheck path/to/n017-something.json
uv run python -m packcheck --require-tight certificates/*.json
```

Exit status is 0 iff every certificate was accepted.

## Reproducibility

`uv`, Python 3.12 (`.python-version`), `sympy==1.13.3`, `mpmath==1.3.0`,
`pytest==8.3.4`, locked in `uv.lock`. There is no randomness anywhere in this
experiment, so there is no seed to pin.
