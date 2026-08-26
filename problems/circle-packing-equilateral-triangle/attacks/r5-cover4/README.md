# AG. The k = 4 covering question, decided in the NO direction

**This is a lower-bound (optimality-side) attack, aimed at RECONSTRUCTING a `cited` result
(Melissen 1993, `s(9) = 6 + 2√3`). It is not new mathematics, and it establishes no bound on
`s(n)` or `d(n)`. Its outcome is that the covering route cannot reconstruct that result.**

```
status:  numerical  — the SAT/colouring results and containment figures
         sketch     — the corner-sector reduction, and the reading in §4
author:  claude (worker r5-cover4) for the machinery and the refutation;
         manager for the write-up and the independent verification in §2, 2026-08-24
issue:   #110, round-4 proposal AG
code:    experiments/packing-r5-cover4/
kill:    KILL-CRITERION.md — did not fire (k = 3 calibrated; a direction closed)
```

**Nothing here is assumable** (`RULES.md` §3).

> **Provenance.** The worker was terminated by a connection loss, having committed seven times
> (the round-5 commit-early rule working as intended — nothing was lost). Its last message was
> "**UNSAT.** Now I must redo that in exact arithmetic — the float run proves nothing", and its
> final commit shows it *had* redone it exactly. It never wrote this file. The manager wrote it,
> and independently re-verified the central claim rather than transcribing it.

---

## 0. The question

Oler normalisation: points at mutual separation `≥ 1` in equilateral `T(a)` of side `a`.
(Repo units: separation 2, side `d = 2a`, `s = d + 2√3`.)

If `T(a)` admits a cover by `m` sets each of **diameter `< 1`**, then any `m+1` points include two
within distance `< 1`, so at most `m` points fit. To reconstruct EO(4) — that `n = 9` points force
`a ≥ 3` — one needs, **for every `a < 3`, an 8-piece cover of `T(a)`**.

Round-4 proposal AG asserted this should work at `Δ(k) − 1`, on the ground that "the required
piece count sits exactly at the packing-duality floor". The instruction was to *test that claim,
not assume it*.

## 1. Calibration at k = 3 — passed, two-sided

The gate was: settle `k = 3` (`n = 5`, `a` just under 2, needing a 4-piece cover of `T(2⁻)`)
before touching `k = 4`. From `k3_results.json`:

| case | expected | result |
|---|---|---|
| medial 4-piece dissection of `T(2)` | cover, diam `< 1` | **ok** |
| same at `a = 199/100`, strict | ok | **ok** |
| kite dissection of `T(2)` | must FAIL on diameter | **correctly failed** |
| medial minus one piece | must FAIL to cover | **correctly failed** |
| kites at `a = 3/2`, strict | ok | **ok** |

Exact `Q(√3)` geometry with exact inclusion–exclusion coverage, plus two negative controls that a
broken checker would have passed. The procedure works.

## 2. The k = 4 answer: **NO**, and it was verified independently

The committed refutation (`refutation_points.json`, `refutation.cnf`, `refutation.drat`):
`a = 3`, `k_total = 8`, and after a **corner-sector reduction** — an 8-cover of `T(3)` forces a
**5-cover of a residual region `U`**, three pieces being absorbed by the corners — a witness set of
**441 points in `U`** with **52 684** conflict pairs, refuted in exact rational arithmetic with a
DRAT proof.

**The manager re-verified this from the point set alone**, not by re-running the worker's pipeline:

- Rebuilt the conflict graph from the 441 exact rational points (edge iff squared distance `≥ 1`).
  Recomputed **52 684 edges — matches the file exactly**.
- Re-encoded the colouring independently and solved with a **different SAT solver** (Cadical153):
  **5-colourable? False.** 6-colourable? True. So the residual's chromatic number is exactly 6,
  one more than a valid 8-cover would permit.
- Containment: every one of the 441 points lies in the closed `T(a)` for `a ≥ 2.999989683…`, and
  some lie exactly on edge `AB` (`min y = 0`).

So, as a `numerical` statement: **`U`'s witness set needs 6 colours, not 5.** Given the corner
reduction, **`T(a)` admits no 8-piece cover of diameter `< 1` for any `a ≥ 2.99999`.**

