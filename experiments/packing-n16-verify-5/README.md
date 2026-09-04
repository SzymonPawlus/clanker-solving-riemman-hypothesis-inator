# packing-n16-verify-5 — independent exact checker for n = 16 (worker V5)

Write-up and verdicts: [`problems/circle-packing-equilateral-triangle/attacks/n16-verification-5/README.md`](../../problems/circle-packing-equilateral-triangle/attacks/n16-verification-5/README.md).

Written from the problem statement (`problems/circle-packing-equilateral-triangle/README.md`) and
`RULES.md` §2 only. No code was read, imported, or adapted from `packing-n16-upper-2/` or any
other lane (problem `RULES.md` §3.2).

## One command

```sh
sh experiments/packing-n16-verify-5/verify.sh
```

Exit 0 iff every gate passes and every injected corruption is handled as required.
Stored output: [`verify.log`](./verify.log). Runtime ≈ 3 s, one core.

## Files

| file | what it does |
|---|---|
| `check_v5.py` | the checker. Exact `Fraction` + a $\mathbb{Q}(\sqrt3)$ ordered field with an exact `sign()`. Gates: G0 schema/exact-field hygiene, G1 the reduction $d = s - 2\sqrt3$, G2 all $\binom{16}{2}$ squared distances $\ge 4$, G3 closed-triangle containment in **two** independent encodings plus a randomised test of the squaring equivalence, G4 exact minimal enclosing side and tightness. |
| `attack_v5.py` | 14 adversarial cases: overlap by $10^{-12}$, exits across each of the three edges (**including both slanted ones**), inflated and deflated `side_length`, decimal and scientific-notation coordinate strings, the separation-1/2 rescale, a lying `coordinate_type`, a rigid translation, and a discrimination test against a sign-slip mutant checker. |
| `rigidity_v5.py` | contact graph, wall incidences, rattler, and the rigidity matrix rank by exact Gauss–Jordan **over the field $\mathbb{Q}(\sqrt3)$** — no SVD, no tolerance in the rank. Also reproduces the sibling lane's "isostatic" reading to explain it. |
| `verify.sh` | runs all three in order. |
| `verify.log` | recorded output of the above. |

## Determinism and dependencies

CPython 3.11.15, **standard library only** for every gate that decides anything (`fractions`,
`math.isqrt`, `re`, `json`, `itertools`). `numpy` 2.4.6 / `scipy` 1.17.1 are used **only** in the
side investigation reported in §5 of the write-up (comparing two float configurations) and decide
no reported result. The single randomised component — the containment-encoding equivalence sweep,
4000 points — is seeded with `20260822`.

Decimal magnitudes are rendered with an integer-`isqrt` routine, not floats: a double cannot
represent $s = 12.71362877415147158705\ldots$ past its 14th decimal, and a float rendering
produces a phantom $1.6\times10^{-13}$ disagreement with the certificate's own note.
