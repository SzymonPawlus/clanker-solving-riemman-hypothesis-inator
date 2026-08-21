# `packing-exact-algebraic` — exact algebraic certificates for triangle packings

**Claim type: construction (upper bounds) only. Status `numerical` for the search, `sketch` for
the closed forms. Nothing here is an optimality proof.**

- Issue: [#74](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/74)
- Write-up and derivations:
  [`../../problems/circle-packing-equilateral-triangle/attacks/exact-algebraic-constructions/`](../../problems/circle-packing-equilateral-triangle/attacks/exact-algebraic-constructions/)
- Author: `claude` (Claude Opus 5), 2026-08-19

## Reproduce

```sh
sh run.sh
```

Runs in a few seconds. Steps 1–4 use **only the Python standard library**. Step 5 (the candidate
search) is optional and is the only part that needs numpy/scipy.

## Files

| File | What it is | Depends on |
|---|---|---|
| `quadfield.py` | exact arithmetic in $\mathbb{Q}(\sqrt{p_1},\dots,\sqrt{p_k})$ over `Fraction` | stdlib |
| `exact_check.py` | the certificate checker — parses, verifies feasibility, measures tightness | stdlib |
| `construct.py` | emits the certificates | stdlib |
| `test_exact.py` | tests, including the negative controls | stdlib |
| `search.py` | multi-start SLSQP candidate generator (hypotheses only) | numpy 2.4.6, scipy 1.17.1 |

Version pins: python3 ≥ 3.10, numpy 2.4.6, scipy 1.17.1, sympy 1.14.0. Search seed `20260819`.
sympy was used **only** to solve the $n = 8$ contact system while deriving it by hand; no shipped
artifact imports sympy, and the checker does not trust it — the closed form is re-verified from
scratch in `quadfield.py`.

## Why the arithmetic is exact rather than very precise

An element is a $\mathbb{Q}$-combination $\sum_S c_S \sqrt{\prod S}$ over sets $S$ of distinct
primes. Two properties make every decision the checker takes a proof rather than an estimate:

1. **Equality is syntactic.** Square roots of distinct squarefree integers are linearly
   independent over $\mathbb{Q}$, so an element is zero exactly when every stored coefficient is
   zero. No tolerance is involved in deciding `== 0`.
2. **Sign is decided by refinement that provably halts.** For a nonzero element, each $\sqrt m$ is
   bracketed by rationals $\lfloor\sqrt{m\,4^p}\rfloor/2^p \le \sqrt m \le (\lfloor\sqrt{m\,4^p}\rfloor+1)/2^p$
   and $p$ doubles until the resulting rational interval excludes $0$. It terminates because the
   value is nonzero, and the bracket is a rigorous enclosure, so the sign returned is correct.

Floats are refused by construction: `QF` raises on any attempt to combine with a float, and the
certificate parser rejects decimal literals outright (problem `RULES.md` §2 bans them).

## What the checker checks

Conventions are taken verbatim from the problem's `RULES.md` §2 and not reinterpreted: point
formulation, triangle at $A=(0,0)$, $B=(d,0)$, $C=(d/2, d\sqrt3/2)$, no search over rigid motions,
`side_length` means $s$, all inequalities non-strict.

Containment is re-derived here rather than copied: with $A,B,C$ counter-clockwise, $P=(x,y)$ is in
the closed triangle iff $y \ge 0$, $y \le \sqrt3\,x$, and $y \le \sqrt3\,(d-x)$. Only the last
involves $d$ and it is increasing in $d$, so the **exact minimal enclosing side** for a fixed point
set in this fixed position is

$$d_{\min} \;=\; \max_i \left( x_i + \frac{y_i}{\sqrt 3} \right),$$

and a certificate is *tight* iff $d = d_{\min}$. Tightness is what stops an inflated $s$ from
passing: containment alone would happily certify $s(3) \le 10^6$.

## Negative controls

`test_exact.py` deliberately tries to get bad certificates past the checker. It must reject: a
pair at distance $199/100 < 2$; a point at $y = -1/1000$; a $d$ too small to contain the points; a
declared `point_triangle_side` inconsistent with $s - 2\sqrt3$; and a certificate that *declares*
itself tight when it is not. It must **accept but mark not-tight** an inflated side length, since
that is an honest (if weak) upper bound. A checker that passed everything would pass this
directory's certificates too, which is why these tests exist.

## Independence

Written from the problem statement in `README.md` and the conventions in `RULES.md` §2. The
checker in PR #16 / `experiments/circle-packing-checker` and the `cpbnb` tree were **not** read,
imported, or adapted — problem `RULES.md` §3 asks for independent reimplementation, and a second
checker is only worth anything if it is genuinely second.

As a by-product this checker independently confirms the two certificates already on `main`
(`results/n003-lean-corners.json`, `results/n006-lean-t3-lattice.json`): both pass and both are
tight (step 4 of `run.sh`).
