# rh-robin-criterion — certified verification of Robin's inequality on [5041, 10^9)

Status of everything here: **`numerical`** (repo RULES.md §3). Not assumable, not a
proof step, says nothing about the truth of RH. Write-up and interpretation:
[`problems/riemann-hypothesis/attacks/robin-criterion/README.md`](../../problems/riemann-hypothesis/attacks/robin-criterion/README.md).
Issue: #75.

## Reproduce

```sh
./run_all.sh        # ~4 minutes, single core, no seeds (fully deterministic)
```

This recompiles the sieve, re-runs both validation gates (the known ≤ 5040 exception
list; 100k-value sieve cross-check), regenerates the certified per-segment threshold
table, sieves [5041, 10^9) with per-segment checkpointing, and certifies every
flagged candidate with interval arithmetic. Exit code 0 means: certified
`sigma(n) < e^gamma * n * log log n` for all 5041 <= n < 10^9.

## Files

| file | role |
|---|---|
| `robin_core.py` | exact sigma / factorization; certified interval decision (`mpmath.iv`); certified filter thresholds |
| `validate_5040.py` | mandatory gate: reproduces the 27 known exceptions in [2, 5040] exactly, else exits 1 |
| `sigma_sieve.c` | segmented exact divisor-pair sieve, uint64; doubles only in the conservative over-flagging filter |
| `certify_results.py` | coverage check; certifies each flagged n (sigma recomputed independently); near-miss catalogue |
| `run_all.sh` | one-command reproduction |
| `VERSIONS.txt` | pinned tool versions |
| `checkpoints/segments.csv` | per-2^20-segment checkpoint: `L,R,argmax_n,sigma,checksum,flags` |
| `checkpoints/candidates.txt` | every n flagged by the conservative filter (all certified 'holds') |
| `checkpoints/near_misses.csv` | certified Robin-ratio enclosures for top per-segment argmaxes |
| `checkpoints/thresholds.txt` | certified per-segment filter thresholds (hex doubles) |

## Soundness argument, in one paragraph

sigma(n) is computed by two independent exact-integer methods (divisor-pair sieve in
C; trial-division factorization in Python) which are asserted equal on every
candidate and on a 100k-value validation window. The transcendental side is never
evaluated in floating point for a decision: the C filter uses a per-segment double
threshold that is *certifiably* at most (1 - 1e-9)·e^gamma·log log L (interval lower
bound, two nextafter steps down, then the margin — the margin exceeds the filter's
worst-case double rounding error by ~6 orders of magnitude, and log log is
increasing on the segment), so the filter over-flags but cannot miss a violation;
every flagged n is then decided by comparing the exact integer sigma(n) against an
outward-rounded mpmath interval enclosure of e^gamma·n·log log n at 80/120/200 bits,
with 'undecided' (never observed) a declared kill-criterion rather than a silent pass.
