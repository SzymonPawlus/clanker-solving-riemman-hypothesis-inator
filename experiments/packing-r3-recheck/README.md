# packing-r3-recheck — independent exact recheck of the `+4*sqrt(3)` certificates

**What this is:** an independently written exact checker for point-formulation packing
certificates, applied to the three certificates in
`experiments/packing-r3-qsqrt3/certificates/` (n = 17, 24, 31). It is a *check*, not a
construction — it produces no new packing and no new bound.

## Question

Do the certificates claiming, as constructions (upper bounds),

- s(17) <= 6 + 4*sqrt(3)
- s(24) <= 8 + 4*sqrt(3)
- s(31) <= 10 + 4*sqrt(3)

actually satisfy the specification in `problems/circle-packing-equilateral-triangle/RULES.md`
§2 — exact coordinates, pairwise distances >= 2, containment in the *fixed* closed triangle
A = (0,0), B = (d,0), C = (d/2, d*sqrt(3)/2) with d = s - 2*sqrt(3) — and are they **tight**?

## Independence

Problem `RULES.md` §3 requires the second checker to be written from the problem statement, not
by reading or adapting the author's code. Accordingly `recheck.py` was written having read only:

- `problems/circle-packing-equilateral-triangle/README.md` (the point reformulation),
- `problems/circle-packing-equilateral-triangle/RULES.md` §2–3 (the conventions),
- the three certificate JSON files themselves (the object under test).

Nothing under `experiments/packing-r3-qsqrt3/` other than the certificates was opened — not its
README, not `check.py`, not `snap.py`, not `rattler.py` — and nothing under
`problems/circle-packing-equilateral-triangle/attacks/r3-qsqrt3/`. The half-plane forms, the
sign conventions and the minimal-enclosing-side formula are derived in the module docstring of
`recheck.py` from the vertex convention alone.

**This check cannot promote anything.** Repo `RULES.md` §5 restricts `verified:review` to an
agent of a *different model family* than the author. Both the author (`r3-qsqrt3`) and this
worker (`r3-recheck`) are `claude`. The certificates stay `numerical`.

## Method

Exact arithmetic over Q(sqrt(3)): every quantity is a pair of `fractions.Fraction` (a, b)
meaning a + b*sqrt(3), with addition, multiplication and an exact `sign()` (a + b*sqrt(3) = 0
iff a = b = 0; mixed signs decided by comparing a^2 with 3b^2). **No float takes part in any
accept/reject decision.** Floats appear only in `approx()` for printing and in one clearly
labelled diagnostic that cannot pass or fail anything.

Per certificate the checker verifies:

1. every exact field parses (decimal strings are rejected outright, per §2), `n` matches the
   coordinate count, points are distinct, `claim` and `status` are well formed, and the
   informational `_d` field equals the independently derived `s - 2*sqrt(3)`;
2. all C(n,2) pairwise squared distances >= 4, exactly;
3. containment in the closed triangle via the three half planes y >= 0, sqrt(3)x - y >= 0,
   sqrt(3)x + y <= sqrt(3)d, all non-strict, **without any search over rigid motions**;
4. the exact minimal enclosing side in that fixed placement,
   d_min = max_i (x_i + y_i*sqrt(3)/3), and whether the declared d equals it (**tight**),
   exceeds it (valid but inflated) or falls below it (invalid).

## Controls

- **A — positive.** The triangular-lattice packings n = 3, 6, 10, 15, 21, whose optimal
  s = 2(k-1) + 2*sqrt(3) is `cited` (Oler 1961) in the problem README. All five are accepted and
  reported tight.
- **B — negative,** on the n = 17 certificate: (B1) move one point 1/1000 toward its nearest
  neighbour — rejected on separation; (B2) push the d_min-attaining point 1/1000 past edge BC —
  rejected on containment; (B2b) push a point 1/1000 below edge AB — rejected on containment;
  (B3) deflate the declared s by 1/1000 — rejected; (B4) inflate the declared s by 1/1000 —
  **accepted but reported NOT tight**, as required; (B5) a decimal string in an exact field —
  rejected by the parser.
- **C — external consistency,** exact: s(n) is non-decreasing in n and s(Delta(k)) =
  2(k-1) + 2*sqrt(3) is `cited`, so the claimed s must lie between the bracketing triangular
  values. This is the control that catches the worst available convention error — writing d into
  the `side_length` field — since all three certificates' d values fall *below* their lower
  bracket and would be rejected.
- **Self-tests** (`selftest.py`): the exact `sign()` routine against mpmath at 1000 dps on 20000
  random inputs (0 mismatches), ring identities, and the parser on 11 shapes it must accept and
  10 it must reject.
- **Diagnostic** (floats, non-load-bearing): a scan over rotations, using the support-function
  form side(t) = (2/sqrt(3)) * sum_k max_i <p_i, u_k(t)>, checking whether a rotated copy of each
  point set would fit a strictly smaller equilateral triangle. None does — the minimum is
  attained at the repo's fixed orientation.

## Result

All three certificates are **confirmed**: separation exact, containment exact, `side_length`
consistent, and **tight** in the fixed placement.

| certificate | n | claimed s | pairs checked | min sq. dist. | exact contacts | pts on boundary | d_min | tight |
|---|---:|---|---:|---:|---:|---:|---|---|
| `n017-r3-qsqrt3.json` | 17 | 6 + 4*sqrt(3) | 136 | 4 | 26 | 11 | 6 + 2*sqrt(3) | yes |
| `n024-r3-qsqrt3.json` | 24 | 8 + 4*sqrt(3) | 276 | 4 | 45 | 15 | 8 + 2*sqrt(3) | yes |
| `n031-r3-qsqrt3.json` | 31 | 10 + 4*sqrt(3) | 465 | 4 | 59 | 18 | 10 + 2*sqrt(3) | yes |

No disagreement with the author's certificate was found on any quantity, including the secondary
`_contacts_at_distance_exactly_2` and `_points_on_the_boundary` fields, which this checker
recomputed and matched.

**What this does and does not establish.** It establishes s(17) <= 6 + 4*sqrt(3),
s(24) <= 8 + 4*sqrt(3), s(31) <= 10 + 4*sqrt(3) as constructions, at status `numerical`. It says
**nothing** about optimality: all three n are open, and a tight certificate is tight *for its own
point set*, not minimal over all point sets.

## Reproduce

Python 3.11.15, standard library only (`fractions`, `json`, `re`, `math`, `itertools`). One
command, from the repository root:

```
python3 experiments/packing-r3-recheck/recheck.py
```

Exit status 0 iff all controls pass and all three certificates are accepted. It runs in about one
second and is fully deterministic (no seeds are involved anywhere).

Optional, additionally requires `mpmath` 1.3.0 (the arithmetic self-tests; seed 20260823 pinned
in the file):

```
cd experiments/packing-r3-recheck && python3 selftest.py
```

To check some other certificate, pass paths: `python3 recheck.py path/to/cert.json ...`.

## Files

- `recheck.py` — the checker, the controls and the diagnostic. Its module docstring is the
  specification restated in its own words, with the half planes derived.
- `selftest.py` — arithmetic and parser self-tests.
- `output.txt` — the full recorded output of `python3 recheck.py`.
