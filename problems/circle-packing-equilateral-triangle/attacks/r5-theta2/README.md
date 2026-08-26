# θ′, continued: the gain is exactly zero where it is needed

**Lower-bound (optimality-side) attack. No bound on `s(n)` or `d(n)` is established here.**

```
status:  numerical  — every solve, gain and table below
         sketch     — the criticality argument in §2 and the reading in §4
author:  claude (worker r5-theta2) for the instrument, sweep and analysis;
         manager for this write-up, 2026-08-24
issue:   #110, continuing attacks/r4-theta/ where its own "least sure of" pointed
code:    experiments/packing-r5-theta2/
kill:    KILL-CRITERION.md — see §3; the stated trigger did not fire, and a
         stronger obstruction was found instead
```

**Nothing here is assumable** (`RULES.md` §3).

> **Provenance.** The worker was terminated by a connection loss having committed four times, so
> the instrument, the 1132-solve sweep and its analysis script all survived. It never wrote this
> file; the manager wrote it from the committed analysis output.

---

## 0. Where this picks up

`attacks/r4-theta/` established (`numerical`/`sketch`, not assumable): `α ≤ ϑ′ ≤ χ̄` with both ends
`Θ(d²)`, so `d_{ϑ′}(n) = Θ(√n)` — **the right order**, unlike the moment hierarchy's bounded
`√(6(n−1)/n)`. It built a **one-sided instrument**: for finite `W ⊂ T_d`, a feasible kernel
restricts, so `ϑ′(G_d[W]) ≤ ϑ′(G_d)`, which upper-bounds the achievable ϑ′ floor against *every*
kernel of *every* degree with no SOS. Across 20 solves it never reached `n`; best gain
`ϑ′ − α = +0.447`; firing needs `+1`. Its stated "least sure of" was whether a **sharper witness
family** would fire the gate.

This lane answers that, with an independently written instrument (self-tested including exact
distance-2 ties at 60 dps).

## 1. The sweep: 1132 solves, 1129 converged

Best gain per witness family:

| family | best gain | witness | N | α | ϑ′ ≥ | χ̄_f |
|---|---:|:--|---:|---:|---:|---:|
| **R-ring** | **+0.6212** | `n11/ring/m23/R0.95` | 23 | 5 | 5.6212 | 5.7500 |
| PG-perturbed-grid | +0.5249 | `n16/pgrid/ref2/s0.25/1` | 55 | 10 | 10.5249 | — |
| CR-concentric | +0.5055 | `n11/conc/7+14/0.45,0.9` | 21 | 4 | 4.5055 | 4.6667 |
| RND-random | +0.3863 | `n12/rnd/N30/0` | 30 | 6 | 6.3863 | — |
| E-edge-ring | +0.3601 | `n16/edge/4/in0.4` | 12 | 7 | 7.3601 | 7.5000 |
| CF-corner-fan | +0.3601 | `n11/fan/2/[0,2,3.5]` | 18 | 7 | 7.3601 | 7.5000 |
| G-anchored-grid | −0.0000 | `n7/grid/ref1` | 6 | 6 | 6.0000 | — |

The ring family did beat `r4-theta`'s `+0.447`, reaching **`+0.6212`**. **Witnesses reaching
`ϑ′ ≥ n`: 0.**

Soundness control: the sandwich `α ≤ ϑ′ ≤ χ̄_f` was **violated on 0 of the 883 solves** where
`χ̄_f` was computed.

## 2. The finding: gain vanishes exactly at criticality

This is the part that matters, and it is a structural obstruction rather than a failed search.

A witness fires the gate at `n` only if `ϑ′(W) ≥ n`. Since `α(W) ≤ α(G_d) = n − 1`, firing requires
**gain ≥ 1 while `α(W) = n − 1`** — i.e. gain must appear *at criticality*. Bucketing all solves by
`α/(n−1)`:

| α/(n−1) | solves | max gain | mean gain |
|---|---:|---:|---:|
| 0.0–0.2 | 116 | +0.5365 | +0.0401 |
| 0.2–0.4 | 323 | **+0.6212** | +0.2328 |
| 0.4–0.6 | 430 | +0.6212 | +0.0948 |
| 0.6–0.8 | 164 | +0.5249 | +0.0285 |
| **0.8–1.0** | **96** | **−0.0000** | **−0.0000** |

> **Critical witnesses (`α = n−1`) in the sweep: 28. Maximum gain over all of them:
> `−0.000000`.**

So the gain is not merely too small at criticality — it is **exactly zero** there, across every
family tried, while reaching `+0.62` on witnesses far from critical. Every witness that gains is a
witness that cannot fire; every witness that could fire, gains nothing.

## 3. Kill-criterion

As written, the trigger was: *if no family exceeds the `+0.447` already observed after at least
three structurally different families, stop.* **That trigger did not fire** — the ring family
reached `+0.6212`.

But the criticality result in §2 is a **stronger negative than the trigger was designed to
detect**, and the honest response is to stop anyway rather than keep hunting families. The
instrument is one-sided; it can only detect weakness; and it now says the weakness sits exactly
where a firing witness would have to live.

## 4. Reading (`sketch`)

Two limits, both real:

1. **This bounds what the *witness* method can show, not what ϑ′ is.** The instrument upper-bounds
   the achievable floor; a null from it is evidence that no *finite witness* will fire, not that
   `ϑ′(G_d) < n`.
2. **Prong 2 — the actual SOS — is only barely begun.** `sos_theta.py` exists and at bidegree
   `m = 2` reproduces `ϑ′(G_2) = 3` and `ϑ′(G_{1.5}) = 1`, with a clean feasible/infeasible
   transition between `d = 2.4` (λ ≈ 25) and `d = 2.6` (infeasible). Block sizes at `m = 2` are
   tiny (`K = 6`, `τ₀ = 15`, 70 degree-4 equations). **It produced no ϑ′-derived floor for any
   open `n`.** So `r4-theta`'s central gap — no ϑ′ value anywhere — is *narrowed, not closed*.

Combined with `r4-theta`: ϑ′ has the right growth order and is **not** ceiling-bound like the
moment hierarchy, but no finite-witness route to firing it has been found, and the failure is now
localised to criticality rather than merely observed in aggregate.

## 5. Reproduce

```
cd experiments/packing-r5-theta2
python3 theta2_core.py --selftest     # instrument self-test, incl. exact distance-2 ties at 60 dps
python3 run_p1.py                     # the 1132-solve sweep
python3 analyse_p1.py                 # the tables above; committed at out_analysis.txt
python3 run_p2.py                     # prong-2 SOS at m = 2
```

Float SDP output throughout, hence `numerical`: **a relaxation value is a hypothesis about a
bound, never a bound.**
