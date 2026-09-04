# Two-family counting: the δ-window, and the refutation of the comparison I drew from it

**Lower-bound (optimality) direction, and CONDITIONAL throughout. Nothing here proves EO(7), and
no bound on `s(n)` or `d(n)` is established.**

```
status:  numerical  — every count and scan below
         sketch     — the two-family counting statement
         refuted    — the comparative claim "a two-family delta-window where the
                      one-family count had none" (§4). Withdrawn 2026-09-04 after
                      this lane's own scripts were run against each other.
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

What this table does and does not say: the two-family scan **did not break** anywhere it was run.
`δ = 0.43 η` is where the scan *stopped*, not where the bound *failed*. It is a truncation point,
and the distinction is the whole subject of §4.

## 4. The comparison is REFUTED — two different quantities were being called "the δ-window"

**Status of the comparative claim in the first version of this file — "a window where there was
none" — is `refuted`.** It was withdrawn, not weakened. `RULES.md` §0: a documented refutation is a
success, and this one was found by this lane's own committed scripts.

### 4.1 The two quantities, defined

Two different things in this directory were both being written "the δ-window". They are not
comparable, and they order in **opposite** directions.

**`W_scan` — the *measured* breakpoint of a counting scan.** Produced by `one_family.py`,
`delta_window.py` and `twofamily_scan.py`. Definition: the largest `δ` at which a numerically
evaluated counting scan — cap `floor(ℓ^δ / √(1 − 4δ²)) + 1`, swept over a *finite grid* of family
orientations `φ`, offsets `h` and rotations `θ` — still returns a bound `≤` target. It is an
observed property of one cap formula on one grid. **It controls nothing.** It is a diagnostic of
the counting step's numerical behaviour, not a bound on anything.

**`W_cont` — the *provable* containment window.** Produced by `twofamily_delta.py`, derivation in
its docstring. Definition: if every point of `P` lies within `δ` of the assumed line family or
families, then `π` is injective and `P` is contained in an inflated triangle, giving
`|P| ≤ M(a + Γδ)`. For that inflated side to stay below `6` — where the Jump Lemma of §2 makes the
count `28` and no bound below `26` can hold — one needs `Γδ ≤ η = 6 − a`, i.e.

    W_cont  =  η / Γ.

**`W_cont` is the load-bearing quantity.** It is the number a forcing theorem must supply `δ` below
for the conditional of §5 to be usable at all. `W_scan` is evidence about the scan; `W_cont` is the
hypothesis budget.

### 4.2 On `W_cont` the ordering is the opposite of what §3 suggested

Reproduced from `out/twofamily_delta.json` (rerun 2026-09-04, values identical):

| | `Γ` | `W_cont = η/Γ` |
|---|---:|---:|
| one family | `2/√3 = 1.1547` | **`0.8660 η`** |
| two families, isotropic floor | `2√3 = 3.4641` | `0.2887 η` |
| two families, best over all direction pairs (`φ₁=0°, φ₂=90°`) | `4.3094` | **`0.2321 η`** |
| two families, best hexagonal orientation | `4.6188` | `0.2165 η` |
| two families, the extremal `M=22` lattice (`φ = 29.33°`) | `5.3330` | `0.1875 η` |

**Two families give a strictly *smaller* provable window than one**, by roughly `3.7×`. This is not
a defect of the implementation and it is not tunable: `δ`-slack along two independent normals
inflates the containing triangle in more directions than `δ`-slack along one, so `Γ` can only grow
when a second family is added. `Γ ≥ 2√3` is proved in the docstring; the sweep only locates the
minimum.

So the second family buys a **better count** at fixed `a` (§3: 22 against 24, a real gain) while
buying a **worse δ-budget**. Those are the two halves of the same trade, and the first version of
this file reported only the half that flattered the lane.

### 4.3 And the "exactly zero" one-family window was an artifact

The claim that the one-family count "had a δ-window of exactly zero — it broke at `10⁻⁹`" is
**false**, and this directory's own `delta_window.py` says why in its docstring: `r5-eo7` ran its
δ-scan at `a = 6` with the cap `ceil(ℓ^δ / √(1 − 4δ²))`, whose `1` fixes the separation at exactly
`1`. But `ceil(·)` is only a valid cap when the separation is *strictly* `> 1`, which is precisely
what `a' < 6` buys after rescaling. So the `δ = 0` row and the `δ > 0` rows were computed under
**different separations**, and the 24 → 27 jump between them is that inconsistency — not a property
of the counting step.

