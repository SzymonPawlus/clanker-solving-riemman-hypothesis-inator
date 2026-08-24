# r3-recheck — independent exact recheck of the n = 17, 24, 31 certificates

**This file establishes no new mathematics.** It reports an independent *verification attempt*
on three existing certificates. Every claim below is about those certificates; the three bounds
they carry remain **constructions** (upper bounds), status **`numerical`**, exactly as before.

```
kind:      verification (independent second checker), not a construction and not a lower bound
claims:    s(17) <= 6 + 4*sqrt(3),  s(24) <= 8 + 4*sqrt(3),  s(31) <= 10 + 4*sqrt(3)
           -- all three CONFIRMED as constructions and TIGHT for their point sets
status:    numerical (unchanged; see "What this is worth" -- this check CANNOT promote anything)
author:    claude (Opus 5), worker r3-recheck, 2026-08-23
certificates under test:
           experiments/packing-r3-qsqrt3/certificates/n0{17,24,31}-r3-qsqrt3.json
this checker:
           experiments/packing-r3-recheck/recheck.py   (stdlib only, exact Q(sqrt 3))
```

---

## 1. What was checked, and the answer

| | n = 17 | n = 24 | n = 31 |
|---|---|---|---|
| exact parse, no decimal strings | PASS | PASS | PASS |
| `n` matches coordinate count, points distinct | PASS (17) | PASS (24) | PASS (31) |
| **separation:** all C(n,2) squared distances >= 4, exactly | **PASS** (136 pairs) | **PASS** (276 pairs) | **PASS** (465 pairs) |
| min squared distance | 4 (exact) | 4 (exact) | 4 (exact) |
| exact contacts (distance exactly 2) | 26 | 45 | 59 |
| **containment:** closed triangle, fixed placement, non-strict | **PASS** | **PASS** | **PASS** |
| points on the triangle boundary | 11 | 15 | 18 |
| **`side_length` consistent:** d = s - 2*sqrt(3) holds all points | **PASS** | **PASS** | **PASS** |
| exact minimal enclosing d in the fixed placement | 6 + 2*sqrt(3) | 8 + 2*sqrt(3) | 10 + 2*sqrt(3) |
| **tight** (declared d equals d_min, exactly) | **YES** | **YES** | **YES** |

**No disagreement was found on any quantity.** That includes the certificates' own secondary
fields `_min_squared_distance`, `_contacts_at_distance_exactly_2` and `_points_on_the_boundary`,
which this checker recomputed independently and matched exactly (26/45/59 contacts, 11/15/18
boundary points). Per problem `RULES.md` §3.4 a disagreement would have been a finding to
investigate; there is none to report.

So, as **constructions** (`RULES.md` §1 — upper bounds, not optimality):

> s(17) <= 6 + 4*sqrt(3) = 12.928203230275..., s(24) <= 8 + 4*sqrt(3),
> s(31) <= 10 + 4*sqrt(3), each witnessed by an exact packing in Q(sqrt(3)) whose declared side
> is exactly the minimal side of the fixed-placement triangle containing it.

All three n are **open**. Nothing here bears on optimality, and a certificate being "tight" means
only that its declared s cannot be shrunk *for that point set* — not that no other point set does
better.

## 2. How independence was maintained

Problem `RULES.md` §3 requires the second checker to be written from the problem statement, "not
by reading, importing, or adapting the author's code". The only inputs to `recheck.py` were:

- `problems/circle-packing-equilateral-triangle/README.md` — the point reformulation
  s(n) = 2*sqrt(3) + d(n);
- `problems/circle-packing-equilateral-triangle/RULES.md` §2–3 — the fixed conventions;
- the three certificate JSON files, which are the object under test.

Nothing else under `experiments/packing-r3-qsqrt3/` was opened (not its README, `check.py`,
`snap.py` or `rattler.py`), and nothing under `attacks/r3-qsqrt3/`. The three half planes, their
sign conventions and the minimal-enclosing-side formula were derived from the vertex convention
A = (0,0), B = (d,0), C = (d/2, d*sqrt(3)/2) alone; that derivation is written out in the module
docstring of `recheck.py`:

- (H1) y >= 0; (H2) sqrt(3)x - y >= 0; (H3) sqrt(3)x + y <= sqrt(3)d, signs fixed by testing the
  centroid (d/2, d*sqrt(3)/6);
- d occurs only in (H3), which rearranges to d >= x + y/sqrt(3), so the exact minimal enclosing
  side is d_min = max_i (x_i + y_i*sqrt(3)/3) once (H1) and (H2) hold.

The author's certificates state the same formula in their `_tightness_witness` field. That field
was read (it is part of the object under test) *after* the derivation above was written, and the
agreement is a genuine two-route agreement rather than a copy.

Arithmetic: every quantity is a + b*sqrt(3) with a, b `fractions.Fraction`; comparison is by an
exact sign rule (a + b*sqrt(3) = 0 iff a = b = 0, since sqrt(3) is irrational; mixed signs decided
by a^2 vs 3b^2). **No float participates in any accept/reject decision.** The sign routine was
tested against mpmath at 1000 dps on 20000 random inputs, 0 mismatches.

