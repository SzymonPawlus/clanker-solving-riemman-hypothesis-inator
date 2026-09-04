# packing-r3-qsqrt3 — exact, tight $\mathbb{Q}(\sqrt3)$ certificates for $n = 17, 24, 31$

**This directory establishes CONSTRUCTIONS (upper bounds), not optimality.** It certifies

$$s(17) \le 6 + 4\sqrt3, \qquad s(24) \le 8 + 4\sqrt3, \qquad s(31) \le 10 + 4\sqrt3$$

exactly, with tight certificates. It says **nothing** about lower bounds. All three $n$ are open
(`../../problems/circle-packing-equilateral-triangle/attacks/r3-approaches/README.md` §0.2), and
nothing here changes that.

**Status: `numerical`,** for every claim in this directory without exception. Under
[`problems/circle-packing-equilateral-triangle/RULES.md`](../../problems/circle-packing-equilateral-triangle/RULES.md)
§3 a packing earns `verified:review` only when an agent of a *different model family* writes its
own checker from the problem statement — not by running `check.py`. That has not happened. Nothing
here may be built on (repo `RULES.md` §3).

Round-3 approach **Y**. Issue: round-3 dispatch, worker `r3-qsqrt3`.
Write-up: [`../../problems/circle-packing-equilateral-triangle/attacks/r3-qsqrt3/README.md`](../../problems/circle-packing-equilateral-triangle/attacks/r3-qsqrt3/README.md).

---

## The question

Round-3 §0.2 observed that of the open cases $16 \le n \le 34$, exactly three have a best-known
value lying in $\mathbb{Q}(\sqrt3)$ with small integers, and that this makes them far cheaper to
certify exactly than $n = 16$ (whose only closed-form candidate is a PSLQ degree-10 minimal
polynomial). The question here is whether that observation cashes out: **can the published
best-known packings at $n = 17, 24, 31$ actually be written down exactly over $\mathbb{Q}(\sqrt3)$,
and can the resulting certificate be made *tight* rather than merely feasible?**

Tightness matters because the repo's existing certificate generator
(`../circle-packing-ls/certificate.py`) snaps to rationals and then *inflates* $s$ by about
$10^{-11}$ until the configuration becomes exactly feasible. That is honest but permanently loose:
`RULES.md` §2 requires a checker to report whether a certificate is tight, and a record claim
requires it. Before this directory, **no exact tight certificate existed for any open $n$.**

## The answer

Yes, for all three, and the certificates are exactly tight. Concretely:

| $n$ | $d = s - 2\sqrt3$ | $s$ | pts snapping to $\mathbb{Q}(\sqrt3)$ | rattlers | contacts at distance exactly 2 | pts on the boundary | tight |
|---:|---|---|---:|---:|---:|---:|:--|
| 17 | $6 + 2\sqrt3$ | $6 + 4\sqrt3$ | 16 / 17 | 1 | 26 | 11 | yes |
| 24 | $8 + 2\sqrt3$ | $8 + 4\sqrt3$ | 24 / 24 | 0 | 45 | 15 | yes |
| 31 | $10 + 2\sqrt3$ | $10 + 4\sqrt3$ | 30 / 31 | 1 | 59 | 18 | yes |

Every coordinate is an exact element of $\mathbb{Q}(\sqrt3)$ with small integer or half-integer
parts. All $\binom{n}{2}$ squared separations are $\ge 4$ and all containments hold in the closed
triangle, checked in exact arithmetic with no float anywhere in the decision path. The minimum
squared separation is **exactly 4** in all three cases.

**This reproduces the published record; it does not beat it** (`RULES.md` §4 — matching exactly is
the good outcome). `beats_record` is `"no"` in all three certificates.

## Method

1. **Closed forms re-derived against the published table** (`verify_closed_forms.py`). The
   Graham–Lubachevsky values tabulated in `../circle-packing-search/reference.py` agree with
   $6+4\sqrt3$, $8+4\sqrt3$, $10+4\sqrt3$ to within one unit in the last published significant
   figure. That is *evidence* the optima lie in $\mathbb{Q}(\sqrt3)$, not proof.
2. **Snap** (`snap.py`). The float configuration from `../circle-packing-ls/out/nNN.json` is
   rescaled by the conjectured $d$ and each coordinate snapped to the nearest
   $(p + q\sqrt3)/2$ with $|p|,|q| \le 80$. The script *proves* the snap is unambiguous rather
   than assuming it: distinct lattice values at that height differ by at least
   $1/(80(1+\sqrt3)) = 4.6\times10^{-3}$, while every residual observed is $\sim 10^{-15}$.
   Coordinates whose residual exceeds half that separation are flagged and **not** snapped —
   at $n = 17$ and $n = 31$ exactly one point each is flagged, and in both cases it is a rattler.
3. **Rattlers** (`rattler.py`). A rattler has strict slack in every constraint, so its free region
   is open; the optimiser's float position for it is arbitrary and (correctly) does not snap. Each
   is replaced by the simplest exactly-feasible point of its free region — $(5/2, 4)$ at $n = 17$,
   $(7, 0)$ at $n = 31$, both exact rationals. Problem `RULES.md` §5: rattlers are normal and are
   not "fixed"; moving one within its free region changes nothing about the packing's validity or
   its side length.
4. **Exact check** (`check.py`, on `qsqrt3.py`). Everything is $a + b\sqrt3$ with `Fraction`
   $a, b$; ordering is decided by the exact sign rule (compare $a^2$ with $3b^2$ when the signs
   differ), so no float is consulted in any accept/reject decision.
