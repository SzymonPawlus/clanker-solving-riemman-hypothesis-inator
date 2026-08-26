# Capacity spectra by cell shape: skipped capacities are shape-specific, and several shapes skip none

**Lower-bound (optimality) direction, exploratory. No bound on `s(n)` or `d(n)` is established.**

```
status:  numerical  — the whole spectrum table (FLOAT maximin optimiser; see §3)
         sketch     — the reading in §4
author:  claude (worker r6-nontri), 2026-08-26; write-up by the manager after the worker
         was terminated by an account session limit before writing up or reaching a partition
issue:   #110, round-6 execution of BRIEF-R6 §4 opening 2
code:    experiments/packing-r6-nontri/
kill:    KILL-CRITERION.md — did not reach its trigger; the lane stopped short (§5)
```

**Nothing here is assumable** (`RULES.md` §3).

---

## 0. The opening

`attacks/r5-exhaust4/` recorded, `sketch` and unverified, and could not find it anywhere in the repo:

> **No triangle has capacity exactly 2**, because `a(2) = a(3)`.

Here `a(m)` is the least scale at which a shape holds `m` points at separation `≥ 1`. If a shape's
capacity jumps `1 → 3`, then a **partition-and-capacity** proof — cover `T(a)` by cells, sum
capacities, get `< n` — can never use a capacity-2 cell of that shape. Every partition attempt in
this repo has used triangles or convex polygons, and the merged partition engine (PR #53) has sat
unused since calibration.

**The question: is there a cell family with no skipped capacities?**

## 1. The answer: yes

`a(m)` computed for `m = 2..10` over nine families (`out/spectrum.log`). A capacity `m` is
**skipped** when `a(m) = a(m+1)`, i.e. no size of that shape has capacity exactly `m`:

| shape | skipped capacities, `m = 2..10` |
|---|---|
| **half-triangle** | **none** |
| **90° sector** | **none** |
| **slab (3:1)** | **none** |
| **slab (6:1)** | **none** |
| 60° sector | 2 |
| 120° sector | 3 |
| half-disc | 4 |
| hexagon | 6 |
| 60° rhombus | 3, 5, 8 |

So the skipped-capacity phenomenon is **real, shape-specific, and avoidable**. The 60° sector shares
the equilateral triangle's own skip at capacity 2 — unsurprising, since it is a corner of one — but
**half-triangles, right-angle sectors and slabs skip nothing in this range.** A partition-capacity
argument is therefore not blocked in principle; it just cannot be built from triangles.

That the 60° rhombus skips **three** capacities is the sharpest warning in the table: highly
symmetric cells are the *worst* choice here, which is the opposite of the natural instinct.

## 2. Validation

The maximin optimiser was validated against `cited` values on the disc and the square before any
spectrum run (`out/validate.log`): agreement to `~1e-16` on 14 of 15 rows. **One row misses**:
`disc, m = 9`, found `0.754684` against the known `0.765367` (`err = -1.07e-2`) — the optimiser
lands in a wrong basin there. So the table above is **not certified**; see §3.

## 3. What is NOT established — read before using the table

- **These are float optimiser outputs.** A skip is detected as `a(m) = a(m+1)` at `1e-9` tolerance.
  Neither the equalities nor the non-equalities are exact, and problem `RULES.md` is explicit that
  float output is a hypothesis. **Every entry needs exact confirmation before use.**
- The `disc, m = 9` miss shows the optimiser *does* fail to find optima. A missed optimum inflates
  `a(m)` and can therefore **manufacture or erase a skip**. The "none" rows are the ones most at
  risk, since a single missed optimum would create a spurious skip — and the ones most load-bearing.
- **The originating claim itself, `a(2) = a(3)` for the equilateral triangle, was not re-verified
  here** — the triangle is not in the scanned families. It remains where `r5-exhaust4` left it:
  `sketch`, propagating unverified through three write-ups now including this one.
- No partition was built. The lane stopped at the table.

## 4. Reading (`sketch`)

If the table survives exact confirmation, it removes an obstruction rather than supplying a proof.
Partition-capacity remains **interaction-blind** — it sums independent per-cell capacities — and
`BRIEF-R6` §3 (F2), plus `r5-exhaust4`'s finding that every interaction-blind method closes exactly
zero of the missing `+1`, says that is how it will fail at `Δ(k) − 1` regardless of cell shape. The
honest expectation is that non-triangular cells help *away* from `Δ(k) − 1` and not at it.

## 5. Where the lane stopped

The worker was terminated mid-run by an account session limit. It had built and validated the shape
library and optimiser, produced the spectrum table, and started a mobility Monte-Carlo
(`out/mob_long.log`, uninterpreted here). It never attempted step 3 of its assignment — building an
actual partition-capacity certificate at EO(3) or EO(4) — so the lane's central question is
untouched.

**Next step, unchanged:** confirm the "none" rows exactly, then attempt a `Σ`-capacity-8 partition
of `T(3⁻)` from half-triangles or slabs, which is the branch `attacks/r5-cover4/` never reached.

## 6. Reproduce

```
cd experiments/packing-r6-nontri
python3 validate.py    # optimiser against cited disc/square values
python3 spectrum.py    # the capacity spectra
```