Measured consistently at `a = 6 − η` with a cap valid for every `η ≥ 0`
(`out/delta_window_one_family.json`, reproduced 2026-09-04):

| `η` | `W_scan`/`η` (coarse) | bound at `δ=0` | fine-grid bound at the window | fine-grid at `1.25×` |
|---|---:|---:|---:|---:|
| 0.1 | 0.5815 | 23 | **27** | 27 |
| 0.03 | 0.8659 | 24 | **27** | 27 |
| 0.01 | 0.8643 | 24 | 26 | 27 |
| 0.003 | 0.8626 | 24 | 26 | 27 |

The one-family `W_scan` is **positive** — around `0.86 η` — not zero. So "a window where there was
none" is false in both readings available to it: the one-family window is not zero, and on the only
quantity that controls a bound the two-family window is the *smaller* of the two.

### 4.4 Three further cautions, recorded rather than buried

1. **`W_scan` is itself unreliable, in the unsafe direction.** The `fine-grid bound at the window`
   column above is `27 > 26` in the first two rows: the window endpoint located by the coarse binary
   search does **not** survive refinement. The coarse grid *overestimates* the window. Do not build
   on these numbers even as evidence.
2. **`δ = 0.43 η` is a truncation, not a breakpoint** (§3). Comparing a point where a search *was
   stopped* against a point where another search *broke* is the failed-search-as-evidence error that
   `RULES.md` §0 exists for. The two-family scan establishes `W_scan ≥ 0.43 η` and nothing more; no
   two-family breakpoint has been measured at all.
3. **The `delta_window.py` run is incomplete.** Its `ETAS` list has seven entries and the committed
   JSON has four; the worker was terminated mid-run. `η = 3·10⁻⁴` and `10⁻⁴` were never measured.

### 4.5 What survives

The §3 count itself — one-family `B` versus two-family `M` at fixed `a`, 24 against 22 at
`a = 5.99` — is unaffected by any of this and remains `numerical`. What is withdrawn is the
*comparative robustness* reading built on top of it. The lane's honest summary is: **the second
family improves the count and degrades the δ-budget, and the target it set itself ("a window where
there was none") was not met, because the thing it was measured against did not exist.**

## 5. What this is not

- **Not EO(7), and not unconditional.** It is the *robustness* half of a conditional whose
  hypothesis (H) — that near-optimal 27-point configurations lie within `δ` of a line family — is
  **unproved**. After §4 the usable budget is the provable one: a forcing theorem would have to
  supply `δ ≤ W_cont ≈ 0.23 η` for the two-family route, which is a **tighter** requirement than the
  `≈ 0.87 η` the one-family route would need. Supplying either is the hard part and nothing here
  touches it. The earlier reading — that the conditional had become newly non-vacuous — is
  `refuted`; see §4.
- **Not covering `h`.** `r5-eo7`'s own "least sure of" stands: `h ≥ √3/2` is a hypothesis, not a
  consequence, for general line-structured sets.
- **Not cross-examined.** `numerical`/`sketch`, same model family.

## 6. Reproduce

**Dependencies.** This lane is a floating-point scan and genuinely requires `numpy`; it is
declared in `experiments/packing-r6-secondline/pyproject.toml`, not advertised as stdlib-only.
Run with `numpy` 2.5.2 on CPython 3.14.5.

```
cd experiments/packing-r6-secondline
python3 -m venv .venv && .venv/bin/pip install 'numpy>=1.26'

.venv/bin/python one_family.py       # reproduces r5-eo7's 24/27/28 table
.venv/bin/python witness28.py        # the 28-point witness in T(6)
.venv/bin/python interaction.py      # one-family vs two-family across a
.venv/bin/python twofamily_scan.py   # the W_scan scan at a = 5.99 (truncated at 0.43 eta)

# the two scripts whose disagreement §4 resolves -- run BOTH before citing either
.venv/bin/python twofamily_delta.py  # W_cont: the provable containment window (seconds)
.venv/bin/python delta_window.py     # W_scan for one family, measured consistently (slow)
```

`twofamily_delta.py` is pure geometry and reruns in under a second; its output was reproduced
exactly on 2026-09-04. `delta_window.py` sweeps fine grids and the committed run is **incomplete**
(4 of its 7 `ETAS` rows) — see §4.4.