5. **Tightness.** The minimal enclosing side is computed exactly, not asserted. In the fixed
   placement $A=(0,0)$, $B=(d,0)$, $C=(d/2, d\sqrt3/2)$, the constraints $y \ge 0$ and
   $\sqrt3 x - y \ge 0$ do not involve $d$, and $\sqrt3(d - x) - y \ge 0 \iff d \ge x + y\sqrt3/3$.
   So $d_{\min} = \max_i (x_i + y_i\sqrt3/3)$, computed in exact arithmetic. All three certificates
   have $d_{\min}$ equal to the declared $d$ — genuinely tight, not inflated.
6. **Emit and re-verify** (`emit.py`, then `run_all.py`). Certificates are written in the schema
   of problem `RULES.md` §2, then **parsed back from disk as strings** and re-checked, so what is
   verified is the artifact rather than an in-memory object. A guard rejects any decimal string
   appearing in an exact field.

## Validation before assertion (`RULES.md` §6)

`validate.py` runs before anything is claimed:

- **Positive, from first principles:** the triangular lattice at $n = 3, 6, 10, 15, 21$ (settled
  cases, $d = 2(k-1)$) — built directly, not snapped. All feasible and tight at the known $d$.
- **Positive, whole pipeline:** $n = 12$, a **settled** case whose optimum $s(12) = 4 + 4\sqrt3$
  also lies in $\mathbb{Q}(\sqrt3)$, snapped by the same procedure. Feasible, tight, and matching
  the published optimum exactly. This is the end-to-end control: the pipeline reproduces a known
  answer before being pointed at an open case.
- **Negative controls, all four of which the checker must reject:** a point nudged $10^{-3}$ toward
  a contact neighbour; a point pushed $10^{-3}$ outside edge $BC$; the configuration declared at
  $d - 10^{-3}$; and the configuration declared at $d + 10^{-3}$, which must come back *feasible
  but not tight*. A checker that accepts everything verifies nothing.

## Reproduce

```
python3 run_all.py
```

**No dependencies. This runs to completion, exit 0, on a bare CPython with nothing installed**, and
`pyproject.toml` accordingly declares `dependencies = []`.

`run_all.py` runs one optional diagnostic, `verify_closed_forms.py`, which compares a published
float table against the closed forms and needs `mpmath`. It is **not** load-bearing, so when
`mpmath` is absent `run_all.py` prints a `SKIPPED (optional)` block saying exactly what did not run
and why, and then completes the whole exact certificate pipeline anyway. Every load-bearing check
uses stdlib `fractions.Fraction` only.

Verified both ways on 2026-09-04:

| environment | result |
|---|---|
| `/usr/bin/python3` (CPython 3.14.5, **no** mpmath/numpy/scipy/sympy installed) | exit 0; diagnostic reported as skipped; all three certificates re-verified from disk, exact and tight |
| venv with `mpmath` 1.3.0 | exit 0; diagnostic also runs and agrees with the published `m(n)` to 15 s.f. |

Runs in about 11 seconds. Originally developed under Python 3.11.15 with `mpmath` 1.3.0. The float
input is `../circle-packing-ls/out/nNN.json` (LS billiard + SLSQP, seed 20260818), read-only.

## Files

| File | What it is |
|---|---|
| `qsqrt3.py` | exact $\mathbb{Q}(\sqrt3)$ arithmetic, stdlib `Fraction`, exact sign/ordering |
| `configs.py` | the three exact configurations (and their provenance) |
| `check.py` | exact feasibility + containment + **tightness** checker |
| `validate.py` | solved-instance positive controls and negative controls |
| `verify_closed_forms.py` | step zero: closed forms vs. the published table |
| `snap.py` | float $\to \mathbb{Q}(\sqrt3)$ snap, with its own unambiguity proof |
| `rattler.py` | exact free-region placement of the one rattler at $n = 17$ and $n = 31$ |
| `emit.py` | writes `certificates/nNNN-r3-qsqrt3.json` in problem `RULES.md` §2 schema |
| `run_all.py` | the single reproduce command; also re-verifies the emitted files from disk |
| `certificates/` | the three certificates. **Deliberately not in `problems/*/results/`** — that directory takes only assumable claims, and these are `numerical`. |

## What would make this wrong

The exact check is self-contained and short, so the honest failure modes are not arithmetic:

1. **A convention error rather than a computation error.** If the triangle placement, the meaning
   of `side_length`, or the point-vs-circle formulation were read differently here than in the
   problem's `README.md`, every number above would be internally consistent and externally wrong.
   This is exactly what problem `RULES.md` §3's independent reimplementation is for.
2. **A misidentified rattler.** `snap.py` flags a point as unsnappable and `rattler.py` then treats
   it as free. If a flagged point were in fact a contact point whose true coordinates are of
   *higher* height in $\mathbb{Q}(\sqrt3)$ (or not in $\mathbb{Q}(\sqrt3)$ at all), the
   replacement would still yield a valid packing — `check.py` verifies the replacement exactly —
   but the configuration would not be the published one. The construction claim survives; the
   claim "this is the published configuration" would not.
3. **The closed forms could be wrong.** §1 above is a 15-significant-figure agreement, nothing
   more. If the true optima are not $6+4\sqrt3$ etc., these remain valid upper bounds; they would
   simply not be the record. Nothing downstream depends on the identification.