**What the manager did NOT verify: the corner-sector reduction itself** (`corner_reduction.py`),
which is the step carrying "8-cover of `T(3)`" to "5-cover of `U`". That is the load-bearing
`sketch` here. The chromatic fact above stands on its own regardless; the *conclusion about
8-covers* depends on the reduction being right.

## 3. A near-miss the manager walked into, recorded because it is the point of the protocol

The worktree also contained `refutation_core.json` / `core.cnf` / `core.drat` — 21 points, 146
edges — from a `minimize.py` core-minimisation that the connection loss interrupted. **These were
never committed by the worker.**

The manager initially verified *those* and found the 21-point graph is **7-colourable**, i.e. it
refutes nothing. Had that been reported as "the refutation fails to check out", it would have been
a false alarm against a correct result; had the file been committed and read later by someone else
as the refutation, it would have been a false positive in the other direction. It is an
**incomplete intermediate**, not a certificate, and it is not merged.

The lesson is the round-5 protocol's §6: the arithmetic was never wrong, the *input selection* was.

## 4. Reading: the covering route cannot reconstruct EO(4)

To prove `d(9) ≥ 3` by covering, one needs an 8-cover of `T(a)` for **every** `a < 3`. §2 says no
such cover exists for `a ≥ 2.99999`. The route therefore **fails precisely in the sliver where it
would have to work** — it falls short of 3 by about `10⁻⁵`.

This is a quantified instance of round 4's finding that the counting tools are
**interaction-blind** and "close exactly zero of the missing `+1`" at `Δ(k) − 1`. Here the shortfall
is not merely qualitative: it is `1.03 × 10⁻⁵` in `a`, measured.

**AG's premise is therefore wrong as stated.** At `Δ(4) − 1` the required piece count does *not*
sit at a floor the covering method can reach; it sits one colour above it.

Two limits on this reading, both real:

1. It says covering **alone** cannot do it. It does **not** establish `d(9) ≥ 2.99999` — that would
   need the YES direction (8-covers actually existing for all `a ≤ 2.99999`), which was **not**
   attempted before the worker died.
2. It rests on the unverified corner reduction (§2).

## 4a. Cross-lane: the sibling exhaustion attempt failed too, for a *different* reason

`attacks/r5-exhaust4/` attacked the **same** case (EO(4)) by the **exhaustion** route, deliberately
without coordination. It also fails, and the two failures are not the same failure:

- **Covering (here):** the method's ceiling is *below* the target — no 8-cover exists for
  `a ≥ 2.99999`, so it falls `10⁻⁵` short of `a = 3`.
- **Exhaustion (there):** no computational wall at all — shrinking the residual gap 50× cost only
  4.3× the nodes — but the route is *unreachable* in principle, because for every dyadic level
  `L ≥ 2` the node containing the `Δ(4)`-lattice-minus-one-point is refuted by none of the pair,
  capacity or Oler-hull rules. That lane's `sketch` criterion: **dyadic pigeonhole closes EO(k) iff
  `k ≤ 3`.**

Both are counting-family methods, and both die at `Δ(k) − 1`. This is round 4's
"interaction-blind, closes exactly zero of the missing `+1`" observed twice more, from two
independent directions, on a case whose answer is `cited`.

**One observation from that lane bears directly on this one and widens its question**
(`sketch`, theirs, not verified here): **no triangle has capacity exactly 2**, because
`a(2) = a(3)`. So any partition-and-capacity closure is forced to use **non-triangular pieces** —
which is a constraint on the YES direction this lane never attempted, and the worker that found it
could not locate it recorded anywhere in the repo.

## 5. Reproduce

```
cd experiments/packing-r5-cover4 && python3 k3_calibrate.py     # k=3 gate, exact, ~50 ms
python3 refute_exact.py                                          # the exact k=4 refutation
```

The manager's independent re-verification is deliberately not scripted here: it was performed from
`refutation_points.json` alone, with an independently written encoding and a different solver, and
is reproduced by doing the same rather than by running this directory's code.
