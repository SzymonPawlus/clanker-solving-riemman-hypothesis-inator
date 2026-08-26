# packing-r5-n17 — independent audit of the `n = 17 / 24 / 31` disagreement

**Question.** `attacks/r4-famcert/README.md` §1 flags that the `r3-qsqrt3` exact certificate for
`n = 17` and the `r4-famcert` four-grain generator at `j = 3` share only 12 of 17 points, at the
same `s = 6 + 4√3`, and that "one rattler explains one differing point, not five". Are both
packings valid? Are they the same packing? What actually explains the difference — at `n = 17`,
and at `n = 24` (reported identical) and `n = 31` (reported 30/31)?

**Method.** Everything rebuilt from scratch: my own `Q(√3)` arithmetic (`q3.py`, `Fraction`
pairs, exact sign rule — no float appears in any accept/reject decision), my own exact-expression
parser (`parse_exact.py`), my own checker written from the problem `README.md`/`RULES.md` §2
(`checker.py`), and my own transcription of the four-grain generator from the *docstring spec*
of `experiments/packing-r4-famcert/generator.py` (`famgen.py`), not from its code.

`famgen.py` is confirmed to emit the same point sets as the original generator for `j = 0..5`
(that cross-check is in the report, not in `run_all.py`); everything else is independent.

**Result.** Both configurations are feasible, tight and minimally-spaced at all three `n`.
`n = 24` is identical; `n = 31` differs by exactly one rattler sliding on the bottom edge;
`n = 17` is two genuinely distinct packings at the same side. Full verdict in
`../../problems/circle-packing-equilateral-triangle/attacks/r5-n17/README.md`.

## Reproduce

```
cd experiments/packing-r5-n17 && python3 run_all.py
```

Deterministic, exact, no seeds, no network, ~40 s. Python 3.11.15, `sympy` 1.14.0 (used only to
parse exact expression strings; all arithmetic afterwards is stdlib `Fraction`). Transcript
committed at `out/run_all.txt`; per-step transcripts at `out/*.txt`, machine-readable audit at
`out/audit.json`.

## Files

| file | what it is |
|---|---|
| `q3.py` | exact `Q(√3)`: add/sub/mul/inv, exact sign, 2×2 inverse |
| `parse_exact.py` | `"a + b*sqrt(3)"` → `Q3`; rejects decimals and anything outside `Q(√3)` |
| `checker.py` | feasibility, containment, exact minimal enclosing side, contacts, boundary, rattlers, exact free-radius bracket |
| `selftest.py` | **validation gate**: `n = 3, 4, 6, 10` proven optima + 5 negative controls |
| `famgen.py` | independent transcription of the four-grain generator |
| `symmetry.py` | the 6 exact isometries of the fixed triangle, as affine maps over `Q(√3)` |
| `audit.py` | the main comparison at `n = 17, 24, 31` |
| `diffs.py` | which points differ; per-point contacts/walls/mobility; degree histograms |
| `rigidity.py`, `rigid_run.py` | exact rank of the rigidity matrix (contacts + active walls); exact slide intervals |
| `stab.py` | symmetry stabiliser of each configuration |
| `n31_seg.py` | exact endpoints of the `n = 31` rattler segment and the `n = 17` free disc |
| `famtable.py` | independent re-run of the famcert Gate-1/Gate-2 table, `j = 0..7` |

## Validation gate (runs first, `selftest.py`)

Proven optima accepted and reported tight: `n = 3` (`d = 2`), `n = 4` (`d = 2√3`), `n = 6`
(`d = 4`), `n = 10` (`d = 6`). Negative controls: overlap → rejected; `s` deflated by 1 →
rejected; `s` **inflated** by 1 → accepted but reported **not tight**; point below `AB` →
rejected; duplicate point → rejected. Rigidity code has its own controls (`Δ(3)` lattice → kernel
0; one free point in a big triangle → kernel 2).