## 3. Controls — why this check is worth something

A checker that accepts everything proves nothing, so:

- **Positive.** The triangular lattices n = 3, 6, 10, 15, 21, whose optimum
  s = 2(k-1) + 2*sqrt(3) is `cited` (Oler 1961), are all accepted **and reported tight**.
- **Negative,** on n = 17: one point moved 1/1000 toward its nearest neighbour → **rejected**
  (separation); the d_min-attaining point pushed 1/1000 past edge BC → **rejected**
  (containment); a point pushed 1/1000 below edge AB → **rejected**; declared s deflated by
  1/1000 → **rejected**; declared s **inflated** by 1/1000 → **accepted but reported NOT tight**,
  which is the required behaviour (an inflated s is an honest, loose upper bound); a decimal
  string in an exact field → **rejected by the parser**, per `RULES.md` §2.
- **External consistency, exact.** s(n) is non-decreasing in n and s(Delta(k)) = 2(k-1) +
  2*sqrt(3) is `cited`, so each claimed s must sit between its bracketing triangular values:
  11.4641 <= s(17) <= 13.4641, 13.4641 <= s(24) <= 15.4641, 15.4641 <= s(31) <= 17.4641. All
  three pass. This is precisely the control that catches the convention error the author named as
  their main exposure — writing d into the `side_length` field: each certificate's d
  (9.4641, 11.4641, 13.4641) falls *below* its lower bracket, so that error would have been
  caught here rather than passing silently.
- **Rotation diagnostic** (floats, explicitly non-load-bearing, cannot pass or fail anything):
  minimising the support-function side (2/sqrt(3)) * sum_k max_i <p_i, u_k(t)> over orientations
  t finds its minimum at the repo's fixed orientation for all three point sets. No rotated copy
  fits a smaller triangle, so the fixed-placement tightness is not an artefact of the convention.

## 4. What this is worth — and what it is not

**It cannot grant `verified:review`, and it promotes nothing.** Repo `RULES.md` §5 restricts
`verified:review` to an agent of a **different model family** than the author, precisely so that
the two checks fail in decorrelated ways. The author (`r3-qsqrt3`) and this worker
(`r3-recheck`) are both `claude`. The three certificates therefore remain **`numerical`**, and
this file must not be cited as if it had upgraded them. A cross-family check by codex is still
required, and would examine the certificates from scratch, not this file.

What it *is* worth: a genuinely independent reimplementation catches exactly the failure mode the
author flagged — that if the triangle placement or the meaning of `side_length` had been
misread, the certificate and the author's own checker would be internally consistent and
externally wrong, since both would share the misreading. That class of error is ruled out here:
the placement, the half planes, the s-to-d reduction and the minimal-enclosing formula were all
re-derived, and the exact numbers agree. Also ruled out: a floating-point-slop acceptance
(there are no floats in the decisions), an accepted decimal string, and a certificate whose
declared s is inflated (that would now be reported as not tight rather than as a record).

**Not checked here** (stated so nobody mistakes its scope):

- **optimality.** Nothing in this file bounds s(n) from below. n = 17, 24, 31 remain open.
- **the published record values.** The certificates quote Graham–Lubachevsky (1995) via
  `experiments/circle-packing-search/reference.py` for m(17), m(24), m(31). This check does not
  open that paper or that table; it only observes that the claimed s values are arithmetically
  consistent with the quoted m via s = 2/m + 2*sqrt(3) (agreement to 4e-14, the precision of
  the quoted 15-digit m values -- a float observation, deliberately not load-bearing), and that
  they sit inside the bracket
  forced by the `cited` triangular values. The attribution of the records is literature work
  (verification-critical) and is not touched here.
- **how the packings were found.** The provenance chain (LS billiard, SLSQP, snapping, rattler
  placement) was deliberately not read. Only the certificates are load-bearing, and they stand
  or fall on their own.

## 5. Kill-criterion

Declared before the check: *if any of the three certificates fails separation, containment or
`side_length` consistency, stop and report the refutation loudly and specifically — the exact
quantity, the exact index and both values — rather than repairing the certificate* (repo
`RULES.md` §6.2–6.3, problem `RULES.md` §3.4). Secondary: *if my checker and the author's
disagree on any recomputed quantity, report the disagreement; do not average it away.*

**The kill-criterion did not fire.** All three certificates passed every test, and every
recomputed quantity agreed. The controls in §3 are the evidence that this is a real pass and not
a checker that accepts anything.

## 6. Reproduce

From the repository root, Python 3.11.15, standard library only, about one second, deterministic:

```
python3 experiments/packing-r3-recheck/recheck.py
```

Exit status 0 iff all controls pass and all three certificates are accepted. Full recorded output
is in `experiments/packing-r3-recheck/output.txt`; method and file inventory are in
`experiments/packing-r3-recheck/README.md`.
