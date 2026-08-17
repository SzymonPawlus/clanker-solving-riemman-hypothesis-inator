# Rules — circle packing in an equilateral triangle

Problem-specific. The repo-wide protocol in [`../../RULES.md`](../../RULES.md) still applies in
full; this file adds what is particular to a *continuous geometric optimisation* problem.

---

## 0. What makes this problem different

Progress here is **cheap to state and cheap to check, but easy to fake**. A packing is a finite
list of coordinates; anyone can verify it in seconds. That is the good news, and it means this
problem rewards agents far more than a pure proof problem does.

The bad news is the corresponding failure mode. Every optimiser you write will return a
configuration that is *slightly* infeasible — two circles overlapping by $10^{-9}$, a centre
$10^{-12}$ outside the triangle — and will report a side length beating the world record. **That
result is always wrong.** Floating-point slop is not a small error here; it is the difference
between a discovery and nothing at all.

So the governing rule of this directory: **no packing is a result until an exact or rigorously
rounded check confirms it.** Optimiser output is a hypothesis.

---

## 1. Two kinds of result — never conflate them

| | Claim | Difficulty |
|---|---|---|
| **Construction** | $s(n) \le c$ — here is a packing | self-certifying, do this |
| **Optimality** | $s(n) \ge c$ — nothing does better | hard, needs exhaustive argument |

State which you have in the first line of any file or PR. "I found the optimal packing for
$n = 17$" is two claims, and you almost certainly have only the first. An optimiser that
converges to the same configuration from a thousand random starts is **evidence for**
optimality, not a proof of it — status `numerical`, permanently, until an actual lower-bound
argument exists.

---

## 2. Certificate format

Work in the **point formulation** (`README.md`): $n$ points, pairwise distance $\ge 2$, inside an
equilateral triangle of side $d = s - 2\sqrt{3}$.

Every claimed packing lives in `results/n<NNN>-<slug>.json`:

```json
{
  "n": 17,
  "claim": "construction",
  "side_length": "exact or interval-bounded value of s(n)",
  "coordinates": [["exact x", "exact y"], "..."],
  "coordinate_type": "rational | algebraic | interval",
  "verified_by": "path to the checker that confirmed it",
  "status": "numerical | verified:review | verified:lean",
  "beats_record": "yes/no, vs which published record and source"
}
```

Coordinates must be **exact rationals, exact algebraic numbers, or rigorous intervals** — never
bare floats. If your optimiser produced floats, either round them to nearby rationals and prove
feasibility at those rationals, or give a rigorous interval enclosure. Both are acceptable;
pasting the float output is not.

## 3. Verification — the other agent writes an independent checker

This is how a packing earns `verified:review` here, and it replaces prose cross-examination
(`../../RULES.md` §5) for computational claims:

1. The author submits the certificate and their own checker.
2. The **other agent writes a checker independently**, from the problem statement in
   `README.md` — not by reading, importing, or adapting the author's code.
3. Both checkers must confirm: all $\binom{n}{2}$ pairwise distances $\ge 2$, all points inside
   the triangle, and the reported side length.
4. Disagreement between checkers is a finding. Investigate it; do not average them.

Reimplementing the check is the whole point. A second agent running the first agent's script
verifies nothing except that the script is deterministic.

`verified:lean` requires the feasibility check formalised in Lean over exact rationals. That is
genuinely reachable for a fixed small $n$ — a finite conjunction of rational inequalities — and
is the strongest thing this problem can produce short of an optimality proof.

## 4. Claiming a record

Before claiming any improvement:

1. Check the current record in Graham–Lubachevsky (for $22 \le n \le 34$), Friedman's tables,
   and Packomania. Cite which you checked and what the record is.
2. Confirm the improvement **exceeds your error bars**. If your $s$ beats the record by less than
   your verification tolerance, you have not beaten it.
3. Reproduce it from a fresh random seed.

An improvement of $10^{-7}$ over a published record is, in order of likelihood: a bug, a
misread table, an infeasible configuration, or a genuine record. Rule out the first three
explicitly in the PR.

Matching a known record exactly is a **good outcome** — report it as successful reproduction and
a validated pipeline, not as a failure to improve.

## 5. Numerical practice

- Standard method for generating candidates is Lubachevsky–Stillinger billiard simulation
  (inflate circles, resolve collisions); the Graham–Lubachevsky paper describes it. Random
  restarts plus local perturbation is the workhorse.
- Pin your seeds and library versions; an unreproducible packing is worthless even if correct.
- Use `mpmath` or exact rationals for the final check. NumPy floats are for search only.
- Symmetry is a strong prior for good packings but is **not** a constraint — several known
  optima are asymmetric. Do not restrict the search to symmetric configurations and then report
  the result as optimal.
- Rattlers (circles free to move without changing $s$) are normal and do not invalidate a
  packing. Do not "fix" them.

## 6. Realistic targets

In rough order of achievability. Partial results count — a single $n$ is a real contribution.

1. Reproduce and independently verify the known table for $n \le 15$. Establishes the pipeline.
2. **Resolve the proven/best-known discrepancy** flagged in `README.md` against Melissen's
   thesis. This is pure literature work, needs no optimiser, and fixes a wrong table.
3. Verify Graham–Lubachevsky's $22 \le n \le 34$ packings with exact certificates.
4. Formalise feasibility in Lean for one small $n$.
5. Improve a best-known packing for some $n$ in the 16–34 range, or extend past 34.

Do not attempt a general optimality proof for arbitrary $n$. Oler's inequality is the tool for
lower bounds; understand it before proposing anything in that direction.
