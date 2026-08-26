# Two-family counting: the δ-window that the one-family count did not have

**Lower-bound (optimality) direction, and CONDITIONAL throughout. Nothing here proves EO(7), and
no bound on `s(n)` or `d(n)` is established.**

```
status:  numerical  — every count and scan below
         sketch     — the two-family counting statement and the reading in §4
author:  claude (worker r6-secondline), 2026-08-26; write-up by the manager after the worker
         was terminated by an account session limit mid-run
issue:   #110, round-6 execution of BRIEF-R6 §4 opening 1 (r5-eo7's own named next step)
code:    experiments/packing-r6-secondline/
kill:    KILL-CRITERION.md
```

**Nothing here is assumable** (`RULES.md` §3).

---

## 0. The question r5-eo7 left

`attacks/r5-eo7/` proved Theorem L (line-structured sets in `T(a')`, `a' < 6`, have `≤ 25` points)
and then refuted the only usable form of its bridging hypothesis: the counting bound is
**discontinuous at `δ = 0`** — 24 exactly-on-lines, 27 at `δ = 10⁻⁹` — because the whole gain came
from six chords being *exactly* integers. Its named next step: the relaxation counts along **one**
line direction and throws the second family away; use both.

**Target it set: beat `28 − 26 = 2` units of loss as `δ → 0⁺`.**

## 1. Control: r5-eo7's table reproduced independently

`out/repro_r5eo7_delta.json`, from independently written geometry: `δ = 0 → 24`, `10⁻⁹ → 27`,
`10⁻⁶ → 28`. **Matches r5-eo7 exactly.** The lane is measuring the same object.

## 2. The Jump Lemma, hit independently

At `a = 6.0` the two-family count returns **28** (`out/two_family.log`, refined and confirmed) —
the `Δ(7)` lattice witness sits in `T(6)`. So **no correct bound can be `< 26` at `a = 6`**, and the
"2-unit target *at* `a = 6`" was ill-posed.

This is `attacks/r6-interaction/`'s **Jump Lemma** arrived at from a completely different direction,
by a lane that did not read it: any valid `B` has `B(k−1) ≥ Δ(k)`. The work must happen strictly
below `a = 6`.

## 3. What the two-family count buys, strictly below 6

`out/interaction.log` — one-family bound `B` versus two-family bound `M`:

| `a` | one-family | two-family | gain |
|---|---:|---:|---:|
| 6.0 | 28 | 28 | 0 |
| 5.999999 | 24 | **22** | **2** |
| 5.99 | 24 | **22** | **2** |
| 5.9 | 23 | 22 | 1 |
| 5.5 | 21 | 21 | 0 |
| 5.0 | 21 | 21 | 0 |

And the δ-scan at `a = 5.99` (`η = 0.01`, `out/twofamily_scan_a5.99.json`) — the point of the whole
exercise:

| `δ/η` | 0 | 10⁻⁷ | 10⁻⁴ | 0.1 | 0.2 | 0.3 | 0.4 | 0.43 |
|---|---|---|---|---|---|---|---|---|
| two-family bound | 22 | 22 | 22 | 22 | 22 | 22 | 22 | 22 |
| `≤ 26`? | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

**The one-family count had a δ-window of exactly zero — it broke at `10⁻⁹`. The two-family count
holds at 22 across every `δ` the scan reached, out to `δ = 0.43 η`.** That is the qualitative change
the target was asking for: not a better constant, a window where there was none.

## 4. The tension I could not resolve, and will not paper over

The worker's own commit message for its final commit reads:

> two-family delta inflation constant Gamma>=4.31, window 0.19-0.23*eta vs one-family 0.866*eta

which describes the two-family window as **smaller** (`0.19–0.23 η`) than a one-family window of
`0.866 η` — the opposite ordering to §3, where the one-family count breaks immediately and the
two-family one survives to `0.43 η`.

The committed `out/delta_window.log` measures `≈ 0.86 η` and its companion file is named
`delta_window_one_family.json`, so the `0.866 η` figure is plausibly a *different quantity* (a
window for a different bound convention, or a worst case over more parameters) rather than a
contradiction. **The worker died before reconciling them and I am not going to guess.** Treat §3 as
what is measured and §4 as an open discrepancy for whoever picks this up; the two scans use
different scripts (`delta_window.py` vs `twofamily_scan.py`) and should be run against each other
first.

## 5. What this is not

- **Not EO(7), and not unconditional.** It is the *robustness* half of a conditional whose
  hypothesis (H) — that near-optimal 27-point configurations lie within `δ` of a line family — is
  **unproved**. What changed is that the conditional is no longer vacuous: it now tolerates
  `δ > 0`, so a forcing theorem supplying `δ ≲ 0.4 η` would be usable. Supplying it is the hard part
  and nothing here touches it.
- **Not covering `h`.** `r5-eo7`'s own "least sure of" stands: `h ≥ √3/2` is a hypothesis, not a
  consequence, for general line-structured sets.
- **Not cross-examined.** `numerical`/`sketch`, same model family.

## 6. Reproduce

```
cd experiments/packing-r6-secondline
python3 one_family.py       # reproduces r5-eo7's 24/27/28 table
python3 witness28.py        # the 28-point witness in T(6)
python3 interaction.py      # one-family vs two-family across a
python3 twofamily_scan.py   # the delta-window scan at a = 5.99
```
